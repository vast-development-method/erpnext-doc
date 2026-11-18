# Web content and issued documents · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Personal data deletion request

[Record definition](../../../../data/record-types/personal_data_deletion_request.json)

<a id="op-6e138610767e8c"></a>
### Confirm deletion

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_confirm_deletion`

**Inputs** email, name, host\_name.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** resolve a document from “Personal Data Deletion Request” via get\_doc.

**State and service calls** call save on doc · commit.

**Explicit results** no value.

**Local steps**

- If not verify\_request().
  - Return no value.
- Set doc from Platform.get\_doc(“Personal Data Deletion Request”, name).
- Set host\_name from Platform.utils.get\_url().
- If doc.status equals “Pending Verification”.
  - Set doc.status from “Pending Approval”.
  - Evaluate doc.save(ignore\_permissions = true).
  - Evaluate doc.notify\_system\_managers().
  - Evaluate Platform.db.commit().
  - Evaluate Platform.respond\_as\_web\_page(translated “Confirmed”, translated “The process for deletion of {0} data associated with {1} has been initiated.”.format(host\_name, email), indicator\_color = “green”).
- Otherwise.
  - Evaluate Platform.respond\_as\_web\_page(translated “Link Expired”, translated “This link has already been activated for verification.”, indicator\_color = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L5670) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1227)

<a id="op-6ed0538aff2d75"></a>
### Get pattern

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_get_pattern`

**Inputs** full\_match.

**Explicit results** re.compile(formatted text (?&lt;!\\.)\\b{re.escape(full\_match)}\\b(?!\\.)).

**Local steps**

- Return re.compile(formatted text (?&lt;!\\.)\\b{re.escape(full\_match)}\\b(?!\\.)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L6115) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1228)

## Record · Personal data download request

[Record definition](../../../../data/record-types/personal_data_download_request.json)

<a id="op-8cfe1a654d8590"></a>
### Personal Data Download Request.as dict

`operation_foundation_website_record_definitions_personal_data_download_request_business_behavior_personal_data_download_request_as_mapping`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** d.

**Local steps**

- Set d from super().as\_dict(expanded args, expanded names kwargs).
- Evaluate d.pop(“user\_name”, no value).
- Return d.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L299) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1261)

<a id="op-38a73c8c6029c6"></a>
### Personal Data Download Request.insert

`operation_foundation_website_record_definitions_personal_data_download_request_business_behavior_personal_data_download_request_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Record and data access** read “User” via exists.

**State and service calls** call insert on super().

**Explicit results** self · super().insert(expanded args, expanded names kwargs).

**Local steps**

- If not Platform.db.exists(“User”, self.user).
  - Set self.name from Platform.generate\_hash(length = 10).
  - Evaluate self.set\_user\_and\_timestamp().
  - Set self.user\_name from empty text.
  - Evaluate self.set(“\_\_islocal”, false).
  - Evaluate self.set(“\_\_unsaved”, false).
  - Return self.
- Return super().insert(expanded args, expanded names kwargs).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L426) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1263)

<a id="op-cb0da91817fe1b"></a>
### Personal Data Download Request.after insert

`operation_foundation_website_record_definitions_personal_data_download_request_business_behavior_personal_data_download_request_after_insert`

**Inputs** self.

**State and service calls** enqueue doc with self.doctype.

**Local steps**

- Set personal\_data from get\_user\_data(self.user).
- Evaluate Platform.enqueue\_doc(self.doctype, self.name, “generate\_file\_and\_send\_mail”, queue = “short”, personal\_data = personal\_data, now = Platform.in\_test).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue\_doc(self.doctype, self.name, “generate\_file\_and\_send\_mail”, queue = “short”, personal\_data = personal\_data, now = Platform.in\_test).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L695) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1260)

<a id="op-c418f2aaf47a75"></a>
### Personal Data Download Request.generate file and send mail

`operation_foundation_website_record_definitions_personal_data_download_request_business_behavior_personal_data_download_request_generate_file_and_send_mail`

**Inputs** self, personal\_data.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → ((((“Personal-Data-” + user\_name) + “-”) + self.name) + “.json”), “attached\_to\_doctype” → “Personal Data Download Request”, “attached\_to\_name” → self.name, …) via get\_doc.

**State and service calls** call save on f · request set\_value on “File” · call db\_set on self · sendmail.

**Local steps**

- Set user\_name from self.user\_name.replace(one space, “-”).
- Set f from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → ((((“Personal-Data-” + user\_name) + “-”) + self.name) + “.json”), “attached\_to\_doctype” → “Personal Data Download Request”, “attached\_to\_name” → s ….
- Evaluate f.save(ignore\_permissions = true).
- Evaluate Platform.db.set\_value(“File”, f.name, “owner”, self.user).
- Evaluate self.db\_set(“owner”, self.user).
- Set file\_link from ((Platform.utils.get\_url(“/api/method/Platform.utils.file\_manager.download\_file”) + “?”) + get\_signed\_params(mapping(“file\_url” → f.file\_url))).
- Set host\_name from Platform.local.site.
- Evaluate Platform.sendmail(recipients = self.user, subject = translated “Download Your Data”, template = “download\_data”, args = mapping(“user” → self.user, “user\_name” → self.user\_name, “link” → file\_link, “host\_n ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.user, subject = translated “Download Your Data”, template = “download\_data”, args = mapping(“user” → self.user, “user\_name” → self.user\_name, “link” → file\_link, “host\_n ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L32) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1262)

<a id="op-0452b742aa9349"></a>
### Get user data

`operation_foundation_website_record_definitions_personal_data_download_request_business_behavior_get_user_data`

**Inputs** user.

**Record and data access** read hook.get(“doctype”) via get\_all.

**Explicit results** json.dumps(data, indent = 2, default = str).

**Local steps**

- Set hooks from Platform.get\_hooks(“user\_data\_fields”).
- Set data from mapping().
- For each hook in hooks.
  - Set d from data.get(hook.get(“doctype”), list()).
  - Update d using + Platform.get\_all(hook.get(“doctype”), mapping(hook.get(“filter\_by”, “owner”) → user), list(“\*”)).
  - If d.
    - Evaluate data.update(mapping(hook.get(“doctype”) → d)).
- Return json.dumps(data, indent = 2, default = str).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_data\_fields”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L1527) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1259)

## Record · Portal settings

[Record definition](../../../../data/record-types/portal_settings.json)

<a id="op-278bf9ba8f743d"></a>
### Portal Settings.get all menu items

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_get_all_menu_items`

**Inputs** self.

**Explicit results** ((self.get(“menu”) or list()) + (self.get(“custom\_menu”) or list())).

**Local steps**

- Return ((self.get(“menu”) or list()) + (self.get(“custom\_menu”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“menu”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“custom\_menu”) → list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L4442) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1273)

<a id="op-5c24f38cef2901"></a>
### Portal Settings.init menu tables

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_initialize_menu_tables`

**Inputs** self.

**Local steps**

- For each fieldname in tuple(“menu”, “custom\_menu”).
  - If self.get(fieldname) is identical to no value.
    - Evaluate self.set(fieldname, list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L4549) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1274)

<a id="op-f5c8ed571fb97a"></a>
### Portal Settings.add item

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_add_item`

**Inputs** self, item.

**Explicit results** true.

**Local steps**

- Set exists from list of d for d drawn from (self.get(“menu”) or list()) where d.get(“route”) equals item.get(“route”).
  - Draw d from (self.get(“menu”) or list()), keep a combination only if (d.get(“route”) equals item.get(“route”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“menu”) → list().
- If (exists and item.get(“role”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in exists → item.get(“role”).
  - If exists at 0.role differs from item.get(“role”).
    - Set exists at 0.role from item.get(“role”).
    - Return true.
- Otherwise.
  - If not exists.
    - Set item at “enabled” from 1.
    - Evaluate self.append(“menu”, item).
    - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L4678) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1271)

<a id="op-b63a74d3327f30"></a>
### Portal Settings.reset

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_reset`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set self.menu from list().
- Evaluate self.sync\_menu().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync menu](operations-007.md#op-3ccccdae3a9237).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L5060) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1277)

<a id="op-3ccccdae3a9237"></a>
### Portal Settings.sync menu

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_sync_menu`

**Inputs** self.

**Record and data access** read “Role” via exists · resolve a document from mapping(“doctype” → “Role”, “role\_name” → item.get(“role”), “desk\_access” → 0) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Role”, “role\_name” → item.get(“role”), “desk\_access” → 0)) · call save on self.

**Local steps**

- Evaluate self.init\_menu\_tables().
- Set dirty from false.
- For each item in Platform.get\_hooks(“standard\_portal\_menu\_items”).
  - If (item.get(“role”) and not Platform.db.exists(“Role”, item.get(“role”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“role”) → not Platform.db.exists(“Role”, item.get(“role”)).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “Role”, “role\_name” → item.get(“role”), “desk\_access” → 0)).insert().
  - If self.add\_item(item).
    - Set dirty from true.
- Evaluate self.remove\_deleted\_doctype\_items().
- If dirty.
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [init menu tables](operations-007.md#op-5c24f38cef2901), [add item](operations-007.md#op-f5c8ed571fb97a), [remove deleted doctype items](operations-007.md#op-72e7731a5743de).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“standard\_portal\_menu\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L5146) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1278)

<a id="op-a8eb27428b0367"></a>
### Portal Settings.on update

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-007.md#op-da2631dc429c7c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L5535) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1275)

<a id="op-da2631dc429c7c"></a>
### Portal Settings.clear cache

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(user = “Guest”).
- Bind dependencies clear\_cache.
- Evaluate clear\_cache().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L5586) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1272)

<a id="op-72e7731a5743de"></a>
### Portal Settings.remove deleted doctype items

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_remove_deleted_record_type_items`

**Inputs** self.

**Record and data access** read “DocType” via get\_list.

**Local steps**

- Set existing\_doctypes from set(Platform.get\_list(“DocType”, pluck = “name”)).
- For each menu\_item in self.get\_all\_menu\_items().
  - If menu\_item.reference\_doctype does not belong to existing\_doctypes.
    - Evaluate self.remove(menu\_item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get all menu items](operations-007.md#op-278bf9ba8f743d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L5686) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1276)

<a id="op-566a1c720ae416"></a>
### Portal Settings.validate

`operation_foundation_website_record_definitions_portal_settings_business_behavior_portal_settings_validate`

**Inputs** self.

**Local steps**

- If (Platform.request and self.default\_portal\_home).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.request → self.default\_portal\_home.
  - Evaluate validate\_path(self.default\_portal\_home).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0524.json#L5858) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1279)

## Workspace · Print

<a id="op-c8bca55fe71e78"></a>
### Get print styles

`operation_foundation_binding_foundation_printing_page_print_print_get_print_styles`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Print Style” via get\_all.

**Explicit results** Platform.get\_all(“Print Style”, filters = mapping(“disabled” → 0), pluck = “name”, order\_by = “creation asc”).

**Local steps**

- Return Platform.get\_all(“Print Style”, filters = mapping(“disabled” → 0), pluck = “name”, order\_by = “creation asc”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1689)

<a id="op-2339abb5dcf28a"></a>
### Get print settings to show

`operation_foundation_printing_page_print_business_behavior_get_print_settings_to_show`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc · read “Print Settings” via get\_single.

**Explicit results** list() · print\_settings\_fields.

**Local steps**

- Set doc from Platform.get\_doc(doctype, docname).
- Evaluate doc.check\_permission(“read”).
- Set print\_settings from Platform.get\_single(“Print Settings”).
- If hasattr(doc, “get\_print\_settings”).
  - Set fields from (doc.get\_print\_settings() or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_print\_settings() → list().
- Otherwise.
  - Return list().
- Set print\_settings\_fields from list().
- For each fieldname in fields.
  - Set df from print\_settings.meta.get\_field(fieldname).
  - If not df.
    - Continue with the next iteration or loop test.
  - Set df.default from print\_settings.get(fieldname).
  - Evaluate print\_settings\_fields.append(df).
- Return print\_settings\_fields.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L41) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1725)

## Record · Print format

[Record definition](../../../../data/record-types/print_format.json)

<a id="op-5604a082280ff2"></a>
### Renders from file

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_renders_from_file`

**Inputs** doc.

**Declared result** bool.

**Record and data access** read “DocType” via get\_value · read “Module Def” via get\_cached\_value.

**Explicit results** false · os.path.exists(path).

**Local steps**

- Bind dependencies os.
- Bind dependencies get\_module\_path, scrub.
- If (doc.get(“standard”) differs from “Yes” or doc.get(“custom\_format”) or doc.get(“raw\_printing”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“standard”) differs from “Yes” → doc.get(“custom\_format”) → doc.get(“raw\_printing”).
  - Return false.
- Set module from (doc.get(“module”) or Platform.db.get\_value(“DocType”, doc.get(“doc\_type”), “module”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“module”) → Platform.db.get\_value(“DocType”, doc.get(“doc\_type”), “module”).
- If (not module or Platform.get\_cached\_value(“Module Def”, module, “custom”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not module → Platform.get\_cached\_value(“Module Def”, module, “custom”).
  - Return false.
- Attempt the following.
  - Set path from os.path.join(get\_module\_path(module, “Print Format”, doc.name), (scrub(doc.name) + “.html”)).
- On failure (tuple(Platform.DoesNotExistError, ImportError)).
  - Return false.
- Return os.path.exists(path).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Module Def”, module, “custom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L223) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1655)

<a id="op-51c2b96b42d826"></a>
### Is classic layout

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_is_classic_layout`

**Inputs** format\_data.

**Declared result** bool.

**Explicit results** false · isinstance(format\_data, list).

**Local steps**

- If not format\_data.
  - Return false.
- If isinstance(format\_data, str).
  - Attempt the following.
    - Set format\_data from json.loads(format\_data).
  - On failure (ValueError).
    - Return false.
- Return isinstance(format\_data, list).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L966) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1771)

<a id="op-3d68439538c6f6"></a>
### Uses beta renderer

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_uses_beta_renderer`

**Inputs** print\_format.

**Declared result** bool.

**Explicit results** false · (print\_format.get(“standard”) differs from “Yes” or bool(print\_format.get(“format\_data”))).

**Local steps**

- If not print\_format.
  - Return false.
- If (print\_format.get(“custom\_format”) or print\_format.get(“raw\_printing”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.get(“custom\_format”) → print\_format.get(“raw\_printing”).
  - Return false.
- If print\_format.get(“print\_designer”).
  - Return false.
- If not print\_format.get(“print\_format\_builder\_beta”).
  - Return false.
- Return (print\_format.get(“standard”) differs from “Yes” or bool(print\_format.get(“format\_data”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.get(“standard”) differs from “Yes” → bool(print\_format.get(“format\_data”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L64) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1774)

<a id="op-0fbeb4a8c1db25"></a>
### Uses legacy weasyprint

`operation_foundation_binding_foundation_printing_doctype_print_format_classic_converter_uses_legacy_weasyprint`

**Inputs** print\_format.

**Declared result** bool.

**Explicit results** (uses\_beta\_renderer(print\_format) and print\_format.get(“pdf\_generator”) equals “WeasyPrint”).

**Local steps**

- Return (uses\_beta\_renderer(print\_format) and print\_format.get(“pdf\_generator”) equals “WeasyPrint”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in uses\_beta\_renderer(print\_format) → print\_format.get(“pdf\_generator”) equals “WeasyPrint”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L226) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1658)

<a id="op-766fab928642ad"></a>
### Convert classic to beta

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_convert_classic_to_beta`

**Inputs** format\_data, meta, print\_format = no value.

**Declared result** tuple at tuple(dict, list).

**State and service calls** call insert on section at “columns” at 0 at “fields”.

**Explicit results** tuple(layout, dropped).

**Local steps**

- Bind dependencies layout\_page\_settings.
- Set dropped from list().
- Set show\_section\_headings from cint(print\_format.get(“show\_section\_headings”)) when print\_format, otherwise 0.
  - Value choice on print\_format — true gives cint(print\_format.get(“show\_section\_headings”)), false gives 0.
- Set line\_breaks from cint(print\_format.get(“line\_breaks”)) when print\_format, otherwise 0.
  - Value choice on print\_format — true gives cint(print\_format.get(“line\_breaks”)), false gives 0.
- Set paper\_size from print\_format.get(“paper\_size”) when print\_format, otherwise no value.
  - Value choice on print\_format — true gives print\_format.get(“paper\_size”), false gives no value.
- Set layout from mapping(“sections” → list(), “header” → mapping(“columns” → list(mapping(“label” → empty text, “fields” → list()))), “footer” → mapping(“columns” → list(mapping(“label” → empty text, “fields” → list())))).
- If layout\_page\_settings(mapping(“page” → mapping(“size” → paper\_size))).
  - Set layout at “page” from mapping(“size” → paper\_size).
- Set data from list of Platform.\_dict(df) for df drawn from (format\_data or list()) where isinstance(df, dict).
  - Draw df from (format\_data or list()), keep a combination only if (isinstance(df, dict)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in format\_data → list().
- If (data and data at 0.fieldname equals “print\_heading\_template”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → data at 0.fieldname equals “print\_heading\_template”.
  - Set head from data.pop(0).
  - If head.options.
    - Evaluate layout at “header” at “columns” at 0 at “fields”.append(mapping(“label” → empty text, “fieldname” → “print\_heading\_template”, “fieldtype” → “HTML”, “html” → head.options, …)).
- Set state from Platform.\_dict(section = no value, column = no value, html\_count = 0, skip = false).
- Bind local operation new\_section for subsequent calls.
- Bind local operation new\_column for subsequent calls.
- Bind local operation add\_field for subsequent calls.
- For each df in data.
  - If df.fieldtype belongs to tuple(“Section Break”, “Tab Break”).
    - Set state.skip from bool(cint(df.print\_hide)).
    - If state.skip.
      - Set state.section, state.column from no value.
    - Otherwise.
      - Evaluate new\_section(df.label when df.fieldtype equals “Section Break”, otherwise empty text).
        - Value choice on df.fieldtype equals “Section Break” — true gives df.label, false gives empty text.
  - Otherwise.
    - If state.skip.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If df.fieldtype equals “Column Break”.
        - Evaluate new\_column().
      - Otherwise.
        - If df.fieldtype equals “HTML”.
          - Update state.html\_count using + 1.
          - Evaluate add\_field(mapping(“label” → (df.label or “Custom HTML”), “fieldname” → formatted text custom\_html\_{state.html\_count}, “fieldtype” → “HTML”, “html” → (df.options or empty text), …)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → “Custom HTML”.
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.options → empty text.
        - Otherwise.
          - If df.fieldname.
            - If cint(df.print\_hide).
              - Continue with the next iteration or loop test.
            - Set meta\_df from meta.get\_field(df.fieldname).
            - If not meta\_df.
              - Evaluate dropped.append(df.fieldname).
              - Continue with the next iteration or loop test.
            - Set field from mapping(“label” → (df.label or meta\_df.label or meta\_df.fieldname), “fieldname” → meta\_df.fieldname, “fieldtype” → meta\_df.fieldtype, “options” → meta\_df.options).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → meta\_df.label → meta\_df.fieldname.
            - If df.align.
              - Set field at “align” from df.align.
            - If cint(df.nolabel).
              - Set field at “show\_label” from “hide”.
            - If meta\_df.fieldtype equals “Table”.
              - Set field at “show\_label” from “hide”.
              - Set field at “table\_columns” from convert\_table\_columns(df, meta\_df, dropped).
            - Evaluate add\_field(field).
- Set layout at “sections” from list of section for section drawn from layout at “sections” where any(generator of column at “fields” for column drawn from section at “columns”).
  - Draw section from layout at “sections”, keep a combination only if (any(generator of column at “fields” for column drawn from section at “columns”)).
  - Draw column from section at “columns”.
- If (not data and not layout at “sections”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not data → not layout at “sections”.
  - Set layout at “sections” from create\_default\_layout(meta) at “sections”.
- For each section in layout at “sections” at slice 1 to no value.
  - Set section at “margin” from mapping(“top” → CONVERTED\_SECTION\_GAP\_PX, “right” → 0, “bottom” → 0, “left” → 0).
- If line\_breaks.
  - For each section in layout at “sections” at slice 1 to no value.
    - Evaluate section at “columns” at 0 at “fields”.insert(0, mapping(“label” → empty text, “fieldname” → “divider”, “fieldtype” → “Divider”, “custom” → 1)).
- Return tuple(layout, dropped).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L59) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1760)

<a id="op-9fb8b4cc584823"></a>
### Convert classic to beta.new section

`operation_foundation_printing_record_definitions_print_format_classic_converter_business_behavior_convert_classic_to_beta_new_section`

**Inputs** label = empty text.

**Local steps**

- Set state.section from mapping(“label” → (label or empty text), “columns” → list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in label → empty text.
- If (label and not show\_section\_headings).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in label → not show\_section\_headings.
  - Set state.section at “show\_label” from “hide”.
- Set state.column from no value.
- Evaluate layout at “sections”.append(state.section).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L3811) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1763)
