# Rename and media-adapter observations

The [record administration and video contract](../../services/identity-and-media.md) describes admission, permission, record ownership, partial failure, retry and refresh. In the observed implementation, the selected rename target must allow renaming and belong to a module other than Core. The tool grants its standard permissions to System Manager. The form confirms queue admission and shows job counts by worker status. A job can finish with individual failures because the worker handles exceptions row by row. The reference worker identifies failures using a translated message prefix. A rebuild can expose an explicit outcome per row, localize its message for the operator and preserve the original keys, input position and merge flag. A translated label for a customer or item must continue to refer to the same identity. [Language contract](../marketplace-guides/languages/README.md)

## Media adapter details

The Video record uses its unique title for its initial record name. Title, provider, URL and description are required. The provider choices are YouTube and Vimeo. Publication date, duration and image belong to the local catalog. A distinct provider-specific ID supports tracking. The declared Desk User rights are owner-scoped, while System Manager has a separate grant. The form's playback action passes the stored provider ID when available or otherwise passes the supplied URL.

The statistics adapter accepts youtube.com, youtu.be, youtube-nocookie.com and their subdomains. It reads the first path segment of a short link, the second segment of embed, shorts, live and v routes, or the first v query parameter. A valid eleven-character provider ID is stored even when tracking is disabled. Vimeo uses playback without the YouTube identifier or statistics path. Enabling tracking verifies the credential through the language-list service, independently of content language. The retained half-hour setting converts to one hour on save.

## Acceptance examples

| Input | Expected observation | Evidence level |
|---|---|---|
| Rename A to B, request a rename that raises an error, supply one incomplete row, then merge C into D using TRUE | Three calls to the record operation, two commits, one rollback and one search rebuild request. Only the last call carries the merge flag. | Source-derived row-processing case. |
| Submit 501 valid rename pairs in one attached CSV | The committed request schedules blocks of 500 and 1. A failure in the first block cannot undo a committed row in the second. Use row outcomes to determine the items still outstanding. | Proposed end-to-end case from the admission and worker code. |
| The same ID Abc_012-DEF appears as a short URL and a shorts URL, then with an unrelated hostname | Both accepted forms yield exactly Abc_012-DEF. The unrelated hostname yields no parsed ID. The public validator surfaces invalid input as a validation failure. | Source-derived parser and validator case. |
| Six-hour tracking last ran at 06:55. The scheduler checks at 11:59 and 12:01 on the same date | The first check is early. The second is due, although fewer than six full elapsed hours have passed at 12:01. | Source-derived clock-boundary case. |
| The provider returns 70 views for one ID and omits another ID. A German-speaking operator opens the same videos after an Afrikaans-speaking editor | The first record shows 70 views and the second retains its prior counts. Both operators see the same local and provider identities. UI language affects presentation. | Proposed integrated acceptance case. |

The upstream [rename tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/test_rename_tool.py#L14-L75) exercise attachment ownership over successive imports and row-failure notification with inline jobs. The [video tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/test_video.py#L17-L139) supply provider fixtures, and the [settings tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video_settings/test_video_settings.py#L10-L38) cover missing credentials, video-save failure handling and frequency migration. Production provider quotas, current responses and concurrent workers require separate integration evidence.

The full upstream rename, video and video-settings suites passed in the [recorded workflow run](reference-tests.md).

## Sources by operation

### Rename or merge records from an attachment

- [Tool metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/rename_tool.json#L32-L51)
- [Admission](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/rename_tool.py#L44-L75)
- [Record checks](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L334-L393)
- [Upload and pagination](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/rename_tool.py#L44-L63)
- [Attachment selection and cleanup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/rename_tool.py#L101-L118)
- [Row reader](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L673-L710)
- [Pre-rename processing](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L143-L167)
- [Destination rules](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L346-L390)
- [Identity changes](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L169-L232)
- [Parent, children and naming field](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L319-L332)
- [Row transactions](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/rename_doc.py#L686-L710)
- [Failure notification](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/rename_tool.py#L77-L98)
- [User confirmation and worker counts](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/rename_tool/rename_tool.js#L16-L75)

### Register a video and refresh counts

- [Record definition and permissions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.json)
- [Playback action](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.js#L4-L17)
- [Validation and individual refresh](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.py#L42-L72)
- [URL and ID rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.py#L114-L144)
- [Settings declaration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video_settings/video_settings.json#L13-L63)
- [Settings validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video_settings/video_settings.py#L26-L53)
- [Single-record refresh and schedule decision](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.py#L54-L102)
- [Hourly registration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/hooks.py#L523-L532)
- [Batch selection and updates](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.py#L147-L193)
- [Timestamp update](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/utilities/doctype/video/video.py#L75-L82)
