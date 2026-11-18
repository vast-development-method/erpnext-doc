# Regional rules and controller overrides · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Electronic invoice register

<a id="op-c4d089f8af7757"></a>
### Execute

`operation_enterprise_regional_report_electronic_invoice_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** \_execute(filters).

**Explicit failure paths** validation helper — translated “Please select a Company”.

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not (filters or mapping()).get(“company”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
  - Call the validation error handler Platform.throw(translated “Please select a Company”).
- Return \_execute(filters).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L996)

## Record · Import supplier invoice

[Record definition](../../../../data/record-types/import_supplier_invoice.json)

<a id="op-a75d5352ba4bab"></a>
### Import Supplier Invoice.validate

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_validate`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_value.

**Explicit failure paths** validation helper — translated “Please set default UOM in Stock Settings”.

**Local steps**

- If not Platform.db.get\_value(“Stock Settings”, fieldname = “stock\_uom”).
  - Call the validation error handler Platform.throw(translated “Please set default UOM in Stock Settings”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0615.json#L1185) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L988)

<a id="op-014281f3ebb320"></a>
### Import Supplier Invoice.autoname

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_autoname`

**Inputs** self.

**Local steps**

- If not self.name.
  - Set self.name from append\_number\_if\_name\_exists(self.doctype, (“Import Invoice on ” + format\_datetime(self.creation))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L982)

<a id="op-e171f6ff033996"></a>
### Import Supplier Invoice.import xml data

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_import_extensible_markup_data`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_value.

**State and service calls** call save on self.

**Local steps**

- Evaluate self.publish(“File Import”, translated “Processing XML Files”, 1, 3).
- Set self.file\_count from 0.
- Set self.purchase\_invoices\_count from 0.
- Set self.default\_uom from Platform.db.get\_value(“Stock Settings”, fieldname = “stock\_uom”).
- Attempt the following.
  - Evaluate self.import\_zip\_file().
- On failure (Exception).
  - Evaluate Platform.log\_error(“Unable to import the zip file”, reference\_doctype = self.doctype, reference\_name = self.name).
  - Set self.status from “Error”.
- When the protected block completes normally.
  - If self.purchase\_invoices\_count equals self.file\_count.
    - Set self.status from “File Import Completed”.
  - Otherwise.
    - Set self.status from “Partially Completed - Check Error Log”.
- Evaluate self.publish(“File Import”, translated “XML Files Processed”, 2, 3).
- Evaluate self.save().
- Evaluate self.publish(“File Import”, translated “XML Files Processed”, 3, 3).

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish](operations-001.md#op-49c2b6711b1257), [import zip file](operations-001.md#op-5a1554c88ff957).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L983)

<a id="op-5a1554c88ff957"></a>
### Import Supplier Invoice.import zip file

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_importsupplierinvoice_import_zip_file`

**Inputs** self.

**Record and data access** resolve a document from “File” via get\_doc.

**Local steps**

- Set zip\_file from Platform.get\_doc(“File”, mapping(“file\_url” → self.zip\_file, “attached\_to\_doctype” → self.doctype, “attached\_to\_name” → self.name)).
- Within zipfile.ZipFile(zip\_file.get\_full\_path()) bound as zf.
  - For each file\_name in zf.namelist().
    - If file\_name.lower().endswith(“.p7m”).
      - Evaluate self.log\_signed\_file(file\_name).
      - Continue with the next iteration or loop test.
    - Attempt the following.
      - Set content from get\_file\_content(file\_name, zf).
    - On failure (Exception).
      - Evaluate self.log\_unreadable\_file(file\_name).
      - Continue with the next iteration or loop test.
    - Set file\_content from bs(content, “xml”).
    - Evaluate self.prepare\_data\_for\_import(file\_content, file\_name, content).

If control reaches the end, it returns no value.

**Methods declared on this owner** [log signed file](operations-001.md#op-2e574d8dd8e888), [log unreadable file](operations-001.md#op-29534af003fee1), [prepare data for import](operations-001.md#op-a6e78f73133d2f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1395)

<a id="op-29534af003fee1"></a>
### Import Supplier Invoice.log unreadable file

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_importsupplierinvoice_log_unreadable_file`

**Inputs** self, file\_name.

**Declared result** no value.

**Local steps**

- Update self.file\_count using + 1.
- Evaluate Platform.log\_error(title = translated “Unable to read file {0}”.format(file\_name), reference\_doctype = self.doctype, reference\_name = self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1397)

<a id="op-2e574d8dd8e888"></a>
### Import Supplier Invoice.log signed file

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_importsupplierinvoice_log_signed_file`

**Inputs** self, file\_name.

**Declared result** no value.

**Local steps**

- Update self.file\_count using + 1.
- Evaluate Platform.log\_error(title = translated “Unable to import a signed file”, message = translated “Signed file {0} is not supported, import the XML file instead”.format(file\_name), reference\_doctype = self.doct ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1396)

<a id="op-a6e78f73133d2f"></a>
### Import Supplier Invoice.prepare data for import

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_prepare_data_for_import`

**Inputs** self, file\_content, file\_name, encoded\_content.

**State and service calls** savepoint “import\_invoice” · rollback.

**Local steps**

- For each line in file\_content.find\_all(“DatiGeneraliDocumento”).
  - Update self.file\_count using + 1.
  - Evaluate Platform.db.savepoint(“import\_invoice”).
  - Attempt the following.
    - Set pi\_name from self.create\_invoice\_from\_file(line, file\_content, file\_name).
    - Evaluate attach\_file\_to\_invoice(pi\_name, file\_name, encoded\_content).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = “import\_invoice”).
    - Evaluate Platform.log\_error(“Unable to create Purchase Invoice”, reference\_doctype = self.doctype, reference\_name = self.name).
    - Continue with the next iteration or loop test.
  - Update self.purchase\_invoices\_count using + 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [create invoice from file](operations-001.md#op-c018fa557b0711).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L984)

<a id="op-c018fa557b0711"></a>
### Import Supplier Invoice.create invoice from file

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_importsupplierinvoice_create_invoice_from_file`

**Inputs** self, line, file\_content, file\_name.

**Explicit results** create\_purchase\_invoice(supplier\_name, file\_name, invoices\_args, self.name).

**Explicit failure paths** validation helper — translated “Numero has not set in the XML file”.

**Local steps**

- Set invoices\_args from mapping(“company” → self.company, “naming\_series” → self.invoice\_series, “document\_type” → line.TipoDocumento.text, “bill\_date” → get\_datetime\_str(line.Data.text), …).
- If not invoices\_args.get(“bill\_no”, empty text).
  - Call the validation error handler Platform.throw(translated “Numero has not set in the XML file”).
- Set supp\_dict from get\_supplier\_details(file\_content).
- Set invoices\_args at “destination\_code” from get\_destination\_code\_from\_file(file\_content).
- Evaluate self.prepare\_items\_for\_invoice(file\_content, invoices\_args).
- Set invoices\_args at “taxes” from get\_taxes\_from\_file(file\_content, self.tax\_account, invoices\_args at “is\_return”).
- Set invoices\_args at “terms” from get\_payment\_terms\_from\_file(file\_content).
- Set supplier\_name from create\_supplier(self.supplier\_group, supp\_dict).
- Evaluate create\_address(supplier\_name, supp\_dict).
- Evaluate validate\_invoice\_not\_imported(supplier\_name, invoices\_args).
- Return create\_purchase\_invoice(supplier\_name, file\_name, invoices\_args, self.name).

**Methods declared on this owner** [prepare items for invoice](operations-001.md#op-827530cb451bd1).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1394)

<a id="op-827530cb451bd1"></a>
### Import Supplier Invoice.prepare items for invoice

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_prepare_items_for_invoice`

**Inputs** self, file\_content, invoices\_args.

**Local steps**

- For each line in file\_content.find\_all(“DettaglioLinee”).
  - If (line.find(“PrezzoUnitario”) and line.find(“PrezzoTotale”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in line.find(“PrezzoUnitario”) → line.find(“PrezzoTotale”).
    - Evaluate self.append\_item(line, invoices\_args).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append item](operations-001.md#op-2627eba7855010).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L985)

<a id="op-2627eba7855010"></a>
### Import Supplier Invoice.append item

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_importsupplierinvoice_append_item`

**Inputs** self, line, invoices\_args.

**Local steps**

- Set rate from flt(line.PrezzoUnitario.text).
- Set line\_total from flt(line.PrezzoTotale.text).
- Set qty from flt(line.Quantita.text) when line.find(“Quantita”), otherwise 1.
  - Value choice on line.find(“Quantita”) — true gives flt(line.Quantita.text), false gives 1.
- Set uom from create\_uom(line.UnitaMisura.text) when line.find(“UnitaMisura”), otherwise self.default\_uom.
  - Value choice on line.find(“UnitaMisura”) — true gives create\_uom(line.UnitaMisura.text), false gives self.default\_uom.
- If (invoices\_args at “is\_return” or (rate &lt; 0 and line\_total &lt; 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in invoices\_args at “is\_return” → (rate &lt; 0 and line\_total &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rate &lt; 0 → line\_total &lt; 0.
  - Set qty from negative abs(qty).
- If (line.find(“ScontoMaggiorazione”) and qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in line.find(“ScontoMaggiorazione”) → qty.
  - Set rate from (line\_total ÷ qty).
- Set line\_str from re.sub(“&#91;^A-Za-z0-9&#93;+”, “-”, line.Descrizione.text).
- Evaluate invoices\_args at “items”.append(mapping(“item\_code” → self.item\_code, “item\_name” → line\_str at slice 0 to 140, “description” → line\_str, “qty” → qty, …)).
  - Value choice on line.find(“AliquotaIVA”) — true gives flt(line.AliquotaIVA.text), false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1393)

<a id="op-6900baa460b593"></a>
### Import Supplier Invoice.process file data

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_process_file_data`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_set on self · enqueue doc with self.doctype.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.db\_set(“status”, “Processing File Data”, notify = true, commit = true).
- Evaluate Platform.enqueue\_doc(self.doctype, self.name, “import\_xml\_data”, queue = “long”, timeout = 3600).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from Platform.enqueue\_doc(self.doctype, self.name, “import\_xml\_data”, queue = “long”, timeout = 3600).

**Boundaries to resolve** stored data, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L986)

<a id="op-49c2b6711b1257"></a>
### Import Supplier Invoice.publish

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_import_supplier_invoice_publish`

**Inputs** self, title, message, count, total.

**State and service calls** publish realtime with “import\_invoice\_update”.

**Local steps**

- Evaluate Platform.publish\_realtime(“import\_invoice\_update”, mapping(“title” → title, “message” → message, “count” → count, “total” → total), user = self.modified\_by).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“import\_invoice\_update”, mapping(“title” → title, “message” → message, “count” → count, “total” → total), user = self.modified\_by).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0615.json#L4241) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L987)

<a id="op-7848fd2a21f5c3"></a>
### Attach file to invoice

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_attach_file_to_invoice`

**Inputs** pi\_name, file\_name, encoded\_content.

**State and service calls** request new\_doc for “File” · call insert on file\_doc.

**Local steps**

- Set file\_doc from Platform.new\_doc(“File”).
- Set file\_doc.file\_name from file\_name.
- Set file\_doc.attached\_to\_doctype from “Purchase Invoice”.
- Set file\_doc.attached\_to\_name from pi\_name.
- Set file\_doc.content from encoded\_content.
- Set file\_doc.decode from false.
- Set file\_doc.is\_private from true.
- Evaluate file\_doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L266) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1391)

<a id="op-917b6dfe87178f"></a>
### Get file content

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_get_file_content`

**Inputs** file\_name, zip\_file\_object.

**Explicit results** content.

**Local steps**

- Set content from empty text.
- Set encoded\_content from zip\_file\_object.read(file\_name).
- Attempt the following.
  - Set content from encoded\_content.decode(“utf-8-sig”).
- On failure (UnicodeDecodeError).
  - Attempt the following.
    - Set content from encoded\_content.decode(“utf-16”).
  - On failure (UnicodeDecodeError).
    - Evaluate Platform.log\_error((“UTF-16 encoding error for File Name: ” + file\_name)).
- Return content.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0615.json#L4406) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L978)

<a id="op-0e3c8302f3bbd7"></a>
### Get supplier details

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_get_supplier_details`

**Inputs** file\_content.

**Explicit results** supplier\_info.

**Local steps**

- Set supplier\_info from mapping().
- For each line in file\_content.find\_all(“CedentePrestatore”).
  - Set supplier\_info at “tax\_id” from (line.DatiAnagrafici.IdPaese.text + line.DatiAnagrafici.IdCodice.text).
  - If line.find(“CodiceFiscale”).
    - Set supplier\_info at “fiscal\_code” from line.DatiAnagrafici.CodiceFiscale.text.
  - If line.find(“RegimeFiscale”).
    - Set supplier\_info at “fiscal\_regime” from line.DatiAnagrafici.RegimeFiscale.text.
  - If line.find(“Denominazione”).
    - Set supplier\_info at “supplier” from line.DatiAnagrafici.Anagrafica.Denominazione.text.
  - If line.find(“Nome”).
    - Set supplier\_info at “supplier” from ((line.DatiAnagrafici.Anagrafica.Nome.text + one space) + line.DatiAnagrafici.Anagrafica.Cognome.text).
  - Set supplier\_info at “address\_line1” from line.Sede.Indirizzo.text.
  - Set supplier\_info at “city” from line.Sede.Comune.text.
  - If line.find(“Provincia”).
    - Set supplier\_info at “province” from line.Sede.Provincia.text.
  - Set supplier\_info at “pincode” from line.Sede.CAP.text.
  - Set supplier\_info at “country” from get\_country(line.Sede.Nazione.text).
  - Return supplier\_info.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L980)

<a id="op-fc14def6721907"></a>
### Get taxes from file

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_get_taxes_from_file`

**Inputs** file\_content, tax\_account, is\_return = false.

**Explicit results** taxes.

**Local steps**

- Set taxes from list().
- For each line in file\_content.find\_all(“DatiRiepilogo”).
  - If line.find(“AliquotaIVA”).
    - If line.find(“EsigibilitaIVA”).
      - Set descr from line.EsigibilitaIVA.text.
    - Otherwise.
      - Set descr from “None”.
    - Set tax\_amount from flt(line.Imposta.text) when line.find(“Imposta”), otherwise 0.
      - Value choice on line.find(“Imposta”) — true gives flt(line.Imposta.text), false gives 0.
    - Evaluate taxes.append(mapping(“charge\_type” → “Actual”, “account\_head” → tax\_account, “tax\_rate” → (flt(line.AliquotaIVA.text) or 0), “description” → descr, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(line.AliquotaIVA.text) → 0.
      - Value choice on is\_return — true gives negative abs(tax\_amount), false gives tax\_amount.
- Return taxes.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L981)

<a id="op-bb64d0173d5498"></a>
### Get payment terms from file

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_get_payment_terms_from_file`

**Inputs** file\_content.

**Explicit results** terms.

**Local steps**

- Set terms from list().
- Set mop\_dict from dict(generator of code.split(“-”, 1) for code drawn from mode\_of\_payment\_codes).
  - Draw code from mode\_of\_payment\_codes.
- For each line in file\_content.find\_all(“DettaglioPagamento”).
  - Set code from line.ModalitaPagamento.text.
  - Set mop\_code from formatted text {code}-{mop\_dict at code} when code belongs to mop\_dict, otherwise empty text.
    - Value choice on code belongs to mop\_dict — true gives formatted text {code}-{mop\_dict at code}, false gives empty text.
  - If line.find(“DataScadenzaPagamento”).
    - Set due\_date from dateutil.parser.parse(line.DataScadenzaPagamento.text).strftime(“%Y-%m-%d”).
  - Otherwise.
    - Set due\_date from today().
  - Evaluate terms.append(mapping(“mode\_of\_payment\_code” → mop\_code, “bank\_account\_iban” → line.IBAN.text when line.find(“IBAN”), otherwise empty text, “due\_date” → due\_date, “payment\_amount” → line.ImportoPagamento.text)).
    - Value choice on line.find(“IBAN”) — true gives line.IBAN.text, false gives empty text.
- Return terms.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L979)

<a id="op-24b1cabe35b77c"></a>
### Get destination code from file

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_get_destination_code_from_file`

**Inputs** file\_content.

**Explicit results** destination\_code.

**Local steps**

- Set destination\_code from empty text.
- For each line in file\_content.find\_all(“DatiTrasmissione”).
  - Set destination\_code from line.CodiceDestinatario.text.
- Return destination\_code.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0615.json#L6163) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L977)

<a id="op-9e3883d07485fc"></a>
### Create supplier

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_create_supplier`

**Inputs** supplier\_group, args.

**Record and data access** read “Supplier” via get\_value · read “Contact” via get\_all.

**State and service calls** request new\_doc for “Contact” · call insert on new\_contact · request new\_doc for “Supplier” · call insert on new\_supplier.

**Explicit results** existing\_supplier\_name · new\_supplier.name.

**Local steps**

- Set args from Platform.\_dict(args).
- Set existing\_supplier\_name from Platform.db.get\_value(“Supplier”, filters = mapping(“tax\_id” → args.tax\_id), fieldname = “name”).
- If existing\_supplier\_name.
  - Set filters from list(list(“Dynamic Link”, “link\_doctype”, “=”, “Supplier”), list(“Dynamic Link”, “link\_name”, “=”, existing\_supplier\_name), list(“Dynamic Link”, “parenttype”, “=”, “Contact”)).
  - If not Platform.get\_all(“Contact”, filters).
    - Set new\_contact from Platform.new\_doc(“Contact”).
    - Set new\_contact.first\_name from args.supplier at slice no value to 30.
    - Evaluate new\_contact.append(“links”, mapping(“link\_doctype” → “Supplier”, “link\_name” → existing\_supplier\_name)).
    - Evaluate new\_contact.insert(ignore\_mandatory = true, ignore\_permissions = true).
  - Return existing\_supplier\_name.
- Otherwise.
  - Set new\_supplier from Platform.new\_doc(“Supplier”).
  - Set new\_supplier.supplier\_name from re.sub(“&amp;amp”, “&amp;”, args.supplier).
  - Set new\_supplier.supplier\_group from supplier\_group.
  - Set new\_supplier.tax\_id from args.tax\_id.
  - Set new\_supplier.fiscal\_code from args.fiscal\_code.
  - Set new\_supplier.fiscal\_regime from args.fiscal\_regime.
  - Evaluate new\_supplier.insert(set\_name = get\_unique\_supplier\_name(new\_supplier.supplier\_name), ignore\_permissions = true).
  - Set new\_contact from Platform.new\_doc(“Contact”).
  - Set new\_contact.first\_name from args.supplier at slice no value to 30.
  - Evaluate new\_contact.append(“links”, mapping(“link\_doctype” → “Supplier”, “link\_name” → new\_supplier.name)).
  - Evaluate new\_contact.insert(ignore\_mandatory = true, ignore\_permissions = true).
  - Return new\_supplier.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L974)

<a id="op-7fecdf4a38c812"></a>
### Get unique supplier name

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_get_unique_supplier_name`

**Inputs** supplier\_name.

**Declared result** (str bitwise or no value).

**Record and data access** read “Supplier” via exists.

**Explicit results** append\_number\_if\_name\_exists(“Supplier”, supplier\_name).

**Local steps**

- If Platform.db.exists(“Supplier”, supplier\_name).
  - Return append\_number\_if\_name\_exists(“Supplier”, supplier\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L267) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1392)

<a id="op-341f1cddc35b1e"></a>
### Create address

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_create_address`

**Inputs** supplier\_name, args.

**Record and data access** read “Address” via get\_all · resolve a document from “Address” via get\_doc.

**State and service calls** request new\_doc for “Address” · call insert on new\_address\_doc.

**Explicit results** address · new\_address\_doc.name · no value.

**Local steps**

- Set args from Platform.\_dict(args).
- Set filters from list(list(“Dynamic Link”, “link\_doctype”, “=”, “Supplier”), list(“Dynamic Link”, “link\_name”, “=”, supplier\_name), list(“Dynamic Link”, “parenttype”, “=”, “Address”)).
- Set existing\_address from Platform.get\_all(“Address”, filters).
- If args.address\_line1.
  - Set new\_address\_doc from Platform.new\_doc(“Address”).
  - Set new\_address\_doc.address\_line1 from args.address\_line1.
  - If args.city.
    - Set new\_address\_doc.city from args.city.
  - Otherwise.
    - Set new\_address\_doc.city from “Not Provided”.
  - For each field in list(“province”, “pincode”, “country”).
    - If args.get(field).
      - Evaluate new\_address\_doc.set(field, args.get(field)).
  - For each address in existing\_address.
    - Set address\_doc from Platform.get\_doc(“Address”, address at “name”).
    - If (address\_doc.address\_line1 equals new\_address\_doc.address\_line1 and address\_doc.pincode equals new\_address\_doc.pincode).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in address\_doc.address\_line1 equals new\_address\_doc.address\_line1 → address\_doc.pincode equals new\_address\_doc.pincode.
      - Return address.
  - Evaluate new\_address\_doc.append(“links”, mapping(“link\_doctype” → “Supplier”, “link\_name” → supplier\_name)).
  - Set new\_address\_doc.address\_type from “Billing”.
  - Evaluate new\_address\_doc.insert(ignore\_mandatory = true, ignore\_permissions = true).
  - Return new\_address\_doc.name.
- Otherwise.
  - Return no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L972)

<a id="op-3ab300accdc097"></a>
### Validate invoice not imported

`operation_enterprise_binding_enterprise_regional_doctype_import_supplier_invoice_import_supplier_invoice_validate_invoice_not_imported`

**Inputs** supplier\_name, args.

**Declared result** no value.

**Record and data access** read “Purchase Invoice” via exists.

**Explicit failure paths** validation helper — translated “Supplier Invoice {0} is already imported in Purchase Invoice {1}”.format(args at “bill\_no”, existing\_invoice).

**Local steps**

- Set existing\_invoice from Platform.db.exists(“Purchase Invoice”, mapping(“company” → args at “company”, “supplier” → supplier\_name, “is\_return” → args at “is\_return”, “bill\_no” → args at “bill\_no”, …)).
- If existing\_invoice.
  - Call the validation error handler Platform.throw(translated “Supplier Invoice {0} is already imported in Purchase Invoice {1}”.format(args at “bill\_no”, existing\_invoice)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1398)

<a id="op-798ad7720ae1cb"></a>
### Create purchase invoice

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_create_purchase_invoice`

**Inputs** supplier\_name, file\_name, args, name.

**Record and data access** resolve a document from mapping(“doctype” → “Purchase Invoice”, “company” → args.company, “currency” → Enterprise.get\_company\_currency(args.company), “naming\_series” → args.naming\_series, …) via get\_doc.

**State and service calls** call insert on pi · call save on pi.

**Explicit results** pi.name.

**Local steps**

- Set args from Platform.\_dict(args).
- Set pi from Platform.get\_doc(mapping(“doctype” → “Purchase Invoice”, “company” → args.company, “currency” → Enterprise.get\_company\_currency(args.company), “naming\_series” → args.naming\_series, …)).
- Evaluate pi.set\_missing\_values().
- Evaluate pi.insert(ignore\_mandatory = true).
- Set calc\_total from 0.
- Set adj from 0.
- For each term in args.terms.
  - Update calc\_total using + flt(term at “payment\_amount”).
- If flt((calc\_total − flt(pi.grand\_total))) differs from 0.
  - Set adj from (calc\_total − flt(pi.grand\_total)).
- Set pi.payment\_schedule from list().
- For each term in args.terms.
  - Evaluate pi.append(“payment\_schedule”, mapping(“mode\_of\_payment\_code” → term at “mode\_of\_payment\_code”, “bank\_account\_iban” → term at “bank\_account\_iban”, “due\_date” → term at “due\_date”, “payment\_amount” → (flt(te ….
  - Set adj from 0.
- Set pi.imported\_grand\_total from calc\_total.
- Evaluate pi.save().
- Return pi.name.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L973)
