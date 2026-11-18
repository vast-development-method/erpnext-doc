# Web content and issued documents · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Discussion reply

[Record definition](../../../../data/record-types/discussion_reply.json)

<a id="op-cbde1dd2170453"></a>
### Discussion Reply.after insert

`operation_foundation_website_record_definitions_discussion_reply_business_behavior_discussion_reply_after_insert`

**Inputs** self.

**Record and data access** read “Discussion Reply” via count · read “Discussion Topic” via get\_all.

**State and service calls** publish realtime.

**Local steps**

- Set replies from Platform.db.count(“Discussion Reply”, mapping(“topic” → self.topic)).
- Set topic\_info from Platform.get\_all(“Discussion Topic”, mapping(“name” → self.topic), list(“reference\_doctype”, “reference\_docname”, “name”, “title”, …)).
- Set template from Platform.render\_template(“Platform/templates/discussions/reply\_card.html”, mapping(“reply” → self, “topic” → mapping(“name” → self.topic), “loop” → mapping(“index” → replies), “single\_thread” → true when n ….
  - Value choice on not topic\_info at 0.title — true gives true, false gives false.
- Set sidebar from Platform.render\_template(“Platform/templates/discussions/sidebar.html”, mapping(“topic” → topic\_info at 0)).
- Set new\_topic\_template from Platform.render\_template(“Platform/templates/discussions/reply\_section.html”, mapping(“topic” → topic\_info at 0)).
- Evaluate Platform.publish\_realtime(event = “publish\_message”, room = get\_website\_room(), message = mapping(“template” → template, “topic\_info” → topic\_info at 0, “sidebar” → sidebar, “new\_topic\_template” → new\_topi ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(event = “publish\_message”, room = get\_website\_room(), message = mapping(“template” → template, “topic\_info” → topic\_info at 0, “sidebar” → sidebar, “new\_topic\_template” → new\_topi ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1196)

<a id="op-034c685dd8100a"></a>
### Discussion Reply.after delete

`operation_foundation_website_record_definitions_discussion_reply_business_behavior_discussion_reply_after_delete`

**Inputs** self.

**State and service calls** publish realtime.

**Local steps**

- Evaluate Platform.publish\_realtime(event = “delete\_message”, room = get\_website\_room(), message = mapping(“reply\_name” → self.name), after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(event = “delete\_message”, room = get\_website\_room(), message = mapping(“reply\_name” → self.name), after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L632) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1195)

<a id="op-1f52e4a2c6c704"></a>
### Delete message

`operation_foundation_website_record_definitions_discussion_reply_business_behavior_delete_message`

**Inputs** reply\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Discussion Reply” via get\_value.

**State and service calls** request delete\_doc for “Discussion Reply”.

**Local steps**

- Set owner from Platform.db.get\_value(“Discussion Reply”, reply\_name, “owner”).
- If owner equals Platform.session.user.
  - Evaluate Platform.delete\_doc(“Discussion Reply”, reply\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L746) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1194)

## Record · Discussion topic

[Record definition](../../../../data/record-types/discussion_topic.json)

<a id="op-74c70f1e3d20d5"></a>
### Submit discussion

`operation_foundation_website_record_definitions_discussion_topic_business_behavior_submit_discussion`

**Inputs** doctype, docname, reply, title, topic\_name = no value, reply\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Discussion Reply” via get\_doc · resolve a document from mapping(“doctype” → “Discussion Topic”, “title” → title, “reference\_doctype” → doctype, “reference\_docname” → docname) via get\_doc.

**State and service calls** call save on doc · call save on topic.

**Explicit results** no value · topic\_name · topic.name.

**Explicit failure paths** validation helper with Platform.PermissionError — Platform.\_(“You can only edit your own replies.”).

**Local steps**

- If reply\_name.
  - Set doc from Platform.get\_doc(“Discussion Reply”, reply\_name).
  - If doc.owner differs from Platform.session.user.
    - Call the validation error handler Platform.throw(Platform.\_(“You can only edit your own replies.”), Platform.PermissionError).
  - Set doc.reply from reply.
  - Evaluate doc.save(ignore\_permissions = true).
  - Return no value.
- If topic\_name.
  - Evaluate save\_message(reply, topic\_name).
  - Return topic\_name.
- Set topic from Platform.get\_doc(mapping(“doctype” → “Discussion Topic”, “title” → title, “reference\_doctype” → doctype, “reference\_docname” → docname)).
- Evaluate topic.save(ignore\_permissions = true).
- Evaluate save\_message(reply, topic.name).
- Return topic.name.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L1959) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1203)

<a id="op-41e2223c0a3068"></a>
### Save message

`operation_foundation_website_record_definitions_discussion_topic_business_behavior_save_message`

**Inputs** reply, topic.

**Record and data access** resolve a document from mapping(“doctype” → “Discussion Reply”, “reply” → reply, “topic” → topic) via get\_doc.

**State and service calls** call save on Platform.get\_doc(mapping(“doctype” → “Discussion Reply”, “reply” → reply, “topic” → topic)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Discussion Reply”, “reply” → reply, “topic” → topic)).save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L2501) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1202)

## Service · Doctype

<a id="op-bb0ebc88a54f60"></a>
### Extract

`operation_foundation_gettext_extractors_record_type_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- Set doctype from data.get(“name”).
- yield tuple(get\_line\_number(text, “name”, doctype), “\_”, doctype, list(“Name of a DocType”)).
- Set doctype\_description from data.get(“description”).
- If doctype\_description.
  - yield tuple(get\_line\_number(text, “description”, doctype\_description), “\_”, doctype\_description, list(“Description of a DocType”)).
- Set messages from list().
- For each field in data.get(“fields”, list()).
  - Evaluate messages.extend(extract\_messages\_from\_docfield(doctype, field, text)).
- Evaluate messages.extend(extract\_messages\_from\_links(doctype, data.get(“links”, list()), text)).
- yield values from generator of tuple(lineno, “\_”, message, list(comment)) for tuple(lineno, message, comment) drawn from messages.
  - Draw tuple(lineno, message, comment) from messages.
- yield values from generator of tuple(get\_line\_number(text, “role”, perm at “role”), “\_”, perm at “role”, list(“Name of a role”)) for perm drawn from data.get(“permissions”, list()) where “role” belongs to perm.
  - Draw perm from data.get(“permissions”, list()), keep a combination only if (“role” belongs to perm).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L3) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L364)

## Service · Document page

<a id="op-fd52a5a86772ad"></a>
### Document Page.can render

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_can_render`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- If self.search\_in\_doctypes\_with\_web\_view().
  - Return true.
- If self.search\_web\_page\_dynamic\_routes().
  - Return true.
- Return false.

**Methods declared on this owner** [search in doctypes with web view](operations-002.md#op-e87aebc30264a7), [search web page dynamic routes](operations-002.md#op-53f6a8d690cc9e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L1787) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1118)

<a id="op-e87aebc30264a7"></a>
### Document Page.search in doctypes with web view

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_search_in_record_types_with_web_view`

**Inputs** self.

**Record and data access** resolve a document from self.doctype via get\_cached\_doc.

**Explicit results** (doc.meta.allow\_guest\_to\_view or doc.has\_permission() or Platform.has\_website\_permission(doc)).

**Local steps**

- If document bound to \_find\_matching\_document\_webview(self.path).
  - Set tuple(self.doctype, self.docname) from document.
  - Set doc from Platform.get\_cached\_doc(self.doctype, self.docname).
  - Return (doc.meta.allow\_guest\_to\_view or doc.has\_permission() or Platform.has\_website\_permission(doc)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.meta.allow\_guest\_to\_view → doc.has\_permission() → Platform.has\_website\_permission(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(self.doctype, self.docname) · effective access from doc.has\_permission().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L1885) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1122)

<a id="op-53f6a8d690cc9e"></a>
### Document Page.search web page dynamic routes

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_search_web_page_dynamic_routes`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Set d from get\_page\_info\_from\_web\_page\_with\_dynamic\_routes(self.path).
- If d.
  - Set self.doctype from d.doctype.
  - Set self.docname from d.name.
  - Return true.
- Otherwise.
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L2081) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1123)

<a id="op-3d0d33dc4e3c14"></a>
### Document Page.render

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_render`

**Inputs** self.

**Explicit results** self.build\_response(html).

**Local steps**

- Set html from self.get\_html().
- Set html from self.add\_csrf\_token(html).
- Return self.build\_response(html).

**Methods declared on this owner** [get html](operations-002.md#op-2bb195365d6c1b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L2212) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1121)

<a id="op-2bb195365d6c1b"></a>
### Document Page.get html

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_get_document_markup`

**Inputs** self.

**Wrappers, in declaration order** cache\_html.

**Record and data access** resolve a document from self.doctype via get\_cached\_doc.

**Explicit results** Platform.get\_template(self.template\_path).render(self.context).

**Local steps**

- Set self.doc from Platform.get\_cached\_doc(self.doctype, self.docname).
- Evaluate self.init\_context().
- Evaluate self.update\_context().
- Evaluate self.post\_process\_context().
- Return Platform.get\_template(self.template\_path).render(self.context).

**Methods declared on this owner** [update context](operations-002.md#op-8fdcb04546ac0a).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(self.doctype, self.docname).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L2322) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1120)

<a id="op-8fdcb04546ac0a"></a>
### Document Page.update context

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_update_context`

**Inputs** self.

**Local steps**

- Set self.context.doc from self.doc.
- Evaluate self.context.update(self.context.doc.as\_dict()).
- Evaluate self.context.update(self.context.doc.get\_page\_info()).
- Set self.template\_path from (self.context.template or self.template\_path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.context.template → self.template\_path.
- If not self.template\_path.
  - Set self.template\_path from self.context.doc.meta.get\_web\_template().
- If hasattr(self.doc, “get\_context”).
  - Set ret from self.doc.get\_context(self.context).
  - If ret.
    - Evaluate self.context.update(ret).
- For each prop in tuple(“no\_cache”, “sitemap”).
  - If prop does not belong to self.context.
    - Set self.context at prop from getattr(self.doc, prop, false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self.doc, prop, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L2509) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1124)

<a id="op-17db95297fac59"></a>
### Document Page.get condition field

`operation_foundation_website_page_renderers_document_page_business_behavior_document_page_get_condition_field`

**Inputs** meta.

**Wrappers, in declaration order** staticmethod.

**Explicit results** condition\_field.

**Local steps**

- Set condition\_field from no value.
- If meta.is\_published\_field.
  - Set condition\_field from meta.is\_published\_field.
- Otherwise.
  - If not meta.custom.
    - Set controller from get\_controller(meta.name).
    - Set condition\_field from controller.website.condition\_field.
- Return condition\_field.

**Values supplied outside this operation** selected callable from get\_controller(meta.name).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L2954) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1119)

<a id="op-209cae17a0201f"></a>
### Find matching document webview

`operation_foundation_website_page_renderers_document_page_business_behavior_find_matching_document_webview`

**Inputs** route.

**Wrappers, in declaration order** redis\_cache(ttl = (60 × 60)).

**Declared result** (tuple at tuple(str, str) bitwise or no value).

**Record and data access** read doctype via get\_all · read doctype via get\_value.

**Explicit results** tuple(doctype, docname).

**Explicit failure paths** e.

**Local steps**

- For each doctype in get\_doctypes\_with\_web\_view().
  - Set filters from dict(route = route).
  - Set meta from Platform.get\_meta(doctype).
  - Set condition\_field from DocumentPage.get\_condition\_field(meta).
  - If condition\_field.
    - Set filters at condition\_field from 1.
  - Attempt the following.
    - Set docname from no value.
    - If meta.is\_virtual.
      - If doclist bound to Platform.get\_all(doctype, filters = filters, fields = list(“name”), limit = 1).
        - Set docname from doclist at 0.get(“name”).
    - Otherwise.
      - Set docname from Platform.db.get\_value(doctype, filters, “name”).
    - If docname.
      - Return tuple(doctype, docname).
  - On failure (Exception) bound to e.
    - If not Platform.db.is\_missing\_column(e).
      - Raise e.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L3113) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1125)

## Service · Error page

<a id="op-308728590861d1"></a>
### Error Page.initialize

`operation_foundation_website_page_renderers_error_page_business_behavior_error_page_initialize`

**Inputs** self, path = no value, http\_status\_code = no value, exception = no value, title = no value, message = no value.

**Local steps**

- Set path from “error”.
- Evaluate super().\_\_init\_\_(path = path, http\_status\_code = http\_status\_code).
- Set self.exception from exception.
- Set self.http\_status\_code from http\_status\_code.
- Set self.title from title.
- Set self.message from message.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L3631) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1127)

<a id="op-da97c5ad304dfd"></a>
### Error Page.can render

`operation_foundation_website_page_renderers_error_page_business_behavior_error_page_can_render`

**Inputs** self.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L3842) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1126)

<a id="op-ae345982a22281"></a>
### Error Page.init context

`operation_foundation_website_page_renderers_error_page_business_behavior_error_page_initialize_context`

**Inputs** self.

**Local steps**

- Evaluate super().init\_context().
- Set self.context.http\_status\_code from (self.http\_status\_code or getattr(self.exception, “http\_status\_code”, no value) or 500).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.http\_status\_code → getattr(self.exception, “http\_status\_code”, no value) → 500.
- Set self.context.title from (self.title or getattr(self.exception, “title”, no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.title → getattr(self.exception, “title”, no value).
- Set self.context.message from (self.message or getattr(self.exception, “message”, no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.message → getattr(self.exception, “message”, no value).
- Set self.context.command from getattr(self.exception, “command”, no value).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self.exception, “http\_status\_code”, no value), getattr(self.exception, “title”, no value) and 2 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L3879) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1128)

## Service · Fieldtypes

<a id="op-ce8f253ee316e4"></a>
### Is image column

`operation_foundation_binding_foundation_printing_fieldtypes_is_image_column`

**Inputs** fieldtype, src.

**Declared result** bool.

**Explicit results** true · (fieldtype equals “Attach” and Platform.utils.is\_image(str((src or empty text)))).

**Local steps**

- If fieldtype belongs to IMAGE\_FIELDTYPES.
  - Return true.
- Return (fieldtype equals “Attach” and Platform.utils.is\_image(str((src or empty text)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Attach” → Platform.utils.is\_image(str((src or empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in src → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1681)

## Record · Help article

[Record definition](../../../../data/record-types/help_article.json)

<a id="op-43410cad1b8abd"></a>
### Help Article.validate

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_route().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set route](operations-002.md#op-e3b9370bc934b0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3090) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1217)

<a id="op-e3b9370bc934b0"></a>
### Help Article.set route

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_set_route`

**Inputs** self.

**Record and data access** read “Help Category” via get\_value.

**Local steps**

- If not self.route.
  - Set self.route from “/”.join(list(Platform.get\_value(“Help Category”, self.category, “route”), self.scrub(self.title))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3141) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1215)

<a id="op-ce81fc53f18978"></a>
### Help Article.on update

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_category().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update category](operations-002.md#op-34eee2f1f0260d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3293) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1214)

<a id="op-c9b8f933c36c04"></a>
### Help Article.clear cache

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate clear\_knowledge\_base\_cache().
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3344) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1211)

<a id="op-34eee2f1f0260d"></a>
### Help Article.update category

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_update_category`

**Inputs** self.

**Record and data access** read “Help Article” via count · resolve a document from “Help Category” via get\_doc.

**State and service calls** call save on cat.

**Local steps**

- Set cnt from Platform.db.count(“Help Article”, filters = mapping(“category” → self.category, “published” → 1)).
- Set cat from Platform.get\_doc(“Help Category”, self.category).
- Set cat.help\_articles from cnt.
- Evaluate cat.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3417) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1216)

<a id="op-7dc806c4692dad"></a>
### Help Article.get context

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_get_context`

**Inputs** self, context.

**Record and data access** resolve a document from “Help Category” via get\_doc.

**Local steps**

- If is\_markdown(context.content).
  - Set context.content from markdown(context.content).
- Set context.login\_required from true.
- Set context.category from Platform.get\_doc(“Help Category”, self.category).
- Set context.level\_class from get\_level\_class(self.level).
- Set context.comment\_list from get\_comment\_list(self.doctype, self.name).
- Set context.show\_sidebar from true.
- Set context.sidebar\_items from get\_sidebar\_items().
- Set context.parents from self.get\_parents(context).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get parents](operations-003.md#op-dea8d36dc06516).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3610) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1212)
