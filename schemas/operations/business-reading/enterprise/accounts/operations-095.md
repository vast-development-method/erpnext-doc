# Accounting and settlement · operations 95

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase invoice

[Record definition](../../../../data/record-types/purchase_invoice.json)

<a id="op-2eb11a2ac5948c"></a>
### Purchase Invoice.unblock invoice

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_unblock_invoice`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.db\_set(mapping(“on\_hold” → 0, “release\_date” → no value)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L5258) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L939)

<a id="op-26084e5aaf5b98"></a>
### Purchase Invoice.change release date

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_change_release_date`

**Inputs** self, release\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Invoice is not blocked. Block the invoice to change the release date.”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- If not self.on\_hold.
  - Call the validation error handler Platform.throw(translated “Invoice is not blocked. Block the invoice to change the release date.”).
- Set self.release\_date from release\_date.
- Evaluate self.validate\_block\_invoice().
- Evaluate self.db\_set(“release\_date”, release\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate block invoice](operations-095.md#op-b0f7bbaaf8ebee).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L5407) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L918)

<a id="op-b0f7bbaaf8ebee"></a>
### Purchase Invoice.validate block invoice

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_block_invoice`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Purchase Invoice without any outstanding amount cannot be held.”.

**Local steps**

- Evaluate self.validate\_invoice\_hold().
- <a id="op-b0f7bbaaf8ebee-guard-3"></a>If self.outstanding\_amount ≤ 0.
  - Call the validation error handler Platform.throw(translated “Purchase Invoice without any outstanding amount cannot be held.”).
- Evaluate self.validate\_release\_date().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.outstanding\_amount ≤ 0, self.outstanding\_amount = 0 selects the branch that calls the validation-error handler with translated “Purchase Invoice without any outstanding amount cannot be held.”. With self.outstanding\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b0f7bbaaf8ebee-guard-3)

**Methods declared on this owner** [validate invoice hold](operations-092.md#op-d26e935504da6d), [validate release date](operations-092.md#op-fe315f014fa5f4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L5650) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L772) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L944)

<a id="op-89809126a1dff5"></a>
### Purchase Invoice.set status

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_set_status`

**Inputs** self, update = false, status = no value, update\_modified = true.

**Record and data access** read “Purchase Invoice” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - If self.get(“amended\_from”).
    - Set self.status from “Draft”.
  - Return no value.
- Set outstanding\_amount from flt(self.outstanding\_amount, self.precision(“outstanding\_amount”)).
- Set total from get\_total\_in\_party\_account\_currency(self).
- If not status.
  - If self.docstatus equals 2.
    - Set status from “Cancelled”.
  - Otherwise.
    - If self.docstatus equals 1.
      - If self.is\_internal\_transfer().
        - Set self.status from “Internal Transfer”.
      - Otherwise.
        - If is\_overdue(self, total).
          - Set self.status from “Overdue”.
        - Otherwise.
          - If 0 &lt; outstanding\_amount &lt; total.
            - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; outstanding\_amount &lt; total.
            - Set self.status from “Partly Paid”.
          - Otherwise.
            - If (outstanding\_amount &gt; 0 and getdate(self.due\_date) ≥ getdate()).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in outstanding\_amount &gt; 0 → getdate(self.due\_date) ≥ getdate().
              - Set self.status from “Unpaid”.
            - Otherwise.
              - If (self.is\_return equals 0 and Platform.db.get\_value(“Purchase Invoice”, mapping(“is\_return” → 1, “return\_against” → self.name, “docstatus” → 1))).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return equals 0 → Platform.db.get\_value(“Purchase Invoice”, mapping(“is\_return” → 1, “return\_against” → self.name, “docstatus” → 1)).
                - Set self.status from “Debit Note Issued”.
              - Otherwise.
                - If self.is\_return equals 1.
                  - Set self.status from “Return”.
                - Otherwise.
                  - <a id="op-89809126a1dff5-guard-29"></a>If outstanding\_amount ≤ 0.
                    - Set self.status from “Paid”.
                  - Otherwise.
                    - Set self.status from “Submitted”.
    - Otherwise.
      - Set self.status from “Draft”.
- If update.
  - Evaluate self.db\_set(“status”, self.status, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison outstanding\_amount ≤ 0, outstanding\_amount = 0 selects the branch that assigns “Paid” to self.status. With outstanding\_amount = 1, the alternative assigns “Submitted” to self.status. [Local guard](#op-89809126a1dff5-guard-29)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L5786) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L938)

<a id="op-30ec28d0d0a733"></a>
### Get purchase document details

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_get_purchase_document_details`

**Inputs** doc.

**Record and data access** read parent\_doctype via get\_all · read child\_doctype via get\_all.

**Explicit results** tuple(exchange\_rate\_map, net\_rate\_map).

**Local steps**

- If doc.doctype equals “Purchase Invoice”.
  - Set doc\_reference from “purchase\_receipt”.
  - Set items\_reference from “pr\_detail”.
  - Set parent\_doctype from “Purchase Receipt”.
  - Set child\_doctype from “Purchase Receipt Item”.
- Otherwise.
  - Set doc\_reference from “purchase\_invoice”.
  - Set items\_reference from “purchase\_invoice\_item”.
  - Set parent\_doctype from “Purchase Invoice”.
  - Set child\_doctype from “Purchase Invoice Item”.
- Set purchase\_receipts\_or\_invoices from list().
- Set items from list().
- For each item in doc.get(“items”).
  - If item.get(doc\_reference).
    - Evaluate purchase\_receipts\_or\_invoices.append(item.get(doc\_reference)).
  - If item.get(items\_reference).
    - Evaluate items.append(item.get(items\_reference)).
- Set exchange\_rate\_map from Platform.\_dict(Platform.get\_all(parent\_doctype, filters = mapping(“name” → tuple(“in”, purchase\_receipts\_or\_invoices)), fields = list(“name”, “conversion\_rate”), as\_list = 1)).
- Set net\_rate\_map from Platform.\_dict(Platform.get\_all(child\_doctype, filters = mapping(“name” → tuple(“in”, items)), fields = list(“name”, “net\_rate”), as\_list = 1)).
- Return tuple(exchange\_rate\_map, net\_rate\_map).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0148.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L913)

<a id="op-55c4a086fa0842"></a>
### Get list context

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Purchase Invoices”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0148.json#L657) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L912)

<a id="op-f959bd1428dc60"></a>
### Make regional gl entries

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_make_regional_general_ledger_entries`

**Inputs** gl\_entries, doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** gl\_entries.

**Local steps**

- Return gl\_entries.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0148.json#L837) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L914)

<a id="op-a5b05e0890dcb1"></a>
### Make debit note

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_debit_note`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Purchase Invoice”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Purchase Invoice”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L938)

<a id="op-3765b3cd0ec748"></a>
### Make stock entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_stock_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Set doc from get\_mapped\_doc(“Purchase Invoice”, source\_name, mapping(“Purchase Invoice” → mapping(“doctype” → “Stock Entry”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Purchase Invoice Item” → mapping(“docty ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L947)

<a id="op-330c0d4a1b0f41"></a>
### Make inter company sales invoice

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_inter_company_sales_invoice`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_inter\_company\_transaction(“Purchase Invoice”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_inter\_company\_transaction.
- Return make\_inter\_company\_transaction(“Purchase Invoice”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L939)

<a id="op-53bfeb469c080d"></a>
### Make purchase receipt

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set mapped\_qty\_by\_item from get\_qty\_already\_mapped(target\_doc, “purchase\_invoice\_item”).
- Bind local operation received\_and\_mapped\_qty for subsequent calls.
- Bind local operation post\_parent\_process for subsequent calls.
- Bind local operation remove\_items\_with\_zero\_qty for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doc from get\_mapped\_doc(“Purchase Invoice”, source\_name, mapping(“Purchase Invoice” → mapping(“doctype” → “Purchase Receipt”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Purchase Invoice Item” → mapping(“ ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → args.get(“merge\_taxes”).
  - Value choice on args — true gives args.get(“merge\_taxes”), false gives 0.
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L940)

<a id="op-d8e057462f5dda"></a>
### Make purchase receipt.received and mapped qty

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt_received_and_mapped_qty`

**Inputs** obj.

**Explicit results** (flt(obj.received\_qty) + flt(mapped\_qty\_by\_item.get(obj.name, 0))).

**Local steps**

- Return (flt(obj.received\_qty) + flt(mapped\_qty\_by\_item.get(obj.name, 0))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L942)

<a id="op-3d9fa57a0ebfd6"></a>
### Make purchase receipt.post parent process

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt_post_parent_process`

**Inputs** source\_parent, target\_parent.

**Local steps**

- Evaluate remove\_items\_with\_zero\_qty(target\_parent).
- Evaluate set\_missing\_values(source\_parent, target\_parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L941)

<a id="op-2c0c6d3e183aa1"></a>
### Make purchase receipt.remove items with zero qty

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt_remove_items_with_zero_qty`

**Inputs** target\_parent.

**Local steps**

- Set target\_parent.items from list of row for row drawn from target\_parent.get(“items”) where row.get(“qty”) differs from 0.
  - Draw row from target\_parent.get(“items”), keep a combination only if (row.get(“qty”) differs from 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L943)

<a id="op-87e9bd993cd743"></a>
### Make purchase receipt.set missing values

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt_set_missing_values`

**Inputs** source\_parent, target\_parent.

**Local steps**

- Evaluate target\_parent.run\_method(“set\_missing\_values”).
- If (args and args.get(“merge\_taxes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → args.get(“merge\_taxes”).
  - Evaluate merge\_taxes(source\_parent, target\_parent).
- Evaluate target\_parent.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target\_parent.run\_method(“set\_missing\_values”), target\_parent.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L945)

<a id="op-709bb068b5c8d7"></a>
### Make purchase receipt.update item

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Bind dependencies get\_returned\_qty\_map\_for\_row.
- Set returned\_qty\_map from (get\_returned\_qty\_map\_for\_row(source\_parent.name, source\_parent.supplier, obj.name, “Purchase Invoice”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_returned\_qty\_map\_for\_row(source\_parent.name, source\_parent.supplier, obj.name, “Purchase Invoice”) → mapping().
- Set pending\_qty from (flt(obj.qty) − received\_and\_mapped\_qty(obj)).
- Set target.qty from (pending\_qty − flt(returned\_qty\_map.get(“qty”))).
- Set target.received\_qty from pending\_qty.
- Set target.stock\_qty from ((pending\_qty − flt(returned\_qty\_map.get(“qty”))) × flt(obj.conversion\_factor)).
- Set target.amount from (pending\_qty × flt(obj.rate)).
- Set target.base\_amount from ((pending\_qty × flt(obj.rate)) × flt(source\_parent.conversion\_rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L946)

<a id="op-4d58b3cb1e6657"></a>
### Make purchase receipt.select item

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_make_purchase_receipt_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L944)

<a id="op-f064fc8e329ad4"></a>
### Get data

`operation_enterprise_accounts_record_definitions_purchase_invoice_purchase_invoice_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “purchase\_invoice”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Request” → “reference\_name”, “Landed Cost Vouc ….

**Local steps**

- Return mapping(“fieldname” → “purchase\_invoice”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Request” → “reference\_name”, “Landed Cost Vouc ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0148.json#L890) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L958)

## Report · Purchase invoice trends

<a id="op-696587f75f448f"></a>
### Execute

`operation_enterprise_accounts_report_purchase_invoice_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Purchase Invoice”).
- Set data from get\_data(filters, conditions).
- Return tuple(conditions at “columns”, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0271.json#L5189) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1193)

## Report · Purchase register

<a id="op-714d45bae1901c"></a>
### Execute

`operation_enterprise_accounts_report_purchase_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** \_execute(filters).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return \_execute(filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1203)

<a id="op-578cb8b29161d7"></a>
### Execute

`operation_enterprise_accounts_report_purchase_register_business_behavior_execute_2`

**Inputs** filters = no value, additional\_table\_columns = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, invoice\_list) · tuple(columns, res, no value, no value, …).

**Explicit failure paths** validation helper — translated “Please select a supplier for fetching payments.”.

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set include\_payments from filters.get(“include\_payments”).
- If (filters.get(“include\_payments”) and not filters.get(“supplier”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“include\_payments”) → not filters.get(“supplier”).
  - Call the validation error handler Platform.throw(translated “Please select a supplier for fetching payments.”).
- Set invoice\_list from get\_invoices(filters, get\_query\_columns(additional\_table\_columns)).
- If filters.get(“include\_payments”).
  - Update invoice\_list using + get\_payments(filters).
- Set tuple(columns, expense\_accounts, tax\_accounts, unrealized\_profit\_loss\_accounts) from get\_columns(invoice\_list, additional\_table\_columns, include\_payments).
- If not invoice\_list.
  - Evaluate msgprint(translated “No record found”).
  - Return tuple(columns, invoice\_list).
- Set invoice\_expense\_map from get\_invoice\_expense\_map(invoice\_list).
- Set internal\_invoice\_map from get\_internal\_invoice\_map(invoice\_list).
- Set tuple(invoice\_expense\_map, invoice\_tax\_map) from get\_invoice\_tax\_map(invoice\_list, invoice\_expense\_map, expense\_accounts, include\_payments).
- Set invoice\_po\_pr\_map from get\_invoice\_po\_pr\_map(invoice\_list).
- Set suppliers from list(set(generator of d.supplier for d drawn from invoice\_list)).
  - Draw d from invoice\_list.
- Set supplier\_details from get\_party\_details(“Supplier”, suppliers).
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set res from list().
- If include\_payments.
  - Set opening\_row from get\_opening\_row(“Supplier”, filters.supplier, getdate(filters.from\_date), filters.company) at 0.
  - Evaluate res.append(mapping(“payable\_account” → opening\_row.account, “debit” → flt(opening\_row.debit), “credit” → flt(opening\_row.credit), “balance” → flt(opening\_row.balance))).
- Set data from list().
- For each inv in invoice\_list.
  - Set purchase\_order from list(set(invoice\_po\_pr\_map.get(inv.name, mapping()).get(“purchase\_order”, list()))).
  - Set purchase\_receipt from list(set(invoice\_po\_pr\_map.get(inv.name, mapping()).get(“purchase\_receipt”, list()))).
  - Set project from list(set(invoice\_po\_pr\_map.get(inv.name, mapping()).get(“project”, list()))).
  - Set row from mapping(“voucher\_type” → inv.doctype, “voucher\_no” → inv.name, “posting\_date” → inv.posting\_date, “supplier\_id” → inv.supplier, …).
    - Value choice on inv.doctype equals “Purchase Invoice” — true gives “, ”.join(project), false gives inv.project.
  - Set base\_net\_total from 0.
  - For each expense\_acc in expense\_accounts.
    - If is\_internal\_transfer(inv).
      - Set expense\_amount from 0.
    - Otherwise.
      - Set expense\_amount from flt(invoice\_expense\_map.get(inv.name, mapping()).get(expense\_acc)).
    - Update base\_net\_total using + expense\_amount.
    - Evaluate row.update(mapping(Platform.scrub(expense\_acc) → expense\_amount)).
  - For each account in unrealized\_profit\_loss\_accounts.
    - Evaluate row.update(mapping(Platform.scrub((account + “\_unrealized”)) → flt(internal\_invoice\_map.get(tuple(inv.name, account))))).
  - Evaluate row.update(mapping(“net\_total” → (base\_net\_total or inv.base\_net\_total))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in base\_net\_total → inv.base\_net\_total.
  - Set total\_tax from 0.
  - For each tax\_acc in tax\_accounts.
    - If tax\_acc does not belong to expense\_accounts.
      - Set tax\_amount from flt(invoice\_tax\_map.get(inv.name, mapping()).get(tax\_acc)).
      - Update total\_tax using + tax\_amount.
      - Evaluate row.update(mapping(Platform.scrub(tax\_acc) → tax\_amount)).
  - Set outstanding\_precision from (get\_field\_precision(Platform.get\_meta(“Purchase Invoice”).get\_field(“outstanding\_amount”), currency = company\_currency) or 2).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_field\_precision(Platform.get\_meta(“Purchase Invoice”).get\_field(“outstanding\_amount”), currency = company\_currency) → 2.
  - Evaluate row.update(mapping(“total\_tax” → total\_tax, “grand\_total” → inv.base\_grand\_total, “rounded\_total” → inv.base\_rounded\_total)).
  - If inv.doctype equals “Purchase Invoice”.
    - Evaluate row.update(mapping(“debit” → get\_in\_invoice\_payable\_debit(inv), “credit” → get\_payable\_credit(inv), “outstanding\_amount” → flt(get\_outstanding\_in\_company\_currency(inv, company\_currency), outstanding\_precision))).
  - Otherwise.
    - Evaluate row.update(mapping(“debit” → inv.debit, “credit” → inv.credit)).
  - Evaluate data.append(row).
- Update res using + sorted(data, key = deferred anonymous expression).
- If include\_payments.
  - Set running\_balance from flt(opening\_row.balance).
  - For each row in range(1, len(res)).
    - Update running\_balance using + (res at row at “debit” − res at row at “credit”).
    - Evaluate res at row.update(mapping(“balance” → running\_balance)).
- Return tuple(columns, res, no value, no value, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1204)

<a id="op-71b1d25ede470c"></a>
### Get outstanding in company currency

`operation_enterprise_binding_enterprise_accounts_report_purchase_register_purchase_register_get_outstanding_in_company_currency`

**Inputs** inv, company\_currency.

**Explicit results** flt(inv.outstanding\_amount) · (flt(inv.outstanding\_amount) × (inv.conversion\_rate or 1)).

**Local steps**

- If inv.party\_account\_currency equals company\_currency.
  - Return flt(inv.outstanding\_amount).
- Return (flt(inv.outstanding\_amount) × (inv.conversion\_rate or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv.conversion\_rate → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1254)

<a id="op-47ce409273a433"></a>
### Get payable credit

`operation_enterprise_binding_enterprise_accounts_report_purchase_register_purchase_register_get_payable_credit`

**Inputs** inv.

**Explicit results** 0 · inv.base\_rounded\_total · inv.base\_grand\_total.

**Local steps**

- If is\_internal\_transfer(inv).
  - Return 0.
- If (inv.base\_rounding\_adjustment and inv.base\_rounded\_total).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in inv.base\_rounding\_adjustment → inv.base\_rounded\_total.
  - Return inv.base\_rounded\_total.
- Return inv.base\_grand\_total.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1255)

<a id="op-4f74f0bb285cf1"></a>
### Is internal transfer

`operation_enterprise_binding_enterprise_accounts_report_purchase_register_purchase_register_is_internal_transfer`

**Inputs** inv.

**Declared result** bool.

**Explicit results** bool((inv.is\_internal\_supplier and inv.company equals inv.represents\_company)).

**Local steps**

- Return bool((inv.is\_internal\_supplier and inv.company equals inv.represents\_company)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in inv.is\_internal\_supplier → inv.company equals inv.represents\_company.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1256)
