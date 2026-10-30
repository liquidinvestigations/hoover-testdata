# Text spam samples

These files contain encoded binary data (base64, hex, uuencode) beside a small amount of
readable text. A text extractor that copies the encoded data into the stored text adds
bytes that no person searches for. The zip file shows a second defect: the text of an
archive repeats the text of its members.

## Source and license

A script generated every file with a fixed random seed. The files contain no third-party
content. The image data in the files is a 96 x 96 PNG of random pixels. The files are
released under CC0 1.0 (public domain dedication).

The generator is `scripts/make_text_spam_samples.py` at the repository root.
Run it with the output folder as its only argument.
Compressed bytes depend on the runtime zlib version.
The hashes below identify the stored samples.

## Files

| File | SHA-256 | Defect it shows |
|---|---|---|
| `vcard-photo.vcf` | `bfaeeb8ac3022bd9716538329e9ca679151b6051c0f3d9e740b516cafbf9a8fd` | A vCard `PHOTO` property holds a base64 image. 37,074 of 38,793 bytes are base64. Tika 4 returns the whole file as text. |
| `calendar-attach.ics` | `b36b2127526d35d051044a09a7ae34e82da1aed93c20484cd55a6b7614e76f79` | An iCalendar `ATTACH;ENCODING=BASE64` property holds an image. 37,074 of 38,947 bytes are base64. Tika 4 returns the whole file as text. |
| `html-data-uri.html` | `31eafc5194634f239ebfd00472296feb4315801c12a879926726d1774afe1abf` | An `<img>` element holds a `data:` URI. Tika 4 drops it. A reader that stores the HTML source keeps 37,092 bytes of base64. |
| `svg-data-uri.svg` | `30409997f1c32ac8e31b12bcf0f7eeee0c9ad021394510711c3ef46550f74b09` | An SVG `<image>` element holds a `data:` URI. Tika 4 returns only the 49 bytes of text. A reader of the XML source keeps the base64. |
| `rtf-pict-hex.rtf` | `fcb5cfe9fa4c56c198c2fd7b4782103211ec3ef0dd2195df7e8d1a8fc479f6e8` | A `\pict` group holds a PNG as hex. `file` reports `text/rtf`, so a reader that stores the source as plain text keeps 55,634 bytes of hex. Tika 4 returns 102 bytes. |
| `uuencoded-mail.txt` | `acf34dff51c01f93d9f5bc5c782a4ff6aeabe73cae346fdf1b6afd639ab9131c` | A plain mail body holds a uuencoded file. Tika 4 and a plain-text reader both keep 37,698 bytes of uuencoded lines. |
| `xbm-bitmap.xbm` | `a27be24393681c9e560222e50bdc85aa56a8e61bef0a360527d8953040ee61d8` | An X bitmap is C source of hex bytes. `file` reports `text/plain`. Tika 4 and a plain-text reader both keep 12,792 bytes of `0x..` values. |
| `archive-with-text-members.zip` | `787b04992ab1529416ac4ddb48075cee21bd2e9545f90212c548fa17c4e23065` | A zip with two text members. A parser that reads embedded documents stores the member text again as the text of the zip. Tika 4 with embedded documents skipped returns no text. |
