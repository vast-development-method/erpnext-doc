# Business operation reading guide

Find the record, report or service involved in the workflow. Its operation page gives the declared inputs, local decisions, returned values, named calls and failure paths. Each entry opens the applicable decision contract at its own stable identifier.

| Begin with the business area | Retained procedures | Current procedures | Total |
|---|---:|---:|---:|
| [Enterprise transactions](enterprise/README.md) | 4,184 | 6,791 | 10,975 |
| [Shared records and services](foundation/README.md) | 6,028 | 3,402 | 9,430 |
| [Workforce and payroll](workforce/README.md) | 1,458 | 352 | 1,810 |
| [Customer relationships](relationships/README.md) | 711 | 269 | 980 |
| **All four areas** | **12,381** | **10,814** | **23,195** |

Each business area also has an alphabetical stable-identifier lookup for its own bindings. Each workflow index groups operations by their owning record, report or service. An operation declared against a shared controller can apply to more than one document type. [Reading conventions](reading.md)

For a short reading path, follow how a generated user name survives a concurrent insert, how a zero stock rate becomes a row warning, or which payment types pass the first validation. Each example identifies the operation responsible for the decision and the inputs that determine the outcome. [Worked readings](examples.md)

The coverage account distinguishes locally recorded decision sites, worked examples and conditions that depend on the caller, database or external provider. [Scope and evidence](coverage.md)
