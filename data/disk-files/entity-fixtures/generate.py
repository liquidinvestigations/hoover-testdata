#!/usr/bin/env python3
"""Regenerate the entity fixture corpus in this directory.

Every identifier written here is a published test vector: it carries a valid check digit
and names nobody. The vectors are read from the regex entity scanner's conformance
corpus, which is itself extracted from upstream projects' own test suites, so the values
here are the values those projects publish as examples.

Usage::

    python3 generate.py <path-to>/regex_entity_scanner/tests/conformance

Four rules are written from their specifications instead of from the corpus:
degrees/minutes/seconds coordinates, ISO week dates and autonomous system numbers,
because none of the three carries a check digit and a specification example is as good
as an extracted one; and the IMEI, because the corpus's only vector is a sixteen-digit
grouped serial while an IMEI is fifteen digits, so the specification's own worked
example is the shorter route to a value the rule can actually see.

The corpus deliberately spreads dates across centuries and across the Unix epoch, and
one file mentions exactly two dates decades apart with nothing between them. That file
is what distinguishes a mentioned-date filter that asks whether any single mention falls
in range from one that treats a document's mentions as an interval it occupies: the
second matches every year between 1936 and 2020, and is wrong.
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections.abc import Callable
import zipfile

HERE = pathlib.Path(__file__).resolve().parent


def load_vectors(corpus_dir: pathlib.Path) -> dict[str, list[dict]]:
    """Valid vectors per rule id, deterministically ordered."""
    by_rule: dict[str, list[dict]] = {}
    for path in sorted(corpus_dir.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("valid") is not True or not row.get("rule_id"):
                continue
            by_rule.setdefault(row["rule_id"], []).append(row)
    for rows in by_rule.values():
        rows.sort(key=lambda r: r["id"])
    return by_rule


def take(
    vectors: dict[str, list[dict]],
    rule_id: str,
    count: int,
    keep: Callable[[str], bool] | None = None,
) -> list[str]:
    """The first `count` distinct tokens for a rule, optionally filtered.

    `keep` exists because the conformance corpus records the token as the upstream
    project wrote it, and several rules accept only a normalised spelling of what they
    then read: the non-EU VAT pattern has no separators in it, and the IMEI pattern is
    fifteen digits rather than the sixteen a grouped serial can be written with. A vector
    the pattern cannot see is a vector that proves nothing, so it is filtered out here
    rather than discovered as a rule that never fires.
    """
    rows = vectors.get(rule_id) or []
    seen: list[str] = []
    for row in rows:
        token = row["token"]
        if keep is not None and not keep(token):
            continue
        if token not in seen:
            seen.append(token)
        if len(seen) == count:
            return seen
    raise SystemExit(f"{rule_id}: fewer than {count} usable tokens (found {len(seen)})")


# ---------------------------------------------------------------------------
# Container formats, written without a dependency so this script runs anywhere.
# ---------------------------------------------------------------------------

def write_docx(path: pathlib.Path, paragraphs: list[str]) -> None:
    """A minimal but valid .docx: one document part and the two relationship parts."""
    def esc(text: str) -> str:
        return (
            text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

    body = "".join(
        f"<w:p><w:r><w:t xml:space='preserve'>{esc(p)}</w:t></w:r></w:p>"
        for p in paragraphs
    )
    document = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>"
        f"<w:body>{body}</w:body></w:document>"
    )
    content_types = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'>"
        "<Default Extension='rels' ContentType='application/vnd.openxmlformats-package.relationships+xml'/>"
        "<Default Extension='xml' ContentType='application/xml'/>"
        "<Override PartName='/word/document.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'/>"
        "</Types>"
    )
    rels = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>"
        "<Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument' Target='word/document.xml'/>"
        "</Relationships>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/document.xml", document)


def write_pdf(path: pathlib.Path, lines: list[str]) -> None:
    """A single-page PDF whose text is a stream of Tj operators over a base-14 font.

    Uncompressed on purpose: every text extractor handles it, and a fixture whose value
    depends on which decompressor a parser reached for proves less than it appears to.
    """
    def esc(text: str) -> str:
        return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    content = ["BT", "/F1 11 Tf", "14 TL", "40 780 Td"]
    for line in lines:
        content.append(f"({esc(line)}) Tj")
        content.append("T*")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", "replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_at}\n%%EOF\n"
    ).encode()
    path.write_bytes(bytes(out))


# ---------------------------------------------------------------------------
# The documents.
# ---------------------------------------------------------------------------

def build(vectors: dict[str, list[dict]]) -> dict[str, object]:
    iban = take(vectors, "bank.iban", 3)
    bic = take(vectors, "bank.bic", 2)
    card = take(vectors, "bank.payment_card", 2)
    aba = take(vectors, "bank.aba_routing", 2)
    lei = take(vectors, "company.lei", 1)
    vat_eu = take(vectors, "company.vat_eu", 3)
    # The pattern carries no separators, so a dotted or spaced spelling never matches.
    vat_non_eu = take(vectors, "company.vat_non_eu", 2, str.isalnum)
    orgnr = take(vectors, "company.se_organisationsnummer", 2)
    isin = take(vectors, "security.isin", 1)
    cusip = take(vectors, "security.cusip", 1)
    sedol = take(vectors, "security.sedol", 1)
    imo = take(vectors, "vessel.imo", 2)
    mmsi = take(vectors, "vessel.mmsi", 2)
    box = take(vectors, "container.iso6346", 1)
    # The conformance corpus's only IMEI vector is a sixteen-digit grouped serial, and
    # an IMEI is fifteen: eight digits of type allocation code, six of serial and a Luhn
    # check digit. This is the specification's own worked example, in its grouped form.
    imei = ["49-015420-323751-8"]
    mac = take(vectors, "device.mac", 2)
    ip = take(vectors, "network.ip", 3)
    cve = take(vectors, "vulnerability.cve", 3)
    doi = take(vectors, "publication.doi", 3)
    orcid = take(vectors, "publication.orcid", 2)
    msgid = take(vectors, "message.rfc5322", 2)
    coord = take(vectors, "coord.decimal", 2)
    plus = take(vectors, "coord.plus_code", 2)
    btc = take(vectors, "crypto.bitcoin", 2)
    eth = take(vectors, "crypto.ethereum", 2)
    cf = take(vectors, "natid.it_codice_fiscale", 1)
    nif = take(vectors, "natid.es_nif_nie", 2)
    curp = take(vectors, "natid.mx_curp", 1)
    pan = take(vectors, "natid.in_pan", 1)
    pesel = take(vectors, "natid.pl_pesel", 1)
    pnr = take(vectors, "natid.se_personnummer", 1)
    phone = take(vectors, "phone.international", 4)
    email = take(vectors, "email.basic", 4)
    rfc2822 = take(vectors, "date.rfc2822", 2)
    clf = take(vectors, "date.clf", 2)

    files: dict[str, object] = {}

    files["bank-payments-memo.txt"] = "\n".join([
        "INTERNAL MEMORANDUM -- TREASURY OPERATIONS",
        "",
        "Settlement instructions for the quarter are unchanged. Funds move from the",
        f"operating account, IBAN {iban[0]}, to the escrow account held at the",
        f"correspondent bank under BIC {bic[0]}. The secondary escrow line, IBAN",
        f"{iban[1]}, stays dormant until the audit closes.",
        "",
        f"Domestic transfers use routing number {aba[0]}; the payroll bureau still",
        f"quotes routing number {aba[1]} on its remittance files and both are correct.",
        "",
        "The corporate card programme was re-issued this month. The test card the",
        f"processor gave us for the certification run is {card[0]}, and the second",
        f"certification card is {card[1]}. Neither is a live account.",
        "",
        "Fees for the period were USD 4200 for custody and EUR 950 for the transfer",
        "network. The audit engagement is quoted at USD 85000 and the litigation",
        "reserve stands at USD 2400000. Petty cash reconciles to USD 84 exactly.",
        "",
        "The same figures as the ledger prints them, with the symbol rather than the",
        "code: $94,000 settled last quarter, a $48.2 million facility remains undrawn,",
        "and the sterling leg is \u00a32,400,000.",
        "",
        f"Queries to treasury-ops@example.org or {email[0]}.",
        "",
        f"European counterparty IBAN {iban[2]} is quoted for reference only; the",
        f"receiving institution is identified by BIC {bic[1]}.",
    ])

    files["company-registry-extract.html"] = "\n".join([
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'><title>Registry extract</title></head>",
        "<body>",
        "<h1>Counterparty registry extract</h1>",
        "<p>The entity is registered with the legal entity identifier",
        f"{lei[0]}, which resolves through the global index.</p>",
        "<table>",
        "<tr><th>Jurisdiction</th><th>Registration</th></tr>",
        f"<tr><td>European Union</td><td>{vat_eu[0]}</td></tr>",
        f"<tr><td>European Union</td><td>{vat_eu[1]}</td></tr>",
        f"<tr><td>European Union</td><td>{vat_eu[2]}</td></tr>",
        f"<tr><td>Third country</td><td>{vat_non_eu[0]}</td></tr>",
        f"<tr><td>Third country</td><td>{vat_non_eu[1]}</td></tr>",
        f"<tr><td>Sweden</td><td>orgnr {orgnr[0]}</td></tr>",
        f"<tr><td>Sweden, dormant subsidiary</td><td>orgnr {orgnr[1]}</td></tr>",
        "</table>",
        "<p>The registered office moved on 1994-03-17 and the current filing was",
        "accepted on 2018-11-02. Correspondence goes to",
        f"<a href='mailto:{email[1]}'>{email[1]}</a>.</p>",
        "</body></html>",
    ])

    files["securities-position-note.txt"] = "\n".join([
        "POSITION NOTE -- CUSTODY RECONCILIATION",
        "",
        f"The equity line is held under {isin[0]}, which the custodian reports",
        f"against CUSIP {cusip[0]}. The London leg carries SEDOL {sedol[0]}.",
        "",
        "Market value at the close was USD 310000 against a book cost of",
        "USD 250000. The unrealised gain of USD 60000 is unhedged.",
        "",
        "Three settlement dates matter for this line: 1987-10-19, 2008-09-15 and",
        "2020-03-16. Nothing settled between them under this identifier.",
    ])

    files["shipping-manifest.txt"] = "\n".join([
        "CARGO MANIFEST -- COASTAL SERVICE",
        "",
        f"Carrying vessel: IMO {imo[0].split()[-1]}, calling under MMSI {mmsi[0]}.",
        f"Relief vessel on the return leg is IMO {imo[1].split()[-1]}, MMSI {mmsi[1]}.",
        "",
        f"One forty-foot box, {box[0].upper()}, is loaded at the forward hatch.",
        "",
        "Freight is invoiced at EUR 25000 per rotation with a bunker surcharge of",
        "EUR 4100. Demurrage accrues at EUR 950 per day after the free period.",
        "",
        "The charter party is dated 1974-06-30 and the current addendum 2011-09-08.",
        "",
        f"Agency contact: {phone[0]} or {email[2]}.",
    ])

    files["national-identifiers.txt"] = "\n".join([
        "HR FILE NOTE -- CROSS-BORDER SECONDMENT PAPERWORK",
        "",
        "Every number below is a published specification example. No employee record",
        "is described here.",
        "",
        f"Italy: the codice fiscale on the specimen form is {cf[0]}.",
        f"Spain: the specimen NIF is {nif[0]} and the specimen NIE is {nif[1]}.",
        f"Mexico: the CURP shown in the training pack is {curp[0]}.",
        f"India: the PAN quoted in the tax annex is PAN {pan[0]}.",
        f"Poland: the PESEL used in the worked example is PESEL {pesel[0]}.",
        f"Sweden: the personnummer in the same example is personnummer {pnr[0]}.",
        "",
        "The pack was last revised on 1968-04-02 and reissued on 2015-07-21.",
        f"Questions to {email[3]} or {phone[1]}.",
    ])

    files["security-incident.eml"] = "\r\n".join([
        "From: Security Operations <secops@example.org>",
        "To: Infrastructure <infra@example.org>",
        f"Date: {rfc2822[0]}",
        f"Message-ID: <{msgid[0].strip('<>')}>",
        "Subject: Weekly advisory round-up and one live finding",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
        "",
        "Three advisories apply to the estate this week:",
        "",
        f"  * {cve[0]} -- the edge proxy, patched.",
        f"  * {cve[1]} -- the document converter, patch pending.",
        f"  * {cve[2]} -- the mail relay, not applicable to our build.",
        "",
        f"The scan came from {ip[0]} and was relayed through {ip[1]}. The",
        f"originating range is announced by AS15169, and a second probe from {ip[2]}",
        "came out of AS64512, which is a private range and should never appear on the",
        "public side.",
        "",
        f"The device on the affected port reports MAC {mac[0]}; the spare unit is",
        f"{mac[1]}. The handset issued to the on-call engineer has IMEI {imei[0]}.",
        "",
        f"Thread continues from <{msgid[1].strip('<>')}>.",
        "",
        f"On-call: {phone[2]}. Escalation to {phone[3]}.",
        "",
        "The remediation budget for the quarter is USD 45000.",
    ])

    files["research-bibliography.html"] = "\n".join([
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'><title>Bibliography</title></head>",
        "<body><h1>Working bibliography</h1>",
        "<ol>",
        f"<li>Reference one, {doi[0]}, contributed by ORCID {orcid[0]}.</li>",
        f"<li>Reference two, {doi[1]}.</li>",
        f"<li>Reference three, {doi[2]}, contributed by ORCID {orcid[1]}.</li>",
        "</ol>",
        "<p>The reading list was assembled on 2021-01-11 and last checked on",
        "2024-05-30. The oldest item in the series dates from 1899-12-31.</p>",
        "</body></html>",
    ])

    files["field-survey-coordinates.txt"] = "\n".join([
        "FIELD SURVEY -- STATION LOG",
        "",
        # No comma after the pair: a decimal coordinate is itself comma-separated, and a
        # third comma turns the whole run into something the pattern will not read.
        f"Station A sits at {coord[0]} (WGS84), recorded by handheld receiver.",
        f"Station B sits at {coord[1]} (WGS84).",
        "",
        "The theodolite log gives two more stations in sexagesimal form:",
        "41\u00b024'12.2\"N 2\u00b010'26.5\"E and 51\u00b028'40.1\"N 0\u00b000'05.3\"W.",
        "",
        f"The depot is at plus code {plus[0]} and the fuel cache at {plus[1]}.",
        "",
        "Occupation dates were 1955-08-14 for the first pass and 2019-04-22 for the",
        "re-survey. The intervening years hold no observation under this station id.",
    ])

    files["treasury-wallet-ledger.txt"] = "\n".join([
        "DIGITAL ASSET LEDGER -- TEST NET RECONCILIATION",
        "",
        f"The receiving address used throughout the drill is {btc[0]}.",
        f"Change was swept to {btc[1]}.",
        "",
        f"The contract wallet on the account chain is {eth[0]}, and the fee payer",
        f"is {eth[1]}.",
        "",
        "Nominal value moved during the drill was USD 0.50, then USD 7, then",
        "USD 950, then USD 250000000 on the final settlement leg. The last figure is",
        "notional and was never funded.",
        "",
        "The drill ran on 2022-10-05. The procedure it replaced was written 1998-02-09.",
    ])

    files["dates-across-centuries.txt"] = "\n".join([
        "ARCHIVE ACCESSION NOTE",
        "",
        "The series is not continuous, and the accession record names every year the",
        "box actually contains. Written out so a date filter has something to bite on",
        "either side of the Unix epoch:",
        "",
        "  1851-05-01 -- the earliest item, a printed circular.",
        "  1889-03-31 -- correspondence, two folders.",
        "  1912-04-15 -- a single telegram.",
        "  1936-11-20 -- the ledger opens.",
        "  1945-08-15 -- the ledger closes.",
        "  1961-01-20 -- an inventory sheet.",
        "  1969-07-20 -- a press cutting.",
        "  1977-06-07 -- a photograph, captioned.",
        "  1989-11-09 -- a second press cutting.",
        "  2001-09-11 -- a memorandum.",
        "  2014-02-28 -- the digitisation worksheet.",
        "  2029-12-31 -- the review date the policy sets for this series.",
        "",
        "Nothing in the box is dated between 1912 and 1936, or between 1945 and 1961.",
    ])

    files["two-distant-dates.txt"] = "\n".join([
        "SINGLE-ITEM CATALOGUE CARD",
        "",
        "This card mentions exactly two dates and nothing between them.",
        "",
        "The instrument was manufactured in 1936-11-20 and was decommissioned on",
        "2020-06-15. It was in continuous storage for the whole of the intervening",
        "period and produced no record of any kind.",
        "",
        "A filter asking whether this document mentions a date in 2005 must not match",
        "it. A filter asking whether the document's own span covers 2005 would, and",
        "that is a different question from the one the mentions answer.",
    ])

    files["machine-timestamps.txt"] = "\n".join([
        "GATEWAY LOG EXTRACT -- MACHINE-WRITTEN TIMESTAMPS ONLY",
        "",
        "Mail headers as received:",
        f"  Date: {rfc2822[0]}",
        f"  Date: {rfc2822[1]}",
        "",
        "Web log lines as written:",
        f"  10.0.0.7 - - {clf[0]} \"GET /index.html HTTP/1.1\" 200 1043",
        f"  10.0.0.9 - - {clf[1]} \"GET /report.pdf HTTP/1.1\" 200 88213",
        "",
        "Release train, in ISO week form:",
        "  2019-W14-1 cut the branch.",
        "  2021-W53-7 was the last day of the long year.",
        "  2024-W09-3 shipped.",
    ])

    files["remittance-advice.eml"] = "\r\n".join([
        "From: Accounts Payable <ap@example.org>",
        "To: Supplier Ledger <ledger@example.net>",
        f"Date: {rfc2822[1]}",
        f"Message-ID: <{msgid[0].strip('<>')}>",
        "Subject: Remittance advice, ten lines",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
        "",
        f"Payment is on its way to IBAN {iban[0]} at BIC {bic[0]}.",
        "",
        "The advice covers ten lines, deliberately one per order of magnitude so a",
        "magnitude facet has a bucket for each:",
        "",
        "  line 1   USD 0.40",
        "  line 2   USD 7",
        "  line 3   USD 84",
        "  line 4   USD 950",
        "  line 5   USD 4200",
        "  line 6   USD 25000",
        "  line 7   USD 310000",
        "  line 8   USD 2400000",
        "  line 9   USD 45000000",
        "  line 10  USD 250000000",
        "",
        "The euro leg is smaller: EUR 12 and EUR 4100.",
        "",
        "Value date 2023-03-14. The framework agreement is dated 1966-10-01.",
    ])

    files["invoice-batch.docx"] = ("docx", [
        "INVOICE BATCH COVER SHEET",
        f"Remit to IBAN {iban[1]}, BIC {bic[1]}.",
        "Batch total USD 310000 across eleven invoices.",
        "The largest single invoice is USD 85000 and the smallest is USD 12.",
        f"Queries to {email[0]} or {phone[0]}.",
        "Batch date 2017-05-09. The oldest invoice in the batch is dated 1979-01-15.",
    ])

    files["contract-annex.pdf"] = ("pdf", [
        "ANNEX C -- PAYMENT AND NOTICES",
        "",
        f"C.1  Payments are made to IBAN {iban[2]} at BIC {bic[0]}.",
        "C.2  The annual fee is USD 45000, payable in four instalments.",
        "C.3  The cap on aggregate liability is USD 2400000.",
        "C.4  The de minimis threshold is USD 950.",
        "",
        f"C.5  Notices go to {email[1]} and by telephone to {phone[1]}.",
        "",
        "C.6  This annex replaces the annex of 1971-11-30 and takes effect on",
        "     2016-08-01.",
    ])

    return files


README = """# entity-fixtures

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
"""


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    corpus_dir = pathlib.Path(sys.argv[1]).resolve()
    vectors = load_vectors(corpus_dir)
    files = build(vectors)
    for name, payload in files.items():
        path = HERE / name
        if isinstance(payload, str):
            path.write_text(payload + "\n", encoding="utf-8")
        else:
            kind, lines = payload
            if kind == "docx":
                write_docx(path, lines)
            elif kind == "pdf":
                write_pdf(path, lines)
            else:
                raise SystemExit(f"unknown payload kind {kind!r}")
        print(f"wrote {name}")
    (HERE / "README.md").write_text(README, encoding="utf-8")
    print("wrote README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
