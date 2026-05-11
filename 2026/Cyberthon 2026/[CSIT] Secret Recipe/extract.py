from Evtx.Evtx import Evtx

out = ''

with Evtx("Microsoft-Windows-PowerShell-Operational.evtx") as log:
    for record in log.records():
        if '4104' in record.xml():
            out += record.xml() + '\n'

with open("log.txt", 'w') as f:
    f.write(out)