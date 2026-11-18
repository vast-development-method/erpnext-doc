# Lead and deal records · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm products

<a id="op-8d24eaaea77bd6"></a>
### Get product rate details

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_get_product_rate_details`

**Inputs** product\_code, deal = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “CRM Product” via get\_value.

**Explicit results** mapping(“product\_name” → product.get(“product\_name”), “rate” → rate).

**Local steps**

- Set product from (Platform.db.get\_value(“CRM Product”, product\_code, list(“product\_name”, “standard\_rate”), as\_dict = true) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“CRM Product”, product\_code, list(“product\_name”, “standard\_rate”), as\_dict = true) → mapping().
- Set rate from (\_contextual\_rate(product\_code, deal) or product.get(“standard\_rate”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_contextual\_rate(product\_code, deal) → product.get(“standard\_rate”).
- Return mapping(“product\_name” → product.get(“product\_name”), “rate” → rate).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L1889) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1030) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1006)

<a id="op-02ed5fe06969b1"></a>
### Contextual rate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_contextual_rate`

**Inputs** product\_code, deal.

**Record and data access** read “CRM Product” via get\_value.

**Explicit results** no value · get\_deal\_product\_rate(item\_code, deal).

**Local steps**

- If not Platform.get\_meta(“CRM Product”).has\_field(“Enterprise\_item\_code”).
  - Return no value.
- Set item\_code from Platform.db.get\_value(“CRM Product”, product\_code, “Enterprise\_item\_code”).
- If not item\_code.
  - Return no value.
- Return get\_deal\_product\_rate(item\_code, deal).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L2176) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1026) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1002)

<a id="op-4e5e85f1495fd0"></a>
### Resolve price list

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_resolve_price_list`

**Inputs** customer.

**Record and data access** read “Customer” via exists · resolve a document from “Customer” via get\_cached\_doc · read “Selling Settings” via get\_single\_value.

**Explicit results** pl · Platform.db.get\_single\_value(“Selling Settings”, “selling\_price\_list”).

**Local steps**

- If (customer and Platform.db.exists(“Customer”, customer)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in customer → Platform.db.exists(“Customer”, customer).
  - Bind dependencies get\_default\_price\_list.
  - If pl bound to get\_default\_price\_list(Platform.get\_cached\_doc(“Customer”, customer)).
    - Return pl.
- Return Platform.db.get\_single\_value(“Selling Settings”, “selling\_price\_list”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Customer”, customer), Platform.db.get\_single\_value(“Selling Settings”, “selling\_price\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L2381) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1032) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1008)

<a id="op-d0951b3ea092c5"></a>
### Get deal product rate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_get_deal_product_rate`

**Inputs** item\_code, deal = no value.

**Record and data access** read “DocType” via exists · read “CRM Deal” via get\_value · read “Item” via get\_value.

**Explicit results** no value · \_price\_list\_rate(get\_item\_price(pctx, item\_code)).

**Local steps**

- If not Platform.db.exists(“DocType”, “Item Price”).
  - Return no value.
- Set customer from Platform.db.get\_value(“CRM Deal”, deal, “Enterprise\_customer”) when deal, otherwise no value.
  - Value choice on deal — true gives Platform.db.get\_value(“CRM Deal”, deal, “Enterprise\_customer”), false gives no value.
- Set price\_list from \_resolve\_price\_list(customer).
- If not price\_list.
  - Return no value.
- Bind dependencies get\_item\_price.
- Set pctx from Platform.\_dict(mapping(“price\_list” → price\_list, “customer” → customer, “uom” → Platform.db.get\_value(“Item”, item\_code, “stock\_uom”), “transaction\_date” → Platform.utils.nowdate())).
- Return \_price\_list\_rate(get\_item\_price(pctx, item\_code)).

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L2586) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1028) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1004)

<a id="op-92e1ca48737d75"></a>
### Price list rate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_price_list_rate`

**Inputs** rows.

**Explicit results** no value · row.price\_list\_rate when isinstance(row, dict), otherwise row at 1.

**Local steps**

- If not rows.
  - Return no value.
- Set row from rows at 0.
- Return row.price\_list\_rate when isinstance(row, dict), otherwise row at 1.
  - Value choice on isinstance(row, dict) — true gives row.price\_list\_rate, false gives row at 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L2998) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1031) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1007)

<a id="op-2e3046d2270877"></a>
### Create product details script

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_create_product_details_script`

**Inputs** doctype.

**Record and data access** read “CRM Form Script” via exists · read “CRM Form Script” via get\_value · resolve a document from mapping(“doctype” → “CRM Form Script”, “name” → name, “dt” → doctype, “view” → “Form”, …) via get\_doc.

**State and service calls** request set\_value on “CRM Form Script” · call insert on Platform.get\_doc(mapping(“doctype” → “CRM Form Script”, “name” → name, “dt” → doctype, “view” → “Form”, …)).

**Explicit results** no value.

**Local steps**

- Set name from (“Product Details Script for ” + doctype).
- Set script from get\_product\_details\_script(doctype).
- If Platform.db.exists(“CRM Form Script”, name).
  - If Platform.db.get\_value(“CRM Form Script”, name, “script”) differs from script.
    - Evaluate Platform.db.set\_value(“CRM Form Script”, name, “script”, script).
  - Return no value.
- Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Form Script”, “name” → name, “dt” → doctype, “view” → “Form”, …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L3114) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1027) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1003)

<a id="op-8f0e0b8fd7ba77"></a>
### Get product details script

`operation_relationships_fcrm_record_definitions_customer_relationship_management_products_business_behavior_get_product_details_script`

**Inputs** doctype.

**Explicit results** ((doctype\_class + “ {”) + multiline text in the contract).

**Local steps**

- Set doctype\_class from (“class ” + doctype.replace(one space, empty text)).
- Return ((doctype\_class + “ {”) + multiline text in the contract).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L3500) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1029) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1005)

## Record · Crm sales hierarchy

<a id="op-6f9d38266b031c"></a>
### CRMSales Hierarchy.on update

`operation_relationships_fcrm_record_definitions_customer_relationship_management_sales_hierarchy_business_behavior_customer_relationship_sales_hierarchy_on_update`

**Inputs** self.

**Local steps**

- Evaluate update\_nsm(self).
- Evaluate Platform.cache.delete\_value(“crm\_sales\_hierarchy\_subtree”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L6459) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1049) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1025)

<a id="op-26e5b3ed9ffa27"></a>
### CRMSales Hierarchy.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_sales_hierarchy_business_behavior_customer_relationship_sales_hierarchy_validate`

**Inputs** self.

**Record and data access** read “CRM Sales Hierarchy” via get\_value.

**State and service calls** request set\_value on “CRM Sales Hierarchy”.

**Explicit failure paths** validation helper — Platform.\_(“User {0} is already mapped to hierarchy node {1}.”).format(self.user, existing).

**Local steps**

- If self.user.
  - Set existing from Platform.db.get\_value(“CRM Sales Hierarchy”, mapping(“user” → self.user, “name” → list(“!=”, self.name)), “name”).
  - If existing.
    - Call the validation error handler Platform.throw(Platform.\_(“User {0} is already mapped to hierarchy node {1}.”).format(self.user, existing)).
- If (self.reports\_to and not Platform.db.get\_value(“CRM Sales Hierarchy”, self.reports\_to, “is\_group”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reports\_to → not Platform.db.get\_value(“CRM Sales Hierarchy”, self.reports\_to, “is\_group”).
  - Evaluate Platform.db.set\_value(“CRM Sales Hierarchy”, self.reports\_to, “is\_group”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L6539) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1050) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1026)

<a id="op-a371c05aae40ff"></a>
### CRMSales Hierarchy.on trash

`operation_relationships_fcrm_record_definitions_customer_relationship_management_sales_hierarchy_business_behavior_customer_relationship_sales_hierarchy_on_trash`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_value(“crm\_sales\_hierarchy\_subtree”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L6887) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1048) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1024)

<a id="op-0fe25464e62837"></a>
### On doctype update

`operation_relationships_fcrm_record_definitions_customer_relationship_management_sales_hierarchy_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “CRM Sales Hierarchy”.

**Local steps**

- Evaluate Platform.db.add\_index(“CRM Sales Hierarchy”, list(“lft”, “rgt”)).
- Evaluate Platform.db.add\_index(“CRM Sales Hierarchy”, list(“user”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L6945) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1051) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1027)

## Record · Crm service level agreement

<a id="op-8f024d5c8b4635"></a>
### CRMService Level Agreement.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_default().
- Evaluate self.validate\_condition().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate default](operations-007.md#op-8b9a4daa4078bc), [validate condition](operations-007.md#op-9d09ae3c63d355).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0040.json#L7068) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1076) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1052)

<a id="op-8b9a4daa4078bc"></a>
### CRMService Level Agreement.validate default

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_validate_default`

**Inputs** self.

**Record and data access** read “CRM Service Level Agreement” via get\_all.

**Explicit failure paths** validation helper — translated “Default Service Level Agreement already exists for {0}”.format(self.apply\_on).

**Local steps**

- If self.default.
  - Set other\_slas from Platform.get\_all(“CRM Service Level Agreement”, filters = mapping(“apply\_on” → self.apply\_on, “default” → true, “name” → list(“!=”, self.name)), fields = list(“name”)).
  - If other\_slas.
    - Call the validation error handler Platform.throw(translated “Default Service Level Agreement already exists for {0}”.format(self.apply\_on)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1078) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1054)

<a id="op-9d09ae3c63d355"></a>
### CRMService Level Agreement.validate condition

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_validate_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L254) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1077) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1053)

<a id="op-4d92f48b8d5828"></a>
### CRMService Level Agreement.apply

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_apply`

**Inputs** self, doc.

**Local steps**

- Evaluate self.handle\_creation(doc).
- Evaluate self.handle\_communication\_status(doc).
- Evaluate self.handle\_targets(doc).
- Evaluate self.handle\_sla\_status(doc).
- Evaluate self.handle\_rolling\_sla\_status(doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle creation](operations-007.md#op-a28ccc9eb64eea), [handle communication status](operations-007.md#op-3680f32f0e08fb), [handle targets](operations-007.md#op-e790fc3fbcb038), [handle sla status](operations-008.md#op-587315821d584d), [handle rolling sla status](operations-008.md#op-9b84080525ea25).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L486) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1052) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1028)

<a id="op-a28ccc9eb64eea"></a>
### CRMService Level Agreement.handle creation

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_handle_creation`

**Inputs** self, doc.

**Local steps**

- Set doc.sla\_creation from (doc.sla\_creation or now\_datetime()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.sla\_creation → now\_datetime().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L654) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1062) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1038)

<a id="op-3680f32f0e08fb"></a>
### CRMService Level Agreement.handle communication status

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_handle_communication_status`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- If (doc.is\_new() or not doc.has\_value\_changed(“communication\_status”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → not doc.has\_value\_changed(“communication\_status”).
  - Return no value.
- Evaluate self.set\_first\_responded\_on(doc).
- Evaluate self.set\_first\_response\_time(doc).
- If self.rolling\_responses.
  - Evaluate self.set\_rolling\_responses(doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set first responded on](operations-007.md#op-499b820fedf655), [set first response time](operations-007.md#op-800c759914dc66), [set rolling responses](operations-007.md#op-021ff121024000).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L737) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1061) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1037)

<a id="op-499b820fedf655"></a>
### CRMService Level Agreement.set first responded on

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_set_first_responded_on`

**Inputs** self, doc.

**Local steps**

- If doc.communication\_status differs from self.get\_default\_priority().
  - Set doc.first\_responded\_on from (doc.first\_responded\_on or now\_datetime()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.first\_responded\_on → now\_datetime().
  - Set doc.last\_responded\_on from (doc.last\_responded\_on or doc.first\_responded\_on).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.last\_responded\_on → doc.first\_responded\_on.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get default priority](operations-008.md#op-d7f4cb0252e4fa).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L932) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1069) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1045)

<a id="op-800c759914dc66"></a>
### CRMService Level Agreement.set first response time

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_set_first_response_time`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- Set start\_at from doc.sla\_creation.
- Set end\_at from doc.first\_responded\_on.
- If (not start\_at or not end\_at).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not start\_at → not end\_at.
  - Return no value.
- If doc.first\_response\_time is identical to no value.
  - Set doc.first\_response\_time from self.calc\_elapsed\_time(start\_at, end\_at).
- If (doc.last\_response\_time is identical to no value and doc.first\_response\_time is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.last\_response\_time is identical to no value → doc.first\_response\_time is distinct from no value.
  - Set doc.last\_response\_time from doc.first\_response\_time.

If control reaches the end, it returns no value.

**Methods declared on this owner** [calc elapsed time](operations-008.md#op-043fcaf624f32f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L1089) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1070) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1046)

<a id="op-021ff121024000"></a>
### CRMService Level Agreement.set rolling responses

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_set_rolling_responses`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- If (doc.last\_response\_time is identical to no value or not doc.last\_responded\_on).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.last\_response\_time is identical to no value → not doc.last\_responded\_on.
  - Return no value.
- If len(doc.rolling\_responses) equals 0.
  - Evaluate doc.append(“rolling\_responses”, mapping(“response\_time” → doc.last\_response\_time, “responded\_on” → doc.last\_responded\_on, “status” → “Failed” when self.is\_first\_response\_failed(doc), otherwise “Fulfilled”)).
    - Value choice on self.is\_first\_response\_failed(doc) — true gives “Failed”, false gives “Fulfilled”.
- Otherwise.
  - If doc.communication\_status differs from self.get\_default\_priority().
    - Set current\_time from now\_datetime().
    - Set doc.last\_response\_time from self.calc\_elapsed\_time(doc.last\_responded\_on, current\_time).
    - Set doc.last\_responded\_on from current\_time.
    - Set is\_failed from self.is\_rolling\_response\_failed(doc).
    - Evaluate doc.append(“rolling\_responses”, mapping(“response\_time” → doc.last\_response\_time, “responded\_on” → doc.last\_responded\_on, “status” → “Failed” when is\_failed, otherwise “Fulfilled”)).
      - Value choice on is\_failed — true gives “Failed”, false gives “Fulfilled”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is first response failed](operations-008.md#op-de1763303782b1), [get default priority](operations-008.md#op-d7f4cb0252e4fa), [calc elapsed time](operations-008.md#op-043fcaf624f32f), [is rolling response failed](operations-008.md#op-80d01f1c1d88b2).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L1335) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1073) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1049)

<a id="op-e790fc3fbcb038"></a>
### CRMService Level Agreement.handle targets

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_handle_targets`

**Inputs** self, doc.

**Local steps**

- Evaluate self.set\_response\_by(doc).
- If (self.rolling\_responses and len(doc.rolling\_responses) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.rolling\_responses → len(doc.rolling\_responses) &gt; 0.
  - Evaluate self.set\_rolling\_response\_by(doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set response by](operations-007.md#op-43b5c3b0b820f6), [set rolling response by](operations-007.md#op-baa84f6e1796fe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L1836) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1065) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1041)

<a id="op-43b5c3b0b820f6"></a>
### CRMService Level Agreement.set response by

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_set_response_by`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- Set start\_time from doc.sla\_creation.
- Set communication\_status from doc.communication\_status.
- Set priorities from self.get\_priorities().
- Set priority from priorities.get(communication\_status).
- If (not priority or doc.response\_by).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not priority → doc.response\_by.
  - Return no value.
- Set first\_response\_time from priority.get(“first\_response\_time”, 0).
- Set end\_time from self.calc\_time(start\_time, first\_response\_time).
- If end\_time.
  - Set doc.response\_by from end\_time.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get priorities](operations-008.md#op-d0d742c7d28203), [calc time](operations-008.md#op-893dd691820670).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L1982) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1071) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1047)

<a id="op-befd4690714b89"></a>
### CRMService Level Agreement.update rolling response by

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_update_rolling_response_by`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- Set default\_priority from self.get\_default\_priority().
- If doc.communication\_status differs from default\_priority.
  - Return no value.
- Set priorities from self.get\_priorities().
- Set priority from priorities.get(default\_priority).
- If not priority.
  - Return no value.
- Set rolling\_response\_time from priority.get(“first\_response\_time”, 0).
- Set end\_time from self.calc\_time(now\_datetime(), rolling\_response\_time).
- If end\_time.
  - Set doc.response\_by from end\_time.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get default priority](operations-008.md#op-d7f4cb0252e4fa), [get priorities](operations-008.md#op-d0d742c7d28203), [calc time](operations-008.md#op-893dd691820670).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L2249) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1075) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1051)

<a id="op-baa84f6e1796fe"></a>
### CRMService Level Agreement.set rolling response by

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_set_rolling_response_by`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- If (not doc.response\_by or not doc.last\_responded\_on).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.response\_by → not doc.last\_responded\_on.
  - Return no value.
- Evaluate self.\_update\_rolling\_response\_by(doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update rolling response by](operations-007.md#op-befd4690714b89).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L2535) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1072) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1048)
