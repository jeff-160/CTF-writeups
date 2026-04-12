some web chall with a code execution vuln  

basically runs input in a python sandbox that has `__builtins__` disabled  

can use a `().__reduce_ex__(2)` chain to get RCE, and reading `config.py` reveals that there is a `FLAG` env variable  

Flag: `putcCTF{Y0UR3_4_W1Z4RD_H4RRY}`