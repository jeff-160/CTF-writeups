## SecureAuth  

<img src="chall.png" width=600>

`/.well-known/jwks.json` exposes RSA pub key --> alg confusion attack --> /api/admin   

Flag: `CDDC2026{Jwt_alg0_c0nfus10N_rs256_T0_hs256!}`