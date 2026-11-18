# Schema composition by capability

A business capability can add fields to an entity owned by another area or alter a field policy. For example, lending can attach recovery and consolidation controls to the company, and payment collection can add gateway and amount selection to a public form. Read these files together with the [base entity dictionaries](../README.md). Enabling the capability and its associated business configuration determines which contributions apply.

Each row names a receiving entity and either a field definition or a property override. Repeated declarations with identical meaning appear once within that capability. A field can be populated conditionally during setup or operation. An owner marked `owner_selected_by_configuration` is selected by the installation or operation context. Bind it to an actual entity before including it in an effective schema. A fixed target must exist within the combined set of capabilities. Where a relationship says `capability_binding_required`, the field declaration supplies no target identity. The contributing service must declare that target before the field can participate in referential validation. A value supplied through a user interface may add a calculated or transient field without establishing a stored column.

| Capability | Distinct field definitions and overrides | Dictionary |
|---|---:|---|
| Carrier Booking | 7 | [Read fields and overrides](carrier-booking.json) |
| Clinical Services | 84 | [Read fields and overrides](clinical-services.json) |
| Education | 4 | [Read fields and overrides](education.json) |
| French Accounting | 143 | [Read fields and overrides](french-accounting.json) |
| German Accounting | 21 | [Read fields and overrides](german-accounting.json) |
| Indian Accounting | 136 | [Read fields and overrides](indian-accounting.json) |
| Lending | 34 | [Read fields and overrides](lending.json) |
| Nonprofit | 2 | [Read fields and overrides](nonprofit.json) |
| Online Store | 11 | [Read fields and overrides](online-store.json) |
| Payment Services | 11 | [Read fields and overrides](payment-services.json) |
| Relationship Management | 25 | [Read fields and overrides](relationship-management.json) |
| Workforce | 57 | [Read fields and overrides](workforce.json) |
