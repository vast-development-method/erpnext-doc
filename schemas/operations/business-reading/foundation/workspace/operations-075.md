# Forms, reports and navigation · operations 75

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · System health report

[Record definition](../../../../data/record-types/system_health_report.json)

<a id="op-0054429b9df406"></a>
### Get directory size

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_get_directory_size_2`

**Inputs** remaining positional values path.

**Explicit results** total\_size.

**Local steps**

- Set folder from os.path.abspath(Platform.get\_site\_path(expanded path)).
- Set total\_size from os.path.getsize(folder).
- For each item in os.listdir(folder).
  - Set itempath from os.path.join(folder, item).
  - If not os.path.islink(itempath).
    - If os.path.isfile(itempath).
      - Update total\_size using + os.path.getsize(itempath).
    - Otherwise.
      - If os.path.isdir(itempath).
        - Update total\_size using + \_get\_directory\_size(itempath).
- Return total\_size.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L377) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1196)

## Record · System health report errors

[Record definition](../../../../data/record-types/system_health_report_errors.json)

<a id="op-8d73171fed246b"></a>
### System Health Report Errors.db insert

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L1856) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1217)

<a id="op-10a1b971286b93"></a>
### System Health Report Errors.load from db

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_load_from_database`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L1908) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1223)

<a id="op-a85d5f8cf62588"></a>
### System Health Report Errors.db update

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_database_update`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L1950) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1218)

<a id="op-89ab84f83804b5"></a>
### System Health Report Errors.delete

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_delete`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L1992) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1219)

<a id="op-0fbc07edded6ba"></a>
### System Health Report Errors.get list

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_get_list`

**Inputs** filters = no value, page\_length = 20, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2034) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1221)

<a id="op-829ad7097093a4"></a>
### System Health Report Errors.get count

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_get_count`

**Inputs** filters = no value, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2091) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1220)

<a id="op-66346c0b1b483c"></a>
### System Health Report Errors.get stats

`operation_foundation_desk_record_definitions_system_health_report_errors_business_behavior_system_health_report_errors_get_stats`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2137) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1222)

## Record · System health report failing jobs

[Record definition](../../../../data/record-types/system_health_report_failing_jobs.json)

<a id="op-418e4c67faa751"></a>
### System Health Report Failing Jobs.db insert

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2173) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1224)

<a id="op-973690998a29d5"></a>
### System Health Report Failing Jobs.load from db

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_load_from_database`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2225) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1230)

<a id="op-36734c8d8edcd4"></a>
### System Health Report Failing Jobs.db update

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_database_update`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2267) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1225)

<a id="op-df0558881deabb"></a>
### System Health Report Failing Jobs.delete

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_delete`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2309) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1226)

<a id="op-af3601ddef23c4"></a>
### System Health Report Failing Jobs.get list

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_get_list`

**Inputs** filters = no value, page\_length = 20, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2351) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1228)

<a id="op-8900fb7f81ddbc"></a>
### System Health Report Failing Jobs.get count

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_get_count`

**Inputs** filters = no value, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2408) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1227)

<a id="op-6113483f5046a0"></a>
### System Health Report Failing Jobs.get stats

`operation_foundation_desk_record_definitions_system_health_report_failing_jobs_business_behavior_system_health_report_failing_jobs_get_stats`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2454) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1229)

## Record · System health report queue

[Record definition](../../../../data/record-types/system_health_report_queue.json)

<a id="op-98c4a0d9b6ddd1"></a>
### System Health Report Queue.db insert

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2490) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1231)

<a id="op-4a54b167e5c0ee"></a>
### System Health Report Queue.load from db

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_load_from_database`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2542) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1237)

<a id="op-62fa95a5ae9fa2"></a>
### System Health Report Queue.db update

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_database_update`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2584) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1232)

<a id="op-d2b8ea59d3bec2"></a>
### System Health Report Queue.delete

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_delete`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2626) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1233)

<a id="op-30e84f223d8f4a"></a>
### System Health Report Queue.get list

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_get_list`

**Inputs** filters = no value, page\_length = 20, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2668) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1235)

<a id="op-278fb986af02c3"></a>
### System Health Report Queue.get count

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_get_count`

**Inputs** filters = no value, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2725) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1234)

<a id="op-cc1249335e345b"></a>
### System Health Report Queue.get stats

`operation_foundation_desk_record_definitions_system_health_report_queue_business_behavior_system_health_report_queue_get_stats`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2771) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1236)

## Record · System health report tables

[Record definition](../../../../data/record-types/system_health_report_tables.json)

<a id="op-2e5dd5fc897096"></a>
### System Health Report Tables.db insert

`operation_foundation_desk_record_definitions_system_health_report_tables_business_behavior_system_health_report_tables_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2807) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1238)

<a id="op-416175e58180c2"></a>
### System Health Report Tables.load from db

`operation_foundation_desk_record_definitions_system_health_report_tables_business_behavior_system_health_report_tables_load_from_database`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L2859) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1244)
