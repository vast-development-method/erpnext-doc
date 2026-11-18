# Optional report procedures

Each [report guide](../README.md) links its own module bindings and ordered procedures. A procedure identifies its local name, source location, ordered parameters, wrappers and decision steps. Read step tags using the [operation notation](../../../../../schemas/operations/current-decisions/notation.json) and [evaluation rules](../../../../../schemas/operations/current-decisions/README.md). The [adapter vocabulary](adapter-terms.json) supplies exact source spellings for keys carried by adapter terms.

Module bindings identify constants, dependencies and class inheritance. A derived controller may reuse a row selector or column builder from its parent class. Imported service calls depend on their owning component, installed configuration and actual input records. These files cover the definitions in each listed report module; they do not simulate database queries or provider replies.
