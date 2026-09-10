# qa

Browser-suite and stack-verification fixtures that a checkout holds as committed
bytes. A clone at the revision the hoover4 QA contract pins is enough. Nothing
in this directory is generated at run time.

`datasets.json` maps each dataset name to its root inside this repository, the
purpose of the dataset, and the shape a check can assert.

Dataset roots that already live under `data/` stay there. The directories
beside this file hold fixtures that must be identical on every host.
`diskfiles/` is a small subset of `data/disk-files` for the rescan-control
capture. It does not include the `img` or `word` folders.
