# Web content and issued documents · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Workspace

<a id="op-fa9eeccf9f1194"></a>
### Extract

`operation_foundation_gettext_extractors_workspace_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- If data.get(“doctype”) differs from “Workspace”.
  - Return no value.
- Set workspace\_name from data.get(“label”).
- yield tuple(get\_line\_number(text, “label”, workspace\_name), “\_”, workspace\_name, list(“Name of a Workspace”)).
- yield values from generator of tuple(get\_line\_number(text, “label”, chart.get(“label”)), “\_”, chart.get(“label”), list(formatted text Label of a chart in the {workspace\_name} Workspace)) for chart drawn from data.get(“chart ….
  - Draw chart from data.get(“charts”, list()), keep a combination only if (chart.get(“label”)).
- yield values from generator of tuple(get\_line\_number(text, “label”, number\_card.get(“label”)), “\_”, number\_card.get(“label”), list(formatted text Label of a number card in the {workspace\_name} Workspace)) for number\_card dr ….
  - Draw number\_card from data.get(“number\_cards”, list()), keep a combination only if (number\_card.get(“label”)).
- yield values from generator of tuple(get\_line\_number(text, “label”, link.get(“label”)), “\_”, link.get(“label”), list(formatted text Label of a {nested operand in the contract.get(“type”)} in the {workspace\_name} Workspace)) ….
  - Draw link from data.get(“links”, list()), keep a combination only if (link.get(“label”)).
- yield values from generator of tuple(get\_line\_number(text, “description”, link.get(“description”)), “\_”, link.get(“description”), list(formatted text Description of a {nested operand in the contract.get(“type”)} in the {wor ….
  - Draw link from data.get(“links”, list()), keep a combination only if (link.get(“description”)).
- yield values from generator of tuple(get\_line\_number(text, “label”, shortcut.get(“label”)), “\_”, shortcut.get(“label”), list(formatted text Label of a shortcut in the {workspace\_name} Workspace)) for shortcut drawn from dat ….
  - Draw shortcut from data.get(“shortcuts”, list()), keep a combination only if (shortcut.get(“label”)).
- yield values from generator of tuple(get\_line\_number(text, “format”, shortcut.get(“format”)), “\_”, shortcut.get(“format”), list(formatted text Count format of shortcut in the {workspace\_name} Workspace)) for shortcut drawn  ….
  - Draw shortcut from data.get(“shortcuts”, list()), keep a combination only if (shortcut.get(“format”)).
- yield values from generator of tuple(get\_line\_number(text, “label”, quick\_list.get(“label”)), “\_”, quick\_list.get(“label”), list(formatted text Label of a quick\_list in the {workspace\_name} Workspace)) for quick\_list drawn  ….
  - Draw quick\_list from data.get(“quick\_lists”, list()), keep a combination only if (quick\_list.get(“label”)).
- Set content\_json from data.get(“content”, “&#91;&#93;”).
- Set content\_lineno from get\_line\_number(text, “content”, content\_json).
- Set content from json.loads(content\_json).
- For each item in content.
  - Set item\_type from item.get(“type”).
  - If item\_type belongs to tuple(“header”, “paragraph”).
    - If text bound to item.get(“data”, mapping()).get(“text”).
      - yield tuple(content\_lineno, “\_”, text, list(formatted text {item\_type.title()} text in the {workspace\_name} Workspace)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L9) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L377)

## Service · Workspace sidebar

<a id="op-47ea13ae40a78f"></a>
### Extract

`operation_foundation_gettext_extractors_workspace_sidebar_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- Set title from data.get(“title”).
- If title.
  - yield tuple(get\_line\_number(text, “title”, title), “\_”, title, list(“Title of a Workspace Sidebar”)).
- Set items from data.get(“items”, list()).
- If isinstance(items, list).
  - For each item in items.
    - Set label from item.get(“label”).
    - If label.
      - yield tuple(get\_line\_number(text, “label”, label), “\_”, label, list(“Label of a Workspace Sidebar Item”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L10) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L378)
