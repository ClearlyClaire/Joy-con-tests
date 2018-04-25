#!/bin/env python3

import sys
import time

from hid import find_joycons, open_joycons, vibrate, enable_vibration

NOTES2 = [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.0, 233.08, 264.94]
NOTES3 = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.0, 466.16, 493.88]
NOTES4 = [523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.0, 932.33, 987.77]
DO, DOd, RÉ, RÉd, MI, FA, FAd, SOL, SOLd, LA, LAd, SI = NOTES2
DO3, DOd3, RÉ3, RÉd3, MI3, FA3, FAd3, SOL3, SOLd3, LA3, LAd3, SI3 = NOTES3
DO4, DOd4, RÉ4, RÉd4, MI4, FA4, FAd4, SOL4, SOLd4, LA4, LAd4, SI4 = NOTES4

RICKASTLEY = [
              (FA3, 1.5), (SOL3, 1.5), (DO3, 1), (SOL3, 1.5), (LA3, 1.5), (DO4, 0.25), (LAd3, 0.25), (LA3, 0.5),
              (FA3, 1.5), (SOL3, 1.5), (DO3, 1), (DO3, 1.5),
              (0, 1),
              (DO3, 0.24), (0, 0.01), (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.49), (0, 0.01), (FA3, 0.25),
              (FA3, 1.5), (SOL3, 1.5), (DO3, 1), (SOL3, 1.5), (LA3, 1.5), (DO4, 0.25), (LAd3, 0.25), (LA3, 0.5),
              (FA3, 1.5), (SOL3, 1.5), (DO3, 1), (DO3, 1.5),
              (0, 1),
              (DO3, 0.24), (0, 0.01), (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.49), (0, 0.01), (FA3, 0.25),
              (0, 1),
              (RÉ3, 0.5), (MI3, 0.5), (FA3, 0.49), (0, 0.01), (FA3, 0.49), (SOL3, 0.5), (MI3, 1), (RÉ3, 0.5), (DO3, 0.5), (DO3, 1), (DO3, 1),
              (0, 0.5), (RÉ3, 0.49), (0, 0.01), (RÉ3, 0.5), (MI3, 0.5), (FA3, 0.5), (RÉ3, 1), (DO3, 0.5), (DO4, 0.5), (0, 0.5), (DO4, 0.5), (SOL3, 1.5),
              (0, 1),
              (RÉ3, 0.49), (0, 0.01), (RÉ3, 0.5), (MI3, 0.5), (FA3, 0.5), (RÉ3, 0.5), (FA3, 0.5), (SOL3, 0.5), (0, 0.5),
              (0, 0.5), (MI3, 0.5), (RÉ3, 0.5), (DO3, 1.5), (0, 1),
              (0, 0.5), (RÉ3, 0.49), (0, 0.01), (RÉ3, 0.5), (MI3, 0.5), (FA3, 0.5), (RÉ3, 0.5), (DO3, 1),
              (SOL3, 0.49), (0, 0.01), (SOL3, 0.49), (0, 0.01), (SOL3, 0.5), (LA3, 0.5), (SOL3, 1), (0, 1),
              (FA3, 1), (FA3, 1), (FA3, 0.5), (SOL3, 0.5), (LA3, 0.5), (FA3, 0.5),
              (SOL3, 0.49), (0, 0.01), (SOL3, 0.49), (0, 0.01), (SOL3, 0.5), (LA3, 0.5), (SOL3, 1), (DO3, 1),
              (0, 2), (RÉ3, 0.5), (MI3, 0.5), (FA3, 0.5), (RÉ3, 0.5),
              (0, 0.5), (SOL3, 0.5), (LA3, 0.5), (SOL3, 1.5),
              (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.25), (RÉ3, 0.25), (LA3, 0.74), (0, 0.01), (LA3, 0.75), (SOL3, 1.5),
              (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.25), (RÉ3, 0.25), (SOL3, 0.74), (0, 0.01), (SOL3, 0.75), (FA3, 0.75), (MI3, 0.25), (RÉ3, 0.5),
              (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.25), (RÉ3, 0.25), (FA3, 1), (SOL3, 0.5), (MI3, 0.75), (RÉ3, 0.25), (DO3, 0.49), (0, 0.01), (DO3, 0.49), (0, 0.01), (DO3, 0.5),
              (SOL3, 1), (FA3, 1), (FA3, 1), (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.25), (RÉ3, 0.25), (LA3, 0.74), (0, 0.01), (LA3, 0.75), (SOL3, 1.5),
              (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.25), (RÉ3, 0.25), (DO4, 1), (MI3, 0.5), (FA3, 0.75), (MI3, 0.25), (RÉ3, 0.5),
              (DO3, 0.25), (RÉ3, 0.25), (FA3, 0.25), (RÉ3, 0.25), (FA3, 1), (SOL3, 0.5), (MI3, 0.75), (RÉ3, 0.25), (DO3, 0.49), (0, 0.01), (DO3, 0.5),
              (SOL3, 1), (FA3, 1), (FA3, 1)]


def main(*args):
    lefts, rights = find_joycons()
    lefts, rights = open_joycons(lefts, rights)
    for l in lefts:
        enable_vibration(l)
    for r in rights:
        enable_vibration(r)
    for i, (freq, duration) in enumerate(RICKASTLEY):
        amp_lf = amp_hf = 97
        # Attenuate amplitude near base frequencies.
        # Should probably be improved by using proper maths/physics
        proximity_lf = abs(160 - freq)
        if proximity_lf < 20:
            amp_lf = 40
        elif proximity_lf < 25:
            amp_lf = 50
        elif proximity_lf < 30:
            amp_lf = 70
        elif proximity_lf < 50:
            amp_lf = 90
        proximity_hf = abs(330 - freq)
        if proximity_hf < 20:
            amp_hf = 40
        elif proximity_hf < 25:
            amp_hf = 50
        elif proximity_hf < 30:
            amp_hf = 70
        elif proximity_hf < 50:
            amp_hf = 90
        if freq == 0:
            amp_hf = amp_lf = 0
            freq = 320
        for d in lefts + rights:
            vibrate(d, 1 + i, freq, amp_hf, freq, amp_lf)
        time.sleep(duration * 60. / 114.)
    for l in lefts:
        vibrate(l, 2, 320, 0, 160, 0)


if __name__ == '__main__':
    main(*sys.argv[1:])
