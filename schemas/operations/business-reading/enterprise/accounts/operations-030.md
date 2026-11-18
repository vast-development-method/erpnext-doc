# Accounting and settlement · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Consolidated trial balance

<a id="op-216a3e87d6e665"></a>
### Consolidate gle data

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_consolidate_general_ledger_entry_data`

**Inputs** data, entry, tb\_data.

**State and service calls** call insert on data.

**Local steps**

- Set entry\_gle\_exists from false.
- For each gle in data.
  - If (gle and gle at “account\_name” equals entry at “account\_name”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in gle → gle at “account\_name” equals entry at “account\_name”.
    - Set entry\_gle\_exists from true.
    - Update gle at “closing\_credit” using + entry at “closing\_credit”.
    - Update gle at “closing\_debit” using + entry at “closing\_debit”.
    - Update gle at “credit” using + entry at “credit”.
    - Update gle at “debit” using + entry at “debit”.
    - Update gle at “opening\_credit” using + entry at “opening\_credit”.
    - Update gle at “opening\_debit” using + entry at “opening\_debit”.
    - Set gle at “has\_value” from 1.
- If not entry\_gle\_exists.
  - Set entry\_parent\_account from next(generator of d for d drawn from tb\_data where d.get(“account”) equals entry.get(“parent\_account”), no value).
    - Draw d from tb\_data, keep a combination only if (d.get(“account”) equals entry.get(“parent\_account”)).
  - Set parent\_account\_in\_data from no value.
  - If entry\_parent\_account.
    - Set parent\_account\_in\_data from next(generator of d for d drawn from data where (d and d.get(“account\_name”) equals entry\_parent\_account.get(“account\_name”)), no value).
      - Draw d from data, keep a combination only if ((d and d.get(“account\_name”) equals entry\_parent\_account.get(“account\_name”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d → d.get(“account\_name”) equals entry\_parent\_account.get(“account\_name”).
  - If parent\_account\_in\_data.
    - Set entry at “parent\_account” from parent\_account\_in\_data.get(“account”).
    - Set entry at “indent” from ((parent\_account\_in\_data.get(“indent”) or 0) + 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_account\_in\_data.get(“indent”) → 0.
    - Evaluate data.insert((data.index(parent\_account\_in\_data) + 1), entry).
  - Otherwise.
    - Set entry at “parent\_account” from no value.
    - Set entry at “indent” from 0.
    - Evaluate data.append(entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L695) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L795)

<a id="op-5a18760928455e"></a>
### Update to presentation currency

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_update_to_presentation_currency`

**Inputs** data, from\_currency, to\_currency, date, ignore\_reporting\_currency.

**Explicit results** no value.

**Local steps**

- If from\_currency equals to\_currency.
  - Return no value.
- Set exchange\_rate from get\_rate\_as\_at(date, from\_currency, to\_currency).
- For each d in data.
  - If not ignore\_reporting\_currency.
    - For each field in value\_fields.
      - If d.get(field).
        - Set d at field from (d at field × flt(exchange\_rate)).
  - Evaluate d.update(currency = to\_currency).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L1530) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L806)

<a id="op-c7d61bbd59bb82"></a>
### Prepare opening closing for ctb

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_prepare_opening_closing_for_ctb`

**Inputs** data.

**Local steps**

- For each d in data.
  - Evaluate prepare\_opening\_closing(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L1798) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L804)

<a id="op-7bed60ff6169c1"></a>
### Get columns

`operation_enterprise_accounts_report_consolidated_trial_balance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “account\_name”, “label” → translated “Account”, “fieldtype” → “Data”, “width” → 300), mapping(“fieldname” → “acc\_name”, “label” → translated “Account Name”, “fieldtype” → “Data”, ….

**Local steps**

- Return list(mapping(“fieldname” → “account\_name”, “label” → translated “Account”, “fieldtype” → “Data”, “width” → 300), mapping(“fieldname” → “acc\_name”, “label” → translated “Account Name”, “fieldtype” → “Data”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L1865) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L798)

## Record · Cost center

[Record definition](../../../../data/record-types/cost_center.json)

<a id="op-3c574850a84faa"></a>
### Cost Center.autoname

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_autoname`

**Inputs** self.

**Local steps**

- Bind dependencies get\_autoname\_with\_number.
- Set self.name from get\_autoname\_with\_number(self.cost\_center\_number, self.cost\_center\_name, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L5676) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L677)

<a id="op-1aaba2fa4342b3"></a>
### Cost Center.validate

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_changes().
- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_parent\_cost\_center().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate changes](operations-030.md#op-73c81bba4b1d03), [validate mandatory](operations-030.md#op-4e7b0490400fa4), [validate parent cost center](operations-030.md#op-25f5661318efbd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L685)

<a id="op-73c81bba4b1d03"></a>
### Cost Center.validate changes

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_cost_center_costcenter_validate_changes`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Company cannot be changed for an existing Cost Center”.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return no value.
- If self.company differs from previous.company.
  - Call the validation error handler Platform.throw(translated “Company cannot be changed for an existing Cost Center”).
- If cint(self.is\_group) differs from cint(previous.is\_group).
  - If cint(self.is\_group).
    - Evaluate self.validate\_ledger\_to\_group().
  - Otherwise.
    - Evaluate self.validate\_group\_to\_ledger().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate ledger to group](operations-030.md#op-90a91fcb908195), [validate group to ledger](operations-030.md#op-9d84504aa16ec5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L779)

<a id="op-4e7b0490400fa4"></a>
### Cost Center.validate mandatory

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_validate_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please enter parent cost center” · validation helper — translated “Root cannot have a parent cost center”.

**Local steps**

- If (self.cost\_center\_name differs from self.company and not self.parent\_cost\_center).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.cost\_center\_name differs from self.company → not self.parent\_cost\_center.
  - Call the validation error handler Platform.throw(translated “Please enter parent cost center”).
- Otherwise.
  - If (self.cost\_center\_name equals self.company and self.parent\_cost\_center).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.cost\_center\_name equals self.company → self.parent\_cost\_center.
    - Call the validation error handler Platform.throw(translated “Root cannot have a parent cost center”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L5839) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L686)

<a id="op-25f5661318efbd"></a>
### Cost Center.validate parent cost center

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_validate_parent_cost_center`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_value.

**Explicit failure paths** validation helper — translated “{0} is not a group node. Please select a group node as parent cost center”.format(Platform.bold(self.parent\_cost\_center)) · validation helper — translated “Parent Cost Center must belong to the same Company”.

**Local steps**

- If self.parent\_cost\_center.
  - Set parent from Platform.db.get\_value(“Cost Center”, self.parent\_cost\_center, list(“is\_group”, “company”), as\_dict = true).
  - If (not parent or not parent.is\_group).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → not parent.is\_group.
    - Call the validation error handler Platform.throw(translated “{0} is not a group node. Please select a group node as parent cost center”.format(Platform.bold(self.parent\_cost\_center))).
  - If parent.company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Parent Cost Center must belong to the same Company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L687)

<a id="op-29f6755f9e7ef7"></a>
### Cost Center.convert group to ledger

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_convert_group_to_ledger`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** 1.

**Local steps**

- Set self.is\_group from 0.
- Evaluate self.save().
- Return 1.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L682)

<a id="op-d6602e2f89b170"></a>
### Cost Center.convert ledger to group

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_convert_ledger_to_group`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** 1.

**Local steps**

- Set self.is\_group from 1.
- Evaluate self.save().
- Return 1.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L683)

<a id="op-9d84504aa16ec5"></a>
### Cost Center.validate group to ledger

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_cost_center_costcenter_validate_group_to_ledger`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot convert Cost Center to ledger as it has child nodes” · validation helper — translated “Cost Center with existing transactions can not be converted to ledger”.

**Local steps**

- If self.check\_if\_child\_exists().
  - Call the validation error handler Platform.throw(translated “Cannot convert Cost Center to ledger as it has child nodes”).
- Otherwise.
  - If self.check\_gle\_exists().
    - Call the validation error handler Platform.throw(translated “Cost Center with existing transactions can not be converted to ledger”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if child exists](operations-030.md#op-cd0fbc7db2f6c1), [check gle exists](operations-030.md#op-e69c715861a669).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L780)

<a id="op-90a91fcb908195"></a>
### Cost Center.validate ledger to group

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_cost_center_costcenter_validate_ledger_to_group`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cost Center with Allocation records can not be converted to a group” · validation helper — translated “Cost Center is a part of Cost Center Allocation, hence cannot be converted to a group” · validation helper — translated “Cost Center with existing transactions can not be converted to group”.

**Local steps**

- If self.if\_allocation\_exists\_against\_cost\_center().
  - Call the validation error handler Platform.throw(translated “Cost Center with Allocation records can not be converted to a group”).
- If self.check\_if\_part\_of\_cost\_center\_allocation().
  - Call the validation error handler Platform.throw(translated “Cost Center is a part of Cost Center Allocation, hence cannot be converted to a group”).
- If self.check\_gle\_exists().
  - Call the validation error handler Platform.throw(translated “Cost Center with existing transactions can not be converted to group”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [if allocation exists against cost center](operations-030.md#op-794512cd7b8460), [check if part of cost center allocation](operations-030.md#op-0b0c1dabf6be7d), [check gle exists](operations-030.md#op-e69c715861a669).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L781)

<a id="op-e69c715861a669"></a>
### Cost Center.check gle exists

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_check_general_ledger_entry_exists`

**Inputs** self.

**Record and data access** read “GL Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“GL Entry”, mapping(“cost\_center” → self.name)).

**Local steps**

- Return Platform.db.get\_value(“GL Entry”, mapping(“cost\_center” → self.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L6708) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L679)

<a id="op-cd0fbc7db2f6c1"></a>
### Cost Center.check if child exists

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_check_if_child_exists`

**Inputs** self.

**Record and data access** execute query text (SELECT, Cost Center).

**Explicit results** Platform.db.sql(query text (SELECT, Cost Center), self.name).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Cost Center), self.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L680)

<a id="op-794512cd7b8460"></a>
### Cost Center.if allocation exists against cost center

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_if_allocation_exists_against_cost_center`

**Inputs** self.

**Record and data access** read “Cost Center Allocation” via get\_value.

**Explicit results** Platform.db.get\_value(“Cost Center Allocation”, filters = mapping(“main\_cost\_center” → self.name, “docstatus” → 1)).

**Local steps**

- Return Platform.db.get\_value(“Cost Center Allocation”, filters = mapping(“main\_cost\_center” → self.name, “docstatus” → 1)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L684)

<a id="op-0b0c1dabf6be7d"></a>
### Cost Center.check if part of cost center allocation

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_check_if_part_of_cost_center_allocation`

**Inputs** self.

**Record and data access** read “Cost Center Allocation Percentage” via get\_value.

**Explicit results** Platform.db.get\_value(“Cost Center Allocation Percentage”, filters = mapping(“cost\_center” → self.name, “docstatus” → 1)).

**Local steps**

- Return Platform.db.get\_value(“Cost Center Allocation Percentage”, filters = mapping(“cost\_center” → self.name, “docstatus” → 1)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L681)

<a id="op-f6125c3f8b4d09"></a>
### Cost Center.before rename

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_before_rename`

**Inputs** self, olddn, newdn, merge = false.

**Explicit results** new\_cost\_center.

**Local steps**

- Bind dependencies get\_name\_with\_abbr.
- Set new\_cost\_center from get\_name\_with\_abbr(newdn, self.company).
- Evaluate super().before\_rename(olddn, new\_cost\_center, merge, “is\_group”).
- If not merge.
  - Set new\_cost\_center from get\_name\_with\_number(new\_cost\_center, self.cost\_center\_number).
- Return new\_cost\_center.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L230) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L678)

<a id="op-5cddcfd097c501"></a>
### Cost Center.after rename

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_cost_center_after_rename`

**Inputs** self, olddn, newdn, merge = false.

**Record and data access** read “Cost Center” via get\_value.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate super().after\_rename(olddn, newdn, merge).
- If not merge.
  - Set new\_cost\_center from Platform.db.get\_value(“Cost Center”, newdn, list(“cost\_center\_name”, “cost\_center\_number”), as\_dict = 1).
  - Set cost\_center\_name from newdn.rsplit(“ - ”, 1) at 0.
  - If new\_cost\_center.cost\_center\_number.
    - Set cost\_center\_name from cost\_center\_name.removeprefix(formatted text {new\_cost\_center.cost\_center\_number} - ).
  - If new\_cost\_center.cost\_center\_name differs from cost\_center\_name.
    - Set self.cost\_center\_name from cost\_center\_name.
    - Evaluate self.db\_set(“cost\_center\_name”, cost\_center\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L676)

<a id="op-d2d228ebcee67a"></a>
### On doctype update

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Cost Center”.

**Local steps**

- Evaluate Platform.db.add\_index(“Cost Center”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L1055) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L689)

<a id="op-fa262383d453de"></a>
### Get name with number

`operation_enterprise_accounts_record_definitions_cost_center_business_behavior_get_name_with_number`

**Inputs** new\_account, account\_number.

**Explicit results** new\_account.

**Local steps**

- If (account\_number and not new\_account.startswith(formatted text {account\_number} - )).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_number → not new\_account.startswith(formatted text {account\_number} - ).
  - Set new\_account from ((account\_number + “ - ”) + new\_account).
- Return new\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L688)

<a id="op-47a5bd33d6bef8"></a>
### Get data

`operation_enterprise_accounts_record_definitions_cost_center_cost_center_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “cost\_center”, “reports” → list(mapping(“label” → translated “Reports”, “items” → list(“Budget Variance Report”, “General Ledger”)))).

**Local steps**

- Return mapping(“fieldname” → “cost\_center”, “reports” → list(mapping(“label” → translated “Reports”, “items” → list(“Budget Variance Report”, “General Ledger”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L1249) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L690)

## Record · Cost center allocation

[Record definition](../../../../data/record-types/cost_center_allocation.json)

<a id="op-9580828a4076e9"></a>
### Cost Center Allocation.initialize

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.\_skip\_from\_date\_validation from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L1946) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L659)

<a id="op-559399b6ce76f7"></a>
### Cost Center Allocation.validate

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_allocation\_percentages().
- Evaluate self.validate\_total\_allocation\_percentage().
- If not self.\_skip\_from\_date\_validation.
  - Evaluate self.validate\_from\_date\_based\_on\_existing\_gle().
- Evaluate self.validate\_duplicate\_allocation().
- Evaluate self.validate\_backdated\_allocation().
- Evaluate self.validate\_cost\_centers().
- Evaluate self.validate\_main\_cost\_center().
- Evaluate self.validate\_child\_cost\_centers().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate allocation percentages](operations-031.md#op-151812f9f8186d), [validate total allocation percentage](operations-031.md#op-6b306b8c3b5ad4), [validate from date based on existing gle](operations-031.md#op-0ee6acbe7eaf7b), [validate duplicate allocation](operations-031.md#op-a30550b4546b8e), [validate backdated allocation](operations-031.md#op-fec4878cb13383), [validate cost centers](operations-031.md#op-1023e96a6c6466), [validate main cost center](operations-031.md#op-64a79979795cca), [validate child cost centers](operations-031.md#op-40aa36228726fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L660)
