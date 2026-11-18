# Assemble the complete blueprint for local reading

Browse the [September reading edition](september/README.md) directly on GitHub. It includes all 100 Markdown chapters and catalog indexes, the business calculations and 235 original JSON files. The [catalog guide](september/catalog-access.md) shows how to locate each bulk partition or read a single member.

To search all 3,476 original files together with the version-pinned [rebuild supplements](../docs/rebuild/README.md), use the following commands from the repository root. Python 3.8 or later is used only to unpack and verify documentation. Allow about 750 MiB of free space. Windows users can use `py -3` in place of `python3`.

```sh
python3 tools/restore-blueprint ../erpnext-blueprint-expanded
python3 tools/restore-blueprint --verify ../erpnext-blueprint-expanded
```

Open `../erpnext-blueprint-expanded/START-HERE.md`. Choose the complete checkpoint for the original rebuilding specification and machine-readable catalogs, or the rebuild supplements for the version-pinned domain contracts, source catalog and acceptance fixtures. Each group identifies its own observation date and source revision. A newer supplement may describe different behavior from the historic snapshot.

| Path inside the assembled edition | Contents |
|---|---|
| `README.md`, `docs/`, `schemas/` | All 3,476 regular files from the verified checkpoint, including its complete navigation. |
| `docs/rebuild/` | New branch documentation, inventories, schemas and examples. |
| `schemas/traceability/source-snapshot.json`, `schemas/source-file-distribution/` | Earlier source revisions and their artifact locators, used by supplements referring back to the archive boundary. |
| `checkpoints/september/` | The GitHub reading edition and member inventory, at the same paths used by links in the release supplements. |
| `START-HERE.md` | Navigation joining both sets of evidence. |

The restore assembles the 17 numbered parts in order, verifies SHA-256 `bf852d1a552aeeb42579cb2972dacb156f28198bc3349c18b07efff0d88b91b7`, and checks the archive's regular-file count. It writes only to a newly created output directory outside the repository. Choose an existing parent and an unused destination name. No external service or ERP installation is needed. A second restore to an existing directory fails, even if the directory is empty. An interrupted restore can leave a partial output with a `.restore-in-progress` marker. Use a fresh destination to retry.

The verification command reads the same checkout, authenticates the archive again, compares the individual file contents with their expected bytes and reports the first missing, differing or additional file. Run it before adding personal notes. To compare the same edition later, keep the exact branch commit used at assembly. When the branch advances, restore the new revision to a fresh directory. The checkout's archive parts and utility stay in the source checkout, while the expanded edition can be read independently.

For the September machine catalogs use the [corrected operation lookup](../docs/rebuild/checkpoint-corrections/README.md). It joins the original declarations with the recovered stock-controller records.
