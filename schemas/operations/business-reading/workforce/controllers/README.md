# Shared transaction rules

These routines are shared by multiple voucher types. Resolve the concrete controller and enabled settings before applying a row or posting rule.

[Business workflow guide](../../../../../docs/domains/cross-domain-transactions.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

25 bindings across 2 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · Employee boarding controller | 11 | [validate … update task](operations-001.md#op-16043bf74ad805) |
| Service · Employee reminders | 14 | [send reminders in advance weekly … send work anniversary reminder](operations-001.md#op-38b0cc41846edf) · [get sender email](operations-002.md#op-901641a1863352) |
