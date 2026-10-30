#!/usr/bin/env python3
"""Write the synthetic "HTML saved with an .xls name" samples of this folder.

Run from this folder: python3 generate_html_xls.py
Three shapes are written. Report generators write a bare `<table border=1>` fragment.
Excel "Save as Web Page" and many web applications write a full HTML document with the
Office namespaces. Some exports use an `.xlsx` name for the same bytes. All values are
invented.
"""
import os

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html-xls")

ROWS = [
    ("Case", "Date", "Officer", "Amount", "Closed"),
    ("NPF-001", "2016-03-01", "A. Abel", "120.50", "TRUE"),
    ("NPF-002", "2016-03-04", "B. Brook", "75", "FALSE"),
    ("NPF-003", "2016-03-09", "C. Cole", "1,200.00", "TRUE"),
    ("NPF-004", "", "D. Dale & E. Eden", "0", "FALSE"),
]


def bare_fragment():
    # The shape of a report-server export: no <html>, no <body>, upper-case tags in the
    # rows, unquoted attributes, a <br> inside a cell, a colspan, CRLF line ends.
    lines = ["<table border=1>"]
    lines.append("<tr><th colspan=5>Monthly case list</th></tr>")
    for row in ROWS:
        cells = "".join("<TD>%s</TD>" % v.replace("&", "&amp;") for v in row)
        lines.append("<TR>%s</TR>" % cells)
    lines.append("<tr><td>Note</td><td colspan=4>first line<br>second line</td></tr>")
    lines.append("</table>")
    return ("\r\n".join(lines) + "\r\n").encode("windows-1252")


def office_document(sheet_count=2):
    head = (
        '<html xmlns:o="urn:schemas-microsoft-com:office:office"\r\n'
        'xmlns:x="urn:schemas-microsoft-com:office:excel"\r\n'
        'xmlns="http://www.w3.org/TR/REC-html40">\r\n'
        "<head>\r\n"
        '<meta http-equiv=Content-Type content="text/html; charset=utf-8">\r\n'
        '<meta name=ProgId content=Excel.Sheet>\r\n'
        "<!--[if gte mso 9]><xml>\r\n <x:ExcelWorkbook>\r\n  <x:ExcelWorksheets>\r\n"
        "   <x:ExcelWorksheet>\r\n    <x:Name>Cases</x:Name>\r\n   </x:ExcelWorksheet>\r\n"
        "  </x:ExcelWorksheets>\r\n </x:ExcelWorkbook>\r\n</xml><![endif]-->\r\n"
        "<style>td {mso-number-format:\\@;}</style>\r\n"
        "</head>\r\n<body>\r\n"
    )
    body = []
    for sheet in range(sheet_count):
        body.append('<table border=0 cellpadding=0 cellspacing=0 x:str>')
        for row in ROWS:
            cells = "".join(
                '<td x:num>%s</td>' % v if v.replace(".", "", 1).isdigit() else
                "<td>%s</td>" % v.replace("&", "&amp;") for v in row)
            body.append(" <tr>%s</tr>" % cells)
        body.append(" <tr><td>Résumé</td><td>Ünïcode — test</td></tr>")
        body.append("</table>")
    return (head + "\r\n".join(body) + "\r\n</body>\r\n</html>\r\n").encode("utf-8")


if __name__ == "__main__":
    os.makedirs(HERE, exist_ok=True)
    with open(os.path.join(HERE, "report-fragment.xls"), "wb") as f:
        f.write(bare_fragment())
    with open(os.path.join(HERE, "excel-web-page.xls"), "wb") as f:
        f.write(office_document(1))
    with open(os.path.join(HERE, "web-export-two-tables.xlsx"), "wb") as f:
        f.write(office_document(2))
