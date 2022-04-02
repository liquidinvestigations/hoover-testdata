#!/bin/bash -ex


for TYPE in zip gzip bzip2 7z xz wim ; do
  mkdir -p generated/split/$TYPE
  7z a -t$TYPE -v1M generated/split/$TYPE/x p7zip-old || true
done

rmdir generated/*/*
