# Complete specification checkpoint

This checkpoint preserves the complete working specification as of local revision `668b25f436267014f171ed9c302c85a4c6ed6a1b`, including all final catalogs and navigation. The archive contains documentation and machine-readable specifications, with the Apache License preserved; it does not contain the original application repositories.

The archive is split only to fit upload limits. From the repository root, reconstruct and extract into a separate directory:

```sh
cat checkpoints/complete-specification.tar.gz.part-* > complete-specification.tar.gz
sha256sum complete-specification.tar.gz
mkdir restored-specification
tar -xzf complete-specification.tar.gz -C restored-specification
```

Expected archive checksum: `bf852d1a552aeeb42579cb2972dacb156f28198bc3349c18b07efff0d88b91b7`.

The expanded files in this checkpoint supersede the earlier catalogs visible in the branch. Their integration as individually reviewable files remains outstanding. The saved copy has zero `source-artifact-` occurrences in Markdown and structured catalogs, a reading guide in every documentation and schema directory, and the unchanged license. Detailed review coverage and remaining behavioral qualification limits are recorded inside it. A full application equivalence test has not been executed.
