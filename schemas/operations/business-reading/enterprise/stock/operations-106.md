# Inventory and warehouses · operations 106

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-55acc9d5712976"></a>
### Get latest stock balance

`operation_enterprise_stock_utils_business_behavior_get_latest_stock_balance`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Bin).

**Explicit results** bin\_map.

**Local steps**

- Set bin\_map from mapping().
- For each d in Platform.db.sql(query text (SELECT, Bin), as\_dict = 1).
  - Evaluate bin\_map.setdefault(d.warehouse, mapping()).setdefault(d.item\_code, flt(d.stock\_value)).
- Return bin\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L885)

<a id="op-36edc84ec0b885"></a>
### Get bin qty map

`operation_enterprise_stock_utils_business_behavior_get_bin_quantity_map`

**Inputs** rows.

**Declared result** dict at tuple(tuple at tuple(str, str), Platform.\_dict).

**Record and data access** read “Bin” via get\_all.

**Explicit results** mapping() · mapping of tuple(bin.item\_code, bin.warehouse) → bin for bin drawn from bins.

**Local steps**

- Set item\_codes from set().
- Set warehouses from set().
- For each row in rows.
  - If (row.item\_code and row.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → row.warehouse.
    - Evaluate item\_codes.add(row.item\_code).
    - Evaluate warehouses.add(row.warehouse).
- If not item\_codes.
  - Return mapping().
- Set bins from Platform.get\_all(“Bin”, filters = mapping(“item\_code” → list(“in”, item\_codes), “warehouse” → list(“in”, warehouses)), fields = list(“item\_code”, “warehouse”, “actual\_qty”, “projected\_qty”, …)).
- Return mapping of tuple(bin.item\_code, bin.warehouse) → bin for bin drawn from bins.
  - Draw bin from bins.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L877)

<a id="op-d1c13abb173fd1"></a>
### Get bin

`operation_enterprise_stock_utils_business_behavior_get_bin`

**Inputs** item\_code, warehouse.

**Record and data access** read “Bin” via get\_value · resolve a document from “Bin” via get\_doc.

**Explicit results** bin\_obj.

**Local steps**

- Set bin from Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse)).
- If not bin.
  - Set bin\_obj from \_create\_bin(item\_code, warehouse).
- Otherwise.
  - Set bin\_obj from Platform.get\_doc(“Bin”, bin).
- Set bin\_obj.flags.ignore\_permissions from true.
- Return bin\_obj.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L2335) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L876)

<a id="op-24af19baf8da59"></a>
### Get or make bin

`operation_enterprise_stock_utils_business_behavior_get_or_make_bin`

**Inputs** item\_code, warehouse.

**Declared result** str.

**Record and data access** read “Bin” via get\_value.

**Explicit results** bin\_record.

**Local steps**

- Set bin\_record from Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse)).
- If not bin\_record.
  - Set bin\_obj from \_create\_bin(item\_code, warehouse).
  - Set bin\_record from bin\_obj.name.
- Return bin\_record.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L2561) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L887)

<a id="op-98a57a9588d199"></a>
### Create bin

`operation_enterprise_stock_utils_business_behavior_create_bin`

**Inputs** item\_code, warehouse.

**Record and data access** resolve a document from “Bin” via get\_doc · read “Bin” via get\_last\_doc.

**State and service calls** savepoint bin\_creation\_savepoint · call insert on bin\_obj · rollback.

**Explicit results** bin\_obj.

**Local steps**

- Set bin\_creation\_savepoint from “create\_bin”.
- Attempt the following.
  - Evaluate Platform.db.savepoint(bin\_creation\_savepoint).
  - Set bin\_obj from Platform.get\_doc(doctype = “Bin”, item\_code = item\_code, warehouse = warehouse).
  - Set bin\_obj.flags.ignore\_permissions from 1.
  - Evaluate bin\_obj.insert().
- On failure (Platform.UniqueValidationError).
  - Evaluate Platform.db.rollback(save\_point = bin\_creation\_savepoint).
  - Set bin\_obj from Platform.get\_last\_doc(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse)).
- Return bin\_obj.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L2758) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L874)

<a id="op-e89c4d29148dc8"></a>
### Get incoming rate

`operation_enterprise_stock_utils_business_behavior_get_incoming_rate`

**Inputs** args, raise\_error\_if\_no\_rate = true, fallbacks = true.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_incoming\_rate(args, raise\_error\_if\_no\_rate, fallbacks).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted for {0}”.format(warehouse).

**Local steps**

- Set args from Platform.parse\_json(args).
- Set item\_code from args.get(“item\_code”) when isinstance(args, (dict bitwise or Platform.\_dict)), otherwise no value.
  - Value choice on isinstance(args, (dict bitwise or Platform.\_dict)) — true gives args.get(“item\_code”), false gives no value.
- Set warehouse from args.get(“warehouse”) when isinstance(args, (dict bitwise or Platform.\_dict)), otherwise no value.
  - Value choice on isinstance(args, (dict bitwise or Platform.\_dict)) — true gives args.get(“warehouse”), false gives no value.
- If item\_code.
  - Evaluate Platform.has\_permission(“Item”, ptype = “select”, doc = item\_code, throw = true).
- Otherwise.
  - Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- If warehouse.
  - Bind dependencies get\_user\_permissions.
  - If warehouse\_permissions bound to get\_user\_permissions(Platform.session.user).get(“Warehouse”).
    - Set allowed\_warehouses from set of perm.get(“doc”) for perm drawn from warehouse\_permissions where (perm.get(“doc”) and not perm.get(“applicable\_for”)).
      - Draw perm from warehouse\_permissions, keep a combination only if ((perm.get(“doc”) and not perm.get(“applicable\_for”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.get(“doc”) → not perm.get(“applicable\_for”).
    - If (allowed\_warehouses and warehouse does not belong to allowed\_warehouses).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_warehouses → warehouse does not belong to allowed\_warehouses.
      - Call the validation error handler Platform.throw(translated “Not permitted for {0}”.format(warehouse), Platform.PermissionError).
- Return \_get\_incoming\_rate(args, raise\_error\_if\_no\_rate, fallbacks).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, doc = item\_code, throw = true), Platform.has\_permission(“Item”, ptype = “select”, throw = true) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L883)

<a id="op-e6a6326c7cd57b"></a>
### Get incoming rate

`operation_enterprise_binding_enterprise_stock_utils_get_incoming_rate`

**Inputs** args, raise\_error\_if\_no\_rate = true, fallbacks = true.

**Record and data access** read “Item” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** sn\_obj.get\_incoming\_rate() · batch\_obj.get\_incoming\_rate() · flt(in\_rate).

**Local steps**

- Bind dependencies get\_previous\_sle, get\_valuation\_rate.
- If isinstance(args, str).
  - Set args from json.loads(args).
- If (not args.get(“posting\_datetime”) and args.get(“posting\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args.get(“posting\_datetime”) → args.get(“posting\_date”).
  - Set args at “posting\_datetime” from get\_combine\_datetime(args.get(“posting\_date”), args.get(“posting\_time”)).
- Set posting\_datetime from args.get(“posting\_datetime”).
- Set in\_rate from no value.
- Set item\_details from Platform.get\_cached\_value(“Item”, args.get(“item\_code”), list(“has\_serial\_no”, “has\_batch\_no”, “use\_serial\_no\_wise\_valuation”), as\_dict = 1).
- Set skip\_serial\_batch\_valuation from bool((item\_details and item\_details.has\_serial\_no and not item\_details.use\_serial\_no\_wise\_valuation)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.has\_serial\_no → not item\_details.use\_serial\_no\_wise\_valuation.
- If isinstance(args, dict).
  - Set args from Platform.\_dict(args).
- Set use\_moving\_avg\_for\_batch from (Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”) and not has\_batchwise\_valued\_batch(args.get(“batch\_no”), args.get(“serial\_and\_batch\_bundle”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”) → not has\_batchwise\_valued\_batch(args.get(“batch\_no”), args.get(“serial\_and\_batch\_bundle”)).
- If (item\_details and item\_details.has\_serial\_no and args.get(“serial\_and\_batch\_bundle”) and not skip\_serial\_batch\_valuation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.has\_serial\_no → args.get(“serial\_and\_batch\_bundle”) → not skip\_serial\_batch\_valuation.
  - Set args.actual\_qty from args.qty.
  - Set sn\_obj from SerialNoValuation(sle = args, warehouse = args.get(“warehouse”), item\_code = args.get(“item\_code”)).
  - Return sn\_obj.get\_incoming\_rate().
- Otherwise.
  - If (item\_details and item\_details.has\_batch\_no and args.get(“serial\_and\_batch\_bundle”) and not use\_moving\_avg\_for\_batch and not skip\_serial\_batch\_valuation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.has\_batch\_no → args.get(“serial\_and\_batch\_bundle”) → not use\_moving\_avg\_for\_batch → not skip\_serial\_batch\_valuation.
    - Set args.actual\_qty from args.qty.
    - Set batch\_obj from BatchNoValuation(sle = args, warehouse = args.get(“warehouse”), item\_code = args.get(“item\_code”)).
    - Return batch\_obj.get\_incoming\_rate().
  - Otherwise.
    - If ((args.get(“serial\_no”) or empty text).strip() and not args.get(“serial\_and\_batch\_bundle”) and not skip\_serial\_batch\_valuation).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (args.get(“serial\_no”) or empty text).strip() → not args.get(“serial\_and\_batch\_bundle”) → not skip\_serial\_batch\_valuation.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“serial\_no”) → empty text.
      - Set args.actual\_qty from args.qty.
      - Set args.serial\_nos from get\_serial\_nos\_data(args.get(“serial\_no”)).
      - Set sn\_obj from SerialNoValuation(sle = args, warehouse = args.get(“warehouse”), item\_code = args.get(“item\_code”)).
      - Return sn\_obj.get\_incoming\_rate().
    - Otherwise.
      - If (args.get(“batch\_no”) and not args.get(“serial\_and\_batch\_bundle”) and not use\_moving\_avg\_for\_batch and not skip\_serial\_batch\_valuation).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“batch\_no”) → not args.get(“serial\_and\_batch\_bundle”) → not use\_moving\_avg\_for\_batch → not skip\_serial\_batch\_valuation.
        - Set args.actual\_qty from args.qty.
        - Set args.batch\_nos from Platform.\_dict(mapping(args.batch\_no → args)).
        - Set batch\_obj from BatchNoValuation(sle = args, warehouse = args.get(“warehouse”), item\_code = args.get(“item\_code”)).
        - Return batch\_obj.get\_incoming\_rate().
      - Otherwise.
        - Set valuation\_method from get\_valuation\_method(args.get(“item\_code”), args.get(“company”)).
        - Set previous\_sle from get\_previous\_sle(mapping(expand args, “serial\_no” → no value)).
        - If valuation\_method belongs to tuple(“FIFO”, “LIFO”).
          - If previous\_sle.
            - Set previous\_stock\_queue from json.loads((previous\_sle.get(“stock\_queue”, “&#91;&#93;”) or “&#91;&#93;”)).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_sle.get(“stock\_queue”, “&#91;&#93;”) → “&#91;&#93;”.
            - Set in\_rate from \_get\_fifo\_lifo\_rate(previous\_stock\_queue, (args.get(“qty”) or 0), valuation\_method) when previous\_stock\_queue, otherwise no value.
              - Value choice on previous\_stock\_queue — true gives \_get\_fifo\_lifo\_rate(previous\_stock\_queue, (args.get(“qty”) or 0), valuation\_method), false gives no value.
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“qty”) → 0.
        - Otherwise.
          - If valuation\_method equals “Moving Average”.
            - Set in\_rate from previous\_sle.get(“valuation\_rate”).
- If in\_rate is identical to no value.
  - Set voucher\_no from (args.get(“voucher\_no”) or args.get(“name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“voucher\_no”) → args.get(“name”).
  - Set in\_rate from get\_valuation\_rate(args.get(“item\_code”), args.get(“warehouse”), args.get(“voucher\_type”), voucher\_no, currency = Enterprise.get\_company\_currency(args.get(“company”)), company = args.get(“company”), fallba ….
- Return flt(in\_rate).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, args.get(“item\_code”), list(“has\_serial\_no”, “has\_batch\_no”, “use\_serial\_no\_wise\_valuation”), as\_dict = 1), Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1133)

<a id="op-0e2ddcfce6d390"></a>
### Has batchwise valued batch

`operation_enterprise_binding_enterprise_stock_utils_has_batchwise_valued_batch`

**Inputs** batch\_no, serial\_and\_batch\_bundle.

**Declared result** bool.

**Record and data access** read “Serial and Batch Entry” via get\_all · read “Batch” via exists.

**Explicit results** (bool(batches) and Platform.db.exists(“Batch”, mapping(“name” → tuple(“in”, batches), “use\_batchwise\_valuation” → 1)) is distinct from no value).

**Local steps**

- Set batches from list(batch\_no) when batch\_no, otherwise list().
  - Value choice on batch\_no — true gives list(batch\_no), false gives list().
- If serial\_and\_batch\_bundle.
  - Set batches from Platform.get\_all(“Serial and Batch Entry”, mapping(“parent” → serial\_and\_batch\_bundle), pluck = “batch\_no”).
- Return (bool(batches) and Platform.db.exists(“Batch”, mapping(“name” → tuple(“in”, batches), “use\_batchwise\_valuation” → 1)) is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(batches) → Platform.db.exists(“Batch”, mapping(“name” → tuple(“in”, batches), “use\_batchwise\_valuation” → 1)) is distinct from no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1136)

<a id="op-60978e7b8d30f7"></a>
### Get avg purchase rate

`operation_enterprise_stock_utils_business_behavior_get_average_purchase_rate`

**Inputs** serial\_nos.

**State and service calls** execute a supplied database query.

**Explicit results** flt(Platform.db.sql((query text (SELECT, Serial No) modulo or format nested operand in the contract.join((nested operand in the contract × nested operand in the contract))), tuple(serial\_nos)) at 0 at 0).

**Local steps**

- Set serial\_nos from get\_valid\_serial\_nos(serial\_nos).
- Return flt(Platform.db.sql((query text (SELECT, Serial No) modulo or format nested operand in the contract.join((nested operand in the contract × nested operand in the contract))), tuple(serial\_nos)) at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L875)

<a id="op-5ad361d8222bf1"></a>
### Is serial no wise valuation disabled

`operation_enterprise_binding_enterprise_stock_utils_is_serial_no_wise_valuation_disabled`

**Inputs** item\_code.

**Declared result** bool.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** bool((item\_details and item\_details.has\_serial\_no and not item\_details.use\_serial\_no\_wise\_valuation)).

**Local steps**

- Set item\_details from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “use\_serial\_no\_wise\_valuation”), as\_dict = 1).
- Return bool((item\_details and item\_details.has\_serial\_no and not item\_details.use\_serial\_no\_wise\_valuation)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.has\_serial\_no → not item\_details.use\_serial\_no\_wise\_valuation.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “use\_serial\_no\_wise\_valuation”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1137)

<a id="op-2d4b55810ed01a"></a>
### Get valuation method

`operation_enterprise_stock_utils_business_behavior_get_valuation_method`

**Inputs** item\_code, company = no value.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Item” via get\_cached\_value · read “Company” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** val\_method.

**Local steps**

- Set val\_method from Platform.get\_cached\_value(“Item”, item\_code, “valuation\_method”).
- If not val\_method.
  - Set val\_method from Platform.get\_cached\_value(“Company”, company, “valuation\_method”) when company, otherwise (Platform.get\_single\_value(“Stock Settings”, “valuation\_method”) or “FIFO”).
    - Value choice on company — true gives Platform.get\_cached\_value(“Company”, company, “valuation\_method”), false gives (Platform.get\_single\_value(“Stock Settings”, “valuation\_method”) or “FIFO”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “valuation\_method”) → “FIFO”.
- Return val\_method.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “valuation\_method”), Platform.get\_cached\_value(“Company”, company, “valuation\_method”) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L5288) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L893)

<a id="op-acfa472db05eea"></a>
### Clear valuation method cache

`operation_enterprise_binding_enterprise_stock_utils_clear_valuation_method_cache`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set cache from getattr(Platform.local, “request\_cache”, no value).
- If not cache.
  - Return no value.
- Evaluate cache.pop(getattr(get\_valuation\_method, “\_\_wrapped\_\_”, get\_valuation\_method), no value).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request\_cache”, no value), getattr(get\_valuation\_method, “\_\_wrapped\_\_”, get\_valuation\_method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1131)

<a id="op-bd164164b64e3d"></a>
### Get fifo rate

`operation_enterprise_stock_utils_business_behavior_get_first_in_first_out_rate`

**Inputs** previous\_stock\_queue, qty.

**Explicit results** \_get\_fifo\_lifo\_rate(previous\_stock\_queue, qty, “FIFO”).

**Local steps**

- Return \_get\_fifo\_lifo\_rate(previous\_stock\_queue, qty, “FIFO”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L5503) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L881)

<a id="op-2aa77190e41922"></a>
### Get lifo rate

`operation_enterprise_stock_utils_business_behavior_get_last_in_first_out_rate`

**Inputs** previous\_stock\_queue, qty.

**Explicit results** \_get\_fifo\_lifo\_rate(previous\_stock\_queue, qty, “LIFO”).

**Local steps**

- Return \_get\_fifo\_lifo\_rate(previous\_stock\_queue, qty, “LIFO”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L5570) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L884)

<a id="op-7a54b8a7bedae8"></a>
### Get fifo lifo rate

`operation_enterprise_stock_utils_business_behavior_get_first_in_first_out_last_in_first_out_rate`

**Inputs** previous\_stock\_queue, qty, method.

**Explicit results** (total\_value ÷ total\_qty) when total\_qty, otherwise 0.0.

**Local steps**

- Set ValuationKlass from LIFOValuation when method equals “LIFO”, otherwise FIFOValuation.
  - Value choice on method equals “LIFO” — true gives LIFOValuation, false gives FIFOValuation.
- Set stock\_queue from ValuationKlass(previous\_stock\_queue).
- If flt(qty) ≥ 0.
  - Set tuple(total\_qty, total\_value) from stock\_queue.get\_total\_stock\_and\_value().
  - Return (total\_value ÷ total\_qty) when total\_qty, otherwise 0.0.
    - Value choice on total\_qty — true gives (total\_value ÷ total\_qty), false gives 0.0.
- Otherwise.
  - Set popped\_bins from stock\_queue.remove\_stock(abs(flt(qty))).
  - Set tuple(total\_qty, total\_value) from ValuationKlass(popped\_bins).get\_total\_stock\_and\_value().
  - Return (total\_value ÷ total\_qty) when total\_qty, otherwise 0.0.
    - Value choice on total\_qty — true gives (total\_value ÷ total\_qty), false gives 0.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L5637) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L880)

<a id="op-b44c1214899f46"></a>
### Get valid serial nos

`operation_enterprise_stock_utils_business_behavior_get_valid_serial_numbers`

**Inputs** sr\_nos, qty = 0, item\_code = empty text.

**Explicit results** valid\_serial\_nos.

**Explicit failure paths** validation helper — translated “Serial number {0} entered more than once”.format(val) · validation helper — translated “{0} valid serial nos for Item {1}”.format(abs(qty), item\_code).

**Local steps**

- Set serial\_nos from nested operand in the contract(nested operand in the contract).strip().replace(“,”, whitespace '\\n').split(whitespace '\\n').
- Set valid\_serial\_nos from list().
- For each val in serial\_nos.
  - If val.
    - Set val from val.strip().
    - If val belongs to valid\_serial\_nos.
      - Call the validation error handler Platform.throw(translated “Serial number {0} entered more than once”.format(val)).
    - Otherwise.
      - Evaluate valid\_serial\_nos.append(val).
- If (qty and len(valid\_serial\_nos) differs from abs(qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty → len(valid\_serial\_nos) differs from abs(qty).
  - Call the validation error handler Platform.throw(translated “{0} valid serial nos for Item {1}”.format(abs(qty), item\_code)).
- Return valid\_serial\_nos.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L5959) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L892)

<a id="op-682c09bcdc3e7f"></a>
### Validate warehouse company

`operation_enterprise_stock_utils_business_behavior_validate_warehouse_company`

**Inputs** warehouse, company.

**Record and data access** read “Warehouse” via get\_value.

**Explicit failure paths** validation helper with InvalidWarehouseCompany — translated “Warehouse {0} does not belong to company {1}”.format(warehouse, company).

**Local steps**

- Set warehouse\_company from Platform.db.get\_value(“Warehouse”, warehouse, “company”, cache = true).
- If (warehouse\_company and warehouse\_company differs from company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse\_company → warehouse\_company differs from company.
  - Call the validation error handler Platform.throw(translated “Warehouse {0} does not belong to company {1}”.format(warehouse, company), InvalidWarehouseCompany).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L6380) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L902)

<a id="op-f8ad210d9d5ae9"></a>
### Is group warehouse

`operation_enterprise_stock_utils_business_behavior_is_group_warehouse`

**Inputs** warehouse.

**Record and data access** read “Warehouse” via get\_value.

**Explicit failure paths** validation helper — translated “Group node warehouse is not allowed to select for transactions”.

**Local steps**

- If Platform.db.get\_value(“Warehouse”, warehouse, “is\_group”, cache = true).
  - Call the validation error handler Platform.throw(translated “Group node warehouse is not allowed to select for transactions”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L6575) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L894)

<a id="op-92133a93951dca"></a>
### Validate disabled warehouse

`operation_enterprise_stock_utils_business_behavior_validate_disabled_warehouse`

**Inputs** warehouse.

**Record and data access** read “Warehouse” via get\_value.

**Explicit failure paths** validation helper — translated “Disabled Warehouse {0} cannot be used for this transaction.”.format(get\_link\_to\_form(“Warehouse”, warehouse)).

**Local steps**

- If Platform.db.get\_value(“Warehouse”, warehouse, “disabled”, cache = true).
  - Call the validation error handler Platform.throw(translated “Disabled Warehouse {0} cannot be used for this transaction.”.format(get\_link\_to\_form(“Warehouse”, warehouse))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L6704) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L901)

<a id="op-c02b11994c1af2"></a>
### Update included uom in report

`operation_enterprise_stock_utils_business_behavior_update_included_unit_of_measure_in_report`

**Inputs** columns, result, include\_uom, conversion\_factors.

**State and service calls** call insert on columns · call insert on row.

**Explicit results** no value.

**Local steps**

- If (not include\_uom or not conversion\_factors).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not include\_uom → not conversion\_factors.
  - Return no value.
- Set is\_dict\_obj from false.
- If isinstance(result at 0, dict).
  - Set is\_dict\_obj from true.
- Set convertible\_columns from mapping().
- For each tuple(idx, d) in enumerate(columns).
  - Set key from d.get(“fieldname”) when is\_dict\_obj, otherwise idx.
    - Value choice on is\_dict\_obj — true gives d.get(“fieldname”), false gives idx.
  - If d.get(“convertible”).
    - Evaluate convertible\_columns.setdefault(key, d.get(“convertible”)).
    - Evaluate columns.insert((idx + 1), mapping(“label” → “{} (per {})”.format(d.get(“label”), include\_uom), “fieldname” → “{}\_{}”.format(d.get(“fieldname”), Platform.scrub(include\_uom)), “fieldtype” → “Currency” when d ….
      - Value choice on d.get(“convertible”) equals “rate” — true gives “Currency”, false gives “Float”.
- Set update\_dict\_values from list().
- For each tuple(row\_idx, row) in enumerate(result).
  - Set data from row.items() when is\_dict\_obj, otherwise enumerate(row).
    - Value choice on is\_dict\_obj — true gives row.items(), false gives enumerate(row).
  - For each tuple(key, value) in data.
    - If key does not belong to convertible\_columns.
      - Continue with the next iteration or loop test.
    - Set conversion\_factor from conversion\_factors at row\_idx.
    - If not conversion\_factor.
      - Set new\_value from no value.
    - Otherwise.
      - If convertible\_columns.get(key) equals “rate”.
        - Set new\_value from (flt(value) × conversion\_factor).
      - Otherwise.
        - Set new\_value from (flt(value) ÷ conversion\_factor).
    - If not is\_dict\_obj.
      - Evaluate row.insert((key + 1), new\_value).
    - Otherwise.
      - Set new\_key from formatted text {key}\_{Platform.scrub(include\_uom)}.
      - Evaluate update\_dict\_values.append(list(row, new\_key, new\_value)).
- For each data in update\_dict\_values.
  - Set tuple(row, key, value) from data.
  - Set row at key from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L899)

<a id="op-bb0b34fe3cb135"></a>
### Add additional uom columns

`operation_enterprise_stock_utils_business_behavior_add_additional_unit_of_measure_columns`

**Inputs** columns, result, include\_uom, conversion\_factors.

**State and service calls** call insert on columns.

**Explicit results** no value.

**Local steps**

- If (not include\_uom or not conversion\_factors).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not include\_uom → not conversion\_factors.
  - Return no value.
- Set convertible\_column\_map from mapping().
- For each col\_idx in list(reversed(range(0, len(columns)))).
  - Set col from columns at col\_idx.
  - If (isinstance(col, dict) and col.get(“convertible”) belongs to list(“rate”, “qty”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(col, dict) → col.get(“convertible”) belongs to list(“rate”, “qty”).
    - Set next\_col from (col\_idx + 1).
    - Evaluate columns.insert(next\_col, col.copy()).
    - Update columns at next\_col at “fieldname” using + “\_alt”.
    - Set convertible\_column\_map at col.get(“fieldname”) from Platform.\_dict(mapping(“converted\_col” → columns at next\_col at “fieldname”, “for\_type” → col.get(“convertible”))).
    - If col.get(“convertible”) equals “rate”.
      - Update columns at next\_col at “label” using + formatted text  (per {include\_uom}).
    - Otherwise.
      - Update columns at next\_col at “label” using + formatted text  ({include\_uom}).
- For each tuple(row\_idx, row) in enumerate(result).
  - For each tuple(convertible\_col, data) in convertible\_column\_map.items().
    - Set conversion\_factor from (conversion\_factors.get(row.get(“item\_code”)) or 1.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in conversion\_factors.get(row.get(“item\_code”)) → 1.0.
    - Set for\_type from data.for\_type.
    - Set value\_before\_conversion from row.get(convertible\_col).
    - If for\_type equals “rate”.
      - Set row at data.converted\_col from (flt(value\_before\_conversion) × conversion\_factor).
    - Otherwise.
      - Set row at data.converted\_col from (flt(value\_before\_conversion) ÷ conversion\_factor).
  - Set result at row\_idx from row.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L1053) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L872)

<a id="op-ba16654a92841a"></a>
### Get incoming outgoing rate for cancel

`operation_enterprise_stock_utils_business_behavior_get_incoming_outgoing_rate_for_cancel`

**Inputs** item\_code, voucher\_type, voucher\_no, voucher\_detail\_no.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).

**Explicit results** outgoing\_rate.

**Local steps**

- Set outgoing\_rate from Platform.db.sql(query text (SELECT, Stock Ledger Entry), tuple(voucher\_type, voucher\_no, item\_code, voucher\_detail\_no)).
- Set outgoing\_rate from outgoing\_rate at 0 at 0 when outgoing\_rate, otherwise 0.0.
  - Value choice on outgoing\_rate — true gives outgoing\_rate at 0 at 0, false gives 0.0.
- Return outgoing\_rate.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L882)

<a id="op-bccd47948b9f38"></a>
### Is reposting item valuation in progress

`operation_enterprise_stock_utils_business_behavior_is_reposting_item_valuation_in_progress`

**Inputs** no declared parameters.

**Record and data access** read “Repost Item Valuation” via exists.

**State and service calls** msgprint with translated “Item valuation reposting in progress. Report might show incorrect item valuation.”.

**Local steps**

- Set reposting\_in\_progress from Platform.db.exists(“Repost Item Valuation”, mapping(“docstatus” → 1, “status” → list(“in”, list(“Queued”, “In Progress”)))).
- If reposting\_in\_progress.
  - Evaluate Platform.msgprint(translated “Item valuation reposting in progress. Report might show incorrect item valuation.”, alert = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L2423) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L895)

<a id="op-9534634d1f2dab"></a>
### Check pending reposting

`operation_enterprise_stock_utils_business_behavior_check_pending_reposting`

**Inputs** posting\_date, company = no value, throw\_error = true.

**Declared result** bool.

**Record and data access** read “Repost Item Valuation” via exists.

**State and service calls** msgprint with msg.

**Explicit results** bool(reposting\_pending).

**Local steps**

- Set filters from mapping(“docstatus” → 1, “status” → list(“in”, list(“Queued”, “In Progress”)), “posting\_date” → list(“&lt;=”, posting\_date)).
- If company.
  - Set filters at “company” from company.
- Set reposting\_pending from Platform.db.exists(“Repost Item Valuation”, filters).
- If (reposting\_pending and throw\_error).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reposting\_pending → throw\_error.
  - Set msg from translated “Stock/Accounts can not be frozen as processing of backdated entries is going on. Please try again later.”.
  - Evaluate Platform.msgprint(msg, raise\_exception = PendingRepostingError, title = “Stock Reposting Ongoing”, indicator = “red”, primary\_action = mapping(“label” → translated “Show pending entries”, “client\_action” → ….
- Return bool(reposting\_pending).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0948.json#L2600) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L873)
