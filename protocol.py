
import construct as cst
import time
import sys

HEADER = cst.Struct('pc_header',
                    cst.Magic('\x00'),
                    cst.Const(cst.UBInt8('lines'), 1),
                    cst.UBInt8('address'),
                    cst.Magic('\x03'))

SER_STATUS = cst.BitStruct('serst',
                           cst.Magic('\x01\x01\x00'),
                           cst.Flag('schedule_enabled'),
                           cst.Flag('ack_enabled'),
                           cst.Flag('further_pages'),
                           cst.Flag('interrupt_mode'),
                           cst.Magic('\x00'))

PAGE_IDX = cst.Bytes('page_num', 3)
TEMPO = cst.BitStruct('tempo',
                      cst.Magic('\x01\x01'),
                      cst.Enum(cst.BitField('display_ctrl', 2),
                               TIMED=0, FIXED_ON=1, FIXED_OFF=2),
                      cst.Enum(cst.BitField('persist_time', 4),
                               S2=1, S5=2, S10=3, S20=4, S30=5,
                               S45=6, S60=7, S90=8, S120=9))

# TODO: union persist_time with scroll_speed

PAGE_FUNC = cst.BitStruct('page_func',
                          cst.Magic('\x01\x01'),
                          cst.Flag('show_temp'),
                          cst.Flag('show_time'),
                          cst.Enum(cst.BitField('page_effect', 4),
                                   RANDOM=0,
                                   APPEAR=1,
                                   WIPE=2,
                                   OPEN=3,
                                   LOCK=4,
                                   ROTATE=5,
                                   RIGHT=6,
                                   LEFT=7,
                                   ROLL_UP=8,
                                   ROLL_DOWN=9,
                                   PINGPONG=10,
                                   FILL_UP=11,
                                   PAINT=12,
                                   FADE_IN=13,
                                   JUMP=14,
                                   SLIDE=15))

PAGE_CFG = cst.BitStruct('page_cfg',
                         cst.Magic('\x01'),
                         cst.Flag('background_on'),
                         cst.Flag('non_english'),
                         cst.Flag('autocenter'),
                         cst.Flag('bold_joins_78'),
                         cst.Flag('bold_joins_56'),
                         cst.Flag('bold_joins_34'),
                         cst.Flag('bold_joins_12'),
                         )

CMD_SEQ = cst.Sequence('_cmd', cst.Magic('\x1c'),
                       cst.Enum(cst.Byte('cmd'),
                                FLASH='F', ENLARGE='E',
                                RED='R', GREEN='G', YELLOW='Y',
                                MULTICOLOUR='M', DEFAULT='D'))

PAGE = cst.Struct('page',
                  PAGE_IDX,
                  cst.Embed(TEMPO),
                  cst.Embed(PAGE_FUNC),
                  cst.Embed(PAGE_CFG),
                  cst.CString('body', terminators='\x04'))

MESSAGE = cst.Struct('msg', HEADER, SER_STATUS, PAGE)

def main(*args):
    pass

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    main(args)
    
