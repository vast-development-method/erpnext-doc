# Sales

Follow source and target rows from quotation to order, delivery and invoice. Check returns and outstanding quantities in the linked record.

[Business workflow guide](../../../../../docs/transactions/sales-pipeline-and-approval.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

551 bindings across 35 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Report · Address and contacts | 9 | [execute … should add party name](operations-001.md#op-82c66a5ef6a644) |
| Report · Available stock for packing items | 6 | [execute … get user permitted warehouses](operations-001.md#op-a487f80e25566a) |
| Record · Customer | 89 | [onload … get customer group details](operations-001.md#op-8e18bf23d2dcdd) · [check customer group change … set loyalty program](operations-002.md#op-1b8f53c64c61d2) · [make quotation … make contact](operations-003.md#op-073a64792ba819) · [make address … quotation tiles](operations-004.md#op-cf028739928b92) · [sales order tiles … get customer companies](operations-005.md#op-e09f2ffbf00c79) |
| Report · Customer acquisition and loyalty | 5 | [execute … get permitted customers](operations-005.md#op-2a30226240e6c1) |
| Report · Customer credit balance | 3 | [execute … get details](operations-005.md#op-4b71d26d135c75) |
| Report · Customer wise item price | 7 | [execute … get selling items](operations-005.md#op-32f30331a6d2ae) |
| Report · Customers without any sales transactions | 4 | [execute](operations-005.md#op-2826c6b84e4955) · [get columns … get submitted sales](operations-006.md#op-46670e22136f28) |
| Report · Inactive customers | 8 | [execute … get columns](operations-006.md#op-a615fdbbdb2134) |
| Record · Installation note | 14 | [initialize … on submit](operations-006.md#op-0a263f090a9148) · [on cancel](operations-007.md#op-b3990aa6b00df0) |
| Report · Item wise sales history | 8 | [execute … get chart data](operations-007.md#op-243e97b24faeb1) |
| Report · Lost quotations | 5 | [execute … get report summary](operations-007.md#op-3a506e0b5cf3c1) |
| Record · Party specific item | 14 | [validate … validate party](operations-007.md#op-fc016b706568ec) · [get items ranked by orders … count rule items](operations-008.md#op-295f240d9e440e) |
| Report · Payment terms status for sales order | 11 | [get columns … execute](operations-008.md#op-7026deebb477f1) |
| Report · Pending so items for purchase request | 9 | [execute … get packed items](operations-008.md#op-af0a42602db9a0) |
| Workspace · Point of sale | 22 | [search by term … get customer recent transactions](operations-009.md#op-01d81620a8ce0b) |
| Record · Product bundle | 9 | [autoname … validate](operations-009.md#op-b7108c2106fb15) · [on trash … get new item code](operations-010.md#op-13302259e67b84) |
| Record · Proforma invoice | 25 | [validate … initialize](operations-010.md#op-fc7348e8917dd9) · [calculate item values … validate feature enabled](operations-011.md#op-337e7654348687) |
| Record · Quotation | 51 | [set indicator … is partially ordered](operations-011.md#op-9e48a039cb1fc7) · [update lead … make sales invoice](operations-012.md#op-97d4c3731f3b5c) · [make sales invoice … get data](operations-013.md#op-c2def927b1d3bf) |
| Report · Quotation trends | 2 | [execute … get chart data](operations-013.md#op-0bd52ca13d77c2) |
| Report · Sales analytics | 27 | [execute … get sales transactions based on order type](operations-013.md#op-44e819cf307203) · [get sales transactions based on customers or suppliers … get chart data](operations-014.md#op-ba7a77dc882abc) |
| Workspace · Sales funnel | 8 | [validate filters … get pipeline data](operations-014.md#op-0df2d4fb24e99d) |
| Record · Sales order | 125 | [initialize … on cancel](operations-015.md#op-d0e58007df3678) · [on trash … create stock reservation entries](operations-016.md#op-33ef7fe32ed932) · [cancel stock reservation entries … select item](operations-017.md#op-91f9be66d3667e) · [set missing values … update item for packed item](operations-018.md#op-862b4565e7dbdd) · [filter items … get pending qty criterion](operations-019.md#op-5c311bc5189601) · [get qty billed below amount criterion … get data](operations-020.md#op-a4758920bd1a36) |
| Report · Sales order analysis | 22 | [execute … get amount columns](operations-020.md#op-f3fca54123932f) · [get delivery columns … get company column](operations-021.md#op-8fc41cde889b7d) |
| Record · Sales order item | 1 | [on doctype update](operations-021.md#op-e39686a05f8950) |
| Report · Sales order trends | 2 | [execute … get chart data](operations-021.md#op-dd0eae3dd7cd08) |
| Report · Sales partner commission summary | 16 | [execute … extend report query](operations-021.md#op-dc6089c05f04a8) |
| Report · Sales partner target variance based on item group | 9 | [get data column … get data](operations-021.md#op-87ecd1b255183b) · [get sales user map … execute](operations-022.md#op-f958c84076861a) |
| Report · Sales partner transaction summary | 4 | [execute … apply filters](operations-022.md#op-20a447ad468733) |
| Report · Sales person commission summary | 4 | [execute … get conditions](operations-022.md#op-a063d1fbfa36ca) |
| Report · Sales person target variance based on item group | 1 | [execute](operations-022.md#op-878c08ca5e6e35) |
| Report · Sales person wise transaction summary | 6 | [execute … get item details](operations-022.md#op-945adae905a3c3) |
| Record · Selling settings | 8 | [on update … validate](operations-022.md#op-082e02354f53c8) · [validate fallback to default price list … toggle utm analytics section](operations-023.md#op-423ec68bd94baa) |
| Record · Sms center | 7 | [create receiver list … send sms](operations-023.md#op-37da0857a95bb6) |
| Report · Territory target variance based on item group | 1 | [execute](operations-023.md#op-22c6ee94e2c256) |
| Report · Territory wise sales | 9 | [execute … get total](operations-023.md#op-d6919d564095e2) |
