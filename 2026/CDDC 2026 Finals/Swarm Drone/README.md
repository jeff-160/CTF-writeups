# CDDC2026 MAVLink Swarm — Writeup

## TL;DR

The capture contains MAVLink v2 `GPS_RAW_INT` telemetry from 20 drones, mixed with forged packets. MAVLink v2 signing is enabled. Using `swarm.key`, validate each packet signature and discard packets whose 6-byte MAVLink signature does not match. Plot only authenticated GPS points by `sysid`; the real drone paths draw the flag.

Final flag:

```text
CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}
```

## Packet format used

MAVLink v2 frames start with magic byte `0xfd`:

```text
fd len incompat compat seq sysid compid msgid[3] payload checksum[2] signature[13]
```

The `incompat` byte has bit `0x01` set when the packet is signed. The last 13 bytes are:

```text
link_id[1] timestamp[6] signature[6]
```

MAVLink v2 signing computes:

```python
sha256(secret_key + packet_without_signature + link_id_timestamp_7_bytes).digest()[:6]
```

So forged telemetry is easy to identify: it has the wrong signature even though it impersonates real `sysid`s.

## Recovery steps

1. Parse the pcap manually as Ethernet → IPv4 → UDP.
2. Extract MAVLink v2 frames from UDP payloads.
3. Read `swarm.key` as a 32-byte hex key.
4. Verify signed MAVLink packets with the key.
5. Decode only valid `GPS_RAW_INT` messages, message id `24`:
   - `lat` at payload offset `8`, signed int32, scale `1e7`
   - `lon` at payload offset `12`, signed int32, scale `1e7`
   - `alt` at payload offset `16`, signed int32, scale `1000`
6. Sort points by MAVLink timestamp and plot paths per `sysid`.
7. Reading the plotted real paths gives:

```text
CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}
```

## Why the forged data fails

The adversary reused/impersonated drone `sysid`s and sent plausible-looking GPS telemetry, but did not possess the MAVLink signing key. Therefore their packets do not pass the signature check. In this capture, the valid packets form clean letter strokes; the forged packets are noise/poisoning.

## Run

```bash
python3 solve_mavlink_swarm.py capture.pcap swarm.key --out out
```

Outputs:

```text
out/valid_gps.tsv
out/valid_paths.png
out/per_sysid.png
```
