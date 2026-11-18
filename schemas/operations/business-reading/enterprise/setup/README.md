# Company and master data

Determine which company, party, item, address or setting owns the value used by a transaction.

[Business workflow guide](../../../../../docs/domains/company-and-master-governance.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

408 bindings across 36 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Authorization control | 5 | [get appr user role … get value based rule](operations-001.md#op-61ff363f924ecf) |
| Record · Authorization rule | 4 | [check duplicate entry … validate](operations-001.md#op-374eb1300a266f) |
| Record · Brand | 2 | [validate … get brand defaults](operations-001.md#op-f741a659b482bb) |
| Record · Company | 48 | [onload … on update](operations-001.md#op-183dc71eb8cfe0) · [create default warehouses … update company monthly sales](operations-002.md#op-495dd1930a3784) · [update transactions annual history … get data](operations-003.md#op-831a7904f92ff2) |
| Service · Company setup | 2 | [create fiscal year and company … get fy details](operations-003.md#op-b066ef8e0a1497) |
| Record · Currency exchange | 2 | [autoname … validate](operations-003.md#op-1fa37c58045350) |
| Record · Customer group | 6 | [validate … on doctype update](operations-003.md#op-1a17a6496ea0cb) |
| Service · Dashboard charts | 3 | [get company for dashboards … get account](operations-003.md#op-f5b59a8c9e8a37) |
| Service · Default success action | 3 | [get message … get default success action](operations-004.md#op-78a5c4da4af0f3) |
| Service · Defaults setup | 7 | [set default settings … get fy details](operations-004.md#op-b0770bc5ba0124) |
| Service · Demo | 6 | [clear demo data … read data file using hooks](operations-004.md#op-0b85202e085c02) |
| Record · Department | 9 | [autoname … get children](operations-004.md#op-67bedcd18564fd) · [add node](operations-005.md#op-812f3c418b5556) |
| Record · Driver | 1 | [validate](operations-005.md#op-42dcfcdb423578) |
| Record · Email digest | 63 | [initialize … get income](operations-005.md#op-972d0f5becc06e) · [get income year to date … get pending quotations](operations-006.md#op-62854fb5f89a6a) · [get summary of pending … get random quote](operations-007.md#op-1f0f5fb052e809) |
| Record · Employee | 40 | [autoname … validate auto user creation](operations-007.md#op-130f164b2399cd) · [update nsm model … deactivate sales person](operations-008.md#op-0d8af1db55ac89) · [create user … get contact details](operations-009.md#op-c6e69f8b83af25) |
| Record · Employee group | 1 | [validate](operations-009.md#op-c8e258ac21912d) |
| Record · Global defaults | 5 | [validate … toggle in words](operations-009.md#op-ef1b8e7bcbd906) |
| Record · Holiday list | 16 | [validate … get weekly off date list](operations-009.md#op-90359bfb7ae8b1) · [clear table … get data](operations-010.md#op-ffae1b20d0e845) |
| Record · Incoterm | 1 | [create incoterms](operations-010.md#op-ce10e123e97e57) |
| Service · Install | 24 | [after install … create default role profiles](operations-010.md#op-69871d88269d46) · [update pegged currencies … after app uninstall](operations-011.md#op-d29856432f7146) |
| Service · Install fixtures | 16 | [read lines … get fy details](operations-011.md#op-b39054a0ac29b7) |
| Record · Item group | 8 | [validate … get item group defaults](operations-012.md#op-2646a00eee73ad) |
| Record · Party type | 2 | [validate … get party type](operations-012.md#op-6114fb363db13f) |
| Record · Sales partner | 9 | [onload … get commission rate](operations-012.md#op-8e55e14efce63f) |
| Record · Sales person | 12 | [validate … validate sales person](operations-012.md#op-64eea9a38f6112) · [get email id … get data](operations-013.md#op-c080dc2e5d0595) |
| Service · Setup wizard | 6 | [get setup stages … setup complete](operations-013.md#op-f659fc63e35fd8) |
| Record · Supplier group | 5 | [validate … get parent supplier groups](operations-013.md#op-c6e882299f4209) |
| Record · Target detail | 1 | [validate targets](operations-013.md#op-638811f4f91efa) |
| Service · Taxes setup | 9 | [setup taxes and charges … make taxes and charges template](operations-013.md#op-77f94b01ea4ab5) · [make item tax template … make tax category](operations-014.md#op-160e6c2972f021) |
| Record · Terms and conditions | 12 | [validate … get terms module](operations-014.md#op-c100599154668d) |
| Record · Territory | 3 | [validate … on doctype update](operations-014.md#op-d215c8e006fc1d) |
| Record · Transaction deletion record | 60 | [get protected doctypes … on discard](operations-014.md#op-9831fcf1fa6018) · [validate … delete notifications](operations-015.md#op-cf5206809afbde) · [populate doctypes to be ignored table … delete communications](operations-016.md#op-27479377e19588) · [delete comments … check for running deletion job](operations-017.md#op-fc0cf1c30b1c90) |
| Record · Uom | 2 | [validate uoms are enabled … before rename](operations-017.md#op-78750a74ed5b82) |
| Record · Uom conversion factor | 1 | [validate](operations-017.md#op-ba5fb4befa8e17) |
| Service · Utils | 12 | [get pegged currencies … set root as default parent](operations-017.md#op-62a2544e591ed9) |
| Record · Vehicle | 2 | [validate … get data](operations-017.md#op-210825abaf0965) |
