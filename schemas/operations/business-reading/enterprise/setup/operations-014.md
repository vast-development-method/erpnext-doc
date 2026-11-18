# Company and master data · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Taxes setup

<a id="op-160e6c2972f021"></a>
### Make item tax template

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_make_item_tax_template`

**Inputs** company\_name, template.

**Record and data access** read doctype via exists · resolve a document from template via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** no value · doc.

**Local steps**

- Set doctype from “Item Tax Template”.
- Set template at “company” from company\_name.
- Set template at “doctype” from doctype.
- If Platform.db.exists(doctype, mapping(“title” → template.get(“title”), “company” → company\_name)).
  - Return no value.
- For each tax\_row in template.get(“taxes”).
  - Set account\_data from tax\_row.get(“tax\_type”).
  - If isinstance(account\_data, dict).
    - Set account from get\_or\_create\_account(company\_name, account\_data).
    - Set tax\_row at “tax\_type” from account.name.
    - If “tax\_rate” does not belong to tax\_row.
      - Set tax\_row at “tax\_rate” from account\_data.get(“tax\_rate”).
- Set doc from Platform.get\_doc(template).
- Set doc.flags.ignore\_links from true.
- Set doc.flags.ignore\_validate from true.
- Evaluate doc.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L1207) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L666)

<a id="op-8924a1ce95c8db"></a>
### Get or create account

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_get_or_create_account`

**Inputs** company\_name, account.

**Record and data access** read “Account” via get\_all · resolve a document from “Account” via get\_doc · resolve a document from account via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** Platform.get\_doc(“Account”, existing\_accounts at 0.name) · doc.

**Local steps**

- Set default\_root\_type from “Liability”.
- Set root\_type from account.get(“root\_type”, default\_root\_type).
- Set or\_filters from mapping(“account\_name” → account.get(“account\_name”)).
- If account.get(“account\_number”).
  - Evaluate or\_filters.update(mapping(“account\_number” → account.get(“account\_number”))).
- Set existing\_accounts from Platform.get\_all(“Account”, filters = mapping(“company” → company\_name, “root\_type” → root\_type), or\_filters = or\_filters).
- If existing\_accounts.
  - Return Platform.get\_doc(“Account”, existing\_accounts at 0.name).
- Set tax\_group from get\_or\_create\_tax\_group(company\_name, root\_type).
- Set account at “doctype” from “Account”.
- Set account at “company” from company\_name.
- Set account at “parent\_account” from tax\_group.
- Set account at “report\_type” from “Balance Sheet”.
- Set account at “account\_type” from “Tax”.
- Set account at “root\_type” from root\_type.
- Set account at “is\_group” from 0.
- Set doc from Platform.get\_doc(account).
- Set doc.flags.ignore\_links from true.
- Set doc.flags.ignore\_validate from true.
- Evaluate doc.insert(ignore\_permissions = true, ignore\_mandatory = true, ignore\_if\_duplicate = true).
- Return doc.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L1753) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L664)

<a id="op-5a3cca25c74cfd"></a>
### Get or create tax group

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_get_or_create_tax_group`

**Inputs** company\_name, root\_type.

**Record and data access** read “Account” via get\_value · read “Account” via get\_all · resolve a document from mapping(“doctype” → “Account”, “company” → company\_name, “is\_group” → 1, “report\_type” → “Balance Sheet”, …) via get\_doc.

**State and service calls** call insert on tax\_group\_account.

**Explicit results** tax\_group\_name.

**Local steps**

- Set tax\_group\_name from Platform.db.get\_value(“Account”, mapping(“is\_group” → 1, “root\_type” → root\_type, “account\_type” → “Tax”, “company” → company\_name)).
- If tax\_group\_name.
  - Return tax\_group\_name.
- Set account\_name from translated “Duties and Taxes” when root\_type equals “Liability”, otherwise translated “Tax Assets”.
  - Value choice on root\_type equals “Liability” — true gives translated “Duties and Taxes”, false gives translated “Tax Assets”.
- Set tax\_group\_name from Platform.db.get\_value(“Account”, mapping(“is\_group” → 1, “root\_type” → root\_type, “account\_name” → account\_name, “company” → company\_name)).
- If tax\_group\_name.
  - Return tax\_group\_name.
- Set root\_account from Platform.get\_all(“Account”, mapping(“is\_group” → 1, “root\_type” → root\_type, “company” → company\_name, “report\_type” → “Balance Sheet”, …), limit = 1) at 0.
- Set tax\_group\_account from Platform.get\_doc(mapping(“doctype” → “Account”, “company” → company\_name, “is\_group” → 1, “report\_type” → “Balance Sheet”, …)).
- Set tax\_group\_account.flags.ignore\_links from true.
- Set tax\_group\_account.flags.ignore\_validate from true.
- Evaluate tax\_group\_account.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
- Set tax\_group\_name from tax\_group\_account.name.
- Return tax\_group\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L2460) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L665)

<a id="op-896c64e74559e0"></a>
### Make tax category

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_make_tax_category`

**Inputs** tax\_category.

**Record and data access** read doctype via exists · resolve a document from tax\_category via get\_doc.

**State and service calls** call insert on doc.

**Local steps**

- Set doctype from “Tax Category”.
- If isinstance(tax\_category, str).
  - Set tax\_category from mapping(“title” → tax\_category).
- Set tax\_category at “doctype” from doctype.
- If not Platform.db.exists(doctype, tax\_category at “title”).
  - Set doc from Platform.get\_doc(tax\_category).
  - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L3230) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L667)

## Record · Terms and conditions

[Record definition](../../../../data/record-types/terms_and_conditions.json)

<a id="op-c100599154668d"></a>
### Termsand Conditions.validate

`operation_enterprise_setup_record_definitions_terms_and_conditions_business_behavior_termsand_conditions_validate`

**Inputs** self.

**Local steps**

- If self.terms.
  - Evaluate validate\_template(self.terms, restrict\_globals = true).
  - Evaluate validate\_terms\_globals(self.terms).
- If (not cint(self.disabled) and not any(generator of cint(nested operand in the contract.get(module)) for module drawn from tuple(“buying”, “selling”, “hr”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.disabled) → not any(generator of cint(self.get(module)) for module drawn from tuple(“buying”, “selling”, “hr”)).
  - Draw module from tuple(“buying”, “selling”, “hr”).
  - Evaluate throw(translated “At least one of the Applicable Modules should be selected”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L545)

<a id="op-31632eeed9f0c1"></a>
### Get terms and conditions

`operation_enterprise_setup_record_definitions_terms_and_conditions_business_behavior_get_terms_and_conditions`

**Inputs** template\_name, doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Terms and Conditions” via get\_cached\_doc.

**Explicit results** no value · get\_terms\_environment(tnc.modified\_by).from\_string(tnc.terms).render(doc).

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Set tnc from Platform.get\_cached\_doc(“Terms and Conditions”, template\_name).
- Evaluate tnc.check\_permission().
- Evaluate validate\_terms\_and\_conditions(template\_name, get\_terms\_module(doc)).
- If not tnc.terms.
  - Return no value.
- If “.\_\_” belongs to tnc.terms.
  - Evaluate throw(translated “Illegal template”).
- Within safe\_render\_flags().
  - Return get\_terms\_environment(tnc.modified\_by).from\_string(tnc.terms).render(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Terms and Conditions”, template\_name) · effective access from tnc.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L544)

<a id="op-ef9d088c1dfe4a"></a>
### Get terms environment

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_get_terms_environment`

**Inputs** author.

**Explicit results** jenv.

**Local steps**

- Set jenv from SandboxedEnvironment(undefined = DebugUndefined).
- Evaluate set\_filters(jenv).
- Bind local operation get\_list for subsequent calls.
- Evaluate jenv.globals.update(\_ = Platform.\_, Platform = dict(format = format\_terms\_value, format\_value = format\_terms\_value, format\_date = Platform.utils.global\_date\_format, bold = Platform.bold, …)).
  - Draw name from tuple(“cint”, “cstr”, “flt”, “fmt\_money”, …).
- Return jenv.

**Values supplied outside this operation** selected callable from getattr(Platform.utils, name).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L169)

<a id="op-105aa30ce1402a"></a>
### Get terms environment.get list

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_get_terms_environment_get_list`

**Inputs** doctype, filters = no value, fields = no value, order\_by = no value, limit\_page\_length = 20.

**Explicit results** get\_terms\_list(author, doctype, filters, fields, …).

**Local steps**

- Return get\_terms\_list(author, doctype, filters, fields, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L170)

<a id="op-f3395a0add4f16"></a>
### Validate terms globals

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_validate_terms_globals`

**Inputs** terms.

**Local steps**

- Set jenv from get\_terms\_environment(no value).
- For each node in jenv.parse(terms).find\_all(nodes.Getattr).
  - Set path from get\_attribute\_path(node).
  - If (path and path at 0 equals “Platform” and not has\_global(jenv.globals, path)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in path → path at 0 equals “Platform” → not has\_global(jenv.globals, path).
    - Evaluate throw(translated “{0} cannot be used in Terms and Conditions”.format(Platform.bold(“.”.join(path)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L175)

<a id="op-b279030e427a9b"></a>
### Get attribute path

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_get_attribute_path`

**Inputs** node.

**State and service calls** call insert on path.

**Explicit results** list(node.name, expanded path) when isinstance(node, nodes.Name), otherwise no value.

**Local steps**

- Set path from list().
- While isinstance(node, nodes.Getattr).
  - Evaluate path.insert(0, node.attr).
  - Set node from node.node.
- Return list(node.name, expanded path) when isinstance(node, nodes.Name), otherwise no value.
  - Value choice on isinstance(node, nodes.Name) — true gives list(node.name, expanded path), false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L168)

<a id="op-b01d6c5c08bad9"></a>
### Has global

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_has_global`

**Inputs** jenv\_globals, path.

**Explicit results** true · false.

**Local steps**

- Set value from jenv\_globals.
- For each name in path.
  - If not isinstance(value, dict).
    - Return true.
  - If name does not belong to value.
    - Return false.
  - Set value from value at name.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L173)

<a id="op-1770b66740f00d"></a>
### Format terms value

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_format_terms_value`

**Inputs** value, df = no value, doc = no value, currency = no value, translated = false, format = no value.

**Explicit results** Platform.format\_value(value, df = df, currency = currency, translated = translated, format = format).

**Local steps**

- Return Platform.format\_value(value, df = df, currency = currency, translated = translated, format = format).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L167)

<a id="op-25ea64c2b7ead0"></a>
### Get terms list

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_get_terms_list`

**Inputs** author, doctype, filters = no value, fields = no value, order\_by = no value, limit\_page\_length = 20.

**Record and data access** read doctype via get\_list.

**Explicit results** query.where(nested operand in the contract(nested operand in the contract).name.isin(author\_query)).run(as\_dict = true).

**Local steps**

- Set author from (author or “Guest”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in author → “Guest”.
- Evaluate Platform.has\_permission(doctype, “read”, user = author, throw = true).
- Evaluate Platform.has\_permission(doctype, “read”, throw = true).
- Set permitted\_fields from (set(get\_permitted\_fields(doctype, user = author, permission\_type = “read”)) bitwise and set(get\_permitted\_fields(doctype, permission\_type = “read”))).
- Set meta from Platform.get\_meta(doctype).
- Update permitted\_fields using − set of df.fieldname for df drawn from meta.fields where df.get(“mask”).
  - Draw df from meta.fields, keep a combination only if (df.get(“mask”)).
- Update permitted\_fields using − set of df.fieldname for df drawn from meta.fields where df.fieldtype equals “Password”.
  - Draw df from meta.fields, keep a combination only if (df.fieldtype equals “Password”).
- Set fields from (fields or list(“name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields → list(“name”).
- If isinstance(fields, str).
  - Set fields from list(fields).
- If not isinstance(filters, (dict bitwise or type(no value))).
  - Evaluate throw(translated “Terms and Conditions queries require dictionary filters”, Platform.PermissionError).
- If fields equals list(“\*”).
  - Set fields from sorted(permitted\_fields).
- Set query\_fields from (set(fields) bitwise or set((filters or mapping()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If order\_by.
  - For each clause in order\_by.split(“,”).
    - Set parts from clause.strip().split().
    - If (len(parts) does not belong to tuple(1, 2) or (len(parts) equals 2 and parts at 1.lower() does not belong to tuple(“asc”, “desc”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(parts) does not belong to tuple(1, 2) → (len(parts) equals 2 and parts at 1.lower() does not belong to tuple(“asc”, “desc”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(parts) equals 2 → parts at 1.lower() does not belong to tuple(“asc”, “desc”).
      - Evaluate throw(translated “Invalid Terms and Conditions query order”, Platform.PermissionError).
    - Evaluate query\_fields.add(parts at 0).
- If not query\_fields.issubset(permitted\_fields).
  - Evaluate throw(translated “Not permitted to query these fields in Terms and Conditions”, Platform.PermissionError).
- Set author\_query from Platform.get\_list(doctype, fields = list(“name”), user = author, order\_by = empty text, limit\_page\_length = 0, …).
- Set query from Platform.get\_list(doctype, fields = fields, filters = filters, order\_by = order\_by, limit\_page\_length = limit\_page\_length, …).
- Return query.where(nested operand in the contract(nested operand in the contract).name.isin(author\_query)).run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, user = author, throw = true), Platform.has\_permission(doctype, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L171)

<a id="op-cde66292eaf87c"></a>
### Validate terms and conditions

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_validate_terms_and_conditions`

**Inputs** template\_name, module = no value.

**Record and data access** resolve a document from “Terms and Conditions” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If not template\_name.
  - Return no value.
- Set tnc from Platform.get\_cached\_doc(“Terms and Conditions”, template\_name).
- If cint(tnc.disabled).
  - Evaluate throw(translated “Terms and Conditions {0} is disabled”.format(Platform.bold(template\_name))).
- If (module and not cint(tnc.get(module))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in module → not cint(tnc.get(module)).
  - Evaluate throw(translated “Terms and Conditions {0} is not applicable to {1}”.format(Platform.bold(template\_name), translated “Selling” when module equals “selling”, otherwise translated “Buying”)).
    - Value choice on module equals “selling” — true gives translated “Selling”, false gives translated “Buying”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Terms and Conditions”, template\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L174)

<a id="op-2509ded1a00748"></a>
### Clear inapplicable terms

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_clear_inapplicable_terms`

**Inputs** doc.

**Record and data access** read “Terms and Conditions” via get\_cached\_value.

**Local steps**

- Set module from get\_terms\_module(doc).
- Set tc\_name from doc.get(“tc\_name”).
- If (module and tc\_name and not cint(Platform.get\_cached\_value(“Terms and Conditions”, tc\_name, module))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in module → tc\_name → not cint(Platform.get\_cached\_value(“Terms and Conditions”, tc\_name, module)).
  - Set doc.tc\_name from no value.
  - Set doc.terms from no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Terms and Conditions”, tc\_name, module).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L166)

<a id="op-1629e51d85b6d3"></a>
### Get terms module

`operation_enterprise_binding_enterprise_setup_doctype_terms_and_conditions_terms_and_conditions_get_terms_module`

**Inputs** doc.

**Explicit results** “selling” · “buying” · “selling” when doc.get(“blanket\_order\_type”) equals “Selling”, otherwise “buying”.

**Local steps**

- Set doctype from doc.get(“doctype”).
- If doctype belongs to tuple(“Quotation”, “Sales Order”, “Delivery Note”, “Sales Invoice”, …).
  - Return “selling”.
- If doctype belongs to tuple(“Supplier Quotation”, “Purchase Order”, “Purchase Receipt”, “Purchase Invoice”, …).
  - Return “buying”.
- If doctype equals “Blanket Order”.
  - Return “selling” when doc.get(“blanket\_order\_type”) equals “Selling”, otherwise “buying”.
    - Value choice on doc.get(“blanket\_order\_type”) equals “Selling” — true gives “selling”, false gives “buying”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L172)

## Record · Territory

[Record definition](../../../../data/record-types/territory.json)

<a id="op-d215c8e006fc1d"></a>
### Territory.validate

`operation_enterprise_setup_record_definitions_territory_business_behavior_territory_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Either target qty or target amount is mandatory”.

**Local steps**

- Evaluate validate\_targets(self.get(“targets”)).
- Evaluate set\_root\_as\_default\_parent(self).
- For each d in (self.get(“targets”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“targets”) → list().
  - If (not flt(d.target\_qty) and not flt(d.target\_amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(d.target\_qty) → not flt(d.target\_amount).
    - Call the validation error handler Platform.throw(translated “Either target qty or target amount is mandatory”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L548)

<a id="op-5f4c1881ce37a3"></a>
### Territory.on update

`operation_enterprise_setup_record_definitions_territory_business_behavior_territory_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().
- Evaluate self.validate\_one\_root().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0696.json#L914) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L547)

<a id="op-28e580e6f694bb"></a>
### On doctype update

`operation_enterprise_setup_record_definitions_territory_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Territory”.

**Local steps**

- Evaluate Platform.db.add\_index(“Territory”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0696.json#L988) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L546)

## Record · Transaction deletion record

[Record definition](../../../../data/record-types/transaction_deletion_record.json)

<a id="op-9831fcf1fa6018"></a>
### Get protected doctypes

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_get_protected_record_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_protected\_doctypes\_internal().

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Return \_get\_protected\_doctypes\_internal().

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1004) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L552)

<a id="op-cf4b43eff03a46"></a>
### Get company link fields

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_get_company_link_fields`

**Inputs** doctype\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via exists.

**Explicit results** list() · list of field.fieldname for field drawn from Platform.get\_meta(doctype\_name).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Company”)).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If (not doctype\_name or not Platform.db.exists(“DocType”, doctype\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype\_name → not Platform.db.exists(“DocType”, doctype\_name).
  - Return list().
- Return list of field.fieldname for field drawn from Platform.get\_meta(doctype\_name).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Company”)).
  - Draw field from Platform.get\_meta(doctype\_name).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Company”)).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1003) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L551)

<a id="op-7f9d913e8e55af"></a>
### Get protected doctypes internal

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_get_protected_record_types_internal`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via exists · read “DocType” via get\_all.

**Explicit results** protected.

**Local steps**

- Set protected from list().
- For each doctype in PROTECTED\_CORE\_DOCTYPES.
  - If Platform.db.exists(“DocType”, doctype).
    - Evaluate protected.append(doctype).
- Set singles from Platform.get\_all(“DocType”, filters = mapping(“issingle” → 1), pluck = “name”).
- Evaluate protected.extend(singles).
- Return protected.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L486) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1005) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L553)

<a id="op-8e4fdbdd1f06e8"></a>
### Transaction Deletion Record.initialize

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.batch\_size from 5000.
- Set self.task\_to\_internal\_method\_map from OrderedDict(mapping(“Delete Leads and Addresses” → “delete\_lead\_addresses”, “Reset Company Values” → “reset\_company\_values”, “Clear Notifications” → “delete\_notifications”, “Initialize Summary Table” → “in ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1039) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L586)

<a id="op-f8ff48ebe8ba21"></a>
### Transaction Deletion Record.on discard

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L903) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1043) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L590)
