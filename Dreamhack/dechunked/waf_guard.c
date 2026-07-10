/*
 * waf_guard - reconstructed from reverse engineering /mnt/user-data/uploads/waf_guard
 *
 * Original binary: stripped x86-64 ELF PIE, ~14KB, dynamically linked against libc.
 * Behavior recovered via objdump/readelf static analysis (no execution required):
 *
 *   - Forking TCP reverse proxy: accept() -> fork() -> child relays client<->upstream.
 *   - Command line: `waf_guard [LISTEN_HOST LISTEN_PORT UPSTREAM_HOST UPSTREAM_PORT]`
 *     With 0 extra args, defaults to listen 0.0.0.0:8080, upstream 127.0.0.1:18080.
 *   - SIGCHLD is reaped via sigaction(SA_NOCLDWAIT-style waitpid loop), SIGPIPE ignored.
 *   - Only the CLIENT -> UPSTREAM direction is content-inspected. Each recv() chunk
 *     (up to 4096 bytes) is checked against a blocklist of substrings; on a match the
 *     connection is torn down instead of relayed. A 14-byte carry-over window is kept
 *     across recv() calls so a signature can't be smuggled by splitting it over two
 *     TCP segments/packets.
 *   - The blocklist itself is stored in .rodata as 12 entries of the form
 *     [1-byte length][up to 16 bytes, each XOR 0xA7]. Decoding it yields:
 *         {{  {%  %}  {#  #}  __  config  request  class  mro  subclasses  flag
 *     i.e. a Jinja2/Flask SSTI (server-side template injection) blocklist that also
 *     blocks the __class__ / __mro__ / __subclasses__ sandbox-escape chain and the
 *     literal word "flag".
 *
 * This file is a clean re-implementation with the same observable behavior; it does
 * not contain any code copied from the binary (there is no source to copy - it's a
 * stripped executable). It's organized as a straightforward line-by-line match to
 * the disassembly for auditability.
 */

#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define DEFAULT_LISTEN_HOST   "0.0.0.0"
#define DEFAULT_LISTEN_PORT   8080
#define DEFAULT_UPSTREAM_HOST "127.0.0.1"
#define DEFAULT_UPSTREAM_PORT 18080

#define RECV_CHUNK   4096   /* 0x1000, matches the stack buffer size in the binary */
#define CARRY_MAX    15     /* longest blocklist entry ("subclasses") is 10 bytes;
                                the binary keeps up to 14 bytes of carry (min(len-1,14)) */
#define BACKLOG      64

/* ---- blocklist, obfuscated exactly as stored in the binary's .rodata (XOR 0xA7) ---- */
typedef struct {
    unsigned char len;
    unsigned char data[16]; /* XOR 0xA7 encoded */
} pattern_t;

static const pattern_t BLOCKLIST[] = {
    {2,  {0xdc,0xdc}},                                              /* {{ */
    {2,  {0xdc,0x82}},                                              /* {% */
    {2,  {0x82,0xda}},                                              /* %} */
    {2,  {0xdc,0x84}},                                              /* {# */
    {2,  {0x84,0xda}},                                              /* #} */
    {2,  {0xf8,0xf8}},                                              /* __ */
    {6,  {0xc4,0xc8,0xc9,0xc1,0xce,0xc0}},                          /* config */
    {7,  {0xd5,0xc2,0xd6,0xd2,0xc2,0xd4,0xd3}},                     /* request */
    {5,  {0xc4,0xcb,0xc6,0xd4,0xd4}},                               /* class */
    {3,  {0xca,0xd5,0xc8}},                                         /* mro */
    {10, {0xd4,0xd2,0xc5,0xc4,0xcb,0xc6,0xd4,0xd4,0xc2,0xd4}},      /* subclasses */
    {4,  {0xc1,0xcb,0xc6,0xc0}},                                    /* flag */
};
#define N_PATTERNS (sizeof(BLOCKLIST) / sizeof(BLOCKLIST[0]))

/* Deobfuscate blocklist entry `idx` into `out` (caller-supplied, >= 16 bytes). Returns length. */
static int pattern_get(int idx, unsigned char *out) {
    const pattern_t *p = &BLOCKLIST[idx];
    for (int i = 0; i < p->len; i++)
        out[i] = p->data[i] ^ 0xA7;
    return p->len;
}

/* naive substring scan: does buf[0..len) contain any blocklisted pattern anywhere? */
static int contains_blocked_pattern(const unsigned char *buf, size_t len) {
    unsigned char pat[16];
    for (size_t start = 0; start < len; start++) {
        for (size_t p = 0; p < N_PATTERNS; p++) {
            int plen = pattern_get((int)p, pat);
            if (plen == 0) return 1; /* defensive; binary treats len==0 as match */
            if (start + (size_t)plen > len) continue;
            if (memcmp(buf + start, pat, plen) == 0)
                return 1;
        }
    }
    return 0;
}

/* per-direction filter state: carries trailing bytes across recv() calls */
typedef struct {
    unsigned char carry[CARRY_MAX];
    size_t carry_len;
} filter_state_t;

/*
 * Combine leftover carry + newly received bytes, run the blocklist scan over the
 * combined window, then keep the trailing bytes as the new carry for next time.
 * Returns 0 = clean (forward it), 1 = blocked.
 */
static int filter_chunk(filter_state_t *st, const unsigned char *new_data, size_t new_len) {
    unsigned char scratch[CARRY_MAX + RECV_CHUNK];

    if (st->carry_len + new_len > sizeof(scratch)) return 1; /* defensive bound check */

    memcpy(scratch, st->carry, st->carry_len);
    memcpy(scratch + st->carry_len, new_data, new_len);
    size_t total = st->carry_len + new_len;

    if (contains_blocked_pattern(scratch, total))
        return 1;

    size_t keep = total < (CARRY_MAX - 1) ? total : (CARRY_MAX - 1);
    memcpy(st->carry, scratch + (total - keep), keep);
    st->carry_len = keep;
    return 0;
}

/* ---------------------------------------------------------------------- */

static uint16_t hbo_to_nbo16(uint16_t v) { return htons(v); }

static int parse_port(const char *s) {
    char *end = NULL;
    long v = strtol(s, &end, 10);
    if (end == s || *end != '\0') return -1;
    if (v < 1 || v > 65535) return -1;
    return (int)v;
}

static void usage(const char *argv0) {
    fprintf(stderr, "usage: %s [LISTEN_HOST LISTEN_PORT UPSTREAM_HOST UPSTREAM_PORT]\n", argv0);
}

static void reap_children(int signo) {
    (void)signo;
    while (waitpid(-1, NULL, WNOHANG) > 0) { }
}

static int make_listen_socket(const char *host, int port) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) { perror("socket"); return -1; }

    int one = 1;
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)) < 0) {
        perror("setsockopt");
        close(fd);
        return -1;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = hbo_to_nbo16((uint16_t)port);
    if (inet_pton(AF_INET, host, &addr.sin_addr) != 1) {
        fwrite("invalid listen host\n", 1, 20, stderr);
        close(fd);
        return -1;
    }

    if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(fd);
        return -1;
    }
    if (listen(fd, BACKLOG) < 0) {
        perror("listen");
        close(fd);
        return -1;
    }
    return fd;
}

static int connect_upstream(const char *host, int port) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = hbo_to_nbo16((uint16_t)port);
    if (inet_pton(AF_INET, host, &addr.sin_addr) != 1) {
        close(fd);
        return -1;
    }
    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(fd);
        return -1;
    }
    return fd;
}

/* send(): retry on EINTR, loop until all bytes are written */
static int send_all(int fd, const unsigned char *buf, size_t len) {
    size_t sent = 0;
    while (sent < len) {
        ssize_t n = send(fd, buf + sent, len - sent, MSG_NOSIGNAL);
        if (n < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        if (n == 0) return -1;
        sent += (size_t)n;
    }
    return 0;
}

/*
 * Bidirectional relay for one accepted connection.
 * client_fd  <-> upstream_fd
 * Only data flowing client -> upstream is passed through the WAF filter.
 */
static void relay(int client_fd, int upstream_fd) {
    filter_state_t client_to_upstream_state = {0};
    unsigned char buf[RECV_CHUNK];

    for (;;) {
        struct pollfd fds[2];
        fds[0].fd = client_fd;   fds[0].events = POLLIN; fds[0].revents = 0;
        fds[1].fd = upstream_fd; fds[1].events = POLLIN; fds[1].revents = 0;

        int pr = poll(fds, 2, -1);
        if (pr < 0) {
            if (errno == EINTR) continue;
            return;
        }

        if (fds[0].revents & POLLIN) {
            ssize_t n = recv(client_fd, buf, sizeof(buf), 0);
            if (n <= 0) return;

            if (filter_chunk(&client_to_upstream_state, buf, (size_t)n))
                return; /* blocked pattern -> drop connection */

            if (send_all(upstream_fd, buf, (size_t)n) < 0) return;
        }

        if (fds[1].revents & POLLIN) {
            ssize_t n = recv(upstream_fd, buf, sizeof(buf), 0);
            if (n <= 0) return;
            if (send_all(client_fd, buf, (size_t)n) < 0) return;
        }
    }
}

int main(int argc, char **argv) {
    const char *listen_host, *upstream_host;
    int listen_port, upstream_port;

    if (argc != 1 && argc != 5) {
        usage(argv[0]);
        return 2;
    }

    if (argc == 5) {
        listen_host = argv[1];
        listen_port = parse_port(argv[2]);
        upstream_host = argv[3];
        upstream_port = parse_port(argv[4]);
        if (listen_port < 0 || upstream_port < 0) {
            usage(argv[0]);
            return 2;
        }
    } else {
        listen_host = DEFAULT_LISTEN_HOST;
        listen_port = DEFAULT_LISTEN_PORT;
        upstream_host = DEFAULT_UPSTREAM_HOST;
        upstream_port = DEFAULT_UPSTREAM_PORT;
    }

    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = reap_children;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_NOCLDSTOP;
    sigaction(SIGCHLD, &sa, NULL);
    signal(SIGPIPE, SIG_IGN);

    int listen_fd = make_listen_socket(listen_host, listen_port);
    if (listen_fd < 0) return 2;

    fprintf(stderr, "[+] WAF listening on %s:%d\n", listen_host, listen_port);
    fprintf(stderr, "[+] upstream app at %s:%d\n", upstream_host, upstream_port);

    for (;;) {
        int client_fd = accept(listen_fd, NULL, NULL);
        if (client_fd < 0) {
            if (errno == EINTR) continue;
            perror("accept");
            close(listen_fd);
            return 2;
        }

        int upstream_fd = connect_upstream(upstream_host, upstream_port);
        if (upstream_fd < 0) {
            close(client_fd);
            continue;
        }

        pid_t pid = fork();
        if (pid < 0) {
            close(client_fd);
            close(upstream_fd);
            continue;
        }

        if (pid == 0) {
            /* child: handle this one connection, then exit */
            close(listen_fd);
            relay(client_fd, upstream_fd);
            close(client_fd);
            close(upstream_fd);
            return 0;
        }

        /* parent: this connection belongs to the child now */
        close(client_fd);
        close(upstream_fd);
    }
}