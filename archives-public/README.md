# Split archive inputs

These folders hold multi-volume archives for the split archive reader.

| Folder | Volumes | Origin |
|---|---|---|
| `data/disk-files/archives/generated/split/7z` | `x.7z.001` to `x.7z.021` | generated earlier |
| `data/disk-files/archives/generated/split/rar1` | `rar_split1.part01.rar` to `part33.rar` | generated earlier |
| `data/disk-files/archives/generated/split/zip` | `x.zip.001` to `x.zip.029` | generated earlier |
| `data/disk-files/archives/generated/split/zipspan` | `zipspan.zip`, `zipspan.z01`, `zipspan.z02` | `zip -r -s 256k` over `data/disk-files/pdf-doc-txt` |
| `data/disk-files/archives/generated/split/7z-missing` | the `7z` set without `x.7z.010` | copy of the `7z` set |
| `data/disk-files/archives/public/rar-old` | `rar3-old.rar`, `rar3-old.r00`, `rar3-old.r01` | `test/files/` of `markokr/rarfile` at `d2f7df6fc843dae356fd6b0a85971dc36fd6e757` |

The `rar-old` files keep their upstream bytes. Their license is ISC, in `notices/rarfile/LICENSE`.
7-Zip with the RAR plugin reads all sets. It cannot write RAR, so the RAR sets are not generated here.
