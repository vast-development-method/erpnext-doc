# CRM declarations in business application

Each dictionary part contains an ordered field list, source location, record settings and grants. The source column opens the declaration at the reviewed revision.

| Record | Storage | Fields | Dictionary | Source |
|---|---|---:|---|---|
| Appointment | ordinary | 18 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/appointment/appointment.json) |
| Appointment Booking Settings | singleton | 20 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/appointment_booking_settings/appointment_booking_settings.json) |
| Appointment Booking Slots | child | 3 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/appointment_booking_slots/appointment_booking_slots.json) |
| Availability Of Slots | child | 3 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/availability_of_slots/availability_of_slots.json) |
| CRM Note | child | 3 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/crm_note/crm_note.json) |
| CRM Settings | singleton | 19 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/crm_settings/crm_settings.json) |
| Campaign | ordinary | 7 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/campaign/campaign.json) |
| Campaign Email Schedule | child | 2 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/campaign_email_schedule/campaign_email_schedule.json) |
| Competitor | ordinary | 2 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/competitor/competitor.json) |
| Competitor Detail | child | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/competitor_detail/competitor_detail.json) |
| Contract | ordinary | 32 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/contract/contract.json) |
| Contract Fulfilment Checklist | child | 6 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/contract_fulfilment_checklist/contract_fulfilment_checklist.json) |
| Contract Template | ordinary | 7 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/contract_template/contract_template.json) |
| Contract Template Fulfilment Terms | child | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/contract_template_fulfilment_terms/contract_template_fulfilment_terms.json) |
| Email Campaign | ordinary | 8 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/email_campaign/email_campaign.json) |
| CRM integration allowed user | child | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/frappe_crm_allowed_user/frappe_crm_allowed_user.json) |
| Lead | ordinary | 71 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/lead/lead.json) |
| Lost Reason Detail | child | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/lost_reason_detail/lost_reason_detail.json) |
| Market Segment | ordinary | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/market_segment/market_segment.json) |
| Opportunity | ordinary | 84 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity/opportunity.json) |
| Opportunity Item | child | 18 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity_item/opportunity_item.json) |
| Opportunity Lost Reason | ordinary | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity_lost_reason/opportunity_lost_reason.json) |
| Opportunity Lost Reason Detail | child | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity_lost_reason_detail/opportunity_lost_reason_detail.json) |
| Opportunity Type | ordinary | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity_type/opportunity_type.json) |
| Prospect | ordinary | 31 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/prospect/prospect.json) |
| Prospect Lead | child | 7 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/prospect_lead/prospect_lead.json) |
| Prospect Opportunity | child | 9 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/prospect_opportunity/prospect_opportunity.json) |
| Sales Stage | ordinary | 1 | [Part 1](../catalog/erpnext-crm-01.json) | [Source](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/sales_stage/sales_stage.json) |
