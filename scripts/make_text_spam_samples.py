"""Generate synthetic samples that contain encoded data.

The fixed random seed preserves source values.
The runtime zlib version determines compressed bytes.
All content originates in this script.
"""
import base64, binascii, io, random, struct, sys, zipfile, zlib, os

OUT = sys.argv[1]
rnd = random.Random(30)


def png(w=96, h=96) -> bytes:
    raw = b''.join(b'\x00' + bytes(rnd.getrandbits(8) for _ in range(w * 3)) for _ in range(h))
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


IMG = png()
B64 = base64.b64encode(IMG).decode()
B64_LINES = '\n'.join(B64[i:i + 76] for i in range(0, len(B64), 76))


def write(name, data):
    with open(os.path.join(OUT, name), 'wb') as f:
        f.write(data if isinstance(data, bytes) else data.encode())


# 1. vCard with an inline PHOTO (vCard 3.0, folded lines start with a space).
folded = '\r\n '.join(B64[i:i + 74] for i in range(0, len(B64), 74))
write('vcard-photo.vcf', 'BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Example Person\r\nN:Person;Example;;;\r\n'
      'ORG:Example Organisation\r\nEMAIL;TYPE=INTERNET:person@example.org\r\n'
      'TEL;TYPE=WORK:+1 555 0100\r\nPHOTO;ENCODING=b;TYPE=PNG:' + folded + '\r\nEND:VCARD\r\n')

# 2. iCalendar event with an inline ATTACH (RFC 5545, ENCODING=BASE64).
folded = '\r\n '.join(B64[i:i + 74] for i in range(0, len(B64), 74))
write('calendar-attach.ics', 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//hoover4 testdata//text-spam//EN\r\n'
      'BEGIN:VEVENT\r\nUID:text-spam-1@example.org\r\nDTSTAMP:20261005T120000Z\r\n'
      'DTSTART:20261006T090000Z\r\nDTEND:20261006T100000Z\r\nSUMMARY:Quarterly review meeting\r\n'
      'DESCRIPTION:Agenda in the attached image.\r\n'
      'ATTACH;FMTTYPE=image/png;ENCODING=BASE64;VALUE=BINARY:' + folded + '\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n')

# 3. HTML page with an image in a data: URI.
write('html-data-uri.html', '<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Report</title></head>\n'
      '<body><h1>Site inspection report</h1>\n<p>The inspection found no defects in the north wing.</p>\n'
      f'<img alt="photo" src="data:image/png;base64,{B64}">\n<p>Signed, the inspector.</p></body></html>\n')

# 4. SVG drawing with an embedded raster image in a data: URI.
write('svg-data-uri.svg', '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="96" height="120">\n'
      '<title>Floor plan</title>\n<text x="4" y="12" font-size="10">Floor plan, level 2</text>\n'
      f'<image x="0" y="20" width="96" height="96" xlink:href="data:image/png;base64,{B64}"/>\n</svg>\n')

# 5. RTF document with a picture as hex (\pict \pngblip), as word processors write it.
hexdata = binascii.hexlify(IMG).decode()
hexlines = '\n'.join(hexdata[i:i + 128] for i in range(0, len(hexdata), 128))
write('rtf-pict-hex.rtf', '{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0 Times New Roman;}}\n'
      '\\pard\\f0\\fs24 Minutes of the board meeting. The board approved the budget.\\par\n'
      '{\\pict\\pngblip\\picw96\\pich96\\picwgoal1440\\pichgoal1440\n' + hexlines + '\n}\\par\n'
      '\\pard The meeting closed at noon.\\par\n}\n')

# 6. Plain-text mail body with a uuencoded file, as older mail clients sent it.
uu = io.BytesIO()
uu.write(b'begin 644 photo.png\n')
for i in range(0, len(IMG), 45):
    uu.write(binascii.b2a_uu(IMG[i:i + 45]))
uu.write(b'`\nend\n')
write('uuencoded-mail.txt', 'From: sender@example.org\nTo: receiver@example.org\nSubject: photo\n'
      'Date: Mon, 5 Oct 2026 12:00:00 +0000\n\nHere is the photo you asked for.\n\n' + uu.getvalue().decode())

# 7. X bitmap (XBM): a C source file of hex bytes. `file` reports it as text.
w = h = 128
bits = bytes(rnd.getrandbits(8) for _ in range(w * h // 8))
rows = ',\n'.join('   ' + ', '.join('0x%02x' % b for b in bits[i:i + 12]) for i in range(0, len(bits), 12))
write('xbm-bitmap.xbm', f'#define noise_width {w}\n#define noise_height {h}\n'
      f'static unsigned char noise_bits[] = {{\n{rows} }};\n')

# 8. Zip archive with two text members: the archive text repeats the member text.
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, text in (('minutes-2026-01.txt', 'Minutes of January. The committee met on 12 January '
                        'and approved the purchase of three vehicles.\n'),
                       ('minutes-2026-02.txt', 'Minutes of February. The committee met on 9 February '
                        'and reviewed the vehicle contract with Example Motors Ltd.\n')):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 5, 12, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, text)
write('archive-with-text-members.zip', buf.getvalue())
