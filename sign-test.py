#!/usr/bin/env python

import serial
import time
import sys
import platform
import protocol as pcp
import arrow
import random

# header
# pkt_header = bytearray([0x00, # header sync
#                         0x01, # lines (=1)
#                         0x01, # sign address
#                         0x03, # etx - end of header
#                     ])

# #msg_prefix = bytearray("\xC8001\xEF\xC1\x80")
# def build_prefix(func=1, speed=15):
#     msg_prefix = bytearray([
#         0xc8,#0b11000000, # serial status flags (orig. 0xc8)
#         0x30, # page (0xx)
#         0x30, # page (x0x)
#         0x31, # page (xx1) = 001
#         0b11000000 | speed, # ? # tempo
#         0xc0 | (func & 0x0f), # ? # function = paint
#         0x80, # ? # page status
#     ])
#     return msg_prefix

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


# msg_suffix = bytearray([0x04]) # EOT - end of text/packet.

# def construct_message(msg):
#     msgbuf = pkt_header + build_prefix(15, 3) + bytearray(msg) + msg_suffix
#     checksum = build_checksum(msgbuf)
#     msgbuf += bytearray([checksum])
#     return str(msgbuf)

# def build_checksum(buf):
#     chk = 0
#     for c in buf:
#         chk ^= c
#     return chk

def fmt_timedelta(start, end=None):
    if end is None:
        end = arrow.now()
    delta = end - start
    dmins, dsecs = divmod(delta.total_seconds(), 60)
    return '{:02d}:{:06.03f}'.format(int(dmins), dsecs)

def main(portname, msg_arg):
    port = None
    breaks = 0
    try:
        port = serial.Serial(portname, 9600)
        port.flushInput()
        port.flushOutput()
        start_time = arrow.now()
        while True:
            td = fmt_timedelta(start=start_time)
            if random.randint(0, 100) > 90:
                breaks += 1
                print 'Beam broken!'
            body_text = td + ' ' + 'B:{:-3d}'.format(breaks)
            body_text = '{:<16s}'.format(body_text)
            msg_pkt = pcp.simple_static_message(body_text)
            print 'pkt: ', repr(msg_pkt)
            #print str(msg_pkt)
            port.write(msg_pkt)
            port.flush()
            time.sleep(0.2)

    finally:
        if port:
            port.close()
        print "Done"


if __name__ == '__main__':
    msg_arg = ' ' * 12
    cmd_args = sys.argv[1:]
    if len(cmd_args):
        msg_arg = ''.join(cmd_args)
    else:
        msg_arg = ''

    ostype = platform.system().lower()
    if ostype.startswith('darwin'):
        portname = '/dev/tty.usbserial-AH00ROQ8'
        print "OSX, using %s" %  portname
    else:
        portname = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AH00ROQ8-if00-port0'
        print "Other OS, using %s" %  portname
    main(portname, msg_arg)
