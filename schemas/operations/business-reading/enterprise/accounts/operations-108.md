# Accounting and settlement · operations 108

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Share transfer

[Record definition](../../../../data/record-types/share_transfer.json)

<a id="op-36c2ec9a9eb855"></a>
### Share Transfer.validate

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_validate`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “The shares already exist” · validation helper with ShareDontExists — translated “The shares don't exist with the {0}”.format(self.from\_shareholder).

**Local steps**

- Evaluate self.get\_company\_shareholder().
- Evaluate self.basic\_validations().
- Evaluate self.folio\_no\_validation().
- If self.transfer\_type equals “Issue”.
  - Set ret\_val from self.share\_exists(self.get\_company\_shareholder().name).
  - If ret\_val belongs to tuple(“Complete”, “Partial”).
    - Call the validation error handler Platform.throw(translated “The shares already exist”, Platform.DuplicateEntryError).
- Otherwise.
  - Set ret\_val from self.share\_exists(self.from\_shareholder).
  - If ret\_val belongs to tuple(“Outside”, “Partial”).
    - Call the validation error handler Platform.throw(translated “The shares don't exist with the {0}”.format(self.from\_shareholder), ShareDontExists).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get company shareholder](operations-108.md#op-cefe93315abede), [basic validations](operations-108.md#op-73d2408ad84413), [folio no validation](operations-108.md#op-596f7b82145d37), [share exists](operations-108.md#op-b725e7671dcc54).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L2798) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L186)

<a id="op-73d2408ad84413"></a>
### Share Transfer.basic validations

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_basic_validations`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The field From Shareholder cannot be blank” · validation helper — translated “The field Asset Account cannot be blank” · validation helper — translated “The field To Shareholder cannot be blank” · validation helper — translated “The fields From Shareholder and To Shareholder cannot be blank” · validation helper — translated “The field Equity/Liability Account cannot be blank” · 3 additional forms in the steps below.

**Local steps**

- If self.transfer\_type equals “Purchase”.
  - Set self.to\_shareholder from empty text.
  - If not self.from\_shareholder.
    - Call the validation error handler Platform.throw(translated “The field From Shareholder cannot be blank”).
  - If not self.from\_folio\_no.
    - Set self.to\_folio\_no from self.autoname\_folio(self.to\_shareholder).
  - If not self.asset\_account.
    - Call the validation error handler Platform.throw(translated “The field Asset Account cannot be blank”).
- Otherwise.
  - If self.transfer\_type equals “Issue”.
    - Set self.from\_shareholder from empty text.
    - If not self.to\_shareholder.
      - Call the validation error handler Platform.throw(translated “The field To Shareholder cannot be blank”).
    - If not self.to\_folio\_no.
      - Set self.to\_folio\_no from self.autoname\_folio(self.to\_shareholder).
    - If not self.asset\_account.
      - Call the validation error handler Platform.throw(translated “The field Asset Account cannot be blank”).
  - Otherwise.
    - If (not self.from\_shareholder or not self.to\_shareholder).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.from\_shareholder → not self.to\_shareholder.
      - Call the validation error handler Platform.throw(translated “The fields From Shareholder and To Shareholder cannot be blank”).
    - If not self.to\_folio\_no.
      - Set self.to\_folio\_no from self.autoname\_folio(self.to\_shareholder).
- If not self.equity\_or\_liability\_account.
  - Call the validation error handler Platform.throw(translated “The field Equity/Liability Account cannot be blank”).
- If self.from\_shareholder equals self.to\_shareholder.
  - Call the validation error handler Platform.throw(translated “The seller and the buyer cannot be the same”).
- If self.no\_of\_shares differs from ((self.to\_no − self.from\_no) + 1).
  - Call the validation error handler Platform.throw(translated “The number of shares and the share numbers are inconsistent”).
- Set amount from flt((self.rate × self.no\_of\_shares), self.precision(“amount”)).
- If (self.amount and flt(self.amount, self.precision(“amount”)) differs from amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.amount → flt(self.amount, self.precision(“amount”)) differs from amount.
  - Call the validation error handler Platform.throw(translated “There are inconsistencies between the rate, no of shares and the amount calculated”).
- Set self.amount from amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [autoname folio](operations-108.md#op-3815c2315d3d1d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L177)

<a id="op-b725e7671dcc54"></a>
### Share Transfer.share exists

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_share_exists`

**Inputs** self, shareholder.

**Explicit results** “Complete” · “Partial” · “Outside”.

**Local steps**

- Set doc from self.get\_shareholder\_doc(shareholder).
- For each entry in doc.share\_balance.
  - If (entry.share\_type differs from self.share\_type or entry.from\_no &gt; self.to\_no or entry.to\_no &lt; self.from\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.share\_type differs from self.share\_type → entry.from\_no &gt; self.to\_no → entry.to\_no &lt; self.from\_no.
    - Continue with the next iteration or loop test.
  - Otherwise.
    - If (entry.from\_no ≤ self.from\_no and entry.to\_no ≥ self.to\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.from\_no ≤ self.from\_no → entry.to\_no ≥ self.to\_no.
      - Return “Complete”.
    - Otherwise.
      - Return “Partial”.
- Return “Outside”.

**Methods declared on this owner** [get shareholder doc](operations-108.md#op-94976d6fcc091c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L185)

<a id="op-596f7b82145d37"></a>
### Share Transfer.folio no validation

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_folio_number_validation`

**Inputs** self.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper — translated “The shareholder does not belong to this company” · validation helper — translated “The folio numbers are not matching”.

**Local steps**

- Set shareholder\_fields from list(“from\_shareholder”, “to\_shareholder”).
- For each shareholder\_field in shareholder\_fields.
  - Set shareholder\_name from self.get(shareholder\_field).
  - If not shareholder\_name.
    - Continue with the next iteration or loop test.
  - Set doc from self.get\_shareholder\_doc(shareholder\_name).
  - If doc.company differs from self.company.
    - Call the validation error handler Platform.throw(translated “The shareholder does not belong to this company”).
  - If not doc.folio\_no.
    - Set doc.folio\_no from self.from\_folio\_no when shareholder\_field equals “from\_shareholder”, otherwise self.to\_folio\_no.
      - Value choice on shareholder\_field equals “from\_shareholder” — true gives self.from\_folio\_no, false gives self.to\_folio\_no.
    - Evaluate doc.save().
  - Otherwise.
    - If (doc.folio\_no and doc.folio\_no differs from self.from\_folio\_no when shareholder\_field equals “from\_shareholder”, otherwise self.to\_folio\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.folio\_no → doc.folio\_no differs from self.from\_folio\_no when shareholder\_field equals “from\_shareholder”, otherwise self.to\_folio\_no.
      - Value choice on shareholder\_field equals “from\_shareholder” — true gives self.from\_folio\_no, false gives self.to\_folio\_no.
      - Call the validation error handler Platform.throw(translated “The folio numbers are not matching”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get shareholder doc](operations-108.md#op-94976d6fcc091c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L4456) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L178)

<a id="op-3815c2315d3d1d"></a>
### Share Transfer.autoname folio

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_autoname_folio`

**Inputs** self, shareholder, is\_company = false.

**State and service calls** call save on doc.

**Explicit results** doc.folio\_no.

**Local steps**

- If is\_company.
  - Set doc from self.get\_company\_shareholder().
- Otherwise.
  - Set doc from self.get\_shareholder\_doc(shareholder).
- Set doc.folio\_no from make\_autoname(“FN.#####”).
- Evaluate doc.save().
- Return doc.folio\_no.

**Methods declared on this owner** [get company shareholder](operations-108.md#op-cefe93315abede), [get shareholder doc](operations-108.md#op-94976d6fcc091c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L4884) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L176)

<a id="op-d413cbcb1d1b43"></a>
### Share Transfer.remove shares

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_remove_shares`

**Inputs** self, shareholder.

**Record and data access** resolve a document from “Shareholder” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Shareholder”, shareholder).
- Set current\_entries from doc.share\_balance.
- Set new\_entries from list().
- For each entry in current\_entries.
  - If (entry.share\_type differs from self.share\_type or entry.from\_no &gt; self.to\_no or entry.to\_no &lt; self.from\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.share\_type differs from self.share\_type → entry.from\_no &gt; self.to\_no → entry.to\_no &lt; self.from\_no.
    - Evaluate new\_entries.append(entry).
    - Continue with the next iteration or loop test.
  - Otherwise.
    - If (entry.from\_no ≤ self.from\_no and entry.to\_no ≥ self.to\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.from\_no ≤ self.from\_no → entry.to\_no ≥ self.to\_no.
      - If entry.from\_no equals self.from\_no.
        - If entry.to\_no equals self.to\_no.
          - Take no action here.
        - Otherwise.
          - Evaluate new\_entries.append(self.return\_share\_balance\_entry((self.to\_no + 1), entry.to\_no, entry.rate)).
      - Otherwise.
        - If entry.to\_no equals self.to\_no.
          - Evaluate new\_entries.append(self.return\_share\_balance\_entry(entry.from\_no, (self.from\_no − 1), entry.rate)).
        - Otherwise.
          - Evaluate new\_entries.append(self.return\_share\_balance\_entry(entry.from\_no, (self.from\_no − 1), entry.rate)).
          - Evaluate new\_entries.append(self.return\_share\_balance\_entry((self.to\_no + 1), entry.to\_no, entry.rate)).
    - Otherwise.
      - If (entry.from\_no ≥ self.from\_no and entry.to\_no ≤ self.to\_no).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.from\_no ≥ self.from\_no → entry.to\_no ≤ self.to\_no.
        - Take no action here.
      - Otherwise.
        - If (self.from\_no ≤ entry.from\_no ≤ self.to\_no and entry.to\_no ≥ self.to\_no).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_no ≤ entry.from\_no ≤ self.to\_no → entry.to\_no ≥ self.to\_no.
          - Compare adjacent operands in order, stopping at the first false comparison in self.from\_no ≤ entry.from\_no ≤ self.to\_no.
          - Evaluate new\_entries.append(self.return\_share\_balance\_entry((self.to\_no + 1), entry.to\_no, entry.rate)).
        - Otherwise.
          - If (self.from\_no ≤ entry.to\_no ≤ self.to\_no and entry.from\_no ≤ self.from\_no).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_no ≤ entry.to\_no ≤ self.to\_no → entry.from\_no ≤ self.from\_no.
            - Compare adjacent operands in order, stopping at the first false comparison in self.from\_no ≤ entry.to\_no ≤ self.to\_no.
            - Evaluate new\_entries.append(self.return\_share\_balance\_entry(entry.from\_no, (self.from\_no − 1), entry.rate)).
          - Otherwise.
            - Evaluate new\_entries.append(entry).
- Set doc.share\_balance from list().
- For each entry in new\_entries.
  - Evaluate doc.append(“share\_balance”, entry).
- Set doc.flags.from\_share\_transfer from true.
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [return share balance entry](operations-108.md#op-2ea6c9814d4cff).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L183)

<a id="op-2ea6c9814d4cff"></a>
### Share Transfer.return share balance entry

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_return_share_balance_entry`

**Inputs** self, from\_no, to\_no, rate.

**Explicit results** mapping(“share\_type” → self.share\_type, “from\_no” → from\_no, “to\_no” → to\_no, “rate” → rate, …).

**Local steps**

- Return mapping(“share\_type” → self.share\_type, “from\_no” → from\_no, “to\_no” → to\_no, “rate” → rate, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L6167) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L184)

<a id="op-94976d6fcc091c"></a>
### Share Transfer.get shareholder doc

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_get_shareholder_record`

**Inputs** self, shareholder.

**Record and data access** read “Shareholder” via get\_value · resolve a document from “Shareholder” via get\_doc.

**Explicit results** Platform.get\_doc(“Shareholder”, name).

**Local steps**

- If shareholder.
  - Take no action here.
- Set name from Platform.db.get\_value(“Shareholder”, mapping(“name” → shareholder), “name”).
- Return Platform.get\_doc(“Shareholder”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L6370) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L180)

<a id="op-cefe93315abede"></a>
### Share Transfer.get company shareholder

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_get_company_shareholder`

**Inputs** self.

**Record and data access** read “Shareholder” via get\_value · resolve a document from “Shareholder” via get\_doc · resolve a document from mapping(“doctype” → “Shareholder”, “title” → self.company, “company” → self.company, “is\_company” → 1) via get\_doc.

**State and service calls** call insert on shareholder.

**Explicit results** Platform.get\_doc(“Shareholder”, company\_shareholder) · shareholder.

**Local steps**

- Set company\_shareholder from Platform.db.get\_value(“Shareholder”, mapping(“company” → self.company, “is\_company” → 1), “name”).
- If company\_shareholder.
  - Return Platform.get\_doc(“Shareholder”, company\_shareholder).
- Otherwise.
  - Set shareholder from Platform.get\_doc(mapping(“doctype” → “Shareholder”, “title” → self.company, “company” → self.company, “is\_company” → 1)).
  - Evaluate shareholder.insert().
  - Return shareholder.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L179)

<a id="op-c46747f1bf06dc"></a>
### Make jv entry

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_make_journal_voucher_entry`

**Inputs** company, account, amount, payment\_account, credit\_applicant\_type, credit\_applicant, debit\_applicant\_type, debit\_applicant.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** journal\_entry.as\_dict().

**Local steps**

- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.voucher\_type from “Journal Entry”.
- Set journal\_entry.company from company.
- Set journal\_entry.posting\_date from nowdate().
- Set account\_amt\_list from list().
- Evaluate account\_amt\_list.append(mapping(“account” → account, “debit\_in\_account\_currency” → amount, “party\_type” → debit\_applicant\_type, “party” → debit\_applicant)).
- Evaluate account\_amt\_list.append(mapping(“account” → payment\_account, “credit\_in\_account\_currency” → amount, “party\_type” → credit\_applicant\_type, “party” → credit\_applicant)).
- Evaluate journal\_entry.set(“accounts”, account\_amt\_list).
- Return journal\_entry.as\_dict().

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L175)

## Record · Share type

[Record definition](../../../../data/record-types/share_type.json)

<a id="op-eb69face3c3af1"></a>
### Get data

`operation_enterprise_accounts_record_definitions_share_type_share_type_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “share\_type”, “transactions” → list(mapping(“label” → translated “References”, “items” → list(“Share Transfer”, “Shareholder”)))).

**Local steps**

- Return mapping(“fieldname” → “share\_type”, “transactions” → list(mapping(“label” → translated “References”, “items” → list(“Share Transfer”, “Shareholder”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L3611) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L189)

## Record · Shareholder

[Record definition](../../../../data/record-types/shareholder.json)

<a id="op-cb5ea5002e2d86"></a>
### Shareholder.onload

`operation_enterprise_accounts_record_definitions_shareholder_business_behavior_shareholder_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L3745) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L192)

<a id="op-af415f256ebe65"></a>
### Shareholder.validate

`operation_enterprise_binding_enterprise_accounts_doctype_shareholder_shareholder_shareholder_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot change the company or company shareholder status while shares or submitted share transfers exist” · validation helper — translated “Share balances can only be changed through Share Transfer”.

**Local steps**

- If self.is\_new().
  - Set balance\_changed from bool(self.share\_balance).
- Otherwise.
  - Set balance\_changed from not self.is\_child\_table\_same(“share\_balance”).
  - Set previous from self.get\_doc\_before\_save().
  - If ((self.has\_value\_changed(“company”) or self.has\_value\_changed(“is\_company”)) and (previous.share\_balance or previous.has\_submitted\_share\_transfers())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.has\_value\_changed(“company”) or self.has\_value\_changed(“is\_company”)) → (previous.share\_balance or previous.has\_submitted\_share\_transfers()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“company”) → self.has\_value\_changed(“is\_company”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous.share\_balance → previous.has\_submitted\_share\_transfers().
    - Call the validation error handler Platform.throw(translated “Cannot change the company or company shareholder status while shares or submitted share transfers exist”, title = translated “Not Allowed”).
- If (balance\_changed and not self.flags.from\_share\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance\_changed → not self.flags.from\_share\_transfer.
  - Call the validation error handler Platform.throw(translated “Share balances can only be changed through Share Transfer”, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1079)

<a id="op-6f61bcdc283b79"></a>
### Shareholder.on trash

`operation_enterprise_accounts_record_definitions_shareholder_business_behavior_shareholder_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot delete a shareholder with shares or submitted share transfers”.

**Local steps**

- If (self.share\_balance or self.has\_submitted\_share\_transfers()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.share\_balance → self.has\_submitted\_share\_transfers().
  - Call the validation error handler Platform.throw(translated “Cannot delete a shareholder with shares or submitted share transfers”, title = translated “Not Allowed”).
- Evaluate delete\_contact\_and\_address(“Shareholder”, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has submitted share transfers](operations-108.md#op-22673a77309df9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L191)

<a id="op-bb674f8faa43fc"></a>
### Shareholder.before save

`operation_enterprise_accounts_record_definitions_shareholder_business_behavior_shareholder_before_save`

**Inputs** self.

**Local steps**

- For each entry in self.share\_balance.
  - Set entry.amount from (entry.no\_of\_shares × entry.rate).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L3864) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L190)

<a id="op-22673a77309df9"></a>
### Shareholder.has submitted share transfers

`operation_enterprise_binding_enterprise_accounts_doctype_shareholder_shareholder_shareholder_has_submitted_share_transfers`

**Inputs** self.

**Record and data access** read “Share Transfer” via get\_all.

**Explicit results** bool(Platform.get\_all(“Share Transfer”, filters = mapping(“docstatus” → 1), or\_filters = or\_filters, pluck = “name”, limit\_page\_length = 1)).

**Local steps**

- Set or\_filters from mapping(“from\_shareholder” → self.name, “to\_shareholder” → self.name).
- If self.is\_company.
  - Set or\_filters at “company” from self.company.
- Return bool(Platform.get\_all(“Share Transfer”, filters = mapping(“docstatus” → 1), or\_filters = or\_filters, pluck = “name”, limit\_page\_length = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1078)

<a id="op-fd335c67764adf"></a>
### Get data

`operation_enterprise_accounts_record_definitions_shareholder_shareholder_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “shareholder”, “non\_standard\_fieldnames” → mapping(“Share Transfer” → “to\_shareholder”), “transactions” → list(mapping(“items” → list(“Share Transfer”)))).

**Local steps**

- Return mapping(“fieldname” → “shareholder”, “non\_standard\_fieldnames” → mapping(“Share Transfer” → “to\_shareholder”), “transactions” → list(mapping(“items” → list(“Share Transfer”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L3948) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L193)

## Record · Shipping rule

[Record definition](../../../../data/record-types/shipping_rule.json)

<a id="op-e1eccdec95b625"></a>
### Shipping Rule.validate

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_account\_company().
- Evaluate self.validate\_from\_to\_values().
- Evaluate self.sort\_shipping\_rule\_conditions().
- Evaluate self.validate\_overlapping\_shipping\_rule\_conditions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account company](operations-108.md#op-1939eb6ce5d367), [validate from to values](operations-108.md#op-14872e04de337b), [sort shipping rule conditions](operations-109.md#op-10492c70e37277), [validate overlapping shipping rule conditions](operations-109.md#op-355953bc5485ae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L198)

<a id="op-1939eb6ce5d367"></a>
### Shipping Rule.validate account company

`operation_enterprise_binding_enterprise_accounts_doctype_shipping_rule_shipping_rule_shippingrule_validate_account_company`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (not self.company or not self.account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.company → not self.account.
  - Return no value.
- If Platform.get\_cached\_value(“Account”, self.account, “company”) differs from self.company.
  - Evaluate throw(translated “Shipping Account {0} does not belong to Company {1}”.format(Platform.bold(self.account), Platform.bold(self.company)), title = translated “Invalid Shipping Account”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1080)

<a id="op-14872e04de337b"></a>
### Shipping Rule.validate from to values

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_validate_from_to_values`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.calculate\_based\_on equals “Fixed”.
  - If self.conditions.
    - Evaluate self.set(“conditions”, list()).
  - Return no value.
- Set zero\_to\_values from list().
- For each d in self.get(“conditions”).
  - Evaluate self.round\_floats\_in(d).
  - Evaluate self.validate\_value(“from\_value”, “&gt;=”, 0.0, d).
  - Evaluate self.validate\_value(“to\_value”, “&gt;=”, 0.0, d).
  - If not d.to\_value.
    - Evaluate zero\_to\_values.append(d).
  - Otherwise.
    - If d.from\_value ≥ d.to\_value.
      - Evaluate throw(translated “From value must be less than to value in row {0}”.format(d.idx), FromGreaterThanToError).
- If len(zero\_to\_values) ≥ 2.
  - Evaluate throw(translated “There can only be one Shipping Rule Condition with 0 or blank value for "To Value"”, ManyBlankToValuesError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L4161) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L200)

<a id="op-83f45ec6397919"></a>
### Shipping Rule.apply

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_apply`

**Inputs** self, doc.

**Local steps**

- Set shipping\_amount from 0.0.
- Set by\_value from false.
- If doc.get\_shipping\_address().
  - Evaluate self.validate\_countries(doc).
- If self.calculate\_based\_on equals “Net Total”.
  - Set value from doc.base\_net\_total.
  - Set by\_value from true.
- Otherwise.
  - If self.calculate\_based\_on equals “Net Weight”.
    - Set value from doc.total\_net\_weight.
    - Set by\_value from true.
  - Otherwise.
    - If self.calculate\_based\_on equals “Fixed”.
      - Set shipping\_amount from self.shipping\_amount.
- If by\_value.
  - Set shipping\_amount from self.get\_shipping\_amount\_from\_rules(value).
- If doc.currency differs from doc.company\_currency.
  - Set shipping\_amount from flt((shipping\_amount ÷ doc.conversion\_rate), 2).
- Evaluate self.add\_shipping\_rule\_to\_tax\_table(doc, shipping\_amount).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate countries](operations-108.md#op-f038b9f80d2646), [get shipping amount from rules](operations-108.md#op-d331a91f5b66ca), [add shipping rule to tax table](operations-108.md#op-4d67980da01ef2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L4626) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L195)

<a id="op-d331a91f5b66ca"></a>
### Shipping Rule.get shipping amount from rules

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_get_shipping_amount_from_rules`

**Inputs** self, value.

**Explicit results** condition.shipping\_amount · 0.0.

**Local steps**

- For each condition in self.get(“conditions”).
  - If (not condition.to\_value or flt(condition.from\_value) ≤ flt(value) ≤ flt(condition.to\_value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not condition.to\_value → flt(condition.from\_value) ≤ flt(value) ≤ flt(condition.to\_value).
    - Compare adjacent operands in order, stopping at the first false comparison in flt(condition.from\_value) ≤ flt(value) ≤ flt(condition.to\_value).
    - Return condition.shipping\_amount.
- Return 0.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L5035) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L196)

<a id="op-f038b9f80d2646"></a>
### Shipping Rule.validate countries

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_validate_countries`

**Inputs** self, doc.

**Explicit failure paths** validation helper — translated “Shipping Address does not have country, which is required for this Shipping Rule” · validation helper — translated “Shipping rule not applicable for country {0} in Shipping Address”.format(shipping\_country).

**Local steps**

- If self.countries.
  - Set shipping\_country from doc.get\_shipping\_address().get(“country”).
  - If not shipping\_country.
    - Call the validation error handler Platform.throw(translated “Shipping Address does not have country, which is required for this Shipping Rule”).
  - If shipping\_country does not belong to list of d.country for d drawn from self.countries.
    - Draw d from self.countries.
    - Call the validation error handler Platform.throw(translated “Shipping rule not applicable for country {0} in Shipping Address”.format(shipping\_country)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L5216) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L199)

<a id="op-4d67980da01ef2"></a>
### Shipping Rule.add shipping rule to tax table

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_add_shipping_rule_to_tax_table`

**Inputs** self, doc, shipping\_amount.

**Explicit failure paths** validation helper — translated “Shipping rule only applicable for Selling” · validation helper — translated “Shipping rule only applicable for Buying”.

**Local steps**

- Set shipping\_charge from mapping(“charge\_type” → “Actual”, “account\_head” → self.account, “cost\_center” → self.cost\_center).
- If self.shipping\_rule\_type equals “Selling”.
  - If doc.meta.get\_field(“taxes”).options differs from “Sales Taxes and Charges”.
    - Call the validation error handler Platform.throw(translated “Shipping rule only applicable for Selling”).
  - Set shipping\_charge at “doctype” from “Sales Taxes and Charges”.
- Otherwise.
  - If doc.meta.get\_field(“taxes”).options differs from “Purchase Taxes and Charges”.
    - Call the validation error handler Platform.throw(translated “Shipping rule only applicable for Buying”).
  - Set shipping\_charge at “doctype” from “Purchase Taxes and Charges”.
  - Set shipping\_charge at “category” from “Valuation and Total” when (doc.get\_stock\_items() or doc.get\_asset\_items()), otherwise “Total”.
    - Value choice on (doc.get\_stock\_items() or doc.get\_asset\_items()) — true gives “Valuation and Total”, false gives “Total”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_stock\_items() → doc.get\_asset\_items().
  - Set shipping\_charge at “add\_deduct\_tax” from “Add”.
- Set shipping\_charge\_filters from shipping\_charge.copy().
- If not self.cost\_center.
  - Set shipping\_charge\_filters at “cost\_center” from tuple(“in”, tuple(no value, empty text, Enterprise.get\_default\_cost\_center(doc.company))).
- Set existing\_shipping\_charge from doc.get(“taxes”, filters = shipping\_charge\_filters).
- If existing\_shipping\_charge.
  - Set existing\_shipping\_charge at negative 1.tax\_amount from shipping\_amount.
- Otherwise.
  - Set shipping\_charge at “tax\_amount” from shipping\_amount.
  - Set shipping\_charge at “description” from self.label.
  - Evaluate doc.append(“taxes”, shipping\_charge).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L5468) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L194)
