# Purchasing

Locate the ordered row, receipt and invoice links. Supplier, company, units and taxes can change the values copied between documents.

[Business workflow guide](../../../../../docs/domains/procurement-and-fulfilment.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

331 bindings across 22 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Buying settings | 6 | [validate … bills rejected quantity](operations-001.md#op-a45ee85cbf21a0) |
| Report · Item wise purchase history | 7 | [execute … get chart data](operations-001.md#op-09f38ba63046b7) |
| Report · Procurement tracker | 13 | [execute … get mapped pi records](operations-001.md#op-ea880d36e17ee4) · [get mapped pr records … get po entries](operations-002.md#op-2acbda05d19456) |
| Report · Purchase analytics | 1 | [execute](operations-002.md#op-4b80862c2b0019) |
| Record · Purchase order | 60 | [initialize … on cancel](operations-002.md#op-6785a29ac4cb84) · [update status updater … make purchase invoice](operations-003.md#op-8810017227a24f) · [make purchase invoice from portal … get data](operations-004.md#op-a2abf8f628a39e) |
| Report · Purchase order analysis | 21 | [execute … group by purchase order](operations-004.md#op-55847e05911c28) · [group by item … get company column](operations-005.md#op-e43767ccb42467) |
| Record · Purchase order item | 1 | [on doctype update](operations-005.md#op-d61f42dcffc0f0) |
| Report · Purchase order trends | 2 | [execute … get chart data](operations-005.md#op-c163244e67514f) |
| Record · Request for quotation | 39 | [before validate … validate email id](operations-005.md#op-47e3d218218897) · [on submit … add items](operations-006.md#op-f5e28dfb2e37e8) · [create rfq items … get data](operations-007.md#op-b86a1a3152afba) |
| Report · Requested items to order and receive | 8 | [execute … get columns](operations-007.md#op-becd3033fefcf9) |
| Report · Subcontract order summary | 8 | [execute … get columns](operations-007.md#op-462627f019add9) |
| Report · Subcontracted item to be received | 5 | [execute … get columns](operations-007.md#op-e860273111ea65) · [get data … get subcontract order supplied item](operations-008.md#op-4e95995a1f50db) |
| Report · Subcontracted raw materials to be transferred | 4 | [execute … get order items to supply](operations-008.md#op-afff51e3b24e5e) |
| Record · Supplier | 46 | [onload … before rename](operations-008.md#op-d72eeab57b6c48) · [after rename … payment days](operations-009.md#op-d8a2301a7c3c98) · [advances … get supplier companies](operations-010.md#op-5aadeefdb9c842) |
| Record · Supplier quotation | 23 | [before validate … make purchase invoice](operations-010.md#op-58f4b5a4176513) · [make quotation … get data](operations-011.md#op-fec2c8a8b3eef5) |
| Report · Supplier quotation comparison | 11 | [execute … set default supplier](operations-011.md#op-6154c4c1e66b78) |
| Record · Supplier scorecard | 20 | [validate … update standing](operations-011.md#op-abdd75ac6798a6) · [score within standing … get data](operations-012.md#op-144545fdaef742) |
| Record · Supplier scorecard criteria | 6 | [validate … get variables](operations-012.md#op-6556c182037c43) |
| Record · Supplier scorecard period | 14 | [validate … calculate weighted score](operations-012.md#op-6f95f2e20b9fb0) · [get eval statement … post process](operations-013.md#op-74a0a4a7b38b7f) |
| Record · Supplier scorecard standing | 2 | [get scoring standing … get standings list](operations-013.md#op-56a37142adffb5) |
| Record · Supplier scorecard variable | 25 | [validate … get total rejected items](operations-013.md#op-3dbdd15016cdee) · [get total accepted amount … get rfq response days](operations-014.md#op-f8bee6b47dd438) |
| Service · Utils | 9 | [update last purchase rate … get qty to order](operations-014.md#op-b99cdea184dde0) |
