dig _dmarc.krampus.csd.lol TXT  # forensics@ops.krampus.csd.lol

dig ops.krampus.csd.lol TXT # "internal-services: _ldap._tcp.krampus.csd.lol _kerberos._tcp.krampus.csd.lol _metrics._tcp.krampus.csd.lol"

dig _metrics._tcp.krampus.csd.lol SRV   # beacon.krampus.csd.lol

dig beacon.krampus.csd.lol TXT  # "config=ZXhmaWwua3JhbXB1cy5jc2QubG9s=="

dig exfil.krampus.csd.lol TXT   # "status=active; auth=dkim; selector=syndicate"

dig syndicate._domainkey.krampus.csd.lol TXT    # Y3Nke2RuNV9tMTlIVF9CM19LMU5ENF9XME5LeX0=

echo Y3Nke2RuNV9tMTlIVF9CM19LMU5ENF9XME5LeX0= | base64 -d