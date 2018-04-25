# Mostly from https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_notes.md
# and https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/master/bluetooth_hid_subcommands_notes.md

import hidapi

from rumble import encode_rumble

VENDOR_ID = 0x057e
PRODUCT_ID_L = 0x2006
PRODUCT_ID_R = 0x2007

def find_joycons():
    lefts = []
    rights = []

    for d in hidapi.enumerate(vendor_id=VENDOR_ID):
        if d.product_id == PRODUCT_ID_L:
            lefts.append(d)
        elif d.product_id == PRODUCT_ID_R:
             rights.append(d)

    return (lefts, rights)


def open_joycons(lefts, rights):
   return ([hidapi.Device(d) for d in lefts],
           [hidapi.Device(d) for d in rights])


def vibrate(dev, counter, hf_freq, hf_amp, lf_freq, lf_amp):
    rumble = encode_rumble(hf_freq, hf_amp, lf_freq, lf_amp)
    dev.write(bytes([counter & 0x0f]) + rumble + rumble + bytes(0x40 - 11), b'\x10')


def enable_vibration(dev):
    dev.write(bytes([0]) + encode_rumble(320, 0, 160, 0) + encode_rumble(320, 0, 160, 0) + bytes([0x48, 0x01]), b'\x01')
