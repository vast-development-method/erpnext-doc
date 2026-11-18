# Record event boundaries · R

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Reception access and room booking

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Job Applicant | After record creation | 1 | Details outside this boundary inventory |
| Job Applicant | At record update | 1 | Details outside this boundary inventory |

## Recipient template message campaigns

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | After save | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | At value change | 1 | Details outside this boundary inventory |

## Restaurant orders and station routing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | Before record creation | 1 | Details outside this boundary inventory |
| Point of sale configuration | At creation | 1 | Details outside this boundary inventory |
| Point of sale configuration | At record update | 1 | Details outside this boundary inventory |
| Point of sale configuration | Validate record | 1 | Details outside this boundary inventory |
| Point of sale invoice | After record creation | 1 | Read field value · Till shift opening (3 occurrences); Read most recent matching record · Point of sale invoice (2 occurrences); Write field value · Point of sale invoice (3 occurrences); Write field value · Till shift opening (2 occurrences) |
| Point of sale invoice | At cancellation | 1 | Details outside this boundary inventory |
| Point of sale invoice | At record update | 1 | Details outside this boundary inventory |
| Point of sale invoice | At removal | 1 | Details outside this boundary inventory |
| Point of sale invoice | At submission | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before record creation | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before submission | 1 | Details outside this boundary inventory |
| Point of sale invoice | Validate record | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Details outside this boundary inventory |
| Restaurant menu course | Validate record | 1 | Details outside this boundary inventory |
| Till configuration user | At creation | 1 | Details outside this boundary inventory |
| Till configuration user | At record update | 1 | Details outside this boundary inventory |
| Till shift closing | At cancellation | 1 | Details outside this boundary inventory |
| Till shift closing | At submission | 1 | Details outside this boundary inventory |
| Till shift closing | Before save | 1 | Details outside this boundary inventory |
| Till shift closing | Validate record | 1 | Details outside this boundary inventory |
| Till shift opening | Before record creation | 1 | Read most recent matching record · Point of sale invoice (2 occurrences) |
| Till shift opening | Before save | 1 | Details outside this boundary inventory |
| Till shift opening | Validate record | 1 | Read field value · Point of sale configuration |

## Retail checkout

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Validate record | 2 | Details outside this boundary inventory |
| Till shift opening | Validate record | 1 | Check existence · Till shift opening |

## Reusable letterhead design

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Document letterhead | At record update | 1 | Details outside this boundary inventory |

## Role and grant duplication

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User Permission | Before deletion | 1 | Details outside this boundary inventory |

## Role assignment administration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User | At record update | 1 | Details outside this boundary inventory |
