## Investigative Reversing 0  

<img src="images/chall.png" width=600>

We are provided with the binary `mystery` and the image file `mystery.png`.   

Decompiling the binary shows that it takes in `26` bytes and performs a Caesar-cipher encoding on specific bytes, then writes it to `mystery.png`.  

```c
void main(void)
{
  FILE *__stream;
  FILE *__stream_00;
  size_t sVar1;
  long in_FS_OFFSET;
  int local_54;
  int local_50;
  char local_38 [4];
  char local_34;
  char local_33;
  char local_29;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __stream = fopen("flag.txt","r");
  __stream_00 = fopen("mystery.png","a");
  if (__stream == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (__stream_00 == (FILE *)0x0) {
    puts("mystery.png is missing, please run this on the server");
  }
  sVar1 = fread(local_38,0x1a,1,__stream);
  if ((int)sVar1 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("at insert");
  fputc((int)local_38[0],__stream_00);
  fputc((int)local_38[1],__stream_00);
  fputc((int)local_38[2],__stream_00);
  fputc((int)local_38[3],__stream_00);
  fputc((int)local_34,__stream_00);
  fputc((int)local_33,__stream_00);
  for (local_54 = 6; local_54 < 0xf; local_54 = local_54 + 1) {
    fputc((int)(char)(local_38[local_54] + '\x05'),__stream_00);
  }
  fputc((int)(char)(local_29 + -3),__stream_00);
  for (local_50 = 0x10; local_50 < 0x1a; local_50 = local_50 + 1) {
    fputc((int)local_38[local_50],__stream_00);
  }
  fclose(__stream_00);
  fclose(__stream);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Opening `mystery.png` in [Hexed.it](https://hexed.it/) will reveal the ciphertext at the end of the file.  

<img src="images/ciphertext.png" width=600>

We can just extract the bytes and reverse the encryption to get the flag.  

Flag: `picoCTF{f0und_1t_35f69dab}`