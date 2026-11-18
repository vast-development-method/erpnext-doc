# Pane View

Kanak Infosystems' version 15 add-on places the editable form alongside a searchable, filterable list. Selecting a row loads its form. The user can resize the panes, save edits and switch back to the ordinary list. The publisher guide also describes use with custom record types. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/paneview) · [Publisher's versioned guide](https://www.kanakinfosystems.com/frappe/apps/15.0/paneview)

A public copy identifies Kanak in the manifest. The list menu extension derives the record type from the current route and opens a pane page. The page creates a framework list, rebinds row selection after rendering, resolves the selected document and constructs a framework form. Its menu fragment contains an English label and a highlighted keyboard mnemonic. That literal is an example of content a multilingual rebuild must externalize. [Menu integration](https://github.com/ggraza/paneview/blob/080f62824ce423dfb0c47a5fd2568a894062cf8b/paneview/public/js/pane_view_extension.js) · [List and form composition](https://github.com/ggraza/paneview/blob/080f62824ce423dfb0c47a5fd2568a894062cf8b/paneview/pane_view/page/pane_view/pane_view.js)

## Proposed rebuild contract

Persist the current record type, typed filters, sorting, selection ID, list scroll position and pane ratio separately from the document being edited. Selecting a clean row fetches its authorized form. On an unsaved edit, offer save, discard or stay; honour the operator's choice before replacing the form. A save carries the observed revision and changed fields. On success update the row, re-evaluate whether it still matches the filter and preserve a predictable selection. On conflict preserve the pending edits for comparison. Recheck document and field permissions on every load and save.

Drive layout from logical start/end positions. Translate menu names, prompts, tooltips, field labels, selection options and keyboard access hints through the active language's catalog. Use stable field and option keys in routes and filters. A user may switch language without renaming records, discarding text already typed or changing the meaning of a saved filter. Type-ahead may display localized names while selecting by record ID.

| Proposed acceptance case | Expected result |
|---|---|
| Filter open orders, select order 42, edit its notes and save from a German form. | Only order 42 changes. The list retains the filter and displays its updated data without leaving the split view. |
| Start an unsaved Arabic note, switch the layout to right-to-left and select order 43. Choose to stay. | The prompt is in the active language, order 42 remains selected and its note preserves the entered characters and cursor context. |
| A colleague has saved a newer revision, or write access is revoked before save. | A stable conflict or denied result is rendered in the viewer's language. The server preserves the colleague's version and the user can recover their unsaved work. |

Persistence of list state, simultaneous edit outcomes, keyboard accessibility and coverage of translated menus vary with the actual package and require verification. [Named app repository](https://github.com/kanakinfo/paneview)
