# Supporting services · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Party import provider

<a id="op-334fc08fd96c88"></a>
### Party Import Provider.get import fields

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_get_import_fields`

**Inputs** self.

**Declared result** dict.

**Explicit results** schema.

**Local steps**

- Set linked\_tables from list of mapping(“fieldname” → fieldname, “label” → label, “fields” → get\_fields()) for tuple(fieldname, doctype, label, get\_fields) drawn from tuple(tuple(“contacts”, “Contact”, translated “Contact”, \_cont ….
  - Draw tuple(fieldname, doctype, label, get\_fields) from tuple(tuple(“contacts”, “Contact”, translated “Contact”, \_contact\_docfields), tuple(“addresses”, “Address”, translated “Address”, deferred anonymous expression)), keep a combination only if (Platform.has\_permission(doctype, “read”)).
- Set schema from mapping(“fields” → list of df for df drawn from \_doctype\_docfields(self.doctype) where df at “fieldname” does not belong to CONTACT\_FIELDS, “child\_tables” → list(expanded \_doctype\_child\_tables(self.doctype ….
  - Draw df from \_doctype\_docfields(self.doctype), keep a combination only if (df at “fieldname” does not belong to CONTACT\_FIELDS).
- Evaluate \_add\_plain\_headers(schema, tuple(“contacts”, “addresses”)).
- Return schema.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1332)

<a id="op-ac6356f7d1a0be"></a>
### Party Import Provider.import row

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_import_row`

**Inputs** self, importer, doc.

**Explicit results** tuple(party, import\_action).

**Local steps**

- Set contact\_rows from (doc.pop(“contacts”, no value) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.pop(“contacts”, no value) → list().
- Set address\_rows from (doc.pop(“addresses”, no value) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.pop(“addresses”, no value) → list().
- Set has\_child\_rows from bool((contact\_rows or address\_rows)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact\_rows → address\_rows.
- Set tuple(party, import\_action) from self.\_persist\_party(importer, doc, has\_child\_rows).
- Set find\_existing from importer.import\_type differs from INSERT.
- Evaluate self.\_create\_contacts(party, contact\_rows, find\_existing).
- Evaluate self.\_create\_addresses(party, address\_rows, find\_existing).
- Return tuple(party, import\_action).

**Methods declared on this owner** [persist party](operations-005.md#op-e2a7bc6183cebd), [create contacts](operations-005.md#op-c3441ad03079ff), [create addresses](operations-005.md#op-8967155167a6b5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1333)

<a id="op-573b74379406d6"></a>
### Party Import Provider.get export rows

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_get_export_rows`

**Inputs** self, names, tables.

**Record and data access** read self.doctype via get\_all.

**Explicit results** mapping() · rows.

**Local steps**

- Set linked\_tables from list of tuple(table, doctype, flag) for tuple(table, doctype, flag) drawn from tuple(tuple(“contacts”, “Contact”, “is\_primary\_contact”), tuple(“addresses”, “Address”, “is\_primary\_address”)) where tables.get(table).
  - Draw tuple(table, doctype, flag) from tuple(tuple(“contacts”, “Contact”, “is\_primary\_contact”), tuple(“addresses”, “Address”, “is\_primary\_address”)), keep a combination only if (tables.get(table)).
- If not linked\_tables.
  - Return mapping().
- Set parties from Platform.get\_all(self.doctype, filters = mapping(“name” → list(“in”, names)), fields = list(“name”, self.\_field(“primary\_contact”), self.\_field(“primary\_address”))).
- Set rows from mapping().
- For each tuple(table, doctype, flag) in linked\_tables.
  - Set primary\_field from self.\_field(formatted text primary\_{doctype.lower()}).
  - Set primaries from set of tuple(party.name, party.get(primary\_field)) for party drawn from parties.
    - Draw party from parties.
  - Set linked from \_linked\_records(doctype, self.doctype, names, tables at table).
  - For each tuple(party, record\_name, record) in sorted(linked, key = deferred anonymous expression).
    - If flag belongs to record.
      - Set record at flag from int(tuple(party, record\_name) belongs to primaries).
    - Evaluate rows.setdefault(party, mapping()).setdefault(table, list()).append(record).
- Return rows.

**Methods declared on this owner** [field](operations-005.md#op-5ccfdc27046f26).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1331)

<a id="op-5ccfdc27046f26"></a>
### Party Import Provider.field

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_field`

**Inputs** self, name.

**Explicit results** formatted text {Platform.scrub(self.doctype)}\_{name}.

**Local steps**

- Return formatted text {Platform.scrub(self.doctype)}\_{name}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1330)

<a id="op-e2a7bc6183cebd"></a>
### Party Import Provider.persist party

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_persist_party`

**Inputs** self, importer, doc, has\_child\_rows.

**Explicit results** tuple(importer.insert\_record(doc), no value) · tuple(importer.update\_record(doc, raise\_if\_no\_changes = not has\_child\_rows), no value) · importer.upsert\_record(doc).

**Local steps**

- If importer.import\_type equals INSERT.
  - Return tuple(importer.insert\_record(doc), no value).
- If importer.import\_type equals UPDATE.
  - Return tuple(importer.update\_record(doc, raise\_if\_no\_changes = not has\_child\_rows), no value).
- Return importer.upsert\_record(doc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1334)

<a id="op-c3441ad03079ff"></a>
### Party Import Provider.create contacts

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_create_contacts`

**Inputs** self, party, rows, find\_existing.

**Record and data access** resolve a document from “Contact” via get\_doc · resolve a document from mapping(“doctype” → “Contact”, expand contact\_values, “links” → list(mapping(“link\_doctype” → party.doctype, “link\_name” → party.name))) via get\_doc.

**State and service calls** call insert on contact · request set\_value on “Contact” · call db\_set on party.

**Local steps**

- Set primary from no value.
- For each row in rows.
  - Set row from dict(row).
  - Set email from row.pop(“email\_id”, no value).
  - Set mobile from row.pop(“mobile\_no”, no value).
  - Set flag from row.pop(“is\_primary\_contact”, no value).
  - Set flagged from Platform.utils.cint(flag).
  - Set match from mapping(“email\_id” → email) when email, otherwise mapping(“mobile\_no” → mobile) when mobile, otherwise no value.
    - Value choice on email — true gives mapping(“email\_id” → email), false gives mapping(“mobile\_no” → mobile) when mobile, otherwise no value.
    - Value choice on mobile — true gives mapping(“mobile\_no” → mobile), false gives no value.
  - Set existing from (find\_existing and match and \_find\_linked(“Contact”, party.doctype, party.name, match)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in find\_existing → match → \_find\_linked(“Contact”, party.doctype, party.name, match).
  - If existing.
    - Set contact from Platform.get\_doc(“Contact”, existing).
  - Otherwise.
    - Set names from self.\_resolve\_contact\_names(party, row).
    - Set contact\_values from mapping of k → v for tuple(k, v) drawn from mapping(expand row, expand names).items() where v does not belong to tuple(no value, empty text).
      - Draw tuple(k, v) from mapping(expand row, expand names).items(), keep a combination only if (v does not belong to tuple(no value, empty text)).
    - Set contact from Platform.get\_doc(mapping(“doctype” → “Contact”, expand contact\_values, “links” → list(mapping(“link\_doctype” → party.doctype, “link\_name” → party.name)))).
    - If email.
      - Evaluate contact.add\_email(email, is\_primary = true).
    - If mobile.
      - Evaluate contact.add\_phone(mobile, is\_primary\_mobile\_no = true).
    - Evaluate contact.insert().
  - If (flagged or (primary is identical to no value and not (find\_existing and flag is distinct from no value))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flagged → (primary is identical to no value and not (find\_existing and flag is distinct from no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in primary is identical to no value → not (find\_existing and flag is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in find\_existing → flag is distinct from no value.
    - Set primary from contact.
- If primary.
  - Evaluate \_demote\_other\_primary\_contacts(party.doctype, party.name, primary.name).
  - Evaluate Platform.db.set\_value(“Contact”, primary.name, “is\_primary\_contact”, 1).
  - Evaluate party.db\_set(self.\_field(“primary\_contact”), primary.name).
  - Evaluate party.db\_set(“mobile\_no”, primary.mobile\_no).
  - Evaluate party.db\_set(“email\_id”, primary.email\_id).

If control reaches the end, it returns no value.

**Methods declared on this owner** [resolve contact names](operations-005.md#op-dafc78db84e720), [field](operations-005.md#op-5ccfdc27046f26).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1329)

<a id="op-dafc78db84e720"></a>
### Party Import Provider.resolve contact names

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_resolve_contact_names`

**Inputs** self, party, row.

**Explicit results** names.

**Local steps**

- Set names from mapping of field → row.pop(field, no value) for field drawn from tuple(“first\_name”, “middle\_name”, “last\_name”, “company\_name”).
  - Draw field from tuple(“first\_name”, “middle\_name”, “last\_name”, “company\_name”).
- Set party\_name from party.get(self.\_field(“name”)).
- If party.get(self.\_field(“type”)) differs from “Individual”.
  - Set names at “company\_name” from (names at “company\_name” or party\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in names at “company\_name” → party\_name.
  - Return names.
- Set names at “first\_name” from (names at “first\_name” or party.get(“first\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in names at “first\_name” → party.get(“first\_name”).
- Set names at “last\_name” from (names at “last\_name” or party.get(“last\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in names at “last\_name” → party.get(“last\_name”).
- If not names at “first\_name”.
  - Set tuple(first, middle, last) from parse\_full\_name(party\_name).
  - Set names at “first\_name” from first.
  - Set names at “middle\_name” from (names at “middle\_name” or middle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in names at “middle\_name” → middle.
  - Set names at “last\_name” from (names at “last\_name” or last).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in names at “last\_name” → last.
- Return names.

**Methods declared on this owner** [field](operations-005.md#op-5ccfdc27046f26).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1335)

<a id="op-8967155167a6b5"></a>
### Party Import Provider.create addresses

`operation_enterprise_binding_enterprise_utilities_party_import_provider_partyimportprovider_create_addresses`

**Inputs** self, party, rows, find\_existing.

**Record and data access** resolve a document from “Address” via get\_doc · resolve a document from mapping(“doctype” → “Address”, expand mapping of k → v for tuple(k, v) drawn from row.items() where v does not belong to tuple(no value, empty text), “links” → list(mapping(“link\_doctype” → party.doctype,  … via get\_doc.

**State and service calls** call insert on address · call save on primary · call db\_set on party.

**Local steps**

- Bind dependencies get\_address\_display.
- Set primary from no value.
- For each row in rows.
  - Set row from dict(row).
  - Set flag from row.pop(“is\_primary\_address”, no value).
  - Set flagged from Platform.utils.cint(flag).
  - Set existing from (find\_existing and \_find\_linked(“Address”, party.doctype, party.name, mapping(“address\_line1” → row.get(“address\_line1”), “city” → row.get(“city”)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in find\_existing → \_find\_linked(“Address”, party.doctype, party.name, mapping(“address\_line1” → row.get(“address\_line1”), “city” → row.get(“city”))).
  - If existing.
    - Set address from Platform.get\_doc(“Address”, existing).
  - Otherwise.
    - Set row at “address\_type” from (row.get(“address\_type”) or “Billing”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“address\_type”) → “Billing”.
    - Set row at “address\_title” from (row.get(“address\_title”) or party.get(self.\_field(“name”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“address\_title”) → party.get(self.\_field(“name”)).
    - Set address from Platform.get\_doc(mapping(“doctype” → “Address”, expand mapping of k → v for tuple(k, v) drawn from row.items() where v does not belong to tuple(no value, empty text), “links” → list(mapping(“link\_doctype”  ….
      - Draw tuple(k, v) from row.items(), keep a combination only if (v does not belong to tuple(no value, empty text)).
    - Evaluate address.insert().
  - If (flagged or (primary is identical to no value and not (find\_existing and flag is distinct from no value))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flagged → (primary is identical to no value and not (find\_existing and flag is distinct from no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in primary is identical to no value → not (find\_existing and flag is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in find\_existing → flag is distinct from no value.
    - Set primary from address.
- If primary.
  - Set primary.is\_primary\_address from 1.
  - Evaluate primary.save().
  - Evaluate party.db\_set(self.\_field(“primary\_address”), primary.name).
  - Evaluate party.db\_set(“primary\_address”, get\_address\_display(primary.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [field](operations-005.md#op-5ccfdc27046f26).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1328)

<a id="op-a27e9be3214331"></a>
### Find linked

`operation_enterprise_binding_enterprise_utilities_party_import_provider_find_linked`

**Inputs** doctype, link\_doctype, link\_name, filters.

**Declared result** (str bitwise or no value).

**Record and data access** read doctype via get\_value.

**Explicit results** Platform.db.get\_value(doctype, list(list(“Dynamic Link”, “link\_doctype”, “=”, link\_doctype), list(“Dynamic Link”, “link\_name”, “=”, link\_name), expanded list of list(field, “=”, value) for tuple(field, val ….

**Local steps**

- Return Platform.db.get\_value(doctype, list(list(“Dynamic Link”, “link\_doctype”, “=”, link\_doctype), list(“Dynamic Link”, “link\_name”, “=”, link\_name), expanded list of list(field, “=”, value) for tuple(field, val ….
  - Draw tuple(field, value) from filters.items().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1326)

<a id="op-cab6bb7af64255"></a>
### Linked records

`operation_enterprise_binding_enterprise_utilities_party_import_provider_linked_records`

**Inputs** doctype, link\_doctype, link\_names, fields.

**Record and data access** read “Dynamic Link” via get\_all · read doctype via get\_list.

**Explicit results** list() · list of tuple(party, record.name, mapping of field → record.get(field) for field drawn from fields) for record drawn from records, then party drawn from parties\_by\_record at record.name.

**Local steps**

- Set links from Platform.get\_all(“Dynamic Link”, filters = mapping(“link\_doctype” → link\_doctype, “link\_name” → list(“in”, link\_names), “parenttype” → doctype), fields = list(“parent”, “link\_name”)).
- If not links.
  - Return list().
- Set records from Platform.get\_list(doctype, filters = mapping(“name” → list(“in”, list(set of link.parent for link drawn from links))), fields = list(“name”, expanded fields), order\_by = “creation asc”).
  - Draw link from links.
- Set parties\_by\_record from mapping().
- For each link in links.
  - Set parties\_by\_record.setdefault(link.parent, mapping()) at link.link\_name from no value.
- Return list of tuple(party, record.name, mapping of field → record.get(field) for field drawn from fields) for record drawn from records, then party drawn from parties\_by\_record at record.name.
  - Draw record from records.
  - Draw party from parties\_by\_record at record.name.
  - Draw field from fields.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1327)

<a id="op-35e2d322ad72e3"></a>
### Demote other primary contacts

`operation_enterprise_binding_enterprise_utilities_party_import_provider_demote_other_primary_contacts`

**Inputs** link\_doctype, link\_name, keep.

**Declared result** no value.

**Record and data access** read “Dynamic Link” via get\_all · read “Contact” via get\_all.

**State and service calls** request set\_value on “Contact”.

**Local steps**

- Set linked from Platform.get\_all(“Dynamic Link”, filters = mapping(“link\_doctype” → link\_doctype, “link\_name” → link\_name, “parenttype” → “Contact”), pluck = “parent”).
- For each other in Platform.get\_all(“Contact”, filters = mapping(“name” → list(“in”, (linked or list(empty text))), “is\_primary\_contact” → 1), pluck = “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in linked → list(empty text).
  - If other differs from keep.
    - Evaluate Platform.db.set\_value(“Contact”, other, “is\_primary\_contact”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L42) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1323)

<a id="op-822aee396f25a1"></a>
### Doctype docfields

`operation_enterprise_binding_enterprise_utilities_party_import_provider_doctype_docfields`

**Inputs** doctype.

**Declared result** list at dict.

**Explicit results** fields.

**Local steps**

- Bind dependencies display\_fieldtypes, no\_value\_fields.
- Set fields from list().
- For each df in Platform.get\_meta(doctype).fields.
  - If (df.fieldtype belongs to no\_value\_fields or df.fieldtype belongs to display\_fieldtypes).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype belongs to no\_value\_fields → df.fieldtype belongs to display\_fieldtypes.
    - Continue with the next iteration or loop test.
  - If (df.fieldname belongs to tuple(“lft”, “rgt”) or df.get(“is\_virtual”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldname belongs to tuple(“lft”, “rgt”) → df.get(“is\_virtual”).
    - Continue with the next iteration or loop test.
  - Evaluate fields.append(df.as\_dict()).
- Return fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L44) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1325)

<a id="op-16302fc53ee64f"></a>
### Contact docfields

`operation_enterprise_binding_enterprise_utilities_party_import_provider_contact_docfields`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** fields.

**Local steps**

- Set fields from \_doctype\_docfields(“Contact”).
- For each df in fields.
  - If df at “fieldname” belongs to tuple(“email\_id”, “mobile\_no”).
    - Set df at “in\_import\_template” from 1.
- Return fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L41) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1322)

<a id="op-f625e1371572f2"></a>
### Add plain headers

`operation_enterprise_binding_enterprise_utilities_party_import_provider_add_plain_headers`

**Inputs** schema, tables.

**Declared result** no value.

**Local steps**

- Set parent\_headers from set of header for df drawn from schema at “fields”, then header drawn from \_plain\_headers(df).
  - Draw df from schema at “fields”.
  - Draw header from \_plain\_headers(df).
- Set counts from Counter(generator of header for table drawn from schema at “child\_tables”, then df drawn from table at “fields”, then header drawn from \_plain\_headers(df)).
  - Draw table from schema at “child\_tables”.
  - Draw df from table at “fields”.
  - Draw header from \_plain\_headers(df).
- For each table in schema at “child\_tables”.
  - If table at “fieldname” belongs to tables.
    - For each df in table at “fields”.
      - Set df at “import\_labels” from list of header for header drawn from \_plain\_headers(df) where (counts at header equals 1 and header does not belong to parent\_headers).
        - Draw header from \_plain\_headers(df), keep a combination only if ((counts at header equals 1 and header does not belong to parent\_headers)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in counts at header equals 1 → header does not belong to parent\_headers.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L40) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1321)

<a id="op-b72cbe43f88b4e"></a>
### Plain headers

`operation_enterprise_binding_enterprise_utilities_party_import_provider_plain_headers`

**Inputs** df.

**Declared result** set at str.

**Explicit results** set of header for header drawn from tuple(df.get(“label”), translated (df.get(“label”) or empty text), df at “fieldname”) where header.

**Local steps**

- Return set of header for header drawn from tuple(df.get(“label”), translated (df.get(“label”) or empty text), df at “fieldname”) where header.
  - Draw header from tuple(df.get(“label”), translated (df.get(“label”) or empty text), df at “fieldname”), keep a combination only if (header).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“label”) → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1336)

<a id="op-47ab743ebdd770"></a>
### Doctype child tables

`operation_enterprise_binding_enterprise_utilities_party_import_provider_doctype_child_tables`

**Inputs** doctype.

**Declared result** list at dict.

**Explicit results** list of mapping(“fieldname” → tf.fieldname, “label” → translated (tf.label or tf.fieldname), “fields” → \_doctype\_docfields(tf.options)) for tf drawn from Platform.get\_meta(doctype).get\_table\_fields().

**Local steps**

- Return list of mapping(“fieldname” → tf.fieldname, “label” → translated (tf.label or tf.fieldname), “fields” → \_doctype\_docfields(tf.options)) for tf drawn from Platform.get\_meta(doctype).get\_table\_fields().
  - Draw tf from Platform.get\_meta(doctype).get\_table\_fields().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tf.label → tf.fieldname.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L43) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1324)

## Service · Payment setup certification

<a id="op-136eac52867ccc"></a>
### Get context

`operation_enterprise_public_pages_payment_setup_certification_business_behavior_get_context`

**Inputs** context.

**Local steps**

- If Platform.session.user differs from “Guest”.
  - Set context.all\_certifications from get\_all\_certifications\_of\_a\_member().
  - Set context.show\_sidebar from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L7666) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L904)

<a id="op-f59b3f427aa169"></a>
### Get all certifications of a member

`operation_enterprise_public_pages_payment_setup_certification_business_behavior_get_all_certifications_of_a_member`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Certified Consultant, Certification Application).

**Explicit results** all\_certifications.

**Local steps**

- Set all\_certifications from list().
- Set all\_certifications from Platform.db.sql(query text (SELECT, Certified Consultant, Certification Application), mapping(“user” → Platform.session.user), as\_dict = true).
- Return all\_certifications.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L903)

## Service · Product

<a id="op-527d5bca94daab"></a>
### Get price

`operation_enterprise_utilities_product_business_behavior_get_price`

**Inputs** item\_code, price\_list, customer\_group, company, qty = 1, party = no value.

**Record and data access** read “Item” via get\_value · read “Item Price” via get\_all · read “Price List” via get\_value · read “Currency” via get\_value · execute query text (SELECT, UOM Conversion Detail, Item).

**Explicit results** price\_obj.

**Local steps**

- Set template\_item\_code from Platform.db.get\_value(“Item”, item\_code, “variant\_of”).
- If price\_list.
  - Set price from Platform.get\_all(“Item Price”, fields = list(“price\_list\_rate”, “currency”), filters = mapping(“price\_list” → price\_list, “item\_code” → item\_code)).
  - If (template\_item\_code and not price).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in template\_item\_code → not price.
    - Set price from Platform.get\_all(“Item Price”, fields = list(“price\_list\_rate”, “currency”), filters = mapping(“price\_list” → price\_list, “item\_code” → template\_item\_code)).
  - If price.
    - Set pricing\_rule\_dict from Platform.\_dict(mapping(“item\_code” → item\_code, “qty” → qty, “stock\_qty” → qty, “transaction\_type” → “selling”, …)).
    - If (party and party.doctype equals “Customer”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in party → party.doctype equals “Customer”.
      - Evaluate pricing\_rule\_dict.update(mapping(“customer” → party.name)).
    - Set pricing\_rule from get\_pricing\_rule\_for\_item(pricing\_rule\_dict).
    - Set price\_obj from price at 0.
    - If pricing\_rule.
      - Set mrp from (price\_obj.price\_list\_rate or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in price\_obj.price\_list\_rate → 0.
      - Set price\_obj.price\_list\_rate from pricing\_rule.get(“price\_list\_rate”, mrp).
      - If pricing\_rule.margin\_type equals “Percentage”.
        - Update price\_obj.price\_list\_rate using × (1 + (flt(pricing\_rule.margin\_rate\_or\_amount) ÷ 100)).
      - Otherwise.
        - If pricing\_rule.margin\_type equals “Amount”.
          - Update price\_obj.price\_list\_rate using + flt(pricing\_rule.margin\_rate\_or\_amount).
      - If pricing\_rule.pricing\_rule\_for equals “Discount Percentage”.
        - Set price\_obj.discount\_percent from pricing\_rule.discount\_percentage.
        - Set price\_obj.formatted\_discount\_percent from (str(flt(pricing\_rule.discount\_percentage, 0)) + “%”).
        - Set price\_obj.price\_list\_rate from flt((price\_obj.price\_list\_rate × (1.0 − (flt(pricing\_rule.discount\_percentage) ÷ 100.0)))).
      - Otherwise.
        - If pricing\_rule.pricing\_rule\_for equals “Discount Amount”.
          - Update price\_obj.price\_list\_rate using − flt(pricing\_rule.discount\_amount).
      - If pricing\_rule.pricing\_rule\_for belongs to tuple(“Rate”, “Discount Amount”).
        - Set rate\_discount from (flt(mrp) − flt(price\_obj.price\_list\_rate)).
        - If rate\_discount &gt; 0.
          - Set price\_obj.formatted\_discount\_rate from fmt\_money(rate\_discount, currency = price\_obj at “currency”).
    - If price\_obj.
      - Set price\_obj at “formatted\_price” from fmt\_money(price\_obj at “price\_list\_rate”, currency = price\_obj at “currency”).
      - If mrp differs from price\_obj at “price\_list\_rate”.
        - Set price\_obj at “formatted\_mrp” from fmt\_money(mrp, currency = price\_obj at “currency”).
      - Set price\_obj at “currency\_symbol” from ((not cint(nested operand in the contract.db.get\_default(“hide\_currency\_symbol”)) and (Platform.db.get\_value(“Currency”, price\_obj.currency, “symbol”, cache = true) or price\_obj.currency)) or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not cint(Platform.db.get\_default(“hide\_currency\_symbol”)) and (Platform.db.get\_value(“Currency”, price\_obj.currency, “symbol”, cache = true) or price\_obj.currency)) → empty text.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(Platform.db.get\_default(“hide\_currency\_symbol”)) → (Platform.db.get\_value(“Currency”, price\_obj.currency, “symbol”, cache = true) or price\_obj.currency).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Currency”, price\_obj.currency, “symbol”, cache = true) → price\_obj.currency.
      - Set uom\_conversion\_factor from Platform.db.sql(query text (SELECT, UOM Conversion Detail, Item), item\_code).
      - Set uom\_conversion\_factor from uom\_conversion\_factor at 0 at 0 when uom\_conversion\_factor, otherwise 1.
        - Value choice on uom\_conversion\_factor — true gives uom\_conversion\_factor at 0 at 0, false gives 1.
      - Set price\_obj at “formatted\_price\_sales\_uom” from fmt\_money((price\_obj at “price\_list\_rate” × uom\_conversion\_factor), currency = price\_obj at “currency”).
      - If not price\_obj at “price\_list\_rate”.
        - Set price\_obj at “price\_list\_rate” from 0.
      - If not price\_obj at “currency”.
        - Set price\_obj at “currency” from empty text.
      - If not price\_obj at “formatted\_price”.
        - Set tuple(price\_obj at “formatted\_price”, price\_obj at “formatted\_mrp”) from tuple(empty text, empty text).
    - Return price\_obj.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L75)

<a id="op-868ac304342658"></a>
### Get item codes by attributes

`operation_enterprise_utilities_product_business_behavior_get_item_codes_by_attributes`

**Inputs** attribute\_filters, template\_item\_code = no value.

**State and service calls** execute a supplied database query.

**Explicit results** res.

**Local steps**

- Set items from list().
- For each tuple(attribute, values) in attribute\_filters.items().
  - Set attribute\_values from values.
  - If not isinstance(attribute\_values, list).
    - Set attribute\_values from list(attribute\_values).
  - If not attribute\_values.
    - Continue with the next iteration or loop test.
  - Set wheres from list().
  - Set query\_values from list().
  - For each attribute\_value in attribute\_values.
    - Evaluate wheres.append(“( attribute = %s and attribute\_value = %s )”).
    - Update query\_values using + list(attribute, attribute\_value).
  - Set attribute\_query from “ or ”.join(wheres).
  - If template\_item\_code.
    - Set variant\_of\_query from “AND t2.variant\_of = %s”.
    - Evaluate query\_values.append(template\_item\_code).
  - Otherwise.
    - Set variant\_of\_query from empty text.
  - Set query from formatted text   SELECT  t1.parent  FROM  ′tabItem Variant Attribute′ t1  WHERE  1 = 1  AND (  {attribute\_query}  )  AND EXISTS (  SE.
  - Set item\_codes from set(list of r at 0 for r drawn from Platform.db.sql(query, query\_values)).
    - Draw r from Platform.db.sql(query, query\_values).
  - Evaluate items.append(item\_codes).
- Set res from list(set.intersection(expanded items)).
- Return res.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L74)

## Service · Projects

<a id="op-6c6fe3ae31fa27"></a>
### Get data

`operation_enterprise_configuration_projects_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Projects”, “icon” → “fa fa-star”, “items” → list(mapping(“type” → “doctype”, “name” → “Project”, “description” → translated “Project master.”, “onboard” → 1), mapping(“ty ….

**Local steps**

- Return list(mapping(“label” → translated “Projects”, “icon” → “fa fa-star”, “items” → list(mapping(“type” → “doctype”, “name” → “Project”, “description” → translated “Project master.”, “onboard” → 1), mapping(“ty ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L294)

<a id="op-132528e1cf5e81"></a>
### Get context

`operation_enterprise_templates_pages_projects_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Project” via get\_doc.

**Local steps**

- Set project\_user from validate\_and\_get\_project\_user(project = Platform.form\_dict.project).
- Set context.no\_cache from 1.
- Set context.show\_sidebar from true.
- Set project from Platform.get\_doc(“Project”, Platform.form\_dict.project).
- Set project.tasks from get\_tasks(project.name, start = 0, item\_status = “open”, search = Platform.form\_dict.get(“search”)).
- If (project\_user and not project\_user.hide\_timesheets).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in project\_user → not project\_user.hide\_timesheets.
  - Set project.timesheets from get\_timesheets(project.name, start = 0, search = Platform.form\_dict.get(“search”)).
- If (project\_user and project\_user.view\_attachments).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in project\_user → project\_user.view\_attachments.
  - Set project.attachments from get\_attachments(project.name).
- Set context.doc from project.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L2101) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1348)

<a id="op-bba041605759ac"></a>
### Get tasks

`operation_enterprise_templates_pages_projects_business_behavior_get_tasks`

**Inputs** project, start = 0, search = no value, item\_status = no value.

**Record and data access** read “Task” via get\_all.

**Explicit results** list(filter(deferred anonymous expression, tasks)).

**Local steps**

- Set filters from mapping(“project” → project).
- If search.
  - Set filters at “subject” from tuple(“like”, formatted text %{search}%).
- Set tasks from Platform.get\_all(“Task”, filters = filters, fields = list(“name”, “subject”, “status”, “modified”, …), limit\_start = start, limit\_page\_length = 100).
- Set task\_nest from list().
- For each task in tasks.
  - If task.is\_group.
    - Set child\_tasks from list(filter(deferred anonymous expression, tasks)).
    - If len(child\_tasks).
      - Set task.children from child\_tasks.
  - Evaluate task\_nest.append(task).
- Return list(filter(deferred anonymous expression, tasks)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L2525) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1350)

<a id="op-524af967980d84"></a>
### Get task html

`operation_enterprise_templates_pages_projects_business_behavior_get_task_document_markup`

**Inputs** project, start = 0, item\_status = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.render\_template(“Enterprise/templates/includes/projects/project\_tasks.html”, mapping(“doc” → mapping(“name” → project, “project\_name” → project, “tasks” → get\_tasks(project, start, item\_status = i ….

**Local steps**

- Evaluate validate\_and\_get\_project\_user(project = project).
- Return Platform.render\_template(“Enterprise/templates/includes/projects/project\_tasks.html”, mapping(“doc” → mapping(“name” → project, “project\_name” → project, “tasks” → get\_tasks(project, start, item\_status = i ….

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L3055) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1349)
