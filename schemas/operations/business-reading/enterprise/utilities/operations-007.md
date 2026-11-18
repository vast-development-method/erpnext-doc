# Supporting services · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Search help

<a id="op-4f183ee9c98a81"></a>
### Get response

`operation_enterprise_templates_pages_search_help_business_behavior_get_response`

**Inputs** api, text.

**Explicit results** response.json().

**Local steps**

- Set response from requests.get(((api.base\_url + “/”) + api.query\_route), data = mapping(api.search\_term\_param\_name → text)).
- Evaluate response.raise\_for\_status().
- Return response.json().

**Values supplied outside this operation** service or queued work from requests.get(((api.base\_url + “/”) + api.query\_route), data = mapping(api.search\_term\_param\_name → text)).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L6647) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1362)

<a id="op-76f4b8e2017afc"></a>
### Get topics data

`operation_enterprise_templates_pages_search_help_business_behavior_get_topics_data`

**Inputs** api, response\_json.

**Explicit results** (topics\_data or list()).

**Local steps**

- If not response\_json.
  - Set response\_json from mapping().
- Set topics\_data from mapping().
- Set key\_list from api.response\_result\_key\_path.split(“,”).
- For each key in key\_list.
  - Set topics\_data from response\_json.get(key) when not topics\_data, otherwise topics\_data.get(key).
    - Value choice on not topics\_data — true gives response\_json.get(key), false gives topics\_data.get(key).
- Return (topics\_data or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in topics\_data → list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L6800) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1363)

<a id="op-ba8ed725635411"></a>
### Prepare api results

`operation_enterprise_templates_pages_search_help_business_behavior_prepare_application_programming_interface_results`

**Inputs** api, topics\_data.

**Explicit results** results at slice no value to 5.

**Local steps**

- If not topics\_data.
  - Set topics\_data from list().
- Set results from list().
- For each topic in topics\_data.
  - Set route from ((api.base\_url + “/”) + (api.post\_route + “/”) when api.post\_route, otherwise empty text).
    - Value choice on api.post\_route — true gives (api.post\_route + “/”), false gives empty text.
  - For each key in api.post\_route\_key\_list.split(“,”).
    - Update route using + str(topic at key).
  - Evaluate results.append(Platform.\_dict(mapping(“title” → topic at api.post\_title\_key, “preview” → html2text(topic at api.post\_description\_key), “route” → route))).
- Return results at slice no value to 5.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L7003) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1364)

<a id="op-2a13c71707c6dc"></a>
### Prepare doctype results

`operation_enterprise_templates_pages_search_help_business_behavior_prepare_record_type_results`

**Inputs** api, raw.

**Explicit results** results.

**Local steps**

- Set results from list().
- For each r in raw.
  - Set prepared\_result from mapping().
  - Set parts from r at “content”.split(“ \|\|\| ”).
  - For each part in parts.
    - Set pair from part.split(“ : ”, 1).
    - Set prepared\_result at pair at 0 from pair at 1.
  - Evaluate results.append(Platform.\_dict(mapping(“title” → prepared\_result at api.result\_title\_field, “preview” → prepared\_result at api.result\_preview\_field, “route” → prepared\_result at api.result\_route\_field))).
- Return results.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0978.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1365)

## Service · Task info

<a id="op-e6d91bfb5906ef"></a>
### Get context

`operation_enterprise_templates_pages_task_info_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Task” via get\_doc · read “Comment” via get\_all.

**Local steps**

- Set context.no\_cache from 1.
- Set task from Platform.get\_doc(“Task”, Platform.form\_dict.task).
- Evaluate task.check\_permission().
- Set context.comments from Platform.get\_all(“Comment”, filters = mapping(“reference\_doctype” → “Task”, “reference\_name” → task.name, “comment\_type” → “Comment”), fields = list(“content”, “comment\_email”, “creation”)).
- Set context.doc from task.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from task.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0978.json#L336) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1366)

## Service · Timelog info

<a id="op-e8925cd4deb186"></a>
### Get context

`operation_enterprise_templates_pages_timelog_info_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Time Log” via get\_doc.

**Local steps**

- Set context.no\_cache from 1.
- Set timelog from Platform.get\_doc(“Time Log”, Platform.form\_dict.timelog).
- Set context.doc from timelog.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0978.json#L6184) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1371)

## Service · Transaction base

<a id="op-ae976ce2e2a530"></a>
### Transaction Base.on change

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_on_change`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set is\_real\_save from (self.flags.in\_insert or tuple(self.doctype, self.name) belongs to Platform.flags.currently\_saving).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.in\_insert → tuple(self.doctype, self.name) belongs to Platform.flags.currently\_saving.
- If not is\_real\_save.
  - Return no value.
- Evaluate self.copy\_terms\_and\_conditions\_attachments().

If control reaches the end, it returns no value.

**Methods declared on this owner** [copy terms and conditions attachments](operations-007.md#op-f65cd4a37be3c1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L3102) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L111)

<a id="op-165a9b9611a098"></a>
### Transaction Base.validate posting time

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_validate_posting_time`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Invalid Posting Time”.

**Local steps**

- If ((Platform.flags.in\_import or self.flags.from\_restore) and self.posting\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (Platform.flags.in\_import or self.flags.from\_restore) → self.posting\_date.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → self.flags.from\_restore.
  - Set self.set\_posting\_time from 1.
- If not getattr(self, “set\_posting\_time”, no value).
  - Set now from now\_datetime().
  - Set self.posting\_date from now.strftime(“%Y-%m-%d”).
  - Set self.posting\_time from now.strftime(“%H:%M:%S.%f”).
- Otherwise.
  - If self.posting\_time.
    - Attempt the following.
      - Evaluate get\_time(self.posting\_time).
    - On failure (ValueError).
      - Call the validation error handler Platform.throw(translated “Invalid Posting Time”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “set\_posting\_time”, no value) · clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L3243) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L118)

<a id="op-03caf89ff649b9"></a>
### Transaction Base.validate uom is integer

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_validate_unit_of_measure_is_integer`

**Inputs** self, uom\_field, qty\_fields, child\_dt = no value.

**Local steps**

- Evaluate validate\_uom\_is\_integer(self, uom\_field, qty\_fields, child\_dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L3564) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L120)

<a id="op-d297c55d6c57f1"></a>
### Transaction Base.validate item stock uom is integer

`operation_enterprise_binding_enterprise_utilities_transaction_base_transactionbase_validate_item_stock_uom_is_integer`

**Inputs** self, item\_field, qty\_fields, child\_dt, row\_filter = no value.

**Local steps**

- Evaluate validate\_item\_stock\_uom\_is\_integer(self, item\_field, qty\_fields, child\_dt, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1343)

<a id="op-f65cd4a37be3c1"></a>
### Transaction Base.copy terms and conditions attachments

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_copy_terms_and_conditions_attachments`

**Inputs** self.

**Record and data access** read “Terms and Conditions” via get\_value · read “File” via get\_all · resolve a document from “File” via get\_doc.

**Explicit results** no value.

**Local steps**

- If (not self.name or not self.meta.has\_field(“tc\_name”) or not self.tc\_name or not self.has\_value\_changed(“tc\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.name → not self.meta.has\_field(“tc\_name”) → not self.tc\_name → not self.has\_value\_changed(“tc\_name”).
  - Return no value.
- Set copy\_attachments\_to\_transaction from Platform.db.get\_value(“Terms and Conditions”, self.tc\_name, “copy\_attachments\_to\_transaction”).
- If not cint(copy\_attachments\_to\_transaction).
  - Return no value.
- Set source\_attachments from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → “Terms and Conditions”, “attached\_to\_name” → self.tc\_name), fields = list(“name”, “file\_url”)).
- If not source\_attachments.
  - Return no value.
- Set existing\_file\_urls from set of attachment.file\_url for attachment drawn from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → self.doctype, “attached\_to\_name” → self.name), fields = list(“file\_url”)) where attac ….
  - Draw attachment from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → self.doctype, “attached\_to\_name” → self.name), fields = list(“file\_url”)), keep a combination only if (attachment.file\_url).
- For each source\_attachment in source\_attachments.
  - If (not source\_attachment.file\_url or source\_attachment.file\_url belongs to existing\_file\_urls).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not source\_attachment.file\_url → source\_attachment.file\_url belongs to existing\_file\_urls.
    - Continue with the next iteration or loop test.
  - Set new\_attachment from Platform.get\_doc(“File”, source\_attachment.name).create\_attachment\_copy(attached\_to\_doctype = self.doctype, attached\_to\_name = self.name).
  - Evaluate existing\_file\_urls.add(new\_attachment.file\_url).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L3652) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L105)

<a id="op-33e9af352644b1"></a>
### Transaction Base.validate with previous doc

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_validate_with_previous_record`

**Inputs** self, ref.

**Explicit failure paths** validation helper — translated “Duplicate row {0} with same {1}”.format(d.idx, key).

**Local steps**

- Set self.exclude\_fields from list(“conversion\_factor”, “uom”) when self.get(“is\_return”), otherwise list().
  - Value choice on self.get(“is\_return”) — true gives list(“conversion\_factor”, “uom”), false gives list().
- For each tuple(key, val) in ref.items().
  - Set is\_child from val.get(“is\_child\_table”).
  - Set ref\_doc from mapping().
  - Set item\_ref\_dn from list().
  - Set child\_rows from list().
  - For each d in self.get\_all\_children((self.doctype + “ Item”)).
    - Set ref\_dn from d.get(val at “ref\_dn\_field”).
    - If ref\_dn.
      - If is\_child.
        - Evaluate child\_rows.append(tuple(ref\_dn, d)).
        - If ref\_dn does not belong to item\_ref\_dn.
          - Evaluate item\_ref\_dn.append(ref\_dn).
        - Otherwise.
          - If not val.get(“allow\_duplicate\_prev\_row\_id”).
            - Call the validation error handler Platform.throw(translated “Duplicate row {0} with same {1}”.format(d.idx, key)).
      - Otherwise.
        - If ref\_dn.
          - Evaluate ref\_doc.setdefault(key, list()).
          - If ref\_dn does not belong to ref\_doc at key.
            - Evaluate ref\_doc at key.append(ref\_dn).
  - If child\_rows.
    - Set prev\_doc\_detail\_map from self.get\_prev\_doc\_reference\_details(item\_ref\_dn, key, val at “compare\_fields”).
    - For each tuple(ref\_dn, d) in child\_rows.
      - Evaluate self.compare\_prev\_doc\_values(prev\_doc\_detail\_map, key, ref\_dn, val at “compare\_fields”, …).
  - If ref\_doc.
    - Evaluate self.compare\_values(ref\_doc, val at “compare\_fields”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get prev doc reference details](operations-007.md#op-e1c1e661d48b2e), [compare prev doc values](operations-007.md#op-fd967f3791068e), [compare values](operations-007.md#op-0c142f3eae4be5).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L121)

<a id="op-0c142f3eae4be5"></a>
### Transaction Base.compare values

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_compare_values`

**Inputs** self, ref\_doc, fields, doc = no value.

**Local steps**

- For each tuple(reference\_doctype, ref\_dn\_list) in ref\_doc.items().
  - Set prev\_doc\_detail\_map from self.get\_prev\_doc\_reference\_details(ref\_dn\_list, reference\_doctype, fields).
  - For each reference\_name in ref\_dn\_list.
    - Evaluate self.compare\_prev\_doc\_values(prev\_doc\_detail\_map, reference\_doctype, reference\_name, fields, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get prev doc reference details](operations-007.md#op-e1c1e661d48b2e), [compare prev doc values](operations-007.md#op-fd967f3791068e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L102)

<a id="op-fd967f3791068e"></a>
### Transaction Base.compare prev doc values

`operation_enterprise_binding_enterprise_utilities_transaction_base_transactionbase_compare_prev_doc_values`

**Inputs** self, prev\_doc\_detail\_map, reference\_doctype, reference\_name, fields, doc = no value.

**Explicit failure paths** validation helper — translated “Invalid reference {0} {1}”.format(reference\_doctype, reference\_name).

**Local steps**

- Set prevdoc\_values from prev\_doc\_detail\_map.get(reference\_name).
- If not prevdoc\_values.
  - Call the validation error handler Platform.throw(translated “Invalid reference {0} {1}”.format(reference\_doctype, reference\_name)).
- For each tuple(field, condition) in fields.
  - If (prevdoc\_values at field does not belong to list(no value, empty text) and field does not belong to self.exclude\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in prevdoc\_values at field does not belong to list(no value, empty text) → field does not belong to self.exclude\_fields.
    - Evaluate self.validate\_value(field, condition, prevdoc\_values at field, doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1341)

<a id="op-e1c1e661d48b2e"></a>
### Transaction Base.get prev doc reference details

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_get_previous_record_reference_details`

**Inputs** self, reference\_names, reference\_doctype, fields.

**Record and data access** read reference\_doctype via get\_all.

**Explicit results** prev\_doc\_detail\_map.

**Local steps**

- Set prev\_doc\_detail\_map from mapping().
- Set details from Platform.get\_all(reference\_doctype, filters = mapping(“name” → tuple(“in”, reference\_names)), fields = (list(“name”) + list of d at 0 for d drawn from fields)).
  - Draw d from fields.
- For each d in details.
  - Evaluate prev\_doc\_detail\_map.setdefault(d.name, d).
- Return prev\_doc\_detail\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L5334) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L108)

<a id="op-e945dd006ceec7"></a>
### Transaction Base.validate rate with reference doc

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_validate_rate_with_reference_record`

**Inputs** self, ref\_details.

**Record and data access** read “Buying Settings” via get\_cached\_value · read “Selling Settings” via get\_cached\_value.

**State and service calls** msgprint with translated “Row #{0}: Rate must be same as {1}: {2} ({3} / {4})”.format(d.idx, ref\_dt, d.get(ref\_dn\_field), d.rate, …).

**Explicit results** no value.

**Explicit failure paths** validation helper — stop\_actions.

**Local steps**

- If self.get(“is\_internal\_supplier”).
  - Return no value.
- Set buying\_doctypes from list(“Purchase Order”, “Purchase Invoice”, “Purchase Receipt”).
- If self.doctype belongs to buying\_doctypes.
  - Set tuple(action, role\_allowed\_to\_override) from Platform.get\_cached\_value(“Buying Settings”, “Buying Settings”, list(“maintain\_same\_rate\_action”, “role\_to\_override\_stop\_action”)).
- Otherwise.
  - Set tuple(action, role\_allowed\_to\_override) from Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, list(“maintain\_same\_rate\_action”, “role\_to\_override\_stop\_action”)).
- Set stop\_actions from list().
- For each tuple(ref\_dt, ref\_dn\_field, ref\_link\_field) in ref\_details.
  - Set reference\_names from list of d.get(ref\_link\_field) for d drawn from self.get(“items”) where d.get(ref\_link\_field).
    - Draw d from self.get(“items”), keep a combination only if (d.get(ref\_link\_field)).
  - Set reference\_details from self.get\_reference\_details(reference\_names, (ref\_dt + “ Item”)).
  - For each d in self.get(“items”).
    - If d.get(ref\_link\_field).
      - Set ref\_rate from reference\_details.get(d.get(ref\_link\_field)).
      - If abs(flt((d.rate − ref\_rate), d.precision(“rate”))) ≥ 0.01.
        - If action equals “Stop”.
          - If role\_allowed\_to\_override does not belong to Platform.get\_roles().
            - Evaluate stop\_actions.append(translated “Row #{0}: Rate must be same as {1}: {2} ({3} / {4})”.format(d.idx, ref\_dt, d.get(ref\_dn\_field), d.rate, …)).
        - Otherwise.
          - Evaluate Platform.msgprint(translated “Row #{0}: Rate must be same as {1}: {2} ({3} / {4})”.format(d.idx, ref\_dt, d.get(ref\_dn\_field), d.rate, …), title = translated “Warning”, indicator = “orange”).
- If stop\_actions.
  - Call the validation error handler Platform.throw(stop\_actions, as\_list = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference details](operations-007.md#op-a0d3c07623a3e2).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Buying Settings”, “Buying Settings”, list(“maintain\_same\_rate\_action”, “role\_to\_override\_stop\_action”)), Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, list(“maintain\_same\_rate\_action”, “role\_to\_override\_stop\_action”)) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L119)

<a id="op-a0d3c07623a3e2"></a>
### Transaction Base.get reference details

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_get_reference_details`

**Inputs** self, reference\_names, reference\_doctype.

**Record and data access** read reference\_doctype via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(reference\_doctype, filters = mapping(“name” → tuple(“in”, reference\_names)), fields = list(“name”, “rate”), as\_list = 1)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(reference\_doctype, filters = mapping(“name” → tuple(“in”, reference\_names)), fields = list(“name”, “rate”), as\_list = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L6529) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L109)

<a id="op-5412d8022b9797"></a>
### Transaction Base.get link filters

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_get_link_filters`

**Inputs** self, for\_doctype.

**Explicit results** ret.

**Local steps**

- If (hasattr(self, “prev\_link\_mapper”) and self.prev\_link\_mapper.get(for\_doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “prev\_link\_mapper”) → self.prev\_link\_mapper.get(for\_doctype).
  - Set fieldname from self.prev\_link\_mapper at for\_doctype at “fieldname”.
  - Set values from filter(no value, tuple(generator of item.as\_dict() at fieldname for item drawn from self.items)).
    - Draw item from self.items.
  - If values.
    - Set ret from mapping(for\_doctype → mapping(“filters” → list(list(for\_doctype, “name”, “in”, values)))).
  - Otherwise.
    - Set ret from no value.
- Otherwise.
  - Set ret from no value.
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0991.json#L6686) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L107)

<a id="op-d6cb7d8ff4bf51"></a>
### Transaction Base.reset default field value

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_reset_default_field_value`

**Inputs** self, default\_field, child\_table, child\_table\_field.

**Local steps**

- Set child\_table\_values from set().
- For each row in self.get(child\_table).
  - If (default\_field equals “set\_warehouse” and row.get(“delivered\_by\_supplier”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_field equals “set\_warehouse” → row.get(“delivered\_by\_supplier”).
    - Continue with the next iteration or loop test.
  - Evaluate child\_table\_values.add(row.get(child\_table\_field)).
- If len(child\_table\_values) &gt; 1.
  - Evaluate self.set(default\_field, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L113)

<a id="op-4f1d0e5abf53f2"></a>
### Transaction Base.validate currency for receivable payable and advance account

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_validate_currency_for_receivable_payable_and_advance_account`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} Account: {1} ({2}) must be in either customer billing currency: {3} or Company default currency: {4}”.format(account\_type, Platform.bold(x.account), Platform.bold(receivable\_payable\_account … · validation helper — translated “Advance Account: {0} must be in either customer billing currency: {1} or Company default currency: {2}”.format(Platform.bold(x.advance\_account), Platform.bold(self.default\_currency), Platform.b … · validation helper — translated “Both {0} Account: {1} and Advance Account: {2} must be of same currency for company: {3}”.format(account\_type, Platform.bold(x.account), Platform.bold(x.advance\_account), Platform.bold(x.company)).

**Local steps**

- If self.doctype belongs to list(“Customer”, “Supplier”).
  - Set account\_type from “Receivable” when self.doctype equals “Customer”, otherwise “Payable”.
    - Value choice on self.doctype equals “Customer” — true gives “Receivable”, false gives “Payable”.
  - For each x in self.accounts.
    - Set company\_default\_currency from Platform.get\_cached\_value(“Company”, x.company, “default\_currency”).
    - Set receivable\_payable\_account\_currency from no value.
    - Set advance\_account\_currency from no value.
    - If x.account.
      - Set receivable\_payable\_account\_currency from Platform.get\_cached\_value(“Account”, x.account, “account\_currency”).
    - If x.advance\_account.
      - Set advance\_account\_currency from Platform.get\_cached\_value(“Account”, x.advance\_account, “account\_currency”).
    - If (receivable\_payable\_account\_currency and (receivable\_payable\_account\_currency differs from self.default\_currency and receivable\_payable\_account\_currency differs from company\_default\_currency)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in receivable\_payable\_account\_currency → (receivable\_payable\_account\_currency differs from self.default\_currency and receivable\_payable\_account\_currency differs from company\_default\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in receivable\_payable\_account\_currency differs from self.default\_currency → receivable\_payable\_account\_currency differs from company\_default\_currency.
      - Call the validation error handler Platform.throw(translated “{0} Account: {1} ({2}) must be in either customer billing currency: {3} or Company default currency: {4}”.format(account\_type, Platform.bold(x.account), Platform.bold(receivable\_ ….
    - If (advance\_account\_currency and (advance\_account\_currency differs from self.default\_currency and advance\_account\_currency differs from company\_default\_currency)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in advance\_account\_currency → (advance\_account\_currency differs from self.default\_currency and advance\_account\_currency differs from company\_default\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in advance\_account\_currency differs from self.default\_currency → advance\_account\_currency differs from company\_default\_currency.
      - Call the validation error handler Platform.throw(translated “Advance Account: {0} must be in either customer billing currency: {1} or Company default currency: {2}”.format(Platform.bold(x.advance\_account), Platform.bold(self.default\_curren ….
    - If (receivable\_payable\_account\_currency and advance\_account\_currency and receivable\_payable\_account\_currency differs from advance\_account\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in receivable\_payable\_account\_currency → advance\_account\_currency → receivable\_payable\_account\_currency differs from advance\_account\_currency.
      - Call the validation error handler Platform.throw(translated “Both {0} Account: {1} and Advance Account: {2} must be of same currency for company: {3}”.format(account\_type, Platform.bold(x.account), Platform.bold(x.advance\_account), Platfor ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, x.company, “default\_currency”), Platform.get\_cached\_value(“Account”, x.account, “account\_currency”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L283) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L117)

<a id="op-4587063a42a1d6"></a>
### Transaction Base.fetch item details

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_fetch_item_details`

**Inputs** self, item.

**Declared result** dict.

**Explicit results** \_get\_item\_details(Platform.\_dict(mapping(“item\_code” → item.get(“item\_code”), “barcode” → item.get(“barcode”), “serial\_no” → item.get(“serial\_no”), “batch\_no” → item.get(“batch\_no”), …)), self).

**Local steps**

- Return \_get\_item\_details(Platform.\_dict(mapping(“item\_code” → item.get(“item\_code”), “barcode” → item.get(“barcode”), “serial\_no” → item.get(“serial\_no”), “batch\_no” → item.get(“batch\_no”), …)), self).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“customer”) → self.get(“party\_name”).
  - Value choice on self.doctype belongs to list(“Purchase Invoice”, “Sales Invoice”) — true gives self.update\_stock, false gives false.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“selling\_price\_list”) → self.get(“buying\_price\_list”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“project”) → self.get(“project”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“qty”) → 1.
  - Value choice on cint(self.get(“is\_pos”)) — true gives self.get(“pos\_profile”), false gives empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L106)

<a id="op-d791151762385d"></a>
### Transaction Base.process item selection

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_process_item_selection`

**Inputs** self, item\_idx, reset\_item\_details = false, parentfield = “items”.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- Set item\_obj from self.get\_selected\_item\_row(parentfield, item\_idx).
- If (not item\_obj or not item\_obj.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_obj → not item\_obj.item\_code.
  - Return no value.
- If cint(reset\_item\_details).
  - For each fieldname in tuple(“weight\_per\_unit”, “weight\_uom”, “uom”, “conversion\_factor”, …).
    - Evaluate item\_obj.set(fieldname, no value).
  - If item\_obj.get(“mapped\_additional\_discount\_amount”).
    - Evaluate self.drop\_mapped\_discount(item\_obj).
- Set item\_details from self.fetch\_item\_details(item\_obj).
- Evaluate self.set\_fetched\_values(item\_obj, item\_details).
- If self.doctype equals “Request for Quotation”.
  - Return no value.
- Evaluate self.set\_item\_rate\_and\_discounts(item\_obj, item\_details).
- Evaluate self.add\_taxes\_from\_item\_template(item\_obj, item\_details).
- Evaluate self.add\_free\_item(item\_obj, item\_details).
- Evaluate self.handle\_internal\_parties(item\_obj, item\_details).
- Evaluate self.conversion\_factor(item\_obj, item\_details).
- Evaluate self.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get selected item row](operations-007.md#op-0c4ee80b807874), [fetch item details](operations-007.md#op-4587063a42a1d6), [set fetched values](operations-007.md#op-7f778c59803717), [set item rate and discounts](operations-008.md#op-2d4819bc1c183c), [add taxes from item template](operations-008.md#op-e75cacdf884106), [add free item](operations-008.md#op-a4ecede86beb27), [handle internal parties](operations-008.md#op-8e572e4a4bf8d6), [conversion factor](operations-008.md#op-57f699030bf3bb).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L112)

<a id="op-0c4ee80b807874"></a>
### Transaction Base.get selected item row

`operation_enterprise_binding_enterprise_utilities_transaction_base_transactionbase_get_selected_item_row`

**Inputs** self, parentfield, item\_idx.

**Explicit results** rows at 0 when rows, otherwise no value.

**Explicit failure paths** validation helper — translated “{0} is not a child table of {1}”.format(parentfield, self.doctype).

**Local steps**

- If not self.get\_table\_field\_doctype(parentfield).
  - Call the validation error handler Platform.throw(translated “{0} is not a child table of {1}”.format(parentfield, self.doctype)).
- Set rows from self.get(parentfield, mapping(“idx” → item\_idx)).
- Return rows at 0 when rows, otherwise no value.
  - Value choice on rows — true gives rows at 0, false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1342)

<a id="op-7f778c59803717"></a>
### Transaction Base.set fetched values

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_set_fetched_values`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Local steps**

- For each tuple(k, v) in item\_details.items().
  - If hasattr(item\_obj, k).
    - Evaluate setattr(item\_obj, k, v).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L3528) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L114)
