# Web content and issued documents · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Website settings

[Record definition](../../../../data/record-types/website_settings.json)

<a id="op-0cdd98ee37e6f2"></a>
### Get website settings

`operation_foundation_website_record_definitions_website_settings_business_behavior_get_website_settings`

**Inputs** context = no value.

**Explicit results** context.

**Local steps**

- Set hooks from Platform.get\_hooks().
- Set context from Platform.\_dict((context or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → mapping().
- Set settings from Platform.client\_cache.get\_doc(“Website Settings”).
- Set context from context.update(mapping(“top\_bar\_items” → modify\_header\_footer\_items(settings.top\_bar\_items), “footer\_items” → modify\_header\_footer\_items(settings.footer\_items), “post\_login” → list(mapping(“label” → transl ….
- For each k in list(“banner\_html”, “banner\_image”, “brand\_html”, “copyright”, …).
  - If setting\_value bound to settings.get(k).
    - Set context at k from setting\_value.
- For each k in list(“facebook\_share”, “google\_plus\_one”, “twitter\_share”, “linked\_in\_share”, …).
  - Set context at k from cint(context.get(k)).
- If settings.address.
  - Set context at “footer\_address” from settings.address.
- If Platform.request.
  - Set context.url from quote(str(get\_request\_site\_address(full\_address = true)), safe = “/:”).
- Set context.encoded\_title from quote(encode((context.title or empty text)), empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.title → empty text.
- Set context.web\_include\_js from (hooks.web\_include\_js or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.web\_include\_js → list().
- Set context.web\_include\_css from (hooks.web\_include\_css or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.web\_include\_css → list().
- Set context.web\_include\_icons from (hooks.web\_include\_icons or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.web\_include\_icons → list().
- Set via\_hooks from (hooks.website\_context or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.website\_context → list().
- For each key in via\_hooks.
  - Set context at key from via\_hooks at key.
  - If (key does not belong to tuple(“top\_bar\_items”, “footer\_items”, “post\_login”) and isinstance(context at key, (list bitwise or tuple))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in key does not belong to tuple(“top\_bar\_items”, “footer\_items”, “post\_login”) → isinstance(context at key, (list bitwise or tuple)).
    - Set context at key from context at key at negative 1.
- If context.disable\_website\_theme.
  - Set context.theme from Platform.\_dict().
- Otherwise.
  - Bind dependencies get\_active\_theme.
  - Set context.theme from (get\_active\_theme() or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_active\_theme() → Platform.\_dict().
- If not context.get(“favicon”).
  - Set context at “favicon” from “/assets/Platform/images/Platform-favicon.svg”.
- If (settings.favicon and settings.favicon differs from “attach\_files:”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.favicon → settings.favicon differs from “attach\_files:”.
  - Set context at “favicon” from settings.favicon.
- Set context at “hide\_login” from settings.hide\_login.
- If settings.splash\_image.
  - Set context at “splash\_image” from settings.splash\_image.
- Set context.read\_only\_mode from Platform.flags.read\_only.
- Set context.boot from get\_boot\_data().
- Return context.

**Values supplied outside this operation** selected callable from Platform.get\_hooks().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L50) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1464)

<a id="op-3aa7683a5fb76a"></a>
### Get items

`operation_foundation_website_record_definitions_website_settings_business_behavior_get_items`

**Inputs** parentfield.

**Declared result** list at dict.

**Record and data access** read “Top Bar Item” via get\_all.

**Explicit results** modify\_header\_footer\_items(\_items).

**Local steps**

- Set \_items from Platform.get\_all(“Top Bar Item”, filters = mapping(“parent” → “Website Settings”, “parentfield” → parentfield), order\_by = “idx asc”, fields = “\*”).
- Return modify\_header\_footer\_items(\_items).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L1510) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1463)

<a id="op-46deb07991ee05"></a>
### Modify header footer items

`operation_foundation_website_record_definitions_website_settings_business_behavior_modify_header_footer_items`

**Inputs** items.

**Explicit results** top\_items.

**Local steps**

- Set top\_items from items.copy().
- For each item in items.
  - Set item.child\_items from list().
- For each item in items.
  - If not item.parent\_label.
    - Continue with the next iteration or loop test.
  - For each top\_bar\_item in top\_items.
    - If top\_bar\_item.label differs from item.parent\_label.
      - Continue with the next iteration or loop test.
    - If not top\_bar\_item.get(“child\_items”).
      - Set top\_bar\_item.child\_items from list().
    - Evaluate top\_bar\_item.child\_items.append(item).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return top\_items.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L1681) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1465)

<a id="op-236aac15b8ccd8"></a>
### Get auto account deletion

`operation_foundation_website_record_definitions_website_settings_business_behavior_get_auto_account_deletion`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** read “Website Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“Website Settings”, “auto\_account\_deletion”).

**Local steps**

- Return Platform.db.get\_single\_value(“Website Settings”, “auto\_account\_deletion”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Website Settings”, “auto\_account\_deletion”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L1941) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1462)

## Record · Website sidebar

[Record definition](../../../../data/record-types/website_sidebar.json)

<a id="op-4cb41aa4bfb9de"></a>
### Website Sidebar.get items

`operation_foundation_website_record_definitions_website_sidebar_business_behavior_website_sidebar_get_items`

**Inputs** self.

**Record and data access** read “Website Sidebar Item” via get\_all.

**Explicit results** out.

**Local steps**

- Set items from Platform.get\_all(“Website Sidebar Item”, filters = mapping(“parent” → self.name), fields = list(“title”, “route”, “group”), order\_by = “idx asc”).
- Set items\_by\_group from mapping().
- Set items\_without\_group from list().
- For each item in items.
  - If item.group.
    - Evaluate items\_by\_group.setdefault(item.group, list()).append(item).
  - Otherwise.
    - Evaluate items\_without\_group.append(item).
- Set out from list of mapping(“group\_title” → group, “group\_items” → items) for tuple(group, items) drawn from items\_by\_group.items().
  - Draw tuple(group, items) from items\_by\_group.items().
- Update out using + items\_without\_group.
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L2035) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1480)

## Record · Website slideshow

[Record definition](../../../../data/record-types/website_slideshow.json)

<a id="op-cc75344a34f2eb"></a>
### Website Slideshow.validate

`operation_foundation_website_record_definitions_website_slideshow_business_behavior_website_slideshow_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_images().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate images](operations-025.md#op-c74127806d3a81).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L2401) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1483)

<a id="op-87e59ca47b04fd"></a>
### Website Slideshow.on update

`operation_foundation_website_record_definitions_website_slideshow_business_behavior_website_slideshow_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_cache.
- Evaluate clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L2452) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1482)

<a id="op-c74127806d3a81"></a>
### Website Slideshow.validate images

`operation_foundation_website_record_definitions_website_slideshow_business_behavior_website_slideshow_validate_images`

**Inputs** self.

**Record and data access** read “File” via get\_all.

**Explicit failure paths** validation helper — translated “All Images attached to Website Slideshow should be public”.

**Local steps**

- Set files from map(deferred anonymous expression, self.slideshow\_items).
- If (files and self.slideshow\_items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in files → self.slideshow\_items.
  - Set result from Platform.get\_all(“File”, filters = mapping(“file\_url” → tuple(“in”, list(files))), fields = “is\_private”).
  - If any(generator of file.is\_private for file drawn from result).
    - Draw file from result.
    - Call the validation error handler Platform.throw(translated “All Images attached to Website Slideshow should be public”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L2507) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1484)

<a id="op-e1bdf4d355f6e0"></a>
### Get slideshow

`operation_foundation_website_record_definitions_website_slideshow_business_behavior_get_slideshow`

**Inputs** doc.

**Record and data access** resolve a document from “Website Slideshow” via get\_doc.

**Explicit results** mapping() · mapping(“slides” → slideshow.get(mapping(“doctype” → “Website Slideshow Item”)), “slideshow\_header” → (slideshow.header or empty text)).

**Local steps**

- If not doc.slideshow.
  - Return mapping().
- Set slideshow from Platform.get\_doc(“Website Slideshow”, doc.slideshow).
- Return mapping(“slides” → slideshow.get(mapping(“doctype” → “Website Slideshow Item”)), “slideshow\_header” → (slideshow.header or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in slideshow.header → empty text.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L2793) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1481)

## Record · Website theme

[Record definition](../../../../data/record-types/website_theme.json)

<a id="op-c6137c0e5600ff"></a>
### Website Theme.validate

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_if\_customizable().
- Evaluate self.generate\_bootstrap\_theme().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate if customizable](operations-025.md#op-00d64e02920e07), [generate bootstrap theme](operations-025.md#op-7aee6f2b0f44c6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4264) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1498)

<a id="op-32cb15e47d18af"></a>
### Website Theme.on update

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_on_update`

**Inputs** self.

**Local steps**

- If (not self.custom and Platform.local.conf.get(“developer\_mode”) and not Platform.flags.in\_import and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.custom → Platform.local.conf.get(“developer\_mode”) → not Platform.flags.in\_import → not Platform.in\_test.
  - Evaluate self.export\_doc().
- Evaluate self.clear\_cache\_if\_current\_theme().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export doc](operations-025.md#op-309c83caad2b31), [clear cache if current theme](operations-025.md#op-db1d93351b103e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4335) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1496)

<a id="op-a94b76fd19c06f"></a>
### Website Theme.is standard and not valid user

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_is_standard_and_not_valid_user`

**Inputs** self.

**Explicit results** (not self.custom and not Platform.local.conf.get(“developer\_mode”) and not (Platform.flags.in\_import or Platform.in\_test or Platform.flags.in\_migrate)).

**Local steps**

- Return (not self.custom and not Platform.local.conf.get(“developer\_mode”) and not (Platform.flags.in\_import or Platform.in\_test or Platform.flags.in\_migrate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.custom → not Platform.local.conf.get(“developer\_mode”) → not (Platform.flags.in\_import or Platform.in\_test or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.in\_test → Platform.flags.in\_migrate.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4487) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1494)

<a id="op-f76ccfc9fc0b52"></a>
### Website Theme.on trash

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to delete a standard Website Theme”.

**Local steps**

- If self.is\_standard\_and\_not\_valid\_user().
  - Call the validation error handler Platform.throw(translated “You are not allowed to delete a standard Website Theme”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is standard and not valid user](operations-025.md#op-a94b76fd19c06f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4613) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1495)

<a id="op-00d64e02920e07"></a>
### Website Theme.validate if customizable

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_validate_if_customizable`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please Duplicate this Website Theme to customize.”.

**Local steps**

- If self.is\_standard\_and\_not\_valid\_user().
  - Call the validation error handler Platform.throw(translated “Please Duplicate this Website Theme to customize.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is standard and not valid user](operations-025.md#op-a94b76fd19c06f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4714) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1499)

<a id="op-309c83caad2b31"></a>
### Website Theme.export doc

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_export_record`

**Inputs** self.

**Local steps**

- Bind dependencies export\_to\_files.
- Evaluate export\_to\_files(record\_list = list(list(“Website Theme”, self.name)), create\_init = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4807) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1491)

<a id="op-db1d93351b103e"></a>
### Website Theme.clear cache if current theme

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_clear_cache_if_current_theme`

**Inputs** self.

**Record and data access** resolve a document from “Website Settings” via get\_doc.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install equals “Platform”.
  - Return no value.
- Set website\_settings from Platform.get\_doc(“Website Settings”, “Website Settings”).
- If getattr(website\_settings, “website\_theme”, no value) equals self.name.
  - Evaluate website\_settings.clear\_cache().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(website\_settings, “website\_theme”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L4906) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1489)

<a id="op-7aee6f2b0f44c6"></a>
### Website Theme.generate bootstrap theme

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_generate_bootstrap_theme`

**Inputs** self.

**State and service calls** msgprint with translated “Compiled Successfully”.

**Explicit failure paths** validation helper — translated “Theme name cannot contain '/' or path separators” · validation helper — formatted text &lt;div style="font-family: monospace;"&gt;{stderr}&lt;/div&gt;.

**Local steps**

- Bind dependencies PIPE, Popen.
- Set folder\_path from abspath(Platform.utils.get\_files\_path(“website\_theme”, is\_private = false)).
- Evaluate Platform.create\_folder(folder\_path).
- If self.custom.
  - Evaluate self.delete\_old\_theme\_files(folder\_path).
- Set suffix from Platform.generate\_hash(length = 8) when self.custom, otherwise “style”.
  - Value choice on self.custom — true gives Platform.generate\_hash(length = 8), false gives “style”.
- Set file\_name from (((Platform.scrub(self.name) + “\_”) + suffix) + “.css”).
- If (os.sep belongs to file\_name or (os.altsep and os.altsep belongs to file\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.sep belongs to file\_name → (os.altsep and os.altsep belongs to file\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.altsep → os.altsep belongs to file\_name.
  - Call the validation error handler Platform.throw(translated “Theme name cannot contain '/' or path separators”, title = translated “Invalid Website Theme Name”).
- Set output\_path from join\_path(folder\_path, file\_name).
- Set base\_path from os.path.realpath(folder\_path).
- Set real\_output\_path from os.path.realpath(output\_path).
- If os.path.commonpath(tuple(base\_path, real\_output\_path)) differs from base\_path.
  - Call the validation error handler Platform.throw(translated “Theme name cannot contain '/' or path separators”, title = translated “Invalid Website Theme Name”).
- Set self.theme\_scss, content from get\_scss(self).
- Set content from content.replace(whitespace '\\n', “\\n”).
- Set command from list(“node”, “generate\_bootstrap\_theme.js”, output\_path, content).
- Set process from Popen(command, cwd = Platform.get\_app\_source\_path(“Platform”), stdout = PIPE, stderr = PIPE).
- Set stderr from process.communicate() at 1.
- If stderr.
  - Set stderr from Platform.safe\_decode(stderr).
  - Set stderr from stderr.replace(whitespace '\\n', text in the contract).
  - Call the validation error handler Platform.throw(formatted text &lt;div style="font-family: monospace;"&gt;{stderr}&lt;/div&gt;).
- Otherwise.
  - Set self.theme\_url from (“/files/website\_theme/” + file\_name).
- Evaluate Platform.msgprint(translated “Compiled Successfully”, alert = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete old theme files](operations-025.md#op-137a3031970838).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 8).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L55) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1492)

<a id="op-137a3031970838"></a>
### Website Theme.delete old theme files

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_delete_old_theme_files`

**Inputs** self, folder\_path.

**Local steps**

- Bind dependencies os.
- Set theme\_files from list().
- For each fname in os.listdir(folder\_path).
  - If (fname.startswith((Platform.scrub(self.name) + “\_”)) and fname.endswith(“.css”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fname.startswith((Platform.scrub(self.name) + “\_”)) → fname.endswith(“.css”).
    - Evaluate theme\_files.append((Path(folder\_path) ÷ fname)).
- Evaluate theme\_files.sort(key = deferred anonymous expression, reverse = true).
- For each old\_file in theme\_files at slice 2 to no value.
  - Evaluate old\_file.unlink().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L5798) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1490)

<a id="op-3b0742530e8636"></a>
### Website Theme.set as default

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_set_as_default`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Website Settings” via get\_doc.

**State and service calls** call save on self · call save on website\_settings.

**Local steps**

- Evaluate self.save().
- Set website\_settings from Platform.get\_doc(“Website Settings”).
- Set website\_settings.website\_theme from self.name.
- Set website\_settings.ignore\_validate from true.
- Evaluate website\_settings.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L6131) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1497)

<a id="op-c4a99455450b81"></a>
### Website Theme.get apps

`operation_foundation_website_record_definitions_website_theme_business_behavior_website_theme_get_apps`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list of mapping(“name” → app, “title” → values at “title”) for tuple(app, values) drawn from apps.items().

**Local steps**

- Bind dependencies get\_versions.
- Set apps from get\_versions().
- Return list of mapping(“name” → app, “title” → values at “title”) for tuple(app, values) drawn from apps.items().
  - Draw tuple(app, values) from apps.items().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L6291) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1493)

<a id="op-11c561db7c2d80"></a>
### Get active theme

`operation_foundation_website_record_definitions_website_theme_business_behavior_get_active_theme`

**Inputs** no declared parameters.

**Declared result** (“WebsiteTheme” bitwise or no value).

**Explicit results** Platform.client\_cache.get\_doc(“Website Theme”, website\_theme).

**Local steps**

- If website\_theme bound to Platform.get\_website\_settings(“website\_theme”).
  - Attempt the following.
    - Return Platform.client\_cache.get\_doc(“Website Theme”, website\_theme).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L6461) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1486)

<a id="op-d73c4270cc1f6f"></a>
### Get scss

`operation_foundation_website_record_definitions_website_theme_business_behavior_get_style_sheet`

**Inputs** website\_theme.

**Explicit results** Platform.render\_template(“Platform/website/doctype/website\_theme/website\_theme\_template.scss”, context).

**Local steps**

- Set apps\_to\_ignore from tuple(generator of (d.app + “/”) for d drawn from website\_theme.ignored\_apps).
  - Draw d from website\_theme.ignored\_apps.
- Set available\_imports from get\_scss\_paths().
- Set imports\_to\_include from list of d for d drawn from available\_imports where not d.startswith(apps\_to\_ignore).
  - Draw d from available\_imports, keep a combination only if (not d.startswith(apps\_to\_ignore)).
- Set context from website\_theme.as\_dict().
- Set context at “website\_theme\_scss” from imports\_to\_include.
- Return Platform.render\_template(“Platform/website/doctype/website\_theme/website\_theme\_template.scss”, context).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L6621) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1487)

<a id="op-3c63a8ca90539a"></a>
### Get scss paths

`operation_foundation_website_record_definitions_website_theme_business_behavior_get_style_sheet_paths`

**Inputs** no declared parameters.

**Explicit results** import\_path\_list.

**Local steps**

- Set import\_path\_list from list().
- Set scss\_files from list(“public/scss/website.scss”, “public/scss/website.bundle.scss”).
- For each app in Platform.get\_installed\_apps().
  - For each scss\_file in scss\_files.
    - Set full\_path from Platform.get\_app\_path(app, scss\_file).
    - If path\_exists(full\_path).
      - Set import\_path from splitext(join\_path(app, scss\_file)) at 0.
      - Evaluate import\_path\_list.append(import\_path).
- Return import\_path\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L54) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1488)

<a id="op-594146827d91bc"></a>
### After migrate

`operation_foundation_website_record_definitions_website_theme_business_behavior_after_migrate`

**Inputs** no declared parameters.

**Record and data access** read “Website Settings” via get\_single\_value · resolve a document from “Website Theme” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- Set website\_theme from Platform.db.get\_single\_value(“Website Settings”, “website\_theme”).
- If (not website\_theme or website\_theme equals “Standard”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not website\_theme → website\_theme equals “Standard”.
  - Return no value.
- Set doc from Platform.get\_doc(“Website Theme”, website\_theme).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Website Settings”, “website\_theme”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L7097) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1485)
