# Accounting and settlement · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Financial report template

[Record definition](../../../../data/record-types/financial_report_template.json)

<a id="op-2e89f530f37526"></a>
### Financial Report Template.clear hidden fields

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_clear_hidden_fields`

**Inputs** self.

**Local steps**

- Set style\_data\_sources from set(“Blank Line”, “Column Break”, “Section Break”).
- For each row in self.rows.
  - If row.data\_source differs from “Account Data”.
    - Set row.balance\_type from no value.
  - If row.data\_source belongs to style\_data\_sources.
    - Set row.calculation\_formula from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L4701) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L847) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L796)

<a id="op-94fbb933809944"></a>
### Financial Report Template.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_validate`

**Inputs** self.

**Local steps**

- Set validator from TemplateValidator(self).
- Set result from validator.validate().
- Evaluate result.notify\_user().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L4860) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L802)

<a id="op-b2815075feaaa1"></a>
### Financial Report Template.on update

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.\_export\_template().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export template](operations-043.md#op-467c51c2ae8c96).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L4958) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L801)

<a id="op-03acf63e66786a"></a>
### Financial Report Template.on trash

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.\_delete\_template().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete template](operations-043.md#op-0fab73ccb753ae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L5009) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L800)

<a id="op-467c51c2ae8c96"></a>
### Financial Report Template.export template

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_export_template`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies export\_module\_json.
- If not self.module.
  - Return no value.
- Evaluate export\_module\_json(self, true, self.module).
- Evaluate self.\_export\_account\_categories().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export account categories](operations-043.md#op-78cf769d151393).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L5060) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L799)

<a id="op-0fab73ccb753ae"></a>
### Financial Report Template.delete template

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_delete_template`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.module or not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.module → not Platform.conf.developer\_mode.
  - Return no value.
- Set module\_path from Platform.get\_module\_path(self.module).
- Set dir\_path from os.path.join(module\_path, “financial\_report\_template”, Platform.scrub(self.name)).
- Evaluate shutil.rmtree(dir\_path, ignore\_errors = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L5177) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L848) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L797)

<a id="op-78cf769d151393"></a>
### Financial Report Template.export account categories

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_financial_report_template_export_account_categories`

**Inputs** self.

**Record and data access** read “Account Category” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies json.
- Bind dependencies FormulaFieldExtractor.
- If (not self.module or not Platform.conf.developer\_mode or Platform.flags.in\_import).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.module → not Platform.conf.developer\_mode → Platform.flags.in\_import.
  - Return no value.
- Set extractor from FormulaFieldExtractor(field\_name = “account\_category”, exclude\_operators = list(“like”, “not like”)).
- Set account\_data\_rows from list of row for row drawn from self.rows where row.data\_source equals “Account Data”.
  - Draw row from self.rows, keep a combination only if (row.data\_source equals “Account Data”).
- Set category\_names from extractor.extract\_from\_rows(account\_data\_rows).
- If not category\_names.
  - Return no value.
- Set module\_path from Platform.get\_module\_path(self.module).
- Set categories\_file from os.path.join(module\_path, “financial\_report\_template”, “account\_categories.json”).
- Set existing\_categories from mapping().
- If os.path.exists(categories\_file).
  - Attempt the following.
    - Within open(categories\_file) bound as f.
      - Set existing\_data from json.load(f).
      - Set existing\_categories from mapping of cat at “account\_category\_name” → cat for cat drawn from existing\_data.
        - Draw cat from existing\_data.
  - On failure (tuple(json.JSONDecodeError, KeyError)).
    - Take no action here.
- If category\_names.
  - Set db\_categories from Platform.get\_all(“Account Category”, filters = mapping(“account\_category\_name” → list(“in”, list(category\_names))), fields = list(“account\_category\_name”, “description”)).
  - For each cat in db\_categories.
    - Set existing\_categories at cat at “account\_category\_name” from cat.
- Set sorted\_categories from sorted(existing\_categories.values(), key = deferred anonymous expression).
- Evaluate os.makedirs(os.path.dirname(categories\_file), exist\_ok = true).
- Within open(categories\_file, “w”) bound as f.
  - Evaluate json.dump(sorted\_categories, f, indent = 2).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L5386) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L849) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L798)

<a id="op-8ea64fab2c29b4"></a>
### Sync financial report templates

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_sync_financial_report_templates`

**Inputs** chart\_of\_accounts = no value, existing\_company = no value.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_chart.
- If existing\_company.
  - Return no value.
- Set disable\_default\_financial\_report\_template from false.
- If chart\_of\_accounts.
  - Set coa from get\_chart(chart\_of\_accounts).
  - If coa.get(“disable\_default\_financial\_report\_template”, false).
    - Set disable\_default\_financial\_report\_template from true.
- Set installed\_apps from Platform.get\_installed\_apps().
- For each app in installed\_apps.
  - If (disable\_default\_financial\_report\_template and app equals “Enterprise”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in disable\_default\_financial\_report\_template → app equals “Enterprise”.
    - Continue with the next iteration or loop test.
  - Evaluate \_sync\_templates\_for(app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L6275) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L803)

<a id="op-a57f1c8474c274"></a>
### Sync templates for

`operation_enterprise_accounts_record_definitions_financial_report_template_business_behavior_sync_templates_for`

**Inputs** app\_name.

**Record and data access** read “Financial Report Template” via exists · resolve a document from template\_data via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** no value.

**Local steps**

- Set templates from list().
- For each module\_name in (Platform.local.app\_modules.get(app\_name) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.app\_modules.get(app\_name) → list().
  - Set module\_path from Platform.get\_module\_path(module\_name).
  - Set template\_path from os.path.join(module\_path, “financial\_report\_template”).
  - If not os.path.isdir(template\_path).
    - Continue with the next iteration or loop test.
  - Evaluate import\_account\_categories(template\_path).
  - For each template\_dir in os.listdir(template\_path).
    - Set json\_file from os.path.join(template\_path, template\_dir, formatted text {template\_dir}.json).
    - If os.path.isfile(json\_file).
      - Evaluate templates.append(json\_file).
- If not templates.
  - Return no value.
- Set Platform.flags.in\_import from true.
- For each template\_path in templates.
  - Within open(template\_path) bound as f.
    - Set template\_data from Platform.\_dict(Platform.parse\_json(f.read())).
  - Set template\_name from template\_data.get(“name”).
  - If not Platform.db.exists(“Financial Report Template”, template\_name).
    - Set doc from Platform.get\_doc(template\_data).
    - Set doc.flags.ignore\_mandatory from true.
    - Set doc.flags.ignore\_permissions from true.
    - Set doc.flags.ignore\_validate from true.
    - Evaluate doc.insert().
- Set Platform.flags.in\_import from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L6532) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L804)

<a id="op-630d35e298618c"></a>
### Get valid api method

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_get_valid_application_programming_interface_method`

**Inputs** api\_path.

**Explicit results** method.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Method {0} must permit GET requests”.format(Platform.bold(api\_path)).

**Local steps**

- Set method from Platform.get\_attr(api\_path).
- Evaluate is\_whitelisted(method).
- If “GET” does not belong to Platform.allowed\_http\_methods\_for\_whitelisted\_func.get(method, tuple()).
  - Call the validation error handler Platform.throw(translated “Method {0} must permit GET requests”.format(Platform.bold(api\_path)), Platform.PermissionError, title = translated “Method Not Allowed”).
- Return method.

**Values supplied outside this operation** selected callable from Platform.get\_attr(api\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L7240) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L942)

<a id="op-1feca81d498431"></a>
### Get formula field label

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_get_formula_field_label`

**Inputs** data\_source.

**Declared result** str.

**Explicit results** labels.get(data\_source, translated “Calculation Formula”).

**Local steps**

- Set labels from mapping(“Account Data” → translated “Account Filter”, “Custom API” → translated “API Method Path”).
- Return labels.get(data\_source, translated “Calculation Formula”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L7485) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L941)

<a id="op-b8b5be9e34ba36"></a>
### Validation Issue.post init

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_issue_post_initialize`

**Inputs** self.

**Local steps**

- If self.details is identical to no value.
  - Set self.details from mapping().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L7627) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L948)

<a id="op-21f9600d294d8a"></a>
### Validation Issue.str

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_issue_text`

**Inputs** self.

**Declared result** str.

**Explicit results** \_(“Row {0}: {1}”, context = “Financial Report Template”).format(self.row\_idx, self.message) · self.message.

**Local steps**

- If self.row\_idx.
  - Return \_(“Row {0}: {1}”, context = “Financial Report Template”).format(self.row\_idx, self.message).
- Return self.message.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0050.json#L7699) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L949)

<a id="op-c3427f3ef3c5a5"></a>
### Validation Result.is valid

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_is_valid`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** len(self.issues) equals 0.

**Local steps**

- Return len(self.issues) equals 0.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L954)

<a id="op-966215e181459c"></a>
### Validation Result.has warnings

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_has_warnings`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** len(self.warnings) &gt; 0.

**Local steps**

- Return len(self.warnings) &gt; 0.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1006) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L953)

<a id="op-457fe674063d50"></a>
### Validation Result.error count

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_error_count`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** int.

**Explicit results** len(self.issues).

**Local steps**

- Return len(self.issues).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1005) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L952)

<a id="op-3f3bfd6c03291e"></a>
### Validation Result.warning count

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_warning_count`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** int.

**Explicit results** len(self.warnings).

**Local steps**

- Return len(self.warnings).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L957)

<a id="op-a1bb022c8a2841"></a>
### Validation Result.merge

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_merge`

**Inputs** self, other.

**Declared result** “ValidationResult”.

**Explicit results** self.

**Local steps**

- Evaluate self.issues.extend(other.issues).
- Evaluate self.warnings.extend(other.warnings).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L274) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L955)

<a id="op-ad2c2e96f512bf"></a>
### Validation Result.add error

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_add_error`

**Inputs** self, issue.

**Declared result** no value.

**Local steps**

- Evaluate self.issues.append(issue).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L394) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1003) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L950)

<a id="op-4ab56e884c764f"></a>
### Validation Result.add warning

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_add_warning`

**Inputs** self, issue.

**Declared result** no value.

**Local steps**

- Evaluate self.warnings.append(issue).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L464) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1004) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L951)

<a id="op-9a0c686028ca09"></a>
### Validation Result.notify user

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validation_result_notify_user`

**Inputs** self.

**Declared result** no value.

**State and service calls** msgprint with warnings.

**Explicit failure paths** validation helper — errors.

**Local steps**

- Set warnings from text in the contract.join(generator of escape\_html(str(w)) for w drawn from self.warnings where w).
  - Draw w from self.warnings, keep a combination only if (w).
- Set errors from text in the contract.join(generator of escape\_html(str(e)) for e drawn from self.issues where e).
  - Draw e from self.issues, keep a combination only if (e).
- If warnings.
  - Evaluate Platform.msgprint(warnings, title = translated “Warnings”, indicator = “orange”).
- If errors.
  - Call the validation error handler Platform.throw(errors, title = translated “Errors”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L956)

<a id="op-870e6876464e9c"></a>
### Template Validator.initialize

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_template_validator_initialize`

**Inputs** self, template.

**Local steps**

- Set self.template from template.
- Set self.validators from list(TemplateStructureValidator(), DependencyValidator(template)).
- Set self.formula\_validator from FormulaValidator(template).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L829) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L946)

<a id="op-adbc59206cb9a0"></a>
### Template Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_template_validator_validate`

**Inputs** self.

**Declared result** ValidationResult.

**Explicit results** result.

**Local steps**

- Set result from ValidationResult(list()).
- For each validator in self.validators.
  - Evaluate result.merge(validator.validate(self.template)).
- For each row in self.template.rows.
  - Evaluate result.merge(self.formula\_validator.validate(row)).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L958) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L947)

<a id="op-886ee0c3ad570c"></a>
### Validator.validate

`operation_enterprise_accounts_record_definitions_financial_report_template_financial_report_validation_business_behavior_validator_validate`

**Inputs** self, context.

**Wrappers, in declaration order** abstractmethod.

**Declared result** ValidationResult.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0051.json#L1150) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L958)
