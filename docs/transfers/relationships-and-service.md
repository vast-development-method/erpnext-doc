# Relationships and service conversions

[Structured field mappings](relationships-and-service.json) · [All conversions](README.md)

## Register a customer from a sales lead

`sales_relationships.lead` → `sales.customer`

Use a company customer when a company name exists. Otherwise use an individual customer and the lead's personal name. Resolve the default customer group and connect the primary address and contact. A disabled lead flag does not automatically disable its converted customer.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.lead.record_identifier` | `sales.customer.lead_name_identifier` |
| `sales_relationships.lead.company_name` | `sales.customer.customer_name` |

## Qualify a lead into a sales opportunity

`sales_relationships.lead` → `sales_relationships.opportunity`

The new opportunity identifies the lead as its party and preserves the responsible owner and contact details. Contact display text and the customer company name remain separate.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.lead.entity_type` | `sales_relationships.opportunity.opportunity_from_identifier` |
| `sales_relationships.lead.record_identifier` | `sales_relationships.opportunity.party_name_identifier` |
| `sales_relationships.lead.lead_name` | `sales_relationships.opportunity.contact_display` |
| `sales_relationships.lead.company_name` | `sales_relationships.opportunity.customer_name` |
| `sales_relationships.lead.email_identifier` | `sales_relationships.opportunity.contact_email` |
| `sales_relationships.lead.mobile_number` | `sales_relationships.opportunity.contact_mobile` |
| `sales_relationships.lead.lead_owner_identifier` | `sales_relationships.opportunity.opportunity_owner_identifier` |
| `sales_relationships.lead.notes_rows` | `sales_relationships.opportunity.notes_rows` |

## Prepare a quotation for a lead

`sales_relationships.lead` → `sales.quotation`

Use the lead as the party and set the quotation recipient kind to lead. Preparing a quotation does not require creating a customer master first.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.lead.record_identifier` | `sales.quotation.party_name_identifier` |
| `sales_relationships.lead.entity_type` | `sales.quotation.quotation_to_identifier` |

## Quote a sales opportunity

`sales_relationships.opportunity` → `sales.quotation`

Use the opportunity's party kind for the quotation recipient. Retain the opportunity identity and set the exchange rate for the quotation context. Add opportunity item rows only when the receiving collection is empty.

Quotation item rows. Only add rows when the destination collection is empty.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.opportunity.opportunity_from_identifier` | `sales.quotation.quotation_to_identifier` |
| `sales_relationships.opportunity.record_identifier` | `sales.quotation.opportunity_identifier` |
| `sales_relationships.opportunity_item.owning_record_identifier` | `sales.quotation_item.prevdoc_record_identifier` |
| `sales_relationships.opportunity_item.owning_entity_type` | `sales.quotation_item.prevdoc_entity_type_identifier` |
| `sales_relationships.opportunity_item.unit_of_measure_identifier` | `sales.quotation_item.stock_unit_of_measure_identifier` |

## Register the customer represented by an opportunity

`sales_relationships.opportunity` → `sales.customer`

Carry the opportunity currency into the customer's default currency and retain the originating opportunity. When the party is a lead, connect the new customer with that lead. The customer receives its own identity.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.opportunity.currency_identifier` | `sales.customer.default_currency_identifier` |
| `sales_relationships.opportunity.customer_name` | `sales.customer.customer_name` |
| `sales_relationships.opportunity.record_identifier` | `sales.customer.opportunity_name_identifier` |

## Register a company customer from a prospect

`sales_relationships.prospect` → `sales.customer`

Require access to read the prospect and create customers. Block a second conversion of the same prospect. Classify the customer as a company, use the prospect company name and take the prospect group or the default customer group. Associate the lead only when exactly one lead belongs to the prospect and no customer already uses that lead.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.prospect.company_name` | `sales.customer.customer_name` |

## Open an opportunity for a prospect

`sales_relationships.prospect` → `sales_relationships.opportunity`

Select prospect as party kind. Preserve its owner as opportunity owner, its company name and its customer group or the default group.

| Source record and field | Destination record and field |
|---|---|
| `sales_relationships.prospect.record_identifier` | `sales_relationships.opportunity.party_name_identifier` |
| `sales_relationships.prospect.prospect_owner_identifier` | `sales_relationships.opportunity.opportunity_owner_identifier` |
| `sales_relationships.prospect.company_name` | `sales_relationships.opportunity.customer_name` |

## Prepare a quotation for an existing customer

`sales.customer` → `sales.quotation`

Use customer as the party kind, select its selling price list and currency, and retain the customer identity as the quotation party.

| Source record and field | Destination record and field |
|---|---|
| `sales.customer.record_identifier` | `sales.quotation.party_name_identifier` |
| `sales.customer.entity_type` | `sales.quotation.quotation_to_identifier` |

## Open a sales opportunity for a customer

`sales.customer` → `sales_relationships.opportunity`

Use a customer party with its persistent identifier. Opportunity stage and closure remain separate from the customer's standing.

| Source record and field | Destination record and field |
|---|---|
| `sales.customer.record_identifier` | `sales_relationships.opportunity.party_name_identifier` |
| `sales.customer.entity_type` | `sales_relationships.opportunity.opportunity_from_identifier` |

## Raise a support case from a message

`information_management.communication` → `customer_support.issue`

Check read access on the specific message. Create the case with subject, message body, medium and reporting party details, then associate the message with the case. Copying its text is distinct from sharing every related private record.

| Source record and field | Destination record and field |
|---|---|
| `information_management.communication.subject` | `customer_support.issue.subject` |
| `information_management.communication.content` | `customer_support.issue.description` |
