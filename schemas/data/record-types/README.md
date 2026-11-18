# Record types

Each file defines one named record and every declared field in order. Field contracts distinguish scalar persistence, owned child collections, protected values, presentation-only fields and virtual calculations. Common record attributes and lifecycle rules apply in addition to the fields declared here.

[Parent index](../README.md)

## Definitions

| Entry | Contents |
|---|---|
| [About us settings](about_us_settings.json) | 11 declared fields; singleton settings. |
| [About us team member](about_us_team_member.json) | 3 declared fields; owned child record. |
| [Access log](access_log.json) | 17 declared fields; independent record. |
| [Account](account.json) | 21 declared fields; independent record. |
| [Account category](account_category.json) | 4 declared fields; independent record. |
| [Account closing balance](account_closing_balance.json) | 16 declared fields; independent record. |
| [Accounting dimension](accounting_dimension.json) | 5 declared fields; independent record. |
| [Accounting dimension detail](accounting_dimension_detail.json) | 8 declared fields; owned child record. |
| [Accounting dimension filter](accounting_dimension_filter.json) | 13 declared fields; independent record. |
| [Accounting period](accounting_period.json) | 9 declared fields; independent record. |
| [Accounts settings](accounts_settings.json) | 113 declared fields; singleton settings. |
| [Activity cost](activity_cost.json) | 10 declared fields; independent record. |
| [Activity log](activity_log.json) | 21 declared fields; independent record. |
| [Activity type](activity_type.json) | 5 declared fields; independent record. |
| [Additional salary](additional_salary.json) | 23 declared fields; independent record. |
| [Address](address.json) | 19 declared fields; independent record. |
| [Address template](address_template.json) | 3 declared fields; independent record. |
| [Advance payment ledger entry](advance_payment_ledger_entry.json) | 11 declared fields; independent record. |
| [Advance taxes and charges](advance_taxes_and_charges.json) | 24 declared fields; owned child record. |
| [Allowed dimension](allowed_dimension.json) | 2 declared fields; owned child record. |
| [Allowed to transact with](allowed_to_transact_with.json) | 1 declared fields; owned child record. |
| [Amended document naming settings](amended_document_naming_settings.json) | 2 declared fields; owned child record. |
| [Applicable on account](applicable_on_account.json) | 2 declared fields; owned child record. |
| [Application programming interface request log](application_programming_interface_request_log.json) | 3 declared fields; independent record. |
| [Appointment](appointment.json) | 18 declared fields; independent record. |
| [Appointment booking settings](appointment_booking_settings.json) | 20 declared fields; singleton settings. |
| [Appointment booking slots](appointment_booking_slots.json) | 3 declared fields; owned child record. |
| [Appointment letter](appointment_letter.json) | 10 declared fields; independent record. |
| [Appointment letter content](appointment_letter_content.json) | 2 declared fields; owned child record. |
| [Appointment letter template](appointment_letter_template.json) | 4 declared fields; independent record. |
| [Appraisal](appraisal.json) | 36 declared fields; independent record. |
| [Appraisal cycle](appraisal_cycle.json) | 24 declared fields; independent record. |
| [Appraisal goal](appraisal_goal.json) | 7 declared fields; owned child record. |
| [Appraisal key result area](appraisal_key_result_area.json) | 5 declared fields; owned child record. |
| [Appraisal template](appraisal_template.json) | 6 declared fields; independent record. |
| [Appraisal template goal](appraisal_template_goal.json) | 2 declared fields; owned child record. |
| [Appraisee](appraisee.json) | 7 declared fields; owned child record. |
| [Arrear](arrear.json) | 16 declared fields; independent record. |
| [Asset](asset.json) | 76 declared fields; independent record. |
| [Asset activity](asset_activity.json) | 7 declared fields; independent record. |
| [Asset capitalization](asset_capitalization.json) | 39 declared fields; independent record. |
| [Asset capitalization asset item](asset_capitalization_asset_item.json) | 15 declared fields; owned child record. |
| [Asset capitalization service item](asset_capitalization_service_item.json) | 13 declared fields; owned child record. |
| [Asset capitalization stock item](asset_capitalization_stock_item.json) | 25 declared fields; owned child record. |
| [Asset category](asset_category.json) | 9 declared fields; independent record. |
| [Asset category account](asset_category_account.json) | 5 declared fields; owned child record. |
| [Asset depreciation schedule](asset_depreciation_schedule.json) | 25 declared fields; independent record. |
| [Asset finance book](asset_finance_book.json) | 16 declared fields; owned child record. |
| [Asset maintenance](asset_maintenance.json) | 13 declared fields; independent record. |
| [Asset maintenance log](asset_maintenance_log.json) | 23 declared fields; independent record. |
| [Asset maintenance task](asset_maintenance_task.json) | 20 declared fields; owned child record. |
| [Asset maintenance team](asset_maintenance_team.json) | 7 declared fields; independent record. |
| [Asset movement](asset_movement.json) | 11 declared fields; independent record. |
| [Asset movement item](asset_movement_item.json) | 8 declared fields; owned child record. |
| [Asset repair](asset_repair.json) | 37 declared fields; independent record. |
| [Asset repair consumed item](asset_repair_consumed_item.json) | 11 declared fields; owned child record. |
| [Asset repair purchase invoice](asset_repair_purchase_invoice.json) | 3 declared fields; owned child record. |
| [Asset shift allocation](asset_shift_allocation.json) | 9 declared fields; independent record. |
| [Asset shift factor](asset_shift_factor.json) | 3 declared fields; independent record. |
| [Asset value adjustment](asset_value_adjustment.json) | 17 declared fields; independent record. |
| [Assignment rule](assignment_rule.json) | 22 declared fields; independent record. |
| [Assignment rule day](assignment_rule_day.json) | 1 declared fields; owned child record. |
| [Assignment rule user](assignment_rule_user.json) | 2 declared fields; owned child record. |
| [Attendance](attendance.json) | 28 declared fields; independent record. |
| [Attendance request](attendance_request.json) | 16 declared fields; independent record. |
| [Audit trail](audit_trail.json) | 13 declared fields; singleton settings. |
| [Authorization control](authorization_control.json) | 0 declared fields; singleton settings. |
| [Authorization rule](authorization_rule.json) | 18 declared fields; independent record. |
| [Auto email report](auto_email_report.json) | 29 declared fields; independent record. |
| [Auto repeat](auto_repeat.json) | 28 declared fields; independent record. |
| [Auto repeat day](auto_repeat_day.json) | 1 declared fields; owned child record. |
| [Auto repeat user](auto_repeat_user.json) | 1 declared fields; owned child record. |
| [Availability of slots](availability_of_slots.json) | 3 declared fields; owned child record. |
| [Background queue job](background_queue_job.json) | 15 declared fields; virtual record. |
| [Background queue worker](background_queue_worker.json) | 16 declared fields; virtual record. |
| [Background task](background_task.json) | 29 declared fields; independent record. |
| [Bank](bank.json) | 13 declared fields; independent record. |
| [Bank account](bank_account.json) | 30 declared fields; independent record. |
| [Bank account balance](bank_account_balance.json) | 4 declared fields; independent record. |
| [Bank account subtype](bank_account_subtype.json) | 1 declared fields; independent record. |
| [Bank account type](bank_account_type.json) | 1 declared fields; independent record. |
| [Bank clearance](bank_clearance.json) | 10 declared fields; singleton settings. |
| [Bank clearance detail](bank_clearance_detail.json) | 9 declared fields; owned child record. |
| [Bank guarantee](bank_guarantee.json) | 30 declared fields; independent record. |
| [Bank reconciliation tool](bank_reconciliation_tool.json) | 16 declared fields; singleton settings. |
| [Bank statement import](bank_statement_import.json) | 27 declared fields; independent record. |
| [Bank statement import log](bank_statement_import_log.json) | 24 declared fields; independent record. |
| [Bank statement import log column map](bank_statement_import_log_column_map.json) | 4 declared fields; owned child record. |
| [Bank transaction](bank_transaction.json) | 37 declared fields; independent record. |
| [Bank transaction mapping](bank_transaction_mapping.json) | 2 declared fields; owned child record. |
| [Bank transaction payments](bank_transaction_payments.json) | 5 declared fields; owned child record. |
| [Bank transaction rule](bank_transaction_rule.json) | 19 declared fields; independent record. |
| [Bank transaction rule accounts](bank_transaction_rule_accounts.json) | 6 declared fields; owned child record. |
| [Bank transaction rule description conditions](bank_transaction_rule_description_conditions.json) | 2 declared fields; owned child record. |
| [Batch](batch.json) | 26 declared fields; independent record. |
| [Bill of materials](bill_of_materials.json) | 95 declared fields; independent record. |
| [Bill of materials creator](bill_of_materials_creator.json) | 40 declared fields; independent record. |
| [Bill of materials creator item](bill_of_materials_creator_item.json) | 34 declared fields; owned child record. |
| [Bill of materials explosion item](bill_of_materials_explosion_item.json) | 20 declared fields; owned child record. |
| [Bill of materials item](bill_of_materials_item.json) | 40 declared fields; owned child record. |
| [Bill of materials operation](bill_of_materials_operation.json) | 39 declared fields; owned child record. |
| [Bill of materials secondary item](bill_of_materials_secondary_item.json) | 23 declared fields; owned child record. |
| [Bill of materials update batch](bill_of_materials_update_batch.json) | 4 declared fields; owned child record. |
| [Bill of materials update log](bill_of_materials_update_log.json) | 11 declared fields; independent record. |
| [Bill of materials update tool](bill_of_materials_update_tool.json) | 6 declared fields; singleton settings. |
| [Bill of materials website item](bill_of_materials_website_item.json) | 5 declared fields; owned child record. |
| [Bill of materials website operation](bill_of_materials_website_operation.json) | 5 declared fields; owned child record. |
| [Bin](bin.json) | 26 declared fields; independent record. |
| [Bisect accounting statements](bisect_accounting_statements.json) | 27 declared fields; singleton settings. |
| [Bisect nodes](bisect_nodes.json) | 9 declared fields; independent record. |
| [Blanket order](blanket_order.json) | 26 declared fields; independent record. |
| [Blanket order item](blanket_order_item.json) | 12 declared fields; owned child record. |
| [Block module](block_module.json) | 1 declared fields; owned child record. |
| [Branch](branch.json) | 1 declared fields; independent record. |
| [Brand](brand.json) | 5 declared fields; independent record. |
| [Budget](budget.json) | 40 declared fields; independent record. |
| [Budget account](budget_account.json) | 2 declared fields; owned child record. |
| [Budget distribution](budget_distribution.json) | 4 declared fields; owned child record. |
| [Bulk salary structure assignment](bulk_salary_structure_assignment.json) | 19 declared fields; singleton settings. |
| [Bulk transaction log](bulk_transaction_log.json) | 7 declared fields; virtual record. |
| [Bulk transaction log detail](bulk_transaction_log_detail.json) | 8 declared fields; independent record. |
| [Bulk update](bulk_update.json) | 5 declared fields; singleton settings. |
| [Buying settings](buying_settings.json) | 47 declared fields; singleton settings. |
| [Calendar view](calendar_view.json) | 6 declared fields; independent record. |
| [Call log](call_log.json) | 21 declared fields; independent record. |
| [Campaign](campaign.json) | 7 declared fields; independent record. |
| [Campaign email schedule](campaign_email_schedule.json) | 2 declared fields; owned child record. |
| [Campaign item](campaign_item.json) | 1 declared fields; owned child record. |
| [Campaign tracking campaign](campaign_tracking_campaign.json) | 2 declared fields; independent record. |
| [Campaign tracking medium](campaign_tracking_medium.json) | 2 declared fields; independent record. |
| [Campaign tracking source](campaign_tracking_source.json) | 2 declared fields; independent record. |
| [Cashier closing](cashier_closing.json) | 12 declared fields; independent record. |
| [Cashier closing payments](cashier_closing_payments.json) | 2 declared fields; owned child record. |
| [Chart of accounts importer](chart_of_accounts_importer.json) | 5 declared fields; singleton settings. |
| [Cheque print template](cheque_print_template.json) | 39 declared fields; independent record. |
| [Client script](client_script.json) | 8 declared fields; independent record. |
| [Closed document](closed_document.json) | 2 declared fields; owned child record. |
| [Code list](code_list.json) | 10 declared fields; independent record. |
| [Color](color.json) | 1 declared fields; independent record. |
| [Comment](comment.json) | 13 declared fields; independent record. |
| [Common code](common_code.json) | 9 declared fields; independent record. |
| [Communication](communication.json) | 46 declared fields; independent record. |
| [Communication link](communication_link.json) | 4 declared fields; owned child record. |
| [Communication medium](communication_medium.json) | 8 declared fields; independent record. |
| [Communication medium timeslot](communication_medium_timeslot.json) | 4 declared fields; owned child record. |
| [Company](company.json) | 145 declared fields; independent record. |
| [Company history](company_history.json) | 2 declared fields; owned child record. |
| [Company restriction](company_restriction.json) | 1 declared fields; owned child record. |
| [Compensatory leave request](compensatory_leave_request.json) | 14 declared fields; independent record. |
| [Competitor](competitor.json) | 2 declared fields; independent record. |
| [Competitor detail](competitor_detail.json) | 1 declared fields; owned child record. |
| [Connected application](connected_application.json) | 19 declared fields; independent record. |
| [Console log](console_log.json) | 3 declared fields; independent record. |
| [Contact](contact.json) | 32 declared fields; independent record. |
| [Contact email](contact_email.json) | 2 declared fields; owned child record. |
| [Contact phone](contact_phone.json) | 3 declared fields; owned child record. |
| [Contact us settings](contact_us_settings.json) | 19 declared fields; singleton settings. |
| [Contract](contract.json) | 32 declared fields; independent record. |
| [Contract fulfilment checklist](contract_fulfilment_checklist.json) | 6 declared fields; owned child record. |
| [Contract template](contract_template.json) | 7 declared fields; independent record. |
| [Contract template fulfilment terms](contract_template_fulfilment_terms.json) | 1 declared fields; owned child record. |
| [Cost center](cost_center.json) | 11 declared fields; independent record. |
| [Cost center allocation](cost_center_allocation.json) | 7 declared fields; independent record. |
| [Cost center allocation percentage](cost_center_allocation_percentage.json) | 2 declared fields; owned child record. |
| [Country](country.json) | 5 declared fields; independent record. |
| [Coupon code](coupon_code.json) | 15 declared fields; independent record. |
| [Currency](currency.json) | 8 declared fields; independent record. |
| [Currency exchange](currency_exchange.json) | 7 declared fields; independent record. |
| [Currency exchange settings](currency_exchange_settings.json) | 13 declared fields; singleton settings. |
| [Currency exchange settings details](currency_exchange_settings_details.json) | 2 declared fields; owned child record. |
| [Currency exchange settings result](currency_exchange_settings_result.json) | 1 declared fields; owned child record. |
| [Custom document markup block](custom_document_markup_block.json) | 12 declared fields; independent record. |
| [Custom field](custom_field.json) | 64 declared fields; independent record. |
| [Custom icon](custom_icon.json) | 2 declared fields; independent record. |
| [Custom record permission](custom_record_permission.json) | 26 declared fields; independent record. |
| [Custom role](custom_role.json) | 6 declared fields; independent record. |
| [Custom sidebar](custom_sidebar.json) | 7 declared fields; independent record. |
| [Custom workspace](custom_workspace.json) | 15 declared fields; independent record. |
| [Customer](customer.json) | 91 declared fields; independent record. |
| [Customer credit limit](customer_credit_limit.json) | 5 declared fields; owned child record. |
| [Customer group](customer_group.json) | 13 declared fields; independent record. |
| [Customer group item](customer_group_item.json) | 1 declared fields; owned child record. |
| [Customer item](customer_item.json) | 1 declared fields; owned child record. |
| [Customer number at supplier](customer_number_at_supplier.json) | 2 declared fields; owned child record. |
| [Customer relationship activity note](customer_relationship_activity_note.json) | 4 declared fields; independent record. |
| [Customer relationship attached note](customer_relationship_attached_note.json) | 3 declared fields; owned child record. |
| [Customer relationship call log](customer_relationship_call_log.json) | 20 declared fields; independent record. |
| [Customer relationship communication status](customer_relationship_communication_status.json) | 1 declared fields; independent record. |
| [Customer relationship contacts](customer_relationship_contacts.json) | 8 declared fields; owned child record. |
| [Customer relationship dashboard](customer_relationship_dashboard.json) | 6 declared fields; independent record. |
| [Customer relationship deal](customer_relationship_deal.json) | 75 declared fields; independent record. |
| [Customer relationship deal status](customer_relationship_deal_status.json) | 6 declared fields; independent record. |
| [Customer relationship dropdown item](customer_relationship_dropdown_item.json) | 9 declared fields; owned child record. |
| [Customer relationship enrichment domain](customer_relationship_enrichment_domain.json) | 1 declared fields; owned child record. |
| [Customer relationship enrichment field mapping](customer_relationship_enrichment_field_mapping.json) | 9 declared fields; independent record. |
| [Customer relationship enrichment link priority](customer_relationship_enrichment_link_priority.json) | 2 declared fields; owned child record. |
| [Customer relationship enrichment rule](customer_relationship_enrichment_rule.json) | 10 declared fields; independent record. |
| [Customer relationship enrichment rule pattern](customer_relationship_enrichment_rule_pattern.json) | 2 declared fields; owned child record. |
| [Customer relationship enrichment run](customer_relationship_enrichment_run.json) | 19 declared fields; independent record. |
| [Customer relationship enrichment settings](customer_relationship_enrichment_settings.json) | 22 declared fields; singleton settings. |
| [Customer relationship enrichment skip pattern](customer_relationship_enrichment_skip_pattern.json) | 1 declared fields; owned child record. |
| [Customer relationship exotel settings](customer_relationship_exotel_settings.json) | 12 declared fields; singleton settings. |
| [Customer relationship fields layout](customer_relationship_fields_layout.json) | 5 declared fields; independent record. |
| [Customer relationship form script](customer_relationship_form_script.json) | 7 declared fields; independent record. |
| [Customer relationship global settings](customer_relationship_global_settings.json) | 5 declared fields; independent record. |
| [Customer relationship holiday](customer_relationship_holiday.json) | 5 declared fields; owned child record. |
| [Customer relationship holiday list](customer_relationship_holiday_list.json) | 11 declared fields; independent record. |
| [Customer relationship industry](customer_relationship_industry.json) | 1 declared fields; independent record. |
| [Customer relationship invitation](customer_relationship_invitation.json) | 8 declared fields; independent record. |
| [Customer relationship lead](customer_relationship_lead.json) | 66 declared fields; independent record. |
| [Customer relationship lead source](customer_relationship_lead_source.json) | 2 declared fields; independent record. |
| [Customer relationship lead status](customer_relationship_lead_status.json) | 5 declared fields; independent record. |
| [Customer relationship lost reason](customer_relationship_lost_reason.json) | 2 declared fields; independent record. |
| [Customer relationship notification](customer_relationship_notification.json) | 16 declared fields; independent record. |
| [Customer relationship organization](customer_relationship_organization.json) | 15 declared fields; independent record. |
| [Customer relationship product](customer_relationship_product.json) | 9 declared fields; independent record. |
| [Customer relationship product sync issue](customer_relationship_product_sync_issue.json) | 5 declared fields; owned child record. |
| [Customer relationship products](customer_relationship_products.json) | 16 declared fields; owned child record. |
| [Customer relationship rolling response time](customer_relationship_rolling_response_time.json) | 3 declared fields; owned child record. |
| [Customer relationship sales hierarchy](customer_relationship_sales_hierarchy.json) | 10 declared fields; independent record. |
| [Customer relationship service day](customer_relationship_service_day.json) | 5 declared fields; owned child record. |
| [Customer relationship service level agreement](customer_relationship_service_level_agreement.json) | 17 declared fields; independent record. |
| [Customer relationship service level priority](customer_relationship_service_level_priority.json) | 6 declared fields; owned child record. |
| [Customer relationship status change log](customer_relationship_status_change_log.json) | 10 declared fields; owned child record. |
| [Customer relationship task](customer_relationship_task.json) | 11 declared fields; independent record. |
| [Customer relationship telephony agent](customer_relationship_telephony_agent.json) | 12 declared fields; independent record. |
| [Customer relationship telephony phone](customer_relationship_telephony_phone.json) | 2 declared fields; owned child record. |
| [Customer relationship territory](customer_relationship_territory.json) | 10 declared fields; independent record. |
| [Customer relationship transaction settings](customer_relationship_transaction_settings.json) | 19 declared fields; singleton settings. |
| [Customer relationship twilio settings](customer_relationship_twilio_settings.json) | 16 declared fields; singleton settings. |
| [Customer relationship view settings](customer_relationship_view_settings.json) | 28 declared fields; independent record. |
| [Customer relationship workspace settings](customer_relationship_workspace_settings.json) | 30 declared fields; singleton settings. |
| [Customize form](customize_form.json) | 62 declared fields; singleton settings. |
| [Customize form field](customize_form_field.json) | 66 declared fields; owned child record. |
| [Customs tariff number](customs_tariff_number.json) | 2 declared fields; independent record. |
| [Daily work summary](daily_work_summary.json) | 3 declared fields; independent record. |
| [Daily work summary group](daily_work_summary_group.json) | 8 declared fields; independent record. |
| [Daily work summary group user](daily_work_summary_group_user.json) | 2 declared fields; owned child record. |
| [Dashboard](dashboard.json) | 7 declared fields; independent record. |
| [Dashboard chart](dashboard_chart.json) | 39 declared fields; independent record. |
| [Dashboard chart field](dashboard_chart_field.json) | 2 declared fields; owned child record. |
| [Dashboard chart link](dashboard_chart_link.json) | 2 declared fields; owned child record. |
| [Dashboard chart source](dashboard_chart_source.json) | 3 declared fields; independent record. |
| [Dashboard settings](dashboard_settings.json) | 2 declared fields; independent record. |
| [Data export](data_export.json) | 7 declared fields; singleton settings. |
| [Data import](data_import.json) | 30 declared fields; independent record. |
| [Data import log](data_import_log.json) | 8 declared fields; independent record. |
| [Data import skipped row](data_import_skipped_row.json) | 2 declared fields; owned child record. |
| [Data import value mapping](data_import_value_mapping.json) | 11 declared fields; owned child record. |
| [Default value](default_value.json) | 2 declared fields; owned child record. |
| [O authentication authorization code](delegated_authorization_authorization_code.json) | 10 declared fields; independent record. |
| [O authentication bearer token](delegated_authorization_bearer_token.json) | 8 declared fields; independent record. |
| [O authentication client](delegated_authorization_client.json) | 27 declared fields; independent record. |
| [O authentication client role](delegated_authorization_client_role.json) | 1 declared fields; owned child record. |
| [O authentication provider settings](delegated_authorization_provider_settings.json) | 1 declared fields; singleton settings. |
| [O authentication scope](delegated_authorization_scope.json) | 1 declared fields; owned child record. |
| [O authentication settings](delegated_authorization_settings.json) | 19 declared fields; singleton settings. |
| [Deleted document](deleted_document.json) | 7 declared fields; independent record. |
| [Delivery note](delivery_note.json) | 169 declared fields; independent record. |
| [Delivery note item](delivery_note_item.json) | 112 declared fields; owned child record. |
| [Delivery schedule item](delivery_schedule_item.json) | 13 declared fields; independent record. |
| [Delivery settings](delivery_settings.json) | 6 declared fields; singleton settings. |
| [Delivery stop](delivery_stop.json) | 24 declared fields; owned child record. |
| [Delivery trip](delivery_trip.json) | 23 declared fields; independent record. |
| [Department](department.json) | 9 declared fields; independent record. |
| [Department approver](department_approver.json) | 1 declared fields; owned child record. |
| [Dependent task](dependent_task.json) | 1 declared fields; owned child record. |
| [Depreciation schedule](depreciation_schedule.json) | 7 declared fields; owned child record. |
| [Designation](designation.json) | 2 declared fields; independent record. |
| [Designation skill](designation_skill.json) | 1 declared fields; owned child record. |
| [Desktop icon](desktop_icon.json) | 19 declared fields; independent record. |
| [Desktop layout](desktop_layout.json) | 2 declared fields; independent record. |
| [Desktop settings](desktop_settings.json) | 2 declared fields; singleton settings. |
| [Discounted invoice](discounted_invoice.json) | 6 declared fields; owned child record. |
| [Discussion reply](discussion_reply.json) | 2 declared fields; independent record. |
| [Discussion topic](discussion_topic.json) | 3 declared fields; independent record. |
| [Dock](dock.json) | 6 declared fields; independent record. |
| [Dock item](dock_item.json) | 7 declared fields; owned child record. |
| [Document follow](document_follow.json) | 3 declared fields; independent record. |
| [Document naming rule](document_naming_rule.json) | 10 declared fields; independent record. |
| [Document naming rule condition](document_naming_rule_condition.json) | 3 declared fields; owned child record. |
| [Document naming settings](document_naming_settings.json) | 18 declared fields; singleton settings. |
| [Document share key](document_share_key.json) | 4 declared fields; independent record. |
| [Document template](document_template.json) | 5 declared fields; independent record. |
| [Domain](domain.json) | 1 declared fields; independent record. |
| [Domain settings](domain_settings.json) | 3 declared fields; singleton settings. |
| [Downtime entry](downtime_entry.json) | 11 declared fields; independent record. |
| [Driver](driver.json) | 17 declared fields; independent record. |
| [Driving license category](driving_license_category.json) | 4 declared fields; owned child record. |
| [Duck database sync](duck_database_sync.json) | 6 declared fields; independent record. |
| [Duck database sync item](duck_database_sync_item.json) | 3 declared fields; owned child record. |
| [Dunning](dunning.json) | 54 declared fields; independent record. |
| [Dunning letter text](dunning_letter_text.json) | 7 declared fields; owned child record. |
| [Dunning type](dunning_type.json) | 14 declared fields; independent record. |
| [Dynamic link](dynamic_link.json) | 3 declared fields; owned child record. |
| [Earned leave schedule](earned_leave_schedule.json) | 10 declared fields; owned child record. |
| [Email account](email_account.json) | 87 declared fields; independent record. |
| [Email campaign](email_campaign.json) | 8 declared fields; independent record. |
| [Email digest](email_digest.json) | 43 declared fields; independent record. |
| [Email digest recipient](email_digest_recipient.json) | 1 declared fields; owned child record. |
| [Email domain](email_domain.json) | 20 declared fields; independent record. |
| [Email flag queue](email_flag_queue.json) | 5 declared fields; independent record. |
| [Email group](email_group.json) | 7 declared fields; independent record. |
| [Email group member](email_group_member.json) | 3 declared fields; independent record. |
| [Email queue](email_queue.json) | 21 declared fields; independent record. |
| [Email queue recipient](email_queue_recipient.json) | 3 declared fields; owned child record. |
| [Email rule](email_rule.json) | 2 declared fields; independent record. |
| [Email template](email_template.json) | 7 declared fields; independent record. |
| [Email unsubscribe](email_unsubscribe.json) | 4 declared fields; independent record. |
| [Employee](employee.json) | 109 declared fields; independent record. |
| [Employee advance](employee_advance.json) | 29 declared fields; independent record. |
| [Employee attendance tool](employee_attendance_tool.json) | 25 declared fields; virtual record. |
| [Employee benefit application](employee_benefit_application.json) | 19 declared fields; independent record. |
| [Employee benefit application detail](employee_benefit_application_detail.json) | 3 declared fields; owned child record. |
| [Employee benefit claim](employee_benefit_claim.json) | 16 declared fields; independent record. |
| [Employee benefit detail](employee_benefit_detail.json) | 3 declared fields; owned child record. |
| [Employee benefit ledger](employee_benefit_ledger.json) | 17 declared fields; independent record. |
| [Employee boarding activity](employee_boarding_activity.json) | 11 declared fields; owned child record. |
| [Employee checkin](employee_checkin.json) | 24 declared fields; independent record. |
| [Employee cost center](employee_cost_center.json) | 2 declared fields; owned child record. |
| [Employee education](employee_education.json) | 6 declared fields; owned child record. |
| [Employee external work history](employee_external_work_history.json) | 6 declared fields; owned child record. |
| [Employee feedback criteria](employee_feedback_criteria.json) | 1 declared fields; independent record. |
| [Employee feedback rating](employee_feedback_rating.json) | 3 declared fields; owned child record. |
| [Employee grade](employee_grade.json) | 3 declared fields; independent record. |
| [Employee grievance](employee_grievance.json) | 26 declared fields; independent record. |
| [Employee group](employee_group.json) | 3 declared fields; independent record. |
| [Employee group table](employee_group_table.json) | 3 declared fields; owned child record. |
| [Employee health insurance](employee_health_insurance.json) | 1 declared fields; independent record. |
| [Employee incentive](employee_incentive.json) | 13 declared fields; independent record. |
| [Employee internal work history](employee_internal_work_history.json) | 5 declared fields; owned child record. |
| [Employee onboarding](employee_onboarding.json) | 21 declared fields; independent record. |
| [Employee onboarding template](employee_onboarding_template.json) | 8 declared fields; independent record. |
| [Employee other income](employee_other_income.json) | 11 declared fields; independent record. |
| [Employee performance feedback](employee_performance_feedback.json) | 21 declared fields; independent record. |
| [Employee promotion](employee_promotion.json) | 14 declared fields; independent record. |
| [Employee property history](employee_property_history.json) | 4 declared fields; owned child record. |
| [Employee referral](employee_referral.json) | 26 declared fields; independent record. |
| [Employee separation](employee_separation.json) | 18 declared fields; independent record. |
| [Employee separation template](employee_separation_template.json) | 8 declared fields; independent record. |
| [Employee skill](employee_skill.json) | 3 declared fields; owned child record. |
| [Employee skill map](employee_skill_map.json) | 8 declared fields; independent record. |
| [Employee tax exemption category](employee_tax_exemption_category.json) | 3 declared fields; independent record. |
| [Employee tax exemption declaration](employee_tax_exemption_declaration.json) | 14 declared fields; independent record. |
| [Employee tax exemption declaration category](employee_tax_exemption_declaration_category.json) | 4 declared fields; owned child record. |
| [Employee tax exemption proof submission](employee_tax_exemption_proof_submission.json) | 18 declared fields; independent record. |
| [Employee tax exemption proof submission detail](employee_tax_exemption_proof_submission_detail.json) | 6 declared fields; owned child record. |
| [Employee tax exemption subordinate category](employee_tax_exemption_subordinate_category.json) | 4 declared fields; independent record. |
| [Employee training](employee_training.json) | 2 declared fields; owned child record. |
| [Employee transfer](employee_transfer.json) | 13 declared fields; independent record. |
| [Employment type](employment_type.json) | 1 declared fields; independent record. |
| [Enterprise resource planning next customer relationship settings](enterprise_resource_planning_next_customer_relationship_settings.json) | 15 declared fields; singleton settings. |
| [Error log](error_log.json) | 12 declared fields; independent record. |
| [Event](event.json) | 48 declared fields; independent record. |
| [Event notifications](event_notifications.json) | 4 declared fields; owned child record. |
| [Event participants](event_participants.json) | 4 declared fields; owned child record. |
| [Exchange rate revaluation](exchange_rate_revaluation.json) | 13 declared fields; independent record. |
| [Exchange rate revaluation account](exchange_rate_revaluation_account.json) | 20 declared fields; owned child record. |
| [Exit interview](exit_interview.json) | 26 declared fields; independent record. |
| [Expected skill set](expected_skill_set.json) | 2 declared fields; owned child record. |
| [Expense claim](expense_claim.json) | 59 declared fields; independent record. |
| [Expense claim account](expense_claim_account.json) | 2 declared fields; owned child record. |
| [Expense claim advance](expense_claim_advance.json) | 16 declared fields; owned child record. |
| [Expense claim detail](expense_claim_detail.json) | 16 declared fields; owned child record. |
| [Expense claim type](expense_claim_type.json) | 4 declared fields; independent record. |
| [Expense taxes and charges](expense_taxes_and_charges.json) | 14 declared fields; owned child record. |
| [Facebook lead form](facebook_lead_form.json) | 6 declared fields; independent record. |
| [Facebook lead form question](facebook_lead_form_question.json) | 6 declared fields; owned child record. |
| [Facebook page](facebook_page.json) | 6 declared fields; independent record. |
| [Failed lead sync log](failed_lead_sync_log.json) | 7 declared fields; independent record. |
| [File](file.json) | 24 declared fields; independent record. |
| [Finance book](finance_book.json) | 1 declared fields; independent record. |
| [Financial report row](financial_report_row.json) | 21 declared fields; owned child record. |
| [Financial report template](financial_report_template.json) | 7 declared fields; independent record. |
| [Fiscal year](fiscal_year.json) | 7 declared fields; independent record. |
| [Fiscal year company](fiscal_year_company.json) | 1 declared fields; owned child record. |
| [Form tour](form_tour.json) | 20 declared fields; independent record. |
| [Form tour step](form_tour_step.json) | 25 declared fields; owned child record. |
| [Foundation customer relationship allowed user](foundation_customer_relationship_allowed_user.json) | 1 declared fields; owned child record. |
| [Full and final asset](full_and_final_asset.json) | 11 declared fields; owned child record. |
| [Full and final outstanding statement](full_and_final_outstanding_statement.json) | 9 declared fields; owned child record. |
| [Full and final statement](full_and_final_statement.json) | 24 declared fields; independent record. |
| [Gender](gender.json) | 1 declared fields; independent record. |
| [General ledger entry](general_ledger_entry.json) | 47 declared fields; independent record. |
| [Geolocation settings](geolocation_settings.json) | 4 declared fields; singleton settings. |
| [Global defaults](global_defaults.json) | 13 declared fields; singleton settings. |
| [Global search record type](global_search_record_type.json) | 2 declared fields; owned child record. |
| [Global search settings](global_search_settings.json) | 1 declared fields; singleton settings. |
| [Goal](goal.json) | 23 declared fields; independent record. |
| [Google calendar](google_calendar.json) | 15 declared fields; independent record. |
| [Google contacts](google_contacts.json) | 13 declared fields; independent record. |
| [Google settings](google_settings.json) | 9 declared fields; singleton settings. |
| [Gratuity](gratuity.json) | 23 declared fields; independent record. |
| [Gratuity applicable component](gratuity_applicable_component.json) | 1 declared fields; owned child record. |
| [Gratuity rule](gratuity_rule.json) | 12 declared fields; independent record. |
| [Gratuity rule slab](gratuity_rule_slab.json) | 3 declared fields; owned child record. |
| [Grievance type](grievance_type.json) | 2 declared fields; independent record. |
| [Has domain](has_domain.json) | 1 declared fields; owned child record. |
| [Has role](has_role.json) | 1 declared fields; owned child record. |
| [Help article](help_article.json) | 14 declared fields; independent record. |
| [Help category](help_category.json) | 5 declared fields; independent record. |
| [Holiday](holiday.json) | 6 declared fields; owned child record. |
| [Holiday list](holiday_list.json) | 19 declared fields; independent record. |
| [Holiday list assignment](holiday_list_assignment.json) | 12 declared fields; independent record. |
| [Human resources settings](human_resources_settings.json) | 54 declared fields; singleton settings. |
| [Human resources telemetry milestone](human_resources_telemetry_milestone.json) | 1 declared fields; independent record. |
| [Identification document type](identification_document_type.json) | 1 declared fields; independent record. |
| [Import supplier invoice](import_supplier_invoice.json) | 11 declared fields; independent record. |
| [Income tax slab](income_tax_slab.json) | 16 declared fields; independent record. |
| [Income tax slab other charges](income_tax_slab_other_charges.json) | 7 declared fields; owned child record. |
| [Incoming call handling schedule](incoming_call_handling_schedule.json) | 4 declared fields; owned child record. |
| [Incoming call settings](incoming_call_settings.json) | 7 declared fields; independent record. |
| [Incoterm](incoterm.json) | 3 declared fields; independent record. |
| [Industry type](industry_type.json) | 1 declared fields; independent record. |
| [Installation note](installation_note.json) | 23 declared fields; independent record. |
| [Installation note item](installation_note_item.json) | 8 declared fields; owned child record. |
| [Installed application](installed_application.json) | 9 declared fields; owned child record. |
| [Installed applications](installed_applications.json) | 1 declared fields; singleton settings. |
| [Integration request](integration_request.json) | 18 declared fields; independent record. |
| [Interest](interest.json) | 1 declared fields; independent record. |
| [Internet message access protocol folder](internet_message_access_protocol_folder.json) | 4 declared fields; owned child record. |
| [Interview](interview.json) | 23 declared fields; independent record. |
| [Interview detail](interview_detail.json) | 1 declared fields; owned child record. |
| [Interview feedback](interview_feedback.json) | 13 declared fields; independent record. |
| [Interview type](interview_type.json) | 9 declared fields; independent record. |
| [Interviewer](interviewer.json) | 1 declared fields; owned child record. |
| [Inventory dimension](inventory_dimension.json) | 24 declared fields; independent record. |
| [Invoice discounting](invoice_discounting.json) | 22 declared fields; independent record. |
| [Issue](issue.json) | 46 declared fields; independent record. |
| [Issue priority](issue_priority.json) | 1 declared fields; independent record. |
| [Issue type](issue_type.json) | 1 declared fields; independent record. |
| [Item](item.json) | 135 declared fields; independent record. |
| [Item alternative](item_alternative.json) | 6 declared fields; independent record. |
| [Item attribute](item_attribute.json) | 11 declared fields; independent record. |
| [Item attribute value](item_attribute_value.json) | 2 declared fields; owned child record. |
| [Item barcode](item_barcode.json) | 3 declared fields; owned child record. |
| [Item customer detail](item_customer_detail.json) | 3 declared fields; owned child record. |
| [Item default](item_default.json) | 54 declared fields; owned child record. |
| [Item group](item_group.json) | 13 declared fields; independent record. |
| [Item lead time](item_lead_time.json) | 27 declared fields; independent record. |
| [Item lead time supplier](item_lead_time_supplier.json) | 4 declared fields; owned child record. |
| [Item manufacturer](item_manufacturer.json) | 7 declared fields; independent record. |
| [Item price](item_price.json) | 27 declared fields; independent record. |
| [Item quality inspection parameter](item_quality_inspection_parameter.json) | 9 declared fields; owned child record. |
| [Item reorder](item_reorder.json) | 5 declared fields; owned child record. |
| [Item standard cost](item_standard_cost.json) | 9 declared fields; independent record. |
| [Item supplier](item_supplier.json) | 3 declared fields; owned child record. |
| [Item tax](item_tax.json) | 5 declared fields; owned child record. |
| [Item tax template](item_tax_template.json) | 6 declared fields; independent record. |
| [Item tax template detail](item_tax_template_detail.json) | 3 declared fields; owned child record. |
| [Item variant](item_variant.json) | 2 declared fields; owned child record. |
| [Item variant attribute](item_variant_attribute.json) | 11 declared fields; owned child record. |
| [Item variant settings](item_variant_settings.json) | 6 declared fields; singleton settings. |
| [Item website specification](item_website_specification.json) | 2 declared fields; owned child record. |
| [Item wise tax detail](item_wise_tax_detail.json) | 5 declared fields; owned child record. |
| [Job applicant](job_applicant.json) | 28 declared fields; independent record. |
| [Job applicant source](job_applicant_source.json) | 2 declared fields; independent record. |
| [Job card](job_card.json) | 97 declared fields; independent record. |
| [Job card item](job_card_item.json) | 14 declared fields; owned child record. |
| [Job card operation](job_card_operation.json) | 4 declared fields; owned child record. |
| [Job card scheduled time](job_card_scheduled_time.json) | 3 declared fields; owned child record. |
| [Job card secondary item](job_card_secondary_item.json) | 10 declared fields; owned child record. |
| [Job card time log](job_card_time_log.json) | 7 declared fields; owned child record. |
| [Job offer](job_offer.json) | 19 declared fields; independent record. |
| [Job offer term](job_offer_term.json) | 3 declared fields; owned child record. |
| [Job offer term template](job_offer_term_template.json) | 2 declared fields; independent record. |
| [Job opening](job_opening.json) | 36 declared fields; independent record. |
| [Job opening template](job_opening_template.json) | 15 declared fields; independent record. |
| [Job requisition](job_requisition.json) | 25 declared fields; independent record. |
| [Journal entry](journal_entry.json) | 74 declared fields; independent record. |
| [Journal entry account](journal_entry_account.json) | 32 declared fields; owned child record. |
| [Journal entry template](journal_entry_template.json) | 10 declared fields; independent record. |
| [Journal entry template account](journal_entry_template_account.json) | 7 declared fields; owned child record. |
| [Kanban board](kanban_board.json) | 10 declared fields; independent record. |
| [Kanban board column](kanban_board_column.json) | 4 declared fields; owned child record. |
| [Key result area](key_result_area.json) | 2 declared fields; independent record. |
| [Landed cost item](landed_cost_item.json) | 15 declared fields; owned child record. |
| [Landed cost purchase receipt](landed_cost_purchase_receipt.json) | 6 declared fields; owned child record. |
| [Landed cost taxes and charges](landed_cost_taxes_and_charges.json) | 16 declared fields; owned child record. |
| [Landed cost vendor invoice](landed_cost_vendor_invoice.json) | 2 declared fields; owned child record. |
| [Landed cost voucher](landed_cost_voucher.json) | 20 declared fields; independent record. |
| [Language](language.json) | 10 declared fields; independent record. |
| [Lead](lead.json) | 71 declared fields; independent record. |
| [Lead sync source](lead_sync_source.json) | 10 declared fields; independent record. |
| [Leave adjustment](leave_adjustment.json) | 20 declared fields; independent record. |
| [Leave allocation](leave_allocation.json) | 28 declared fields; independent record. |
| [Leave application](leave_application.json) | 29 declared fields; independent record. |
| [Leave block list](leave_block_list.json) | 10 declared fields; independent record. |
| [Leave block list allow](leave_block_list_allow.json) | 1 declared fields; owned child record. |
| [Leave block list date](leave_block_list_date.json) | 2 declared fields; owned child record. |
| [Leave control panel](leave_control_panel.json) | 23 declared fields; singleton settings. |
| [Leave encashment](leave_encashment.json) | 31 declared fields; independent record. |
| [Leave ledger entry](leave_ledger_entry.json) | 15 declared fields; independent record. |
| [Leave period](leave_period.json) | 6 declared fields; independent record. |
| [Leave policy](leave_policy.json) | 5 declared fields; independent record. |
| [Leave policy assignment](leave_policy_assignment.json) | 12 declared fields; independent record. |
| [Leave policy detail](leave_policy_detail.json) | 2 declared fields; owned child record. |
| [Leave type](leave_type.json) | 33 declared fields; independent record. |
| [Ledger health](ledger_health.json) | 5 declared fields; independent record. |
| [Ledger health monitor](ledger_health_monitor.json) | 7 declared fields; singleton settings. |
| [Ledger health monitor company](ledger_health_monitor_company.json) | 1 declared fields; owned child record. |
| [Ledger merge](ledger_merge.json) | 10 declared fields; independent record. |
| [Ledger merge accounts](ledger_merge_accounts.json) | 3 declared fields; owned child record. |
| [Letter head](letter_head.json) | 30 declared fields; independent record. |
| [Lightweight directory access protocol group mapping](lightweight_directory_access_protocol_group_mapping.json) | 2 declared fields; owned child record. |
| [Lightweight directory access protocol settings](lightweight_directory_access_protocol_settings.json) | 43 declared fields; singleton settings. |
| [Linked location](linked_location.json) | 1 declared fields; owned child record. |
| [List filter](list_filter.json) | 11 declared fields; independent record. |
| [List view settings](list_view_settings.json) | 12 declared fields; independent record. |
| [Location](location.json) | 17 declared fields; independent record. |
| [Log setting user](log_setting_user.json) | 1 declared fields; owned child record. |
| [Log settings](log_settings.json) | 1 declared fields; singleton settings. |
| [Logs to clear](logs_to_clear.json) | 2 declared fields; owned child record. |
| [Lost reason detail](lost_reason_detail.json) | 1 declared fields; owned child record. |
| [Lower deduction certificate](lower_deduction_certificate.json) | 18 declared fields; independent record. |
| [Loyalty point entry](loyalty_point_entry.json) | 12 declared fields; independent record. |
| [Loyalty point entry redemption](loyalty_point_entry_redemption.json) | 3 declared fields; owned child record. |
| [Loyalty program](loyalty_program.json) | 22 declared fields; independent record. |
| [Loyalty program collection](loyalty_program_collection.json) | 4 declared fields; owned child record. |
| [Maintenance schedule](maintenance_schedule.json) | 24 declared fields; independent record. |
| [Maintenance schedule detail](maintenance_schedule_detail.json) | 12 declared fields; owned child record. |
| [Maintenance schedule item](maintenance_schedule_item.json) | 16 declared fields; owned child record. |
| [Maintenance team member](maintenance_team_member.json) | 3 declared fields; owned child record. |
| [Maintenance visit](maintenance_visit.json) | 32 declared fields; independent record. |
| [Maintenance visit purpose](maintenance_visit_purpose.json) | 12 declared fields; owned child record. |
| [Manufacturer](manufacturer.json) | 11 declared fields; independent record. |
| [Manufacturing settings](manufacturing_settings.json) | 35 declared fields; singleton settings. |
| [Map reduce job](map_reduce_job.json) | 12 declared fields; independent record. |
| [Map reduce task](map_reduce_task.json) | 8 declared fields; independent record. |
| [Market segment](market_segment.json) | 1 declared fields; independent record. |
| [Master production schedule](master_production_schedule.json) | 27 declared fields; independent record. |
| [Master production schedule item](master_production_schedule_item.json) | 9 declared fields; owned child record. |
| [Material request](material_request.json) | 40 declared fields; independent record. |
| [Material request item](material_request_item.json) | 61 declared fields; owned child record. |
| [Material request plan item](material_request_plan_item.json) | 33 declared fields; owned child record. |
| [Milestone](milestone.json) | 5 declared fields; independent record. |
| [Milestone tracker](milestone_tracker.json) | 3 declared fields; independent record. |
| [Mode of payment](mode_of_payment.json) | 4 declared fields; independent record. |
| [Mode of payment account](mode_of_payment_account.json) | 2 declared fields; owned child record. |
| [Module def](module_def.json) | 9 declared fields; independent record. |
| [Module onboarding](module_onboarding.json) | 7 declared fields; independent record. |
| [Module profile](module_profile.json) | 3 declared fields; independent record. |
| [Monthly distribution](monthly_distribution.json) | 3 declared fields; independent record. |
| [Monthly distribution percentage](monthly_distribution_percentage.json) | 2 declared fields; owned child record. |
| [Navbar item](navbar_item.json) | 9 declared fields; owned child record. |
| [Navbar settings](navbar_settings.json) | 9 declared fields; singleton settings. |
| [Network printer settings](network_printer_settings.json) | 4 declared fields; independent record. |
| [New record type 1](new_record_type_1.json) | 2 declared fields; singleton settings. |
| [New record type 2](new_record_type_2.json) | 2 declared fields; independent record. |
| [Non conformance](non_conformance.json) | 10 declared fields; independent record. |
| [Note](note.json) | 8 declared fields; independent record. |
| [Note seen by](note_seen_by.json) | 1 declared fields; owned child record. |
| [Notification](notification.json) | 47 declared fields; independent record. |
| [Notification log](notification_log.json) | 25 declared fields; independent record. |
| [Notification recipient](notification_recipient.json) | 5 declared fields; owned child record. |
| [Notification settings](notification_settings.json) | 12 declared fields; independent record. |
| [Notification subscribed document](notification_subscribed_document.json) | 1 declared fields; owned child record. |
| [Notification type](notification_type.json) | 2 declared fields; independent record. |
| [Notification type preference](notification_type_preference.json) | 1 declared fields; owned child record. |
| [Number card](number_card.json) | 29 declared fields; independent record. |
| [Number card link](number_card_link.json) | 1 declared fields; owned child record. |
| [Offer term](offer_term.json) | 1 declared fields; independent record. |
| [Onboarding permission](onboarding_permission.json) | 1 declared fields; owned child record. |
| [Onboarding step](onboarding_step.json) | 29 declared fields; independent record. |
| [Onboarding step map](onboarding_step_map.json) | 1 declared fields; owned child record. |
| [Opening invoice creation tool](opening_invoice_creation_tool.json) | 11 declared fields; singleton settings. |
| [Opening invoice creation tool item](opening_invoice_creation_tool_item.json) | 18 declared fields; owned child record. |
| [Operation](operation.json) | 14 declared fields; independent record. |
| [Opportunity](opportunity.json) | 83 declared fields; independent record. |
| [Opportunity item](opportunity_item.json) | 18 declared fields; owned child record. |
| [Opportunity lost reason](opportunity_lost_reason.json) | 1 declared fields; independent record. |
| [Opportunity lost reason detail](opportunity_lost_reason_detail.json) | 1 declared fields; owned child record. |
| [Opportunity type](opportunity_type.json) | 1 declared fields; independent record. |
| [Overdue payment](overdue_payment.json) | 18 declared fields; owned child record. |
| [Overtime details](overtime_details.json) | 7 declared fields; owned child record. |
| [Overtime salary component](overtime_salary_component.json) | 1 declared fields; owned child record. |
| [Overtime slip](overtime_slip.json) | 18 declared fields; independent record. |
| [Overtime type](overtime_type.json) | 16 declared fields; independent record. |
| [Package](package.json) | 4 declared fields; independent record. |
| [Package import](package_import.json) | 4 declared fields; independent record. |
| [Package release](package_release.json) | 9 declared fields; independent record. |
| [Packed item](packed_item.json) | 40 declared fields; owned child record. |
| [Packing slip](packing_slip.json) | 22 declared fields; independent record. |
| [Packing slip item](packing_slip_item.json) | 15 declared fields; owned child record. |
| [Page](page.json) | 12 declared fields; independent record. |
| [Party account](party_account.json) | 3 declared fields; owned child record. |
| [Party link](party_link.json) | 5 declared fields; independent record. |
| [Party specific item](party_specific_item.json) | 5 declared fields; independent record. |
| [Party type](party_type.json) | 2 declared fields; independent record. |
| [Patch log](patch_log.json) | 3 declared fields; independent record. |
| [Pause service level agreement on status](pause_service_level_agreement_on_status.json) | 1 declared fields; owned child record. |
| [Payment entry](payment_entry.json) | 93 declared fields; independent record. |
| [Payment entry deduction](payment_entry_deduction.json) | 7 declared fields; owned child record. |
| [Payment entry reference](payment_entry_reference.json) | 20 declared fields; owned child record. |
| [Payment gateway account](payment_gateway_account.json) | 10 declared fields; independent record. |
| [Payment ledger entry](payment_ledger_entry.json) | 20 declared fields; independent record. |
| [Payment order](payment_order.json) | 12 declared fields; independent record. |
| [Payment order reference](payment_order_reference.json) | 12 declared fields; owned child record. |
| [Payment reconciliation](payment_reconciliation.json) | 32 declared fields; virtual record. |
| [Payment reconciliation allocation](payment_reconciliation_allocation.json) | 23 declared fields; virtual record. |
| [Payment reconciliation invoice](payment_reconciliation_invoice.json) | 8 declared fields; virtual record. |
| [Payment reconciliation payment](payment_reconciliation_payment.json) | 13 declared fields; virtual record. |
| [Payment reference](payment_reference.json) | 10 declared fields; owned child record. |
| [Payment request](payment_request.json) | 60 declared fields; independent record. |
| [Payment schedule](payment_schedule.json) | 27 declared fields; owned child record. |
| [Payment term](payment_term.json) | 15 declared fields; independent record. |
| [Payment terms template](payment_terms_template.json) | 3 declared fields; independent record. |
| [Payment terms template detail](payment_terms_template_detail.json) | 16 declared fields; owned child record. |
| [Payroll correction](payroll_correction.json) | 21 declared fields; independent record. |
| [Payroll correction child](payroll_correction_child.json) | 2 declared fields; owned child record. |
| [Payroll employee detail](payroll_employee_detail.json) | 6 declared fields; owned child record. |
| [Payroll entry](payroll_entry.json) | 45 declared fields; independent record. |
| [Payroll period](payroll_period.json) | 6 declared fields; independent record. |
| [Payroll period date](payroll_period_date.json) | 2 declared fields; owned child record. |
| [Payroll settings](payroll_settings.json) | 26 declared fields; singleton settings. |
| [Pegged currencies](pegged_currencies.json) | 2 declared fields; singleton settings. |
| [Pegged currency details](pegged_currency_details.json) | 3 declared fields; owned child record. |
| [Period closing voucher](period_closing_voucher.json) | 11 declared fields; independent record. |
| [Permission inspector](permission_inspector.json) | 9 declared fields; virtual record. |
| [Permission log](permission_log.json) | 15 declared fields; independent record. |
| [Permission type](permission_type.json) | 2 declared fields; independent record. |
| [Personal data deletion request](personal_data_deletion_request.json) | 4 declared fields; independent record. |
| [Personal data deletion step](personal_data_deletion_step.json) | 5 declared fields; owned child record. |
| [Personal data download request](personal_data_download_request.json) | 3 declared fields; independent record. |
| [Pick list](pick_list.json) | 35 declared fields; independent record. |
| [Pick list item](pick_list_item.json) | 39 declared fields; owned child record. |
| [Plaid settings](plaid_settings.json) | 9 declared fields; singleton settings. |
| [Plant floor](plant_floor.json) | 9 declared fields; independent record. |
| [Point of sale closing entry](point_of_sale_closing_entry.json) | 31 declared fields; independent record. |
| [Point of sale closing entry detail](point_of_sale_closing_entry_detail.json) | 5 declared fields; owned child record. |
| [Point of sale closing entry taxes](point_of_sale_closing_entry_taxes.json) | 2 declared fields; owned child record. |
| [Point of sale customer group](point_of_sale_customer_group.json) | 1 declared fields; owned child record. |
| [Point of sale field](point_of_sale_field.json) | 8 declared fields; owned child record. |
| [Point of sale invoice](point_of_sale_invoice.json) | 185 declared fields; independent record. |
| [Point of sale invoice item](point_of_sale_invoice_item.json) | 102 declared fields; owned child record. |
| [Point of sale invoice merge log](point_of_sale_invoice_merge_log.json) | 15 declared fields; independent record. |
| [Point of sale invoice reference](point_of_sale_invoice_reference.json) | 7 declared fields; owned child record. |
| [Point of sale item group](point_of_sale_item_group.json) | 1 declared fields; owned child record. |
| [Point of sale opening entry](point_of_sale_opening_entry.json) | 16 declared fields; independent record. |
| [Point of sale opening entry detail](point_of_sale_opening_entry_detail.json) | 2 declared fields; owned child record. |
| [Point of sale payment method](point_of_sale_payment_method.json) | 3 declared fields; owned child record. |
| [Point of sale profile](point_of_sale_profile.json) | 78 declared fields; independent record. |
| [Point of sale profile user](point_of_sale_profile_user.json) | 2 declared fields; owned child record. |
| [Point of sale search fields](point_of_sale_search_fields.json) | 2 declared fields; owned child record. |
| [Point of sale settings](point_of_sale_settings.json) | 6 declared fields; singleton settings. |
| [Portal menu item](portal_menu_item.json) | 6 declared fields; owned child record. |
| [Portal settings](portal_settings.json) | 7 declared fields; singleton settings. |
| [Portal user](portal_user.json) | 1 declared fields; owned child record. |
| [Prepared report](prepared_report.json) | 13 declared fields; independent record. |
| [Price list](price_list.json) | 9 declared fields; independent record. |
| [Price list country](price_list_country.json) | 1 declared fields; owned child record. |
| [Pricing rule](pricing_rule.json) | 88 declared fields; independent record. |
| [Pricing rule brand](pricing_rule_brand.json) | 2 declared fields; owned child record. |
| [Pricing rule detail](pricing_rule_detail.json) | 6 declared fields; owned child record. |
| [Pricing rule item code](pricing_rule_item_code.json) | 2 declared fields; owned child record. |
| [Pricing rule item group](pricing_rule_item_group.json) | 2 declared fields; owned child record. |
| [Print format](print_format.json) | 41 declared fields; independent record. |
| [Print format field template](print_format_field_template.json) | 8 declared fields; independent record. |
| [Print format snippet](print_format_snippet.json) | 7 declared fields; independent record. |
| [Print heading](print_heading.json) | 2 declared fields; independent record. |
| [Print settings](print_settings.json) | 25 declared fields; singleton settings. |
| [Print style](print_style.json) | 5 declared fields; independent record. |
| [Process deferred accounting](process_deferred_accounting.json) | 8 declared fields; independent record. |
| [Process payment reconciliation](process_payment_reconciliation.json) | 20 declared fields; independent record. |
| [Process payment reconciliation log](process_payment_reconciliation_log.json) | 13 declared fields; independent record. |
| [Process payment reconciliation log allocations](process_payment_reconciliation_log_allocations.json) | 20 declared fields; owned child record. |
| [Process period closing voucher](process_period_closing_voucher.json) | 9 declared fields; independent record. |
| [Process period closing voucher detail](process_period_closing_voucher_detail.json) | 4 declared fields; owned child record. |
| [Process statement of accounts](process_statement_of_accounts.json) | 58 declared fields; independent record. |
| [Process statement of accounts carbon copy](process_statement_of_accounts_carbon_copy.json) | 1 declared fields; owned child record. |
| [Process statement of accounts cost center](process_statement_of_accounts_cost_center.json) | 1 declared fields; owned child record. |
| [Process statement of accounts customer](process_statement_of_accounts_customer.json) | 4 declared fields; owned child record. |
| [Process statement of accounts project](process_statement_of_accounts_project.json) | 1 declared fields; owned child record. |
| [Process subscription](process_subscription.json) | 3 declared fields; independent record. |
| [Product bundle](product_bundle.json) | 11 declared fields; independent record. |
| [Product bundle item](product_bundle_item.json) | 5 declared fields; owned child record. |
| [Production plan](production_plan.json) | 60 declared fields; independent record. |
| [Production plan item](production_plan_item.json) | 24 declared fields; owned child record. |
| [Production plan item reference](production_plan_item_reference.json) | 4 declared fields; owned child record. |
| [Production plan material request](production_plan_material_request.json) | 3 declared fields; owned child record. |
| [Production plan material request warehouse](production_plan_material_request_warehouse.json) | 1 declared fields; owned child record. |
| [Production plan sales order](production_plan_sales_order.json) | 6 declared fields; owned child record. |
| [Production plan schedule](production_plan_schedule.json) | 19 declared fields; independent record. |
| [Production plan subordinate assembly item](production_plan_subordinate_assembly_item.json) | 35 declared fields; owned child record. |
| [Proforma invoice](proforma_invoice.json) | 29 declared fields; independent record. |
| [Proforma invoice item](proforma_invoice_item.json) | 8 declared fields; owned child record. |
| [Progressive web application notification](progressive_web_application_notification.json) | 10 declared fields; independent record. |
| [Project](project.json) | 59 declared fields; independent record. |
| [Project template](project_template.json) | 3 declared fields; independent record. |
| [Project template task](project_template_task.json) | 2 declared fields; owned child record. |
| [Project type](project_type.json) | 2 declared fields; independent record. |
| [Project update](project_update.json) | 9 declared fields; independent record. |
| [Project user](project_user.json) | 10 declared fields; owned child record. |
| [Projects settings](projects_settings.json) | 5 declared fields; singleton settings. |
| [Promotional scheme](promotional_scheme.json) | 37 declared fields; independent record. |
| [Promotional scheme price discount](promotional_scheme_price_discount.json) | 24 declared fields; owned child record. |
| [Promotional scheme product discount](promotional_scheme_product_discount.json) | 26 declared fields; owned child record. |
| [Property setter](property_setter.json) | 15 declared fields; independent record. |
| [Prospect](prospect.json) | 31 declared fields; independent record. |
| [Prospect lead](prospect_lead.json) | 7 declared fields; owned child record. |
| [Prospect opportunity](prospect_opportunity.json) | 9 declared fields; owned child record. |
| [Purchase invoice](purchase_invoice.json) | 199 declared fields; independent record. |
| [Purchase invoice advance](purchase_invoice_advance.json) | 10 declared fields; owned child record. |
| [Purchase invoice item](purchase_invoice_item.json) | 118 declared fields; owned child record. |
| [Purchase order](purchase_order.json) | 154 declared fields; independent record. |
| [Purchase order item](purchase_order_item.json) | 107 declared fields; owned child record. |
| [Purchase receipt](purchase_receipt.json) | 147 declared fields; independent record. |
| [Purchase receipt item](purchase_receipt_item.json) | 128 declared fields; owned child record. |
| [Purchase receipt item supplied](purchase_receipt_item_supplied.json) | 23 declared fields; owned child record. |
| [Purchase taxes and charges](purchase_taxes_and_charges.json) | 32 declared fields; owned child record. |
| [Purchase taxes and charges template](purchase_taxes_and_charges_template.json) | 8 declared fields; independent record. |
| [Purpose of travel](purpose_of_travel.json) | 1 declared fields; independent record. |
| [Push notification settings](push_notification_settings.json) | 5 declared fields; singleton settings. |
| [Putaway rule](putaway_rule.json) | 12 declared fields; independent record. |
| [Quality action](quality_action.json) | 10 declared fields; independent record. |
| [Quality action resolution](quality_action_resolution.json) | 5 declared fields; owned child record. |
| [Quality feedback](quality_feedback.json) | 6 declared fields; independent record. |
| [Quality feedback parameter](quality_feedback_parameter.json) | 5 declared fields; owned child record. |
| [Quality feedback template](quality_feedback_template.json) | 3 declared fields; independent record. |
| [Quality feedback template parameter](quality_feedback_template_parameter.json) | 1 declared fields; owned child record. |
| [Quality goal](quality_goal.json) | 8 declared fields; independent record. |
| [Quality goal objective](quality_goal_objective.json) | 4 declared fields; owned child record. |
| [Quality inspection](quality_inspection.json) | 30 declared fields; independent record. |
| [Quality inspection parameter](quality_inspection_parameter.json) | 3 declared fields; independent record. |
| [Quality inspection parameter group](quality_inspection_parameter_group.json) | 1 declared fields; independent record. |
| [Quality inspection reading](quality_inspection_reading.json) | 26 declared fields; owned child record. |
| [Quality inspection template](quality_inspection_template.json) | 2 declared fields; independent record. |
| [Quality meeting](quality_meeting.json) | 6 declared fields; independent record. |
| [Quality meeting agenda](quality_meeting_agenda.json) | 1 declared fields; owned child record. |
| [Quality meeting minutes](quality_meeting_minutes.json) | 5 declared fields; owned child record. |
| [Quality procedure](quality_procedure.json) | 11 declared fields; independent record. |
| [Quality procedure process](quality_procedure_process.json) | 2 declared fields; owned child record. |
| [Quality review](quality_review.json) | 9 declared fields; independent record. |
| [Quality review objective](quality_review_objective.json) | 7 declared fields; owned child record. |
| [Query parameters](query_parameters.json) | 2 declared fields; owned child record. |
| [Quick stock balance](quick_stock_balance.json) | 12 declared fields; singleton settings. |
| [Quotation](quotation.json) | 132 declared fields; independent record. |
| [Quotation item](quotation_item.json) | 79 declared fields; owned child record. |
| [Quotation lost reason](quotation_lost_reason.json) | 1 declared fields; independent record. |
| [Quotation lost reason detail](quotation_lost_reason_detail.json) | 1 declared fields; owned child record. |
| [Record field](record_field.json) | 80 declared fields; owned child record. |
| [Record permission](record_permission.json) | 24 declared fields; owned child record. |
| [Record share](record_share.json) | 9 declared fields; independent record. |
| [Record type](record_type.json) | 94 declared fields; independent record. |
| [Record type action](record_type_action.json) | 6 declared fields; owned child record. |
| [Record type layout](record_type_layout.json) | 19 declared fields; independent record. |
| [Record type layout child table](record_type_layout_child_table.json) | 2 declared fields; owned child record. |
| [Record type layout field](record_type_layout_field.json) | 16 declared fields; owned child record. |
| [Record type link](record_type_link.json) | 8 declared fields; owned child record. |
| [Record type settings map](record_type_settings_map.json) | 5 declared fields; independent record. |
| [Record type settings map item](record_type_settings_map_item.json) | 2 declared fields; owned child record. |
| [Record type state](record_type_state.json) | 3 declared fields; owned child record. |
| [Record type to sync](record_type_to_sync.json) | 1 declared fields; owned child record. |
| [Recorder](recorder.json) | 22 declared fields; virtual record. |
| [Recorder event](recorder_event.json) | 10 declared fields; virtual record. |
| [Recorder query](recorder_query.json) | 13 declared fields; virtual record. |
| [Recorder suggested index](recorder_suggested_index.json) | 2 declared fields; virtual record. |
| [Reminder](reminder.json) | 6 declared fields; independent record. |
| [Rename tool](rename_tool.json) | 3 declared fields; singleton settings. |
| [Reply to address](reply_to_address.json) | 3 declared fields; owned child record. |
| [Report](report.json) | 32 declared fields; independent record. |
| [Report column](report_column.json) | 5 declared fields; owned child record. |
| [Report filter](report_filter.json) | 8 declared fields; owned child record. |
| [Repost accounting ledger](repost_accounting_ledger.json) | 12 declared fields; independent record. |
| [Repost accounting ledger items](repost_accounting_ledger_items.json) | 6 declared fields; owned child record. |
| [Repost allowed types](repost_allowed_types.json) | 1 declared fields; owned child record. |
| [Repost item valuation](repost_item_valuation.json) | 31 declared fields; independent record. |
| [Repost payment ledger](repost_payment_ledger.json) | 12 declared fields; independent record. |
| [Repost payment ledger items](repost_payment_ledger_items.json) | 2 declared fields; owned child record. |
| [Request for quotation](request_for_quotation.json) | 42 declared fields; independent record. |
| [Request for quotation item](request_for_quotation_item.json) | 30 declared fields; owned child record. |
| [Request for quotation supplier](request_for_quotation_supplier.json) | 8 declared fields; owned child record. |
| [Retention bonus](retention_bonus.json) | 14 declared fields; independent record. |
| [Role](role.json) | 20 declared fields; independent record. |
| [Role permission for page and report](role_permission_for_page_and_report.json) | 8 declared fields; singleton settings. |
| [Role profile](role_profile.json) | 3 declared fields; independent record. |
| [Route history](route_history.json) | 2 declared fields; independent record. |
| [Routing](routing.json) | 3 declared fields; independent record. |
| [Salary component](salary_component.json) | 36 declared fields; independent record. |
| [Salary component account](salary_component_account.json) | 2 declared fields; owned child record. |
| [Salary detail](salary_detail.json) | 30 declared fields; owned child record. |
| [Salary slip](salary_slip.json) | 99 declared fields; independent record. |
| [Salary slip leave](salary_slip_leave.json) | 6 declared fields; owned child record. |
| [Salary slip loan](salary_slip_loan.json) | 9 declared fields; owned child record. |
| [Salary slip timesheet](salary_slip_timesheet.json) | 2 declared fields; owned child record. |
| [Salary structure](salary_structure.json) | 31 declared fields; independent record. |
| [Salary structure assignment](salary_structure_assignment.json) | 31 declared fields; independent record. |
| [Salary withholding](salary_withholding.json) | 21 declared fields; independent record. |
| [Salary withholding cycle](salary_withholding_cycle.json) | 4 declared fields; owned child record. |
| [Sales forecast](sales_forecast.json) | 20 declared fields; independent record. |
| [Sales forecast item](sales_forecast_item.json) | 6 declared fields; owned child record. |
| [Sales invoice](sales_invoice.json) | 235 declared fields; independent record. |
| [Sales invoice advance](sales_invoice_advance.json) | 10 declared fields; owned child record. |
| [Sales invoice item](sales_invoice_item.json) | 121 declared fields; owned child record. |
| [Sales invoice payment](sales_invoice_payment.json) | 9 declared fields; owned child record. |
| [Sales invoice reference](sales_invoice_reference.json) | 7 declared fields; owned child record. |
| [Sales invoice timesheet](sales_invoice_timesheet.json) | 15 declared fields; owned child record. |
| [Sales order](sales_order.json) | 176 declared fields; independent record. |
| [Sales order item](sales_order_item.json) | 115 declared fields; owned child record. |
| [Sales partner](sales_partner.json) | 25 declared fields; independent record. |
| [Sales partner item](sales_partner_item.json) | 1 declared fields; owned child record. |
| [Sales partner type](sales_partner_type.json) | 1 declared fields; independent record. |
| [Sales person](sales_person.json) | 14 declared fields; independent record. |
| [Sales stage](sales_stage.json) | 1 declared fields; independent record. |
| [Sales taxes and charges](sales_taxes_and_charges.json) | 27 declared fields; owned child record. |
| [Sales taxes and charges template](sales_taxes_and_charges_template.json) | 8 declared fields; independent record. |
| [Sales team](sales_team.json) | 6 declared fields; owned child record. |
| [Salutation](salutation.json) | 1 declared fields; independent record. |
| [Scheduled job log](scheduled_job_log.json) | 4 declared fields; independent record. |
| [Scheduled job type](scheduled_job_type.json) | 12 declared fields; independent record. |
| [Scheduler event](scheduler_event.json) | 2 declared fields; independent record. |
| [Security settings](security_settings.json) | 6 declared fields; singleton settings. |
| [Security settings contact](security_settings_contact.json) | 2 declared fields; owned child record. |
| [Security settings language](security_settings_language.json) | 1 declared fields; owned child record. |
| [Selling settings](selling_settings.json) | 60 declared fields; singleton settings. |
| [Serial and batch bundle](serial_and_batch_bundle.json) | 30 declared fields; independent record. |
| [Serial and batch entry](serial_and_batch_entry.json) | 23 declared fields; owned child record. |
| [Serial no](serial_no.json) | 36 declared fields; independent record. |
| [Server script](server_script.json) | 19 declared fields; independent record. |
| [Service day](service_day.json) | 5 declared fields; owned child record. |
| [Service level agreement](service_level_agreement.json) | 25 declared fields; independent record. |
| [Service level agreement fulfilled on status](service_level_agreement_fulfilled_on_status.json) | 1 declared fields; owned child record. |
| [Service level priority](service_level_priority.json) | 7 declared fields; owned child record. |
| [Session default](session_default.json) | 1 declared fields; owned child record. |
| [Session default settings](session_default_settings.json) | 1 declared fields; singleton settings. |
| [Share balance](share_balance.json) | 10 declared fields; owned child record. |
| [Share transfer](share_transfer.json) | 26 declared fields; independent record. |
| [Share type](share_type.json) | 2 declared fields; independent record. |
| [Shareholder](shareholder.json) | 15 declared fields; independent record. |
| [Shift assignment](shift_assignment.json) | 17 declared fields; independent record. |
| [Shift assignment tool](shift_assignment_tool.json) | 28 declared fields; singleton settings. |
| [Shift location](shift_location.json) | 8 declared fields; independent record. |
| [Shift request](shift_request.json) | 11 declared fields; independent record. |
| [Shift schedule](shift_schedule.json) | 6 declared fields; independent record. |
| [Shift schedule assignment](shift_schedule_assignment.json) | 12 declared fields; independent record. |
| [Shift type](shift_type.json) | 28 declared fields; independent record. |
| [Shipment](shipment.json) | 56 declared fields; independent record. |
| [Shipment delivery note](shipment_delivery_note.json) | 2 declared fields; owned child record. |
| [Shipment parcel](shipment_parcel.json) | 5 declared fields; owned child record. |
| [Shipment parcel template](shipment_parcel_template.json) | 5 declared fields; independent record. |
| [Shipping rule](shipping_rule.json) | 20 declared fields; independent record. |
| [Shipping rule condition](shipping_rule_condition.json) | 3 declared fields; owned child record. |
| [Shipping rule country](shipping_rule_country.json) | 1 declared fields; owned child record. |
| [Short message service center](short_message_service_center.json) | 13 declared fields; singleton settings. |
| [Short message service log](short_message_service_log.json) | 10 declared fields; independent record. |
| [Short message service parameter](short_message_service_parameter.json) | 3 declared fields; owned child record. |
| [Short message service settings](short_message_service_settings.json) | 8 declared fields; singleton settings. |
| [Sidebar](sidebar.json) | 11 declared fields; independent record. |
| [Sidebar item](sidebar_item.json) | 28 declared fields; owned child record. |
| [Skill](skill.json) | 2 declared fields; independent record. |
| [Skill assessment](skill_assessment.json) | 2 declared fields; owned child record. |
| [Slack webhook resource address](slack_webhook_resource_address.json) | 3 declared fields; independent record. |
| [Social link settings](social_link_settings.json) | 3 declared fields; owned child record. |
| [Social login key](social_login_key.json) | 28 declared fields; independent record. |
| [South africa value added tax account](south_africa_value_added_tax_account.json) | 1 declared fields; owned child record. |
| [South africa value added tax settings](south_africa_value_added_tax_settings.json) | 2 declared fields; independent record. |
| [Staffing plan](staffing_plan.json) | 11 declared fields; independent record. |
| [Staffing plan detail](staffing_plan_detail.json) | 8 declared fields; owned child record. |
| [Stock closing balance](stock_closing_balance.json) | 25 declared fields; independent record. |
| [Stock closing entry](stock_closing_entry.json) | 7 declared fields; independent record. |
| [Stock entry](stock_entry.json) | 90 declared fields; independent record. |
| [Stock entry detail](stock_entry_detail.json) | 80 declared fields; owned child record. |
| [Stock entry type](stock_entry_type.json) | 4 declared fields; independent record. |
| [Stock ledger entry](stock_ledger_entry.json) | 36 declared fields; independent record. |
| [Stock reconciliation](stock_reconciliation.json) | 24 declared fields; independent record. |
| [Stock reconciliation item](stock_reconciliation_item.json) | 35 declared fields; owned child record. |
| [Stock reposting settings](stock_reposting_settings.json) | 17 declared fields; singleton settings. |
| [Stock reservation entry](stock_reservation_entry.json) | 34 declared fields; independent record. |
| [Stock settings](stock_settings.json) | 80 declared fields; singleton settings. |
| [Subcontracting bill of materials](subcontracting_bill_of_materials.json) | 13 declared fields; independent record. |
| [Subcontracting inward order](subcontracting_inward_order.json) | 31 declared fields; independent record. |
| [Subcontracting inward order item](subcontracting_inward_order_item.json) | 17 declared fields; owned child record. |
| [Subcontracting inward order received item](subcontracting_inward_order_received_item.json) | 20 declared fields; owned child record. |
| [Subcontracting inward order secondary item](subcontracting_inward_order_secondary_item.json) | 13 declared fields; owned child record. |
| [Subcontracting inward order service item](subcontracting_inward_order_service_item.json) | 14 declared fields; owned child record. |
| [Subcontracting order](subcontracting_order.json) | 57 declared fields; independent record. |
| [Subcontracting order item](subcontracting_order_item.json) | 50 declared fields; owned child record. |
| [Subcontracting order service item](subcontracting_order_service_item.json) | 18 declared fields; owned child record. |
| [Subcontracting order supplied item](subcontracting_order_supplied_item.json) | 21 declared fields; owned child record. |
| [Subcontracting receipt](subcontracting_receipt.json) | 80 declared fields; independent record. |
| [Subcontracting receipt item](subcontracting_receipt_item.json) | 76 declared fields; owned child record. |
| [Subcontracting receipt supplied item](subcontracting_receipt_supplied_item.json) | 35 declared fields; owned child record. |
| [Submission queue](submission_queue.json) | 10 declared fields; independent record. |
| [Subordinate operation](subordinate_operation.json) | 4 declared fields; owned child record. |
| [Subscription](subscription.json) | 40 declared fields; independent record. |
| [Subscription invoice](subscription_invoice.json) | 2 declared fields; owned child record. |
| [Subscription plan](subscription_plan.json) | 20 declared fields; independent record. |
| [Subscription plan detail](subscription_plan_detail.json) | 2 declared fields; owned child record. |
| [Subscription settings](subscription_settings.json) | 3 declared fields; singleton settings. |
| [Success action](success_action.json) | 6 declared fields; independent record. |
| [Supplier](supplier.json) | 75 declared fields; independent record. |
| [Supplier group](supplier_group.json) | 10 declared fields; independent record. |
| [Supplier group item](supplier_group_item.json) | 1 declared fields; owned child record. |
| [Supplier item](supplier_item.json) | 1 declared fields; owned child record. |
| [Supplier number at customer](supplier_number_at_customer.json) | 2 declared fields; owned child record. |
| [Supplier quotation](supplier_quotation.json) | 111 declared fields; independent record. |
| [Supplier quotation item](supplier_quotation_item.json) | 72 declared fields; owned child record. |
| [Supplier scorecard](supplier_scorecard.json) | 21 declared fields; independent record. |
| [Supplier scorecard criteria](supplier_scorecard_criteria.json) | 4 declared fields; independent record. |
| [Supplier scorecard period](supplier_scorecard_period.json) | 12 declared fields; independent record. |
| [Supplier scorecard scoring criteria](supplier_scorecard_scoring_criteria.json) | 7 declared fields; owned child record. |
| [Supplier scorecard scoring standing](supplier_scorecard_scoring_standing.json) | 15 declared fields; owned child record. |
| [Supplier scorecard scoring variable](supplier_scorecard_scoring_variable.json) | 5 declared fields; owned child record. |
| [Supplier scorecard standing](supplier_scorecard_standing.json) | 12 declared fields; independent record. |
| [Supplier scorecard variable](supplier_scorecard_variable.json) | 6 declared fields; independent record. |
| [Support search source](support_search_source.json) | 20 declared fields; owned child record. |
| [Support settings](support_settings.json) | 23 declared fields; singleton settings. |
| [System console](system_console.json) | 9 declared fields; singleton settings. |
| [System health report](system_health_report.json) | 63 declared fields; virtual record. |
| [System health report errors](system_health_report_errors.json) | 2 declared fields; virtual record. |
| [System health report failing jobs](system_health_report_failing_jobs.json) | 2 declared fields; virtual record. |
| [System health report queue](system_health_report_queue.json) | 2 declared fields; virtual record. |
| [System health report tables](system_health_report_tables.json) | 2 declared fields; virtual record. |
| [System health report workers](system_health_report_workers.json) | 4 declared fields; virtual record. |
| [System settings](system_settings.json) | 120 declared fields; singleton settings. |
| [Tag](tag.json) | 1 declared fields; independent record. |
| [Tag link](tag_link.json) | 4 declared fields; independent record. |
| [Target detail](target_detail.json) | 5 declared fields; owned child record. |
| [Task](task.json) | 51 declared fields; independent record. |
| [Task depends on](task_depends_on.json) | 4 declared fields; owned child record. |
| [Task type](task_type.json) | 2 declared fields; independent record. |
| [Tax category](tax_category.json) | 2 declared fields; independent record. |
| [Tax rule](tax_rule.json) | 32 declared fields; independent record. |
| [Tax withholding account](tax_withholding_account.json) | 2 declared fields; owned child record. |
| [Tax withholding category](tax_withholding_category.json) | 12 declared fields; independent record. |
| [Tax withholding entry](tax_withholding_entry.json) | 29 declared fields; owned child record. |
| [Tax withholding group](tax_withholding_group.json) | 1 declared fields; independent record. |
| [Tax withholding rate](tax_withholding_rate.json) | 7 declared fields; owned child record. |
| [Taxable salary slab](taxable_salary_slab.json) | 6 declared fields; owned child record. |
| [Telephony call type](telephony_call_type.json) | 2 declared fields; independent record. |
| [Terms and conditions](terms_and_conditions.json) | 10 declared fields; independent record. |
| [Territory](territory.json) | 10 declared fields; independent record. |
| [Territory item](territory_item.json) | 1 declared fields; owned child record. |
| [Timesheet](timesheet.json) | 37 declared fields; independent record. |
| [Timesheet detail](timesheet_detail.json) | 28 declared fields; owned child record. |
| [To do](to_do.json) | 18 declared fields; independent record. |
| [Token cache](token_cache.json) | 10 declared fields; independent record. |
| [Top bar item](top_bar_item.json) | 6 declared fields; owned child record. |
| [Training event](training_event.json) | 26 declared fields; independent record. |
| [Training event employee](training_event_employee.json) | 7 declared fields; owned child record. |
| [Training feedback](training_feedback.json) | 11 declared fields; independent record. |
| [Training program](training_program.json) | 13 declared fields; independent record. |
| [Training result](training_result.json) | 5 declared fields; independent record. |
| [Training result employee](training_result_employee.json) | 9 declared fields; owned child record. |
| [Transaction deletion record](transaction_deletion_record.json) | 19 declared fields; independent record. |
| [Transaction deletion record details](transaction_deletion_record_details.json) | 4 declared fields; owned child record. |
| [Transaction deletion record item](transaction_deletion_record_item.json) | 1 declared fields; owned child record. |
| [Transaction deletion record to delete](transaction_deletion_record_to_delete.json) | 5 declared fields; owned child record. |
| [Translation](translation.json) | 10 declared fields; independent record. |
| [Travel itinerary](travel_itinerary.json) | 15 declared fields; owned child record. |
| [Travel request](travel_request.json) | 31 declared fields; independent record. |
| [Travel request costing](travel_request_costing.json) | 7 declared fields; owned child record. |
| [Unhandled email](unhandled_email.json) | 5 declared fields; independent record. |
| [Unit of measure](unit_of_measure.json) | 8 declared fields; independent record. |
| [Unit of measure category](unit_of_measure_category.json) | 1 declared fields; independent record. |
| [Unit of measure conversion detail](unit_of_measure_conversion_detail.json) | 3 declared fields; owned child record. |
| [Unit of measure conversion factor](unit_of_measure_conversion_factor.json) | 5 declared fields; independent record. |
| [United arab emirates value added tax account](united_arab_emirates_value_added_tax_account.json) | 1 declared fields; owned child record. |
| [United arab emirates value added tax settings](united_arab_emirates_value_added_tax_settings.json) | 2 declared fields; independent record. |
| [Unreconcile payment](unreconcile_payment.json) | 6 declared fields; independent record. |
| [Unreconcile payment entries](unreconcile_payment_entries.json) | 8 declared fields; owned child record. |
| [User](user.json) | 107 declared fields; independent record. |
| [User document type](user_document_type.json) | 17 declared fields; owned child record. |
| [User email](user_email.json) | 6 declared fields; owned child record. |
| [User group](user_group.json) | 1 declared fields; independent record. |
| [User group member](user_group_member.json) | 1 declared fields; owned child record. |
| [User invitation](user_invitation.json) | 10 declared fields; independent record. |
| [User permission](user_permission.json) | 10 declared fields; independent record. |
| [User role](user_role.json) | 1 declared fields; owned child record. |
| [User role profile](user_role_profile.json) | 1 declared fields; owned child record. |
| [User select document type](user_select_document_type.json) | 1 declared fields; owned child record. |
| [User session display](user_session_display.json) | 9 declared fields; virtual record. |
| [User social login](user_social_login.json) | 5 declared fields; owned child record. |
| [User type](user_type.json) | 12 declared fields; independent record. |
| [User type module](user_type_module.json) | 1 declared fields; owned child record. |
| [User workspaces](user_workspaces.json) | 1 declared fields; owned child record. |
| [Variant field](variant_field.json) | 1 declared fields; owned child record. |
| [Vehicle](vehicle.json) | 28 declared fields; independent record. |
| [Vehicle log](vehicle_log.json) | 21 declared fields; independent record. |
| [Vehicle service](vehicle_service.json) | 4 declared fields; owned child record. |
| [Vehicle service item](vehicle_service_item.json) | 1 declared fields; independent record. |
| [Version](version.json) | 6 declared fields; independent record. |
| [Video](video.json) | 16 declared fields; independent record. |
| [Video settings](video_settings.json) | 3 declared fields; singleton settings. |
| [View log](view_log.json) | 3 declared fields; independent record. |
| [Voice call settings](voice_call_settings.json) | 6 declared fields; independent record. |
| [Warehouse](warehouse.json) | 35 declared fields; independent record. |
| [Warehouse type](warehouse_type.json) | 1 declared fields; independent record. |
| [Warranty claim](warranty_claim.json) | 38 declared fields; independent record. |
| [Web form](web_form.json) | 63 declared fields; independent record. |
| [Web form field](web_form_field.json) | 23 declared fields; owned child record. |
| [Web form list column](web_form_list_column.json) | 4 declared fields; owned child record. |
| [Web form request](web_form_request.json) | 11 declared fields; independent record. |
| [Web page](web_page.json) | 45 declared fields; independent record. |
| [Web page block](web_page_block.json) | 15 declared fields; owned child record. |
| [Web page view](web_page_view.json) | 12 declared fields; independent record. |
| [Web template](web_template.json) | 5 declared fields; independent record. |
| [Web template field](web_template_field.json) | 6 declared fields; owned child record. |
| [Webhook](webhook.json) | 26 declared fields; independent record. |
| [Webhook data](webhook_data.json) | 3 declared fields; owned child record. |
| [Webhook header](webhook_header.json) | 2 declared fields; owned child record. |
| [Webhook request log](webhook_request_log.json) | 13 declared fields; independent record. |
| [Website attribute](website_attribute.json) | 1 declared fields; owned child record. |
| [Website filter field](website_filter_field.json) | 1 declared fields; owned child record. |
| [Website item group](website_item_group.json) | 1 declared fields; owned child record. |
| [Website meta tag](website_meta_tag.json) | 2 declared fields; owned child record. |
| [Website route meta](website_route_meta.json) | 1 declared fields; independent record. |
| [Website route redirect](website_route_redirect.json) | 5 declared fields; owned child record. |
| [Website script](website_script.json) | 1 declared fields; singleton settings. |
| [Website settings](website_settings.json) | 69 declared fields; singleton settings. |
| [Website sidebar](website_sidebar.json) | 2 declared fields; independent record. |
| [Website sidebar item](website_sidebar_item.json) | 3 declared fields; owned child record. |
| [Website slideshow](website_slideshow.json) | 4 declared fields; independent record. |
| [Website slideshow item](website_slideshow_item.json) | 4 declared fields; owned child record. |
| [Website theme](website_theme.json) | 24 declared fields; independent record. |
| [Website theme ignore application](website_theme_ignore_application.json) | 1 declared fields; owned child record. |
| [Work order](work_order.json) | 86 declared fields; independent record. |
| [Work order additional item](work_order_additional_item.json) | 7 declared fields; virtual record. |
| [Work order item](work_order_item.json) | 28 declared fields; owned child record. |
| [Work order operation](work_order_operation.json) | 40 declared fields; owned child record. |
| [Workflow](workflow.json) | 12 declared fields; independent record. |
| [Workflow action](workflow_action.json) | 9 declared fields; independent record. |
| [Workflow action master](workflow_action_master.json) | 1 declared fields; independent record. |
| [Workflow action permitted role](workflow_action_permitted_role.json) | 1 declared fields; owned child record. |
| [Workflow document state](workflow_document_state.json) | 14 declared fields; owned child record. |
| [Workflow state](workflow_state.json) | 3 declared fields; independent record. |
| [Workflow transition](workflow_transition.json) | 12 declared fields; owned child record. |
| [Workflow transition task](workflow_transition_task.json) | 4 declared fields; owned child record. |
| [Workflow transition tasks](workflow_transition_tasks.json) | 1 declared fields; independent record. |
| [Workspace](workspace.json) | 34 declared fields; independent record. |
| [Workspace chart](workspace_chart.json) | 2 declared fields; owned child record. |
| [Workspace custom block](workspace_custom_block.json) | 2 declared fields; owned child record. |
| [Workspace link](workspace_link.json) | 16 declared fields; owned child record. |
| [Workspace number card](workspace_number_card.json) | 2 declared fields; owned child record. |
| [Workspace quick list](workspace_quick_list.json) | 5 declared fields; owned child record. |
| [Workspace shortcut](workspace_shortcut.json) | 15 declared fields; owned child record. |
| [Workspace sidebar](workspace_sidebar.json) | 10 declared fields; independent record. |
| [Workspace sidebar item](workspace_sidebar_item.json) | 23 declared fields; owned child record. |
| [Workstation](workstation.json) | 27 declared fields; independent record. |
| [Workstation cost](workstation_cost.json) | 2 declared fields; owned child record. |
| [Workstation operating component](workstation_operating_component.json) | 3 declared fields; independent record. |
| [Workstation operating component account](workstation_operating_component_account.json) | 2 declared fields; owned child record. |
| [Workstation type](workstation_type.json) | 7 declared fields; independent record. |
| [Workstation working hour](workstation_working_hour.json) | 5 declared fields; owned child record. |
