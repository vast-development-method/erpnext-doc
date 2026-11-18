# Record event boundaries · Q

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Quotation and proposal synchronization

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Quotation | At record update | 1 | Details outside this boundary inventory |
