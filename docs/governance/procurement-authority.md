# Purchasing authority in two organisations

An order with the same display number can exist in two separate tenants. The tenant, company, user, effective field permissions and workflow state together determine what an operator can see or do. This example assumes valid supplier, product, account and currency references and no additional sharing grants.

| Setting | Inland purchasing | Coastal purchasing |
|---|---|---|
| Tender field | Tender decision reference, protected at access level one | Procurement reference, ordinary read access |
| Purchasing officer | Read, create and update orders for authorised companies | Read orders within the officer’s authority |
| Purchasing manager | Read level one and approve eligible Trading orders | Subject to the coastal role and transition rules |
| Stock observer | No order read grant | Ordinary order read grant |
| Trading order-number counter | Company-specific prefix PO-T-, four digits, last issued 9 | Same prefix, last issued 79 |

The field has one durable identity throughout the document. Changing its label from *Tender reference* to *Tender decision reference* changes neither the contents nor the access level by itself. An effective rule can change the access level independently. Resolve record access before returning individual field values.

| Attempt | Expected decision |
|---|---|
| Stock observer reads order PO-041 in each tenant | Coastal permits its read and exposes its tender value CO-812. Inland refuses the order read. |
| Purchasing officer reads inland PO-041, company Trading | Return the ordinary order fields. Exclude the protected tender value IN-315 from the returned fields. |
| Manager reads that order, then requests an order for unauthorised company Transport | Include the inland tender value on the first order. Refuse the second read and its list of eligible actions. |
| Manager approves another user's inland order at a validated company-currency total of 10,000.00 | Allow the transition within the inclusive threshold, then run ordinary order submission. Reject 10,000.01. |
| Manager tries to approve their own 25.00 order | The action can appear when listed. At execution, the self-approval condition refuses it. The order remains a draft. |
| Manager repeats approval after successful submission | Reload the stored state and refuse the unavailable transition. The coastal order with the same number remains a draft. |
| Each tenant allocates its next Trading purchase order number | Inland issues PO-T-0010, coastal PO-T-0080. A lower-priority inland rule can issue PO-0040 for Transport without consuming the next Trading number, PO-T-0011. |

Changing a field definition, hiding a control, removing a read grant and rejecting a business transition have four separate observable results. An import and a remote service need the same company and action checks as the interactive form.

[Company eligibility](company-and-master-governance.md) · [Access and tenancy](../services/identity-permissions-and-tenancy.md)
