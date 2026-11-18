# Relationship decisions

Static and variable relationships are part of the record contracts. The entries below require a decision before instantiating a specific optional configuration. When binding a supplied external class, specify its key, tenant and company scope, cardinality, deletion policy and effective access checks. When choosing between local variants, bind one variant consistently for each field. For a collection whose target is declared independent, define whether the parent owns a child row or merely references a separately owned row before applying cascade rules.

| Capability and configuration | Owner and field | Required decision | Candidate record or records | Contract |
|---|---|---|---|---|
| Accommodation reservations, 1 | `channel_provider_connection.handles_agent` | Supply the external record contract | `agent` | [Open](volume-001.json) |
| Accommodation reservations, 1 | `vendor_bill.vendor` | Supply the external record contract | `vendor` | [Open](volume-003.json) |
| Congregational care and events, 1 | `expense.vendor` | Supply the external record contract | `vendor` | [Open](volume-013.json) |
| Consignment delivery management, 1 | `indent.rate_type` | Choose the local record configuration | `truck_type_master_data`, `truck_type_configuration` | [Open](volume-016.json) |
| Consignment delivery management, 1 | `truck.truck_model` | Choose the local record configuration | `truck_model_master_data`, `truck_model_configuration` | [Open](volume-016.json) |
| Consignment delivery management, 1 | `truck.truck_type` | Choose the local record configuration | `truck_type_master_data`, `truck_type_configuration` | [Open](volume-016.json) |
| Ecuadorian electronic invoicing, 1 | `purchase_withholding_tax_authority_ec_alternate_configuration.establishment` | Choose the local record configuration | `tax_authority_establishment_alternate_configuration`, `tax_authority_establishment_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `purchase_withholding_tax_authority_ec_alternate_configuration.issuing_point` | Choose the local record configuration | `tax_authority_issuing_point_alternate_configuration`, `tax_authority_issuing_point_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `purchase_withholding_tax_authority_ec_alternate_configuration.taxes` | Choose the local record configuration | `purchase_taxes_and_charges_ec_alternate_configuration`, `purchase_taxes_and_charges_ec_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `purchase_withholding_tax_authority_ec_operating_configuration.establishment` | Choose the local record configuration | `tax_authority_establishment_alternate_configuration`, `tax_authority_establishment_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `purchase_withholding_tax_authority_ec_operating_configuration.issuing_point` | Choose the local record configuration | `tax_authority_issuing_point_alternate_configuration`, `tax_authority_issuing_point_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `purchase_withholding_tax_authority_ec_operating_configuration.taxes` | Choose the local record configuration | `purchase_taxes_and_charges_ec_alternate_configuration`, `purchase_taxes_and_charges_ec_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `tax_authority_establishment_alternate_configuration.tax_authority_issuing_point_detail` | Choose the local record configuration | `tax_authority_issuing_point_alternate_configuration`, `tax_authority_issuing_point_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `tax_authority_establishment_link.tax_authority_establishment` | Choose the local record configuration | `tax_authority_establishment_alternate_configuration`, `tax_authority_establishment_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `tax_authority_establishment_operating_configuration.tax_authority_issuing_point_detail` | Choose the local record configuration | `tax_authority_issuing_point_alternate_configuration`, `tax_authority_issuing_point_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `tax_authority_issuing_point_alternate_configuration.tax_authority_establishment_reference` | Choose the local record configuration | `tax_authority_establishment_alternate_configuration`, `tax_authority_establishment_operating_configuration` | [Open](volume-021.json) |
| Ecuadorian electronic invoicing, 1 | `tax_authority_type_test.tax_authority_establishment_reference` | Choose the local record configuration | `tax_authority_establishment_alternate_configuration`, `tax_authority_establishment_operating_configuration` | [Open](volume-021.json) |
| Marketplace inquiry synchronization, 1 | `marketplace_settings.buy_lead_source` | Supply the external record contract | `lead_source` | [Open](volume-027.json) |
| Marketplace inquiry synchronization, 1 | `marketplace_settings.call_lead_source` | Supply the external record contract | `lead_source` | [Open](volume-027.json) |
| Marketplace inquiry synchronization, 1 | `marketplace_settings.direct_lead_source` | Supply the external record contract | `lead_source` | [Open](volume-027.json) |
| Tanzanian maintenance and inspection, 1 | `email_salary_slips_operating_configuration.amended_from` | Choose the local record configuration | `email_salary_slips_alternate_configuration`, `email_salary_slips_operating_configuration` | [Open](volume-045.json) |
| Tanzanian maintenance and inspection, 1 | `export.container_information` | Resolve collection ownership | `container` | [Open](volume-044.json) |
| Tanzanian maintenance and inspection, 1 | `order_track.containers` | Resolve collection ownership | `container` | [Open](volume-047.json) |
| Tanzanian maintenance and inspection, 1 | `order_track.items` | Supply the external record contract | `order_tracking_item` | [Open](volume-047.json) |
| Tanzanian maintenance and inspection, 1 | `order_track.order_progress` | Supply the external record contract | `order_progress` | [Open](volume-047.json) |
| Technology asset management, 1 | `network_jack.destination_room` | Supply the external record contract | `destination_room` | [Open](volume-049.json) |
| Technology asset management, 1 | `network_jack.source_room` | Supply the external record contract | `source_room` | [Open](volume-049.json) |
| Web content and enquiry management, 1 | `services.service_category` | Supply the external record contract | `page_category` | [Open](volume-053.json) |
| Web content and enquiry management, 1 | `theme.theme_features` | Supply the external record contract | `theme_features` | [Open](volume-053.json) |
