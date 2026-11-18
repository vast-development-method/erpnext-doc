# Production

Identify the bill of materials, work order, required materials and actual stock movements. Job-card progress and transferred quantities have different owners.

[Business workflow guide](../../../../../docs/domains/manufacturing-and-subcontracting.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

1,159 bindings across 39 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Blanket order | 34 | [before validate … refresh blanket orders of fulfilled rows](operations-001.md#op-9c1878a7786247) · [get data … apply price list](operations-002.md#op-2802de62a43822) |
| Record · Bom | 128 | [initialize … set default last step](operations-002.md#op-c6dd248af089ce) · [validate semi finished goods … get rm rate](operations-003.md#op-6c3ba70ff05e0c) · [update cost … get item data](operations-004.md#op-c4372c2b24970d) · [add materials from bom … validate operations](operations-005.md#op-3e99612fb18c1b) · [get tree representation … add fg based operating cost](operations-006.md#op-5789b21fcae98f) · [get component account … get data](operations-007.md#op-e3ac150d1ea71b) |
| Record · Bom creator | 148 | [validate … before cancel](operations-007.md#op-707af0b6324548) · [on cancel … create items](operations-008.md#op-ed319c79972c1b) · [create boms job id … get node item](operations-009.md#op-922cdf0c6ced41) · [get bom quantity … get part key](operations-010.md#op-7585058d428285) · [get code key … validate material](operations-011.md#op-92248e28525ff6) · [validate previous output … get duplicate problems](operations-012.md#op-792e713c5be460) · [get assembly problems … get arguments](operations-013.md#op-b0ff79cfb3e1ba) |
| Report · Bom explorer | 4 | [execute … get data](operations-013.md#op-77d69bcf34d9a9) · [get exploded items … get columns](operations-014.md#op-977aad0a0abae1) |
| Report · Bom operations time | 6 | [execute … get columns](operations-014.md#op-29363a8f479842) |
| Report · Bom stock analysis | 16 | [execute … get producible qty](operations-014.md#op-432adea209155a) |
| Record · Bom update log | 27 | [clear old logs … get leaf boms](operations-015.md#op-6870ed4ec2cb07) · [generate dependence map … handle exception](operations-016.md#op-5c58bdc5c3d945) |
| Record · Bom update tool | 5 | [enqueue replace bom … create bom update log](operations-016.md#op-52c859e4905afe) |
| Report · Bom variance report | 7 | [execute … get work orders](operations-016.md#op-306601daedfa1d) |
| Report · Cost of poor quality report | 8 | [execute … get columns](operations-016.md#op-8e8a0f0c28ad68) |
| Service · Dashboard fixtures | 4 | [get data](operations-016.md#op-53aab65769630b) · [get dashboards … get number cards](operations-017.md#op-0a30b7f4e6f3ff) |
| Report · Downtime analysis | 4 | [execute … get columns](operations-017.md#op-6c1a3dc81541c6) |
| Record · Downtime entry | 2 | [validate … validate overlap](operations-017.md#op-c13be202f17aef) |
| Report · Exponential smoothing forecasting | 11 | [execute … get summary data](operations-017.md#op-9daf15c31ad82e) |
| Record · Job card | 167 | [onload … before validate](operations-017.md#op-675ab5c2f115e9) · [validate … set total completed qty from sub operations](operations-018.md#op-ea0e3a2172d00f) · [get overlap for … update time logs](operations-019.md#op-ecc98152945d87) · [reset required items … set transferred qty in job card item](operations-020.md#op-70426cdf04bb4b) · [get job card items transferred qty … get operation input qty](operations-021.md#op-099ed6252837d5) · [validate input from previous operations … make subcontracting po](operations-022.md#op-9c7693c17b45b2) · [set missing values … get job card timer](operations-023.md#op-c90c5d1c183ad1) · [get timer rows … qty yet to manufacture](operations-024.md#op-485abc9bbc6102) |
| Report · Job card summary | 5 | [execute … get columns](operations-024.md#op-09a45da70107d0) |
| Record · Manufacturing settings | 5 | [before save … is material consumption enabled](operations-025.md#op-3c61c67014b259) |
| Record · Master production schedule | 37 | [get actual demand … is in date range](operations-025.md#op-3b485854bbcc05) · [get item wise mps data … deduct delivered qty](operations-026.md#op-59607021ee8fb7) |
| Service · Material request receipt notification | 1 | [get context](operations-026.md#op-6507cb0b7c8df9) |
| Report · Material requirements planning report | 60 | [execute … get demand beyond mps](operations-026.md#op-53ab7fb104101c) · [get orders to skip … get subcontracted data](operations-027.md#op-b4baa2b776c2e3) · [update rm details … get purchase order item](operations-028.md#op-d705395a0498e2) · [make work orders … round shares keeping total](operations-029.md#op-cb7fd88df16d1f) |
| Record · Operation | 4 | [validate … get data](operations-029.md#op-3f2938e6752efd) |
| Record · Plant floor | 6 | [validate … get stock details](operations-029.md#op-6187352b8e822c) |
| Report · Process loss report | 6 | [execute … update data with total pl value](operations-029.md#op-e0cd6f0d90460e) |
| Report · Production analytics | 7 | [execute](operations-029.md#op-6ce11f3b741c44) · [get columns … get chart data](operations-030.md#op-e7bfaa1a95a825) |
| Record · Production plan | 137 | [onload … add mr in table](operations-030.md#op-7ce5599be221b7) · [combine so items … set status](operations-031.md#op-98463244b91b3c) · [update ordered status … get plans with references](operations-032.md#op-8c7038bd1db380) · [get planned qty by order row … cover from surplus](operations-033.md#op-410a3cbfd6fdd8) · [stock quantity … get reserved qty for production plan](operations-034.md#op-1fe1947812f323) · [get remaining reserved qty … get committed qty](operations-035.md#op-e7c3f31fe94e36) |
| Report · Production plan summary | 9 | [execute](operations-035.md#op-40bebee66eccac) · [get data … get column](operations-036.md#op-35722c05db1777) |
| Report · Production planning report | 14 | [execute … get columns](operations-036.md#op-494b7631b887f7) |
| Report · Quality inspection summary | 4 | [execute … get data](operations-036.md#op-163a5d07a47a8e) · [get chart data … get columns](operations-037.md#op-a023e06a5cef62) |
| Record · Routing | 8 | [validate … get data](operations-037.md#op-9ff1c63bd63f9b) |
| Record · Sales forecast | 13 | [validate … get data](operations-037.md#op-f2e4771e09de87) |
| Record · Work order | 196 | [onload](operations-037.md#op-b3edddb66dd7c1) · [secondary items … validate sales order](operations-038.md#op-38637030a00ac1) · [set default warehouse … validate warehouse](operations-039.md#op-e49ccc119614ee) · [before submit … update work order qty in so](operations-040.md#op-6c6e6700985d19) · [get work order qty against sales order … set required item amounts](operations-041.md#op-c8bdb41034bf45) · [update transferred qty for required items … get bom operation row](operations-042.md#op-4f878759c4272e) · [set reserved qty for wip and fg … add variant item](operations-043.md#op-c1cfbba118b404) · [variant row qty … close work order](operations-044.md#op-1589e90fba471f) · [get operation qty … make stock return entry](operations-045.md#op-44076aaa39692f) · [get row wise serial batch … get data](operations-046.md#op-6c33464855e0f8) |
| Record · Work order additional item | 7 | [get list … delete](operations-046.md#op-22b75c6d8353a6) |
| Report · Work order consumed materials | 5 | [execute … get columns](operations-046.md#op-b496bcd27c0b82) |
| Record · Work order item | 1 | [on doctype update](operations-046.md#op-80e0bf58b7d1c7) |
| Report · Work order stock report | 13 | [execute … allocate stock](operations-046.md#op-34f980f4015e57) · [get bom descriptions … get columns](operations-047.md#op-971aef8b03b7a8) |
| Report · Work order summary | 9 | [execute … get columns](operations-047.md#op-f79dafc1779eb4) |
| Record · Workstation | 29 | [validate … on update](operations-047.md#op-8231bdd2ea09e0) · [validate overlap for operation timings … get data](operations-048.md#op-ae77b13977cf3b) |
| Record · Workstation operating component | 3 | [validate … validate accounts](operations-048.md#op-e609b2cad099bd) |
| Record · Workstation type | 9 | [validate … validate duplicate operating component](operations-048.md#op-ea4838b86b443e) · [before save … get workstations](operations-049.md#op-5aec5a0cc4651c) |
