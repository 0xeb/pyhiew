import hiew

def buf_to_c_array(buf):
    i = 1
    out = []
    for ch in buf:
        out.append('0x%02x, ' % ch)
        if i % 16 == 0:
            i = 1
            out.append('\n  ')
        else:
            i += 1
    return ''.join(out).rstrip()[:-1]


r, s = hiew.FileRead(0, 10)


hiew.Message(f"Read {r} byte(s)", buf_to_c_array(s))
