# Restoring document state, attachment access and a numbering counter

A MariaDB and filesystem backup from a disposable reference site restored a private note, its two attachment records and their byte content into a separately provisioned site. The restored site resumed the sequence from the value at backup time. Its private download handler returned the original bytes to the administrator and HTTP 403 to both Guest and a newly created, unrelated website user. This experiment ran on the business and foundation packages with MariaDB 11.8.6. The [successful receipt](observed.json) and [failed path-layout control](absolute-root-control.json) record two different destination sites. [Business application revision](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264) · [Framework revision](https://github.com/frappe/frappe/tree/199a0385c00e572664a099a57a00be6ce7404eeb)

| Check | Source at snapshot | Source after snapshot | Restored target |
|---|---|---|---|
| Saved Note content | Committed before backup | Committed after backup | Committed before backup |
| Naming counter | Last value 0002 | Next allocation 0003 | Next allocation 0003 |
| Public attachment | 34 known bytes | Retained | Identical hash, original File identity, URL, privacy flag and parent link |
| Private attachment | 35 known bytes | Retained | Identical hash and original metadata; authorized read returned identical bytes |
| Physical database and connection | Distinct source database | Checked again after restore | A fresh connection opened the separate target database |

## Why the first restore failed the acceptance test

The first trial initialized the application with an **absolute** sites directory when constructing the backup. The file archiver embedded several ancestor directories in the member names. Native restore reported success for the database and both file archives, and the saved Note and public File metadata matched. Opening the public attachment through the restored record raised a missing-file error. Examination found both files, with correct hashes, beneath surplus source-path components in the destination. Neither file existed at its recorded target location. The trial stopped at that point. It did not check download authorization or counter continuity.

The file generator archives each site's `public/files` and `private/files` paths. The extractor removes two leading components from member paths. Native Bench site initialization defaults to a relative sites root. In the second trial, initialization from the Bench's `sites` directory used that default. Before consuming the new target, the runner verified that removing two components from each generated archive would produce the exact expected destination for its attachment. The fresh target then passed the table above. A replacement restore can check record-to-file mappings and SHA-256 values following extraction, even if its storage layout or archive format differs. [File backup](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/backups.py#L345) · [Extraction](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/installer.py#L1021)

## Transaction and access boundary

The runner commits the Note, website user, two File records and the first two naming allocations before the backup. It requires four nonempty outputs: SQL database image, public tar, private tar and site configuration snapshot. Only the SQL and two file archives are supplied to restore. The target retains its own database connection configuration. Once the snapshot exists, the source changes its Note and reserves another number. After restore, the runner reconnects, checks the database identity, verifies both attachments, and exercises the private download handler with distinct session identities. It then commits the target's first new sequence value and reconnects to the source to confirm the source's later Note and counter. The private download check calls the real handler with a local request environment. Public-file validation uses the stored record and filesystem. [Restore flow](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/commands/site.py#L220) · [Access-controlled download](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/utils/response.py#L294) · [Sequence update](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/naming.py#L408)

This is a quiescent, same-version, same-host logical restore to a separate MariaDB database and separate site directories. It tests full local SQL and tar backup, snapshot boundaries, private access and sequence continuity. Provider-managed storage, encrypted backup and site-key recovery, restoring secrets, point-in-time replay, simultaneous writes during capture, alternate database products, remote disaster recovery, HTTP proxy behavior and recovery-time objectives remain unqualified.

## Reproduce on a disposable Bench

Run the following Bash commands from a Bench already configured with the recorded revisions, MariaDB, Redis, the MariaDB and tar tools and the reference virtual environment. Supply a separate fresh pair of site names each time. The example derives both names from a random suffix, checks their absence, and provisions both before applying the experiment markers. A new target is required after a failed or successful restore. Use the same database administrator identity for provisioning and for restore. The runner reads its password from a private temporary file. The report written to the chosen directory contains measurements and hashes.

```bash
set -euo pipefail
umask 077
read -r -p 'Absolute blueprint checkout path: ' blueprint
bench_dir=$(pwd -P)
test -x "$bench_dir/env/bin/python"
test -d "$bench_dir/sites"
run_id=$("$bench_dir/env/bin/python" -c 'import secrets; print(secrets.token_hex(6))')
src="restore-source-$run_id.test"
dst="restore-target-$run_id.test"
test ! -e "$bench_dir/sites/$src"
test ! -e "$bench_dir/sites/$dst"
bench new-site "$src" --install-app erpnext
bench new-site "$dst" --install-app erpnext
for site in "$src" "$dst"; do
  bench --site "$site" set-config -p allow_tests True
  bench --site "$site" set-config -p blueprint_witness True
done
bench --site "$src" set-config -p blueprint_recovery_source True
bench --site "$dst" set-config blueprint_recovery_fresh_target "$src"
output_dir=$(mktemp -d)
secret_file=$(mktemp)
trap 'rm -f "$secret_file"' EXIT
read -r -s -p 'Local database administrator password: ' database_password
printf '\n'
printf '%s' "$database_password" > "$secret_file"
unset database_password
"$bench_dir/env/bin/python" -B "$blueprint/docs/rebuild/recovery-live/observe.py" \
  --sites-path "$bench_dir/sites" --source-site "$src" --fresh-target "$dst" \
  --db-root-password-file "$secret_file" --output "$output_dir/observed.json"
printf 'Observation file: %s\n' "$output_dir/observed.json"
```

Source and destination must have distinct physical databases. The runner checks both before claiming the destination, and uses exclusive file creation for the restore claim. The source backup archives and site configuration snapshot remain temporary. The [observation schema](observed.schema.json) defines successful receipt shape. The [offline audit](../verify/README.md) verifies the committed receipt and the two file hashes without performing a restore.
