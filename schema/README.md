# Entity and field dictionary

Use the [alphabetical entity index](index.tsv) to find a qualified entity and its dictionary. Each domain file contains the field definitions, relationships, selection values, access grants and controls for its entities. The [capability-specific field and policy tables](configuration/README.md) describe additions and overrides. The [dictionary schema](dictionary.schema.json) defines the machine-readable structure. The [relational design guide](../docs/model/README.md) defines shared keys, ownership, reference cardinality, configuration variants, currency selection and access rules.

| Business area | Entities | Value and collection fields | Relationship fields | Dictionary |
|---|---:|---:|---:|---|
| Accounting | 191 | 2466 | 898 | [1](entities/accounting-01.json), [2](entities/accounting-02.json), [3](entities/accounting-03.json), [4](entities/accounting-04.json) |
| Accounting Export | 3 | 16 | 7 | [Dictionary](entities/accounting-export.json) |
| Administration | 4 | 19 | 2 | [Dictionary](entities/administration.json) |
| Application Design | 10 | 75 | 11 | [Dictionary](entities/application-design.json) |
| Approval Workflows | 9 | 49 | 20 | [Dictionary](entities/approval-workflows.json) |
| Automation | 16 | 144 | 31 | [Dictionary](entities/automation.json) |
| Batch Processing | 2 | 12 | 3 | [Dictionary](entities/batch-processing.json) |
| Business Correspondence | 2 | 10 | 4 | [Dictionary](entities/business-correspondence.json) |
| Business Integrations | 1 | 6 | 0 | [Dictionary](entities/business-integrations.json) |
| Carrier Booking | 5 | 17 | 3 | [Dictionary](entities/carrier-booking.json) |
| Clinical Services | 135 | 1801 | 756 | [1](entities/clinical-services-01.json), [2](entities/clinical-services-02.json) |
| Configuration | 7 | 209 | 20 | [Dictionary](entities/configuration.json) |
| Contacts | 7 | 51 | 11 | [Dictionary](entities/contacts.json) |
| Crop Management | 22 | 122 | 39 | [Dictionary](entities/crop-management.json) |
| Customer Support | 11 | 119 | 31 | [Dictionary](entities/customer-support.json) |
| Digital Commerce | 21 | 203 | 65 | [Dictionary](entities/digital-commerce.json) |
| Document Output | 8 | 96 | 10 | [Dictionary](entities/document-output.json) |
| Education | 74 | 530 | 236 | [Dictionary](entities/education.json) |
| Electronic Document Exchange | 2 | 15 | 3 | [Dictionary](entities/electronic-document-exchange.json) |
| Fixed Assets | 26 | 288 | 113 | [Dictionary](entities/fixed-assets.json) |
| French Accounting | 17 | 94 | 26 | [Dictionary](entities/french-accounting.json) |
| Geography | 2 | 13 | 0 | [Dictionary](entities/geography.json) |
| German Accounting | 15 | 102 | 32 | [Dictionary](entities/german-accounting.json) |
| Hospitality | 17 | 72 | 34 | [Dictionary](entities/hospitality.json) |
| Indian Accounting | 32 | 444 | 88 | [Dictionary](entities/indian-accounting.json) |
| Information Management | 112 | 972 | 181 | [1](entities/information-management-01.json), [2](entities/information-management-02.json) |
| Inventory | 76 | 1443 | 486 | [1](entities/inventory-01.json), [2](entities/inventory-02.json), [3](entities/inventory-03.json) |
| Lending | 84 | 922 | 318 | [1](entities/lending-01.json), [2](entities/lending-02.json) |
| Lodging | 10 | 39 | 17 | [Dictionary](entities/lodging.json) |
| Mail | 17 | 199 | 33 | [Dictionary](entities/mail.json) |
| Maintenance | 5 | 67 | 31 | [Dictionary](entities/maintenance.json) |
| Manufacturing | 53 | 758 | 255 | [Dictionary](entities/manufacturing.json) |
| Multichannel Fulfilment | 1 | 6 | 2 | [Dictionary](entities/multichannel-fulfilment.json) |
| Nonprofit | 17 | 161 | 46 | [Dictionary](entities/nonprofit.json) |
| Online Store | 9 | 99 | 31 | [Dictionary](entities/online-store.json) |
| Operator Workspace | 67 | 530 | 136 | [Dictionary](entities/operator-workspace.json) |
| Organization | 40 | 428 | 154 | [Dictionary](entities/organization.json) |
| Payment Services | 10 | 55 | 2 | [Dictionary](entities/payment-services.json) |
| Process Design | 20 | 146 | 37 | [Dictionary](entities/process-design.json) |
| Procurement | 20 | 533 | 174 | [Dictionary](entities/procurement.json) |
| Projects | 15 | 171 | 43 | [Dictionary](entities/projects.json) |
| Quality Management | 16 | 69 | 25 | [Dictionary](entities/quality-management.json) |
| Regional Accounting | 5 | 23 | 14 | [Dictionary](entities/regional-accounting.json) |
| Relationship Management | 54 | 443 | 103 | [Dictionary](entities/relationship-management.json) |
| Sales | 20 | 535 | 189 | [Dictionary](entities/sales.json) |
| Sales Relationships | 28 | 234 | 81 | [Dictionary](entities/sales-relationships.json) |
| Sales Tax Exchange | 7 | 41 | 9 | [Dictionary](entities/sales-tax-exchange.json) |
| Self Service | 2 | 2 | 1 | [Dictionary](entities/self-service.json) |
| Service Integrations | 24 | 205 | 24 | [Dictionary](entities/service-integrations.json) |
| Subcontracting | 13 | 296 | 114 | [Dictionary](entities/subcontracting.json) |
| Telephone Exchange | 1 | 6 | 0 | [Dictionary](entities/telephone-exchange.json) |
| Telephony | 5 | 32 | 9 | [Dictionary](entities/telephony.json) |
| Web Publishing | 39 | 310 | 45 | [Dictionary](entities/web-publishing.json) |
| Workforce | 166 | 1633 | 657 | [1](entities/workforce-01.json), [2](entities/workforce-02.json), [3](entities/workforce-03.json) |

The dictionaries contain 1,575 scoped entity definitions, 17,331 value and collection fields, 5,660 relationship fields and 2,702 declared role grants. Relationship fields include owned rows, fixed references and fields whose target entity is selected at runtime. Presentation controls appear separately. The [entity cross-reference](../docs/rebuild/coverage-review/entity-cross-reference.tsv) identifies 1,561 declared entities and 14 layouts retained for interpreting existing data. The [compatibility field register](../docs/rebuild/coverage-review/compatibility-fields.tsv) identifies 155 retired fields on otherwise active entities. Counts in this table include those retained layouts and fields. New entries and postings use the active definitions for the installed capabilities.

Every fixed entity reference in these dictionaries resolves to a defined entity. A deployment must enable the corresponding capability or supply an equivalent identity contract before accepting a mandatory reference. A polymorphic reference also requires a registered target type at runtime.

## Exchange formats

The schemas use JSON Schema Draft 2020-12. Each describes one complete volume. The identifiers in a volume can link to definitions in another business area. Resolve those references against the applicable configuration after validating the volume structure.

| Contents | Consumer schema |
|---|---|
| Shared entities, fields, relationships and role grants | [Entity dictionary](dictionary.schema.json) |
| Optional entities, relationship bindings, contributed fields and permissions | [Optional record volume](optional-record-volume.schema.json) |
| Optional services, caller admission, input defaults, report filters and output columns | [Optional service volume](optional-service-volume.schema.json) |
