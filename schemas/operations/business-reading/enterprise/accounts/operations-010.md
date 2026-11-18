# Accounting and settlement · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Address

<a id="op-c5ec0528c65bcd"></a>
### Enterprise Address.update company address

`operation_enterprise_accounts_custom_address_business_behavior_enterprise_resource_planning_next_address_update_company_address`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to link an address to a Company”.

**Local steps**

- Set company\_links from self.get\_company\_links(self).
- If not company\_links.
  - Return no value.
- If (not self.flags.ignore\_permissions and Platform.session.user differs from “Administrator” and not self.has\_permlevel\_access\_to(“is\_your\_company\_address”, permission\_type = “write”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.ignore\_permissions → Platform.session.user differs from “Administrator” → not self.has\_permlevel\_access\_to(“is\_your\_company\_address”, permission\_type = “write”).
  - Set stored\_links from set() when self.is\_new(), otherwise self.get\_company\_links(self.get\_latest()).
    - Value choice on self.is\_new() — true gives set(), false gives self.get\_company\_links(self.get\_latest()).
  - If company\_links differs from stored\_links.
    - Call the validation error handler Platform.throw(translated “You are not permitted to link an address to a Company”, Platform.PermissionError, title = translated “Not Permitted”).
- Set self.is\_your\_company\_address from 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get company links](operations-010.md#op-fb56c06a8ddb39).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L10) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L4)

<a id="op-fb56c06a8ddb39"></a>
### Enterprise Address.get company links

`operation_enterprise_binding_enterprise_accounts_custom_address_enterpriseaddress_get_company_links`

**Inputs** doc.

**Wrappers, in declaration order** staticmethod.

**Explicit results** set of link.link\_name for link drawn from (doc.get(“links”) or list()) where link.link\_doctype equals “Company”.

**Local steps**

- Return set of link.link\_name for link drawn from (doc.get(“links”) or list()) where link.link\_doctype equals “Company”.
  - Draw link from (doc.get(“links”) or list()), keep a combination only if (link.link\_doctype equals “Company”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“links”) → list().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L742)

<a id="op-a922763c417be1"></a>
### Enterprise Address.validate reference

`operation_enterprise_accounts_custom_address_business_behavior_enterprise_resource_planning_next_address_validate_reference`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Address needs to be linked to a Company. Please add a row for Company in the Links table.”.

**Local steps**

- If (self.get(“is\_your\_company\_address”) and not list of row for row drawn from self.links where row.link\_doctype equals “Company”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_your\_company\_address”) → not list of row for row drawn from self.links where row.link\_doctype equals “Company”.
  - Draw row from self.links, keep a combination only if (row.link\_doctype equals “Company”).
  - Call the validation error handler Platform.throw(translated “Address needs to be linked to a Company. Please add a row for Company in the Links table.”, title = translated “Company Not Linked”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0002.json#L5466) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L12) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L6)

<a id="op-3ac7535c85f994"></a>
### Enterprise Address.on update

`operation_enterprise_accounts_custom_address_business_behavior_enterprise_resource_planning_next_address_on_update`

**Inputs** self.

**Record and data access** read “Customer” via get\_all.

**State and service calls** request set\_value on “Customer”.

**Local steps**

- If hasattr(super(), “on\_update”).
  - Evaluate super().on\_update().
- Set address\_display from get\_address\_display(self.as\_dict()).
- Set customers from Platform.db.get\_all(“Customer”, filters = mapping(“customer\_primary\_address” → self.name), pluck = “name”).
- For each customer in customers.
  - Evaluate Platform.db.set\_value(“Customer”, customer, “primary\_address”, address\_display, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L9) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L3)

<a id="op-7c94f85338d243"></a>
### Address query

`operation_enterprise_binding_enterprise_accounts_custom_address_address_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list() · query.run().

**Explicit failure paths** validation helper — translated “Invalid company address filter”.

**Local steps**

- If doctype differs from “Address”.
  - Return list().
- Set filters from Platform.\_dict((Platform.parse\_json(filters) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(filters) → mapping().
- Set company\_address from filters.pop(“is\_your\_company\_address”, no value).
- If company\_address does not belong to tuple(no value, 0, 1, “0”, …).
  - Call the validation error handler Platform.throw(translated “Invalid company address filter”).
- Set link\_filters from mapping(“parenttype” → “Address”).
- For each fieldname in tuple(“link\_doctype”, “link\_name”).
  - If value bound to filters.pop(fieldname, no value).
    - Set link\_filters at fieldname from value.
- Set permitted\_fields from get\_permitted\_fields(“Address”).
- Set fields from list of fieldname for fieldname drawn from get\_std\_fields\_list(Platform.get\_meta(“Address”), searchfield) where fieldname belongs to permitted\_fields.
  - Draw fieldname from get\_std\_fields\_list(Platform.get\_meta(“Address”), searchfield), keep a combination only if (fieldname belongs to permitted\_fields).
- Set address from Platform.qb.DocType(“Address”).
- Set query from Platform.qb.get\_query(“Address”, fields = fields, filters = filters, or\_filters = list of list(fieldname, “like”, formatted text %{nested operand in the contract}%) for fieldname drawn from fields when txt ….
  - Value choice on txt — true gives list of list(fieldname, “like”, formatted text %{txt}%) for fieldname drawn from fields, false gives no value.
  - Draw fieldname from fields.
- If len(link\_filters) &gt; 1.
  - Set linked\_addresses from Platform.qb.get\_query(“Dynamic Link”, fields = list(“parent”), filters = link\_filters).
  - Set query from query.where(address.name.isin(linked\_addresses)).
- If company\_address is distinct from no value.
  - Set query from query.where(address.is\_your\_company\_address equals cint(company\_address)).
- Return query.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L741)

<a id="op-607b55b8dd9159"></a>
### Get shipping address

`operation_enterprise_accounts_custom_address_business_behavior_get_shipping_address`

**Inputs** company, address = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Dynamic Link” via get\_value · read “Address” via get\_all.

**Explicit results** tuple(address\_as\_dict.get(“name”), Platform.render\_template(address\_template, address\_as\_dict, restrict\_globals = true)).

**Local steps**

- Evaluate Platform.has\_permission(“Company”, ptype = “select”, doc = company, throw = true).
- Set filters from list(list(“Dynamic Link”, “link\_doctype”, “=”, “Company”), list(“Dynamic Link”, “link\_name”, “=”, company), list(“Address”, “is\_your\_company\_address”, “=”, 1)).
- Set fields from list(“\*”).
- If (address and Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → address, “link\_name” → company))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in address → Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → address, “link\_name” → company)).
  - Evaluate filters.append(list(“Address”, “name”, “=”, address)).
- If not address.
  - Evaluate filters.append(list(“Address”, “is\_shipping\_address”, “=”, 1)).
- Set address from (Platform.get\_all(“Address”, filters = filters, fields = fields) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Address”, filters = filters, fields = fields) → mapping().
- If address.
  - Set address\_as\_dict from address at 0.
  - Set tuple(name, address\_template) from get\_address\_templates(address\_as\_dict).
  - Return tuple(address\_as\_dict.get(“name”), Platform.render\_template(address\_template, address\_as\_dict, restrict\_globals = true)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, ptype = “select”, doc = company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L13) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L7)

## Record · Advance payment ledger entry

[Record definition](../../../../data/record-types/advance_payment_ledger_entry.json)

<a id="op-98c967f810e0f7"></a>
### Advance Payment Ledger Entry.on update

`operation_enterprise_accounts_record_definitions_advance_payment_ledger_entry_business_behavior_advance_payment_ledger_entry_on_update`

**Inputs** self.

**Local steps**

- If (self.against\_voucher\_type belongs to get\_advance\_payment\_doctypes() and self.flags.update\_outstanding equals “Yes” and not Platform.flags.is\_reverse\_depr\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.against\_voucher\_type belongs to get\_advance\_payment\_doctypes() → self.flags.update\_outstanding equals “Yes” → not Platform.flags.is\_reverse\_depr\_entry.
  - Evaluate update\_voucher\_outstanding(self.against\_voucher\_type, self.against\_voucher\_no, no value, no value, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L6731) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L228)

<a id="op-548a2c5648573b"></a>
### On doctype update

`operation_enterprise_accounts_record_definitions_advance_payment_ledger_entry_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Advance Payment Ledger Entry”.

**Local steps**

- Evaluate Platform.db.add\_index(“Advance Payment Ledger Entry”, list(“against\_voucher\_type”, “against\_voucher\_no”)).
- Evaluate Platform.db.add\_index(“Advance Payment Ledger Entry”, list(“voucher\_type”, “voucher\_no”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L6885) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L229)

## Report · Asset depreciation ledger

<a id="op-317ee778295fbb"></a>
### Execute

`operation_enterprise_accounts_report_asset_depreciation_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(get\_columns(), get\_data(filters)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L645)

<a id="op-c491de19cde163"></a>
### Get data

`operation_enterprise_accounts_report_asset_depreciation_ledger_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Asset” via get\_all · read “GL Entry” via get\_all.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set depreciation\_accounts from Platform.db.sql\_list(query text (SELECT, Account)).
- Set filters\_data from list(list(“company”, “=”, filters.get(“company”)), list(“posting\_date”, “&gt;=”, filters.get(“from\_date”)), list(“posting\_date”, “&lt;=”, filters.get(“to\_date”)), list(“against\_voucher\_type”, “=”, “Asset”), …).
- If filters.get(“asset”).
  - Evaluate filters\_data.append(list(“against\_voucher”, “=”, filters.get(“asset”))).
- Set asset\_filters from mapping of key → filters.get(key) for key drawn from tuple(“asset\_category”, “cost\_center”) where filters.get(key).
  - Draw key from tuple(“asset\_category”, “cost\_center”), keep a combination only if (filters.get(key)).
- If asset\_filters.
  - Set assets from Platform.get\_all(“Asset”, filters = mapping(expand asset\_filters, “docstatus” → 1), pluck = “name”).
  - Evaluate filters\_data.append(list(“against\_voucher”, “in”, assets)).
- Set or\_filters\_data from get\_finance\_book\_filters(filters).
- Set gl\_entries from Platform.get\_all(“GL Entry”, filters = filters\_data, or\_filters = or\_filters\_data, fields = list(“against\_voucher”, mapping(“SUB” → list(“debit\_in\_account\_currency”, “credit\_in\_account\_currency”), “as” → “ ….
- If not gl\_entries.
  - Return data.
- Set assets from list of d.against\_voucher for d drawn from gl\_entries.
  - Draw d from gl\_entries.
- Set assets\_details from get\_assets\_details(assets).
- Set depreciation\_before\_from\_date from get\_depreciation\_before\_from\_date(filters\_data, or\_filters\_data, filters.get(“from\_date”)).
- Set cost\_adjustments from get\_cost\_adjustments(filters, or\_filters\_data, assets\_details).
- For each d in gl\_entries.
  - Set asset\_data from assets\_details.get(d.against\_voucher).
  - If asset\_data.
    - If asset\_data.get(“accumulated\_depreciation\_amount”) is identical to no value.
      - Set asset\_data.accumulated\_depreciation\_amount from (flt(asset\_data.opening\_accumulated\_depreciation) + depreciation\_before\_from\_date.get(d.against\_voucher, 0)).
    - Update asset\_data.accumulated\_depreciation\_amount using + d.depreciation\_amount.
    - Set asset\_data.opening\_accumulated\_depreciation from (asset\_data.accumulated\_depreciation\_amount − d.depreciation\_amount).
    - Set row from Platform.\_dict(asset\_data).
    - Evaluate row.update(mapping(“depreciation\_amount” → d.depreciation\_amount, “depreciation\_date” → d.posting\_date, “value\_after\_depreciation” → ((flt(row.net\_purchase\_amount) + get\_cost\_adjustment\_till(nested operand ….
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L648)

<a id="op-199db434c19a18"></a>
### Get finance book filters

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciation_ledger_asset_depreciation_ledger_get_finance_book_filters`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** list(list(“finance\_book”, “in”, list(empty text, finance\_book)), list(“finance\_book”, “is”, “not set”)) · list(list(“finance\_book”, “in”, list(empty text)), list(“finance\_book”, “is”, “not set”)).

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Assets'”.

**Local steps**

- Set company\_fb from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_finance\_book”).
- If (filters.get(“include\_default\_book\_assets”) and company\_fb).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“include\_default\_book\_assets”) → company\_fb.
  - If (filters.get(“finance\_book”) and cstr(filters.get(“finance\_book”)) differs from cstr(company\_fb)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“finance\_book”) → cstr(filters.get(“finance\_book”)) differs from cstr(company\_fb).
    - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Assets'”).
  - Otherwise.
    - Set finance\_book from company\_fb.
- Otherwise.
  - If filters.get(“finance\_book”).
    - Set finance\_book from filters.get(“finance\_book”).
  - Otherwise.
    - Set finance\_book from no value.
- If finance\_book.
  - Return list(list(“finance\_book”, “in”, list(empty text, finance\_book)), list(“finance\_book”, “is”, “not set”)).
- Return list(list(“finance\_book”, “in”, list(empty text)), list(“finance\_book”, “is”, “not set”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_finance\_book”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1119)

<a id="op-1a534f109bb546"></a>
### Get depreciation before from date

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciation_ledger_asset_depreciation_ledger_get_depreciation_before_from_date`

**Inputs** filters\_data, or\_filters\_data, from\_date.

**Declared result** dict.

**Record and data access** read “GL Entry” via get\_all.

**Explicit results** mapping of d.against\_voucher → flt(d.depreciation\_amount) for d drawn from gl\_entries.

**Local steps**

- Set filters\_data from list of f for f drawn from filters\_data where f at 0 differs from “posting\_date”.
  - Draw f from filters\_data, keep a combination only if (f at 0 differs from “posting\_date”).
- Evaluate filters\_data.append(list(“posting\_date”, “&lt;”, from\_date)).
- Set gl\_entries from Platform.get\_all(“GL Entry”, filters = filters\_data, or\_filters = or\_filters\_data, fields = list(“against\_voucher”, mapping(“SUM” → list(mapping(“SUB” → list(“debit\_in\_account\_currency”, “credit\_in\_account ….
- Return mapping of d.against\_voucher → flt(d.depreciation\_amount) for d drawn from gl\_entries.
  - Draw d from gl\_entries.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1118)

<a id="op-964bb88b37f9bb"></a>
### Get cost adjustments

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciation_ledger_asset_depreciation_ledger_get_cost_adjustments`

**Inputs** filters, or\_filters\_data, assets\_details.

**Declared result** dict.

**Record and data access** read “Account” via get\_all.

**Explicit results** cost\_adjustments.

**Local steps**

- Set fixed\_asset\_accounts from Platform.get\_all(“Account”, filters = mapping(“account\_type” → “Fixed Asset”), pluck = “name”).
- Set common\_filters from list(list(“company”, “=”, filters.get(“company”)), list(“posting\_date”, “&lt;=”, filters.get(“to\_date”)), list(“account”, “in”, fixed\_asset\_accounts), list(“is\_cancelled”, “=”, 0)).
- Set asset\_filters from list(list(“against\_voucher\_type”, “=”, “Asset”), list(“against\_voucher”, “in”, list(assets\_details))).
- Set gl\_entries from get\_fixed\_asset\_entries((common\_filters + asset\_filters), or\_filters\_data).
- Update gl\_entries using + get\_repair\_stock\_entries(common\_filters, or\_filters\_data, list(assets\_details)).
- Set cost\_adjustments from mapping().
- For each d in gl\_entries.
  - If d.voucher\_no differs from assets\_details at d.against\_voucher.journal\_entry\_for\_scrap.
    - Evaluate cost\_adjustments.setdefault(d.against\_voucher, list()).append(d).
- Return cost\_adjustments.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1117)

<a id="op-46f5416feb4ebe"></a>
### Get repair stock entries

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciation_ledger_asset_depreciation_ledger_get_repair_stock_entries`

**Inputs** common\_filters, or\_filters\_data, assets.

**Declared result** list.

**Record and data access** read “Asset Repair” via get\_all.

**Explicit results** list() · gl\_entries.

**Local steps**

- Set repair\_assets from dict(Platform.get\_all(“Asset Repair”, filters = mapping(“asset” → list(“in”, assets), “docstatus” → 1), fields = list(“name”, “asset”), as\_list = 1)).
- If not repair\_assets.
  - Return list().
- Set repair\_filters from list(list(“voucher\_type”, “=”, “Asset Repair”), list(“voucher\_no”, “in”, list(repair\_assets)), list(“against\_voucher\_type”, “=”, “Stock Entry”)).
- Set gl\_entries from get\_fixed\_asset\_entries((common\_filters + repair\_filters), or\_filters\_data).
- For each d in gl\_entries.
  - Set d.against\_voucher from repair\_assets at d.voucher\_no.
- Return gl\_entries.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1121)

<a id="op-0e373be881bfbc"></a>
### Get fixed asset entries

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciation_ledger_asset_depreciation_ledger_get_fixed_asset_entries`

**Inputs** filters\_data, or\_filters\_data.

**Declared result** list.

**Record and data access** read “GL Entry” via get\_all.

**Explicit results** Platform.get\_all(“GL Entry”, filters = filters\_data, or\_filters = or\_filters\_data, fields = list(“against\_voucher”, “voucher\_no”, “posting\_date”, mapping(“SUB” → list(“debit\_in\_account\_currency”, “credit\_i ….

**Local steps**

- Return Platform.get\_all(“GL Entry”, filters = filters\_data, or\_filters = or\_filters\_data, fields = list(“against\_voucher”, “voucher\_no”, “posting\_date”, mapping(“SUB” → list(“debit\_in\_account\_currency”, “credit\_i ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1120)

<a id="op-ee5f4c4169e9d5"></a>
### Get cost adjustment till

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciation_ledger_asset_depreciation_ledger_get_cost_adjustment_till`

**Inputs** cost\_adjustments, date.

**Declared result** float.

**Explicit results** sum(generator of flt(d.amount) for d drawn from cost\_adjustments where d.posting\_date ≤ date).

**Local steps**

- Return sum(generator of flt(d.amount) for d drawn from cost\_adjustments where d.posting\_date ≤ date).
  - Draw d from cost\_adjustments, keep a combination only if (d.posting\_date ≤ date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1116)

<a id="op-e91674bb003058"></a>
### Get assets details

`operation_enterprise_accounts_report_asset_depreciation_ledger_business_behavior_get_assets_details`

**Inputs** assets.

**Record and data access** read “Asset” via get\_all.

**Explicit results** assets\_details.

**Local steps**

- Set assets\_details from mapping().
- Set fields from list(“name as asset”, “asset\_name”, “net\_purchase\_amount”, “opening\_accumulated\_depreciation”, …).
- For each d in Platform.get\_all(“Asset”, fields = fields, filters = mapping(“name” → tuple(“in”, assets))).
  - Evaluate assets\_details.setdefault(d.asset, d).
- Return assets\_details.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L646)

<a id="op-140dfce25edcb6"></a>
### Get columns

`operation_enterprise_accounts_report_asset_depreciation_ledger_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Asset”, “fieldname” → “asset”, “fieldtype” → “Link”, “options” → “Asset”, …), mapping(“label” → translated “Asset Name”, “fieldname” → “asset\_name”, “fieldtype” → “Data”, ….

**Local steps**

- Return list(mapping(“label” → translated “Asset”, “fieldname” → “asset”, “fieldtype” → “Link”, “options” → “Asset”, …), mapping(“label” → translated “Asset Name”, “fieldname” → “asset\_name”, “fieldtype” → “Data”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0225.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L647)

## Report · Asset depreciations and balances

<a id="op-ecdb5f2de794e0"></a>
### Execute

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters.day\_before\_from\_date from add\_days(filters.from\_date, negative 1).
- Set tuple(columns, data) from tuple(get\_columns(filters), get\_data(filters)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L649)

<a id="op-3ae5fb3fc8b891"></a>
### Get data

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_data`

**Inputs** filters.

**Explicit results** get\_group\_by\_asset\_category\_data(filters) · get\_group\_by\_asset\_data(filters).

**Local steps**

- If filters.get(“group\_by”) equals “Asset Category”.
  - Return get\_group\_by\_asset\_category\_data(filters).
- Otherwise.
  - If filters.get(“group\_by”) equals “Asset”.
    - Return get\_group\_by\_asset\_data(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0225.json#L1645) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L657)

<a id="op-a2d09ac7b60ab3"></a>
### Get group by asset category data

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_group_by_asset_category_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set asset\_categories from get\_asset\_categories\_for\_grouped\_by\_category(filters).
- Set assets from get\_assets\_for\_grouped\_by\_category(filters).
- Set asset\_value\_adjustment\_map from get\_asset\_value\_adjustment\_map\_by\_category(filters).
- For each asset\_category in asset\_categories.
  - Set row from Platform.\_dict().
  - Evaluate row.update(asset\_category).
  - Evaluate apply\_value\_adjustments(row, asset\_value\_adjustment\_map.get(asset\_category.get(“asset\_category”), mapping())).
  - Set row.value\_as\_on\_to\_date from (((((flt(nested operand in the contract.value\_as\_on\_from\_date) + flt(nested operand in the contract.value\_of\_new\_purchase)) − flt(row.value\_of\_sold\_asset)) − flt(row.value\_of\_scrapped\_asset)) − flt(row.val ….
  - Evaluate row.update(next(generator of asset for asset drawn from assets where asset at “asset\_category” equals asset\_category.get(“asset\_category”, empty text))).
    - Draw asset from assets, keep a combination only if (asset at “asset\_category” equals asset\_category.get(“asset\_category”, empty text)).
  - Set row.accumulated\_depreciation\_as\_on\_to\_date from (((flt(row.accumulated\_depreciation\_as\_on\_from\_date) + flt(row.depreciation\_amount\_during\_the\_period)) − flt(row.depreciation\_eliminated\_during\_the\_period)) − flt(row.depreciation\_eliminated\_via\_reversal)).
  - Set row.net\_asset\_value\_as\_on\_from\_date from (flt(row.value\_as\_on\_from\_date) − flt(row.accumulated\_depreciation\_as\_on\_from\_date)).
  - Set row.net\_asset\_value\_as\_on\_to\_date from (flt(row.value\_as\_on\_to\_date) − flt(row.accumulated\_depreciation\_as\_on\_to\_date)).
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L658)

<a id="op-1f16f0a52ed7e0"></a>
### Get asset categories for grouped by category

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_asset_categories_for_grouped_by_category`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set asset\_depreciation\_schedule from Platform.qb.DocType(“Asset Depreciation Schedule”).
- Set asset\_capitalization\_asset\_item from Platform.qb.DocType(“Asset Capitalization Asset Item”).
- Set asset\_capitalization from Platform.qb.DocType(“Asset Capitalization”).
- Set disposal\_in\_period from ((IfNull(asset.disposal\_date, 0) differs from 0 bitwise and asset.disposal\_date ≥ filters.from\_date) bitwise and asset.disposal\_date ≤ filters.to\_date).
- Set value\_as\_on\_from\_date from IfNull(Sum(nested operand in the contract(nested operand in the contract, nested operand in the contract).else\_(0)), 0).as\_(“value\_as\_on\_from\_date”).
- Set value\_of\_new\_purchase from IfNull(Sum(nested operand in the contract(nested operand in the contract, nested operand in the contract).else\_(0)), 0).as\_(“value\_of\_new\_purchase”).
- Set value\_of\_sold\_asset from IfNull(Sum(nested operand in the contract(nested operand in the contract, nested operand in the contract).else\_(0)), 0).as\_(“value\_of\_sold\_asset”).
- Set value\_of\_scrapped\_asset from IfNull(Sum(nested operand in the contract(nested operand in the contract, nested operand in the contract).else\_(0)), 0).as\_(“value\_of\_scrapped\_asset”).
- Set value\_of\_capitalized\_asset from IfNull(Sum(nested operand in the contract(nested operand in the contract, nested operand in the contract).else\_(0)), 0).as\_(“value\_of\_capitalized\_asset”).
- Set capitalized\_before\_from\_date from nested operand in the contract(nested operand in the contract).select(asset\_capitalization\_asset\_item.asset).where(asset\_capitalization.posting\_date &lt; filters.from\_date).where(asset\_capitalization.docstatu ….
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.purchase\_date ≤ nested operand in the contract.to\_date).where(asset.name.notin(capitalized\_before\_from\_da ….
- If filters.get(“asset\_category”).
  - Set query from query.where(asset.asset\_category equals filters.get(“asset\_category”)).
- If filters.get(“finance\_book”).
  - Set assets\_with\_finance\_book from nested operand in the contract.qb.from\_(asset\_depreciation\_schedule).select(asset\_depreciation\_schedule.asset).where(asset\_depreciation\_schedule.finance\_book equals filters.get(“finance\_book”)).
  - Set query from query.where(asset.name.isin(assets\_with\_finance\_book)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L650)

<a id="op-fb800c56c70c42"></a>
### Get assets for grouped by category

`operation_enterprise_accounts_report_asset_depreciations_and_balances_business_behavior_get_assets_for_grouped_by_category`

**Inputs** filters.

**Explicit results** list(combined.values()).

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set gl\_entry from Platform.qb.DocType(“GL Entry”).
- Set asset\_category\_account from Platform.qb.DocType(“Asset Category Account”).
- Set company from Platform.qb.DocType(“Company”).
- Set asset\_depreciation\_schedule from Platform.qb.DocType(“Asset Depreciation Schedule”).
- Set assets\_with\_finance\_book from no value.
- If filters.get(“finance\_book”).
  - Set assets\_with\_finance\_book from nested operand in the contract.qb.from\_(asset\_depreciation\_schedule).select(asset\_depreciation\_schedule.asset).where(asset\_depreciation\_schedule.finance\_book equals filters.get(“finance\_book”)).
- Set from\_gl\_entries\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_cancelled equals 0).where(gl\_entry.account equals IfNull(asset\_category\_account.depreciation\_expense\_a ….
- Set from\_opening\_depreciation\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals nested operand in the contract.company).where(asset.purchase\_date ≤ filters.to\_date).group ….
- If filters.get(“asset\_category”).
  - Set from\_gl\_entries\_query from from\_gl\_entries\_query.where(asset.asset\_category equals filters.get(“asset\_category”)).
  - Set from\_opening\_depreciation\_query from from\_opening\_depreciation\_query.where(asset.asset\_category equals filters.get(“asset\_category”)).
- Set from\_gl\_entries\_query from from\_gl\_entries\_query.where(get\_finance\_book\_condition(gl\_entry, filters)).
- If assets\_with\_finance\_book is distinct from no value.
  - Set from\_gl\_entries\_query from from\_gl\_entries\_query.where(asset.name.isin(assets\_with\_finance\_book)).
  - Set from\_opening\_depreciation\_query from from\_opening\_depreciation\_query.where(asset.name.isin(assets\_with\_finance\_book)).
- Set combined from mapping().
- For each row in from\_gl\_entries\_query.run(as\_dict = true).
  - Set combined at row.asset\_category from mapping(“asset\_category” → row.asset\_category, “accumulated\_depreciation\_as\_on\_from\_date” → flt(row.accumulated\_depreciation\_as\_on\_from\_date), “depreciation\_eliminated\_via\_reversal” → flt(row.depreciation\_ ….
- For each row in from\_opening\_depreciation\_query.run(as\_dict = true).
  - If row.asset\_category does not belong to combined.
    - Set combined at row.asset\_category from mapping(“asset\_category” → row.asset\_category, “accumulated\_depreciation\_as\_on\_from\_date” → 0.0, “depreciation\_eliminated\_via\_reversal” → 0.0, “depreciation\_eliminated\_during\_the\_period” → 0.0, …).
  - Update combined at row.asset\_category at “accumulated\_depreciation\_as\_on\_from\_date” using + flt(row.accumulated\_depreciation\_as\_on\_from\_date).
  - Update combined at row.asset\_category at “depreciation\_eliminated\_during\_the\_period” using + flt(row.depreciation\_eliminated\_during\_the\_period).
- Return list(combined.values()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L655)

<a id="op-7c7ec7115e46a7"></a>
### Get finance book condition

`operation_enterprise_binding_enterprise_accounts_report_asset_depreciations_and_balances_asset_depreciations_and_balances_get_finance_book_condition`

**Inputs** gl\_entry, filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** IfNull(gl\_entry.finance\_book, empty text).isin(list(empty text, (finance\_book or empty text))).

**Local steps**

- Set finance\_book from (filters.get(“finance\_book”) or Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“finance\_book”) → Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
- Return IfNull(gl\_entry.finance\_book, empty text).isin(list(empty text, (finance\_book or empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in finance\_book → empty text.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1124)
