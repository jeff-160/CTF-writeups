table = {str(k):v for k, v in enumerate(')!@#$%^&*(') }

enc = '^&,*$,&),!@#,*#,!!^,(&,!!$,(%,$^,(%,*&,(&,!!$,!!%,(%,$^,(%,&),!!!,!!$,(%,$^,(%,&^,!)%,!)@,!)!,!@%'

for k, v in table.items():
    enc = enc.replace(v, k)

flag = ''.join([chr(int(i)) for i in enc.split(",")])
print("Flag:", flag)