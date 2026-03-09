#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *f = fopen("/flag.txt", "r");
    if (!f) {
        perror("fopen");
        return 1;
    }

    char buf[256];
    if (!fgets(buf, sizeof(buf), f)) {
        perror("fgets");
        return 1;
    }
    fclose(f);

    puts(buf);
    return 0;
}
