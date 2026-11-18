# Inventory and warehouses

Read item, warehouse, posting time, stock units and valuation state together. A document quantity and a stock-ledger quantity can use different units.

[Business workflow guide](../../../../../docs/domains/inventory-and-valuation.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

2,656 bindings across 105 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Report · Available batch report | 7 | [execute … get query based on filters](operations-001.md#op-095586dd11f463) |
| Report · Available serial no | 9 | [execute … get items](operations-001.md#op-dedd130cd77951) |
| Record · Batch | 28 | [get name from hash … after delete](operations-001.md#op-785d9d1dc98f5c) · [validate … get data](operations-002.md#op-1a19f7f160b9b8) |
| Report · Batch item expiry status | 7 | [execute … get data](operations-002.md#op-ebfd5580bc98e6) · [get batch details … get batch qty in warehouses](operations-003.md#op-638ac67a50e54b) |
| Report · Batch wise balance history | 11 | [execute … get item details](operations-003.md#op-6519061250c7a6) |
| Record · Bin | 18 | [recalculate values … update reserved stock](operations-003.md#op-725b04392b1840) · [on doctype update … get last sle values](operations-004.md#op-12a3c7bf10858b) |
| Report · Bom search | 2 | [execute … get parent filters](operations-004.md#op-7017b9fa7e8944) |
| Report · Cogs by item group | 18 | [execute … get row](operations-004.md#op-d8e5acd5fe9092) · [assign item groups to svd list … update leveled dict](operations-005.md#op-cbae3feed1a165) |
| Record · Company restriction | 19 | [get allowed companies … company query](operations-005.md#op-c019bdf7dc4ab6) |
| Report · Delayed item report | 7 | [execute](operations-005.md#op-bc8dcef8aa7cca) · [initialize … get group and descendants](operations-006.md#op-9c8966c488553c) |
| Report · Delayed order report | 4 | [execute … get columns](operations-006.md#op-bf5075d3e1b672) |
| Record · Delivery note | 70 | [initialize … validate sales invoice references](operations-006.md#op-a4fba00c928ead) · [validate dependent item fields … update billed amount based on so](operations-007.md#op-713b883e6305aa) · [get list context … validate address link](operations-008.md#op-03277e31269120) · [update item … get data](operations-009.md#op-2d508957d71823) |
| Report · Delivery note trends | 3 | [execute … wrap in quotes](operations-009.md#op-9c53836bc48be5) |
| Record · Delivery settings | 2 | [validate … validate dispatch attachment](operations-009.md#op-fa22ae5af1c120) |
| Record · Delivery trip | 34 | [initialize … validate stop contacts](operations-009.md#op-f4b72bbd7a2812) · [validate driver … get driver email](operations-010.md#op-136cd3943f4e42) |
| Service · Deprecated serial batch | 5 | [has legacy batch ledgers](operations-010.md#op-5b41b541970966) · [get last inward sle for serial no … use batch pool for moving average](operations-011.md#op-8e11aa51f3e710) |
| Service · Expected valuation | 64 | [initialize … pool basis](operations-011.md#op-ec16cf9d213977) · [get rate to fall back on … get batches](operations-012.md#op-4448d054f4fb39) · [get valuation method … get inventory dimension fields](operations-013.md#op-8a3d3da6cc10c1) |
| Report · Fifo queue vs qty after transaction comparison | 7 | [execute … find first bad queue](operations-013.md#op-63bb2942907ada) · [keeps fifo queue … get columns](operations-014.md#op-0276e207779df4) |
| Service · Get item details | 86 | [preprocess ctx … update bin details](operations-014.md#op-12593369f18ce3) · [get item code … get default discount account](operations-015.md#op-d3d4ecee6df523) · [get default deferred account … get bin details](operations-016.md#op-cb0221e8ab681a) · [get bin details … get blanket order details](operations-017.md#op-4f0fec7c41420c) |
| Report · Incorrect balance qty after transaction | 7 | [execute … get columns](operations-017.md#op-347b80a7c199ae) |
| Report · Incorrect serial and batch bundle | 7 | [execute … set bundle docstatus](operations-018.md#op-b472347ae4405e) |
| Report · Incorrect serial no valuation | 9 | [execute … get columns](operations-018.md#op-ef1734b28fef55) |
| Report · Incorrect stock value report | 7 | [execute … get columns](operations-018.md#op-52a3dbae0d88ae) |
| Record · Inventory dimension | 32 | [onload](operations-018.md#op-79cf9ed0af17c5) · [has stock ledger … get mandatory dimension fields](operations-019.md#op-5cca1d513742b4) · [get inventory dimensions … remove field from doctype layouts](operations-020.md#op-ce886e7b2220de) |
| Record · Item | 116 | [onload … validate item tax net rate range](operations-020.md#op-7903f0eb128e63) · [update template tables … validate item defaults](operations-021.md#op-251388c7177ae9) · [update defaults from item group … make item price](operations-022.md#op-368fb1c3a19425) · [get timeline data … set opening stock serial batch bundle](operations-023.md#op-3244b2f9b87445) · [get default warehouse for opening stock … reindex item](operations-024.md#op-335392f35a57df) · [reindex renamed item … get item search candidates](operations-025.md#op-0ff8b709162e94) |
| Record · Item alternative | 6 | [validate … get alternative items](operations-025.md#op-8232cd106aea65) |
| Record · Item attribute | 9 | [validate … validate duplication](operations-025.md#op-5473c99fb2b87f) |
| Report · Item balance (simple) | 3 | [execute … get data](operations-025.md#op-71e9b866963f7d) |
| Service · Item dashboard | 2 | [make stock entry … get data](operations-025.md#op-ed616c5a8573be) |
| Record · Item lead time | 3 | [validate](operations-025.md#op-9088aae2b646cf) · [set capacity per day … has manufacturing inputs changed](operations-026.md#op-c0235cdba3ba36) |
| Record · Item manufacturer | 9 | [validate … get item manufacturer part no](operations-026.md#op-87e050edf1482e) |
| Record · Item price | 11 | [validate … before save](operations-026.md#op-b6517addc672f4) |
| Report · Item price stock | 5 | [execute … get columns](operations-026.md#op-2ece2e0e6e0132) · [get data … get price map](operations-027.md#op-f91e6a7deb2395) |
| Report · Item prices | 8 | [execute … get valuation rate](operations-027.md#op-1109cf04bb599f) |
| Report · Item shortage report | 5 | [execute … get columns](operations-027.md#op-2645eeb854ff21) |
| Report · Item variant details | 16 | [execute … get columns](operations-027.md#op-953249802e431a) · [get selected warehouses … get attribute values map](operations-028.md#op-ecf6b94df4b1e4) |
| Record · Item variant settings | 3 | [set default fields … validate](operations-028.md#op-4a1fe6cf2a8815) |
| Report · Item where used | 20 | [execute … get item alternative rows](operations-028.md#op-e111a30c1cdb00) · [get bom map … get permitted list](operations-029.md#op-752ad635d31b2c) |
| Report · Item wise consumption | 6 | [execute … get suppliers details](operations-029.md#op-ee7b5b064b6473) |
| Report · Items to be requested | 3 | [execute … get data](operations-029.md#op-59171f1bac369c) |
| Report · Itemwise recommended reorder level | 6 | [execute … get filtered query](operations-029.md#op-7148a3d17af418) |
| Report · Landed cost report | 6 | [execute … get columns](operations-029.md#op-bdf8dd70603504) · [get data … get vendor invoices](operations-030.md#op-bd168890409b1f) |
| Record · Landed cost voucher | 36 | [get items from purchase receipts … on cancel](operations-030.md#op-9e3364b33c6fa2) · [update project purchase cost … get custom dimension overrides](operations-031.md#op-b79f850821f030) |
| Record · Manufacturer | 1 | [onload](operations-031.md#op-a7bca18f0d5064) |
| Record · Material request | 73 | [initialize … on update](operations-031.md#op-42efab875d935b) · [update item rates … update requested qty in job card](operations-032.md#op-db46186a9c7a90) · [validate work order qty … get item default suppliers](operations-033.md#op-3a3fa0c679cd75) · [make purchase orders by supplier … get data](operations-034.md#op-bfa72b91062166) |
| Record · Material request item | 1 | [on doctype update](operations-034.md#op-a715e43db28235) |
| Report · Negative batch report | 5 | [execute … get batches](operations-034.md#op-eb7377ae54dba6) |
| Record · Packed item | 41 | [set actual and projected qty … get packed items of order rows](operations-035.md#op-7adef094c9de83) · [pop order packed item … get items from product bundle](operations-036.md#op-8b36172b78bd44) |
| Record · Packing slip | 17 | [initialize … validate case nos](operations-036.md#op-fe6fd263511c28) · [validate items … item details](operations-037.md#op-c5f95a1604cfe4) |
| Record · Pick list | 125 | [initialize … validate pending qty in work order](operations-037.md#op-dcddde727b9b32) · [validate sales order … update sales order item qty](operations-038.md#op-35c2ba3ae2a68f) · [update sales order picking status … has reserved stock](operations-039.md#op-3c055ff2b15a01) · [validate no reserved stock … get header key](operations-040.md#op-3034d9bf30e128) · [has order specific amounts … set delivery note missing values](operations-041.md#op-fea97b0e5a2aef) · [set target missing values … get data](operations-042.md#op-ca3966462e0f19) |
| Record · Price list | 15 | [validate … update default price list](operations-042.md#op-7915e0477fe35a) · [delete price list details key … validate price list country](operations-043.md#op-a9c78b923b53f4) |
| Report · Product bundle balance | 6 | [execute … get item wise max posting datetime](operations-043.md#op-d8d5de44464d38) |
| Record · Purchase receipt | 92 | [initialize … get already received qty](operations-043.md#op-c4db21f8e90c16) · [get po qty and warehouse … update status](operations-044.md#op-97ac5d5e253124) · [update billing status … get pending qty](operations-045.md#op-0b88afb7b5cf84) · [select item … get provisional balances](operations-046.md#op-54dd06ba4d3bd3) · [get provisional receipt rows … get data](operations-047.md#op-44d0ff22b94e00) |
| Report · Purchase receipt trends | 3 | [execute … wrap in quotes](operations-047.md#op-1eaafb5e5819ba) |
| Record · Putaway rule | 20 | [validate … get ordered putaway rules](operations-047.md#op-ff91c929da0fed) · [get item putaway rules … get serial nos to allocate](operations-048.md#op-7dd0a324f313b3) |
| Record · Quality inspection | 37 | [on discard … is linked on reference](operations-048.md#op-f0aab739dcf14c) · [on cancel … validate qi reference](operations-049.md#op-ed40e7503621d4) |
| Record · Quality inspection template | 5 | [validate … validate acceptance formula](operations-049.md#op-e8780deddf7a77) · [get template details](operations-050.md#op-6bbd1c013a0058) |
| Record · Quick stock balance | 3 | [get stock item details … get leaf warehouses](operations-050.md#op-9e5e9eebc179c2) |
| Service · Reorder item | 12 | [reorder item … notify errors](operations-050.md#op-b33d167c15dd27) |
| Record · Repost item valuation | 65 | [clear old logs … validate update stock](operations-050.md#op-a003a96a2082ae) · [validate recalculate valuation rate … get repost started at](operations-051.md#op-55d2493a171797) · [get saved repost started at … get entries with active jobs](operations-052.md#op-fe9b5f02b4078f) · [get items with active reposting … get existing reposting only gl entries](operations-053.md#op-b696b0f3adf092) |
| Report · Reserved stock | 5 | [execute … get columns](operations-053.md#op-14b2087d884427) |
| Service · Return charges | 6 | [initialize … get actual valuation charges](operations-053.md#op-522407df58ab2c) |
| Record · Serial and batch bundle | 148 | [autoname … validate serial no status](operations-053.md#op-dbb39664aaccce) · [validate voucher detail no … get sle for outward transaction](operations-054.md#op-87656f4855e411) · [get return against … validate serial and batch no for returned](operations-055.md#op-bcbf7e69a1d3e5) · [validate returned batch qty … throw negative batch](operations-056.md#op-8b55d011f0ff48) · [get batchwise available qty … allow negative stock for batch](operations-057.md#op-94cf5b2dc143fa) · [get batch … get serial no reservation](operations-058.md#op-7e277dc79c3ffc) · [get reserved batches for pos … on doctype update](operations-059.md#op-aa40e66d5f3def) |
| Record · Serial and batch entry | 1 | [on doctype update](operations-060.md#op-89b12767080426) |
| Report · Serial and batch summary | 8 | [execute … has filter scope](operations-060.md#op-f4b958ac1c776a) |
| Service · Serial batch bundle | 90 | [get serial no status … validate item](operations-060.md#op-fc2fdcc8ebb4aa) · [set serial and batch bundle … get inward serial no rates](operations-061.md#op-5154e4af494f6a) · [get serial nos … initialize](operations-062.md#op-12bea2b3b6259c) · [set … get batch current qty](operations-063.md#op-c31a07270ab07e) · [throw negative batch validation … get serial batch list from item](operations-064.md#op-7307db9e7ddd68) |
| Record · Serial no | 17 | [initialize … on doctype update](operations-064.md#op-a2d46eb15d8fb1) |
| Report · Serial no and batch traceability | 27 | [execute … validate filters](operations-064.md#op-d98eef53abd372) · [get data … get material qty](operations-065.md#op-8adc63474dbf9e) |
| Report · Serial no ledger | 4 | [execute](operations-065.md#op-6cf2e836d5b9b1) · [get columns … get serial nos](operations-066.md#op-031ff58fd25f15) |
| Record · Shipment | 20 | [on discard … get company contact](operations-066.md#op-c76d8ab6ebf4a2) |
| Record · Shipment parcel template | 1 | [validate](operations-066.md#op-5181e6ccebbe78) |
| Service · Stock | 4 | [get warehouse account map … get company stock accounts](operations-067.md#op-d31436a5ea3bfa) |
| Report · Stock ageing | 69 | [execute … initialize](operations-067.md#op-7738d32a481653) · [generate … add to negative fifo head](operations-068.md#op-90d344ed4a05c0) · [compute outgoing stock … get warehouse conditions](operations-069.md#op-a32aed9474c22a) · [prepare stock reco voucher wise count](operations-070.md#op-842c2eb7c2622d) |
| Report · Stock analytics | 16 | [execute … get item details](operations-070.md#op-4ef48794d8efa1) |
| Report · Stock and account value comparison | 13 | [execute … create reposting entries](operations-070.md#op-21471b885d7440) · [repost based on transaction … get pending gl reposting vouchers](operations-071.md#op-83d49e4f9ffadf) |
| Report · Stock balance | 61 | [execute … is valued in pool](operations-071.md#op-95270c52872739) · [get latest valuation rates … get stock ageing data](operations-072.md#op-deb3e33dba2c18) · [filter items with no transactions … run sql](operations-073.md#op-b70e0a538134b4) |
| Service · Stock balance | 13 | [repost … get reserved qty](operations-073.md#op-b623caae3234db) · [get indented qty … set stock balance as per serial no](operations-074.md#op-7ef1dfef577068) |
| Record · Stock closing entry | 46 | [apply unscoped filters … on cancel](operations-074.md#op-39fec321d231bd) · [validate later closing entry … get initialized entry](operations-075.md#op-1b4d0d97fed46f) · [get sle entries … get data](operations-076.md#op-c59a1bf9ce692a) |
| Record · Stock entry | 252 | [is costed out of finished item … reset serial batch on fg row](operations-076.md#op-bd4756c109b965) · [validate repack entry … validate difference account](operations-077.md#op-fb8688d70f2cc7) · [validate warehouse … check if operations completed](operations-078.md#op-b9682769e17d70) · [check duplicate entry for work order … get basic rate for repacked items](operations-079.md#op-d7ae0226a4c4aa) · [set bomless secondary valuation types … recalculate for bundles picked while posting](operations-080.md#op-50758a10b3e86f) · [get finished item row … set items for stock in](operations-081.md#op-cfe2b722db42e5) · [get items for disassembly … split alternative items](operations-082.md#op-1a6f3ec0d74523) · [get secondary items … get stock in transferred qty](operations-083.md#op-71a15391fcc3c0) · [update transferred qty … split qty by alternative items](operations-084.md#op-2c0345c4548920) · [get valuation rate for finished good entry … get transferred qty](operations-085.md#op-fb96c4125d6ae8) · [get previous operation output sn batch … process serial numbers](operations-086.md#op-3fcbba44027db6) |
| Record · Stock entry type | 15 | [validate … make stock entry](operations-086.md#op-514b87d8244cda) · [prepare source warehouse … add finished good](operations-087.md#op-e060c868541907) |
| Report · Stock ledger | 25 | [execute … get item details](operations-087.md#op-fe45452b5d1971) · [get sle conditions … get inv dimension wise value](operations-088.md#op-82380f8ba6f8b2) |
| Service · Stock ledger | 141 | [initialize … get args for future sle](operations-088.md#op-d80bf06423faed) · [validate cancellation … build](operations-089.md#op-c413ecb125a379) · [initialize reposting … calculate valuation for serial batch bundle](operations-090.md#op-a5278f4a553f43) · [update serial batch no valuation … recalculate amounts in stock entry](operations-091.md#op-036cb973ba0fad) · [update rate on delivery and sales return … get sle by voucher detail no](operations-092.md#op-48749af69859a4) · [get prior ledger condition … is internal transfer](operations-093.md#op-a13fffe7d3ef3f) · [get stock value difference … has correct data](operations-094.md#op-1009e1338f19c5) |
| Report · Stock ledger entries of cancelled vouchers | 14 | [execute … repost future entries](operations-094.md#op-2499126399d21d) |
| Record · Stock ledger entry | 25 | [autoname … set posting datetime](operations-094.md#op-29be4f20076eef) · [validate inventory dimension negative stock … check stock frozen date](operations-095.md#op-c870dab4c2f604) |
| Report · Stock ledger invariant check | 9 | [execute … get data](operations-095.md#op-472f1cf6ddcdca) · [get stock ledger entries … create reposting entries](operations-096.md#op-dbb662874ae093) |
| Report · Stock ledger variance | 5 | [execute … has difference](operations-096.md#op-482cb737201a38) |
| Report · Stock projected qty | 4 | [execute … get item map](operations-096.md#op-1b12508b9b6c47) |
| Report · Stock qty vs batch qty | 4 | [execute … update batch qty](operations-096.md#op-ab051097adf549) |
| Report · Stock qty vs serial no count | 15 | [execute … get warehouses](operations-096.md#op-ab36bf017253b3) · [get data … set legacy last moves](operations-097.md#op-24f99f57df6ae6) |
| Record · Stock reconciliation | 59 | [initialize … has change in serial batch](operations-097.md#op-ade4e3e6fa844e) · [set new bundle from current … validate opening stock](operations-098.md#op-dab8263c3915af) · [get existing ledger entries … on doctype update](operations-099.md#op-f11986ed21b2e7) |
| Record · Stock reposting settings | 15 | [validate … before save](operations-099.md#op-88a6ff1574c92b) · [reset parallel reposting settings … has pending valuation repost](operations-100.md#op-ad2871a72557bf) |
| Record · Stock reservation entry | 86 | [validate … validate reserved entries](operations-100.md#op-3d6280fd39d09f) · [update unreserved qty in sre … get total reserved qty](operations-101.md#op-da43635c420173) · [get row reserved qty … initialize](operations-102.md#op-d6613b28622897) · [initialize fields … move serial batch delivered qty](operations-103.md#op-3ec41c7818bf49) · [get open serial batch entries … add serial batch delivered qty](operations-104.md#op-caeda0784be79a) |
| Record · Stock settings | 19 | [validate … has open stock reservation](operations-104.md#op-037eb30b9aeb56) |
| Report · Stock valuation comparison | 13 | [execute … get data](operations-104.md#op-1a6bbdd895e91a) · [get rows to show … make adjustment entry](operations-105.md#op-9318e24f68d007) |
| Service · Stock value by item group | 2 | [get … get stock value by item group](operations-105.md#op-123bf38651ad64) |
| Report · Total stock summary | 3 | [execute … get total stock](operations-105.md#op-8c3128553d5998) |
| Service · Utils | 39 | [get stock value from bin … get bin warehouse condition](operations-105.md#op-2b8df0a9f2920f) · [get latest stock balance … check pending reposting](operations-106.md#op-55acc9d5712976) · [scan barcode … get default stock uom](operations-107.md#op-6f3abbb28f4040) |
| Service · Valuation | 16 | [add stock … round off if near zero](operations-107.md#op-79b51b156b0e1e) |
| Service · Valuation adjustment | 39 | [key](operations-107.md#op-915eff38656c9d) · [qty … make bundle](operations-108.md#op-ff4b2ebdbf7c39) · [validate result … get adjusted until](operations-109.md#op-76638edecf6507) |
| Record · Warehouse | 28 | [autoname … validate inventory account](operations-109.md#op-077b89de98e702) · [on update … get warehouses for reorder](operations-110.md#op-4294d1bc083c9b) |
| Service · Warehouse capacity dashboard | 4 | [get data … get warehouse capacity data](operations-110.md#op-899595ca383874) |
| Record · Warehouse type | 1 | [on trash](operations-110.md#op-be758810c29cf3) |
| Report · Warehouse wise item balance age and value | 9 | [execute](operations-110.md#op-8deaa25c081ea8) · [apply permitted warehouses … get group by key](operations-111.md#op-d2e18b367dc622) |
| Report · Warehouse wise stock balance | 7 | [execute … get columns](operations-111.md#op-c0288f8f0df8a1) |
| Service · Warehouse wise stock value | 1 | [get](operations-111.md#op-fd6b9e4bbad9a8) |
