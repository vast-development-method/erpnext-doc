# Workflow, automation and dispatch · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow skill

<a id="op-fe13d455162cb9"></a>
### Flow Skill.validate description

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_validate_description`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Description must be at most {0} characters.”.format(MAX\_DESCRIPTION\_LENGTH).

**Local steps**

- If len((self.description or empty text)) &gt; MAX\_DESCRIPTION\_LENGTH.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.description → empty text.
  - Call the validation error handler Platform.throw(translated “Description must be at most {0} characters.”.format(MAX\_DESCRIPTION\_LENGTH), title = translated “Description Too Long”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1115)

<a id="op-020ec0e7abf5bb"></a>
### Flow Skill.validate command

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_validate_command`

**Inputs** self, name = no value.

**Record and data access** read “Flow Skill” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A user-invocable skill needs a letter or digit in its title.” · validation helper — translated “{0} already answers to /skill:{1}. Choose a different name.”.format(other, command).

**Local steps**

- If not self.user\_invocable.
  - Return no value.
- Set command from skill\_command((name or self.name or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → self.name → empty text.
- If not command.
  - Call the validation error handler Platform.throw(translated “A user-invocable skill needs a letter or digit in its title.”, title = translated “Invalid Title”).
- For each other in Platform.get\_all(“Flow Skill”, filters = mapping(“user\_invocable” → 1, “name” → list(“!=”, (self.name or empty text))), pluck = “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
  - If skill\_command(other) equals command.
    - Call the validation error handler Platform.throw(translated “{0} already answers to /skill:{1}. Choose a different name.”.format(other, command), title = translated “Duplicate Skill Command”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1114)

<a id="op-a1cdb9bab17abc"></a>
### Flow Skill.validate global limit

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_flowskill_validate_global_limit`

**Inputs** self.

**Record and data access** read “Flow Skill” via count.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “At most {0} skills can be available to all agents.”.format(MAX\_GLOBAL\_SKILLS).

**Local steps**

- If not (self.is\_global and self.enabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_global → self.enabled.
  - Return no value.
- Set others from Platform.db.count(“Flow Skill”, mapping(“is\_global” → 1, “enabled” → 1, “name” → list(“!=”, (self.name or empty text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- If others ≥ MAX\_GLOBAL\_SKILLS.
  - Call the validation error handler Platform.throw(translated “At most {0} skills can be available to all agents.”.format(MAX\_GLOBAL\_SKILLS), title = translated “Too Many Global Skills”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1116)

<a id="op-14ef212491d690"></a>
### Expand skill command

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_expand_skill_command`

**Inputs** agent, text.

**Declared result** str.

**Record and data access** resolve a document from “Flow Agent” via get\_doc.

**Explicit results** text · whitespace '\\n\\n'.join(list(expanded blocks, instructions) when instructions, otherwise blocks).

**Explicit failure paths** validation helper — translated “No skill named {0}. Available: {1}”.format(leading.group(1), (“, ”.join(skills) or “none”)).

**Local steps**

- Set stripped from text.strip().
- Set leading from \_SKILL\_COMMAND\_RE.match(stripped).
- Set instructions from (leading.group(2) or empty text).strip() when leading, otherwise stripped.
  - Value choice on leading — true gives (leading.group(2) or empty text).strip(), false gives stripped.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in leading.group(2) → empty text.
- Set later from list of command for line drawn from instructions.split(whitespace '\\n') where not line.startswith(“&gt;”), then command drawn from \_SKILL\_TOKEN\_RE.findall(line).
  - Draw line from instructions.split(whitespace '\\n'), keep a combination only if (not line.startswith(“&gt;”)).
  - Draw command from \_SKILL\_TOKEN\_RE.findall(line).
- If (leading and leading.group(1) belongs to later).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in leading → leading.group(1) belongs to later.
  - Set instructions from stripped.
- Set commands from (list(leading.group(1)) when leading, otherwise list() + later).
  - Value choice on leading — true gives list(leading.group(1)), false gives list().
- If not commands.
  - Return text.
- Set skills from mapping().
- For each row in Platform.get\_doc(“Flow Agent”, agent).invocable\_skills().
  - Evaluate skills.setdefault(row at “command”, row).
- If (leading and leading.group(1) does not belong to skills).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in leading → leading.group(1) does not belong to skills.
  - Call the validation error handler Platform.throw(translated “No skill named {0}. Available: {1}”.format(leading.group(1), (“, ”.join(skills) or “none”)), title = translated “Unknown Skill”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “, ”.join(skills) → “none”.
- Set blocks from list of \_skill\_block(skills at command) for command drawn from dict.fromkeys(commands) where command belongs to skills.
  - Draw command from dict.fromkeys(commands), keep a combination only if (command belongs to skills).
- If not blocks.
  - Return text.
- Return whitespace '\\n\\n'.join(list(expanded blocks, instructions) when instructions, otherwise blocks).
  - Value choice on instructions — true gives list(expanded blocks, instructions), false gives blocks.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1109)

<a id="op-f68dc2736aa316"></a>
### Skill block

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_skill_block`

**Inputs** row.

**Declared result** str.

**Record and data access** read “Flow Skill” via get\_value.

**Explicit results** formatted text &lt;skill name="{row at “command”}" location="Flow Skill/{escape(row at “name”, quote = true)}"&gt; {SKILL\_LOADED\_NOTE}  {body} &lt;/skill&gt;.

**Local steps**

- Set body from (Platform.db.get\_value(“Flow Skill”, row at “name”, “instructions”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Flow Skill”, row at “name”, “instructions”) → empty text.
- Return formatted text &lt;skill name="{row at “command”}" location="Flow Skill/{escape(row at “name”, quote = true)}"&gt; {SKILL\_LOADED\_NOTE}  {body} &lt;/skill&gt;.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1118)

<a id="op-06f3b18a20d14b"></a>
### Skill command

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_skill_command`

**Inputs** name.

**Declared result** str.

**Explicit results** re.sub(“&#91;^a-z0-9&#93;+”, “-”, name.lower()).strip(“-”).

**Local steps**

- Return re.sub(“&#91;^a-z0-9&#93;+”, “-”, name.lower()).strip(“-”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1119)

<a id="op-1cf6dbb7ea9700"></a>
### Sync skills

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_sync_skills`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Flow Skill” via get\_all.

**State and service calls** request delete on “Flow Agent Skill” · request delete\_doc for “Flow Skill”.

**Explicit results** sorted(synced).

**Local steps**

- Bind dependencies MAX\_SKILL\_DIRECTORY\_ENTRIES, list\_skill\_files, load\_skill.
- Set shipped from mapping().
- Set skills\_to\_keep from set().
- For each app in Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - Set folder from Platform.get\_app\_source\_path(app, “skills”).
  - Set tuple(paths, truncated) from list\_skill\_files(folder).
  - If truncated.
    - Evaluate log\_skipped(formatted text Flow Skills of {app} skipped, translated “Skills folder {0} has more than {1} entries.”.format(folder, MAX\_SKILL\_DIRECTORY\_ENTRIES)).
    - Evaluate skills\_to\_keep.update(Platform.get\_all(“Flow Skill”, mapping(“is\_system\_generated” → 1, “app” → app), pluck = “name”)).
    - Continue with the next iteration or loop test.
  - For each path in paths.
    - Set name from formatted text {app}/{Path(path).parent.name}.
    - Evaluate skills\_to\_keep.add(name).
    - Attempt the following.
      - Set skill from load\_skill(path).
      - Within open(path, encoding = “utf-8”) bound as file.
        - Set instructions from \_FRONTMATTER\_RE.sub(empty text, file.read(), count = 1).strip().
    - On failure (ValueError) bound to e.
      - Evaluate log\_skipped(formatted text Flow Skill {name} skipped, translated “Invalid skill {0}: {1}”.format(path, str(e))).
      - Continue with the next iteration or loop test.
    - Set shipped at name from tuple(app, skill.description, instructions).
- Set synced from list().
- For each tuple(name, tuple(app, description, instructions)) in shipped.items().
  - Within skip\_if\_invalid(formatted text Flow Skill {name} skipped).
    - Evaluate \_ensure\_skill(name, app, description, instructions).
    - Evaluate synced.append(name).
- For each name in Platform.get\_all(“Flow Skill”, mapping(“is\_system\_generated” → 1), pluck = “name”).
  - If name does not belong to skills\_to\_keep.
    - Evaluate Platform.db.delete(“Flow Agent Skill”, mapping(“skill” → name)).
    - Evaluate Platform.delete\_doc(“Flow Skill”, name, ignore\_permissions = true).
- Return sorted(synced).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1121)

<a id="op-7c3e144e4edef3"></a>
### Ensure skill

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_ensure_skill`

**Inputs** name, app, description, instructions.

**Declared result** no value.

**Record and data access** read “Flow Skill” via get\_value · resolve a document from “Flow Skill” via get\_doc · resolve a document from mapping(“doctype” → “Flow Skill”, “title” → name) via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- Set definition from mapping(“app” → app, “description” → description, “instructions” → instructions, “is\_system\_generated” → 1).
- Set row from Platform.db.get\_value(“Flow Skill”, name, list(definition), as\_dict = true).
- If (row and all(generator of row at key equals value for tuple(key, value) drawn from definition.items())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → all(generator of row at key equals value for tuple(key, value) drawn from definition.items()).
  - Draw tuple(key, value) from definition.items().
  - Return no value.
- If row.
  - Set doc from Platform.get\_doc(“Flow Skill”, name).
- Otherwise.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Flow Skill”, “title” → name)).
- Evaluate doc.update(definition).
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1108)

<a id="op-40edc6b80329bc"></a>
### Skill file

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_skill_file`

**Inputs** name, file.

**Declared result** str.

**Record and data access** read “Flow Skill” via get\_value.

**Explicit results** \_list\_files(folder, path) · path.read\_text(encoding = “utf-8”).

**Explicit failure paths** validation helper — translated “Skill {0} has no files.”.format(name) · validation helper — translated “Skill {0} has no file {1}.”.format(name, file) · validation helper — translated “{0} is larger than {1} KB.”.format(file, (MAX\_SKILL\_FILE\_BYTES floor divide 1024)) · validation helper — translated “{0} is not a text file.”.format(file).

**Local steps**

- Bind dependencies valid\_skill\_name.
- Set app from Platform.db.get\_value(“Flow Skill”, name, “app”).
- Set folder\_name from name.removeprefix(formatted text {app}/).
- If (app does not belong to Platform.get\_installed\_apps() or not valid\_skill\_name(folder\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app does not belong to Platform.get\_installed\_apps() → not valid\_skill\_name(folder\_name).
  - Call the validation error handler Platform.throw(translated “Skill {0} has no files.”.format(name), title = translated “Unknown File”).
- Set folder from Path(Platform.get\_app\_source\_path(app, “skills”), folder\_name).resolve().
- Set path from (folder ÷ file).resolve().
- Set hidden from any(generator of part.startswith(“.”) for part drawn from Path(file).parts).
  - Draw part from Path(file).parts.
- If (hidden or not path.is\_relative\_to(folder) or not (path.is\_file() or path.is\_dir())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hidden → not path.is\_relative\_to(folder) → not (path.is\_file() or path.is\_dir()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path.is\_file() → path.is\_dir().
  - Call the validation error handler Platform.throw(translated “Skill {0} has no file {1}.”.format(name, file), title = translated “Unknown File”).
- If path.is\_dir().
  - Return \_list\_files(folder, path).
- If path.stat().st\_size &gt; MAX\_SKILL\_FILE\_BYTES.
  - Call the validation error handler Platform.throw(translated “{0} is larger than {1} KB.”.format(file, (MAX\_SKILL\_FILE\_BYTES floor divide 1024)), title = translated “File Too Large”).
- Attempt the following.
  - Return path.read\_text(encoding = “utf-8”).
- On failure (UnicodeDecodeError).
  - Call the validation error handler Platform.throw(translated “{0} is not a text file.”.format(file), title = translated “Not a Text File”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1120)

<a id="op-7d9dd6ad8b2bbf"></a>
### List files

`operation_foundation_binding_foundation_flow_doctype_flow_skill_flow_skill_list_files`

**Inputs** folder, path.

**Declared result** str.

**Explicit results** whitespace '\\n'.join(sorted(files)).

**Local steps**

- Set files from list().
- For each entry in path.rglob(“\*”).
  - Set relative from entry.relative\_to(folder).
  - Set hidden from any(generator of part.startswith(“.”) for part drawn from relative.parts).
    - Draw part from relative.parts.
  - If (not hidden and entry.is\_file() and entry.resolve().is\_relative\_to(folder)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not hidden → entry.is\_file() → entry.resolve().is\_relative\_to(folder).
    - Evaluate files.append(relative.as\_posix()).
- Return whitespace '\\n'.join(sorted(files)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1117)

## Record · Flow tool

<a id="op-59bb841a4d1c66"></a>
### Flow Tool.validate

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_normalize().
- Evaluate self.\_validate\_slug().
- Evaluate self.\_validate\_type\_fields().
- If self.type equals “Script”.
  - Evaluate self.\_validate\_code().
  - Evaluate self.\_warn\_if\_server\_scripts\_disabled().
- Evaluate validate\_immutable(self, tuple(“type”, “import\_path”, “description”, “requires\_confirmation”, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [normalize](operations-028.md#op-f1e7b804601b79), [validate slug](operations-028.md#op-5953b501c6d71e), [validate type fields](operations-028.md#op-b602046d7695ca), [validate code](operations-028.md#op-0abac4193a9c03), [warn if server scripts disabled](operations-028.md#op-75260de5ffea81).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1127)

<a id="op-dd73b474c109c3"></a>
### Flow Tool.on update

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_on_update`

**Inputs** self.

**Record and data access** read “Flow Agent Tool” via get\_all.

**Local steps**

- Bind dependencies warn\_existing\_sessions.
- If (self.has\_value\_changed(“enabled”) or self.has\_value\_changed(“code”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“enabled”) → self.has\_value\_changed(“code”).
  - Set agents from Platform.get\_all(“Flow Agent Tool”, filters = mapping(“tool” → self.name), pluck = “parent”).
  - Evaluate warn\_existing\_sessions(agents).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1125)

<a id="op-d44b26ebeaf1b0"></a>
### Flow Tool.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies BUILTIN\_TOOLS, builtin\_name.
- Evaluate block\_delete(self, always = self.name belongs to set of builtin\_name(tool.name) for tool drawn from BUILTIN\_TOOLS).
  - Draw tool from BUILTIN\_TOOLS.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1124)

<a id="op-3e5d627b4e456d"></a>
### Flow Tool.before rename

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_before_rename`

**Inputs** self, old, \_new, \_merge = false.

**Declared result** no value.

**Record and data access** read “Flow Agent Tool” via get\_all · read “Flow Agent Sub Agent” via get\_all.

**Local steps**

- Bind dependencies block\_rename\_in\_chats.
- Evaluate block\_rename(self, old).
- Set agents from Platform.get\_all(“Flow Agent Tool”, filters = mapping(“tool” → old), pluck = “parent”).
- If agents.
  - Update agents using + Platform.get\_all(“Flow Agent Sub Agent”, filters = mapping(“agent” → tuple(“in”, agents)), pluck = “parent”).
- Evaluate block\_rename\_in\_chats(old, agents).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1122)

<a id="op-532a563181f7bc"></a>
### Flow Tool.to tool

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_to_tool`

**Inputs** self.

**Explicit results** resolve\_tool(self).

**Local steps**

- Bind dependencies resolve\_tool.
- Return resolve\_tool(self).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1126)

<a id="op-f1e7b804601b79"></a>
### Flow Tool.normalize

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_normalize`

**Inputs** self.

**Local steps**

- For each field in tuple(“title”, “slug”, “import\_path”).
  - Set value from self.get(field).
  - If isinstance(value, str).
    - Evaluate self.set(field, value.strip()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1123)

<a id="op-5953b501c6d71e"></a>
### Flow Tool.validate slug

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_validate_slug`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Function Name must be snake\_case: start with a lowercase letter, then lowercase letters, digits or underscores.”.

**Local steps**

- Set tuple(app, \_sep, function\_name) from (self.slug or empty text).rpartition(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.slug → empty text.
- If ((app and not self.is\_system\_generated) or not SLUG\_PATTERN.match(function\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (app and not self.is\_system\_generated) → not SLUG\_PATTERN.match(function\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in app → not self.is\_system\_generated.
  - Call the validation error handler Platform.throw(translated “Function Name must be snake\_case: start with a lowercase letter, then lowercase letters, digits or underscores.”, title = translated “Invalid Function Name”).
- Evaluate self.\_validate\_reserved\_name(function\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reserved name](operations-028.md#op-169c9201bf64d8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1130)

<a id="op-169c9201bf64d8"></a>
### Flow Tool.validate reserved name

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_validate_reserved_name`

**Inputs** self, function\_name.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Function Name {0} is reserved for Flow's own tools and app tools.”.format(function\_name).

**Local steps**

- Bind dependencies BUILTIN\_TOOLS.
- If self.is\_system\_generated.
  - Return no value.
- If (“\_\_” belongs to function\_name or function\_name belongs to set of tool.name for tool drawn from BUILTIN\_TOOLS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “\_\_” belongs to function\_name → function\_name belongs to set of tool.name for tool drawn from BUILTIN\_TOOLS.
  - Draw tool from BUILTIN\_TOOLS.
  - Call the validation error handler Platform.throw(translated “Function Name {0} is reserved for Flow's own tools and app tools.”.format(function\_name), title = translated “Reserved Function Name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1129)

<a id="op-b602046d7695ca"></a>
### Flow Tool.validate type fields

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_validate_type_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Import Path is required for Imported tools.” · validation helper — translated “Import Path must be a dotted Python path (e.g. &lt;code&gt;Platform.flow.tools.builtins.search&lt;/code&gt;).” · validation helper — translated “Imported tools must not define inline code.” · validation helper — translated “Code is required for Script tools.” · validation helper — translated “Script tools must not specify an Import Path.” · 3 additional forms in the steps below.

**Local steps**

- If self.type equals “Imported”.
  - If not self.import\_path.
    - Call the validation error handler Platform.throw(translated “Import Path is required for Imported tools.”, title = translated “Missing Import Path”).
  - If not IMPORT\_PATH\_PATTERN.match(self.import\_path).
    - Call the validation error handler Platform.throw(translated “Import Path must be a dotted Python path (e.g. &lt;code&gt;Platform.flow.tools.builtins.search&lt;/code&gt;).”, title = translated “Invalid Import Path”).
  - If self.code.
    - Call the validation error handler Platform.throw(translated “Imported tools must not define inline code.”, title = translated “Unexpected Code”).
- Otherwise.
  - If self.type equals “Script”.
    - If not self.code.
      - Call the validation error handler Platform.throw(translated “Code is required for Script tools.”, title = translated “Missing Code”).
    - If self.import\_path.
      - Call the validation error handler Platform.throw(translated “Script tools must not specify an Import Path.”, title = translated “Unexpected Import Path”).
  - Otherwise.
    - If self.type equals “Server”.
      - If not self.is\_system\_generated.
        - Call the validation error handler Platform.throw(translated “Server tools come from the flow server's extensions; add an extension instead.”, title = translated “Server Tool”).
      - If (self.import\_path or self.code).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_path → self.code.
        - Call the validation error handler Platform.throw(translated “Server tools have no code here; the flow server provides them.”, title = translated “Unexpected Code”).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Type must be Imported, Script or Server.”, title = translated “Invalid Type”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1131)

<a id="op-75260de5ffea81"></a>
### Flow Tool.warn if server scripts disabled

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_warn_if_server_scripts_disabled`

**Inputs** self.

**State and service calls** msgprint with translated “Server Scripts are disabled, so this tool won't run until they are enabled.”.

**Local steps**

- Bind dependencies is\_safe\_exec\_enabled.
- If not is\_safe\_exec\_enabled().
  - Evaluate Platform.msgprint(translated “Server Scripts are disabled, so this tool won't run until they are enabled.”, title = translated “Server Scripts Disabled”, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1132)

<a id="op-0abac4193a9c03"></a>
### Flow Tool.validate code

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_flowtool_validate_code`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Code has invalid Python syntax: {0}”.format(str(e)) · validation helper — translated “Code must define a top-level &lt;code&gt;main&lt;/code&gt; function.” · validation helper — translated text in the contract · validation helper — translated “Code must not call &lt;code&gt;main()&lt;/code&gt; directly (line {0}).”.format(node.lineno).

**Local steps**

- Attempt the following.
  - Set tree from ast.parse(self.code, filename = formatted text &lt;ai\_tool:{self.slug}&gt;).
- On failure (SyntaxError) bound to e.
  - Call the validation error handler Platform.throw(translated “Code has invalid Python syntax: {0}”.format(str(e)), title = translated “Invalid Code”).
- Set main\_function from no value.
- For each node in tree.body.
  - If (isinstance(node, ast.FunctionDef) and node.name equals MAIN\_FUNCTION\_NAME).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ast.FunctionDef) → node.name equals MAIN\_FUNCTION\_NAME.
    - Set main\_function from node.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If main\_function is identical to no value.
  - Call the validation error handler Platform.throw(translated “Code must define a top-level &lt;code&gt;main&lt;/code&gt; function.”, title = translated “Missing main()”).
- Set fn\_args from main\_function.args.
- If (fn\_args.vararg is distinct from no value or fn\_args.kwarg is distinct from no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fn\_args.vararg is distinct from no value → fn\_args.kwarg is distinct from no value.
  - Call the validation error handler Platform.throw(translated text in the contract, title = translated “Invalid Signature”).
- For each node in ast.walk(tree).
  - If (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id equals MAIN\_FUNCTION\_NAME).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ast.Call) → isinstance(node.func, ast.Name) → node.func.id equals MAIN\_FUNCTION\_NAME.
    - Call the validation error handler Platform.throw(translated “Code must not call &lt;code&gt;main()&lt;/code&gt; directly (line {0}).”.format(node.lineno), title = translated “Invalid Code”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1128)

<a id="op-befbd402b93787"></a>
### Sync server tools

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_sync_server_tools`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read “Flow Tool” via get\_all · read “Flow Tool” via exists · resolve a document from mapping(“doctype” → “Flow Tool”, “slug” → name, “title” → name.replace(“\_”, one space).title(), “type” → “Server”, …) via get\_doc.

**State and service calls** request delete on “Flow Agent Tool” · request delete\_doc for “Flow Tool” · request set\_value on “Flow Tool” · call insert on Platform.get\_doc(mapping(“doctype” → “Flow Tool”, “slug” → name, “title” → name.replace(“\_”, one space).title(), “type” → “Server”, …)).

**Local steps**

- Bind dependencies lifecycle.
- Bind dependencies BUILTIN\_TOOLS.
- Set folder from lifecycle.site\_extensions\_dir().
- Set rows from lifecycle.extension\_tools(list(folder)) when folder.is\_dir(), otherwise list().
  - Value choice on folder.is\_dir() — true gives lifecycle.extension\_tools(list(folder)), false gives list().
- Set live from mapping of row at “name” → row at “description” for row drawn from rows.
  - Draw row from rows.
- Set mirrored from set(Platform.get\_all(“Flow Tool”, mapping(“type” → “Server”), pluck = “name”)).
- For each name in (mirrored − set(live)).
  - Evaluate Platform.db.delete(“Flow Agent Tool”, mapping(“tool” → name)).
  - Evaluate Platform.delete\_doc(“Flow Tool”, name, ignore\_permissions = true).
- For each tuple(name, description) in live.items().
  - If name belongs to mirrored.
    - Evaluate Platform.db.set\_value(“Flow Tool”, name, “description”, description).
  - Otherwise.
    - If not SLUG\_PATTERN.match(name).
      - Evaluate Platform.log\_error(title = formatted text Extension tool {name} is not a valid slug; skipped).
    - Otherwise.
      - If “\_\_” belongs to name.
        - Evaluate Platform.log\_error(title = formatted text Extension tool {name} has \_\_, which app tools use; skipped).
      - Otherwise.
        - If (Platform.db.exists(“Flow Tool”, name) or name belongs to set of tool.name for tool drawn from BUILTIN\_TOOLS).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“Flow Tool”, name) → name belongs to set of tool.name for tool drawn from BUILTIN\_TOOLS.
          - Draw tool from BUILTIN\_TOOLS.
          - Evaluate Platform.log\_error(title = formatted text Flow Tool {name} is not a Server tool; extension tool skipped).
        - Otherwise.
          - Evaluate Platform.get\_doc(mapping(“doctype” → “Flow Tool”, “slug” → name, “title” → nested operand in the contract(nested operand in the contract, nested operand in the contract).title(), “type” → “Server”, …)).ins ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1133)

<a id="op-5bd3afc56a6a09"></a>
### Unavailable tools

`operation_foundation_binding_foundation_flow_doctype_flow_tool_flow_tool_unavailable_tools`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Record and data access** read “Flow Tool” via get\_all · read “Flow Agent” via get\_list · read “Flow Agent Tool” via get\_all.

**Explicit results** list() · tools · Platform.get\_all(“Flow Agent Tool”, filters = mapping(“parent” → list(“in”, agents), “tool” → list(“in”, tools)), pluck = “tool”, distinct = true).

**Local steps**

- Bind dependencies EXECUTE\_SLUG, builtin\_name.
- Bind dependencies is\_safe\_exec\_enabled.
- If is\_safe\_exec\_enabled().
  - Return list().
- Set tools from list(builtin\_name(EXECUTE\_SLUG), expanded Platform.get\_all(“Flow Tool”, mapping(“type” → “Script”), pluck = “name”)).
- If Platform.has\_permission(“Flow Tool”, “read”).
  - Return tools.
- Set agents from Platform.get\_list(“Flow Agent”, pluck = “name”).
- Return Platform.get\_all(“Flow Agent Tool”, filters = mapping(“parent” → list(“in”, agents), “tool” → list(“in”, tools)), pluck = “tool”, distinct = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Tool”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1134)

## Record · Flow trigger

<a id="op-1cec15f4a10d19"></a>
### Flow Trigger.before insert

`operation_foundation_binding_foundation_flow_doctype_flow_trigger_flow_trigger_flowtrigger_before_insert`

**Inputs** self.

**Local steps**

- Evaluate block\_insert(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1135)
