# Pane View

[Business workflow and acceptance cases](../../../capabilities/guides/workspace.md#split-view-record-editing).

Kanak Infosystems' version 15 add-on places the editable form alongside a searchable, filterable list. Selecting a row loads its form. The user can resize the panes, save edits and switch back to the ordinary list. The publisher guide also describes use with custom record types. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/paneview) · [Publisher's versioned guide](https://www.kanakinfosystems.com/frappe/apps/15.0/paneview)

A public copy identifies Kanak in the manifest. The list menu extension derives the record type from the current route and opens a pane page. The page creates a framework list, rebinds row selection after rendering, resolves the selected document and constructs a framework form. Its menu fragment contains an English label and a highlighted keyboard mnemonic. That literal is an example of content a multilingual rebuild must externalize. [Menu integration](https://github.com/ggraza/paneview/blob/080f62824ce423dfb0c47a5fd2568a894062cf8b/paneview/public/js/pane_view_extension.js) · [List and form composition](https://github.com/ggraza/paneview/blob/080f62824ce423dfb0c47a5fd2568a894062cf8b/paneview/pane_view/page/pane_view/pane_view.js)

## Proposed rebuild contract

Persistence of list state, simultaneous edit outcomes, keyboard accessibility and coverage of translated menus vary with the actual package and require verification. [Named app repository](https://github.com/kanakinfo/paneview)

[Read the consolidated workflow](../../../capabilities/guides/workspace.md#split-view-record-editing-1).
