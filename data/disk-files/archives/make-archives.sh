#!/bin/bash -ex

rm -rf generated
# avoided types: wim (is a concatenated text format, no compression)
for TYPE in zip gzip bzip2 7z xz ; do
  mkdir -p generated/split/$TYPE
  7z a -t$TYPE -v1K generated/split/$TYPE/x nlp-service || true
done


mkdir -p generated/split/rar1
rar a -v1K rar_split1 nlp-service
mv rar_split1.* generated/split/rar1

# Needs to happen on the Windows WinRAR client for -vn param:
# mkdir -p generated/split/rar2
# rar a -vn -v1K rar_split2 nlp-service
# mv rar_split2.* generated/split/rar2

rmdir generated/*/*

