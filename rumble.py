# Mostly from https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/issues/11

import math

HF_FREQ_BASE = 80
LF_FREQ_BASE = 40

def decode_freq(raw, base):
    return 2**(raw/32.) * base


def encode_freq(freq, base):
    assert (freq >= 0)
    val = math.log2(freq / base) * 32
    if val < 0:
        return 0
    elif val > 0x7f:
        return 0x7f
    else:
      return int(round(val)) & 0x7f


def decode_rumble(buff):
    raw_value = (buff[3] << 24) | (buff[2] << 16) | (buff[1] << 8) | buff[0]
    mode = raw_value >> 30
    assert (mode == 1) # Dual-wave
    silent = raw_value & 0x03
    assert (silent == 0)
    raw_value >>= 2
    hf_freq = raw_value & 0x7f
    raw_value >>= 7
    hf_amp = raw_value & 0x7f
    raw_value >>= 7
    lf_freq = raw_value & 0x7f
    raw_value >>= 7
    lf_amp = raw_value & 0x7f
    raw_value >>= 7
    assert (mode == raw_value) # Just to be sure I didn't fuck up
    return (decode_freq(hf_freq, HF_FREQ_BASE), hf_amp, decode_freq(lf_freq, LF_FREQ_BASE), lf_amp)



def encode_rumble(hf_freq, hf_amp, lf_freq, lf_amp):
    assert (0 <= hf_amp < 100)
    assert (0 <= lf_amp < 100)
    raw_value = 1 # Mode
    raw_value <<= 7
    raw_value |= lf_amp
    raw_value <<= 7
    raw_value |= encode_freq(lf_freq, LF_FREQ_BASE)
    raw_value <<= 7
    raw_value |= hf_amp
    raw_value <<= 7
    raw_value |= encode_freq(hf_freq, HF_FREQ_BASE)
    raw_value <<= 2
    return bytes([raw_value & 0xff, (raw_value >> 8) & 0xff, (raw_value >> 16) & 0xff, raw_value >> 24])
