# Sales relationships · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Appointment booking settings

[Record definition](../../../../data/record-types/appointment_booking_settings.json)

<a id="op-0f932cdadd69b9"></a>
### Appointment Booking Settings.validate appointment scheduling

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_appointment_scheduling`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.enable\_scheduling.
  - Return no value.
- Evaluate self.validate\_availability\_of\_slots().
- Evaluate self.validate\_holiday\_list().
- Evaluate self.validate\_advance\_booking\_days().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate availability of slots](operations-003.md#op-db3e28c9bc4bed), [validate holiday list](operations-003.md#op-1ac7b52a726df6), [validate advance booking days](operations-003.md#op-2f1892c7afd034).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0427.json#L4538) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1033)

<a id="op-db3e28c9bc4bed"></a>
### Appointment Booking Settings.validate availability of slots

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_availability_of_slots`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please fill up the Availability of Slots table to enable Appointment Scheduling.”.

**Local steps**

- If not self.availability\_of\_slots.
  - Call the validation error handler Platform.throw(translated “Please fill up the Availability of Slots table to enable Appointment Scheduling.”).
- Set format\_string from “%Y-%m-%d %H:%M:%S”.
- For each record in self.availability\_of\_slots.
  - Set from\_time from datetime.datetime.strptime(formatted text 1970-01-01 {record.from\_time}, format\_string).
  - Set to\_time from datetime.datetime.strptime(formatted text 1970-01-01 {record.to\_time}, format\_string).
  - Evaluate self.validate\_from\_and\_to\_time(from\_time, to\_time, record).
  - Evaluate self.duration\_is\_divisible(from\_time, to\_time).
- Evaluate self.validate\_no\_overlapping\_slots().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate from and to time](operations-003.md#op-db2ece244fcfe8), [duration is divisible](operations-003.md#op-975ebbdbe7eb7d), [validate no overlapping slots](operations-003.md#op-196f89ea680153).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1034)

<a id="op-196f89ea680153"></a>
### Appointment Booking Settings.validate no overlapping slots

`operation_enterprise_binding_enterprise_crm_doctype_appointment_booking_settings_appointment_booking_settings_appointmentbookingsettings_validate_no_overlapping_slots`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Availability slots for {0} cannot overlap: rows {1} and {2}”.format(translated current.day\_of\_week, previous.idx, current.idx).

**Local steps**

- Set slots from sorted(self.availability\_of\_slots, key = deferred anonymous expression).
- For each tuple(previous, current) in pairwise(slots).
  - Set same\_day from previous.day\_of\_week equals current.day\_of\_week.
  - If (same\_day and to\_timedelta(current.from\_time) &lt; to\_timedelta(previous.to\_time)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in same\_day → to\_timedelta(current.from\_time) &lt; to\_timedelta(previous.to\_time).
    - Call the validation error handler Platform.throw(translated “Availability slots for {0} cannot overlap: rows {1} and {2}”.format(translated current.day\_of\_week, previous.idx, current.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L477)

<a id="op-db2ece244fcfe8"></a>
### Appointment Booking Settings.validate from and to time

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_from_and_to_time`

**Inputs** self, from\_time, to\_time, record.

**Explicit failure paths** validation helper — translated err\_msg.

**Local steps**

- If from\_time &gt; to\_time.
  - Set err\_msg from translated text in the contract.format(record.day\_of\_week).
  - Call the validation error handler Platform.throw(translated err\_msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1035)

<a id="op-975ebbdbe7eb7d"></a>
### Appointment Booking Settings.duration is divisible

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_duration_is_divisible`

**Inputs** self, from\_time, to\_time.

**Explicit failure paths** validation helper — translated “The difference between from time and To Time must be a multiple of Appointment”.

**Local steps**

- Set timedelta from (to\_time − from\_time).
- If (timedelta.total\_seconds() modulo or format (self.appointment\_duration × 60)).
  - Call the validation error handler Platform.throw(translated “The difference between from time and To Time must be a multiple of Appointment”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0427.json#L5096) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1030)

<a id="op-1ac7b52a726df6"></a>
### Appointment Booking Settings.validate holiday list

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_holiday_list`

**Inputs** self.

**Record and data access** read “Holiday List” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Please select a Holiday List to enable Appointment Scheduling.” · validation helper — translated “Holiday List - {0} is not valid for current date.”.format(self.holiday\_list).

**Local steps**

- If not self.holiday\_list.
  - Call the validation error handler Platform.throw(translated “Please select a Holiday List to enable Appointment Scheduling.”).
- Set tuple(hl\_from\_date, hl\_to\_date) from Platform.get\_cached\_value(“Holiday List”, self.holiday\_list, list(“from\_date”, “to\_date”)).
- Set now from getdate().
- If not (now ≥ hl\_from\_date and now ≤ hl\_to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in now ≥ hl\_from\_date → now ≤ hl\_to\_date.
  - Call the validation error handler Platform.throw(translated “Holiday List - {0} is not valid for current date.”.format(self.holiday\_list)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Holiday List”, self.holiday\_list, list(“from\_date”, “to\_date”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0427.json#L5243) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1036)

<a id="op-2f1892c7afd034"></a>
### Appointment Booking Settings.validate advance booking days

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_advance_booking_days`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Advance Booking Days is mandatory for Appointment Scheduling.”.

**Local steps**

- If not self.advance\_booking\_days.
  - Call the validation error handler Platform.throw(translated “Advance Booking Days is mandatory for Appointment Scheduling.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0427.json#L5533) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1032)

<a id="op-aa95ef1494ba5d"></a>
### Appointment Booking Settings.validate portal booking

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_portal_booking`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Appointment Scheduling needs to be enabled for Appointment Booking through portal.”.

**Local steps**

- If not self.enable\_appointment\_portal.
  - Return no value.
- If not self.enable\_scheduling.
  - Call the validation error handler Platform.throw(translated “Appointment Scheduling needs to be enabled for Appointment Booking through portal.”).
- Evaluate self.validate\_link\_expiry\_duration().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate link expiry duration](operations-003.md#op-5a3d805c1502ef).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0427.json#L5621) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1038)

<a id="op-5a3d805c1502ef"></a>
### Appointment Booking Settings.validate link expiry duration

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate_link_expiry_duration`

**Inputs** self.

**Explicit failure paths** validation helper — translated “'Verification Link Expiry Duration' must be between 15 to 60 minutes.”.

**Local steps**

- If (not self.verification\_link\_expiry\_duration or self.verification\_link\_expiry\_duration &gt; 60 or self.verification\_link\_expiry\_duration &lt; 15).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.verification\_link\_expiry\_duration → self.verification\_link\_expiry\_duration &gt; 60 → self.verification\_link\_expiry\_duration &lt; 15.
  - Call the validation error handler Platform.throw(translated “'Verification Link Expiry Duration' must be between 15 to 60 minutes.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0427.json#L5753) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1037)

## Record · Campaign

[Record definition](../../../../data/record-types/campaign.json)

<a id="op-7fd7b3b444363b"></a>
### Campaign.after insert

`operation_enterprise_customer_relationship_management_record_definitions_campaign_business_behavior_campaign_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.sync\_utm\_campaign().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync utm campaign](operations-003.md#op-18cc39b50a3927).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L1259) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1128)

<a id="op-83367d09ea300c"></a>
### Campaign.on change

`operation_enterprise_customer_relationship_management_record_definitions_campaign_business_behavior_campaign_on_change`

**Inputs** self.

**Local steps**

- If not self.flags.in\_delete.
  - Evaluate self.sync\_utm\_campaign().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync utm campaign](operations-003.md#op-18cc39b50a3927).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1131)

<a id="op-e70582cc72e9a8"></a>
### Campaign.on trash

`operation_enterprise_binding_enterprise_crm_doctype_campaign_campaign_campaign_on_trash`

**Inputs** self.

**State and service calls** request set\_value on “UTM Campaign”.

**Local steps**

- Evaluate Platform.db.set\_value(“UTM Campaign”, mapping(“crm\_campaign” → self.name), “crm\_campaign”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L478)

<a id="op-18cc39b50a3927"></a>
### Campaign.sync utm campaign

`operation_enterprise_customer_relationship_management_record_definitions_campaign_business_behavior_campaign_sync_campaign_tracking_campaign`

**Inputs** self.

**State and service calls** call save on mc.

**Local steps**

- Set mc from self.get\_utm\_campaign\_mirror().
- Set mc.campaign\_description from self.description.
- Set mc.crm\_campaign from self.name.
- Evaluate mc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get utm campaign mirror](operations-003.md#op-bd1e7e3a31748a).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L1361) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1132)

<a id="op-bd1e7e3a31748a"></a>
### Campaign.get utm campaign mirror

`operation_enterprise_customer_relationship_management_record_definitions_campaign_business_behavior_campaign_get_campaign_tracking_campaign_mirror`

**Inputs** self.

**Record and data access** read “UTM Campaign” via get\_value · resolve a document from “UTM Campaign” via get\_doc · read “UTM Campaign” via exists.

**State and service calls** request new\_doc for “UTM Campaign”.

**Explicit results** Platform.get\_doc(“UTM Campaign”, owned) · same\_name · mc.

**Local steps**

- If owned bound to Platform.db.get\_value(“UTM Campaign”, mapping(“crm\_campaign” → self.name)).
  - Return Platform.get\_doc(“UTM Campaign”, owned).
- If Platform.db.exists(“UTM Campaign”, self.campaign\_name).
  - Set same\_name from Platform.get\_doc(“UTM Campaign”, self.campaign\_name).
  - If (not same\_name.crm\_campaign or same\_name.crm\_campaign equals self.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not same\_name.crm\_campaign → same\_name.crm\_campaign equals self.name.
    - Return same\_name.
- Set mc from Platform.new\_doc(“UTM Campaign”).
- Set mc.name from self.name when Platform.db.exists(“UTM Campaign”, self.campaign\_name), otherwise self.campaign\_name.
  - Value choice on Platform.db.exists(“UTM Campaign”, self.campaign\_name) — true gives self.name, false gives self.campaign\_name.
- Return mc.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L1491) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1130)

<a id="op-6f9fbbc7f2b26f"></a>
### Campaign.autoname

`operation_enterprise_customer_relationship_management_record_definitions_campaign_business_behavior_campaign_autoname`

**Inputs** self.

**Local steps**

- If Platform.defaults.get\_global\_default(“campaign\_naming\_by”) differs from “Naming Series”.
  - Set self.name from self.campaign\_name.
- Otherwise.
  - Evaluate set\_name\_by\_naming\_series(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L1872) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1129)

<a id="op-b9abe64470a99f"></a>
### Get utm campaign

`operation_enterprise_binding_enterprise_crm_doctype_campaign_campaign_get_utm_campaign`

**Inputs** campaign.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read “UTM Campaign” via get\_value.

**Explicit results** (Platform.db.get\_value(“UTM Campaign”, mapping(“crm\_campaign” → campaign)) or campaign).

**Local steps**

- Evaluate Platform.has\_permission(“Campaign”, “read”, campaign, throw = true).
- Return (Platform.db.get\_value(“UTM Campaign”, mapping(“crm\_campaign” → campaign)) or campaign).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Campaign”, mapping(“crm\_campaign” → campaign)) → campaign.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Campaign”, “read”, campaign, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L479)

## Report · Campaign efficiency

<a id="op-e81658b51c1049"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns(“utm\_campaign”).
- Set data from get\_lead\_data(filters, “utm\_campaign”).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1285)

<a id="op-386e8298b627c2"></a>
### Get columns

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_get_columns`

**Inputs** based\_on.

**Explicit results** list(mapping(“fieldname” → Platform.scrub(based\_on), “label” → translated based\_on, “fieldtype” → “Data”, “width” → 150), mapping(“fieldname” → “lead\_count”, “label” → translated “Lead Count”, “fieldtype”  ….

**Local steps**

- Return list(mapping(“fieldname” → Platform.scrub(based\_on), “label” → translated based\_on, “fieldtype” → “Data”, “width” → 150), mapping(“fieldname” → “lead\_count”, “label” → translated “Lead Count”, “fieldtype”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L5935) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1286)

<a id="op-15cb120bfe2770"></a>
### Get lead data

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_get_lead_data`

**Inputs** filters, based\_on.

**Record and data access** read “Lead” via get\_list.

**Explicit results** data.

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set based\_on\_field from Platform.scrub(based\_on).
- Set lead\_filters from list(list(based\_on\_field, “is”, “set”)).
- If filters.from\_date.
  - Evaluate lead\_filters.append(list(“creation”, “&gt;=”, filters.from\_date)).
- If filters.to\_date.
  - Evaluate lead\_filters.append(list(“creation”, “&lt;”, add\_days(filters.to\_date, 1))).
- Set lead\_details from Platform.get\_list(“Lead”, filters = lead\_filters, fields = list(based\_on\_field, “name”)).
- Set lead\_map from Platform.\_dict().
- For each d in lead\_details.
  - Evaluate lead\_map.setdefault(d.get(based\_on\_field), list()).append(d.name).
- Set data from list().
- For each tuple(based\_on\_value, leads) in lead\_map.items().
  - Set row from mapping(based\_on\_field → based\_on\_value, “lead\_count” → len(leads)).
  - Set customers from get\_converted\_customers(leads).
  - Set row at “quot\_count” from get\_lead\_quotation\_count(leads, customers).
  - Set row at “opp\_count” from get\_lead\_opp\_count(leads, customers).
  - Set row at “order\_count” from get\_quotation\_ordered\_count(leads, customers).
  - Set row at “order\_value” from (get\_order\_amount(leads, customers) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_order\_amount(leads, customers) → 0.
  - Set row at “opp\_lead” from ((flt(row at “opp\_count”) ÷ flt((row at “lead\_count” or 1.0))) × 100.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “lead\_count” → 1.0.
  - Set row at “quot\_lead” from ((flt(row at “quot\_count”) ÷ flt((row at “lead\_count” or 1.0))) × 100.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “lead\_count” → 1.0.
  - Set row at “order\_quot” from ((flt(row at “order\_count”) ÷ flt((row at “quot\_count” or 1.0))) × 100.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “quot\_count” → 1.0.
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1287)

<a id="op-5661ef24ef9db8"></a>
### Get converted customers

`operation_enterprise_binding_enterprise_crm_report_campaign_efficiency_campaign_efficiency_get_converted_customers`

**Inputs** leads.

**Record and data access** read “Customer” via get\_list.

**Explicit results** Platform.get\_list(“Customer”, filters = mapping(“lead\_name” → list(“in”, leads)), pluck = “name”).

**Local steps**

- Return Platform.get\_list(“Customer”, filters = mapping(“lead\_name” → list(“in”, leads)), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L557)

<a id="op-9597e4e2280310"></a>
### Get lead quotation count

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_get_lead_quotation_count`

**Inputs** leads, customers.

**Explicit results** count\_by\_party(“Quotation”, “quotation\_to”, leads, customers, …).

**Local steps**

- Return count\_by\_party(“Quotation”, “quotation\_to”, leads, customers, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1289)

<a id="op-3813ade1a7ed7f"></a>
### Get lead opp count

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_get_lead_opportunity_count`

**Inputs** leads, customers.

**Explicit results** count\_by\_party(“Opportunity”, “opportunity\_from”, leads, customers).

**Local steps**

- Return count\_by\_party(“Opportunity”, “opportunity\_from”, leads, customers).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1288)

<a id="op-91e13f5244385a"></a>
### Get quotation ordered count

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_get_quotation_ordered_count`

**Inputs** leads, customers.

**Explicit results** count\_by\_party(“Quotation”, “quotation\_to”, leads, customers, …).

**Local steps**

- Return count\_by\_party(“Quotation”, “quotation\_to”, leads, customers, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1291)

<a id="op-1e55f99db207b3"></a>
### Count by party

`operation_enterprise_binding_enterprise_crm_report_campaign_efficiency_campaign_efficiency_count_by_party`

**Inputs** doctype, party\_type\_field, leads, customers, filters = no value.

**Record and data access** read doctype via count.

**Explicit results** count.

**Local steps**

- Set count from 0.
- For each tuple(party\_type, parties) in tuple(tuple(“Lead”, leads), tuple(“Customer”, customers)).
  - If parties.
    - Set party\_filters from mapping(party\_type\_field → party\_type, “party\_name” → list(“in”, parties)).
    - Update count using + Platform.db.count(doctype, mapping(expand (filters or mapping()), expand party\_filters)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Return count.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L556)
