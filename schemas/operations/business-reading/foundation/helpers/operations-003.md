# Shared value and file services · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Backups

<a id="op-2d77169fb4b560"></a>
### Backup Generator.set backup tables from config

`operation_foundation_utils_backups_business_behavior_backup_generator_set_backup_tables_from_configuration`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.ignore\_conf.
  - Return no value.
- Set backup\_conf from Platform.conf.get(“backup”, mapping()).
- Evaluate self.\_set\_existing\_tables().
- If not self.backup\_includes.
  - If specified\_tables bound to \_get\_tables(backup\_conf.get(“includes”, list()), self.\_existing\_tables).
    - Set self.backup\_includes from (specified\_tables + base\_tables).
  - Otherwise.
    - Set self.backup\_includes from list().
- If not self.backup\_excludes.
  - Set self.backup\_excludes from \_get\_tables(backup\_conf.get(“excludes”, list()), self.\_existing\_tables).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set existing tables](operations-002.md#op-32ad6fc863aefc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L69) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1515)

<a id="op-adcf8d0afc7f28"></a>
### Backup Generator.site config backup path

`operation_foundation_utils_backups_business_behavior_backup_generator_site_configuration_backup_path`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** getattr(self, “backup\_path\_conf”, no value).

**Local steps**

- Evaluate click.secho(“BackupGenerator.site\_config\_backup\_path has been deprecated in favour of BackupGenerator.backup\_path\_conf”, fg = “yellow”).
- Return getattr(self, “backup\_path\_conf”, no value).

**Values supplied outside this operation** selected callable from getattr(self, “backup\_path\_conf”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L6928) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1519)

<a id="op-706cb83733ef30"></a>
### Backup Generator.get backup

`operation_foundation_utils_backups_business_behavior_backup_generator_get_backup`

**Inputs** self, older\_than = 24, ignore\_files = false, force = false.

**Local steps**

- If not force.
  - Set tuple(last\_db, last\_file, last\_private\_file, site\_config\_backup\_path) from self.get\_recent\_backup(older\_than).
- Otherwise.
  - Set tuple(last\_db, last\_file, last\_private\_file, site\_config\_backup\_path) from tuple(false, false, false, false).
- If not (self.backup\_path\_conf and self.backup\_path\_db and self.backup\_path\_files and self.backup\_path\_private\_files).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.backup\_path\_conf → self.backup\_path\_db → self.backup\_path\_files → self.backup\_path\_private\_files.
  - Evaluate self.set\_backup\_file\_name().
- If not (last\_db and last\_file and last\_private\_file and site\_config\_backup\_path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_db → last\_file → last\_private\_file → site\_config\_backup\_path.
  - Evaluate self.delete\_if\_step\_fails(self.take\_dump, self.backup\_path\_db).
  - Evaluate self.delete\_if\_step\_fails(self.copy\_site\_config, self.backup\_path\_conf).
  - If not ignore\_files.
    - Evaluate self.delete\_if\_step\_fails(self.backup\_files, self.backup\_path\_files, self.backup\_path\_private\_files).
  - If Platform.get\_system\_settings(“encrypt\_backup”).
    - Evaluate self.backup\_encryption().
- Otherwise.
  - Set self.backup\_path\_files from last\_file.
  - Set self.backup\_path\_db from last\_db.
  - Set self.backup\_path\_private\_files from last\_private\_file.
  - Set self.backup\_path\_conf from site\_config\_backup\_path.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get recent backup](operations-003.md#op-8b7cb7027a0d50), [set backup file name](operations-003.md#op-df658bb6ca809e), [delete if step fails](operations-003.md#op-bdb93b376a435f), [backup encryption](operations-003.md#op-e5fd296aa90b95).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“encrypt\_backup”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L7023) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1505)

<a id="op-df658bb6ca809e"></a>
### Backup Generator.set backup file name

`operation_foundation_utils_backups_business_behavior_backup_generator_set_backup_file_name`

**Inputs** self.

**Local steps**

- Set partial from “-partial” when self.partial, otherwise empty text.
  - Value choice on self.partial — true gives “-partial”, false gives empty text.
- Set ext from “tgz” when self.compress\_files, otherwise “tar”.
  - Value choice on self.compress\_files — true gives “tgz”, false gives “tar”.
- Set enc from “-enc” when Platform.get\_system\_settings(“encrypt\_backup”), otherwise empty text.
  - Value choice on Platform.get\_system\_settings(“encrypt\_backup”) — true gives “-enc”, false gives empty text.
- Set self.todays\_date from now\_datetime().strftime(“%Y%m%d\_%H%M%S”).
- Set for\_conf from formatted text {self.todays\_date}-{self.site\_slug}-site\_config\_backup{enc}.json.
- Set for\_db from formatted text {self.todays\_date}-{self.site\_slug}{partial}-database{enc}.sql.gz.
- Set for\_public\_files from formatted text {self.todays\_date}-{self.site\_slug}-files{enc}.{ext}.
- Set for\_private\_files from formatted text {self.todays\_date}-{self.site\_slug}-private-files{enc}.{ext}.
- Set backup\_path from (self.backup\_path or get\_backup\_path()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.backup\_path → get\_backup\_path().
- If not self.backup\_path\_conf.
  - Set self.backup\_path\_conf from os.path.join(backup\_path, for\_conf).
- If not self.backup\_path\_db.
  - Set self.backup\_path\_db from os.path.join(backup\_path, for\_db).
- If not self.backup\_path\_files.
  - Set self.backup\_path\_files from os.path.join(backup\_path, for\_public\_files).
- If not self.backup\_path\_private\_files.
  - Set self.backup\_path\_private\_files from os.path.join(backup\_path, for\_private\_files).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“encrypt\_backup”) · clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1514)

<a id="op-e5fd296aa90b95"></a>
### Backup Generator.backup encryption

`operation_foundation_utils_backups_business_behavior_backup_generator_backup_encryption`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** self.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L751) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1501)

<a id="op-8b7cb7027a0d50"></a>
### Backup Generator.get recent backup

`operation_foundation_utils_backups_business_behavior_backup_generator_get_recent_backup`

**Inputs** self, older\_than, partial = false.

**Explicit results** tuple(recent\_backups.get(“database”), recent\_backups.get(“public”), recent\_backups.get(“private”), recent\_backups.get(“config”)).

**Local steps**

- Set backup\_path from get\_backup\_path().
- Set separator, suffix from empty text.
- If partial.
  - Set separator from “\*”.
- If Platform.get\_system\_settings(“encrypt\_backup”).
  - Set suffix from “-enc”.
- Set file\_type\_slugs from mapping(“database” → formatted text \*-{}-{separator}database{suffix}.sql.gz, “public” → formatted text \*-{}-files{suffix}.tar, “private” → formatted text \*-{}-private-files{suffix}.tar, “config” → formatte ….
- Bind local operation backup\_time for subsequent calls.
- Bind local operation get\_latest for subsequent calls.
- Bind local operation old\_enough for subsequent calls.
- Set latest\_backups from mapping of file\_type → get\_latest(pattern) for tuple(file\_type, pattern) drawn from file\_type\_slugs.items().
  - Draw tuple(file\_type, pattern) from file\_type\_slugs.items().
- Set recent\_backups from mapping of file\_type → old\_enough(file\_name) for tuple(file\_type, file\_name) drawn from latest\_backups.items().
  - Draw tuple(file\_type, file\_name) from latest\_backups.items().
- Return tuple(recent\_backups.get(“database”), recent\_backups.get(“public”), recent\_backups.get(“private”), recent\_backups.get(“config”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“encrypt\_backup”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L1153) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1506)

<a id="op-5662bdf880e364"></a>
### Backup Generator.get recent backup.backup time

`operation_foundation_utils_backups_business_behavior_backup_generator_get_recent_backup_backup_time`

**Inputs** file\_path.

**Explicit results** timegm(datetime.strptime(file\_timestamp, “%Y%m%d\_%H%M%S”).utctimetuple()).

**Local steps**

- Set file\_name from file\_path.split(os.sep) at negative 1.
- Set file\_timestamp from file\_name.split(“-”, 1) at 0.
- Return timegm(datetime.strptime(file\_timestamp, “%Y%m%d\_%H%M%S”).utctimetuple()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L2111) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1507)

<a id="op-65152443df63fe"></a>
### Backup Generator.get recent backup.get latest

`operation_foundation_utils_backups_business_behavior_backup_generator_get_recent_backup_get_latest`

**Inputs** file\_pattern.

**Explicit results** max(file\_list, key = backup\_time).

**Local steps**

- Set file\_pattern from os.path.join(backup\_path, file\_pattern.format(self.site\_slug)).
- Set file\_list from glob(file\_pattern).
- If file\_list.
  - Return max(file\_list, key = backup\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L2276) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1508)

<a id="op-f552dae1a9ea01"></a>
### Backup Generator.get recent backup.old enough

`operation_foundation_utils_backups_business_behavior_backup_generator_get_recent_backup_old_enough`

**Inputs** file\_path.

**Explicit results** no value · file\_path.

**Local steps**

- If file\_path.
  - If (not os.path.isfile(file\_path) or is\_file\_old(file\_path, older\_than)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not os.path.isfile(file\_path) → is\_file\_old(file\_path, older\_than).
    - Return no value.
  - Return file\_path.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L2428) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1509)

<a id="op-33c96204f695ec"></a>
### Backup Generator.zip files

`operation_foundation_utils_backups_business_behavior_backup_generator_zip_files`

**Inputs** self.

**Explicit results** self.backup\_files().

**Local steps**

- Evaluate click.secho(“BackupGenerator.zip\_files has been deprecated in favour of BackupGenerator.backup\_files”, fg = “yellow”).
- Return self.backup\_files().

**Methods declared on this owner** [backup files](operations-003.md#op-441f53682d882d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L2545) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1521)

<a id="op-20316cea3fb5da"></a>
### Backup Generator.get summary

`operation_foundation_utils_backups_business_behavior_backup_generator_get_summary`

**Inputs** self.

**Explicit results** summary.

**Local steps**

- Set summary from mapping(“config” → mapping(“path” → self.backup\_path\_conf, “size” → get\_file\_size(self.backup\_path\_conf, format = true)), “database” → mapping(“path” → self.backup\_path\_db, “size” → get\_file\_size(self.back ….
- If (os.path.exists(self.backup\_path\_files) and os.path.exists(self.backup\_path\_private\_files)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(self.backup\_path\_files) → os.path.exists(self.backup\_path\_private\_files).
  - Evaluate summary.update(mapping(“public” → mapping(“path” → self.backup\_path\_files, “size” → get\_file\_size(self.backup\_path\_files, format = true)), “private” → mapping(“path” → self.backup\_path\_private\_files, “size ….
- Return summary.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L2630) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1510)

<a id="op-891605702dd0bb"></a>
### Backup Generator.print summary

`operation_foundation_utils_backups_business_behavior_backup_generator_print_summary`

**Inputs** self.

**Local steps**

- Set backup\_summary from self.get\_summary().
- Evaluate print(formatted text Backup Summary for {Platform.local.site} at {now()}).
- Set title from max(generator of len(x) for x drawn from backup\_summary).
  - Draw x from backup\_summary.
- Set path from max(generator of len(x at “path”) for x drawn from backup\_summary.values()).
  - Draw x from backup\_summary.values().
- For each tuple(\_type, info) in backup\_summary.items().
  - Set template from formatted text {0:{title}}: {1:{path}} {2}.
  - Evaluate print(template.format(\_type.title(), os.path.abspath(info at “path”), info at “size”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get summary](operations-003.md#op-20316cea3fb5da).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L3094) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1512)

<a id="op-441f53682d882d"></a>
### Backup Generator.backup files

`operation_foundation_utils_backups_business_behavior_backup_generator_backup_files`

**Inputs** self.

**Explicit failure paths** e.

**Local steps**

- For each folder in tuple(“public”, “private”).
  - Set files\_path from Platform.get\_site\_path(folder, “files”).
  - Set backup\_path from self.backup\_path\_files when folder equals “public”, otherwise self.backup\_path\_private\_files.
    - Value choice on folder equals “public” — true gives self.backup\_path\_files, false gives self.backup\_path\_private\_files.
  - If self.compress\_files.
    - Set cmd\_string from “set -o pipefail; tar cf - {1} \| gzip &gt; {0}”.
  - Otherwise.
    - Set cmd\_string from “tar -cf {0} {1}”.
  - Attempt the following.
    - Evaluate Platform.utils.execute\_in\_shell(cmd\_string.format(backup\_path, files\_path), verbose = self.verbose, low\_priority = true, check\_exit\_code = true).
  - On failure (Platform.CommandFailedError) bound to e.
    - If (e.err and “file changed as we read it” belongs to e.err).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.err → “file changed as we read it” belongs to e.err.
      - Evaluate click.secho(“Ignoring ′tar: file changed as we read it′ to prevent backup failure”, fg = “red”).
    - Otherwise.
      - Raise e.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L3530) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1502)

<a id="op-8d62f861c6ed97"></a>
### Backup Generator.copy site config

`operation_foundation_utils_backups_business_behavior_backup_generator_copy_site_configuration`

**Inputs** self.

**Local steps**

- Set site\_config\_backup\_path from self.backup\_path\_conf.
- Set site\_config\_path from os.path.join(Platform.get\_site\_path(), “site\_config.json”).
- Within open(site\_config\_backup\_path, “w”) bound as n, open(site\_config\_path) bound as c.
  - Evaluate n.write(c.read()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L3907) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1503)

<a id="op-bed7512cfe50a7"></a>
### Backup Generator.take dump

`operation_foundation_utils_backups_business_behavior_backup_generator_take_dump`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ExecutableNotFound — translated “gzip not found in PATH! This is required to take a backup.” · validation helper with Platform.ExecutableNotFound — translated “{} not found in PATH! This is required to take a backup.”.format(bin\_name).

**Local steps**

- If self.db\_type equals “sqlite”.
  - Bind dependencies Path.
  - Bind dependencies Platform.
  - Set db\_path from ((Path(Platform.get\_site\_path()) ÷ “db”) ÷ formatted text {self.db\_name}.db).
  - Set command from formatted text gzip -k {db\_path} -c &gt; {self.backup\_path\_db}.
  - Evaluate Platform.utils.execute\_in\_shell(command, low\_priority = true, check\_exit\_code = true).
  - Return no value.
- Bind dependencies shlex.
- Bind dependencies Platform.utils.
- Bind dependencies get\_app\_branch.
- Set gzip\_exc from which(“gzip”).
- If not gzip\_exc.
  - Call the validation error handler Platform.throw(translated “gzip not found in PATH! This is required to take a backup.”, exc = Platform.ExecutableNotFound).
- If self.old\_backup\_metadata.
  - Set database\_header\_content from list(formatted text Backup generated by Platform {Platform.\_\_version\_\_} on branch {(get\_app\_branch(“Platform”) or “N/A”)}, empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_app\_branch(“Platform”) → “N/A”.
- Otherwise.
  - Set database\_header\_content from list(“begin Platform metadata”, “&#91;Platform&#93;”, formatted text version = {Platform.\_\_version\_\_}, formatted text branch = {(get\_app\_branch(“Platform”) or “N/A”)}, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_app\_branch(“Platform”) → “N/A”.
- If self.backup\_includes.
  - Set backup\_info from tuple(“Backing Up Tables: ”, “, ”.join(self.backup\_includes)).
- Otherwise.
  - If self.backup\_excludes.
    - Set backup\_info from tuple(“Skipping Tables: ”, “, ”.join(self.backup\_excludes)).
- If self.partial.
  - If self.verbose.
    - Evaluate print(empty text.join(backup\_info), whitespace '\\n').
  - Evaluate database\_header\_content.extend(list(formatted text Partial Backup of Platform Site {Platform.local.site}, (“Backup contains: ” when self.backup\_includes, otherwise “Backup excludes: ” + backup\_info at 1),  ….
    - Value choice on self.backup\_includes — true gives “Backup contains: ”, false gives “Backup excludes: ”.
- Set generated\_header from (whitespace '\\n'.join(generator of formatted text -- {x} for x drawn from database\_header\_content) + whitespace '\\n').
  - Draw x from database\_header\_content.
- Within gzip.open(self.backup\_path\_db, “wt”) bound as f.
  - Evaluate f.write(generated\_header).
- Set cmd from list().
- Set extra from list().
- If self.db\_type equals “mariadb”.
  - If self.backup\_includes.
    - Evaluate extra.extend(self.backup\_includes).
  - Otherwise.
    - If self.backup\_excludes.
      - Evaluate extra.extend(list of formatted text --ignore-table={self.db\_name}.{table} for table drawn from self.backup\_excludes).
        - Draw table from self.backup\_excludes.
- Otherwise.
  - If self.db\_type equals “postgres”.
    - If self.backup\_includes.
      - Evaluate extra.extend(list of formatted text --table=public."{table}" for table drawn from self.backup\_includes).
        - Draw table from self.backup\_includes.
    - Otherwise.
      - If self.backup\_excludes.
        - Evaluate extra.extend(list of formatted text --exclude-table-data=public."{table}" for table drawn from self.backup\_excludes).
          - Draw table from self.backup\_excludes.
- Bind dependencies get\_command.
- Set tuple(bin, args, bin\_name) from get\_command(socket = self.db\_socket, host = self.db\_host, port = self.db\_port, user = self.user, …).
- If not bin.
  - Call the validation error handler Platform.throw(translated “{} not found in PATH! This is required to take a backup.”.format(bin\_name), exc = Platform.ExecutableNotFound).
- Evaluate cmd.append(bin).
- Evaluate cmd.append(shlex.join(args)).
- Set command from one space.join(list(“set -o pipefail;”, expanded cmd, “\|”, gzip\_exc, …)).
- If self.verbose.
  - Evaluate print((command.replace(shlex.quote(self.password), (“\*” × 10)) + whitespace '\\n')).
- Evaluate Platform.utils.execute\_in\_shell(command, low\_priority = true, check\_exit\_code = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L4092) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1520)

<a id="op-04601f1411682e"></a>
### Backup Generator.send email

`operation_foundation_utils_backups_business_behavior_backup_generator_send_email`

**Inputs** self.

**State and service calls** sendmail.

**Explicit results** recipient\_list.

**Local steps**

- Bind dependencies get\_system\_managers.
- Set recipient\_list from get\_system\_managers().
- Set db\_backup\_url from get\_url(os.path.join(“backups”, os.path.basename(self.backup\_path\_db))).
- Set files\_backup\_url from get\_url(os.path.join(“backups”, os.path.basename(self.backup\_path\_files))).
- Set msg from formatted text Hello,  Your backups are ready to be downloaded.  1. &#91;Click here to download the database backup&#93;({db\_backup\_url}) 2. &#91;Click here to download the file.
- Set datetime\_str from datetime.fromtimestamp(os.stat(self.backup\_path\_db).st\_ctime).
- Set subject from (datetime\_str.strftime(“%d/%m/%Y %H:%M:%S”) + “ - Backup ready to be downloaded”).
- Evaluate Platform.sendmail(recipients = recipient\_list, message = msg, subject = subject).
- Return recipient\_list.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipient\_list, message = msg, subject = subject).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L5898) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1513)

<a id="op-9804233259a081"></a>
### Backup Generator.add to rollback

`operation_foundation_utils_backups_business_behavior_backup_generator_add_to_rollback`

**Inputs** self, func.

**Declared result** no value.

**Local steps**

- If self.rollback\_callback.
  - Evaluate self.rollback\_callback.add(func).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L6298) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1500)

<a id="op-bdb93b376a435f"></a>
### Backup Generator.delete if step fails

`operation_foundation_utils_backups_business_behavior_backup_generator_delete_if_step_fails`

**Inputs** self, step, remaining positional values paths.

**Explicit failure paths** e.

**Local steps**

- Attempt the following.
  - Evaluate step().
- On failure (Exception) bound to e.
  - For each path in paths.
    - If os.path.exists(path).
      - Evaluate os.remove(path).
  - Raise e.
- For each path in paths.
  - Evaluate self.add\_to\_rollback(deferred anonymous expression).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add to rollback](operations-003.md#op-9804233259a081).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L6382) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1504)

<a id="op-e3d3698ef0e8da"></a>
### Get tables

`operation_foundation_utils_backups_business_behavior_get_tables`

**Inputs** doctypes, existing\_tables.

**Declared result** list at str.

**Explicit results** tables.

**Local steps**

- Set tables from list().
- For each doctype in doctypes.
  - If not doctype.
    - Continue with the next iteration or loop test.
  - Set table from Platform.utils.get\_table\_name(doctype).
  - If table belongs to existing\_tables.
    - Evaluate tables.append(table).
- Return tables.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L70) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1528)

<a id="op-5d28199377911a"></a>
### Fetch latest backups

`operation_foundation_utils_backups_business_behavior_fetch_latest_backups`

**Inputs** partial = false.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“database” → database, “public” → public, “private” → private, “config” → config).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set odb from BackupGenerator(Platform.conf.db\_name, Platform.conf.db\_user, Platform.conf.db\_password, db\_socket = Platform.conf.db\_socket, db\_host = Platform.conf.db\_host, db\_port = Platform.conf.db\_port, db\_type = Pla ….
- Set tuple(database, public, private, config) from odb.get\_recent\_backup(older\_than = (24 × 30), partial = partial).
- Return mapping(“database” → database, “public” → public, “private” → private, “config” → config).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L7184) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1524)

<a id="op-61503683036989"></a>
### Scheduled backup

`operation_foundation_utils_backups_business_behavior_scheduled_backup`

**Inputs** older\_than = 6, ignore\_files = false, backup\_path = no value, backup\_path\_db = no value, backup\_path\_files = no value, backup\_path\_private\_files = no value, backup\_path\_conf = no value, ignore\_conf = false, include\_doctypes = empty text, exclude\_doctypes = empty text, compress = false, force = false, verbose = false, old\_backup\_metadata = false, rollback\_callback = no value.

**Explicit results** new\_backup(older\_than = older\_than, ignore\_files = ignore\_files, backup\_path = backup\_path, backup\_path\_db = backup\_path\_db, …).

**Local steps**

- Return new\_backup(older\_than = older\_than, ignore\_files = ignore\_files, backup\_path = backup\_path, backup\_path\_db = backup\_path\_db, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0463.json#L7526) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1531)

<a id="op-b560395c922a18"></a>
### New backup

`operation_foundation_utils_backups_business_behavior_new_backup`

**Inputs** older\_than = 6, ignore\_files = false, backup\_path = no value, backup\_path\_db = no value, backup\_path\_files = no value, backup\_path\_private\_files = no value, backup\_path\_conf = no value, ignore\_conf = false, include\_doctypes = empty text, exclude\_doctypes = empty text, compress = false, force = false, verbose = false, old\_backup\_metadata = false, rollback\_callback = no value.

**Explicit results** odb.

**Local steps**

- Evaluate delete\_temp\_backups().
- Set odb from BackupGenerator(Platform.conf.db\_name, Platform.conf.db\_user, Platform.conf.db\_password, db\_socket = Platform.conf.db\_socket, db\_host = Platform.conf.db\_host, db\_port = Platform.conf.db\_port, db\_type = Pla ….
- Evaluate odb.get\_backup(older\_than, ignore\_files, force = force).
- Return odb.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1530)

<a id="op-ac3e6af0cf3494"></a>
### Delete temp backups

`operation_foundation_utils_backups_business_behavior_delete_temporary_backups`

**Inputs** older\_than = 23.

**Local steps**

- Set older\_than from (cint(Platform.conf.keep\_backups\_for\_hours) or older\_than).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.keep\_backups\_for\_hours) → older\_than.
- Set backup\_path from get\_backup\_path().
- If os.path.exists(backup\_path).
  - Set file\_list from os.listdir(get\_backup\_path()).
  - For each this\_file in file\_list.
    - Set this\_file\_path from os.path.join(get\_backup\_path(), this\_file).
    - If is\_file\_old(this\_file\_path, older\_than).
      - Evaluate os.remove(this\_file\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L484) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1523)

<a id="op-bdb37d022f39d9"></a>
### Is file old

`operation_foundation_utils_backups_business_behavior_is_file_old`

**Inputs** file\_path, older\_than = 24.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If os.path.isfile(file\_path).
  - Bind dependencies timedelta.
  - Set file\_datetime from datetime.fromtimestamp(os.stat(file\_path).st\_ctime).
  - If (datetime.today() − file\_datetime) ≥ timedelta(hours = older\_than).
    - If \_verbose.
      - Evaluate print(formatted text File {file\_path} is older than {older\_than} hours).
    - Return true.
  - Otherwise.
    - If \_verbose.
      - Evaluate print(formatted text File {file\_path} is recent).
    - Return false.
- Otherwise.
  - If \_verbose.
    - Evaluate print(formatted text File {file\_path} does not exist).
  - Return true.

**Values supplied outside this operation** clock or generated value from datetime.today().

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L71) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1529)
