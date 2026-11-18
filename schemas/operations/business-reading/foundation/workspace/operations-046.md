# Forms, reports and navigation · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Notifications

<a id="op-2073af6eedd9e5"></a>
### Get external links

`operation_foundation_desk_notifications_business_behavior_get_external_links`

**Inputs** doctype, name, links, fieldname = no value.

**Explicit results** get\_external\_links\_in\_child\_tables(doctype, name, fieldname, child\_doctypes, …) · mapping(“doctype” → doctype, “fieldname” → fieldname, “count” → total\_count, “open\_count” → open\_count).

**Local steps**

- Set fieldname from (fieldname or get\_external\_link\_fieldname(doctype, links)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname → get\_external\_link\_fieldname(doctype, links).
- Set filters from (get\_dynamic\_link\_filters(doctype, links, fieldname) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_dynamic\_link\_filters(doctype, links, fieldname) → mapping().
- If len(child\_doctypes bound to get\_child\_doctypes\_with\_field(doctype, fieldname)) &gt; 1.
  - Return get\_external\_links\_in\_child\_tables(doctype, name, fieldname, child\_doctypes, …).
- Set filters at fieldname from name.
- Set total\_count from get\_doc\_count(doctype, filters).
- Set open\_count from 0.
- If open\_count\_filters bound to get\_filters\_for(doctype).
  - Evaluate filters.update(open\_count\_filters).
  - Set open\_count from get\_doc\_count(doctype, filters).
- Return mapping(“doctype” → doctype, “fieldname” → fieldname, “count” → total\_count, “open\_count” → open\_count).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L78) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L309)

<a id="op-a2637720cab968"></a>
### Get external links in child tables

`operation_foundation_desk_notifications_business_behavior_get_external_links_in_child_tables`

**Inputs** doctype, name, fieldname, child\_doctypes, filters.

**Record and data access** read doctype via get\_list.

**Explicit results** mapping(“doctype” → doctype, “fieldname” → fieldname, “count” → “?”, “open\_count” → 0) · mapping(“doctype” → doctype, “fieldname” → fieldname, “count” → len(names), “open\_count” → open\_count, …).

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Set names from Platform.get\_list(doctype, filters = filters, or\_filters = list of list(child\_doctype, fieldname, “=”, name) for child\_doctype drawn from child\_doctypes, limit = 100, distinct = true, …).
    - Draw child\_doctype from child\_doctypes.
- On failure (Exception) bound to e.
  - If Platform.db.is\_statement\_timeout(e).
    - Return mapping(“doctype” → doctype, “fieldname” → fieldname, “count” → “?”, “open\_count” → 0).
  - Propagate the active failure.
- Set open\_count from 0.
- If (names and open\_count\_filters bound to get\_filters\_for(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in names → open\_count\_filters bound to get\_filters\_for(doctype).
  - Set open\_count from get\_doc\_count(doctype, mapping(“name” → tuple(“in”, names), expand open\_count\_filters)).
- Return mapping(“doctype” → doctype, “fieldname” → fieldname, “count” → len(names), “open\_count” → open\_count, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L79) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L310)

<a id="op-5d394ed7f31ef1"></a>
### Get doc count

`operation_foundation_desk_notifications_business_behavior_get_record_count`

**Inputs** doctype, filters.

**Declared result** (int bitwise or Literal at “?”).

**Record and data access** read doctype via get\_all.

**Explicit results** len(docs) · “?”.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Set docs from Platform.get\_all(doctype, filters = filters, limit = 100, distinct = true, ignore\_ifnull = true, …).
  - Return len(docs).
- On failure (Exception) bound to e.
  - If Platform.db.is\_statement\_timeout(e).
    - Return “?”.
  - Propagate the active failure.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L4881) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L321)

<a id="op-c069fe5efe37f6"></a>
### Get dynamic link filters

`operation_foundation_desk_notifications_business_behavior_get_dynamic_link_filters`

**Inputs** doctype, links, fieldname.

**Explicit results** no value · mapping(doctype\_fieldname → doctype\_value).

**Local steps**

- Set dynamic\_link from links.get(“dynamic\_links”, mapping()).get(fieldname).
- If not dynamic\_link.
  - Return no value.
- Set tuple(doctype\_value, doctype\_fieldname) from dynamic\_link.
- Set meta from Platform.get\_meta(doctype).
- If not meta.has\_field(doctype\_fieldname).
  - Return no value.
- Return mapping(doctype\_fieldname → doctype\_value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L5105) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L307)

<a id="op-8d68405390b155"></a>
### Notify mentions

`operation_foundation_desk_notifications_business_behavior_notify_mentions`

**Inputs** ref\_doctype, ref\_name, content, source\_doctype = no value, source\_name = no value.

**Record and data access** read “User” via get\_value.

**Explicit results** no value.

**Local steps**

- If (ref\_doctype and ref\_name and content).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doctype → ref\_name → content.
  - Set mentions from extract\_mentions(content).
  - If not mentions.
    - Return no value.
  - Set sender\_fullname from get\_fullname(Platform.session.user).
  - Set title from get\_title(ref\_doctype, ref\_name).
  - Set recipients from list of Platform.db.get\_value(“User”, mapping(“enabled” → 1, “name” → name, “user\_type” → “System User”, “allowed\_in\_mentions” → 1), “email”) for name drawn from mentions.
    - Draw name from mentions.
  - Set notification\_message from translated “{0} mentioned you in a comment in {1} {2}”.format(Platform.bold(sender\_fullname), Platform.bold(ref\_doctype), get\_title\_html(title)).
  - Set notification\_doc from mapping(“type” → “Mention”, “document\_type” → ref\_doctype, “document\_name” → ref\_name, “source\_doctype” → source\_doctype, …).
  - Evaluate enqueue\_create\_notification(recipients, notification\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L5325) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L323)

<a id="op-f0a42a498c37d2"></a>
### Extract mentions

`operation_foundation_desk_notifications_business_behavior_extract_mentions`

**Inputs** txt.

**Record and data access** resolve a document from “User Group” via get\_cached\_doc.

**Explicit results** emails.

**Local steps**

- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(txt, “html.parser”).
- Set emails from list().
- For each mention in soup.find\_all(class\_ = “mention”).
  - If mention.get(“data-is-group”) equals “true”.
    - Attempt the following.
      - Set user\_group from Platform.get\_cached\_doc(“User Group”, mention at “data-id”).
      - Update emails using + list of d.user for d drawn from user\_group.user\_group\_members.
        - Draw d from user\_group.user\_group\_members.
    - On failure (Platform.DoesNotExistError).
      - Take no action here.
    - Continue with the next iteration or loop test.
  - Set email from mention at “data-id”.
  - Evaluate emails.append(email).
- Return emails.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“User Group”, mention at “data-id”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0206.json#L5937) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L305)

## Record · Number card

[Record definition](../../../../data/record-types/number_card.json)

<a id="op-a85c91be2a268c"></a>
### Number Card.autoname

`operation_foundation_desk_record_definitions_number_card_business_behavior_number_card_autoname`

**Inputs** self.

**Record and data access** read “Number Card” via exists.

**Local steps**

- If not self.name.
  - Set self.name from self.label.
- If Platform.db.exists(“Number Card”, self.name).
  - Set self.name from append\_number\_if\_name\_exists(“Number Card”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L5562) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L973)

<a id="op-a96c2f088a521f"></a>
### Number Card.validate

`operation_foundation_desk_record_definitions_number_card_business_behavior_number_card_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Document Type and Function are required to create a number card” · validation helper — translated “Aggregate Field is required to create a number card” · validation helper — translated “Parent Document Type is required to create a number card” · validation helper — translated “Report Name, Report Field and Fucntion are required to create a number card” · validation helper — translated “Method is required to create a number card”.

**Local steps**

- If self.type equals “Document Type”.
  - If not (self.document\_type and self.function).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.document\_type → self.function.
    - Call the validation error handler Platform.throw(translated “Document Type and Function are required to create a number card”).
  - If (self.function differs from “Count” and not self.aggregate\_function\_based\_on).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.function differs from “Count” → not self.aggregate\_function\_based\_on.
    - Call the validation error handler Platform.throw(translated “Aggregate Field is required to create a number card”).
  - If (Platform.get\_meta(self.document\_type).istable and not self.parent\_document\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_meta(self.document\_type).istable → not self.parent\_document\_type.
    - Call the validation error handler Platform.throw(translated “Parent Document Type is required to create a number card”).
- Otherwise.
  - If self.type equals “Report”.
    - If not (self.report\_name and self.report\_field and self.function).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.report\_name → self.report\_field → self.function.
      - Call the validation error handler Platform.throw(translated “Report Name, Report Field and Fucntion are required to create a number card”).
  - Otherwise.
    - If self.type equals “Custom”.
      - If not self.method.
        - Call the validation error handler Platform.throw(translated “Method is required to create a number card”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L5730) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L975)

<a id="op-4dedf530172a5f"></a>
### Number Card.on update

`operation_foundation_desk_record_definitions_number_card_business_behavior_number_card_on_update`

**Inputs** self.

**Local steps**

- If (Platform.conf.developer\_mode and self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.is\_standard.
  - Evaluate export\_to\_files(record\_list = list(list(“Number Card”, self.name)), record\_module = self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L6220) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L974)

<a id="op-951ecdc6906abc"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_number_card_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0179.json#L6349) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L970)

<a id="op-59c40b470162a0"></a>
### Has permission

`operation_foundation_desk_record_definitions_number_card_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L23) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L972)

<a id="op-96aeb0634dd46b"></a>
### Get result

`operation_foundation_desk_record_definitions_number_card_business_behavior_get_result`

**Inputs** doc, filters, to\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doc.document\_type via get\_list.

**Explicit results** flt(number).

**Local steps**

- Set doc from Platform.parse\_json(doc).
- Set fields from list().
- Set sql\_function\_map from mapping(“Count” → “COUNT”, “Sum” → “SUM”, “Average” → “AVG”, “Minimum” → “MIN”, …).
- Set function from sql\_function\_map at doc.function.
- If function equals “COUNT”.
  - Set arg from “\*”.
- Otherwise.
  - Set arg from doc.aggregate\_function\_based\_on.
- Set fields from list(mapping(function → arg, “as” → “result”)).
- If not filters.
  - Set filters from list().
- Otherwise.
  - If isinstance(filters, str).
    - Set filters from Platform.parse\_json(filters).
- If to\_date.
  - Evaluate filters.append(list(doc.document\_type, “creation”, “&lt;”, to\_date)).
- Set res from Platform.get\_list(doc.document\_type, fields = fields, filters = filters, parent\_doctype = doc.parent\_document\_type, order\_by = no value).
- Set number from res at 0 at “result” when res, otherwise 0.
  - Value choice on res — true gives res at 0 at “result”, false gives 0.
- Return flt(number).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L971)

<a id="op-268a389bebfe6d"></a>
### Get percentage difference

`operation_foundation_desk_record_definitions_number_card_business_behavior_get_percentage_difference`

**Inputs** doc, filters, result.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Number Card” via get\_doc.

**Explicit results** no value · 0 · (((result ÷ previous\_result) − 1) × 100.0).

**Local steps**

- Set doc from Platform.parse\_json(doc).
- Set result from Platform.parse\_json(result).
- Set doc from Platform.get\_doc(“Number Card”, doc.name).
- If not doc.get(“show\_percentage\_stats”).
  - Return no value.
- Set previous\_result from calculate\_previous\_result(doc, filters).
- If previous\_result equals 0.
  - Return no value.
- Otherwise.
  - If result equals previous\_result.
    - Return 0.
  - Otherwise.
    - Return (((result ÷ previous\_result) − 1) × 100.0).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L698) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L969)

<a id="op-c37f26c0a5dd06"></a>
### Calculate previous result

`operation_foundation_desk_record_definitions_number_card_business_behavior_calculate_previous_result`

**Inputs** doc, filters.

**Explicit results** get\_result(doc, filters, previous\_date).

**Local steps**

- Bind dependencies add\_to\_date.
- Set current\_date from Platform.utils.now().
- If doc.stats\_time\_interval equals “Daily”.
  - Set previous\_date from add\_to\_date(current\_date, days = negative 1).
- Otherwise.
  - If doc.stats\_time\_interval equals “Weekly”.
    - Set previous\_date from add\_to\_date(current\_date, weeks = negative 1).
  - Otherwise.
    - If doc.stats\_time\_interval equals “Monthly”.
      - Set previous\_date from add\_to\_date(current\_date, months = negative 1).
    - Otherwise.
      - Set previous\_date from add\_to\_date(current\_date, years = negative 1).
- Return get\_result(doc, filters, previous\_date).

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L1120) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L965)

<a id="op-2dbd960216b065"></a>
### Create number card

`operation_foundation_desk_record_definitions_number_card_business_behavior_create_number_card`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Number Card” · call insert on doc.

**Explicit results** doc.

**Local steps**

- Set args from Platform.parse\_json(args).
- Set doc from Platform.new\_doc(“Number Card”).
- Evaluate doc.update(args).
- Evaluate doc.insert(ignore\_permissions = true).
- Return doc.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L1462) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L966)

<a id="op-daa032fbb2778d"></a>
### Get cards for user

`operation_foundation_desk_record_definitions_number_card_business_behavior_get_cards_for_user`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise or nested operand in the contract) bitwise or nested operand in the contract equals nested oper ….run().

**Local steps**

- Set doctype from “Number Card”.
- Set meta from Platform.get\_meta(doctype).
- Set searchfields from meta.get\_search\_fields().
- Set search\_conditions from list().
- Set numberCard from DocType(“Number Card”).
- If txt.
  - Set search\_conditions from list of numberCard at field.like(formatted text %{txt}%) for field drawn from searchfields.
    - Draw field from searchfields.
- Set condition\_query from Platform.qb.get\_query(doctype, filters = filters).
- Set allowed\_modules from set of module.get(“module\_name”) for module drawn from get\_modules\_from\_all\_apps\_for\_user().
  - Draw module from get\_modules\_from\_all\_apps\_for\_user().
- Return nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise or nested operand in the contract) bitwise or nested operand in the contract equals nested oper ….run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L1663) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L968)

<a id="op-fb72e108381dc5"></a>
### Create report number card

`operation_foundation_desk_record_definitions_number_card_business_behavior_create_report_number_card`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set card from create\_number\_card(args).
- Set args from Platform.parse\_json(args).
- Set args.name from card.name.
- If args.dashboard.
  - Evaluate add\_card\_to\_dashboard(Platform.as\_json(args)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L2358) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L967)

<a id="op-b5b6e6dd235ad1"></a>
### Add card to dashboard

`operation_foundation_desk_record_definitions_number_card_business_behavior_add_card_to_dashboard`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Dashboard” via get\_doc · resolve a document from “Number Card” via get\_doc.

**State and service calls** request new\_doc for “Number Card Link” · call save on card · call save on dashboard.

**Local steps**

- Set args from Platform.parse\_json(args).
- Set dashboard from Platform.get\_doc(“Dashboard”, args.dashboard).
- Set dashboard\_link from Platform.new\_doc(“Number Card Link”).
- Set dashboard\_link.card from args.name.
- If (args.set\_standard and dashboard.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.set\_standard → dashboard.is\_standard.
  - Set card from Platform.get\_doc(“Number Card”, dashboard\_link.card).
  - Set card.is\_standard from 1.
  - Set card.module from dashboard.module.
  - Evaluate card.save().
- Evaluate dashboard.append(“cards”, dashboard\_link).
- Evaluate dashboard.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L2572) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L964)

## Service · Onboarding

<a id="op-fd60d9bf11ea1b"></a>
### Get onboarding status

`operation_foundation_onboarding_business_behavior_get_onboarding_status`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.parse\_json(onboarding\_status) when onboarding\_status, otherwise mapping().

**Local steps**

- Set onboarding\_status from Platform.db.get\_value(“User”, Platform.session.user, “onboarding\_status”).
- Return Platform.parse\_json(onboarding\_status) when onboarding\_status, otherwise mapping().
  - Value choice on onboarding\_status — true gives Platform.parse\_json(onboarding\_status), false gives mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L7175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1440)

<a id="op-212420957b8933"></a>
### Update user onboarding status

`operation_foundation_onboarding_business_behavior_update_user_onboarding_status`

**Inputs** steps, appName.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_value.

**State and service calls** request set\_value on “User”.

**Local steps**

- Set steps from json.loads(steps).
- Set onboarding\_status from Platform.db.get\_value(“User”, Platform.session.user, “onboarding\_status”).
- Set onboarding\_status from Platform.parse\_json(onboarding\_status).
- Set onboarding\_status at (appName + “\_onboarding\_status”) from steps.
- Evaluate Platform.db.set\_value(“User”, Platform.session.user, “onboarding\_status”, json.dumps(onboarding\_status), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L34) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1441)

## Record · Onboarding step

[Record definition](../../../../data/record-types/onboarding_step.json)

<a id="op-6c5da22bc46a0c"></a>
### Onboarding Step.before export

`operation_foundation_desk_record_definitions_onboarding_step_business_behavior_onboarding_step_before_export`

**Inputs** self, doc.

**Local steps**

- Set doc.is\_complete from 0.
- Set doc.is\_skipped from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L5730) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L980)

<a id="op-26b4c497be2b8c"></a>
### Onboarding Step.is done

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_onboardingstep_is_done`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool((self.is\_complete or self.is\_skipped or self.is\_work\_done())).

**Local steps**

- Return bool((self.is\_complete or self.is\_skipped or self.is\_work\_done())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_complete → self.is\_skipped → self.is\_work\_done().

**Methods declared on this owner** [is work done](operations-046.md#op-70469febe62770).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L729)

<a id="op-70469febe62770"></a>
### Onboarding Step.is work done

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_onboardingstep_is_work_done`

**Inputs** self.

**Declared result** (bool bitwise or no value).

**Record and data access** read “DocType” via exists · read doctype via get\_all · read doctype via get\_single\_value.

**Explicit results** self.is\_onboarding\_done() · no value · bool(Platform.get\_all(doctype, filters = filters, limit = 1, pluck = “name”)) · bool(value) · cstr(value) equals cstr(self.value\_to\_validate).

**Local steps**

- If self.action equals “Complete Onboarding”.
  - Return self.is\_onboarding\_done().
- Set doctype from self.reference\_document.
- If (not doctype or not Platform.db.exists(“DocType”, doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not Platform.db.exists(“DocType”, doctype).
  - Return no value.
- If doctype equals “User”.
  - Return no value.
- Set meta from Platform.get\_meta(doctype).
- If (self.action equals “Create Entry” and not meta.issingle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.action equals “Create Entry” → not meta.issingle.
  - Set filters from self.get\_record\_filters(meta).
  - If meta.is\_submittable.
    - Set filters at “docstatus” from 1.
  - Return bool(Platform.get\_all(doctype, filters = filters, limit = 1, pluck = “name”)).
- If (self.action equals “Update Settings” and self.validate\_action and self.field and meta.issingle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.action equals “Update Settings” → self.validate\_action → self.field → meta.issingle.
  - Set value from Platform.db.get\_single\_value(doctype, self.field).
  - If self.value\_to\_validate equals “%”.
    - Return bool(value).
  - Return cstr(value) equals cstr(self.value\_to\_validate).
- Return no value.

**Methods declared on this owner** [is onboarding done](operations-046.md#op-5e747c4fe132aa), [get record filters](operations-047.md#op-a21a37b0881cda).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(doctype, self.field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L731)

<a id="op-5e747c4fe132aa"></a>
### Onboarding Step.is onboarding done

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_onboardingstep_is_onboarding_done`

**Inputs** self.

**Declared result** (bool bitwise or no value).

**Record and data access** read “Module Onboarding” via exists · resolve a document from “Module Onboarding” via get\_doc · resolve a document from “Onboarding Step” via get\_doc.

**Explicit results** no value · true · false.

**Local steps**

- If (not self.module\_onboarding or not Platform.db.exists(“Module Onboarding”, self.module\_onboarding)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.module\_onboarding → not Platform.db.exists(“Module Onboarding”, self.module\_onboarding).
  - Return no value.
- Set onboarding from Platform.get\_doc(“Module Onboarding”, self.module\_onboarding).
- If onboarding.is\_complete.
  - Return true.
- For each row in onboarding.steps.
  - If row.is\_optional.
    - Continue with the next iteration or loop test.
  - Set step from Platform.get\_doc(“Onboarding Step”, row.step).
  - If step.action equals “Complete Onboarding”.
    - Set done from (step.is\_complete or step.is\_skipped).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.is\_complete → step.is\_skipped.
  - Otherwise.
    - Set done from step.is\_done().
  - If not done.
    - Return false.
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L730)
