# Lead and deal records · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm product

<a id="op-ad7842ffbab9ca"></a>
### CRMProduct.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_product\_name().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set product name](operations-006.md#op-0c80bf478bbc10).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L1634) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L974) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L950)

<a id="op-0c80bf478bbc10"></a>
### CRMProduct.set product name

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_set_product_name`

**Inputs** self.

**Local steps**

- Set self.product\_name from (self.product\_name or self.product\_code or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.product\_name → self.product\_code → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L1685) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L973) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L949)

<a id="op-9a07eea3943194"></a>
### CRMProduct.on update

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.get(“ignore\_Enterprise\_sync”).
  - Return no value.
- If not self.get(“Enterprise\_item\_code”).
  - Return no value.
- If not should\_push\_to\_Enterprise().
  - Return no value.
- Evaluate \_push\_to\_item(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L1766) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L972) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L948)

<a id="op-69fdd13f0918b7"></a>
### CRMProduct.before rename

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_before_rename`

**Inputs** self, olddn, newdn, merge = false.

**Local steps**

- Evaluate validate\_rename\_conflict(“CRM Product”, olddn, newdn, merge).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L1920) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L970) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L946)

<a id="op-fd2eba0da57fd6"></a>
### CRMProduct.after rename

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_after_rename`

**Inputs** self, olddn, newdn, merge = false.

**Local steps**

- Evaluate cascade\_rename(“CRM Product”, olddn, newdn, merge).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L2014) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L968) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L944)

<a id="op-fc11b84d7bf9ee"></a>
### CRMProduct.on trash

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_on_trash`

**Inputs** self.

**Record and data access** execute query text (SELECT, Quotation Item).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot delete: linked Enterprise Item {0} is referenced by a Quotation. Remove the reference or delete the I …”.format(self.Enterprise\_item\_code).

**Local steps**

- If in\_cascade().
  - Return no value.
- If not self.get(“Enterprise\_item\_code”).
  - Return no value.
- If not should\_push\_to\_Enterprise().
  - Return no value.
- If Platform.db.sql(query text (SELECT, Quotation Item), self.Enterprise\_item\_code).
  - Call the validation error handler Platform.throw(translated “Cannot delete: linked Enterprise Item {0} is referenced by a Quotation. Remove the reference or delete the I …”.format(self.Enterprise\_item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L2108) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L971) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L947)

<a id="op-85334c1e6b019d"></a>
### Push to item

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_push_to_item`

**Inputs** doc.

**Record and data access** read “Item” via exists · read “Item” via get\_value · resolve a document from “Item” via get\_doc.

**State and service calls** request set\_value on “CRM Product” · call save on item.

**Explicit results** no value.

**Local steps**

- Set item\_code from doc.Enterprise\_item\_code.
- If not Platform.db.exists(“Item”, item\_code).
  - Evaluate Platform.db.set\_value(“CRM Product”, doc.name, “Enterprise\_item\_code”, no value).
  - Return no value.
- Set data from mapping(“item\_name” → doc.product\_name, expand mapping of f → doc.get(f) for f drawn from CATALOGUE\_FIELDS).
  - Draw f from CATALOGUE\_FIELDS.
- Set current from (Platform.db.get\_value(“Item”, item\_code, list(data.keys()), as\_dict = true) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Item”, item\_code, list(data.keys()), as\_dict = true) → mapping().
- If not payload\_differs(data, current).
  - Return no value.
- Set item from Platform.get\_doc(“Item”, item\_code).
- Evaluate item.update(data).
- Set item.flags.ignore\_crm\_sync from true.
- Evaluate item.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L2368) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L975) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L951)

<a id="op-8dfc7f503559de"></a>
### Enqueue reconciliation

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_enqueue_reconciliation`

**Inputs** no declared parameters.

**State and service calls** enqueue with “crm.fcrm.doctype.crm\_product.reconcile\_job.run\_reconciliation”.

**Local steps**

- Evaluate Platform.enqueue(“crm.fcrm.doctype.crm\_product.reconcile\_job.run\_reconciliation”, queue = “long”, timeout = 1200, job\_id = “crm\_product\_item\_reconciliation”, deduplicate = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“crm.fcrm.doctype.crm\_product.reconcile\_job.run\_reconciliation”, queue = “long”, timeout = 1200, job\_id = “crm\_product\_item\_reconciliation”, deduplicate = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L2824) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L978) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L954)

<a id="op-25c91e6b498d58"></a>
### Run reconciliation

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_run_reconciliation`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “Enterprise CRM Settings” via get\_single.

**State and service calls** publish realtime with “crm\_product\_sync\_complete”.

**Explicit results** mapping(“skipped” → skip\_reason) · summary.

**Local steps**

- Set settings from Platform.get\_single(“Enterprise CRM Settings”).
- Set skip\_reason from \_get\_skip\_reason(settings).
- If skip\_reason.
  - Return mapping(“skipped” → skip\_reason).
- Set summary from \_initial\_summary().
- Set items from \_get\_items\_by\_code().
- Set products from \_get\_products\_by\_code().
- Evaluate \_sync\_items\_to\_products(items, products, summary).
- Set issues from \_sync\_products\_to\_items(products, set(items.keys()), summary, settings).
- Evaluate \_record\_issues(settings, issues).
- Evaluate \_sync\_framework\_mirrors().
- Evaluate Platform.publish\_realtime(“crm\_product\_sync\_complete”, user = Platform.session.user).
- Evaluate Platform.log\_error(message = Platform.as\_json(summary), title = “CRM Product Reconciliation”).
- Return summary.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“crm\_product\_sync\_complete”, user = Platform.session.user).

**Boundaries to resolve** stored data, external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L2968) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L984) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L960)

<a id="op-51f4cd281cb475"></a>
### Initial summary

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_initial_summary`

**Inputs** no declared parameters.

**Explicit results** mapping(“already\_linked” → 0, “linked\_by\_exact\_code” → 0, “created\_in\_crm” → 0, “created\_in\_Enterprise” → 0, …).

**Local steps**

- Return mapping(“already\_linked” → 0, “linked\_by\_exact\_code” → 0, “created\_in\_crm” → 0, “created\_in\_Enterprise” → 0, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L3390) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L982) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L958)

<a id="op-c492e75f6e6833"></a>
### Sync items to products

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_sync_items_to_products`

**Inputs** items, products, summary.

**Local steps**

- For each tuple(code, item) in items.items().
  - Evaluate \_sync\_item\_to\_product(item, products.get(code), summary).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L3475) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L987) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L963)

<a id="op-7d82f7f3bef7c3"></a>
### Sync products to items

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_sync_products_to_items`

**Inputs** products, existing\_item\_codes, summary, settings.

**Record and data access** resolve a document from “CRM Product” via get\_doc.

**Explicit results** issues.

**Local steps**

- Set issues from list().
- For each tuple(code, product) in products.items().
  - If code belongs to existing\_item\_codes.
    - Continue with the next iteration or loop test.
  - If \_unlink\_orphan(product, existing\_item\_codes, issues).
    - Update summary at “unlinked\_orphans” using + 1.
    - Continue with the next iteration or loop test.
  - If (product.get(“Enterprise\_item\_code”) or not settings.sync\_products).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in product.get(“Enterprise\_item\_code”) → not settings.sync\_products.
    - Continue with the next iteration or loop test.
  - Set doc from Platform.get\_doc(“CRM Product”, product at “name”).
  - Evaluate \_create\_item\_from\_product(doc).
  - Update summary at “created\_in\_Enterprise” using + 1.
- Return issues.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L3601) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L988) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L964)

<a id="op-d0b7623cc655e6"></a>
### Unlink orphan

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_unlink_orphan`

**Inputs** product, existing\_item\_codes, issues.

**State and service calls** request set\_value on “CRM Product”.

**Explicit results** false · true.

**Local steps**

- If not detect\_orphan(product, existing\_item\_codes).
  - Return false.
- Evaluate Platform.db.set\_value(“CRM Product”, product at “name”, “Enterprise\_item\_code”, no value).
- Evaluate issues.append(mapping(“product” → product at “name”, “kind” → “unlinked\_orphan”, “detail” → translated “Linked Item {0} no longer exists”.format(product at “Enterprise\_item\_code”))).
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L3925) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L989) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L965)

<a id="op-53d522cd65bed3"></a>
### Get skip reason

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_get_skip_reason`

**Inputs** settings.

**Record and data access** read “DocType” via exists.

**Explicit results** “Enterprise\_not\_installed” · “integration\_disabled” · “cross\_site\_not\_supported”.

**Local steps**

- If not Platform.db.exists(“DocType”, “Item”).
  - Return “Enterprise\_not\_installed”.
- If not settings.enabled.
  - Return “integration\_disabled”.
- If settings.is\_Enterprise\_in\_different\_site.
  - Return “cross\_site\_not\_supported”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L4193) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L981) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L957)

<a id="op-7c3d0b7342d1e5"></a>
### Get items by code

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_get_items_by_code`

**Inputs** no declared parameters.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping of i at “item\_code” → i for i drawn from Platform.db.get\_all(“Item”, fields = list(“item\_code”, “item\_name”, “standard\_rate”, “image”, …)).

**Local steps**

- Return mapping of i at “item\_code” → i for i drawn from Platform.db.get\_all(“Item”, fields = list(“item\_code”, “item\_name”, “standard\_rate”, “image”, …)).
  - Draw i from Platform.db.get\_all(“Item”, fields = list(“item\_code”, “item\_name”, “standard\_rate”, “image”, …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L4327) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L979) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L955)

<a id="op-81b5b6ae7c2ace"></a>
### Get products by code

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_get_products_by_code`

**Inputs** no declared parameters.

**Record and data access** read “CRM Product” via get\_all.

**Explicit results** mapping of p at “product\_code” → p for p drawn from Platform.db.get\_all(“CRM Product”, fields = list(“name”, “product\_code”, “product\_name”, “standard\_rate”, …)).

**Local steps**

- Return mapping of p at “product\_code” → p for p drawn from Platform.db.get\_all(“CRM Product”, fields = list(“name”, “product\_code”, “product\_name”, “standard\_rate”, …)).
  - Draw p from Platform.db.get\_all(“CRM Product”, fields = list(“name”, “product\_code”, “product\_name”, “standard\_rate”, …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L4485) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L980) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L956)

<a id="op-1b888b4c7aa2a1"></a>
### Sync item to product

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_sync_item_to_product`

**Inputs** item, product, summary.

**State and service calls** request set\_value on “CRM Product” · request set\_value on “Item”.

**Explicit results** no value.

**Local steps**

- If not product.
  - Evaluate \_create\_crm\_product\_from\_item(item).
  - Update summary at “created\_in\_crm” using + 1.
  - Return no value.
- Set action from classify\_pair(item, product).
- If action.rule equals “already\_linked”.
  - Update summary at “already\_linked” using + 1.
- Otherwise.
  - Update summary at “linked\_by\_exact\_code” using + 1.
- If action.crm\_updates.
  - Evaluate Platform.db.set\_value(“CRM Product”, product at “name”, action.crm\_updates).
- If action.item\_updates.
  - Evaluate Platform.db.set\_value(“Item”, item at “item\_code”, action.item\_updates).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L4652) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L986) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L962)

<a id="op-c429821e05bd46"></a>
### Sync framework mirrors

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_sync_framework_mirrors`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies sync\_shared\_docs.
- Bind dependencies sync\_user\_permissions.
- Evaluate sync\_user\_permissions().
- Evaluate sync\_shared\_docs().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L4993) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L985) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L961)

<a id="op-0d41b57007a821"></a>
### Create crm product from item

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_create_customer_relationship_product_from_item`

**Inputs** item.

**State and service calls** request new\_doc for “CRM Product” · call insert on product · request set\_value on “Item”.

**Local steps**

- Set product from Platform.new\_doc(“CRM Product”).
- Set product.product\_code from item at “item\_code”.
- Set product.Enterprise\_item\_code from item at “item\_code”.
- Set product.product\_name from item.get(“item\_name”).
- For each f in CATALOGUE\_FIELDS.
  - Evaluate product.set(f, item.get(f)).
- Set product.flags.ignore\_Enterprise\_sync from true.
- Evaluate product.insert(ignore\_permissions = true).
- Evaluate Platform.db.set\_value(“Item”, item at “item\_code”, “crm\_product\_code”, product.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L5064) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L976) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L952)

<a id="op-4852c622c2fab3"></a>
### Create item from product

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_create_item_from_product`

**Inputs** product\_doc.

**Record and data access** resolve a document from mapping(“doctype” → “Item”, “item\_code” → product\_doc.product\_code, “item\_name” → (product\_doc.product\_name or product\_doc.product\_code), “standard\_rate” → product\_doc.standard\_rate, …) via get\_doc · read “Stock Settings” via get\_single\_value.

**State and service calls** call insert on item · request set\_value on “CRM Product”.

**Local steps**

- Set item from Platform.get\_doc(mapping(“doctype” → “Item”, “item\_code” → product\_doc.product\_code, “item\_name” → (product\_doc.product\_name or product\_doc.product\_code), “standard\_rate” → product\_doc.standard\_rate, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in product\_doc.product\_name → product\_doc.product\_code.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Stock Settings”, “item\_group”) → “All Item Groups”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Stock Settings”, “stock\_uom”) → “Nos”.
- Set item.flags.ignore\_crm\_sync from true.
- Evaluate item.insert(ignore\_permissions = true).
- Evaluate Platform.db.set\_value(“CRM Product”, product\_doc.name, “Enterprise\_item\_code”, item.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “item\_group”), Platform.db.get\_single\_value(“Stock Settings”, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L5393) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L977) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L953)

<a id="op-82b77e80e85fc8"></a>
### Record issues

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconcile_job_business_behavior_record_issues`

**Inputs** settings, issues.

**State and service calls** call save on settings.

**Explicit results** no value.

**Local steps**

- If not issues.
  - Return no value.
- For each issue in issues.
  - Evaluate settings.append(“sync\_issues”, issue).
- Evaluate settings.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L5866) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L983) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L959)

<a id="op-147162caab1054"></a>
### Classify pair

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconciliation_business_behavior_classify_pair`

**Inputs** item, product.

**Declared result** PairAction.

**Explicit results** PairAction(rule = “already\_linked”) · PairAction(rule = “exact\_code”, crm\_updates = updates, item\_updates = mapping(“crm\_product\_code” → product at “name”)) · PairAction(rule = “no\_match”).

**Local steps**

- If (item.get(“crm\_product\_code”) equals product.get(“name”) and product.get(“Enterprise\_item\_code”) equals item.get(“item\_code”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“crm\_product\_code”) equals product.get(“name”) → product.get(“Enterprise\_item\_code”) equals item.get(“item\_code”).
  - Return PairAction(rule = “already\_linked”).
- If item.get(“item\_code”) equals product.get(“product\_code”).
  - Set updates from mapping(“Enterprise\_item\_code” → item at “item\_code”).
  - For each f in CATALOGUE\_FIELDS.
    - Set updates at f from item.get(f).
  - If (not product.get(“product\_name”) and item.get(“item\_name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not product.get(“product\_name”) → item.get(“item\_name”).
    - Set updates at “product\_name” from item at “item\_name”.
  - Return PairAction(rule = “exact\_code”, crm\_updates = updates, item\_updates = mapping(“crm\_product\_code” → product at “name”)).
- Return PairAction(rule = “no\_match”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L5999) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L990) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L966)

<a id="op-e4407756efdadc"></a>
### Detect orphan

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_reconciliation_business_behavior_detect_orphan`

**Inputs** product, existing\_item\_codes.

**Declared result** bool.

**Explicit results** (bool(linked) and linked does not belong to existing\_item\_codes).

**Local steps**

- Set linked from product.get(“Enterprise\_item\_code”).
- Return (bool(linked) and linked does not belong to existing\_item\_codes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(linked) → linked does not belong to existing\_item\_codes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L6527) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L991) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L967)

<a id="op-a8072dc09ac6a9"></a>
### Payload differs

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_sync_utils_business_behavior_payload_differs`

**Inputs** payload, target.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each tuple(key, new\_value) in payload.items().
  - If (new\_value or no value) differs from (target.get(key) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_value → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in target.get(key) → no value.
    - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L6657) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L992) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L968)
