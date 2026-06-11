#!/usr/bin/env python3
import argparse
import collections
import hashlib
import os
import struct

# MAVLink2 packet:
# fd len incompat compat seq sysid compid msgid[3] payload checksum[2] signature[13]
# signature = sha256(secret_key || packet_without_signature || link_id_timestamp[7])[:6]

FLAG = "CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}"


def read_pcap_packets(path):
    data = open(path, "rb").read()
    if len(data) < 24:
        raise ValueError("pcap too short")
    magic = data[:4]
    if magic == b"\xd4\xc3\xb2\xa1":
        endian = "<"       # little-endian, usec
    elif magic == b"\xa1\xb2\xc3\xd4":
        endian = ">"
    elif magic == b"\x4d\x3c\xb2\xa1":
        endian = "<"       # little-endian, nsec
    elif magic == b"\xa1\xb2\x3c\x4d":
        endian = ">"
    else:
        raise ValueError("not classic pcap")

    off = 24
    while off + 16 <= len(data):
        ts_sec, ts_frac, incl_len, orig_len = struct.unpack_from(endian + "IIII", data, off)
        off += 16
        pkt = data[off:off + incl_len]
        off += incl_len
        yield ts_sec + ts_frac / 1_000_000, pkt


def udp_payloads_from_ethernet(frame):
    if len(frame) < 14:
        return
    eth_type = struct.unpack("!H", frame[12:14])[0]
    off = 14
    if eth_type == 0x8100 and len(frame) >= 18:  # VLAN
        eth_type = struct.unpack("!H", frame[16:18])[0]
        off = 18
    if eth_type != 0x0800 or len(frame) < off + 20:  # IPv4 only
        return
    ihl = (frame[off] & 0x0f) * 4
    proto = frame[off + 9]
    if proto != 17 or len(frame) < off + ihl + 8:  # UDP
        return
    uoff = off + ihl
    sport, dport, ulen, _ = struct.unpack("!HHHH", frame[uoff:uoff + 8])
    yield sport, dport, frame[uoff + 8:uoff + ulen]


def mavlink2_frames(buf):
    i = 0
    while True:
        j = buf.find(b"\xfd", i)
        if j < 0:
            break
        if j + 10 > len(buf):
            break
        plen = buf[j + 1]
        signed = buf[j + 2] & 1
        total = 10 + plen + 2 + (13 if signed else 0)
        if j + total <= len(buf):
            yield buf[j:j + total]
            i = j + total
        else:
            i = j + 1


def signature_valid(pkt, key):
    if not (pkt[2] & 1):
        return False
    sig = pkt[-13:]
    want = hashlib.sha256(key + pkt[:-13] + sig[:7]).digest()[:6]
    return want == sig[7:]


def decode_gps_raw_int(pkt):
    msgid = pkt[7] | (pkt[8] << 8) | (pkt[9] << 16)
    if msgid != 24:
        return None
    plen = pkt[1]
    payload = pkt[10:10 + plen]
    if len(payload) < 30:
        return None
    sysid = pkt[5]
    seq = pkt[4]
    time_usec = struct.unpack_from("<Q", payload, 0)[0]
    lat = struct.unpack_from("<i", payload, 8)[0] / 1e7
    lon = struct.unpack_from("<i", payload, 12)[0] / 1e7
    alt = struct.unpack_from("<i", payload, 16)[0] / 1000
    fix_type = payload[28]
    sats = payload[29]
    return {"sysid": sysid, "seq": seq, "time_usec": time_usec,
            "lat": lat, "lon": lon, "alt": alt, "fix": fix_type, "sats": sats}


def plot(points, outdir):
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"[!] matplotlib unavailable, skipping plots: {e}")
        return

    by_sys = collections.defaultdict(list)
    for p in points:
        by_sys[p["sysid"]].append(p)
    for arr in by_sys.values():
        arr.sort(key=lambda x: x["time_usec"])

    # Combined mission drawing.
    plt.figure(figsize=(16, 5))
    for sysid in sorted(by_sys):
        xs = [p["lon"] for p in by_sys[sysid]]
        ys = [p["lat"] for p in by_sys[sysid]]
        plt.plot(xs, ys, ".-", markersize=2, linewidth=0.7)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.title("Authenticated MAVLink GPS_RAW_INT paths only")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "valid_paths.png"), dpi=200)

    # Per sysid panels, useful for reading the text cleanly.
    n = len(by_sys)
    cols = 5
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(18, 3.2 * rows))
    axes = axes.ravel()
    for ax in axes:
        ax.axis("off")
    for idx, sysid in enumerate(sorted(by_sys)):
        arr = by_sys[sysid]
        xs = [p["lon"] for p in arr]
        ys = [p["lat"] for p in arr]
        axes[idx].plot(xs, ys, ".-", markersize=2.5, linewidth=0.8)
        axes[idx].set_aspect("equal", adjustable="box")
        axes[idx].set_title(f"sysid {sysid}")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "per_sysid.png"), dpi=200)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap", nargs="?", default="capture.pcap")
    ap.add_argument("key", nargs="?", default="swarm.key")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    key_text = open(args.key, "rb").read().strip()
    key = bytes.fromhex(key_text.decode())
    os.makedirs(args.out, exist_ok=True)

    stats = collections.Counter()
    valid_gps = []
    forged_gps = 0

    for ts, eth in read_pcap_packets(args.pcap):
        for _sport, _dport, udp in udp_payloads_from_ethernet(eth) or []:
            for pkt in mavlink2_frames(udp):
                msgid = pkt[7] | (pkt[8] << 8) | (pkt[9] << 16)
                sysid = pkt[5]
                signed = bool(pkt[2] & 1)
                ok = signature_valid(pkt, key)
                stats[(msgid, sysid, signed, ok)] += 1
                gps = decode_gps_raw_int(pkt)
                if gps is None:
                    continue
                if ok:
                    gps["capture_time"] = ts
                    valid_gps.append(gps)
                else:
                    forged_gps += 1

    print(f"[+] valid GPS points:  {len(valid_gps)}")
    print(f"[+] forged GPS points: {forged_gps}")
    print(f"[+] real sysids:       {sorted(set(p['sysid'] for p in valid_gps))}")

    tsv = os.path.join(args.out, "valid_gps.tsv")
    with open(tsv, "w") as f:
        f.write("sysid\ttime_usec\tlat\tlon\talt\n")
        for p in sorted(valid_gps, key=lambda x: (x["sysid"], x["time_usec"])):
            f.write(f"{p['sysid']}\t{p['time_usec']}\t{p['lat']:.7f}\t{p['lon']:.7f}\t{p['alt']:.3f}\n")
    print(f"[+] wrote {tsv}")

    plot(valid_gps, args.out)
    print(f"[+] plots written to {args.out}/valid_paths.png and {args.out}/per_sysid.png")
    print(f"[+] flag: {FLAG}")

if __name__ == "__main__":
    main()
