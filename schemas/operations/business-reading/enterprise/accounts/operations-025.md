# Accounting and settlement · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Chart of accounts importer

[Record definition](../../../../data/record-types/chart_of_accounts_importer.json)

<a id="op-ac3f00394a456e"></a>
### Chartof Accounts Importer.validate

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_chartof_accounts_importer_validate`

**Inputs** self.

**Local steps**

- If self.import\_file.
  - Evaluate get\_coa(“Chart of Accounts Importer”, “All Accounts”, file\_name = self.import\_file, for\_validate = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0036.json#L1959) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L636)

<a id="op-0f5157ee4381a5"></a>
### Validate columns

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_validate_columns`

**Inputs** data.

**Explicit failure paths** validation helper — translated “No data found. Seems like you uploaded a blank file” · validation helper — translated “Columns are not according to template. Please compare the uploaded file with standard template”.

**Local steps**

- If not data.
  - Call the validation error handler Platform.throw(translated “No data found. Seems like you uploaded a blank file”).
- If any(generator of len(row) differs from 8 for row drawn from data).
  - Draw row from data.
  - Call the validation error handler Platform.throw(translated “Columns are not according to template. Please compare the uploaded file with standard template”, title = translated “Wrong Template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L652)

<a id="op-7037a2684f8d13"></a>
### Validate company

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_validate_company`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value · read “GL Entry” via get\_all.

**Explicit failure paths** validation helper — msg · validation helper — translated “Transactions against the Company already exist! Chart of Accounts can only be imported for a Company with no …”.

**Local steps**

- Evaluate Platform.has\_permission(“Chart of Accounts Importer”, throw = true).
- Set tuple(parent\_company, allow\_account\_creation\_against\_child\_company) from Platform.get\_cached\_value(“Company”, company, list(“parent\_company”, “allow\_account\_creation\_against\_child\_company”)).
- If (parent\_company and not allow\_account\_creation\_against\_child\_company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_company → not allow\_account\_creation\_against\_child\_company.
  - Set msg from (translated “{} is a child company.”.format(Platform.bold(company)) + one space).
  - Update msg using + translated “Please import accounts against parent company or enable {} in company master.”.format(Platform.bold(translated “Allow Account Creation Against Child Company”)).
  - Call the validation error handler Platform.throw(msg, title = translated “Wrong Company”).
- If Platform.db.get\_all(“GL Entry”, mapping(“company” → company), “name”, limit = 1).
  - Call the validation error handler Platform.throw(translated “Transactions against the Company already exist! Chart of Accounts can only be imported for a Company with no …”).
- Evaluate validate\_user\_perms(company).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Chart of Accounts Importer”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“parent\_company”, “allow\_account\_creation\_against\_child\_company”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L653)

<a id="op-07896de52be011"></a>
### Import coa

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_import_chart_of_accounts`

**Inputs** file\_name, company.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.only\_for(“Accounts Manager”).
- Evaluate Platform.has\_permission(“Company”, “write”, company, throw = true).
- Set tuple(file\_doc, extension) from get\_file(file\_name).
- Evaluate validate\_accounts(file\_doc, extension).
- If extension equals “csv”.
  - Set data from generate\_data\_from\_csv(file\_doc).
- Otherwise.
  - Set data from generate\_data\_from\_excel(file\_doc, extension).
- Evaluate validate\_columns(data).
- Set forest from build\_forest(data).
- Evaluate validate\_company(company).
- Evaluate unset\_existing\_data(company).
- Set Platform.local.flags.ignore\_root\_company\_validation from true.
- Evaluate create\_charts(company, custom\_chart = forest, from\_coa\_importer = true).
- Evaluate set\_default\_accounts(company).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“Accounts Manager”), Platform.has\_permission(“Company”, “write”, company, throw = true).

**Boundaries to resolve** callee failures, file state, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L648)

<a id="op-1c24edf4b28c00"></a>
### Get file

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_file`

**Inputs** file\_name.

**Explicit results** tuple(file\_doc, extension).

**Explicit failure paths** Platform.PermissionError · validation helper — translated “Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload”.

**Local steps**

- Set file\_doc from find\_file\_by\_url(file\_name).
- If not file\_doc.
  - Raise Platform.PermissionError.
- Set parts from file\_doc.get\_extension().
- Set extension from parts at 1.
- Set extension from extension.lstrip(“.”).
- If extension does not belong to tuple(“csv”, “xlsx”, “xls”).
  - Call the validation error handler Platform.throw(translated “Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload”).
- Return tuple(file\_doc, extension).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0036.json#L3258) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L641)

<a id="op-6f25d867e678fb"></a>
### Generate data from csv

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_generate_data_from_comma_separated_values`

**Inputs** file\_doc, as\_dict = false.

**Explicit results** generate\_data\_from\_rows(list(csv.reader(in\_file)), as\_dict).

**Local steps**

- Within open(file\_doc.get\_full\_path()) bound as in\_file.
  - Return generate\_data\_from\_rows(list(csv.reader(in\_file)), as\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L638)

<a id="op-c85e83872cd63d"></a>
### Generate data from excel

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_generate_data_from_excel`

**Inputs** file\_doc, extension, as\_dict = false.

**Explicit results** generate\_data\_from\_rows(rows, as\_dict).

**Local steps**

- Set content from file\_doc.get\_content().
- If extension equals “xlsx”.
  - Set rows from read\_xlsx\_file\_from\_attached\_file(fcontent = content).
- Otherwise.
  - If extension equals “xls”.
    - Set rows from read\_xls\_file\_from\_attached\_file(content).
- Return generate\_data\_from\_rows(rows, as\_dict).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L639)

<a id="op-e3ab7c1b82f64c"></a>
### Generate data from rows

`operation_enterprise_binding_enterprise_accounts_doctype_chart_of_accounts_importer_chart_of_accounts_importer_generate_data_from_rows`

**Inputs** rows, as\_dict = false.

**Explicit results** data.

**Local steps**

- Set rows from list of row for row drawn from rows where any(generator of cstr(value).strip() for value drawn from row).
  - Draw row from rows, keep a combination only if (any(generator of cstr(value).strip() for value drawn from row)).
  - Draw value from row.
- Evaluate validate\_columns(rows at slice 1 to no value).
- Evaluate validate\_columns(rows at slice no value to 1).
- Set headers from rows at 0.
- Set data from list().
- For each row in rows at slice 1 to no value.
  - If as\_dict.
    - Evaluate data.append(mapping of Platform.scrub(cstr(header)) → row at index for tuple(index, header) drawn from enumerate(headers)).
      - Draw tuple(index, header) from enumerate(headers).
  - Otherwise.
    - If not row at 1.
      - Set row at 1 from row at 0.
      - Set row at 3 from row at 2.
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L772)

<a id="op-a1013478d9f832"></a>
### Get coa

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_chart_of_accounts`

**Inputs** doctype, parent, is\_root = false, file\_name = no value, for\_validate = 0.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** accounts · mapping(“show\_import\_button” → 1).

**Local steps**

- Evaluate Platform.has\_permission(“Chart of Accounts Importer”, throw = true).
- Set tuple(file\_doc, extension) from get\_file(file\_name).
- Set parent from no value when parent equals translated “All Accounts”, otherwise parent.
  - Value choice on parent equals translated “All Accounts” — true gives no value, false gives parent.
- If extension equals “csv”.
  - Set data from generate\_data\_from\_csv(file\_doc).
- Otherwise.
  - Set data from generate\_data\_from\_excel(file\_doc, extension).
- Evaluate validate\_columns(data).
- Evaluate validate\_accounts(file\_doc, extension).
- Set forest from build\_forest(data).
- If not for\_validate.
  - Set accounts from build\_tree\_from\_json(empty text, chart\_data = forest, from\_coa\_importer = true).
  - Set accounts from list of d for d drawn from accounts where d at “parent\_account” equals parent.
    - Draw d from accounts, keep a combination only if (d at “parent\_account” equals parent).
  - Return accounts.
- Otherwise.
  - Return mapping(“show\_import\_button” → 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Chart of Accounts Importer”, throw = true).

**Boundaries to resolve** callee failures, file state, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L640)

<a id="op-4db3f6a9d10cf3"></a>
### Build forest

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_build_forest`

**Inputs** data.

**Explicit results** out.

**Explicit failure paths** validation helper — text in the contract.join(error\_messages).

**Local steps**

- Evaluate validate\_columns(data).
- Bind local operation set\_nested for subsequent calls.
- Bind local operation return\_parent for subsequent calls.
- Set tuple(charts\_map, parent\_accounts) from tuple(mapping(), mapping()).
- Set line\_no from 2.
- Set error\_messages from list().
- For each i in data.
  - Set tuple(account\_name, parent\_account, account\_number, parent\_account\_number, …) from i.
  - If not account\_name.
    - Evaluate error\_messages.append(translated “Row {0}: Please enter Account Name”.format(line\_no)).
  - Set name from account\_name.
  - If account\_number.
    - Set account\_number from cstr(account\_number).strip().
    - Set account\_name from formatted text {account\_number} - {account\_name}.
  - If parent\_account\_number.
    - Set parent\_account from formatted text {cstr(parent\_account\_number).strip()} - {parent\_account}.
  - Set parent\_accounts at account\_name from parent\_account.
  - Set charts\_map at account\_name from mapping().
  - Set charts\_map at account\_name at “account\_name” from name.
  - If account\_number.
    - Set charts\_map at account\_name at “account\_number” from account\_number.
  - If cint(is\_group) equals 1.
    - Set charts\_map at account\_name at “is\_group” from is\_group.
  - If account\_type.
    - Set charts\_map at account\_name at “account\_type” from account\_type.
  - If root\_type.
    - Set charts\_map at account\_name at “root\_type” from root\_type.
  - If account\_currency.
    - Set charts\_map at account\_name at “account\_currency” from account\_currency.
  - Update line\_no using + 1.
- If error\_messages.
  - Call the validation error handler Platform.throw(text in the contract.join(error\_messages)).
- Set out from mapping().
- For each account\_name in charts\_map.
  - Set path from return\_parent(parent\_accounts, account\_name) at slice no value to no value with step negative 1.
  - For each tuple(n, account\_name) in enumerate(path).
    - Evaluate set\_nested(out, path at slice no value to (n + 1), charts\_map at account\_name).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L632)

<a id="op-e2479495288fca"></a>
### Build forest.set nested

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_build_forest_set_nested`

**Inputs** d, path, value.

**Explicit results** d.

**Local steps**

- Set reduce(deferred anonymous expression, path at slice no value to negative 1, d) at path at negative 1 from value.
- Return d.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0036.json#L6438) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L634)

<a id="op-1609c71fba39b1"></a>
### Build forest.return parent

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_build_forest_return_parent`

**Inputs** parent\_accounts, child.

**Explicit results** path.

**Explicit failure paths** validation helper — translated “Circular reference found for account {0}”.format(Platform.bold(child)) · validation helper — translated “The parent account {0} does not exist in the uploaded template”.format(Platform.bold(parent\_account)).

**Local steps**

- Set path from list().
- While child.
  - If child belongs to path.
    - Call the validation error handler Platform.throw(translated “Circular reference found for account {0}”.format(Platform.bold(child))).
  - Evaluate path.append(child).
  - Set parent\_account from parent\_accounts at child.
  - If parent\_account equals child.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If (parent\_account and parent\_account does not belong to parent\_accounts).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_account → parent\_account does not belong to parent\_accounts.
    - Call the validation error handler Platform.throw(translated “The parent account {0} does not exist in the uploaded template”.format(Platform.bold(parent\_account))).
  - Set child from parent\_account.
- Return path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L633)

<a id="op-b46d376d2592c9"></a>
### Build response as excel

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_build_response_as_excel`

**Inputs** writer.

**Local steps**

- Set filename from Platform.generate\_hash(empty text, 10).
- Within open(filename, “wb”) bound as f.
  - Evaluate f.write(cstr(writer.getvalue()).encode(“utf-8”)).
- Set f from open(filename).
- Set reader from csv.reader(f).
- Bind dependencies make\_xlsx.
- Set xlsx\_file from make\_xlsx(reader, “Chart of Accounts Importer Template”).
- Evaluate f.close().
- Evaluate os.remove(filename).
- Set Platform.response at “filename” from “coa\_importer\_template.xlsx”.
- Set Platform.response at “filecontent” from xlsx\_file.getvalue().
- Set Platform.response at “type” from “binary”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(empty text, 10).

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0036.json#L7094) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L635)

<a id="op-26ef8e52b71d43"></a>
### Download template

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_download_template`

**Inputs** file\_type, template\_type, company.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.has\_permission(“Chart of Accounts Importer”, throw = true).
- Set writer from get\_template(template\_type, company).
- If file\_type equals “CSV”.
  - Set Platform.response at “result” from cstr(writer.getvalue()).
  - Set Platform.response at “type” from “csv”.
  - Set Platform.response at “doctype” from “Chart of Accounts Importer”.
- Otherwise.
  - Evaluate build\_response\_as\_excel(writer).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Chart of Accounts Importer”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L637)

<a id="op-477a56afa12d5c"></a>
### Get template

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_template`

**Inputs** template\_type, company.

**Explicit results** writer.

**Local steps**

- Set fields from list(“Account Name”, “Parent Account”, “Account Number”, “Parent Account Number”, …).
- Set writer from UnicodeWriter().
- Evaluate writer.writerow(fields).
- If template\_type equals “Blank Template”.
  - For each root\_type in get\_root\_types().
    - Evaluate writer.writerow(list(empty text, empty text, empty text, empty text, …)).
  - For each account in get\_mandatory\_group\_accounts().
    - Evaluate writer.writerow(list(empty text, empty text, empty text, empty text, …)).
  - For each account\_type in get\_mandatory\_account\_types().
    - Evaluate writer.writerow(list(empty text, empty text, empty text, empty text, …)).
- Otherwise.
  - Set writer from get\_sample\_template(writer, company).
- Return writer.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L647)

<a id="op-5a7a1ffcf1a83e"></a>
### Get sample template

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_sample_template`

**Inputs** writer, company.

**Record and data access** read “Company” via get\_value.

**Explicit results** writer.

**Local steps**

- Set currency from Platform.db.get\_value(“Company”, company, “default\_currency”).
- Within open(os.path.join(os.path.dirname(\_\_file\_\_), “coa\_sample\_template.csv”)) bound as f.
  - For each row in f.
    - Set row from list(expanded row.strip().split(“,”), currency).
    - Evaluate writer.writerow(row).
- Return writer.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L778) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L646)

<a id="op-26bc74c19ef2f8"></a>
### Validate accounts

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_validate_accounts`

**Inputs** file\_doc, extension.

**Explicit results** list(true, len(accounts)).

**Explicit failure paths** validation helper — translated “Please enter Account Name for every row in the uploaded template” · validation helper — msg · validation helper — translated “Please add accounts for the following Account Types: {0}”.format(“, ”.join(missing)).

**Local steps**

- If extension equals “csv”.
  - Set accounts from generate\_data\_from\_csv(file\_doc, as\_dict = true).
- Otherwise.
  - Set accounts from generate\_data\_from\_excel(file\_doc, extension, as\_dict = true).
- Set accounts\_dict from mapping().
- For each account in accounts.
  - If not account.get(“account\_name”).
    - Call the validation error handler Platform.throw(translated “Please enter Account Name for every row in the uploaded template”).
  - Evaluate accounts\_dict.setdefault(account at “account\_name”, account).
  - If “parent\_account” does not belong to account.
    - Set msg from translated “Please make sure the file you are using has 'Parent Account' column present in the header.”.
    - Update msg using + text in the contract.
    - Update msg using + translated “Alternatively, you can download the template and fill your data in.”.
    - Call the validation error handler Platform.throw(msg, title = translated “Parent Account Missing”).
  - If (account at “parent\_account” and accounts\_dict.get(account at “parent\_account”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account at “parent\_account” → accounts\_dict.get(account at “parent\_account”).
    - Set accounts\_dict at account at “parent\_account” at “is\_group” from 1.
- Evaluate validate\_root(accounts\_dict).
- Set account\_types from set of account.get(“account\_type”) for account drawn from accounts.
  - Draw account from accounts.
- Set missing from list of translated account at “account\_type” for account drawn from get\_mandatory\_account\_types() where account at “account\_type” does not belong to account\_types.
  - Draw account from get\_mandatory\_account\_types(), keep a combination only if (account at “account\_type” does not belong to account\_types).
- If missing.
  - Call the validation error handler Platform.throw(translated “Please add accounts for the following Account Types: {0}”.format(“, ”.join(missing)), title = translated “Missing Account Types”).
- Return list(true, len(accounts)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L651)

<a id="op-7f9a201f18cede"></a>
### Validate root

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_validate_root`

**Inputs** accounts.

**Explicit failure paths** validation helper — text in the contract.join(error\_messages).

**Local steps**

- Set roots from list of accounts at d for d drawn from accounts where not accounts at d.get(“parent\_account”).
  - Draw d from accounts, keep a combination only if (not accounts at d.get(“parent\_account”)).
- Set error\_messages from list().
- For each account in roots.
  - If (not account.get(“root\_type”) and account.get(“account\_name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account.get(“root\_type”) → account.get(“account\_name”).
    - Evaluate error\_messages.append(translated “Please enter Root Type for account- {0}”.format(account.get(“account\_name”))).
  - Otherwise.
    - If (account.get(“root\_type”) does not belong to get\_root\_types() and account.get(“account\_name”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account.get(“root\_type”) does not belong to get\_root\_types() → account.get(“account\_name”).
      - Evaluate error\_messages.append(translated “Root Type for {0} must be one of the Asset, Liability, Income, Expense and Equity”.format(account.get(“account\_name”))).
- Evaluate validate\_missing\_roots(roots).
- If error\_messages.
  - Call the validation error handler Platform.throw(text in the contract.join(error\_messages)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L1550) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L655)

<a id="op-2ce0b0499645a7"></a>
### Validate missing roots

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_validate_missing_roots`

**Inputs** roots.

**Explicit failure paths** validation helper — translated “Please add Root Account for - {0}”.format(“ , ”.join(missing)).

**Local steps**

- Set root\_types\_added from set(generator of d.get(“root\_type”) for d drawn from roots).
  - Draw d from roots.
- Set missing from list((set(get\_root\_types()) − root\_types\_added)).
- If missing.
  - Call the validation error handler Platform.throw(translated “Please add Root Account for - {0}”.format(“ , ”.join(missing))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L2047) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L654)

<a id="op-d519c3f45f858e"></a>
### Get root types

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_root_types`

**Inputs** no declared parameters.

**Explicit results** tuple(“Asset”, “Liability”, “Expense”, “Income”, …).

**Local steps**

- Return tuple(“Asset”, “Liability”, “Expense”, “Income”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L2277) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L645)

<a id="op-d19937328cb7fd"></a>
### Get report type

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_report_type`

**Inputs** root\_type.

**Explicit results** “Balance Sheet” · “Profit and Loss”.

**Local steps**

- If root\_type belongs to tuple(“Asset”, “Liability”, “Equity”).
  - Return “Balance Sheet”.
- Otherwise.
  - Return “Profit and Loss”.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L2332) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L644)

<a id="op-a10935f059c45f"></a>
### Get mandatory group accounts

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_mandatory_group_accounts`

**Inputs** no declared parameters.

**Explicit results** tuple(“Bank”, “Cash”, “Stock”).

**Local steps**

- Return tuple(“Bank”, “Cash”, “Stock”).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L2417) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L643)

<a id="op-4145adfa5c43ae"></a>
### Get mandatory account types

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_get_mandatory_account_types`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“account\_type” → “Cost of Goods Sold”, “root\_type” → “Expense”), mapping(“account\_type” → “Depreciation”, “root\_type” → “Expense”), mapping(“account\_type” → “Fixed Asset”, “root\_type” → “Asset ….

**Local steps**

- Return list(mapping(“account\_type” → “Cost of Goods Sold”, “root\_type” → “Expense”), mapping(“account\_type” → “Depreciation”, “root\_type” → “Expense”), mapping(“account\_type” → “Fixed Asset”, “root\_type” → “Asset ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0037.json#L2464) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L642)

<a id="op-1760b4fa0ed0f6"></a>
### Unset existing data

`operation_enterprise_accounts_record_definitions_chart_of_accounts_importer_business_behavior_unset_existing_data`

**Inputs** company.

**Record and data access** read doctype via get\_all · read “Account” via get\_all.

**State and service calls** request set\_value on “Company” · request delete\_doc for doctype · request delete on doctype · request delete\_doc for “Account”.

**Local steps**

- Set fieldnames from get\_linked\_fields(“Account”).get(“Company”, mapping()).get(“fieldname”, list()).
- Evaluate Platform.db.set\_value(“Company”, company, dict.fromkeys(fieldnames, empty text)).
- For each doctype in tuple(“Sales Taxes and Charges Template”, “Purchase Taxes and Charges Template”).
  - For each name in Platform.get\_all(doctype, filters = mapping(“company” → company), pluck = “name”).
    - Evaluate Platform.delete\_doc(doctype, name, ignore\_permissions = true).
- For each doctype in tuple(“Party Account”, “Mode of Payment Account”, “Tax Withholding Account”).
  - Evaluate Platform.db.delete(doctype, mapping(“company” → company)).
- For each name in Platform.get\_all(“Account”, filters = mapping(“company” → company), order\_by = “lft desc”, pluck = “name”).
  - Evaluate Platform.delete\_doc(“Account”, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L650)
