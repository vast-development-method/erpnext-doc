# Subcontracting

Distinguish quantities issued to the subcontractor, consumed material, received products and service costs.

[Business workflow guide](../../../../../docs/operations/subcontract-cost.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

176 bindings across 9 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Report · Subcontracted items to be delivered | 3 | [execute … get columns](operations-001.md#op-0e64a6a0989951) |
| Report · Subcontracted raw materials to be received | 5 | [execute … get columns](operations-001.md#op-07d066dd741325) |
| Record · Subcontracting bom | 14 | [validate … get subcontracting boms for service item](operations-001.md#op-317b9aa65563d0) |
| Record · Subcontracting inward order | 27 | [validate … on submit](operations-001.md#op-b4ad8ea518564f) · [on cancel … update subcontracting inward order status](operations-002.md#op-43462398a7cf44) · [get data](operations-003.md#op-93f6025ddd3188) |
| Record · Subcontracting inward order item | 1 | [update manufacturing qty fields](operations-003.md#op-a2f44c0df9a448) |
| Report · Subcontracting inward order summary | 6 | [execute … get columns](operations-003.md#op-f6755d9c25b52e) |
| Record · Subcontracting order | 37 | [onload … calculate service costs](operations-003.md#op-770345e95bc84a) · [calculate supplied items qty and amount … get data](operations-004.md#op-54e3ec1464b022) |
| Record · Subcontracting receipt | 80 | [initialize … before validate](operations-004.md#op-de114933a7fa21) · [validate … get secondary items](operations-005.md#op-ae33c3647dad00) · [get returned receipt rows … validate bom required qty](operations-006.md#op-de0bd256ce04ce) · [get rm wise required qty … get discount terms](operations-007.md#op-43dd9061671415) · [get tax terms … get data](operations-008.md#op-da4e110d800b33) |
| Service · Utils | 3 | [get inward order filters … get inward order columns](operations-008.md#op-8745cf19007fdd) |
