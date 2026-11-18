# Company and master data · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Default success action

<a id="op-78a5c4da4af0f3"></a>
### Get message

`operation_enterprise_setup_default_success_action_business_behavior_get_message`

**Inputs** doctype.

**Explicit results** translated “{0} has been submitted successfully”.format(doctype).

**Local steps**

- Return translated “{0} has been submitted successfully”.format(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L1947) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L238)

<a id="op-60ee83972687a6"></a>
### Get first success message

`operation_enterprise_setup_default_success_action_business_behavior_get_first_success_message`

**Inputs** doctype.

**Explicit results** get\_message(doctype).

**Local steps**

- Return get\_message(doctype).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L2016) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L237)

<a id="op-b7435b4702161c"></a>
### Get default success action

`operation_enterprise_setup_default_success_action_business_behavior_get_default_success_action`

**Inputs** no declared parameters.

**Explicit results** list of mapping(“doctype” → “Success Action”, “ref\_doctype” → doctype, “message” → get\_message(doctype), “first\_success\_message” → get\_first\_success\_message(doctype), …) for doctype drawn from doctype\_list.

**Local steps**

- Return list of mapping(“doctype” → “Success Action”, “ref\_doctype” → doctype, “message” → get\_message(doctype), “first\_success\_message” → get\_first\_success\_message(doctype), …) for doctype drawn from doctype\_list.
  - Draw doctype from doctype\_list.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L2068) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L236)

## Service · Defaults setup

<a id="op-b0770bc5ba0124"></a>
### Set default settings

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_set_default_settings`

**Inputs** args.

**Record and data access** resolve a document from “Global Defaults” via get\_doc · resolve a document from “System Settings” via get\_doc · resolve a document from “Stock Settings” via get\_doc · resolve a document from “Selling Settings” via get\_doc · resolve a document from “Buying Settings” via get\_doc · 1 additional forms in the steps below.

**State and service calls** request set\_value on “Currency” · call save on global\_defaults · call save on system\_settings · call save on stock\_settings · call save on selling\_settings · 2 additional forms in the steps below.

**Local steps**

- Evaluate Platform.db.set\_value(“Currency”, args.get(“currency”), “enabled”, 1).
- Set global\_defaults from Platform.get\_doc(“Global Defaults”, “Global Defaults”).
- Evaluate global\_defaults.update(mapping(“current\_fiscal\_year” → get\_fy\_details(args.get(“fy\_start\_date”), args.get(“fy\_end\_date”)), “default\_currency” → args.get(“currency”), “default\_company” → args.get(“company\_n ….
- Evaluate global\_defaults.save().
- Set system\_settings from Platform.get\_doc(“System Settings”).
- Set system\_settings.email\_footer\_address from args.get(“company\_name”).
- Evaluate system\_settings.save().
- Set stock\_settings from Platform.get\_doc(“Stock Settings”).
- Set stock\_settings.item\_naming\_by from “Item Code”.
- Set stock\_settings.valuation\_method from “FIFO”.
- Set stock\_settings.stock\_uom from “Nos”.
- Set stock\_settings.auto\_indent from 1.
- Set stock\_settings.auto\_insert\_price\_list\_rate\_if\_missing from 1.
- Set stock\_settings.update\_price\_list\_based\_on from “Rate”.
- Evaluate stock\_settings.save().
- Set selling\_settings from Platform.get\_doc(“Selling Settings”).
- Set selling\_settings.cust\_master\_name from “Customer Name”.
- Set selling\_settings.so\_required from “No”.
- Set selling\_settings.dn\_required from “No”.
- Set selling\_settings.allow\_multiple\_items from 1.
- Set selling\_settings.sales\_update\_frequency from “Daily”.
- Evaluate selling\_settings.save().
- Set buying\_settings from Platform.get\_doc(“Buying Settings”).
- Set buying\_settings.supp\_master\_name from “Supplier Name”.
- Set buying\_settings.po\_required from “No”.
- Set buying\_settings.pr\_required from “No”.
- Set buying\_settings.maintain\_same\_rate from 1.
- Set buying\_settings.allow\_multiple\_items from 1.
- Evaluate buying\_settings.save().
- Set delivery\_settings from Platform.get\_doc(“Delivery Settings”).
- Set delivery\_settings.dispatch\_template from translated “Dispatch Notification”.
- Evaluate delivery\_settings.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L645)

<a id="op-52a577330e9397"></a>
### Set no copy fields in variant settings

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_set_number_copy_fields_in_variant_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Item Variant Settings” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Item Variant Settings”).
- Evaluate doc.set\_default\_fields().
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L4673) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L646)

<a id="op-95e63c8b76c2dc"></a>
### Create price lists

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_create_price_lists`

**Inputs** args.

**Record and data access** resolve a document from mapping(“doctype” → “Price List”, “price\_list\_name” → pl\_name, “enabled” → 1, “buying” → 1 when pl\_type equals “Buying”, otherwise 0, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Price List”, “price\_list\_name” → pl\_name, “enabled” → 1, “buying” → 1 when pl\_type equals “Buying”, otherwise 0, …)).

**Local steps**

- For each tuple(pl\_type, pl\_name) in tuple(tuple(“Selling”, translated “Standard Selling”), tuple(“Buying”, translated “Standard Buying”)).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Price List”, “price\_list\_name” → pl\_name, “enabled” → 1, “buying” → 1 when pl\_type equals “Buying”, otherwise 0, …)).insert().
    - Value choice on pl\_type equals “Buying” — true gives 1, false gives 0.
    - Value choice on pl\_type equals “Selling” — true gives 1, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L4766) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L642)

<a id="op-f7c6bbfad02d4e"></a>
### Create employee for self

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_create_employee_for_self`

**Inputs** args.

**Record and data access** resolve a document from mapping(“doctype” → “Employee”, “employee\_name” → one space.join(filter(no value, list(args.get(“first\_name”), args.get(“last\_name”)))), “user\_id” → Platform.session.user, “status” → “Active”, …) via get\_doc.

**State and service calls** call insert on emp.

**Explicit results** no value.

**Local steps**

- If Platform.session.user equals “Administrator”.
  - Return no value.
- Set emp from Platform.get\_doc(mapping(“doctype” → “Employee”, “employee\_name” → one space.join(filter(no value, list(nested operand in the contract.get(“first\_name”), nested operand in the contract.get(“last\_name”)))), ….
- Set emp.flags.ignore\_mandatory from true.
- Evaluate emp.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L5070) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1099) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L640)

<a id="op-c84046c21df572"></a>
### Create territories

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_create_territories`

**Inputs** no declared parameters.

**Record and data access** read “Territory” via exists · resolve a document from mapping(“doctype” → “Territory”, “territory\_name” → name.replace(“'”, empty text), “parent\_territory” → root\_territory, “is\_group” → “No”) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Territory”, “territory\_name” → name.replace(“'”, empty text), “parent\_territory” → root\_territory, “is\_group” → “No”)).

**Local steps**

- Bind dependencies get\_root\_of.
- Set country from Platform.db.get\_default(“country”).
- Set root\_territory from get\_root\_of(“Territory”).
- For each name in tuple(country, translated “Rest Of The World”).
  - If (name and not Platform.db.exists(“Territory”, name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in name → not Platform.db.exists(“Territory”, name).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “Territory”, “territory\_name” → name.replace(“'”, empty text), “parent\_territory” → root\_territory, “is\_group” → “No”)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L5410) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L643)

<a id="op-787dda2466d0e2"></a>
### Create feed and todo

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_create_feed_and_todo`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L5727) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L641)

<a id="op-7a74a503ab8ccb"></a>
### Get fy details

`operation_enterprise_setup_setup_wizard_operations_defaults_setup_business_behavior_get_financial_year_details`

**Inputs** fy\_start\_date, fy\_end\_date.

**Explicit results** fy.

**Local steps**

- Set start\_year from getdate(fy\_start\_date).year.
- If start\_year equals getdate(fy\_end\_date).year.
  - Set fy from cstr(start\_year).
- Otherwise.
  - Set fy from ((cstr(start\_year) + “-”) + cstr((start\_year + 1))).
- Return fy.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L5755) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L644)

## Service · Demo

<a id="op-0b85202e085c02"></a>
### Clear demo data

`operation_enterprise_setup_demo_business_behavior_clear_demo_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Global Defaults” via get\_single\_value.

**State and service calls** rollback.

**Explicit failure paths** validation helper — translated “Failed to erase demo data, please delete the demo company manually.”.

**Local steps**

- Bind dependencies capture.
- Evaluate Platform.only\_for(“System Manager”).
- Evaluate capture(“demo\_data\_erased”, “Enterprise”).
- Attempt the following.
  - Set company from Platform.db.get\_single\_value(“Global Defaults”, “demo\_company”).
  - Evaluate create\_transaction\_deletion\_record(company).
  - Evaluate clear\_masters().
  - Evaluate delete\_company(company).
  - Set default\_company from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).
  - Evaluate Platform.db.set\_default(“company”, default\_company).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(“Failed to erase demo data”).
  - Call the validation error handler Platform.throw(translated “Failed to erase demo data, please delete the demo company manually.”, title = translated “Could Not Delete Demo Data”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “demo\_company”), Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L2864) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L239)

<a id="op-3d1c77db8e4457"></a>
### Create transaction deletion record

`operation_enterprise_setup_demo_business_behavior_create_transaction_deletion_record`

**Inputs** company.

**State and service calls** request new\_doc for “Transaction Deletion Record” · call save on transaction\_deletion\_record · call submit on transaction\_deletion\_record.

**Local steps**

- Set transaction\_deletion\_record from Platform.new\_doc(“Transaction Deletion Record”).
- Set transaction\_deletion\_record.company from company.
- Set transaction\_deletion\_record.process\_in\_single\_transaction from true.
- Evaluate transaction\_deletion\_record.save(ignore\_permissions = true).
- Evaluate transaction\_deletion\_record.generate\_to\_delete\_list().
- Evaluate transaction\_deletion\_record.reload().
- Evaluate transaction\_deletion\_record.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L242)

<a id="op-5d0f60c43a0426"></a>
### Clear masters

`operation_enterprise_setup_demo_business_behavior_clear_masters`

**Inputs** no declared parameters.

**Local steps**

- For each doctype in Platform.get\_hooks(“demo\_master\_doctypes”) at slice no value to no value with step negative 1.
  - Set data from read\_data\_file\_using\_hooks(doctype).
  - If data.
    - For each item in json.loads(data).
      - Evaluate clear\_demo\_record(item).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“demo\_master\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L5879) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L241)

<a id="op-c094e85cf9bdf8"></a>
### Clear demo record

`operation_enterprise_setup_demo_business_behavior_clear_demo_record`

**Inputs** document.

**Record and data access** resolve a document from document\_type via get\_doc.

**Local steps**

- Set document\_type from document.get(“doctype”).
- Remove document at “doctype”.
- Set valid\_columns from Platform.get\_meta(document\_type).get\_valid\_columns().
- Set filters from document.
- For each key in list(filters).
  - If key does not belong to valid\_columns.
    - Evaluate filters.pop(key, no value).
- Attempt the following.
  - Set doc from Platform.get\_doc(document\_type, filters).
  - Evaluate doc.delete(ignore\_permissions = true).
- On failure (Platform.exceptions.DoesNotExistError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L6045) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L240)

<a id="op-6b597c6c3a9bb0"></a>
### Delete company

`operation_enterprise_setup_demo_business_behavior_delete_company`

**Inputs** company.

**State and service calls** request set\_single\_value on “Global Defaults” · request delete\_doc for “Company”.

**Local steps**

- Evaluate Platform.db.set\_single\_value(“Global Defaults”, “demo\_company”, empty text).
- Evaluate Platform.delete\_doc(“Company”, company, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L6351) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L243)

<a id="op-66442dcd113244"></a>
### Read data file using hooks

`operation_enterprise_setup_demo_business_behavior_read_data_file_using_hooks`

**Inputs** doctype.

**Explicit results** data.

**Local steps**

- Set path from os.path.join(os.path.dirname(\_\_file\_\_), “demo\_data”).
- Within open(os.path.join(path, (doctype + “.json”))) bound as f.
  - Set data from f.read().
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0680.json#L6473) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L244)

## Record · Department

[Record definition](../../../../data/record-types/department.json)

<a id="op-67bedcd18564fd"></a>
### Department.autoname

`operation_enterprise_setup_record_definitions_department_business_behavior_department_autoname`

**Inputs** self.

**Local steps**

- If self.company.
  - Set self.name from get\_abbreviated\_name(self.department\_name, self.company).
- Otherwise.
  - Set self.name from self.department\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L1656) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L793) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L351)

<a id="op-bc6783af456f16"></a>
### Department.validate

`operation_enterprise_setup_record_definitions_department_business_behavior_department_validate`

**Inputs** self.

**Record and data access** read “Department” via get\_value.

**Explicit failure paths** validation helper — translated “Department company cannot be changed” · validation helper — translated “Parent Department must be a group” · validation helper — translated “Parent Department must belong to the same company”.

**Local steps**

- If (not self.is\_new() and self.has\_value\_changed(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“company”).
  - Call the validation error handler Platform.throw(translated “Department company cannot be changed”).
- If not self.parent\_department.
  - Set root from get\_root\_of(“Department”).
  - If root.
    - Set self.parent\_department from root.
- If self.parent\_department.
  - Set parent from Platform.db.get\_value(“Department”, self.parent\_department, list(“company”, “is\_group”), as\_dict = true).
  - If (parent and not parent.is\_group).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → not parent.is\_group.
    - Call the validation error handler Platform.throw(translated “Parent Department must be a group”).
  - If (parent and parent.company and parent.company differs from self.company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → parent.company → parent.company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Parent Department must belong to the same company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L797) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L355)

<a id="op-7fd456b94519ad"></a>
### Department.before rename

`operation_enterprise_setup_record_definitions_department_business_behavior_department_before_rename`

**Inputs** self, old, new, merge = false.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** new.

**Local steps**

- If not new.endswith(formatted text  - {Platform.get\_cached\_value(“Company”, self.company, “abbr”)}).
  - Set new from get\_abbreviated\_name(new, self.company).
- Return new.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “abbr”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L794) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L352)

<a id="op-32568c134d605d"></a>
### Department.on update

`operation_enterprise_setup_record_definitions_department_business_behavior_department_on_update`

**Inputs** self.

**Local steps**

- If not (Platform.local.flags.ignore\_update\_nsm or Platform.flags.in\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.ignore\_update\_nsm → Platform.flags.in\_setup\_wizard.
  - Evaluate super().on\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L2037) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L354)

<a id="op-6c454382e31d0e"></a>
### Department.on trash

`operation_enterprise_setup_record_definitions_department_business_behavior_department_on_trash`

**Inputs** self.

**Local steps**

- Evaluate super().on\_trash().
- Evaluate delete\_events(self.doctype, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L2137) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L795) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L353)

<a id="op-42e6b2ed295730"></a>
### On doctype update

`operation_enterprise_setup_record_definitions_department_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Department”.

**Local steps**

- Evaluate Platform.db.add\_index(“Department”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L2229) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L800) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L358)

<a id="op-012e4fbce6132c"></a>
### Get abbreviated name

`operation_enterprise_setup_record_definitions_department_business_behavior_get_abbreviated_name`

**Inputs** name, company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** new\_name.

**Local steps**

- Set abbr from Platform.get\_cached\_value(“Company”, company, “abbr”).
- Set new\_name from formatted text {name} - {abbr}.
- Return new\_name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “abbr”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L2307) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L356)

<a id="op-3c198eb1dfdf11"></a>
### Get children

`operation_enterprise_setup_record_definitions_department_business_behavior_get_children`

**Inputs** doctype, parent = no value, company = no value, is\_root = false, include\_disabled = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Department” via get\_list.

**Explicit results** Platform.get\_list(“Department”, fields = fields, filters = filters, order\_by = “name”).

**Local steps**

- If isinstance(include\_disabled, str).
  - Set include\_disabled from json.loads(include\_disabled).
- Set fields from list(“name as value”, “is\_group as expandable”).
- Set filters from mapping().
- If company equals parent.
  - Set filters at “name” from get\_root\_of(“Department”).
- Otherwise.
  - If company.
    - Set filters at “parent\_department” from parent.
    - Set filters at “company” from company.
  - Otherwise.
    - Set filters at “parent\_department” from parent.
- If (Platform.db.has\_column(“Department”, “disabled”) and not include\_disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.has\_column(“Department”, “disabled”) → not include\_disabled.
  - Set filters at “disabled” from false.
- Return Platform.get\_list(“Department”, fields = fields, filters = filters, order\_by = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L357)
