# Web content and issued documents · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Help article

[Record definition](../../../../data/record-types/help_article.json)

<a id="op-dea8d36dc06516"></a>
### Help Article.get parents

`operation_foundation_website_record_definitions_help_article_business_behavior_help_article_get_parents`

**Inputs** self, context.

**Explicit results** list(mapping(“title” → context.category.category\_name, “route” → context.category.route)).

**Local steps**

- Return list(mapping(“title” → context.category.category\_name, “route” → context.category.route)).

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L3933) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1213)

<a id="op-94d084fabb98ca"></a>
### Get list context

`operation_foundation_website_record_definitions_help_article_business_behavior_get_list_context`

**Inputs** context = no value.

**Record and data access** read “Help Category” via get\_value.

**Explicit results** list\_context.

**Local steps**

- Set filters from dict(published = 1).
- Set category from Platform.db.get\_value(“Help Category”, mapping(“route” → Platform.local.path)).
- If category.
  - Set filters at “category” from category.
- Set list\_context from Platform.\_dict(title = (category or translated “Knowledge Base”), get\_level\_class = get\_level\_class, show\_sidebar = true, sidebar\_items = get\_sidebar\_items(), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in category → translated “Knowledge Base”.
- If Platform.local.form\_dict.txt.
  - Set list\_context.blog\_subtitle from translated “Filtered by "{0}"”.format(Platform.local.form\_dict.txt).
- Return list\_context.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L4031) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1208)

<a id="op-a55f245f106621"></a>
### Get level class

`operation_foundation_website_record_definitions_help_article_business_behavior_get_level_class`

**Inputs** level.

**Explicit results** mapping(“Beginner” → “green”, “Intermediate” → “orange”, “Expert” → “red”) at level.

**Local steps**

- Return mapping(“Beginner” → “green”, “Intermediate” → “orange”, “Expert” → “red”) at level.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L4427) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1207)

<a id="op-7e2aba82f912ee"></a>
### Get sidebar items

`operation_foundation_website_record_definitions_help_article_business_behavior_get_sidebar_items`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.get\_value(“knowledge\_base:category\_sidebar”, \_get).

**Local steps**

- Bind local operation \_get for subsequent calls.
- Return Platform.cache.get\_value(“knowledge\_base:category\_sidebar”, \_get).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L28) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1209)

<a id="op-ca6bd02c813b37"></a>
### Get sidebar items.get

`operation_foundation_website_record_definitions_help_article_business_behavior_get_sidebar_items_get`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Help Category).

**Explicit results** Platform.db.sql(query text (SELECT, Help Category), as\_dict = true).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Help Category), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L29) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1210)

<a id="op-910e7a17aa1ba0"></a>
### Clear knowledge base cache

`operation_foundation_website_record_definitions_help_article_business_behavior_clear_knowledge_base_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.cache.delete\_value(“knowledge\_base:category\_sidebar”).
- Evaluate Platform.cache.delete\_value(“knowledge\_base:faq”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L4675) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1206)

<a id="op-9b5ba99259a046"></a>
### Add feedback

`operation_foundation_website_record_definitions_help_article_business_behavior_add_feedback`

**Inputs** article, helpful.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), rate\_limit(key = “article”, limit = 5, seconds = (60 × 60)).

**Record and data access** read “Help Article” via get\_value.

**State and service calls** request set\_value on “Help Article”.

**Local steps**

- Set field from “not\_helpful” when helpful equals “No”, otherwise “helpful”.
  - Value choice on helpful equals “No” — true gives “not\_helpful”, false gives “helpful”.
- Set value from cint(Platform.db.get\_value(“Help Article”, article, field)).
- Evaluate Platform.db.set\_value(“Help Article”, article, field, (value + 1), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L4751) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1205)

## Record · Help category

[Record definition](../../../../data/record-types/help_category.json)

<a id="op-b42d1a2f557bce"></a>
### Help Category.before insert

`operation_foundation_website_record_definitions_help_category_business_behavior_help_category_before_insert`

**Inputs** self.

**Local steps**

- Set self.published from 1.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L5921) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L276) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1223)

<a id="op-4c5e2215251a01"></a>
### Help Category.autoname

`operation_foundation_website_record_definitions_help_category_business_behavior_help_category_autoname`

**Inputs** self.

**Local steps**

- Set self.name from self.category\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L5968) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L275) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1222)

<a id="op-2bcae89a8e9aae"></a>
### Help Category.validate

`operation_foundation_website_record_definitions_help_category_business_behavior_help_category_validate`

**Inputs** self.

**Record and data access** read “Help Article” via get\_all.

**State and service calls** request set\_value on “Help Article”.

**Local steps**

- Evaluate self.set\_route().
- If not self.published.
  - For each d in Platform.get\_all(“Help Article”, dict(category = self.name)).
    - Evaluate Platform.db.set\_value(“Help Article”, d.name, “published”, 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set route](operations-003.md#op-a3b1d955342cfe).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6021) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1226)

<a id="op-a3b1d955342cfe"></a>
### Help Category.set route

`operation_foundation_website_record_definitions_help_category_business_behavior_help_category_set_route`

**Inputs** self.

**Local steps**

- If not self.route.
  - Set self.route from (“kb/” + self.scrub(self.category\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6211) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1225)

<a id="op-72e3f752a8396a"></a>
### Help Category.clear cache

`operation_foundation_website_record_definitions_help_category_business_behavior_help_category_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate clear\_knowledge\_base\_cache().
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6305) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L277) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1224)

## Service · Html template

<a id="op-2f56ed289e9e93"></a>
### Extract

`operation_foundation_gettext_extractors_hypertext_markup_template_business_behavior_extract`

**Inputs** remaining positional values args, remaining named values kwargs.

**Local steps**

- Set fileobj from (args at 0 or kwargs at “fileobj”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args at 0 → kwargs at “fileobj”.
- Set code from fileobj.read().decode(“utf-8”).
- For each tuple(lineno, funcname, messages, comments) in babel\_extract(expanded args, expanded names kwargs).
  - If (funcname equals “\_” and isinstance(messages, tuple) and len(messages) &gt; 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in funcname equals “\_” → isinstance(messages, tuple) → len(messages) &gt; 1.
    - Set funcname from “pgettext”.
    - Set messages from tuple(messages at negative 1, messages at 0).
  - yield tuple(lineno, funcname, messages, comments).
- For each tuple(lineno, message, context) in extract\_messages\_from\_code(code).
  - If context.
    - yield tuple(lineno, “pgettext”, tuple(context, message), list()).
  - Otherwise.
    - yield tuple(lineno, “\_”, message, list()).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L7133) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L356)

## Service · Javascript

<a id="op-7d4d5c7e82370b"></a>
### Extract

`operation_foundation_gettext_extractors_presentation_expression_runtime_business_behavior_extract`

**Inputs** fileobj, keywords, comment\_tags, options.

**Local steps**

- Set code from fileobj.read().decode(“utf-8”).
- For each tuple(lineno, funcname, messages) in extract\_javascript(code, options = options).
  - If (not messages or not messages at 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not messages → not messages at 0.
    - Continue with the next iteration or loop test.
  - Set funcname from “gettext”.
  - If isinstance(messages, tuple).
    - If (len(messages) equals 3 and messages at 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(messages) equals 3 → messages at 2.
      - Set funcname from “pgettext”.
      - Set messages from tuple(messages at 2, messages at 0).
    - Otherwise.
      - Set messages from messages at 0.
  - yield tuple(lineno, funcname, messages, list()).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L361)

<a id="op-af6ad9c4031c83"></a>
### Extract javascript

`operation_foundation_gettext_extractors_presentation_expression_runtime_business_behavior_extract_client_language`

**Inputs** code, keywords = no value, options = no value, lineno = 1.

**Local steps**

- Bind dependencies Token, tokenize, unquote\_string.
- If options is identical to no value.
  - Set options from mapping().
- If keywords is identical to no value.
  - Set keywords from tuple(“\_\_”).
- Set funcname, message\_lineno from no value.
- Set messages from list().
- Set last\_argument from no value.
- Set concatenate\_next from false.
- Set last\_token from no value.
- Set call\_stack from negative 1.
- Set tree\_level from 0.
- Set opening\_operators from set(“&#91;”, “{”).
- Set closing\_operators from set(“&#93;”, “}”).
- Set all\_container\_operators from opening\_operators.union(closing\_operators).
- Set dotted from any(generator of “.” belongs to kw for kw drawn from keywords).
  - Draw kw from keywords.
- Set outer\_calls from list().
- For each token in tokenize(code, jsx = true, dotted = dotted, template\_string = options.get(“template\_string”, true), lineno = lineno).
  - If (funcname and (last\_token and last\_token.type equals “name”) and token.type equals “template\_string”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in funcname → (last\_token and last\_token.type equals “name”) → token.type equals “template\_string”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_token → last\_token.type equals “name”.
    - Set message\_lineno from token.lineno.
    - Set messages from list(unquote\_string(token.value)).
    - Set call\_stack from 0.
    - Set tree\_level from 0.
    - Set token from Token(“operator”, “)”, token.lineno).
  - If (not funcname and token.type equals “template\_string”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not funcname → token.type equals “template\_string”.
    - yield values from parse\_template\_string(token.value, keywords, options, token.lineno).
  - If (token.type equals “operator” and token.value equals “(”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in token.type equals “operator” → token.value equals “(”.
    - If (call\_stack ≥ 0 and last\_token.type equals “name” and last\_token.value belongs to keywords).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in call\_stack ≥ 0 → last\_token.type equals “name” → last\_token.value belongs to keywords.
      - Evaluate outer\_calls.append(tuple(funcname, message\_lineno, messages, last\_argument, …)).
      - Set funcname from last\_token.value.
      - Set message\_lineno from token.lineno.
      - Set messages from list().
      - Set last\_argument from no value.
      - Set concatenate\_next from false.
      - Set call\_stack from 0.
      - Set tree\_level from 0.
    - Otherwise.
      - If funcname.
        - Set message\_lineno from token.lineno.
        - Update call\_stack using + 1.
  - Otherwise.
    - If (call\_stack ≥ 0 and token.type equals “operator” and token.value belongs to all\_container\_operators).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in call\_stack ≥ 0 → token.type equals “operator” → token.value belongs to all\_container\_operators.
      - If token.value belongs to opening\_operators.
        - Update tree\_level using + 1.
      - If token.value belongs to closing\_operators.
        - Update tree\_level using − 1.
    - Otherwise.
      - If ((call\_stack equals negative 1 and token.type equals “linecomment”) or token.type equals “multilinecomment”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (call\_stack equals negative 1 and token.type equals “linecomment”) → token.type equals “multilinecomment”.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in call\_stack equals negative 1 → token.type equals “linecomment”.
        - Take no action here.
      - Otherwise.
        - If (funcname and call\_stack equals 0).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in funcname → call\_stack equals 0.
          - If (token.type equals “operator” and token.value equals “)”).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in token.type equals “operator” → token.value equals “)”.
            - If last\_argument is distinct from no value.
              - Evaluate messages.append(last\_argument).
            - If len(messages) &gt; 1.
              - Set messages from tuple(messages).
            - Otherwise.
              - If messages.
                - Set messages from messages at 0.
              - Otherwise.
                - Set messages from no value.
            - If messages is distinct from no value.
              - yield tuple(message\_lineno, funcname, messages).
            - If outer\_calls.
              - Set tuple(funcname, message\_lineno, messages, last\_argument, …) from outer\_calls.pop().
            - Otherwise.
              - Set funcname, message\_lineno, last\_argument from no value.
              - Set concatenate\_next from false.
              - Set messages from list().
              - Set call\_stack from negative 1.
              - Set tree\_level from 0.
          - Otherwise.
            - If token.type belongs to tuple(“string”, “template\_string”).
              - Set new\_value from unquote\_string(token.value).
              - If tree\_level &gt; 0.
                - Take no action here.
              - Otherwise.
                - If concatenate\_next.
                  - Set last\_argument from ((last\_argument or empty text) + new\_value).
                    - Evaluate in order, stop at the first true operand, otherwise use the last operand in last\_argument → empty text.
                  - Set concatenate\_next from false.
                - Otherwise.
                  - Set last\_argument from new\_value.
            - Otherwise.
              - If token.type equals “operator”.
                - If token.value equals “,”.
                  - If last\_argument is distinct from no value.
                    - Evaluate messages.append(last\_argument).
                    - Set last\_argument from no value.
                  - Otherwise.
                    - If tree\_level equals 0.
                      - Evaluate messages.append(no value).
                  - Set concatenate\_next from false.
                - Otherwise.
                  - If token.value equals “+”.
                    - Set concatenate\_next from true.
        - Otherwise.
          - If (call\_stack &gt; 0 and token.type equals “operator” and token.value equals “)”).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in call\_stack &gt; 0 → token.type equals “operator” → token.value equals “)”.
            - Update call\_stack using − 1.
            - Set tree\_level from 0.
          - Otherwise.
            - If (funcname and call\_stack equals negative 1).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in funcname → call\_stack equals negative 1.
              - Set funcname from no value.
            - Otherwise.
              - If (call\_stack equals negative 1 and token.type equals “name” and token.value belongs to keywords and (last\_token is identical to no value or last\_token.type differs from “name” or last\_token.value differs fr ….
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in call\_stack equals negative 1 → token.type equals “name” → token.value belongs to keywords → (last\_token is identical to no value or last\_token.type differs from “name” or last\_token.value differs from “function”).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in last\_token is identical to no value → last\_token.type differs from “name” → last\_token.value differs from “function”.
                - Set funcname from token.value.
  - Set last\_token from token.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L2) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L362)

<a id="op-6147f6e6e5ecf1"></a>
### Parse template string

`operation_foundation_gettext_extractors_presentation_expression_runtime_business_behavior_parse_template_string`

**Inputs** template\_string, keywords, options, lineno = 1.

**Local steps**

- Set prev\_character from no value.
- Set current\_lineno from lineno.
- Set level from 0.
- Set inside\_expression\_str from false.
- Set expression\_lineno from lineno.
- Set expression\_contents from empty text.
- For each character in template\_string at slice 1 to negative 1.
  - If not level.
    - If (character equals “{” and prev\_character equals “$”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in character equals “{” → prev\_character equals “$”.
      - Set expression\_lineno from current\_lineno.
      - Update level using + 1.
  - Otherwise.
    - Update expression\_contents using + character.
    - If inside\_expression\_str.
      - If (inside\_expression\_str equals character and prev\_character differs from “\\\\”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in inside\_expression\_str equals character → prev\_character differs from “\\\\”.
        - Set inside\_expression\_str from false.
    - Otherwise.
      - If character belongs to tuple(“"”, “'”, “′”).
        - Set inside\_expression\_str from character.
      - Otherwise.
        - If character equals “{”.
          - Update level using + 1.
        - Otherwise.
          - If character equals “}”.
            - Update level using − 1.
            - If (level equals 0 and expression\_contents).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in level equals 0 → expression\_contents.
              - Set expression\_contents from expression\_contents at slice no value to negative 1.
              - yield values from extract\_javascript(expression\_contents, keywords, options, expression\_lineno).
              - Set expression\_contents from empty text.
              - Set inside\_expression\_str from false.
  - If character equals whitespace '\\n'.
    - Update current\_lineno using + 1.
  - Set prev\_character from character.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L2513) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L363)

## Service · Kanban board

<a id="op-1ab635aa27f856"></a>
### Extract

`operation_foundation_binding_foundation_gettext_extractors_kanban_board_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If (not isinstance(data, dict) or data.get(“doctype”) differs from “Kanban Board”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(data, dict) → data.get(“doctype”) differs from “Kanban Board”.
  - Return no value.
- If board\_name bound to data.get(“kanban\_board\_name”).
  - yield tuple(get\_line\_number(text, “kanban\_board\_name”, board\_name), “\_”, board\_name, list(formatted text Name of a Kanban board for {data.get(“reference\_doctype”)})).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1455)

## Service · Layout

<a id="op-c89734c87ffd37"></a>
### Iter zones

`operation_foundation_binding_foundation_printing_layout_iter_zones`

**Inputs** layout.

**Declared result** Iterator at tuple at tuple(str, dict).

**Local steps**

- Set header from layout.get(“header”).
- If isinstance(header, dict).
  - yield tuple(translated “Header”, header).
- For each section in (layout.get(“sections”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in layout.get(“sections”) → list().
  - If isinstance(section, dict).
    - yield tuple((section.get(“label”) or translated “Section”), section).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“label”) → translated “Section”.
- Set footer from layout.get(“footer”).
- If isinstance(footer, dict).
  - yield tuple(translated “Footer”, footer).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1686)

<a id="op-7e459da6b6da88"></a>
### Iter columns

`operation_foundation_binding_foundation_printing_layout_iter_columns`

**Inputs** zone.

**Declared result** Iterator at dict.

**Local steps**

- Set columns from zone.get(“columns”).
- For each column in columns when isinstance(columns, list), otherwise list().
  - Value choice on isinstance(columns, list) — true gives columns, false gives list().
  - If isinstance(column, dict).
    - yield column.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1682)

<a id="op-e9cb7baf198199"></a>
### Iter fields

`operation_foundation_binding_foundation_printing_layout_iter_fields`

**Inputs** zone.

**Declared result** Iterator at dict.

**Local steps**

- For each column in iter\_columns(zone).
  - Set fields from column.get(“fields”).
  - For each df in fields when isinstance(fields, list), otherwise list().
    - Value choice on isinstance(fields, list) — true gives fields, false gives list().
    - If isinstance(df, dict).
      - yield df.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1683)

<a id="op-f23fcd86144a8a"></a>
### Iter layout columns

`operation_foundation_binding_foundation_printing_layout_iter_layout_columns`

**Inputs** layout.

**Declared result** Iterator at dict.

**Local steps**

- For each tuple(\_where, zone) in iter\_zones(layout).
  - yield values from iter\_columns(zone).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1684)

<a id="op-e3c32ab9f7e24b"></a>
### Iter nodes

`operation_foundation_binding_foundation_printing_layout_iter_nodes`

**Inputs** layout.

**Declared result** Iterator at tuple at tuple(str, dict).

**Local steps**

- For each tuple(where, zone) in iter\_zones(layout).
  - yield tuple(where, zone).
  - For each df in iter\_fields(zone).
    - yield tuple(where, df).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1685)

## Record · Letter head

[Record definition](../../../../data/record-types/letter_head.json)

<a id="op-a36c798f30ce07"></a>
### Letter Head.before insert

`operation_foundation_binding_foundation_printing_doctype_letter_head_letter_head_letterhead_before_insert`

**Inputs** self.

**Local steps**

- If (not Platform.flags.in\_migrate and not Platform.flags.in\_install).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.in\_migrate → not Platform.flags.in\_install.
  - Set self.source from “Image”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L218) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1650)

<a id="op-2e09b79cf2b84c"></a>
### Letter Head.on trash

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_default.
- Evaluate clear\_default(“letter\_head”, self.name).
- Evaluate clear\_default(“default\_letter\_head\_content”, self.content).
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L42) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1726)
