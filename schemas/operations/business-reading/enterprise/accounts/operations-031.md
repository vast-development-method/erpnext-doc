# Accounting and settlement · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Cost center allocation

[Record definition](../../../../data/record-types/cost_center_allocation.json)

<a id="op-151812f9f8186d"></a>
### Cost Center Allocation.validate allocation percentages

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_allocation_cost_center_allocation_costcenterallocation_validate_allocation_percentages`

**Inputs** self.

**Explicit failure paths** validation helper with WrongPercentageAllocation — translated “Row #{0}: Percentage (%) for Cost Center {1} must be greater than 0”.format(row.idx, Platform.bold(row.cost\_center)).

**Local steps**

- For each row in self.get(“allocation\_percentages”, list()).
  - If flt(row.percentage) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Percentage (%) for Cost Center {1} must be greater than 0”.format(row.idx, Platform.bold(row.cost\_center)), WrongPercentageAllocation).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L776)

<a id="op-6b306b8c3b5ad4"></a>
### Cost Center Allocation.validate total allocation percentage

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_validate_total_allocation_percentage`

**Inputs** self.

**Explicit failure paths** validation helper with WrongPercentageAllocation — translated “Total percentage against cost centers should be 100”.

**Local steps**

- Set total\_percentage from sum(generator of Decimal(str(flt(d.percentage))) for d drawn from self.get(“allocation\_percentages”, list())).
  - Draw d from self.get(“allocation\_percentages”, list()).
- <a id="op-6b306b8c3b5ad4-guard-6"></a>If total\_percentage differs from 100.
  - Call the validation error handler Platform.throw(translated “Total percentage against cost centers should be 100”, WrongPercentageAllocation).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison total\_percentage differs from 100, total\_percentage = 101 selects the branch that calls the validation-error handler with translated “Total percentage against cost centers should be 100”. With total\_percentage = 100, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6b306b8c3b5ad4-guard-6)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L665)

<a id="op-0ee6acbe7eaf7b"></a>
### Cost Center Allocation.validate from date based on existing gle

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_validate_from_date_based_on_existing_general_ledger_entry`

**Inputs** self.

**Record and data access** read “GL Entry” via get\_value.

**Explicit failure paths** validation helper with InvalidDateError — translated “Valid From must be after {0} as last GL Entry against the cost center {1} posted on this date”.format(last\_gle\_date, self.main\_cost\_center).

**Local steps**

- Set last\_gle\_date from Platform.db.get\_value(“GL Entry”, mapping(“cost\_center” → self.main\_cost\_center, “is\_cancelled” → 0), “posting\_date”, order\_by = “posting\_date desc”).
- If last\_gle\_date.
  - If getdate(self.valid\_from) ≤ getdate(last\_gle\_date).
    - Call the validation error handler Platform.throw(translated “Valid From must be after {0} as last GL Entry against the cost center {1} posted on this date”.format(last\_gle\_date, self.main\_cost\_center), InvalidDateError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L2376) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L663)

<a id="op-a30550b4546b8e"></a>
### Cost Center Allocation.validate duplicate allocation

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_allocation_cost_center_allocation_costcenterallocation_validate_duplicate_allocation`

**Inputs** self.

**Record and data access** read “Cost Center Allocation” via get\_value.

**Explicit failure paths** validation helper with DuplicateCostCenterAllocation — translated “Cost Center Allocation {0} for {1} is already valid from {2}”.format(get\_link\_to\_form(“Cost Center Allocation”, duplicate\_allocation), Platform.bold(self.main\_cost\_center), Platform.bold(format ….

**Local steps**

- Set duplicate\_allocation from Platform.db.get\_value(“Cost Center Allocation”, mapping(“main\_cost\_center” → self.main\_cost\_center, “valid\_from” → self.valid\_from, “name” → tuple(“!=”, self.name), “docstatus” → 1)).
- If duplicate\_allocation.
  - Call the validation error handler Platform.throw(translated “Cost Center Allocation {0} for {1} is already valid from {2}”.format(get\_link\_to\_form(“Cost Center Allocation”, duplicate\_allocation), Platform.bold(self.main\_cost\_center), Platf ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L778)

<a id="op-fec4878cb13383"></a>
### Cost Center Allocation.validate backdated allocation

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_validate_backdated_allocation`

**Inputs** self.

**Record and data access** read “Cost Center Allocation” via get\_value.

**State and service calls** msgprint with translated “Another Cost Center Allocation record {0} applicable from {1}, hence this allocation will be applicable upto {2}”.format(Platform.bold(future\_allocation.name), Platform.bold(format\_date(future\_ ….

**Local steps**

- Set future\_allocation from Platform.db.get\_value(“Cost Center Allocation”, filters = mapping(“main\_cost\_center” → self.main\_cost\_center, “valid\_from” → tuple(“&gt;=”, self.valid\_from), “name” → tuple(“!=”, self.name), “docstatus” → 1), ….
- If future\_allocation.
  - Evaluate Platform.msgprint(translated “Another Cost Center Allocation record {0} applicable from {1}, hence this allocation will be applicable upto {2}”.format(Platform.bold(future\_allocation.name), Platform.bold(f ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L2636) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L661)

<a id="op-1023e96a6c6466"></a>
### Cost Center Allocation.validate cost centers

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_allocation_cost_center_allocation_costcenterallocation_validate_cost_centers`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_all.

**Explicit failure paths** validation helper with exception — error.

**Local steps**

- Set cost\_centers from list(self.main\_cost\_center, expanded list of d.cost\_center for d drawn from self.allocation\_percentages).
  - Draw d from self.allocation\_percentages.
- For each cost\_center in Platform.get\_all(“Cost Center”, filters = mapping(“name” → tuple(“in”, cost\_centers)), fields = list(“name”, “company”, “is\_group”, “disabled”)).
  - If error bound to self.get\_cost\_center\_error(cost\_center).
    - Set exception from InvalidMainCostCenter when cost\_center.name equals self.main\_cost\_center, otherwise InvalidChildCostCenter.
      - Value choice on cost\_center.name equals self.main\_cost\_center — true gives InvalidMainCostCenter, false gives InvalidChildCostCenter.
    - Call the validation error handler Platform.throw(error, exception).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get cost center error](operations-031.md#op-64d111b66e55ed).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L777)

<a id="op-64d111b66e55ed"></a>
### Cost Center Allocation.get cost center error

`operation_enterprise_binding_enterprise_accounts_doctype_cost_center_allocation_cost_center_allocation_costcenterallocation_get_cost_center_error`

**Inputs** self, cost\_center.

**Explicit results** translated “Cost Center {0} does not belong to Company {1}”.format(Platform.bold(cost\_center.name), Platform.bold(self.company)) · translated “Cost Center {0} is a group cost center and cannot be used in an allocation”.format(Platform.bold(cost\_center.name)) · translated “Cost Center {0} is disabled”.format(Platform.bold(cost\_center.name)).

**Local steps**

- If cost\_center.company differs from self.company.
  - Return translated “Cost Center {0} does not belong to Company {1}”.format(Platform.bold(cost\_center.name), Platform.bold(self.company)).
- If cost\_center.is\_group.
  - Return translated “Cost Center {0} is a group cost center and cannot be used in an allocation”.format(Platform.bold(cost\_center.name)).
- If cost\_center.disabled.
  - Return translated “Cost Center {0} is disabled”.format(Platform.bold(cost\_center.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L775)

<a id="op-64a79979795cca"></a>
### Cost Center Allocation.validate main cost center

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_validate_main_cost_center`

**Inputs** self.

**Record and data access** read “Cost Center Allocation Percentage” via get\_value.

**Explicit failure paths** validation helper with MainCostCenterCantBeChild — translated “Main Cost Center {0} cannot be entered in the child table”.format(self.main\_cost\_center) · validation helper with InvalidMainCostCenter — translated “{0} cannot be used as a Main Cost Center because it has been used as child in Cost Center Allocation {1}”.format(self.main\_cost\_center, parent).

**Local steps**

- If self.main\_cost\_center belongs to list of d.cost\_center for d drawn from self.allocation\_percentages.
  - Draw d from self.allocation\_percentages.
  - Call the validation error handler Platform.throw(translated “Main Cost Center {0} cannot be entered in the child table”.format(self.main\_cost\_center), MainCostCenterCantBeChild).
- Set parent from Platform.db.get\_value(“Cost Center Allocation Percentage”, filters = mapping(“cost\_center” → self.main\_cost\_center, “docstatus” → 1), fieldname = “parent”).
- If parent.
  - Call the validation error handler Platform.throw(translated “{0} cannot be used as a Main Cost Center because it has been used as child in Cost Center Allocation {1}”.format(self.main\_cost\_center, parent), InvalidMainCostCenter).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L3096) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L664)

<a id="op-40aa36228726fb"></a>
### Cost Center Allocation.validate child cost centers

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_validate_child_cost_centers`

**Inputs** self.

**Record and data access** read “Cost Center Allocation” via get\_all.

**Explicit failure paths** validation helper with InvalidChildCostCenter — translated “Cost Center {0} cannot be used for allocation as it is used as main cost center in other allocation record.”.format(d.cost\_center).

**Local steps**

- Set main\_cost\_centers from list of d.main\_cost\_center for d drawn from Platform.get\_all(“Cost Center Allocation”, mapping(“docstatus” → 1), “main\_cost\_center”).
  - Draw d from Platform.get\_all(“Cost Center Allocation”, mapping(“docstatus” → 1), “main\_cost\_center”).
- For each d in self.allocation\_percentages.
  - If d.cost\_center belongs to main\_cost\_centers.
    - Call the validation error handler Platform.throw(translated “Cost Center {0} cannot be used for allocation as it is used as main cost center in other allocation record.”.format(d.cost\_center), InvalidChildCostCenter).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L3416) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L662)

<a id="op-0aebfe8036dc81"></a>
### Cost Center Allocation.clear cache

`operation_enterprise_accounts_record_definitions_cost_center_allocation_business_behavior_cost_center_allocation_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate Platform.clear\_cache(doctype = “Cost Center”).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0038.json#L3644) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L658)

## Record · Coupon code

[Record definition](../../../../data/record-types/coupon_code.json)

<a id="op-1ef563eb62f895"></a>
### Coupon Code.autoname

`operation_enterprise_accounts_record_definitions_coupon_code_business_behavior_coupon_code_autoname`

**Inputs** self.

**Record and data access** read “Coupon Code” via exists.

**Local steps**

- Set self.coupon\_name from strip(self.coupon\_name).
- Set self.name from self.coupon\_name.
- If not self.coupon\_code.
  - If self.coupon\_type equals “Promotional”.
    - Set prefix from empty text.join(generator of c for c drawn from self.coupon\_name where not (nested operand in the contract or nested operand in the contract)) at slice no value to 8.upper().
      - Draw c from self.coupon\_name, keep a combination only if (not (c.isdigit() or c.isspace())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.isdigit() → c.isspace().
    - Set self.coupon\_code from prefix.
    - While (not self.coupon\_code or Platform.db.exists(“Coupon Code”, mapping(“coupon\_code” → self.coupon\_code))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.coupon\_code → Platform.db.exists(“Coupon Code”, mapping(“coupon\_code” → self.coupon\_code)).
      - Set self.coupon\_code from (prefix + Platform.generate\_hash(length = 6).upper()).
  - Otherwise.
    - If self.coupon\_type equals “Gift Card”.
      - Set self.coupon\_code from Platform.generate\_hash() at slice no value to 10.upper().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 6), Platform.generate\_hash().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L693)

<a id="op-4655bac1c8c560"></a>
### Coupon Code.validate

`operation_enterprise_accounts_record_definitions_coupon_code_business_behavior_coupon_code_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select the customer.”.

**Local steps**

- Evaluate self.validate\_from\_to\_dates(“valid\_from”, “valid\_upto”).
- Evaluate self.validate\_pricing\_rule().
- <a id="op-4655bac1c8c560-guard-5"></a>If self.coupon\_type equals “Gift Card”.
  - Set self.maximum\_use from 1.
  - If not self.customer.
    - Call the validation error handler Platform.throw(translated “Please select the customer.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.coupon\_type equals “Gift Card”, self.coupon\_type = “Gift Card” selects the branch that assigns 1 to self.maximum\_use. With self.coupon\_type = “Promotional”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4655bac1c8c560-guard-5)

**Methods declared on this owner** [validate pricing rule](operations-031.md#op-495a88667ca60b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L694)

<a id="op-495a88667ca60b"></a>
### Coupon Code.validate pricing rule

`operation_enterprise_binding_enterprise_accounts_doctype_coupon_code_coupon_code_couponcode_validate_pricing_rule`

**Inputs** self.

**Record and data access** read “Pricing Rule” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Pricing Rule {0} is disabled”.format(Platform.bold(self.pricing\_rule)).

**Local steps**

- If (not self.pricing\_rule or self.from\_external\_ecomm\_platform).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.pricing\_rule → self.from\_external\_ecomm\_platform.
  - Return no value.
- If not (self.has\_value\_changed(“pricing\_rule”) or self.has\_value\_changed(“from\_external\_ecomm\_platform”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“pricing\_rule”) → self.has\_value\_changed(“from\_external\_ecomm\_platform”).
  - Return no value.
- If Platform.db.get\_value(“Pricing Rule”, self.pricing\_rule, “disable”).
  - Call the validation error handler Platform.throw(translated “Pricing Rule {0} is disabled”.format(Platform.bold(self.pricing\_rule))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L782)

## Record · Currency exchange settings

[Record definition](../../../../data/record-types/currency_exchange_settings.json)

<a id="op-6f1f760395e8e4"></a>
### Currency Exchange Settings.validate

`operation_enterprise_accounts_record_definitions_currency_exchange_settings_business_behavior_currency_exchange_settings_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate self.set\_parameters\_and\_result().
- If (Platform.in\_test or Platform.flags.in\_install or Platform.flags.in\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → Platform.flags.in\_install → Platform.flags.in\_setup\_wizard.
  - Return no value.
- Set tuple(response, value) from self.validate\_parameters().
- Evaluate self.validate\_result(response, value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set parameters and result](operations-031.md#op-b0eec8a3d5ac7c), [validate parameters](operations-031.md#op-ed04635c27bcf3), [validate result](operations-031.md#op-277b81b5ae7aeb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0039.json#L4439) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L700)

<a id="op-7a62a0387c0b49"></a>
### Currency Exchange Settings.on update

`operation_enterprise_binding_enterprise_accounts_doctype_currency_exchange_settings_currency_exchange_settings_currencyexchangesettings_on_update`

**Inputs** self.

**Local steps**

- Bind local operation clear\_rates for subsequent calls.
- Evaluate clear\_rates().
- Evaluate Platform.db.after\_commit.add(clear\_rates).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L783)

<a id="op-348d8dbde9830b"></a>
### Currency Exchange Settings.on update.clear rates

`operation_enterprise_binding_enterprise_accounts_doctype_currency_exchange_settings_currency_exchange_settings_currencyexchangesettings_on_update_clear_rates`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.cache.delete\_keys(“currency\_exchange\_rate\_”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L784)

<a id="op-b0eec8a3d5ac7c"></a>
### Currency Exchange Settings.set parameters and result

`operation_enterprise_accounts_record_definitions_currency_exchange_settings_business_behavior_currency_exchange_settings_set_parameters_and_result`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Access Key is required for Service Provider: {0}”.format(Platform.bold(self.service\_provider)).

**Local steps**

- If self.service\_provider equals “exchangerate.host”.
  - If not self.access\_key.
    - Call the validation error handler Platform.throw(translated “Access Key is required for Service Provider: {0}”.format(Platform.bold(self.service\_provider))).
  - Evaluate self.set(“result\_key”, list()).
  - Evaluate self.set(“req\_params”, list()).
  - Set self.api\_endpoint from get\_api\_endpoint(self.service\_provider, self.use\_http).
  - Evaluate self.append(“result\_key”, mapping(“key” → “result”)).
  - Evaluate self.append(“req\_params”, mapping(“key” → “access\_key”, “value” → self.access\_key)).
  - Evaluate self.append(“req\_params”, mapping(“key” → “amount”, “value” → “1”)).
  - Evaluate self.append(“req\_params”, mapping(“key” → “date”, “value” → “{transaction\_date}”)).
  - Evaluate self.append(“req\_params”, mapping(“key” → “from”, “value” → “{from\_currency}”)).
  - Evaluate self.append(“req\_params”, mapping(“key” → “to”, “value” → “{to\_currency}”)).
- Otherwise.
  - If self.service\_provider belongs to tuple(“frankfurter.dev”, “frankfurter.app”).
    - Evaluate self.set(“result\_key”, list()).
    - Evaluate self.set(“req\_params”, list()).
    - Set self.api\_endpoint from get\_api\_endpoint(self.service\_provider, self.use\_http).
    - Evaluate self.append(“result\_key”, mapping(“key” → “rates”)).
    - Evaluate self.append(“result\_key”, mapping(“key” → “{to\_currency}”)).
    - Evaluate self.append(“req\_params”, mapping(“key” → “base”, “value” → “{from\_currency}”)).
    - Evaluate self.append(“req\_params”, mapping(“key” → “symbols”, “value” → “{to\_currency}”)).
  - Otherwise.
    - If self.service\_provider equals “frankfurter.dev - v2”.
      - Evaluate self.set(“result\_key”, list()).
      - Evaluate self.set(“req\_params”, list()).
      - Set self.api\_endpoint from get\_api\_endpoint(self.service\_provider, self.use\_http).
      - Evaluate self.append(“result\_key”, mapping(“key” → “rate”)).
      - Evaluate self.append(“req\_params”, mapping(“key” → “date”, “value” → “{transaction\_date}”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0039.json#L4604) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L699)

<a id="op-ed04635c27bcf3"></a>
### Currency Exchange Settings.validate parameters

`operation_enterprise_accounts_record_definitions_currency_exchange_settings_business_behavior_currency_exchange_settings_validate_parameters`

**Inputs** self.

**Explicit results** tuple(response, value).

**Explicit failure paths** validation helper — (“Error: ” + str(e)).

**Local steps**

- Set params from mapping().
- For each row in self.req\_params.
  - Set params at row.key from row.value.format(transaction\_date = nowdate(), to\_currency = “INR”, from\_currency = “USD”).
- Set api\_url from self.api\_endpoint.format(transaction\_date = nowdate(), to\_currency = “INR”, from\_currency = “USD”).
- Attempt the following.
  - Set response from requests.get(api\_url, params = params, timeout = (Platform.conf.get(“currency\_exchange\_request\_timeout”) or 10)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“currency\_exchange\_request\_timeout”) → 10.
- On failure (requests.exceptions.RequestException) bound to e.
  - Call the validation error handler Platform.throw((“Error: ” + str(e))).
- Evaluate response.raise\_for\_status().
- Set value from response.json().
- Return tuple(response, value).

**Values supplied outside this operation** clock or generated value from nowdate() · service or queued work from requests.get(api\_url, params = params, timeout = (Platform.conf.get(“currency\_exchange\_request\_timeout”) or 10)).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L701)

<a id="op-277b81b5ae7aeb"></a>
### Currency Exchange Settings.validate result

`operation_enterprise_accounts_record_definitions_currency_exchange_settings_business_behavior_currency_exchange_settings_validate_result`

**Inputs** self, response, value.

**Explicit failure paths** validation helper — ((translated “Invalid result key. Response:” + one space) + response.text) · validation helper — translated “Returned exchange rate must be a positive finite number.”.

**Local steps**

- Attempt the following.
  - For each key in self.result\_key.
    - Set value from value at str(key.key).format(transaction\_date = nowdate(), to\_currency = “INR”, from\_currency = “USD”).
- On failure (Exception).
  - Call the validation error handler Platform.throw(((translated “Invalid result key. Response:” + one space) + response.text)).
- If (isinstance(value, bool) or not isinstance(value, (int bitwise or float)) or not isfinite(value) or value ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(value, bool) → not isinstance(value, (int bitwise or float)) → not isfinite(value) → value ≤ 0.
  - Call the validation error handler Platform.throw(translated “Returned exchange rate must be a positive finite number.”).
- Set self.url from response.url.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L702)

<a id="op-83c5f7dcced087"></a>
### Get api endpoint

`operation_enterprise_accounts_record_definitions_currency_exchange_settings_business_behavior_get_application_programming_interface_endpoint`

**Inputs** service\_provider = no value, use\_http = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** (protocol + api) · no value.

**Local steps**

- If (service\_provider and service\_provider belongs to list(“exchangerate.host”, “frankfurter.dev”, “frankfurter.app”, “frankfurter.dev - v2”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in service\_provider → service\_provider belongs to list(“exchangerate.host”, “frankfurter.dev”, “frankfurter.app”, “frankfurter.dev - v2”).
  - If service\_provider equals “exchangerate.host”.
    - Set api from “api.exchangerate.host/convert”.
  - Otherwise.
    - If service\_provider equals “frankfurter.app”.
      - Set api from “api.frankfurter.app/{transaction\_date}”.
    - Otherwise.
      - If service\_provider equals “frankfurter.dev”.
        - Set api from “api.frankfurter.dev/v1/{transaction\_date}”.
      - Otherwise.
        - If service\_provider equals “frankfurter.dev - v2”.
          - Set api from “api.frankfurter.dev/v2/rate/{from\_currency}/{to\_currency}”.
  - Set protocol from text in the contract.
  - If use\_http.
    - Set protocol from text in the contract.
  - Return (protocol + api).
- Return no value.

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0039.json#L6629) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L703)

## Report · Custom financial statement

<a id="op-b3c30cbf16b389"></a>
### Execute

`operation_enterprise_accounts_report_custom_financial_statement_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** FinancialReportEngine().execute(filters).

**Local steps**

- If (filters and filters.report\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.report\_template.
  - Return FinancialReportEngine().execute(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L4607) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L814)

## Report · Customer ledger summary

<a id="op-802773237f8fe7"></a>
### Party Ledger Summary Report.initialize

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.filters.from\_date from getdate((self.filters.from\_date or nowdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.from\_date → nowdate().
- Set self.filters.to\_date from getdate((self.filters.to\_date or nowdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.to\_date → nowdate().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L6066) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L829)

<a id="op-697ae79ea7d241"></a>
### Party Ledger Summary Report.run

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_run`

**Inputs** self, args.

**Record and data access** read args.get(“naming\_by”) at 0 via get\_single\_value.

**Explicit results** tuple(list(), list()) · tuple(columns, data).

**Local steps**

- Set self.filters.party\_type from args.get(“party\_type”).
- Evaluate self.validate\_filters().
- Evaluate self.get\_party\_details().
- If not self.parties.
  - Return tuple(list(), list()).
- Evaluate self.get\_gl\_entries().
- Evaluate self.get\_return\_invoices().
- Evaluate self.get\_party\_adjustment\_amounts().
- Set self.party\_naming\_by from Platform.db.get\_single\_value(args.get(“naming\_by”) at 0, args.get(“naming\_by”) at 1).
- Set columns from self.get\_columns().
- Set data from self.get\_data().
- Return tuple(columns, data).

**Methods declared on this owner** [validate filters](operations-031.md#op-59d6b8289c0bf7), [get party details](operations-032.md#op-6dde74d8fa691f), [get gl entries](operations-032.md#op-78636530254299), [get return invoices](operations-032.md#op-59bec48e68abee), [get party adjustment amounts](operations-032.md#op-d7d77154923cfe), [get columns](operations-032.md#op-0916f626c4d7e9), [get data](operations-032.md#op-f07d0cf9a1cbbb).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(args.get(“naming\_by”) at 0, args.get(“naming\_by”) at 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L6273) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L831)

<a id="op-59d6b8289c0bf7"></a>
### Party Ledger Summary Report.validate filters

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”) · validation helper — translated “From Date must be before To Date”.

**Local steps**

- Evaluate validate\_date\_range(self.filters).
- If not self.filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- If self.filters.from\_date &gt; self.filters.to\_date.
  - Call the validation error handler Platform.throw(translated “From Date must be before To Date”).
- Evaluate self.update\_hierarchical\_filters().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update hierarchical filters](operations-032.md#op-90e09db4014583).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L833)
