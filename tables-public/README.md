# Public JSON and JSONL table inputs

The files under `../data/tables-public/` are inputs for the JSON and JSONL table reader.
There are 20 JSON files and 20 JSONL files, and each file is smaller than 1 MB.

`manifest.json` records the upstream repository, pinned revision, upstream path, byte count,
SHA-256, stored path and source license of each file. The `kind` field is `json` or `jsonl`,
and it states the content. Some JSONL files keep an upstream `.json` name.

The files keep their upstream bytes, with one exception. Nine `.json.gz` and `.jsonl.gz`
files are stored decompressed. Their entries have `derived`, `upstream_bytes` and
`upstream_sha256`.

The set covers these shapes:

- top-level arrays of flat and nested objects
- objects that hold one or more arrays of objects
- objects keyed by name, with no array
- GeoJSON and TopoJSON
- STIX 2 bundles with mixed object types
- JSONL with nested arrays, annotation spans and keys that contain dots
- arrays of strings with unusual Unicode
- invalid inputs with very deep nesting, and a UTF-16 file with a byte order mark

Read the source notices under `notices/` before redistribution.
The license in the repository root does not replace these source terms.
The `zed-sample-data` files are CC-BY-SA-4.0.
