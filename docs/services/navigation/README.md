# Navigation and destinations

Each entry gives an operator-facing area, an ordered collection, and either a layout group or a destination. Positions are one-based within each area and collection. Separate menus can legitimately lead to the same report with different filters. Shortcuts opening a new record can supply initial field values. The destination must still apply its effective read, creation or reporting rights.

| Navigation surface | Entries |
|---|---:|
| [Area Menu](area-menu.json) | 479 |
| [Area Selector](area-selector.json) | 26 |
| [Dashboard](dashboard.json) | 74 |
| [Report Centre](report-centre.json) | 4 |
| [Workspace](workspace.json) | 953 |
| [Workspace Menu](workspace-menu.json) | 395 |

Two destination names require a tenant-provided binding. The inventory workspace names an item standard cost record and the system area menu names a background task record. Resolve their effective record types and permissions before displaying an actionable destination. A visible but unresolved label must not grant access or select a similarly named record by accident.
