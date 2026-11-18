# Record lifecycle and persistence · operations 68

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Operator map

<a id="op-5ca444aae6c5fa"></a>
### Like

`operation_foundation_database_operator_map_business_behavior_like`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** key.like(value).

**Local steps**

- Return key.like(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L92) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1018) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1159)

<a id="op-038d13c2bd13d9"></a>
### Ilike

`operation_foundation_database_operator_map_business_behavior_ilike`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** key.ilike(value).

**Local steps**

- Return key.ilike(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L91) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1017) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1158)

<a id="op-7d158ce3301ff0"></a>
### Func in

`operation_foundation_database_operator_map_business_behavior_function_in`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** (key.isin(value) bitwise or key.isnull()) · key.isin(value).

**Local steps**

- If isinstance(value, str).
  - Set value from value.split(“,”).
- Set value from list of empty text when v is identical to no value, otherwise v for v drawn from value.
  - Draw v from value.
  - Value choice on v is identical to no value — true gives empty text, false gives v.
- If empty text belongs to value.
  - Return (key.isin(value) bitwise or key.isnull()).
- Return key.isin(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L87) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1012) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1153)

<a id="op-8e4569e6738732"></a>
### Not like

`operation_foundation_database_operator_map_business_behavior_not_like`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** key.not\_like(value).

**Local steps**

- Return key.not\_like(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L93) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1019) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1160)

<a id="op-176b87167d8422"></a>
### Func not in

`operation_foundation_database_operator_map_business_behavior_function_not_in`

**Inputs** key, value.

**Explicit results** key.notin(value).

**Local steps**

- If isinstance(value, str).
  - Set value from value.split(“,”).
- Return key.notin(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0135.json#L2883) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1014) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1155)

<a id="op-f3514be2ca1ee6"></a>
### Func regex

`operation_foundation_database_operator_map_business_behavior_function_regular_expression`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** key.regex(value).

**Local steps**

- Return key.regex(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L89) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1015) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1156)

<a id="op-55b22032d6d7a7"></a>
### Func between

`operation_foundation_database_operator_map_business_behavior_function_between`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** key at slice(expanded value).

**Local steps**

- Return key at slice(expanded value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L86) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1011) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1152)

<a id="op-ce602d589d9175"></a>
### Func is

`operation_foundation_database_operator_map_business_behavior_function_is`

**Inputs** key, value, empty\_value = empty text.

**Explicit results** key.isnotnull() when empty\_value is identical to no value, otherwise key differs from empty\_value · key.isnull() when empty\_value is identical to no value, otherwise (key.isnull() bitwise or key equals empty\_value).

**Explicit failure paths** ValueError(“′is′ operator only supports ′set′ and ′not set′ as value”).

**Local steps**

- Select the first matching pattern against cstr(value).lower().
  - Pattern “set”.
    - Return key.isnotnull() when empty\_value is identical to no value, otherwise key differs from empty\_value.
      - Value choice on empty\_value is identical to no value — true gives key.isnotnull(), false gives key differs from empty\_value.
  - Pattern “not set”.
    - Return key.isnull() when empty\_value is identical to no value, otherwise (key.isnull() bitwise or key equals empty\_value).
      - Value choice on empty\_value is identical to no value — true gives key.isnull(), false gives (key.isnull() bitwise or key equals empty\_value).
  - Pattern any value.
    - Raise ValueError(“′is′ operator only supports ′set′ and ′not set′ as value”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L88) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1013) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1154)

<a id="op-092ed1253b089a"></a>
### Func timespan

`operation_foundation_database_operator_map_business_behavior_function_timespan`

**Inputs** key, value.

**Declared result** Platform.qb.

**Explicit results** func\_between(key, get\_timespan\_date\_range(value)).

**Local steps**

- Return func\_between(key, get\_timespan\_date\_range(value)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L90) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1016) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1157)

## Record · Package

[Record definition](../../../../data/record-types/package.json)

<a id="op-e10e5436c04187"></a>
### Package.validate

`operation_foundation_core_record_definitions_package_business_behavior_package_validate`

**Inputs** self.

**Explicit failure paths** validation helper — “Package name can only contain letters, digits and hyphens”.

**Local steps**

- If not self.package\_name.
  - Set self.package\_name from self.name.lower().replace(one space, “-”).
- Set allowed\_characters from ((ascii\_letters + digits) + “-”).
- If not all(generator of c belongs to allowed\_characters for c drawn from self.package\_name).
  - Draw c from self.package\_name.
  - Call the validation error handler Platform.throw(“Package name can only contain letters, digits and hyphens”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L2873) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1713)

<a id="op-61a25c6adc8b44"></a>
### Get license text

`operation_foundation_core_record_definitions_package_business_behavior_get_license_text`

**Inputs** license\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Explicit results** textfile.read().

**Local steps**

- If license\_type belongs to LICENSES.
  - Within open(os.path.join(os.path.dirname(\_\_file\_\_), “licenses”, (license\_type + “.md”))) bound as textfile.
    - Return textfile.read().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L3091) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1712)

## Record · Package import

[Record definition](../../../../data/record-types/package_import.json)

<a id="op-0c014879075e67"></a>
### Package Import.validate

`operation_foundation_core_record_definitions_package_import_business_behavior_package_import_validate`

**Inputs** self.

**Local steps**

- If self.activate.
  - Evaluate self.import\_package().

If control reaches the end, it returns no value.

**Methods declared on this owner** [import package](operations-068.md#op-180cfb4f21e4da).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L4750) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1715)

<a id="op-180cfb4f21e4da"></a>
### Package Import.import package

`operation_foundation_core_record_definitions_package_import_business_behavior_package_import_import_package`

**Inputs** self.

**Explicit failure paths** validation helper — Platform.\_(“Please attach the package”) · validation helper — Platform.\_(“Invalid Package Name”) · validation helper — Platform.\_(formatted text Package contains disallowed link entry: {member.name}) · validation helper — Platform.\_(“Package contains disallowed path entry”).

**Local steps**

- Set attachment from get\_attachments(self.doctype, self.name).
- If not attachment.
  - Call the validation error handler Platform.throw(Platform.\_(“Please attach the package”)).
- Set attachment from attachment at 0.
- Set raw\_name from nested operand in the contract.file\_name.split(“.”, 1) at 0.rsplit(“-”, 1) at 0.
- Set package\_name from re.sub(“&#91;^a-zA-Z0-9\_-&#93;”, empty text, raw\_name).
- If not package\_name.
  - Call the validation error handler Platform.throw(Platform.\_(“Invalid Package Name”)).
- If not os.path.exists(Platform.get\_site\_path(“packages”)).
  - Evaluate os.makedirs(Platform.get\_site\_path(“packages”)).
- Set extract\_path from Platform.get\_site\_path(“packages”).
- Set archive\_path from get\_files\_path(attachment.file\_name, is\_private = attachment.is\_private).
- Within tarfile.open(archive\_path, “r:gz”) bound as tar.
  - For each member in tar.getmembers().
    - If (member.issym() or member.islnk()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in member.issym() → member.islnk().
      - Call the validation error handler Platform.throw(Platform.\_(formatted text Package contains disallowed link entry: {member.name})).
    - Set member\_path from os.path.join(extract\_path, member.name).
    - Set is\_safe from check\_path\_safety(extract\_path, member\_path).
    - If not is\_safe.
      - Call the validation error handler Platform.throw(Platform.\_(“Package contains disallowed path entry”)).
  - Evaluate tar.extractall(path = extract\_path, filter = “data”).
- Set package\_path from Platform.get\_site\_path(“packages”, package\_name).
- Within open(os.path.join(package\_path, (package\_name + “.json”))) bound as packagefile.
  - Set doc\_dict from json.loads(packagefile.read()).
- Set Platform.flags.package from import\_doc(doc\_dict).
- Set files from list().
- Set log from list().
- For each module in os.listdir(package\_path).
  - Set module\_path from os.path.join(package\_path, module).
  - If os.path.isdir(module\_path).
    - Set files from get\_doc\_files(files, module\_path).
- For each file in files.
  - Evaluate import\_file\_by\_path(file, force = self.force, ignore\_version = true).
  - Evaluate log.append(formatted text Imported {file}).
- Set self.log from whitespace '\\n'.join(log).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L4815) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1714)

## Record · Package release

[Record definition](../../../../data/record-types/package_release.json)

<a id="op-0ae9ca80e2a5dd"></a>
### Package Release.set version

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_set_version`

**Inputs** self.

**Local steps**

- Set doctype from Platform.qb.DocType(“Package Release”).
- If not self.major.
  - Set self.major from (nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).run() at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).select(Max(nested operand in the contract.minor)).run() at 0 at 0 → 0.
- If not self.minor.
  - Set self.minor from (nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).run() at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).select(Max(“minor”)).run() at 0 at 0 → 0.
- If not self.patch.
  - Set value from (nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).run() at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).select(Max(“patch”)).run() at 0 at 0 → 0.
  - Set self.patch from (value + 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L6084) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1721)

<a id="op-523b4b8f437b88"></a>
### Package Release.autoname

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_autoname`

**Inputs** self.

**Record and data access** read “Package” via get\_value.

**Local steps**

- Evaluate self.set\_version().
- Set self.name from “{}-{}.{}.{}”.format(Platform.db.get\_value(“Package”, self.package, “package\_name”), self.major, self.minor, self.patch).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set version](operations-068.md#op-0ae9ca80e2a5dd).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L6640) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1716)

<a id="op-5d2033f7687f2c"></a>
### Package Release.validate

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_validate`

**Inputs** self.

**Record and data access** resolve a document from “Package” via get\_doc.

**Explicit failure paths** validation helper — (“Invalid package path: ” + package\_path.as\_posix()).

**Local steps**

- Set package from Platform.get\_doc(“Package”, self.package).
- Set package\_path from Path(Platform.get\_site\_path(“packages”, package.package\_name)).
- If not package\_path.resolve().is\_relative\_to(Path(nested operand in the contract.get\_site\_path()).resolve()).
  - Call the validation error handler Platform.throw((“Invalid package path: ” + package\_path.as\_posix())).
- If self.publish.
  - Evaluate self.export\_files(package).

If control reaches the end, it returns no value.

**Methods declared on this owner** [export files](operations-068.md#op-10b1a2cae85a6b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L6793) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1722)

<a id="op-10b1a2cae85a6b"></a>
### Package Release.export files

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_export_files`

**Inputs** self, package.

**Local steps**

- Evaluate self.export\_modules().
- Evaluate self.export\_package\_files(package).
- Evaluate self.make\_tarfile(package).

If control reaches the end, it returns no value.

**Methods declared on this owner** [export modules](operations-068.md#op-673b1d11b8597f), [export package files](operations-068.md#op-2447e48b0ef265), [make tarfile](operations-068.md#op-0d6357a15cd37a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L7072) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1717)

<a id="op-673b1d11b8597f"></a>
### Package Release.export modules

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_export_modules`

**Inputs** self.

**Record and data access** read “Module Def” via get\_all · resolve a document from “Module Def” via get\_doc · read l.link\_doctype via get\_all · resolve a document from l.link\_doctype via get\_doc.

**Local steps**

- For each m in Platform.get\_all(“Module Def”, dict(package = self.package)).
  - Set module from Platform.get\_doc(“Module Def”, m.name).
  - For each l in module.meta.links.
    - If l.link\_doctype equals “Module Def”.
      - Continue with the next iteration or loop test.
    - For each d in Platform.get\_all(l.link\_doctype, dict(module = m.name)).
      - Evaluate export\_doc(Platform.get\_doc(l.link\_doctype, d.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1718)

<a id="op-2447e48b0ef265"></a>
### Package Release.export package files

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_export_package_files`

**Inputs** self, package.

**Local steps**

- If package.readme.
  - Within open(Platform.get\_site\_path(“packages”, package.package\_name, “README.md”), “w”) bound as readme.
    - Evaluate readme.write(package.readme).
- If package.license.
  - Within open(Platform.get\_site\_path(“packages”, package.package\_name, “LICENSE.md”), “w”) bound as license.
    - Evaluate license.write(package.license).
- Within open(Platform.get\_site\_path(“packages”, package.package\_name, (package.package\_name + “.json”)), “w”) bound as packagefile.
  - Evaluate packagefile.write(Platform.as\_json(package.as\_dict(no\_nulls = true))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L314) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1719)

<a id="op-0d6357a15cd37a"></a>
### Package Release.make tarfile

`operation_foundation_core_record_definitions_package_release_business_behavior_package_release_make_tarfile`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, package.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L691) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1720)

## Record · Page

[Record definition](../../../../data/record-types/page.json)

<a id="op-ca6b3c731cde04"></a>
### Page.autoname

`operation_foundation_core_record_definitions_page_business_behavior_page_autoname`

**Inputs** self.

**Record and data access** read “Page” via exists · execute query text (SELECT, Page).format(self.name).

**Local steps**

- Bind dependencies cint.
- If ((self.name and self.name.startswith(“New Page”)) or not self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.name and self.name.startswith(“New Page”)) → not self.name.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.name → self.name.startswith(“New Page”).
  - Set self.name from nested operand in the contract.replace(“"”, empty text).replace(“'”, empty text).replace(one space, “-”) at slice no value to 20.
  - If Platform.db.exists(“Page”, self.name).
    - Set cnt from Platform.db.sql(query text (SELECT, Page).format(self.name)).
    - If cnt.
      - Set cnt from (cint(nested operand in the contract at nested operand in the contract at 0.split(“-”) at negative 1) + 1).
    - Otherwise.
      - Set cnt from 1.
    - Update self.name using + (“-” + str(cnt)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L1080) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1732)

<a id="op-6b6fc2543ef7c3"></a>
### Page.validate

`operation_foundation_core_record_definitions_page_business_behavior_page_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Not in Developer Mode” · validation helper — translated “Only Administrator can edit”.

**Local steps**

- Evaluate validate\_route\_conflict(self.doctype, self.name).
- If (self.is\_new() and not getattr(conf, “developer\_mode”, 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not getattr(conf, “developer\_mode”, 0).
  - Call the validation error handler Platform.throw(translated “Not in Developer Mode”).
- If (Platform.session.user differs from “Administrator” and not self.flags.ignore\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user differs from “Administrator” → not self.flags.ignore\_permissions.
  - Call the validation error handler Platform.throw(translated “Only Administrator can edit”).
- Evaluate self.validate\_shell().
- Evaluate self.validate\_island().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate shell](operations-068.md#op-e6e1bd4c1f3ad9), [validate island](operations-068.md#op-cd305f31db3bf9).

**Values supplied outside this operation** selected callable from getattr(conf, “developer\_mode”, 0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L87) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1742)

<a id="op-e6e1bd4c1f3ad9"></a>
### Page.validate shell

`operation_foundation_binding_foundation_core_doctype_page_page_page_validate_shell`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L635)

<a id="op-cd305f31db3bf9"></a>
### Page.validate island

`operation_foundation_core_record_definitions_page_business_behavior_page_validate_island`

**Inputs** self.

**State and service calls** msgprint with translated “{0}.js will no longer run. A Platform UI page is drawn by its island.”.format(formatted text {page\_name}.js).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Island "{0}" is not on this site. Build the app that ships it.”.format(self.island) · validation helper — translated “A Platform UI page has to be Standard. Its Vue source lives in the app's page folder.”.

**Local steps**

- If self.type differs from “Platform UI”.
  - Return no value.
- If self.island.
  - Bind dependencies get\_ui\_islands.
  - If self.island does not belong to get\_ui\_islands().
    - Call the validation error handler Platform.throw(translated “Island "{0}" is not on this site. Build the app that ships it.”.format(self.island)).
  - Return no value.
- If self.standard differs from “Yes”.
  - Call the validation error handler Platform.throw(translated “A Platform UI page has to be Standard. Its Vue source lives in the app's page folder.”).
- Set page\_name from Platform.scrub(self.name).
- If (not self.is\_new() and os.path.exists(os.path.join(self.get\_folder\_path(), formatted text {page\_name}.js))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → os.path.exists(os.path.join(self.get\_folder\_path(), formatted text {page\_name}.js)).
  - Evaluate Platform.msgprint(translated “{0}.js will no longer run. A Platform UI page is drawn by its island.”.format(formatted text {page\_name}.js), indicator = “orange”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-069.md#op-c3be235312309a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L88) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1743)
