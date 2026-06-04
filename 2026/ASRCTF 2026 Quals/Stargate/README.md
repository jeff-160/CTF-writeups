## Stargate  

<img src="chall.png" width=600>

need to login as `voss7` to get the flag  

`ORDER BY` sqli in `/crew` --> error based sqli to leak `commanders` creds table  

password hash generated with `os.urandom(4).hex()` --> bruteforce with hashcat  

```bash
hashcat -m 1400 -a 3 hash.txt ?1?1?1?1?1?1?1?1 -1 0123456789abcdef
hashcat -m 1400 hash.txt --show
```

Flag: `ASRCTF{ORDER_BY_att4ck5_are_c001}`