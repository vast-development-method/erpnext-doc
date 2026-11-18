# Accounting and settlement

Trace the document currency, company currency, posting date and linked counterparty or account before following settlement or ledger updates.

[Business workflow guide](../../../../../docs/domains/financial-accounting.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

2,934 bindings across 159 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Account | 63 | [on update … convert ledger to group](operations-001.md#op-37be2220fcb8c3) · [check gle exists … create charts](operations-002.md#op-e259bcb0e1464e) · [import accounts … get](operations-003.md#op-7c37002c3c2b65) |
| Report · Account balance | 5 | [execute … get year start date](operations-003.md#op-43c91e496a5776) |
| Service · Account balance timeline | 4 | [get … get dates from timegrain](operations-003.md#op-899e4b3e38d02f) |
| Record · Account category | 3 | [after rename … create account categories](operations-004.md#op-0e41d099c57341) |
| Record · Account closing balance | 8 | [make closing entries … set amount with exchange rate](operations-004.md#op-32b2ffbba5daf5) |
| Record · Accounting dimension | 21 | [before insert … disable dimension](operations-004.md#op-9ab767756ab5f4) · [toggle disabling … get dimension fieldname](operations-005.md#op-6e62709a94a8b9) |
| Record · Accounting dimension filter | 6 | [before save … build map](operations-005.md#op-945b32ab65e413) |
| Record · Accounting period | 8 | [validate … validate accounting period on doc save](operations-005.md#op-949ec79bdecf2a) |
| Service · Accounts mixin | 10 | [create customer … create supplier](operations-005.md#op-0db752729a09b1) · [create item … clear old entries](operations-006.md#op-543e69eff542fe) |
| Report · Accounts payable | 1 | [execute](operations-006.md#op-d1d0079a6e47b6) |
| Report · Accounts payable summary | 1 | [execute](operations-006.md#op-ecff1d24b01f1f) |
| Report · Accounts receivable | 60 | [execute … update voucher balance](operations-006.md#op-c1c27f0dd6fe55) · [update sub total row … prepare ple query](operations-007.md#op-0fcb4ec2c7e83a) · [get permitted sales persons … get nested set children](operations-008.md#op-d7a92103f9897a) |
| Report · Accounts receivable summary | 10 | [execute … run](operations-008.md#op-fa391d2917c012) · [get data … get party accounts](operations-009.md#op-4831fc268dcb5e) |
| Record · Accounts settings | 14 | [validate … set allow on submit for dimension fields](operations-009.md#op-cf77f667a1d7a3) |
| Service · Address | 8 | [validate … link address](operations-009.md#op-096eccc2fcf79e) · [update company address … get shipping address](operations-010.md#op-c5ec0528c65bcd) |
| Record · Advance payment ledger entry | 2 | [on update … on doctype update](operations-010.md#op-98c967f810e0f7) |
| Report · Asset depreciation ledger | 10 | [execute … get columns](operations-010.md#op-317ee778295fbb) |
| Report · Asset depreciations and balances | 15 | [execute … get finance book condition](operations-010.md#op-ecdb5f2de794e0) · [get asset value adjustment map by category … get columns](operations-011.md#op-1a3385d48c1688) |
| Report · Balance sheet | 11 | [execute … load gl entries duckdb](operations-011.md#op-3b9edf6faddd65) |
| Record · Bank | 3 | [onload … get data](operations-011.md#op-fa3c786727d8a8) |
| Record · Bank account | 14 | [onload](operations-011.md#op-e29463f42a9922) · [autoname … set closing balance as per statement](operations-012.md#op-7107f4f86c6bdf) |
| Record · Bank account balance | 2 | [validate … on doctype update](operations-012.md#op-1bb00e88296e77) |
| Record · Bank clearance | 6 | [get payment entries … get payment entries for bank clearance](operations-012.md#op-dea19254630d3e) |
| Report · Bank clearance summary | 6 | [execute … get entries](operations-012.md#op-3564e4b4ed1be5) · [get entries for bank clearance summary … get amount in bank currency](operations-013.md#op-fc10c6baf92168) |
| Record · Bank guarantee | 3 | [validate … get voucher details](operations-013.md#op-99df2499740dce) |
| Report · Bank reconciliation statement | 12 | [execute … get balance row](operations-013.md#op-26c7b308f99cc3) |
| Record · Bank reconciliation tool | 36 | [get bank transactions … get older unreconciled transactions](operations-013.md#op-cfae8e4f0a26d9) · [update clearance date … get queries](operations-014.md#op-b79b5349b1786a) · [get matching queries … get pi matching query](operations-015.md#op-5931e024fd93d7) |
| Record · Bank statement import | 21 | [initialize … write xlsx](operations-015.md#op-1f0f8a8b71ae3d) · [get import status … upload bank statement](operations-016.md#op-4b51fa56ef302c) |
| Record · Bank statement import log | 53 | [before validate … get final transactions](operations-016.md#op-b9e7847fc4f975) · [get pdf tables … get amount cr dr marker](operations-017.md#op-6ba07318d07de3) · [get file properties … check for conflicts](operations-018.md#op-991e62505c5585) |
| Record · Bank transaction | 48 | [initialize … before validate](operations-018.md#op-5f7021238ab588) · [on discard … get clearance details](operations-019.md#op-277dc4e135c94f) · [get related bank gl entries … get bank mapping](operations-020.md#op-6685d58a3cccfb) |
| Record · Bank transaction rule | 10 | [is expr eval formula … run rule evaluation](operations-020.md#op-869868780dc6ad) |
| Report · Billed items to be received | 8 | [execute … get billed through](operations-020.md#op-a796a7f03aee9d) · [get receipt returns as on … get columns](operations-021.md#op-017d39295e9cc2) |
| Record · Bisect accounting statements | 13 | [validate … move up](operations-021.md#op-672f432dd7a576) |
| Record · Budget | 38 | [validate … validate applicable for](operations-021.md#op-096869a3bd228d) · [validate existing expenses … get actual expense](operations-022.md#op-6d17b282e632ae) · [get accumulated monthly budget … revise budget](operations-023.md#op-eb334470507d23) |
| Report · Budget variance report | 17 | [execute … build comparison chart data](operations-023.md#op-fd27148720be21) |
| Report · Calculated discount mismatch | 5 | [execute … get columns](operations-023.md#op-e5f2976882aab7) · [get data … parse formatted amount](operations-024.md#op-55f0a713d69a6d) |
| Report · Cash flow | 16 | [execute … get chart data](operations-024.md#op-3ffd75a7621fe3) |
| Record · Cashier closing | 5 | [validate … validate time](operations-024.md#op-a5367acc767aa4) |
| Record · Chart of accounts importer | 26 | [validate … unset existing data](operations-025.md#op-ac3f00394a456e) · [validate user perms … set default accounts](operations-026.md#op-883751e0a981f3) |
| Record · Cheque print template | 3 | [create or update cheque print format … update existing cheque print formats](operations-026.md#op-1b320d262ccf23) |
| Report · Cheques and deposits incorrectly cleared | 6 | [execute … get columns](operations-026.md#op-55dc4c476ed41c) |
| Report · Consolidated accounts payable | 1 | [execute](operations-026.md#op-abdcafef5d4567) |
| Report · Consolidated accounts payable summary | 1 | [execute](operations-026.md#op-6fbf434a333cdd) |
| Report · Consolidated accounts receivable | 13 | [execute … row currencies](operations-026.md#op-f32746b81fc47f) · [add company columns … company column index](operations-027.md#op-e1a638e4d902b3) |
| Report · Consolidated accounts receivable summary | 6 | [execute … total row](operations-027.md#op-7ae43ae1f758dd) |
| Report · Consolidated financial statement | 52 | [execute … get column amount](operations-027.md#op-c5478cc6716a03) · [convert to column currency … get companies](operations-028.md#op-bf78ae1444bf59) · [get subsidiary companies … add to list](operations-029.md#op-060b61637d4810) |
| Report · Consolidated trial balance | 16 | [execute … get reporting currency](operations-029.md#op-2c7c4b962cb14b) · [consolidate gle data … get columns](operations-030.md#op-216a3e87d6e665) |
| Record · Cost center | 18 | [autoname … get data](operations-030.md#op-3c574850a84faa) |
| Record · Cost center allocation | 12 | [initialize … validate](operations-030.md#op-9580828a4076e9) · [validate allocation percentages … clear cache](operations-031.md#op-151812f9f8186d) |
| Record · Coupon code | 3 | [autoname … validate pricing rule](operations-031.md#op-1ef563eb62f895) |
| Record · Currency exchange settings | 7 | [validate … get api endpoint](operations-031.md#op-6f1f760395e8e4) |
| Report · Custom financial statement | 1 | [execute](operations-031.md#op-b3c30cbf16b389) |
| Report · Customer ledger summary | 14 | [initialize … validate filters](operations-031.md#op-802773237f8fe7) · [update hierarchical filters … execute](operations-032.md#op-90e09db4014583) |
| Report · Day book | 6 | [execute … get columns](operations-032.md#op-6eabba658b7323) |
| Service · Deferred revenue | 18 | [validate service stop date … calculate amount](operations-032.md#op-bf09c5fef858f1) · [get already booked amount … get deferred booking accounts](operations-033.md#op-9b2a8214131e10) |
| Report · Deferred revenue and expense | 24 | [initialize … estimate future](operations-033.md#op-0115ca060ac700) · [report data … execute](operations-034.md#op-520885f8fba88f) |
| Report · Delivered items to be billed | 3 | [execute … get args](operations-034.md#op-c50f00bc3484ac) |
| Report · Dimension wise accounts balance report | 9 | [execute … get columns](operations-034.md#op-6ea8373cbe3c26) |
| Record · Dunning | 25 | [validate](operations-034.md#op-609134641efdf2) · [validate currency … get related dunnings](operations-035.md#op-460cb59076c542) |
| Record · Dunning type | 9 | [autoname … set default dunning type](operations-036.md#op-2ac4370c172ec4) |
| Record · Exchange rate revaluation | 21 | [validate … make jv entries](operations-036.md#op-dab6e7037e19c1) · [make jv for zero balance … get data](operations-037.md#op-e6b8365553bb04) |
| Record · Finance book | 1 | [get data](operations-037.md#op-051523d6d45917) |
| Report · Financial ratios | 18 | [get accounts … avg ratio balance](operations-037.md#op-7a3de826b8f204) · [calculate ratio](operations-038.md#op-32cf7c22d04555) |
| Record · Financial report template | 164 | [get value … apply view transformation](operations-038.md#op-cbfdd73e2441e1) · [generate chart data … build simple condition](operations-039.md#op-29b0b3b66583b7) · [build logical condition … initialize](operations-040.md#op-ff111d53f6d0e0) · [evaluate formula … get row data](operations-041.md#op-cd398d5a2873f9) · [get filter value … before validate](operations-042.md#op-6e937201c65f22) · [clear hidden fields … validate](operations-043.md#op-2e89f530f37526) · [validate … extract reference codes from formula](operations-044.md#op-d27ee5f5783159) |
| Service · Financial statements | 33 | [get dimension values … build period list](operations-044.md#op-5108c064ad932b) · [is dimension grouped … get account filter query](operations-045.md#op-ac48757dcdc167) · [apply additional conditions … compute margin view data](operations-046.md#op-46a292c5bf7753) |
| Record · Fiscal year | 9 | [validate … get data](operations-046.md#op-3e84dc84ba7aef) |
| Report · General and payment ledger comparison | 14 | [initialize … get permitted parties](operations-046.md#op-259dd19210ec35) · [get account currencies … execute](operations-047.md#op-0bb06d86462ad3) |
| Report · General ledger | 31 | [execute … initialize gle map](operations-047.md#op-d8c401fad4e326) · [get accountwise gle … build gl conditions duckdb](operations-048.md#op-8653ce24890008) |
| Service · General ledger | 32 | [make gl entries … get merge properties](operations-048.md#op-75f652e99d2e0c) · [get merge key … validate allowed dimensions](operations-049.md#op-6c76eb5fc376ac) |
| Record · Gl entry | 21 | [autoname … check mandatory](operations-049.md#op-fa5a684d65ca2d) · [pl must have cost center … rename temporarily named docs](operations-050.md#op-1de5a76106ddbc) |
| Report · Gross and net profit report | 8 | [execute … get profit](operations-050.md#op-73b6730dea2407) · [get net profit](operations-051.md#op-10491baa93f04d) |
| Report · Gross profit | 41 | [execute … get buying amount](operations-051.md#op-9a5dfd4ab61707) · [load drop ship buying rates … load non stock items](operations-052.md#op-0a50cd04568e9c) |
| Report · Inactive sales items | 7 | [execute … get territories](operations-052.md#op-82967992f061a4) · [get items](operations-053.md#op-8069e3f5bb1bc6) |
| Report · Invalid ledger entries | 9 | [execute … get ledger vouchers](operations-053.md#op-d68b5e5d23305a) |
| Record · Invoice discounting | 15 | [validate … get party account based on invoice discounting](operations-053.md#op-292270baa243ba) · [get data](operations-054.md#op-bea3daaa000f7e) |
| Record · Item tax template | 5 | [validate … get data](operations-054.md#op-ae9f08aa17772c) |
| Report · Item wise purchase register | 7 | [execute … get purchase receipts against purchase order](operations-054.md#op-f32881998682a2) |
| Report · Item wise sales register | 21 | [execute … get delivery notes against sales order](operations-054.md#op-cb8c82bf396727) · [get grand total … add sub total row](operations-055.md#op-dc8ce2f800a904) |
| Record · Journal entry | 74 | [initialize … on update after submit](operations-055.md#op-f2ce926a84572c) · [on cancel … validate entries for advance](operations-056.md#op-17ba46956c17ac) · [system generated gain loss … get payment entry against order](operations-057.md#op-851ea152e440cc) · [get payment entry against invoice … post process](operations-058.md#op-9cc76cd663c713) |
| Record · Journal entry template | 3 | [validate … get naming series](operations-058.md#op-3d6fab4ec400e3) |
| Record · Ledger health | 3 | [update ledger health … get vouchers in scan](operations-058.md#op-f4f11314f40df3) |
| Record · Ledger merge | 3 | [start merge … start merge](operations-058.md#op-60d234d7d6451b) |
| Record · Loyalty point entry | 2 | [get loyalty point entries … get redemption details](operations-058.md#op-9bded453f43f9a) |
| Record · Loyalty program | 8 | [validate](operations-058.md#op-bfdb0e9c615e44) · [validate lowest tier … get data](operations-059.md#op-492a573700ad5b) |
| Record · Mode of payment | 5 | [validate … validate enabled mode of payment](operations-059.md#op-5e8dd3c79475bf) |
| Record · Monthly distribution | 5 | [get months … get data](operations-059.md#op-23aad0971c493e) |
| Service · Non billed report | 7 | [get ordered to be billed data … get project field](operations-059.md#op-c7e45363229b13) |
| Service · Notification for new fiscal year | 1 | [get context](operations-060.md#op-6bbcf8dd197899) |
| Record · Opening invoice creation tool | 15 | [onload … get temporary opening account](operations-060.md#op-4f56a6905cf1de) |
| Service · Order billing as on | 14 | [initialize … get billed query](operations-060.md#op-9b7b1527f6220b) · [sum till date … group by order line](operations-061.md#op-03a28e9405d81d) |
| Service · Party | 43 | [get party details … get party account currency](operations-061.md#op-9a5832b1db8fa9) · [generator … render address](operations-062.md#op-f6513d79a9886e) · [validate party currency before merging](operations-063.md#op-b18c7c4017ae47) |
| Record · Party link | 2 | [validate … create party link](operations-063.md#op-63257dde49887f) |
| Record · Payment entry | 128 | [initialize … delink advance entry references](operations-063.md#op-fefcaa66d96d98) · [trigger invoice update for subscriptions … set received amount](operations-064.md#op-e697758c42d7e7) · [set amounts after tax … add bank gl entries](operations-065.md#op-01994b4527f906) · [add tax gl entries … on previous row error](operations-066.md#op-a2b3d9b29619ac) · [get outstanding reference documents … apply early payment discount](operations-067.md#op-665ff61be92cc2) · [set pending discount loss … get data](operations-068.md#op-c1f0f5c9675409) |
| Record · Payment entry reference | 1 | [payment request outstanding](operations-068.md#op-94777ded23b5d1) |
| Record · Payment gateway account | 5 | [autoname … get data](operations-068.md#op-b2530be2363926) |
| Report · Payment ledger | 8 | [initialize … run](operations-068.md#op-e3d04a0017ba8d) · [execute](operations-069.md#op-8a7e1fb62f49f8) |
| Record · Payment ledger entry | 7 | [validate account … on doctype update](operations-069.md#op-01d0ac34c0deaf) |
| Record · Payment order | 23 | [validate … make payment records](operations-069.md#op-2a98167e3ca030) · [make journal entry … get data](operations-070.md#op-8777ccad985f45) |
| Report · Payment period based on invoice date | 8 | [execute … get invoice posting date map](operations-070.md#op-8ddbac327faa39) |
| Record · Payment reconciliation | 42 | [initialize … db update](operations-070.md#op-119a6b229843fc) · [delete … check mandatory to fetch](operations-071.md#op-fc13645521d88b) · [validate entries … get queries for dimension filters](operations-072.md#op-ad1ff0b85593e7) |
| Record · Payment reconciliation allocation | 1 | [get list](operations-072.md#op-a70db83671287b) |
| Record · Payment reconciliation invoice | 1 | [get list](operations-072.md#op-3029d459f141fb) |
| Record · Payment reconciliation payment | 1 | [get list](operations-072.md#op-11a7998bd6b6e8) |
| Record · Payment request | 69 | [run as administrator … set payment references within requestable amount](operations-072.md#op-35088eb613c490) · [validate currency … allocate payment request to pe references](operations-073.md#op-cfc8c63af83f1e) · [make payment request … get subscription plans](operations-074.md#op-30ebc881993af7) · [make payment order … get data](operations-075.md#op-e8d1e9c34188e8) |
| Record · Payment term | 1 | [get data](operations-075.md#op-8635adccde4a76) |
| Record · Payment terms template | 4 | [validate … get data](operations-075.md#op-0e869b95c96ffd) |
| Record · Period closing voucher | 52 | [validate … check closing account currency](operations-075.md#op-50689433187825) · [before submit … get gl entries for current period](operations-076.md#op-de0c95cfbb8801) · [set account balance dict … is within stock value tolerance](operations-077.md#op-446c624cdd87af) |
| Record · Pos closing entry | 27 | [validate … validate duplicate pos invoices](operations-077.md#op-0547ceede392c3) · [validate pos invoices … build invoice query](operations-078.md#op-10e05fe5a8fb4e) |
| Record · Pos invoice | 56 | [initialize … before submit](operations-078.md#op-9f8aa3d95516e7) · [on submit … validate loyalty transaction](operations-079.md#op-902b29bdc653f7) · [set status … make merge log](operations-080.md#op-c4fa1c7ebc3e03) · [add return modes … create payments on invoice](operations-081.md#op-7273bd3e243d05) |
| Record · Pos invoice merge log | 34 | [validate … set summed amounts](operations-081.md#op-f29031eb221551) · [get reversed rows … get error message](operations-082.md#op-ee5c0c17aa2801) |
| Record · Pos opening entry | 11 | [validate … before cancel](operations-082.md#op-34ad5a64dd38b9) · [on cancel … check poe is cancellable](operations-083.md#op-7d7cc7697f0356) |
| Record · Pos profile | 15 | [validate … pos profile query](operations-083.md#op-bb877729d0e785) |
| Report · Pos register | 10 | [execute … validate filters](operations-083.md#op-68b31077d76af2) · [get conditions … get columns](operations-084.md#op-6605f339e94254) |
| Record · Pos settings | 11 | [validate … get pos search field options](operations-084.md#op-c01792dc2d7a6a) |
| Record · Pricing rule | 69 | [validate … validate rate or discount](operations-084.md#op-ceb085bf69f898) · [validate max discount … set transaction type](operations-085.md#op-6077822a21705b) · [get item uoms … is coupon of pricing rule](operations-086.md#op-3b91bc20de9b40) · [get transaction pricing rules … update coupon code count](operations-087.md#op-050a1a6c63630c) |
| Record · Process deferred accounting | 3 | [validate … on cancel](operations-087.md#op-e0a6fc29434735) |
| Record · Process payment reconciliation | 22 | [on discard … is job running](operations-087.md#op-64edb2227875e7) · [pause job for doc … get data](operations-088.md#op-eb8ef938286d2d) |
| Record · Process period closing voucher | 32 | [on discard … start pcv processing](operations-088.md#op-c945bf4f25fba2) · [pause pcv processing … process individual date](operations-089.md#op-172053df6aafc3) |
| Record · Process period closing voucher detail | 1 | [on doctype update](operations-089.md#op-4115c32f67f359) |
| Record · Process statement of accounts | 19 | [validate … validate company for table](operations-089.md#op-d3d51fe3d011a4) · [get report pdf … send auto email](operations-090.md#op-2fc6a8f53f8c6a) |
| Record · Process subscription | 3 | [on submit … create subscription process](operations-090.md#op-dcec576fc4ce82) |
| Report · Profit and loss statement | 7 | [execute … execute snapshot report](operations-090.md#op-d51d7073c29f61) · [get data duckdb … load gl entries duckdb](operations-091.md#op-f5d0be45941b9f) |
| Report · Profitability analysis | 10 | [execute … get finance books](operations-091.md#op-e92bfa3c412830) |
| Record · Promotional scheme | 23 | [validate … are warehouses distinct](operations-091.md#op-fcf51ae4303241) · [are price lists distinct … get data](operations-092.md#op-1589dca492c745) |
| Record · Purchase invoice | 79 | [initialize … create remarks](operations-092.md#op-61f5fc6bba56a8) · [set missing values … update supplier outstanding](operations-093.md#op-7bcccd1a45c166) · [get gl entries … block invoice](operations-094.md#op-1c0e107858bb1d) · [unblock invoice … get data](operations-095.md#op-2eb11a2ac5948c) |
| Report · Purchase invoice trends | 1 | [execute](operations-095.md#op-696587f75f448f) |
| Report · Purchase register | 16 | [execute … is internal transfer](operations-095.md#op-714d45bae1901c) · [get in invoice payable debit … get account details](operations-096.md#op-4ade8433e08754) |
| Record · Purchase taxes and charges template | 3 | [validate … get data](operations-096.md#op-7b0cc5c9bd4a6d) |
| Report · Received items to be billed | 3 | [execute … get args](operations-096.md#op-2a66d0260fd751) |
| Record · Repost accounting ledger | 33 | [initialize … validate no duplicate vouchers](operations-096.md#op-bf0ae3ab4873e1) · [validate vouchers are submitted … validate docs for deferred accounting](operations-097.md#op-d293cb7f2f7552) · [validate docs for voucher types … get repost allowed types](operations-098.md#op-eb303fe66aaae8) |
| Record · Repost payment ledger | 9 | [repost ple for voucher … execute repost payment ledger](operations-098.md#op-b8fe24ebfc4a67) |
| Record · Sales invoice | 168 | [initialize … before submit](operations-098.md#op-8dfc2c9e86f135) · [on submit … validate time sheets are submitted](operations-099.md#op-8ca638d7e387a2) · [set pos fields … validate write off account](operations-100.md#op-bf85303a77c6c0) · [validate account for change amount … get note for asset sale](operations-101.md#op-40c79212842ff2) · [restore asset … verify payment amount is positive](operations-102.md#op-bca9e6987d3bea) · [verify payment amount is negative … get inter company details](operations-103.md#op-39a1f171082386) · [get internal party … get loyalty programs](operations-104.md#op-62cfecbfa2687d) · [create invoice discounting … get data](operations-105.md#op-b21406393b0e48) |
| Record · Sales invoice item | 3 | [validate cost center … set income account for fixed asset](operations-105.md#op-8f164cdb073cf9) |
| Report · Sales invoice trends | 1 | [execute](operations-105.md#op-042a66c554c806) |
| Report · Sales partners commission | 6 | [execute … get columns](operations-105.md#op-a6c5e563edaea0) |
| Report · Sales payment summary | 13 | [execute … get columns](operations-105.md#op-8ca1072140fbf6) · [get pos sales payment data … get permitted invoices](operations-106.md#op-016fca3a7ca972) |
| Report · Sales register | 16 | [execute … get invoice so dn map](operations-106.md#op-ec5aca5a83ba62) · [get invoice cc wh map … get mode of payments](operations-107.md#op-cc0a8395e2fe03) |
| Record · Sales taxes and charges template | 7 | [validate … get data](operations-107.md#op-6969395659b685) |
| Record · Share balance | 2 | [validate … on trash](operations-107.md#op-7fb8e147f8f1a8) |
| Report · Share balance | 8 | [execute … get block](operations-107.md#op-80e6aeb96622ce) |
| Report · Share ledger | 3 | [execute … get all transfers](operations-107.md#op-6174b67a1b7560) |
| Record · Share transfer | 12 | [on submit … on cancel](operations-107.md#op-daf02d7abf7e43) · [validate … make jv entry](operations-108.md#op-36c2ec9a9eb855) |
| Record · Share type | 1 | [get data](operations-108.md#op-eb69face3c3af1) |
| Record · Shareholder | 6 | [onload … get data](operations-108.md#op-cb5ea5002e2d86) |
| Record · Shipping rule | 11 | [validate … add shipping rule to tax table](operations-108.md#op-e1eccdec95b625) · [sort shipping rule conditions … get data](operations-109.md#op-10492c70e37277) |
| Record · Subscription | 42 | [before insert … validate party billing currency](operations-109.md#op-fbeb1418590ed0) · [validate trial period … process all](operations-110.md#op-da9fa5fc9bd2fc) |
| Record · Subscription plan | 5 | [validate … validate interval count](operations-110.md#op-9621725fd0bcb7) · [get plan rate … get data](operations-111.md#op-7c9730cd63baf0) |
| Report · Supplier ledger summary | 1 | [execute](operations-111.md#op-f43ff1e65040c4) |
| Record · Tax category | 1 | [get data](operations-111.md#op-a0fb6bf2fbad62) |
| Record · Tax rule | 11 | [validate … cmp](operations-111.md#op-a3c009988e3819) |
| Record · Tax withholding category | 13 | [validate … get](operations-111.md#op-a967337e462025) · [get ldc details … get data](operations-112.md#op-2b03c88b2916af) |
| Report · Tax withholding details | 18 | [initialize … get columns](operations-112.md#op-2f3e1f4d7f061a) |
| Record · Tax withholding entry | 88 | [set status](operations-112.md#op-b5ebb0936d89ae) · [get status … process return ldc entries](operations-113.md#op-8ac8f44cfb6fae) · [reverse ldc entry … process over withheld entries](operations-114.md#op-e34c502a2d5623) · [create base entry … setup direction fields](operations-115.md#op-6a037ced128185) · [get category names … reset idx](operations-116.md#op-f2037932db9636) |
| Report · Tds computation summary | 4 | [validate filters … get columns](operations-116.md#op-bc4219e15c3ba6) |
| Report · Trial balance | 24 | [execute … get opening balances](operations-116.md#op-24a86282a9f90b) · [get rootwise opening balances … get gl entry opening duckdb](operations-117.md#op-e6c120f6b247cc) |
| Report · Trial balance for party | 8 | [execute … get finance book condition](operations-117.md#op-f2303b86270402) · [toggle debit credit … is party name visible](operations-118.md#op-108c82fd2e469d) |
| Record · Unreconcile payment | 11 | [validate … create unreconcile doc for selection](operations-118.md#op-0965c89cb53258) |
| Service · Utils | 108 | [validate mandatory date range … get query columns](operations-118.md#op-53347427fd9326) · [get values for columns … reconcile against document](operations-119.md#op-f90aa0c88278ff) · [check if advance entry modified … get account name](operations-120.md#op-f0c6d1040fd9e8) · [get companies … check and delete linked reports](operations-121.md#op-e3a46a83321b11) · [create err and its journals … is immutable ledger enabled](operations-122.md#op-6e30d43ef49fd3) · [update subscription on invoice update … refresh subscription status](operations-123.md#op-e1f333db2ea42a) |
| Report · Voucher wise balance | 4 | [execute … apply filters](operations-123.md#op-e1c7a9925cd3c1) |
