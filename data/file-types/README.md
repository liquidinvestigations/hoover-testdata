# File type samples

These files test file type detection and table reading. Each file has the
defect that it covers. The generator scripts beside this file write the
synthetic files. Run each script from this folder with Python 3.

| Folder | Generator |
|---|---|
| `vcard/` | `generate_vcards.py` |
| `html-xls/` (not `online/`) | `generate_html_xls.py` |
| `sqlite/` | `generate_sqlite.py` |
| `spreadsheetml/` (not `online/`) | `generate_spreadsheetml.py` |

The vCard and HTML generators write the same bytes on each run. The SQLite
generator writes the same tables and rows, but the file bytes depend on the
SQLite library version, so its SHA-256 values are for the copies in this
folder.

All names, numbers and addresses in the synthetic files are invented.

## vCard

The defect: a vCard is a text file. Detectors call some vCards `text/csv`,
`text/calendar` or `message/rfc822`, so they get a table reader or the email
parser. The base64 value of a PHOTO is stored and indexed as text.

| File | Bytes | SHA-256 | Source | License | Content |
|---|---|---|---|---|---|
| `vcard/vcard-2.1.vcf` | 381 | `c899be4d941739ba8268e71d079fbcecd0cba58e4305c8b25a4dd730800aeacf` | `generate_vcards.py` | MIT | vCard 2.1 with a quoted-printable value, no PHOTO |
| `vcard/vcard-2.1-photo.vcf` | 10312 | `7aa3898ff94590a5a1139de001899aa981632af277793a4af5583d76475e1862` | `generate_vcards.py` | MIT | vCard 2.1, PHOTO in base64 with indented lines and a blank line after it, as Outlook writes it |
| `vcard/vcard-3.0.vcf` | 266 | `5c5ee2c185a61718b64d1771c6973b249de4a343e5133162ee5db37d56365bc9` | `generate_vcards.py` | MIT | vCard 3.0, no PHOTO |
| `vcard/vcard-3.0-photo.vcf` | 10044 | `39fe202ba5b8164cad3c25f782cbcc1dc9a3caf9188ca0234741cc550be1719f` | `generate_vcards.py` | MIT | vCard 3.0, PHOTO with `ENCODING=b` and folded lines |
| `vcard/vcard-4.0-photo-data-uri.vcf` | 10430 | `ad402c8b3d41849ecab9950f4b7ec8566242bb222b7c707e55ed8e1d0c668049` | `generate_vcards.py` | MIT | vCard 4.0, PHOTO and LOGO as `data:` URIs |
| `vcard/vcard-4.0-photo-link.vcf` | 243 | `009edf28a0325eb807e0f9a5696a242cd55bc12c0848a29af1d4275c95441f80` | `generate_vcards.py` | MIT | vCard 4.0, PHOTO as a link that stays in the text |
| `vcard/vcard-bom-lowercase.vcf` | 271 | `01aad488cdff9bee479cf42b1e4c83d649a8383d0c9504a9396538311e4a8950` | `generate_vcards.py` | MIT | UTF-8 byte order mark, a blank line, lower-case keywords |
| `vcard/address-book-export` | 1589 | `4cdf51c8e3f8f265b72e3447f968ab3b579d2099e233d112415ce534b6e7e681` | `generate_vcards.py` | MIT | six vCard 3.0 cards in one file without an extension |
| `vcard/not-a-vcard.ics` | 155 | `3a259913d5cb7dc65e5615827e6cab4cb97bf9da475d287c0f53bdbea1c52894` | `generate_vcards.py` | MIT | iCalendar file, which the vCard detection must refuse |

Real vCards from the Nauru Police Force release are in
`../mail-public/sources/nauru-police-force/`. The release names its Exchange
contact items `.eml`, and their bytes are vCard 3.0.

## HTML and XML saved with a spreadsheet name

The defect: a spreadsheet program or a report server writes HTML, MHTML or
SpreadsheetML 2003 XML with an `.xls` or `.xlsx` name. calamine reads none of
them. The pipeline indexes them as a web page or as XML, and no table is made.

| File | Bytes | SHA-256 | Source | License | Content |
|---|---|---|---|---|---|
| `html-xls/report-fragment.xls` | 586 | `5c70e20a8c4533b18be70d7b95730d2aa78454ef25a191b33cce706cbeb765d4` | `generate_html_xls.py` | MIT | a bare `<table border=1>` fragment in Windows-1252, with `colspan` and `<br>` |
| `html-xls/excel-web-page.xls` | 1135 | `7252631f664c144ed1a8fa253fb1a4aa8c5cdf22fb21b3be99f11c9f3b8071f3` | `generate_html_xls.py` | MIT | full HTML with the Office Excel namespace and a worksheet name |
| `html-xls/web-export-two-tables.xlsx` | 1719 | `b59e759c690514037d04e31fb4be6052eaf6c43ff11de25c9d260cb0d57961e0` | `generate_html_xls.py` | MIT | the same HTML shape with two tables and an `.xlsx` name |
| `html-xls/online/xls2xlsx-rowcolspan.xls` | 730 | `056b1b0ee7409f8982d85f3ee20133a23b73bfa7cb6445c1efe04759fc69e7c3` | https://github.com/snoopyjc/xls2xlsx/blob/4d93bcaafeb50bba0d095fa43900290c1cc4fc72/tests/inputs/rowcolspan.xls | MIT, `notices/xls2xlsx-LICENSE` | `<table border=20>` with `rowspan` and `colspan` |
| `html-xls/online/xls2xlsx-width.xls` | 5521 | `2ae0c141f5ea3f9b3ef99f80ded6949d785a4dffee91054ba971d1aae2ffe9aa` | https://github.com/snoopyjc/xls2xlsx/blob/4d93bcaafeb50bba0d095fa43900290c1cc4fc72/tests/inputs/width.xls | MIT, `notices/xls2xlsx-LICENSE` | XHTML document whose body is one table |
| `html-xls/online/xls2xlsx-report.xls` | 201462 | `fe930f69a28083b669a190df576d61a422ed53bc56dbed45095d0ae242f2c75e` | https://github.com/snoopyjc/xls2xlsx/blob/4d93bcaafeb50bba0d095fa43900290c1cc4fc72/tests/inputs/report.xls | MIT, `notices/xls2xlsx-LICENSE` | report-server export with the Office Excel namespace |
| `html-xls/online/xls2xlsx-Dates.xls` | 28129 | `400247807bc0aa286d000a139bce89427a35da65de6b7f18b7da2124dc0faf82` | https://github.com/snoopyjc/xls2xlsx/blob/4d93bcaafeb50bba0d095fa43900290c1cc4fc72/tests/inputs/Dates.xls | MIT, `notices/xls2xlsx-LICENSE` | Excel "Single File Web Page" (MHTML) with an `.xls` name |
| `html-xls/online/libreoffice-fdo55572-1.xls` | 9185 | `df2e903d1fe9b16b3669129df132fad95160a4ce62817da2b21b57548c230023` | https://github.com/LibreOffice/core/blob/1440fb4cb852e554f080a9f6b9f3cc694a2f8256/sc/qa/unit/data/xls/fdo55572-1.xls | MPL-2.0, `notices/MPL-2.0.txt` | SpreadsheetML 2003 XML with an `.xls` name |
| `html-xls/online/libreoffice-tdf158483.xls` | 26291 | `4174ce9db6cf0acf46cf94b2c3116843055120c79ae03dd993eb30808d5e0236` | https://github.com/LibreOffice/core/blob/1440fb4cb852e554f080a9f6b9f3cc694a2f8256/sc/qa/unit/data/xls/tdf158483.xls | MPL-2.0, `notices/MPL-2.0.txt` | SpreadsheetML 2003 XML with the `ss:` prefix and an `.xls` name |

## SQLite 3

The defect: no reader opens a SQLite 3 database, so its tables are not
indexed and not shown.

| File | Bytes | SHA-256 | Source | License | Content |
|---|---|---|---|---|---|
| `sqlite/contacts-orders.sqlite3` | 24576 | `68b074bedb7d3713ddf1b9cd8b8b6e40927b2395a52542a890823a5bbfddbe3f` | `generate_sqlite.py` | MIT | tables `contacts` (BLOB column `photo`, NULL values) and `orders`, view `order_totals`, an index and a trigger |
| `sqlite/many-rows.sqlite3` | 299008 | `8ec78dc3c11e7e843dec544dc7b2147f87ac48fc87c361bac62ae89b7c820ed7` | `generate_sqlite.py` | MIT | one table of 6,000 rows, for a row limit |
| `sqlite/app-data` | 20480 | `d0d0b622eff1dd8ead28de6187ac2cd303c5902e1c6d924d0fdcfa0d81ffe6bc` | `generate_sqlite.py` | MIT | no extension, a table name with a quote and a semicolon, an empty table |

## SpreadsheetML 2003

The defect: Excel 2002 and 2003 save a workbook as one XML file, the "XML
Spreadsheet 2003" format. The file has an `.xml` or a spreadsheet extension.
Detectors call it XML or HTML, and no table reader reads it.

| File | Bytes | SHA-256 | Source | License | Content |
|---|---|---|---|---|---|
| `spreadsheetml/doctype-entities.xml` | 416 | `35878bcdf38959e336126f125fdf38de92610140fa248b6f7081317f8a507fe6` | `generate_spreadsheetml.py` | MIT | A document type declaration with entities, which a reader must refuse |
| `spreadsheetml/online/libreoffice-character-set.xml` | 77372 | `ad86c8dc3df476774f9286ed91f4557bde5b77663187edd0e9d8ef2a200663ef` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/character-set.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/online/libreoffice-empty-rows.xml` | 2595 | `a523f8894a43b472f67df70df6b629452369aaa16954f69ebb98ff0701eee222` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/empty-rows.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/online/libreoffice-hidden-rows-columns.xml` | 3820 | `f44f7c42c40a548a426861ecf8677f992a47061235bb92dd6db1fce2bf705d87` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/hidden-rows-columns.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/online/libreoffice-merged-cells.xml` | 3497 | `2b61d4c602903bdf487423ade31d5dca88efb8780ef80ade1db3498c988f0677` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/merged-cells.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/online/libreoffice-named-exp-local.xml` | 4707 | `8d5d55a030996da140b1b7ddfd6030fbfbf12fc6e59919efab2967e3647baa72` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/named-exp-local.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/online/libreoffice-tdf153444.xml` | 1320 | `8c6245b03f29dc92e08006ffd7dfbe132e58fd594e31a3fd77128ebf8bffde21` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/tdf153444.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/online/libreoffice-universal-content.xml` | 4478 | `591b971b2ac46fe34332111c32a0ff33fee150ea22222c0a2436a2ea81839aa7` | LibreOffice/core `19ed84a1d598206ab454dc96beffd26d6b5d4e83`, `sc/qa/unit/data/xml/universal-content.xml` | MPL-2.0 | SpreadsheetML 2003 import test of LibreOffice |
| `spreadsheetml/synthetic-workbook-saved-as.xls` | 1835 | `5605fa635e6c442a3cfe4f888564e4df5457ec95c4c1a83ae083c77e394c94e5` | `generate_spreadsheetml.py` | MIT | The same workbook with an .xls name |
| `spreadsheetml/synthetic-workbook.xml` | 1835 | `5605fa635e6c442a3cfe4f888564e4df5457ec95c4c1a83ae083c77e394c94e5` | `generate_spreadsheetml.py` | MIT | Two sheets: types, a comment, rich text, a link, ss:Index, MergeAcross, a formula, an error |
