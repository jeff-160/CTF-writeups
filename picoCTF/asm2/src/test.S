asm2:
	<+0>:	endbr32 
	<+4>:	push   ebp
	<+5>:	mov    ebp,esp
	<+7>:	sub    esp,0x10
	<+10>:	mov    eax,DWORD PTR [ebp+0xc]
	<+13>:	mov    DWORD PTR [ebp-0x4],eax
	<+16>:	mov    eax,DWORD PTR [ebp+0x8]
	<+19>:	mov    DWORD PTR [ebp-0x8],eax
	<+22>:	jmp    0x11d0 <asm2+35>
	<+24>:	add    DWORD PTR [ebp-0x4],0x1
	<+28>:	add    DWORD PTR [ebp-0x8],0xcb
	<+35>:	cmp    DWORD PTR [ebp-0x8],0xd72d
	<+42>:	jle    0x11c5 <asm2+24>
	<+44>:	mov    eax,DWORD PTR [ebp-0x4]
	<+47>:	leave  
	<+48>:	ret    

