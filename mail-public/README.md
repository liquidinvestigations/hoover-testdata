# Public mail test inputs

The files under `../data/mail-public/` are mail test inputs and attachment inputs.
The input directories contain no license files, reports, or test programs.

`manifest.json` records each upstream path, pinned revision, byte count, SHA-256,
stored path, and source license. A repeated file can refer to one stored copy.
The manifest keeps the original name for each repeated file.
Derived EML entries identify their parent mailbox, parent hash, message offset,
and newline conversion. The parent URL uses the source revision in the manifest.

The files retain their original bytes, except for the derived EML files.
Read the source notices under `notices/` before redistribution.
The license in the repository root does not replace these source terms.

The Apache Tika `testMBOX_lengthy_x-headers.mbox` header requests attribution
to EnronData.org under CC-BY-3.0-US. The `mbox-viewer` sample contains a resized
photo by Uroš Novina under CC-BY-2.0 and a W3C PDF. The manifest identifies
these files and gives their source links.
