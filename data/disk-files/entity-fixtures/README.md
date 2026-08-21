# entity-fixtures

A synthetic corpus for the identifier and date scanning path. Every file here is written
by `generate.py`; nothing in this directory was collected from a real document and no
file describes a real person, account or company.

## Provenance of the values

Each identifier is a published test vector carrying a valid check digit. They are taken
from the regex entity scanner's conformance corpus, which extracts them from upstream
projects' own test suites -- python-stdnum, libphonenumber, open-location-code,
price-parser, pyais, the GitHub advisory database, Crossref, isemail and the Microsoft
and Presidio recognizer suites. Each of those projects publishes its vectors as examples,
which is why they are safe to commit and why they are the right thing to test against:
a value that a validator's own author says is valid is the only value whose acceptance
proves the validator runs.

Four values are written from their specifications instead. Degrees/minutes/seconds
coordinates, ISO week dates and autonomous system numbers have no vector in the corpus
and no check digit either, so a specification example is as good as an extracted one.
The IMEI is the specification's own worked example because the corpus carries only a
sixteen-digit grouped serial, and an IMEI is fifteen digits -- eight of type allocation
code, six of serial and a Luhn check digit.

## Licence

The vectors are facts -- numbers with check digits -- rather than creative work, and each
upstream project publishes them as examples. The prose around them is written for this
directory and carries the repository's licence.

## What the corpus is shaped to exercise

* **Every rule the scanner ships fires at least once.** A rule that fires on no document
  is a rule nobody can tell is broken.
* **Five container formats** -- `.txt`, `.html`, `.eml`, `.docx`, `.pdf` -- so the same
  classes of value arrive through different parsers. The `.docx` and `.pdf` are written
  by hand, uncompressed and minimal, so what they prove does not depend on which
  decompressor a parser reached for.
* **Context words where a rule needs one.** Several validators require a nearby label --
  `BIC`, `PESEL`, `routing number`, `orgnr` -- and a bare list of numbers would exercise
  none of that. The values sit in prose that carries the label.
* **Ten money magnitudes in one document.** `remittance-advice.eml` carries one amount
  per order of magnitude so a magnitude facet has a bucket for each, rather than ten
  amounts inside one bucket.
* **Dates across centuries and across the Unix epoch.** `dates-across-centuries.txt`
  spans 1851 to 2029; several other files carry a pre-1970 date beside a recent one.
* **One document mentioning exactly two dates decades apart.**
  `two-distant-dates.txt` mentions 1936 and 2020 and nothing between. It is the fixture
  that separates a mentioned-date filter asking whether any single mention falls in
  range from one treating a document's mentions as an interval it occupies -- the second
  matches every year from 1936 to 2020, and is wrong. Without this document both
  predicates pass every test.

## Regenerating

    python3 generate.py <path-to>/regex_entity_scanner/tests/conformance
