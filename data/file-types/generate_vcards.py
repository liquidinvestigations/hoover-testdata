#!/usr/bin/env python3
"""Write the synthetic vCard samples of this folder.

Run from this folder: python3 generate_vcards.py
All names, numbers and addresses are invented. The photo is a 48x48 PNG that this
script draws, so the base64 value is several lines long, as in a real card.
"""
import base64
import os
import struct
import zlib

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vcard")


def png(size=48):
    rows = b"".join(
        b"\x00" + b"".join(bytes(((x * 5) % 256, (y * 5) % 256, (x * y) % 256))
                           for x in range(size))
        for y in range(size))

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    header = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(rows, 0)) + chunk(b"IEND", b""))


PHOTO = base64.b64encode(png()).decode()


def fold(line, width=75, indent=" "):
    """RFC 6350 folding: CRLF and one space before each continuation."""
    out, rest = [], line
    out.append(rest[:width])
    rest = rest[width:]
    while rest:
        out.append(indent + rest[:width - 1])
        rest = rest[width - 1:]
    return "\r\n".join(out)


def card_21(photo=True):
    lines = [
        "BEGIN:VCARD", "VERSION:2.1",
        "N;LANGUAGE=en-us:Abel;Ana", "FN:Ana Abel", "ORG:Example Office;Records",
        "TITLE:Clerk", "TEL;WORK;VOICE:+1 555 0101", "TEL;CELL;VOICE:+1 555 0102",
        "ADR;WORK;PREF:;;1 Example Road;Sample Town;;00000;Nowhere",
        "LABEL;WORK;PREF;ENCODING=QUOTED-PRINTABLE:1 Example Road=0D=0A=\r\nSample Town 00000",
        "EMAIL;PREF;INTERNET:ana.abel@example.org",
    ]
    if photo:
        # Outlook writes vCard 2.1 base64 lines with two leading spaces and ends the
        # value with a blank line.
        body = "\r\n".join("  " + PHOTO[i:i + 72] for i in range(0, len(PHOTO), 72))
        lines.append("PHOTO;TYPE=PNG;ENCODING=BASE64:\r\n" + body + "\r\n")
    lines += ["REV:20160301T101500Z", "END:VCARD"]
    return "\r\n".join(lines) + "\r\n"


def card_30(photo=True, name=("Brook", "Ben")):
    last, first = name
    lines = [
        "BEGIN:VCARD", "VERSION:3.0",
        f"N:{last};{first};;;", f"FN:{first} {last}", "ORG:Example Office",
        "TEL;TYPE=WORK,VOICE:+1 555 0201", f"EMAIL;TYPE=INTERNET:{first.lower()}@example.org",
        "item1.URL:https\\://example.org/staff", "item1.X-ABLabel:profile",
    ]
    if photo:
        lines.append(fold("PHOTO;TYPE=PNG;ENCODING=b:" + PHOTO))
    lines += ["NOTE:Met at the 2016 workshop\\, see file 12.", "END:VCARD"]
    return "\r\n".join(lines) + "\r\n"


def card_40(photo="data"):
    lines = [
        "BEGIN:VCARD", "VERSION:4.0",
        "FN:Cora Cole", "N:Cole;Cora;;;", "KIND:individual",
        "TEL;VALUE=uri;TYPE=work:tel:+1-555-0301", "EMAIL;TYPE=work:cora.cole@example.org",
        "LANG;PREF=1:en",
    ]
    if photo == "data":
        lines.append(fold("PHOTO:data:image/png;base64," + PHOTO))
        lines.append(fold("LOGO;MEDIATYPE=image/png:data:image/png;base64," + PHOTO[:400]))
    elif photo == "uri":
        lines.append("PHOTO;MEDIATYPE=image/png:https://example.org/photos/cora.png")
    lines += ["END:VCARD"]
    return "\r\n".join(lines) + "\r\n"


SAMPLES = {
    "vcard-2.1-photo.vcf": card_21(True).encode("windows-1252"),
    "vcard-2.1.vcf": card_21(False).encode("windows-1252"),
    "vcard-3.0-photo.vcf": card_30(True).encode("utf-8"),
    "vcard-3.0.vcf": card_30(False).encode("utf-8"),
    "vcard-4.0-photo-data-uri.vcf": card_40("data").encode("utf-8"),
    "vcard-4.0-photo-link.vcf": card_40("uri").encode("utf-8"),
    # A byte order mark, a blank line and lower-case keywords, still a vCard.
    "vcard-bom-lowercase.vcf": b"\xef\xbb\xbf\r\n" + card_30(False).replace(
        "BEGIN:VCARD", "begin:vcard").replace("VERSION:", "version:").encode("utf-8"),
    # An address book export: several cards in one file, no extension.
    "address-book-export": "".join(
        card_30(False, name) for name in
        [("Dale", "Dan"), ("Eden", "Eli"), ("Frost", "Fay"), ("Gale", "Gus"),
         ("Hale", "Hana"), ("Isle", "Ivo")]).encode("utf-8"),
    # Not a vCard: a calendar file starts the same way with another keyword.
    "not-a-vcard.ics": (
        "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Example//EN\r\nBEGIN:VEVENT\r\n"
        "UID:1@example.org\r\nDTSTART:20160301T100000Z\r\nSUMMARY:Review\r\n"
        "END:VEVENT\r\nEND:VCALENDAR\r\n").encode("utf-8"),
}

if __name__ == "__main__":
    os.makedirs(HERE, exist_ok=True)
    for name, data in SAMPLES.items():
        with open(os.path.join(HERE, name), "wb") as f:
            f.write(data)
