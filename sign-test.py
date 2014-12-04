#!/usr/bin/env python

import serial
import time
import sys

msg_arg = ''.join(sys.argv[1:]) or 'cats like hats'

portname = '/dev/tty.usbserial-AH00ROQ8'

# header 
pkt_header = bytearray([0x00, # header sync
                        0x01, # lines (=1)
                        0x01, # sign address
                        0x03, # etx - end of header
                    ])

#msg_prefix = bytearray("\xC8001\xEF\xC1\x80")
msg_prefix = bytearray([
    0b1100000, # serial status flags (orig. 0xc8)
    0x30, # page (0xx)
    0x30, # page (x0x)
    0x31, # page (xx1) = 001
    0xef, # ? # tempo
    0xc2, # ? # function = paint
    0x80, # ? # page status
])
# flags = 0b1100 1000
# --------
# :0, :5 = 0
# :6, :7 = 1
# 0b110x xxx0
# :1 = interrupt mode
# :2 = more pages to follow flag (clear = no more pages)
# :3 = ack requested
# :4 = schedule mode (clear = no schedule)
# 0b11001010

# tempo
# -----
# 0b11xx xxxx

# function
# --------
# 0b11aa bbbb
# :5 = show temp
# :4 = show time
# :0 - :3
# 0 = random
# 1 = appears
# 2 = wipe
# 3 = open
# 4 = lock
# 5 = rotate
# 6 = right
# 7 = left
# 8 = roll up
# 9 = roll dn
# 10= ping pong
# 11= fill up
# 12= paint
# 13= fade in
# 14= jump
# 15= slide

# page status
# -----------
# 0x80 = 0b10000000
# :7 always set, rest clear.


msg_suffix = bytearray([0x04]) # EOT - end of text/packet.

def construct_message(msg):
    msgbuf = pkt_header + msg_prefix + bytearray(msg) + msg_suffix
    checksum = build_checksum(msgbuf)
    msgbuf += bytearray([checksum])
    return str(msgbuf)

def build_checksum(buf):
    chk = 0
    for c in buf:
        chk ^= c
    return chk

try:
    port = serial.Serial(portname, 9600)
    msg_pkt = construct_message(msg_arg)
    port.flushInput()
    port.flushOutput()
    while True:
        print 'pkt: ', repr(msg_pkt)
        #print str(msg_pkt)
        port.write(msg_pkt)
        port.flush()
        time.sleep(1.0)
        
finally:
    port.close()
    print "Done"
