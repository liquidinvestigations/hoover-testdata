Test data for [Hoover-Snoop](https://github.com/liquidinvestigations/hoover-snoop2)

* Emails in various formats (eml, emlx, msg, pst)
* Text and HTML files
* PDFs
* Office documents (pdf, doc, xls, ppt and their OpenDocument counterparts)
* Archives (zip, 7z, rar, tgz)
* PGP-encrypted emails

## Sources

Some files were downloaded from https://www.learningcontainer.com/ with
recursive curl. Only one type of each file is kept, using the following script:

```bash
for ext in $(find data/www.learningcontainer.com -type f | grep '\.[^.]*$' -o | sort -u); do \
find data/www.learningcontainer.com -type f -name "*$ext" | head -n -1
done
```

Other files were downloaded mercilessly from the public internet at undisclosed
times in the past, or supplied by the developers.
