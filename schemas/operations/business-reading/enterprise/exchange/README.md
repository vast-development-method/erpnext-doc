# Integrations and service calls

Identify the local document and the external party or service. A call to an adapter establishes a handoff and can finish independently of remote delivery.

[Business workflow guide](../../../../../docs/services/external-integrations.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

90 bindings across 8 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Call log | 24 | [validate … get linked call logs](operations-001.md#op-c897616f2bffba) |
| Record · Code list | 23 | [validate … get genericode columns and examples](operations-002.md#op-227e8ca900d383) |
| Record · Common code | 10 | [validate](operations-002.md#op-a42ae3b49e6007) · [validate distinct references … on doctype update](operations-003.md#op-0511b8c85479ca) |
| Record · Communication medium | 2 | [validate … validate timeslots](operations-003.md#op-025dba90c45c62) |
| Record · Incoming call settings | 5 | [validate … time to seconds](operations-003.md#op-8518c48285eaf1) |
| Record · Plaid settings | 20 | [initialize … add institution](operations-003.md#op-022da244d20318) · [add bank accounts … update bank account ids](operations-004.md#op-34e296c92164ce) |
| Service · Utils | 1 | [get webhook address](operations-004.md#op-04d38916936e72) |
| Record · Voice call settings | 5 | [before insert … is admin](operations-004.md#op-ec65c966b3f86e) |
