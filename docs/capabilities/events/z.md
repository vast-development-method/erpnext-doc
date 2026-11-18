# Record event boundaries · Z

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Zambian fiscal inventory reporting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | At update of a submitted record | 1 | Details outside this boundary inventory |
| Product or service | At record update | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Details outside this boundary inventory |
