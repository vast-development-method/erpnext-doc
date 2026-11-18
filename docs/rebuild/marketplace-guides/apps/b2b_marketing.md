# B2B Marketing

Apoorv Soral’s listing describes account-based campaigns that turn an uploaded or filtered contact pool into scheduled agent calls. The publisher lists versions 14 and 15. [Marketplace listing and workflow](https://cloud.frappe.io/marketplace/apps/b2b_marketing)

## Documented workflow

A campaign manager uses Campaign Designer to select contacts by configured filters, set a calling sequence and define a quality review policy. The system distributes scheduled calls across an agent pool. A Do Not Call list, call recording, manager review and agent performance reports support campaign operations. The publisher also describes creating leads and billing campaign customers through the ERP invoicing module. The listing does not define the billable unit, the allocation algorithm or when the suppression list is rechecked. [Publisher’s feature walkthrough](https://cloud.frappe.io/marketplace/apps/b2b_marketing)

## Proposed rebuild contract

Model the customer purchasing the campaign separately from each business contact being called. Track the import batch and source row, canonical contact/number, campaign membership, suppression entry, scheduled attempt, agent, call outcome and recording reference. A review stores its rubric version and links to one attempt. Put billable events through a distinct contract that references the campaign agreement and generated invoice line.

1. Preview a filtered audience with counts for eligible, duplicate and suppressed contacts. Confirm an audience version and sequence before scheduling.
2. At dispatch, recheck current suppression and contact availability. Claim the next eligible attempt atomically and record who owns it. A call provider response completes that attempt. A later retry has its own identity.
3. A manager reviews recordings permitted for that campaign, using the rubric in force for the call. A billing user converts accepted billable events into invoice lines with a trace back to campaign activity.

## Language and acceptance

Store the agent’s interface language separately from the contact’s preferred language, outbound script variant and recording language. Translate review criteria and call outcomes by stable identifiers. A suppression applies to the dialling identity across every script language. Preserve a recorded conversation as spoken and label any subsequent translated transcript separately.

- Import the same normalised telephone number twice. After deduplication a two-step campaign has one eligible member and at most one assignment for the first step. A retry of the scheduling operation leaves that assignment intact.
- If an opted-out contact enters the Do Not Call list after audience selection and before dispatch, a Spanish script must stay suppressed even when the original campaign used English. Record the suppression decision and zero billable calls for that attempt.
- For a contract that charges per accepted review, two completed calls and one accepted review produce one billable unit. Reopening a review after invoicing produces a linked adjustment for approval.

These are proposed acceptance conditions. Consent handling, actual workload tie-breaks, invoice rate calculation and recordings’ retention require deployment evidence. [Publisher-named repository](https://github.com/asoral/b2b_marketing)

The publisher also preserved an illustrated Campaign Designer walkthrough and identifies calling-provider fees in a README in a separate cargo repository. Its screenshots and instructions corroborate the marketing workflow. The package in that repository identifies itself as a cargo app. [Archived publisher walkthrough](https://github.com/asoral/mm_cargo/blob/e35c3ffff274335d72e49280aa2b2f37f5d7fcb0/README.md#L44)
