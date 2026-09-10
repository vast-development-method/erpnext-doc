# Identity, permissions, and tenancy

Identity establishes the acting user and tenant. Permission decides whether that actor may perform a particular action on a particular record and field. Workflow, structural document state, and business constraints impose additional checks. A successful login is not permission to read all accounting or workforce data.

## Tenant and company boundaries

The runtime initializes a tenant context before handling an operation and attaches database, configuration, caches, current user, request, and transaction state to that context. Background jobs carry the tenant identity and restore it before execution. Real-time events also carry tenant scope. A company record inside a tenant is a business entity, not automatically another tenant. Cross-company permissions, account boundaries, and intercompany transactions therefore remain domain concerns.

An implementation must prevent a record reference, cache entry, job identifier, or event subscription from accidentally crossing tenant context. This is a behavioral isolation requirement, not a prescription for a database-per-tenant topology. The source selects a site using configured request information; the replacement's trusted tenant-selection mechanism is a transport decision. It must not treat an arbitrary untrusted tenant selector as sufficient authorization.

Evidence: source-artifact-d8764548dbbd91bf1e51 lines 111–222; source-artifact-b1ad771a8c35d6eebd3d lines 84–218; source-artifact-3d8f5f8af4a5a70b7faf lines 31–136.

## Acting identities

The system distinguishes a guest, authenticated users, and an administrative identity with a direct permission bypass. Authenticated users also have user types, including internal workspace users and website-facing users. The administrative bypass occurs before several ordinary restrictions, including the global document-sharing switch. Test business permissions using ordinary role-bearing accounts; tests performed only as the administrative identity cannot establish isolation.

Interactive sessions start or resume before request-level authentication hooks. Login policy can include account enablement, password verification, additional verification, login hours, source-address restrictions, and failed-attempt lockout. Those are configurable capabilities; the blueprint must not invent universal session lifetimes or password rules. Session-based state-changing requests apply cross-site request-forgery validation when a session token exists. The reviewed validator accepts a matching request token or configured allowed referrer; absent token and configured bypass are separate branches. Reproducing these branches requires an explicit security profile.

Credential-pair authentication supports a key and protected secret belonging to an enabled principal record. A constant-time comparison is used for the secret. The ordinary principal is a user, but a configured authentication source can resolve another enabled record to a user. Bearer-token verification and registered authentication hooks are also supported. A supplied two-part authorization header that fails to establish a non-guest identity raises authentication failure. A valid session and credential header can interact: credential-pair handling only replaces the acting user when the login manager is guest or empty. Define and test identity precedence rather than letting whichever check runs last silently win.

Source-address restrictions are explicitly rechecked when request authentication changes the acting user to a non-guest identity. The reviewed address matching uses configured prefixes; a replacement should document the intended matching syntax rather than assuming network-range parsing. Failed-login tracking uses the first failure within a lock interval and blocks when the failure count is strictly greater than the configured maximum; equality is not the rejection boundary in that helper.

Evidence: source-artifact-187d5fd72469df5def58 lines 29–113; source-artifact-187d5fd72469df5def58 lines 642–775; source-artifact-187d5fd72469df5def58 lines 517–639; source-artifact-187d5fd72469df5def58 lines 476–515; source-artifact-c07b20c42194f0dc2edd lines 82–348.

## Permission evaluation

Permissions include read, select, create, write, submit, cancel, delete, amend, report, export, import, print, email, share, and any explicitly registered custom action. Their existence does not mean every document type supports them. For example, a non-submittable type cannot gain meaningful submission simply through a normal role rule; import also requires type-level import support.

At document level, the reviewed evaluation first checks controller restrictions, then combines applicable role permissions, applies ownership conditions, and enforces user-specific linked-record restrictions. Role rules at permission level zero govern ordinary document access. An owner-only grant can provide access that a nonowner lacks. When user restrictions fail, an owner may retain only the owner-specific grants; create permission is removed in that fallback. A controller permission hook can deny but does not itself grant a missing role permission.

Explicit sharing is a later fallback when the ordinary result is false. Shareable rights include read, write, share, submit, email, print, and registered custom rights. Email and print sharing use read-sharing rights. Select permission is implied by read. Consequently the overall algorithm is not simply the intersection of role rules and controller hooks: a share can restore a shareable permission after ordinary evaluation has failed. Deletion and cancellation are not in the base shareable-right list.

For type-level access checks, the existence of one shared record can make a list surface available. It does not imply access to every row of that type. Every list, count, lookup, report, export, and document read must preserve row-level conditions. Child permission evaluation derives authority from the parent context; a child identifier is not an independent escape from the parent's permission policy.

Evidence: source-artifact-c07b20c42194f0dc2edd lines 82–348; source-artifact-c07b20c42194f0dc2edd lines 358–508.

## User restrictions across links

A user permission can restrict an allowed set of records of a referenced type and can specify the document types where it applies. These constraints can apply directly to the current record and indirectly through its linked fields, including child fields. For example, a company restriction can affect a transaction carrying a company link, but the exact fields and domain hooks decide the final result.

A link marked to ignore user permissions is excluded from this propagation. In non-strict mode an empty link is skipped. Strict mode can reject an empty link that fails the applicable allowed set, but strict checks are disabled for singleton documents and certain unsaved local-document read/write checks. Tree permissions can grant creation below an allowed ancestor unless descendant access is disabled. A specification that reduces all of this to a single company column loses important behavior.

Controller restrictions execute in reverse hook order and a false-like result denies within that layer. A custom hook must therefore deliberately return a truthy result when it intends to permit ordinary evaluation to continue. The base algorithm does not infer that an absent return means allow.

Evidence: source-artifact-c07b20c42194f0dc2edd lines 358–508.

## Field-level access and masking

Higher permission levels restrict individual fields. Read serialization removes inaccessible higher-level parent and child values, then applies masking. Mask permission is distinct from ordinary read permission; a user can read a document while seeing a masked sensitive field. The administrative identity bypasses these restrictions.

When saving an existing record, masked fields are restored from real stored values before link and user-permission checks. Higher-level fields the user cannot write are reset to existing or default values. Existing child rows are matched by identity to restore masked values; a new child has no stored counterpart. This avoids saving display placeholders as real data. It also means a client must not interpret a successful save as proof that every submitted field value was accepted. The returned authorized document is the effective outcome.

Secret fields have a protected backing store. Their normal document value is a mask, and an all-mask supplied value is treated as a placeholder. An empty secret removes its protected backing value under the base helper. A transport serializer must keep masks, absent fields, explicit clearing, and actual new secret values distinct.

Evidence: source-artifact-1c79c95fe9c8ab1bc9d4 lines 1253–1382; source-artifact-444b5a1f4b08e77b3ae8 lines 145–224; source-artifact-0f25eaf4b484dd77cdbb lines 1431–1490.

## Reports, attachments, and real-time subscriptions

Report access checks both the report's own permitted roles and report permission on its reference document type. Disabled reports cannot run. Print and export have additional permissions. Filter values referencing restricted records are checked before execution; report result processing applies its own linked-record visibility logic. A replacement must not treat reporting as a trusted backdoor around transaction permissions.

Authenticated attachment upload checks write access to a target document, including the special case of an unsaved target. File-library reuse requires read access to the selected file. Guest upload is disabled unless enabled in settings; an optional allowed-document-type list further restricts guest targets. Private upload is the default. Website-facing and guest content types have additional restrictions. These are observable settings and permission branches, not a single unconditional upload rule.

Real-time document and document-type subscriptions invoke permission checks. User rooms and tenant rooms have separate routing. The reviewed task-progress subscription joins a room by task identifier without the document-style authorization check, even for guests. This is an observed limitation: do not place secret payloads in a generic progress message based on an assumed ownership check. A replacement may require stricter task access, but that would be an explicit security improvement rather than source-equivalent behavior.

Evidence: source-artifact-e9e5a0c9d8b9908522c7 lines 27–88; source-artifact-e9e5a0c9d8b9908522c7 lines 279–333; source-artifact-e9e5a0c9d8b9908522c7 lines 108–192; source-artifact-9d66d61a7b7d9a437d11 lines 130–261; source-artifact-af5a18ab59f29558dded lines 36–138.

## Acceptance matrix

| Scenario | Required observation |
| --- | --- |
| Ordinary user without role grant | Denied unless a supported share or other documented path supplies that right |
| Owner-only write grant | Owner can write; nonowner cannot acquire write merely through list access |
| User restricted to one linked company | Parent and child links are evaluated under the configured strictness policy |
| Read-sharing without delete grant | Shared read succeeds; delete remains denied |
| Masked financial or workforce field saved unchanged | Stored real value survives; placeholder is not persisted |
| Credential header supplied alongside another user's session | Acting identity follows the documented precedence rule |
| Replayed state-changing request with invalid session token | Rejected unless a documented referrer or configuration branch applies |
| Queued work retries after a transient failure | Acting identity is recorded and compared between attempts |
| Report exported by user without export permission | Export fails even if ordinary report viewing succeeds |
| Task progress subscribed by another user | Current source limitation is measured and any replacement hardening is explicitly recorded |

The identity retained by a background retry needs particular attention: the reviewed retry call drops the initiating-user argument after releasing tenant-local state, and reconnect defaults to the administrative identity. The static call chain indicates identity may change on this retry path. It has not been reproduced in a running system; it is a documented source discrepancy to resolve in acceptance testing, not a recommendation to grant administrative privilege to retries.

Evidence: source-artifact-b1ad771a8c35d6eebd3d lines 250–328; source-artifact-66f1c84f2539463cb381 lines 372–424; source-artifact-66f1c84f2539463cb381 lines 472–479.
