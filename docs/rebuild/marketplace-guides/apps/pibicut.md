# PibiCut

A publisher creates a Shortener record with a destination URL. Saving it produces a site URL with a random five-character path and a QR image that encodes that short URL. A reader can type the short URL or scan the image to reach the destination. The version 12/13 listing allows a centered logo and specifies an opaque white-background PNG for that input. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pibicut)

## Related implementation

A separately published project named PibiCut contains the same Shortener record, five-character default and QR-generation workflow. At the inspected revision its controller also accepts a custom code, derives the public route, regenerates the image when the code changes, and distinguishes expired links from active visits. Its metadata includes a logo, expiration, hit count and last visit. These are details of the linked project revision. The marketplace names a different owner and repository. [Related controller](https://github.com/pibico/pibicut/blob/09697b85ddc94ccdf0ef779780f093d531c0b9cb/pibicut/pibicut/doctype/shortener/shortener.py) · [Related record](https://github.com/pibico/pibicut/blob/09697b85ddc94ccdf0ef779780f093d531c0b9cb/pibicut/pibicut/doctype/shortener/shortener.json)

## Proposed publishing and resolution contract

`publishLink(destination, optionalLogo, requestId)` requires permission to publish to the chosen site. Validate the destination against the site's allowed URI schemes, reserve a unique path atomically and produce a QR image from the actual public URL. Return the record ID, short URL and image reference together. A failed logo or image conversion leaves no live route. Public resolution accepts the exact route token and returns its stored destination. A paper QR remains valid until the route's configured retirement.

| Acceptance example | Observable outcome |
|---|---|
| The editor publishes a French-language destination with an encoded accented path and query string. | A German-speaking reader typing the short URL and an Arabic-speaking reader scanning it obtain the same stored address, including escaped bytes and query order. |
| Two simultaneous saves generate the same candidate path. | Exactly one destination obtains the path. The other operation selects another free path without replacing the first. |
| A transparent logo is supplied under the published logo profile. | The editor receives a localized validation message and can retry. The original destination text remains available for correction. |
| A requested link is missing or retired. | Return the appropriate stable resolution outcome. Localize the explanatory page and image alternative text while preserving the token's exact case and direction. |

**Qualification.** The marketplace package's collision policy, destination validation, response codes, visit counting and route retirement have no independently verified revision. Custom-code and expiry features above are evidenced only in the related implementation. [Named repository](https://github.com/aoaicompany/URL-to-QR)
