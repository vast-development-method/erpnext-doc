# Record event boundaries · G

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Gate compliance and discrepancies

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At removal | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Dispatch note | At cancellation | 1 | Details outside this boundary inventory |
| Dispatch note | At removal | 1 | Details outside this boundary inventory |
| Dispatch note | At submission | 1 | Details outside this boundary inventory |
| Dispatch note | Before submission | 1 | Details outside this boundary inventory |
| Dispatch note | Validate record | 1 | Details outside this boundary inventory |
| File | At removal | 1 | Details outside this boundary inventory |
| Goods receipt | At cancellation | 1 | Details outside this boundary inventory |
| Goods receipt | At removal | 1 | Details outside this boundary inventory |
| Goods receipt | At submission | 1 | Details outside this boundary inventory |
| Goods receipt | Before submission | 1 | Details outside this boundary inventory |
| Goods receipt | Validate record | 1 | Details outside this boundary inventory |
| Inventory movement | At cancellation | 1 | Details outside this boundary inventory |
| Inventory movement | At removal | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 2 | Details outside this boundary inventory |
| Inventory movement | Before submission | 1 | Details outside this boundary inventory |
| Inventory movement | Validate record | 1 | Details outside this boundary inventory |
| Purchase Order | At submission | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | At cancellation | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | At removal | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | At submission | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | Before submission | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | Validate record | 1 | Details outside this boundary inventory |

## Gate dispatch and returns

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Goods receipt | At cancellation | 1 | Details outside this boundary inventory |
| Goods receipt | At removal | 1 | Details outside this boundary inventory |
| Inventory movement | At cancellation | 1 | Details outside this boundary inventory |
| Inventory movement | At removal | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | At cancellation | 1 | Details outside this boundary inventory |
| Subcontracting Receipt | At removal | 1 | Details outside this boundary inventory |

## German accounting export

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At submission | 1 | Details outside this boundary inventory |

## Group appointments and availability

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Leave Application | At cancellation | 1 | Details outside this boundary inventory |
| Leave Application | At removal | 1 | Details outside this boundary inventory |
| Leave Application | At submission | 1 | Details outside this boundary inventory |
