# Web content and issued documents · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Template page

<a id="op-ea924c88c79509"></a>
### Template Page.post process context

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_post_process_context`

**Inputs** self.

**Local steps**

- Evaluate self.set\_user\_info().
- Evaluate self.add\_sidebar\_and\_breadcrumbs().
- Evaluate super().post\_process\_context().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set user info](operations-013.md#op-e7ab6751581d99), [add sidebar and breadcrumbs](operations-013.md#op-6ce66e88e58975).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L1117) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1161)

<a id="op-6ce66e88e58975"></a>
### Template Page.add sidebar and breadcrumbs

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_add_sidebar_and_breadcrumbs`

**Inputs** self.

**Local steps**

- If not self.context.sidebar\_items.
  - Set self.context.sidebar\_items from get\_sidebar\_items(self.context.website\_sidebar, self.basepath).
- If (self.context.add\_breadcrumbs and not self.context.parents).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.context.add\_breadcrumbs → not self.context.parents.
  - Set parent\_path from os.path.dirname(self.path).
  - If self.path.endswith(“index”).
    - Set parent\_path from os.path.dirname(parent\_path).
  - For each parent\_file\_path in self.get\_index\_path\_options(parent\_path).
    - Set parent\_file\_path from os.path.join(self.app\_path, self.file\_dir, parent\_file\_path).
    - If os.path.isfile(parent\_file\_path).
      - Set parent\_page\_context from get\_page\_info(parent\_file\_path, self.app, self.file\_dir).
      - If parent\_page\_context.
        - Set self.context.parents from list(dict(route = os.path.dirname(self.path), title = parent\_page\_context.title)).
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get index path options](operations-012.md#op-180408858fc72f).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L1214) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1150)

<a id="op-88178654755576"></a>
### Template Page.set pymodule

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_pymodule`

**Inputs** self.

**Local steps**

- Set template\_basepath from os.path.splitext(self.template\_path) at 0.
- Set self.pymodule\_name from no value.
- Set self.pymodule\_path from os.path.join(os.path.dirname(template\_basepath), (os.path.basename(template\_basepath.replace(“-”, “\_”)) + “.py”)).
- If os.path.exists(os.path.join(self.app\_path, self.pymodule\_path)).
  - Set self.pymodule\_name from ((self.app + “.”) + self.pymodule\_path.replace(os.path.sep, “.”) at slice no value to negative 3).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L1712) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1169)

<a id="op-49f9b8968522fb"></a>
### Template Page.setup template source

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_setup_template_source`

**Inputs** self.

**Local steps**

- Set self.original\_source, self.source from self.get\_raw\_template().
- Evaluate self.extract\_frontmatter().
- Evaluate self.convert\_from\_markdown().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get raw template](operations-013.md#op-a89fe8d2c62b28), [extract frontmatter](operations-013.md#op-102b7a8e5dc680), [convert from markdown](operations-013.md#op-dd751775824544).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L2064) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1174)

<a id="op-e9c1de74c5707e"></a>
### Template Page.update context

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_update_context`

**Inputs** self.

**Local steps**

- Evaluate self.set\_page\_properties().
- Set self.context.build\_version from Platform.utils.get\_build\_version().
- If self.pymodule\_name.
  - Set self.pymodule from Platform.get\_module(self.pymodule\_name).
  - Evaluate self.set\_pymodule\_properties().
  - Set data from self.run\_pymodule\_method(“get\_context”).
  - If data.
    - Evaluate self.context.update(data).
- Set self.context.developer\_mode from Platform.conf.developer\_mode.
- If self.context.http\_status\_code.
  - Set self.http\_status\_code from self.context.http\_status\_code.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set page properties](operations-013.md#op-9025b383160b50), [set pymodule properties](operations-013.md#op-20cc494d4f018d), [run pymodule method](operations-013.md#op-1893c3f4852f52).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L2173) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1175)

<a id="op-20cc494d4f018d"></a>
### Template Page.set pymodule properties

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_pymodule_properties`

**Inputs** self.

**Local steps**

- For each prop in WEBPAGE\_PY\_MODULE\_PROPERTIES.
  - If hasattr(self.pymodule, prop).
    - Set self.context at prop from getattr(self.pymodule, prop).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self.pymodule, prop).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L2474) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1170)

<a id="op-9025b383160b50"></a>
### Template Page.set page properties

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_page_properties`

**Inputs** self.

**Local steps**

- Set self.context.base\_template from (self.context.base\_template or get\_base\_template(self.path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.context.base\_template → get\_base\_template(self.path).
- Set self.context.basepath from self.basepath.
- Set self.context.basename from self.basename.
- Set self.context.name from self.name.
- Set self.context.path from self.path.
- Set self.context.route from self.path.
- Set self.context.template from self.template\_path.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L2594) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1166)

<a id="op-5ed7085339bf3a"></a>
### Template Page.set properties from source

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_properties_from_source`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.source.
  - Return no value.
- Set context from self.context.
- If not context.title.
  - Set context.title from extract\_title(self.source, self.path).
- Set base\_template from extract\_comment\_tag(self.source, “base\_template”).
- If base\_template.
  - Set context.base\_template from base\_template.
- If (context.base\_template and “{%- extends” does not belong to self.source and “{% extends” does not belong to self.source and “&lt;/body&gt;” does not belong to self.source).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in context.base\_template → “{%- extends” does not belong to self.source → “{% extends” does not belong to self.source → “&lt;/body&gt;” does not belong to self.source.
  - Set self.source from formatted text {% extends "{context.base\_template}" %}  {% block page\_content %}{self.source}{% endblock %}.
- Evaluate self.set\_properties\_via\_comments().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set properties via comments](operations-013.md#op-7a41e461ce8418).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L2836) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1167)

<a id="op-7a41e461ce8418"></a>
### Template Page.set properties via comments

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_properties_via_comments`

**Inputs** self.

**Local steps**

- For each tuple(comment, tuple(context\_key, value)) in COMMENT\_PROPERTY\_KEY\_VALUE\_MAP.items().
  - Set comment\_tag from formatted text &lt;!-- {comment} --&gt;.
  - If comment\_tag belongs to self.source.
    - Bind dependencies click.
    - Set self.context at context\_key from value.
    - Evaluate click.echo(formatted text  ⚠️  DEPRECATION WARNING: {comment\_tag} will be deprecated on 2021-12-31.).
    - Evaluate click.echo(formatted text Please remove it from {self.template\_path} in {self.app}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L3191) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1168)

<a id="op-1893c3f4852f52"></a>
### Template Page.run pymodule method

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_run_pymodule_method`

**Inputs** self, method\_name.

**Explicit results** method(self.context) · method().

**Local steps**

- If hasattr(self.pymodule, method\_name).
  - Bind dependencies inspect.
  - Set method from getattr(self.pymodule, method\_name).
  - If inspect.getfullargspec(method).args.
    - Return method(self.context).
  - Otherwise.
    - Return method().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self.pymodule, method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L3465) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1164)

<a id="op-7a8709e6640ce6"></a>
### Template Page.render template

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_render_template`

**Inputs** self.

**Explicit results** html.

**Local steps**

- If self.template\_path.endswith(“min.js”).
  - Set html from self.source.
- Otherwise.
  - If self.context.safe\_render is distinct from no value.
    - Set safe\_render from self.context.safe\_render.
  - Otherwise.
    - Set safe\_render from true.
  - Set src\_modified from self.source is distinct from self.original\_source.
  - Set html from Platform.render\_template(self.source when src\_modified, otherwise self.context.template, self.context, safe\_render = safe\_render).
    - Value choice on src\_modified — true gives self.source, false gives self.context.template.
- Return html.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L3643) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1163)

<a id="op-a94b9cc9c3d51e"></a>
### Template Page.extends template

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_extends_template`

**Inputs** self.

**Explicit results** (self.template\_path.endswith(tuple(“.html”, “.md”)) and (“{%- extends” belongs to self.source or “{% extends” belongs to self.source)).

**Local steps**

- Return (self.template\_path.endswith(tuple(“.html”, “.md”)) and (“{%- extends” belongs to self.source or “{% extends” belongs to self.source)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.template\_path.endswith(tuple(“.html”, “.md”)) → (“{%- extends” belongs to self.source or “{% extends” belongs to self.source).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “{%- extends” belongs to self.source → “{% extends” belongs to self.source.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L3900) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1153)

<a id="op-a89fe8d2c62b28"></a>
### Template Page.get raw template

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_get_raw_template`

**Inputs** self.

**Explicit results** Platform.get\_jloader().get\_source(Platform.get\_jenv(), self.context.template) at 0.

**Local steps**

- Return Platform.get\_jloader().get\_source(Platform.get\_jenv(), self.context.template) at 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L4019) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1158)

<a id="op-d82e35840cc43a"></a>
### Template Page.load colocated files

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_load_colocated_files`

**Inputs** self.

**Local steps**

- Set js\_path from (self.basename + “.js”).
- If (os.path.exists(js\_path) and “{% block script %}” does not belong to self.source).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(js\_path) → “{% block script %}” does not belong to self.source.
  - Set self.context.colocated\_js from self.get\_colocated\_file(js\_path).
- Set css\_path from (self.basename + “.css”).
- If (os.path.exists(css\_path) and “{% block style %}” does not belong to self.source).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(css\_path) → “{% block style %}” does not belong to self.source.
  - Set self.context.colocated\_css from self.get\_colocated\_file(css\_path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get colocated file](operations-013.md#op-3839d7143956cd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L4119) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1160)

<a id="op-3839d7143956cd"></a>
### Template Page.get colocated file

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_get_colocated_file`

**Inputs** self, path.

**Explicit results** f.read().

**Local steps**

- Within open(path, encoding = “utf-8”) bound as f.
  - Return f.read().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L4389) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1155)

<a id="op-102b7a8e5dc680"></a>
### Template Page.extract frontmatter

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_extract_frontmatter`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.template\_path.endswith(tuple(“.md”, “.html”)).
  - Return no value.
- Attempt the following.
  - Set res from get\_frontmatter(self.source).
  - If res at “attributes”.
    - Evaluate self.context.update(res at “attributes”).
    - Set self.source from res at “body”.
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L4485) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1154)

<a id="op-dd751775824544"></a>
### Template Page.convert from markdown

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_convert_from_markdown`

**Inputs** self.

**Local steps**

- If self.template\_path.endswith(“.md”).
  - Set self.source from Platform.utils.md\_to\_html(self.source).
  - Set self.context.page\_toc\_html from self.source.toc\_html.
  - If not self.context.show\_sidebar.
    - Set self.source from ((text in the contract + self.source) + “&lt;/div&gt;”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L4710) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1152)

<a id="op-2ecb28b6b6b922"></a>
### Template Page.update toc

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_update_toc`

**Inputs** self, html.

**Explicit results** html.

**Local steps**

- If “{index}” belongs to html.
  - Set html from html.replace(“{index}”, get\_toc(self.path)).
- If “{next}” belongs to html.
  - Set html from html.replace(“{next}”, get\_next\_link(self.path)).
- Return html.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L4903) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1176)

<a id="op-fddbefcb21ac2c"></a>
### Template Page.set standard path

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_standard_path`

**Inputs** self, path.

**Local steps**

- Set self.app from “Platform”.
- Set self.app\_path from Platform.get\_app\_path(“Platform”).
- Set self.path from path.
- Set self.template\_path from formatted text www/{path}.html.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5094) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1171)

<a id="op-e74c4d6533ae6e"></a>
### Template Page.set missing values

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_missing_values`

**Inputs** self.

**Local steps**

- Evaluate super().set\_missing\_values().
- Set self.context.docs\_base\_url from “/docs”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5238) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1165)

<a id="op-e7ab6751581d99"></a>
### Template Page.set user info

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_user_info`

**Inputs** self.

**Local steps**

- Bind dependencies get\_fullname\_and\_avatar.
- Set info from get\_fullname\_and\_avatar(Platform.session.user).
- Set self.context at “fullname” from info.fullname.
- Set self.context at “user\_image” from info.avatar.
- Set self.context at “user” from info.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5315) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1173)

<a id="op-36e23c36dbdd18"></a>
### Get start folders

`operation_foundation_website_page_renderers_template_page_business_behavior_get_start_folders`

**Inputs** no declared parameters.

**Explicit results** (Platform.local.flags.web\_pages\_folders or tuple(“www”, “templates/pages”)).

**Local steps**

- Return (Platform.local.flags.web\_pages\_folders or tuple(“www”, “templates/pages”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.web\_pages\_folders → tuple(“www”, “templates/pages”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5485) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1149)

## Service · Translate

<a id="op-ce3cd6b2528d2b"></a>
### New catalog

`operation_foundation_gettext_translate_business_behavior_new_catalog`

**Inputs** app, locale = no value.

**Declared result** Catalog.

**Explicit results** Catalog(locale = locale, domain = “messages”, msgid\_bugs\_address = app\_email, language\_team = app\_email, …).

**Local steps**

- Bind local operation get\_hook for subsequent calls.
- Set app\_email from get\_hook(“app\_email”, app).
- Return Catalog(locale = locale, domain = “messages”, msgid\_bugs\_address = app\_email, language\_team = app\_email, …).

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6112) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L405)

<a id="op-8d9d67d0b6ca5f"></a>
### New catalog.get hook

`operation_foundation_gettext_translate_business_behavior_new_catalog_get_hook`

**Inputs** hook, app.

**Explicit results** Platform.get\_hooks(hook, list(no value), app) at 0.

**Local steps**

- Return Platform.get\_hooks(hook, list(no value), app) at 0.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook, list(no value), app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6438) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L406)
