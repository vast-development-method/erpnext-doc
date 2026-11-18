# Donations, membership and grants

A donor, member, volunteer, chapter participant and customer can refer to the same person. Each has its own purpose and record identity. A recurring membership subscription is an agreement. A membership is a dated entitlement. A donation is a gift. A payment is the movement of funds against its identified purpose.

## Receive a donation

For a configured capture channel, verify the signature and accept the completed capture event for an individual donation. Skip invoice-linked payments and those identified as subscription payments. Resolve the donor by email or create a donor, then resolve or create the payment mode. Store the provider transaction identity and the amount in the currency of the gift. For a configured minor unit of one hundredth, 125,050 minor units become 1,250.50. Submit the donation. With automated accounting enabled, require the configured donation payment account and submit the receipt against the donation with the configured account mappings. Otherwise the submitted donation and the bank transaction still require separate reconciliation.

Repeated notification, later refund and two gifts of equal value from the same donor are separate cases. The required retry safeguard is to deduplicate by the actual external payment identity in its receiving account, while permitting distinct payment identities at the same amount and email. Count one financial receipt and one submitted gift for a retried capture. The signature and email match alone establish neither uniqueness nor settlement.

## Enrol, renew and invoice a member

| Operation | Decision | Effects |
|---|---|---|
| Choose the member | Back-office creation requires a valid member. A signed-in portal user may resolve their member by their own email or create one from their account name, email and membership type. | Store the member on the new application. The billing customer link, subscription identity and membership identity each serve separate lookups. |
| Renew | Find the latest **paid** membership for the member, ordered by end date. For an ordinary renewal by someone other than the system administrator, exclude the membership being edited and refuse a renewal when expiry is more than 30 days away. Exactly 30 days qualifies. | Start the renewal one day after that previous expiry. Yearly billing sets the new end one year after the new start. Other billing cycles on this path set it one month after the start. The automatic end calculation does not subtract a day. |
| Record authorized payment | An accepted authorization or completion notification sets paid. Where membership invoicing and automatic membership invoicing are both enabled, request an invoice, optionally with a payment entry. | The paid indicator is independent of the downstream invoice and posted bank receipt. |
| Generate invoice | Require a member-linked customer, a selling item on the membership plan, the billing company and its membership receivables account. A previously linked invoice blocks another. The initial payment-data check rejects when paid, currency and amount are all absent. | Submit a sales invoice with one unit of the plan's selling item, membership amount as rate, membership currency and selected receivables account. Save the invoice identity on this membership. |
| Generate receipt | When selected, require a membership payment account. Use the invoice grand total and membership reference on the payment. | Submit the receipt into that account and retain the invoice-to-payment allocation. Partial payments outside this operation require their own settlement records. |
| Send acknowledgment | Outbound acknowledgment must be enabled and the member must have an email address. | Render the selected membership form and optionally the linked sales invoice. Delivery and accounting settlement have separate outcomes. |

For a prior paid membership ending 30 June, ordinary renewal on 30 May is too early, and on 31 May it is allowed. The new interval begins 1 July. Under annual billing the end is 1 July of the following year. A pending or unpaid membership does not establish the renewal cutoff by itself.

## Grants and participation

A grant application identifies the individual or organisation, assessment manager, requested amount and review state. The application can be Open, Received, In Progress, Approved, Rejected, Expired or Withdrawn. Inviting the assessment manager sends a message linked to the application, marks the review invitation as sent and changes the state to In Progress. A delivered invitation is neither approval nor disbursement. If the mail service accepts a message but saving the changed application fails, inspect the message history before sending another. Approval and actual distribution of grant cash have separate authorities and dates.

Chapters maintain rows linking people to local participation. Leaving a chapter disables matching membership rows and stores the reason. A departure retains the person's membership and donation history. Volunteers have an availability pattern, preferred time of day and one or more skills. Recruiting a volunteer does not implicitly grant them access to a donor list or a grant assessment. Nonprofit management roles administer donor records, chapters and grant reviews. A membership role may create or maintain membership documents subject to record access and the signed-in member's scope. Financial submission or bank reconciliation requires its own grant.
