# Record event boundaries · D

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Delivery charges and mobile money at tills

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer | After record creation | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |

## Device-bound authentication

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Delegated access token | Before record creation | 1 | Details outside this boundary inventory |
| System Settings | Validate record | 1 | Details outside this boundary inventory |
| User | After renaming | 1 | Details outside this boundary inventory |
| User | At removal | 1 | Details outside this boundary inventory |
| User | Before renaming | 1 | Details outside this boundary inventory |

## Document limits and usage quotas

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | Before record creation | 1 | Details outside this boundary inventory |
| Company | At record update | 1 | Read selected rows · Company (2 occurrences) |
| Company | Validate record | 1 | Read selected rows · Company (2 occurrences) |
| File | Validate record | 1 | Details outside this boundary inventory |
| User | At record update | 1 | Details outside this boundary inventory |
| User | Validate record | 1 | Details outside this boundary inventory |

## Document rendition on submission

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
