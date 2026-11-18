# Application composition and recovery

## Effective metadata and extension precedence

Resolve installed applications and their configured order for the site. Ordinary effective metadata adds site fields, applies property overrides, builds field lookup caches, sorts fields, resolves valid stored columns, replaces permissions with configured custom permissions where applicable, and adds links and actions. Special framework definitions use a limited initialization path to avoid recursive metadata construction. A schema exported from a clean installation must identify its application revisions and site customization profile. Importing a customized invoice with a new required dimension needs the corresponding effective definition before posting.

For a standard type, resolve the base business controller. If multiple applications replace it, the last registered replacement wins and must conform to the original type's contract. Additional behavior extensions are ordered in reverse registration order ahead of the selected base. Cooperative delegation can invoke the next behavior; an extension can also terminate dispatch. With replacements R1 then R2 and extensions A then B, the effective precedence is B, A, R2, original ancestry. This establishes lookup order, not a guarantee that every participant runs. A site-defined custom record takes the generic tree or ordinary path earlier in this controller resolver.

Registration has different collision rules per capability. When two automation action providers publish the same action type, registry construction rejects the duplicate. Treat this differently from last-replacement-wins. Record effective types, field overrides, providers, exposed operations, execution rights and required dependencies before promoting a site's configuration.

## Backup and restore boundaries

The full backup generator handles a database dump, site configuration, public files and private files. A database-only mode can skip the two file archives, and table inclusion/exclusion can yield a partial database. An existing recent set can be reused unless forced. On a fresh generation the path takes the database dump, copies the configuration and optionally archives files, with optional encryption. These are successive steps. Timestamp proximity does not establish one atomic snapshot across the database and both file stores. The restore path restores the database before extracting whichever public and private archives were supplied. A successful database restore does not establish that all attachment bytes or encrypted business credentials are usable.

**Recovery acceptance.** Record generation identity, component sizes and digests, tenant configuration identity, site, table scope, file inclusion and key references in an integrity manifest. In an isolated restore, select known submitted sale and purchase vouchers, verify balanced book entries, re-read an authorized private attachment, confirm that another company restriction still excludes its records, and reconcile the number and statuses of previously in-flight work items. Keep external side effects isolated during the exercise. Reject a completeness claim if a required private archive, key or table is absent. Record recovery point and time from observed evidence, without inferring them from backup frequency.

## Scoped configuration example

Two tenants can both use purchase order PO-041 with independent numbering, permissions and approvals. In the coastal tenant an inventory observer can read the order. In the inland tenant only a buyer or purchasing manager can read it, and a tender decision reference requires an elevated field grant. Approving the inland record must leave the coastal record in draft.

Apply optional capabilities in the tenant's configured order. Apply custom fields to the target type, then typed property settings before deriving valid fields and access levels. Where a nonempty custom grant collection replaces the grants for a top-level record type, evaluate the resulting set in full. An empty collection in a customization import can mean skip permission synchronization. It must be distinguishable from an explicit request to remove all grants. Changing the label of the tender decision reference preserves its identity and existing values.

For numbering, evaluate the company-specific rule before the general rule when its priority is higher. Lock that tenant's matching rule counter for allocation and retain the resulting number under the business record. The coastal and inland tenants can independently allocate the same display key. A restore must preserve the counter state as well as previously issued identifiers.

## Restore exercise

Capture a committed note, its public and restricted attachments and an identifier counter whose last issued number is 0002. After capture, amend the original note and allocate 0003. Restore into a separate tenant and resolve both files through the restored attachment records. Verify content digests, attachment privacy, owner reference and authorized download. The restored note must contain the pre-capture text and its next allocation must be 0003. A new read in the original tenant must still show the later content and its own counters. Detect a restore that copied the files under a different path even if the database, row counts and byte hashes all look correct.
