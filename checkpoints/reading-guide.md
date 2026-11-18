# Reproduce a research observation

The [business chapters](../docs/README.md) and [machine catalogs](../schemas/README.md) are directly searchable in the checkout. To compare a retained research observation with its original bytes, run these commands from the repository root. Choose a new directory outside the checkout with about 750 MiB free.

```sh
python3 tools/restore-blueprint ../original-research
python3 tools/restore-blueprint --verify ../original-research
```

The reader authenticates all 17 numbered parts against SHA-256 `bf852d1a552aeeb42579cb2972dacb156f28198bc3349c18b07efff0d88b91b7` and restores the 3,476 original files. Verification reads the archive again, compares every file, and checks for extra files. The [member inventory](september/members.tsv) gives individual checksums. The [operation lookup](../docs/rebuild/checkpoint-corrections/README.md) uses the reconciled catalogs in the checkout for the applicable decision.
