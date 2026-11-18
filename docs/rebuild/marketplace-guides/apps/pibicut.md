# PibiCut

[Business workflow and acceptance cases](../../../capabilities/guides/workspace.md#short-links-and-scannable-destinations).

A publisher creates a Shortener record with a destination URL. Saving it produces a site URL with a random five-character path and a QR image that encodes that short URL. A reader can type the short URL or scan the image to reach the destination. The version 12/13 listing allows a centered logo and specifies an opaque white-background PNG for that input. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pibicut)

## Related implementation

A separately published project named PibiCut contains the same Shortener record, five-character default and QR-generation workflow. At the inspected revision its controller also accepts a custom code, derives the public route, regenerates the image when the code changes, and distinguishes expired links from active visits. Its metadata includes a logo, expiration, hit count and last visit. These are details of the linked project revision. The marketplace names a different owner and repository. [Related controller](https://github.com/pibico/pibicut/blob/09697b85ddc94ccdf0ef779780f093d531c0b9cb/pibicut/pibicut/doctype/shortener/shortener.py) · [Related record](https://github.com/pibico/pibicut/blob/09697b85ddc94ccdf0ef779780f093d531c0b9cb/pibicut/pibicut/doctype/shortener/shortener.json)

## Proposed publishing and resolution contract

**Qualification.** The marketplace package's collision policy, destination validation, response codes, visit counting and route retirement have no independently verified revision. Custom-code and expiry features above are evidenced only in the related implementation. [Named repository](https://github.com/aoaicompany/URL-to-QR)

[Read the consolidated workflow](../../../capabilities/guides/workspace.md#short-links-and-scannable-destinations-2).
