# Sales · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Quotation

[Record definition](../../../../data/record-types/quotation.json)

<a id="op-97d4c3731f3b5c"></a>
### Quotation.update lead

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_update_lead`

**Inputs** self.

**Record and data access** resolve a document from “Lead” via get\_doc.

**Local steps**

- If (self.quotation\_to equals “Lead” and self.party\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.quotation\_to equals “Lead” → self.party\_name.
  - Evaluate Platform.get\_doc(“Lead”, self.party\_name).set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L972) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1273)

<a id="op-e4313b801a005c"></a>
### Quotation.set customer name

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_set_customer_name`

**Inputs** self.

**Record and data access** read “Customer” via get\_value · read “Lead” via get\_value · read “CRM Deal” via get\_value.

**Local steps**

- If (self.party\_name and self.quotation\_to equals “Customer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_name → self.quotation\_to equals “Customer”.
  - Set self.customer\_name from Platform.db.get\_value(“Customer”, self.party\_name, “customer\_name”).
- Otherwise.
  - If (self.party\_name and self.quotation\_to equals “Lead”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_name → self.quotation\_to equals “Lead”.
    - Set tuple(lead\_name, company\_name) from Platform.db.get\_value(“Lead”, self.party\_name, list(“lead\_name”, “company\_name”)).
    - Set self.customer\_name from (company\_name or lead\_name).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_name → lead\_name.
  - Otherwise.
    - If (self.party\_name and self.quotation\_to equals “Prospect”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_name → self.quotation\_to equals “Prospect”.
      - Set self.customer\_name from self.party\_name.
    - Otherwise.
      - If (self.party\_name and self.quotation\_to equals “CRM Deal”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_name → self.quotation\_to equals “CRM Deal”.
        - Set self.customer\_name from Platform.db.get\_value(“CRM Deal”, self.party\_name, “organization”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L1105) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1269)

<a id="op-1b03aa5113b087"></a>
### Quotation.update opportunity

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_update_opportunity`

**Inputs** self, status.

**Local steps**

- For each opportunity in set(generator of d.prevdoc\_docname for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
  - If opportunity.
    - Evaluate self.update\_opportunity\_status(status, opportunity).
- If self.opportunity.
  - Evaluate self.update\_opportunity\_status(status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update opportunity status](operations-012.md#op-51d00540fd91c7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L1561) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1274)

<a id="op-51d00540fd91c7"></a>
### Quotation.update opportunity status

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_update_opportunity_status`

**Inputs** self, status, opportunity = no value.

**Record and data access** resolve a document from “Opportunity” via get\_doc.

**Local steps**

- If not opportunity.
  - Set opportunity from self.opportunity.
- Set opp from Platform.get\_doc(“Opportunity”, opportunity).
- Evaluate opp.set\_status(status = status, update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L1747) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1275)

<a id="op-e64e07a5dc79af"></a>
### Quotation.declare enquiry lost

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_declare_enquiry_lost`

**Inputs** self, lost\_reasons\_list, competitors, detailed\_reason = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Quotation Lost Reason” via get\_list.

**State and service calls** call db\_set on self · call save on self.

**Explicit failure paths** validation helper — translated “Only a submitted Quotation can be set as Lost.” · validation helper — translated “Please select at least one Lost Reason” · validation helper — translated “Invalid lost reason {0}, please create a new lost reason”.format(Platform.bold(reason.get(“lost\_reason”))) · validation helper — translated “Cannot set as Lost as Sales Order is made.”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- <a id="op-e64e07a5dc79af-guard-6"></a>If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Quotation can be set as Lost.”).
- If not (self.is\_fully\_ordered() or self.is\_partially\_ordered()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_fully\_ordered() → self.is\_partially\_ordered().
  - If not lost\_reasons\_list.
    - Call the validation error handler Platform.throw(translated “Please select at least one Lost Reason”).
  - Set get\_lost\_reasons from Platform.get\_list(“Quotation Lost Reason”, fields = list(“name”)).
  - Set lost\_reasons\_lst from list of reason.get(“name”) for reason drawn from get\_lost\_reasons.
    - Draw reason from get\_lost\_reasons.
  - Evaluate self.db\_set(“status”, “Lost”).
  - If detailed\_reason.
    - Evaluate self.db\_set(“order\_lost\_reason”, detailed\_reason).
  - For each reason in lost\_reasons\_list.
    - If reason.get(“lost\_reason”) belongs to lost\_reasons\_lst.
      - Evaluate self.append(“lost\_reasons”, reason).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Invalid lost reason {0}, please create a new lost reason”.format(Platform.bold(reason.get(“lost\_reason”)))).
  - For each competitor in competitors.
    - Evaluate self.append(“competitors”, competitor).
  - Evaluate self.update\_opportunity(“Lost”).
  - Evaluate self.update\_lead().
  - Evaluate self.save().
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Cannot set as Lost as Sales Order is made.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Quotation can be set as Lost.”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e64e07a5dc79af-guard-6)

**Methods declared on this owner** [is fully ordered](operations-011.md#op-8b27b5ee925b65), [is partially ordered](operations-011.md#op-45c1cfe9052944), [update opportunity](operations-012.md#op-1b03aa5113b087), [update lead](operations-012.md#op-97d4c3731f3b5c).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1258)

<a id="op-848383f3bd0f43"></a>
### Quotation.on submit

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc.

**Local steps**

- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total, self).
- Evaluate self.update\_opportunity(“Quotation”).
- Evaluate self.update\_lead().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update opportunity](operations-012.md#op-1b03aa5113b087), [update lead](operations-012.md#op-97d4c3731f3b5c).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L2587) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1267)

<a id="op-d7dfd910daf448"></a>
### Quotation.before cancel

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_quotation_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().before\_cancel().
- Set self.lost\_reasons from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L13)

<a id="op-a5ab477b3a0511"></a>
### Quotation.on cancel

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().
- Evaluate self.set\_status(update = true).
- Evaluate self.update\_opportunity(“Open”).
- Evaluate self.update\_lead().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update opportunity](operations-012.md#op-1b03aa5113b087), [update lead](operations-012.md#op-97d4c3731f3b5c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1265)

<a id="op-f03128ccb05406"></a>
### Quotation.carry forward communication

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_carry_forward_communication`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Bind dependencies copy\_comments, link\_communications.
- If self.opportunity.
  - Set source from tuple(“Opportunity”, self.opportunity).
- Otherwise.
  - If (self.quotation\_to equals “Lead” and self.party\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.quotation\_to equals “Lead” → self.party\_name.
    - Set source from tuple(“Lead”, self.party\_name).
  - Otherwise.
    - Return no value.
- If Platform.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).
  - Evaluate copy\_comments(expanded source, self, self.flags.ignore\_permissions).
  - Evaluate link\_communications(expanded source, self, self.flags.ignore\_permissions).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1257)

<a id="op-6cf9c88170e2ca"></a>
### Quotation.print other charges

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_print_other_charges`

**Inputs** self, docname.

**Explicit results** print\_lst.

**Local steps**

- Set print\_lst from list().
- For each d in self.get(“taxes”).
  - Set lst1 from list().
  - Evaluate lst1.append(d.description).
  - Evaluate lst1.append(d.total).
  - Evaluate print\_lst.append(lst1).
- Return print\_lst.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L3079) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1268)

<a id="op-74f2a1c4efbdbb"></a>
### Quotation.on recurring

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_on_recurring`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Local steps**

- Evaluate super().on\_recurring(reference\_doc, auto\_repeat\_doc).
- Set self.valid\_till from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1266)

<a id="op-fa8957c1427295"></a>
### Quotation.get rows with alternatives

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_get_rows_with_alternatives`

**Inputs** self.

**Explicit results** rows\_with\_alternatives.

**Local steps**

- Set rows\_with\_alternatives from list().
- Set table\_length from len(self.get(“items”)).
- For each tuple(idx, row) in enumerate(self.get(“items”)).
  - If row.is\_alternative.
    - Continue with the next iteration or loop test.
  - If idx equals (table\_length − 1).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If self.get(“items”) at (idx + 1).is\_alternative.
    - Evaluate rows\_with\_alternatives.append(row.name).
- Return rows\_with\_alternatives.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L3322) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1260)

<a id="op-c26d08b2f14c95"></a>
### Get list context

`operation_enterprise_selling_record_definitions_quotation_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Quotations”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L3603) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1253)

<a id="op-6cb32f3dfb3dba"></a>
### Validate quotation expiry

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_validate_quotation_expiry`

**Inputs** source\_name.

**Record and data access** read “Quotation” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Validity period of this quotation has ended.”.

**Local steps**

- If Platform.db.get\_singles\_value(“Selling Settings”, “allow\_sales\_order\_creation\_for\_expired\_quotation”).
  - Return no value.
- Set quotation from Platform.db.get\_value(“Quotation”, source\_name, list(“transaction\_date”, “valid\_till”), as\_dict = 1).
- If (quotation and quotation.valid\_till and (quotation.valid\_till &lt; quotation.transaction\_date or quotation.valid\_till &lt; getdate(nowdate()))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in quotation → quotation.valid\_till → (quotation.valid\_till &lt; quotation.transaction\_date or quotation.valid\_till &lt; getdate(nowdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in quotation.valid\_till &lt; quotation.transaction\_date → quotation.valid\_till &lt; getdate(nowdate()).
  - Call the validation error handler Platform.throw(translated “Validity period of this quotation has ended.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L17)

<a id="op-fe6c07743b749e"></a>
### Make sales order

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_make\_sales\_order(source\_name, target\_doc, args = args).

**Local steps**

- Evaluate validate\_quotation\_expiry(source\_name).
- Return \_make\_sales\_order(source\_name, target\_doc, args = args).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L6)

<a id="op-8d5b9df1d3b860"></a>
### Make sales order

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order_6d98df05bba3`

**Inputs** source\_name, target\_doc = no value, ignore\_permissions = false, args = no value.

**Record and data access** read “Quotation” via get\_value · read “Accounts Settings” via get\_single\_value.

**Explicit results** doclist.

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set customer from \_make\_customer(source\_name, ignore\_permissions).
- Set ordered\_items from get\_ordered\_items(source\_name).
- Set mapped\_items from get\_qty\_already\_mapped(target\_doc, “quotation\_item”, “stock\_qty”).
- For each tuple(name, stock\_qty) in mapped\_items.items().
  - Set ordered\_items at name from (flt(ordered\_items.get(name)) + stock\_qty).
- Set selected\_rows from list of x.get(“name”) for x drawn from Platform.flags.get(“args”, mapping()).get(“selected\_items”, list()).
  - Draw x from Platform.flags.get(“args”, mapping()).get(“selected\_items”, list()).
- Set has\_unit\_price\_items from Platform.db.get\_value(“Quotation”, source\_name, “has\_unit\_price\_items”).
- Bind local operation is\_unit\_price\_row for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation can\_map\_row for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set automatically\_fetch\_payment\_terms from cint(Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”)).
- Set doclist from get\_mapped\_doc(“Quotation”, source\_name, mapping(“Quotation” → mapping(“doctype” → “Sales Order”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_no\_map” → list(“payment\_terms\_template”)), “Quot ….
- If automatically\_fetch\_payment\_terms.
  - Evaluate doclist.set\_payment\_schedule().
- Return doclist.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L7)

<a id="op-f1d1852406b7de"></a>
### Make sales order.is unit price row

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order_is_unit_price_row`

**Inputs** source.

**Declared result** bool.

**Explicit results** (has\_unit\_price\_items and source.qty equals 0).

**Local steps**

- Return (has\_unit\_price\_items and source.qty equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_unit\_price\_items → source.qty equals 0.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L9)

<a id="op-7c620af33fbf77"></a>
### Make sales order.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Sales Partner” via get\_value.

**Local steps**

- If customer.
  - Set target.customer from customer.name.
  - Set target.customer\_name from customer.customer\_name.
  - If not target.get(“sales\_team”).
    - For each d in (customer.get(“sales\_team”) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer.get(“sales\_team”) → list().
      - Evaluate target.append(“sales\_team”, mapping(“sales\_person” → d.sales\_person, “allocated\_percentage” → (d.allocated\_percentage or no value), “commission\_rate” → d.commission\_rate)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.allocated\_percentage → no value.
- If source.referral\_sales\_partner.
  - Set target.sales\_partner from source.referral\_sales\_partner.
  - Set target.commission\_rate from Platform.get\_value(“Sales Partner”, source.referral\_sales\_partner, “commission\_rate”).
- Set target.flags.ignore\_permissions from ignore\_permissions.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L11)

<a id="op-9d3485d099770c"></a>
### Make sales order.update item

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set balance\_stock\_qty from (obj.stock\_qty − ordered\_items.get(obj.name, 0.0)).
- Set target.stock\_qty from balance\_stock\_qty when balance\_stock\_qty &gt; 0, otherwise 0.
  - Value choice on balance\_stock\_qty &gt; 0 — true gives balance\_stock\_qty, false gives 0.
- Set target.qty from (flt(target.stock\_qty) ÷ flt(obj.conversion\_factor)).
- If obj.against\_blanket\_order.
  - Set target.against\_blanket\_order from obj.against\_blanket\_order.
  - Set target.blanket\_order from obj.blanket\_order.
  - Set target.blanket\_order\_rate from obj.blanket\_order\_rate.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L12)

<a id="op-048a0015f04aab"></a>
### Make sales order.can map row

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order_can_map_row`

**Inputs** item.

**Declared result** bool.

**Explicit results** false · not item.is\_alternative · item.name belongs to selected\_rows · true.

**Local steps**

- If not (item.stock\_qty &gt; ordered\_items.get(item.name, 0.0) or (is\_unit\_price\_row(item) and item.name does not belong to mapped\_items)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.stock\_qty &gt; ordered\_items.get(item.name, 0.0) → (is\_unit\_price\_row(item) and item.name does not belong to mapped\_items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_unit\_price\_row(item) → item.name does not belong to mapped\_items.
  - Return false.
- If not selected\_rows.
  - Return not item.is\_alternative.
- If (selected\_rows and (item.is\_alternative or item.has\_alternative\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_rows → (item.is\_alternative or item.has\_alternative\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.is\_alternative → item.has\_alternative\_item.
  - Return item.name belongs to selected\_rows.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L8)

<a id="op-9bd99d850d09eb"></a>
### Make sales order.select item

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_order_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L10)

<a id="op-7d89eb189a66b5"></a>
### Set expired status

`operation_enterprise_selling_record_definitions_quotation_business_behavior_set_expired_status`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Opportunity” via get\_doc.

**State and service calls** execute a supplied database query.

**Local steps**

- Set cond from “′tabQuotation′.docstatus = 1 and ′tabQuotation′.status NOT IN ('Expired', 'Lost') and ′tabQuotation′.valid\_t …”.
- Set so\_against\_quo from query text (SELECT, Sales).
- Set expired\_quotations from Platform.db.sql(formatted text SELECT name FROM ′tabQuotation′ WHERE {cond} and not exists({so\_against\_quo}), nowdate(), pluck = true).
- Evaluate Platform.db.multisql(mapping(“mariadb” → formatted text UPDATE ′tabQuotation′  SET ′tabQuotation′.status = 'Expired' WHERE {cond} and not exists({so\_against\_quo}), “postgres” → formatted text UPDATE ′tabQu ….
- For each opportunity in get\_opportunities\_of\_quotations(expired\_quotations).
  - Evaluate Platform.get\_doc(“Opportunity”, opportunity).set\_status(update = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1278)

<a id="op-415d51d5066cb8"></a>
### Get opportunities of quotations

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_get_opportunities_of_quotations`

**Inputs** quotations.

**Declared result** set at str.

**Record and data access** read “Quotation” via get\_all · read “Quotation Item” via get\_all.

**Explicit results** set() · set((header\_links + item\_links)).

**Local steps**

- If not quotations.
  - Return set().
- Set header\_links from Platform.get\_all(“Quotation”, mapping(“name” → tuple(“in”, quotations), “opportunity” → tuple(“is”, “set”)), pluck = “opportunity”).
- Set item\_links from Platform.get\_all(“Quotation Item”, mapping(“parent” → tuple(“in”, quotations), “prevdoc\_docname” → tuple(“is”, “set”)), pluck = “prevdoc\_docname”).
- Return set((header\_links + item\_links)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1510)

<a id="op-878b7f6f6c5d3c"></a>
### Make sales invoice

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_invoice`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Quotation” via get\_value.

**Explicit results** \_make\_sales\_invoice(source\_name, target\_doc, args = args).

**Explicit failure paths** validation helper — translated “Cannot create a Sales Invoice against Lost Quotation {0}.”.format(source\_name).

**Local steps**

- If Platform.db.get\_value(“Quotation”, source\_name, “status”) equals “Lost”.
  - Call the validation error handler Platform.throw(translated “Cannot create a Sales Invoice against Lost Quotation {0}.”.format(source\_name)).
- Evaluate validate\_quotation\_expiry(source\_name).
- Return \_make\_sales\_invoice(source\_name, target\_doc, args = args).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1514)
