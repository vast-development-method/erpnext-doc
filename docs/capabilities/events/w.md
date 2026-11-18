# Record event boundaries · W

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Warehouse pallet capacity and pick faces

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Pick List | At cancellation | 1 | Details outside this boundary inventory |
| Pick List | At submission | 1 | Details outside this boundary inventory |

## Warehouse product group restrictions

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Before save | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Dispatch note | Before save | 1 | Details outside this boundary inventory |
| Dispatch note | Before submission | 1 | Details outside this boundary inventory |
| Goods receipt | Before save | 1 | Details outside this boundary inventory |
| Goods receipt | Before submission | 1 | Details outside this boundary inventory |
| Inventory count adjustment | Before save | 1 | Details outside this boundary inventory |
| Inventory count adjustment | Before submission | 1 | Details outside this boundary inventory |
| Inventory movement | Before save | 1 | Details outside this boundary inventory |
| Inventory movement | Before submission | 1 | Details outside this boundary inventory |
| Supplier invoice | Before save | 1 | Details outside this boundary inventory |
| Supplier invoice | Before submission | 1 | Details outside this boundary inventory |

## Web content and enquiry management

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Color Palette | At record update | 1 | Details outside this boundary inventory |
| Footer Component | At record update | 1 | Details outside this boundary inventory |
| Header Component | At record update | 1 | Details outside this boundary inventory |
| Page composition | At record update | 1 | Details outside this boundary inventory |

## Web page composition

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User Invitation | After record creation | 1 | Details outside this boundary inventory |

## Workforce administration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Attendance | At cancellation | 2 | Details outside this boundary inventory |
| Attendance | At removal | 1 | Details outside this boundary inventory |
| Attendance | At submission | 1 | Details outside this boundary inventory |
| Leave Application | At cancellation | 3 | Details outside this boundary inventory |
| Leave Application | At submission | 2 | Details outside this boundary inventory |
| Leave Application | At value change | 1 | Details outside this boundary inventory |
| Leave Application | Validate record | 1 | Details outside this boundary inventory |
| Overtime Ledger Entry | After record creation | 1 | Details outside this boundary inventory |

## Workspace presentation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User | After record creation | 1 | Details outside this boundary inventory |
| User | At record update | 1 | Details outside this boundary inventory |

## Workspace presentation preferences

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | After record creation | 1 | Details outside this boundary inventory |
| Theme Settings | At record update | 1 | Details outside this boundary inventory |

## Workspace sound and theme preferences

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User | After record creation | 2 | Details outside this boundary inventory |
