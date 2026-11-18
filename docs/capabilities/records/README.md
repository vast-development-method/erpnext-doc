# Optional record contracts

The catalogue gives the attributes, relationships and declared role permissions for optional business capabilities. Combine a capability with the shared model using its named integration records. Separate configuration numbers within one capability preserve independent alternatives; merging their required fields or access grants would change their behaviour.

There are 3,143 entity contracts, 29,388 distinct scoped attributes from 29,401 declarations, and 3,808 additional field or form specifications from 4,099 declarations. Permissions comprise 4,971 record grants and 234 additional grants. The 1,136 rule addresses identify configurable properties. [Relationship decisions](relationship-decisions.md) identifies the references requiring a deployment choice or an external record definition.

## Reading a contract

Each concept has a capability and configuration scope. An empty characteristics list denotes a regular independent record. An owned row is a member of a parent collection. A single-configuration record holds settings. A computed record is read as a projection. Submission and hierarchy are additional independent characteristics. A reference selects one record of its named target, and an owned collection can have multiple rows. A variable reference selects its class using the named field on the same record. A plain target identifies a record in the same capability and configuration. A shared-model target gives the qualified name in the [entity index](../../../schema/index.tsv). When several candidates exist, select and bind one applicable target explicitly. A configured optional dependency lists its capability, configuration number and record. An external contract requires the selected installation to supply the record. Where a collection names an independent record, the ownership contract must be resolved before enforcing a delete cascade. Equivalent repeated declarations of one attribute are counted on that attribute and represent a single stored value.

An attribute carries its value kind, applicable constraints and elevated access level when declared. Required applies to entry under its effective conditions. Absence of an explicit required flag leaves conditional or workflow validation to its owning process. An enum value named unselected represents the blank selection. Provider choices and number-series variants are expressed by function. Configure the concrete external party, number prefix, authorized endpoint and settlement terms independently. A value-kind label alone does not specify precision or a rounding rule.

Additional fields extend the stated record, while grouping and action controls only affect the form. Placement names the field or control after which the addition appears. Alternative declarations record distinct configurations for the same field. Equivalent declarations share one listed row with their multiplicity. A grant tuple lists role, access level, allowed actions and owner-only status in that order. Additional grants begin with the affected record. A rule address lists the record, optional field, affected property and value kind. The actual override value is unspecified when the declaration does not supply it.

## Capability index

| Capability | Record volumes |
|---|---|
| Accommodation reservations | [1](volume-001.json), [2](volume-002.json), [3](volume-003.json) |
| Account balance feed reconciliation | [3](volume-003.json) |
| Accounting daybook migration and reversal | [3](volume-003.json) |
| Accounting master data migration | [3](volume-003.json) |
| Accounting system synchronization | [3](volume-003.json) |
| Advertising lead capture | [3](volume-003.json) |
| Analytical report design | [4](volume-004.json) |
| Analytical reporting | [4](volume-004.json) |
| Appointment capacity and coupons | [4](volume-004.json) |
| Argentine electronic invoicing | [4](volume-004.json) |
| Assisted business operations | [4](volume-004.json) |
| Assisted business record lookup | [4](volume-004.json) |
| Assisted operations approval | [5](volume-005.json), [6](volume-006.json) |
| Assisted text generation | [6](volume-006.json) |
| Attachment object storage | [6](volume-006.json) |
| Attachment routing by storage folder | [6](volume-006.json) |
| Attendance and overtime time sheets | [6](volume-006.json) |
| Attendance device collection | [6](volume-006.json) |
| Audience-specific alerts | [6](volume-006.json) |
| Australian accounting and tax | [7](volume-007.json) |
| Balance sheet reconciliation | [7](volume-007.json) |
| Bangladeshi value added tax invoices | [7](volume-007.json) |
| Bank account feed synchronization | [7](volume-007.json) |
| Bank messaging and account reconciliation | [7](volume-007.json) |
| Bank payout integration | [7](volume-007.json) |
| Barcode label printing | [7](volume-007.json) |
| Batch payments and remittance advice | [7](volume-007.json) |
| Billable time capture | [7](volume-007.json) |
| Biometric attendance and leave | [7](volume-007.json) |
| Biometric attendance device import | [7](volume-007.json) |
| British value added tax filing | [8](volume-008.json) |
| Brokerage statement accounting | [8](volume-008.json) |
| Burundian electronic sales reporting | [8](volume-008.json) |
| Business call integration | [8](volume-008.json) |
| Business messaging campaigns | [8](volume-008.json) |
| Business messaging dispatch | [8](volume-008.json) |
| Business messaging notifications | [8](volume-008.json) |
| Cargo bookings and container movements | [9](volume-009.json) |
| Carrier dispatch automation | [9](volume-009.json) |
| Carrier service and parcel booking | [9](volume-009.json) |
| Carrier tracking and shipment registration | [9](volume-009.json) |
| Cashbook and treasury categories | [9](volume-009.json) |
| Certificate-based document signing | [9](volume-009.json) |
| Channel item and warehouse mapping | [10](volume-010.json) |
| Cheque payment runs | [10](volume-010.json) |
| Collaborative diagramming | [10](volume-010.json) |
| Collaborative document spaces | [10](volume-010.json) |
| Collaborative knowledge publishing | [10](volume-010.json) |
| Committee opening of supplier quotations | [10](volume-010.json) |
| Company-scoped navigation | [10](volume-010.json) |
| Compliance obligations and client cases | [11](volume-011.json), [12](volume-012.json) |
| Conditional record access | [12](volume-012.json) |
| Congregational care and events | [13](volume-013.json), [14](volume-014.json), [15](volume-015.json) |
| Consignment delivery management | [16](volume-016.json) |
| Construction quantities and budgets | [16](volume-016.json) |
| Contract dues and settlement | [16](volume-016.json) |
| Contribution points and reviews | [16](volume-016.json) |
| Control evidence and risk assessment | [17](volume-017.json) |
| Controlled credential sharing | [17](volume-017.json) |
| Controlled external file distribution | [17](volume-017.json) |
| Conversation campaigns and notes | [17](volume-017.json) |
| Conversation history and usage | [17](volume-017.json) |
| Conversational business record lookup | [17](volume-017.json) |
| Conversational messaging rules | [18](volume-018.json) |
| Copying document lines | [18](volume-018.json) |
| Counterparty due diligence | [18](volume-018.json) |
| Course delivery and learning assessment | [19](volume-019.json) |
| Customer messaging contacts | [19](volume-019.json) |
| Delivery charges and mobile money at tills | [20](volume-020.json) |
| Device-bound authentication | [20](volume-020.json) |
| Digital signage content | [20](volume-020.json) |
| Document clauses and templates | [20](volume-020.json) |
| Document email reminders | [20](volume-020.json) |
| Document event messaging | [20](volume-020.json) |
| Document intake and extraction | [20](volume-020.json) |
| Document limits and usage quotas | [20](volume-020.json) |
| Document rendition on submission | [20](volume-020.json) |
| Document signing field mapping | [20](volume-020.json) |
| Earnest money deposit accounting | [20](volume-020.json) |
| Ecuadorian electronic invoicing | [21](volume-021.json) |
| Editorial publishing | [21](volume-021.json) |
| Egyptian electronic receipts and invoices | [21](volume-021.json) |
| Electronic invoice interchange | [21](volume-021.json) |
| Electronic invoice network delivery | [21](volume-021.json) |
| Email broadcast and delivery tracking | [21](volume-021.json) |
| Employee advance repayments | [21](volume-021.json) |
| Employee professional tax | [21](volume-021.json) |
| Employee project assignment instructions | [21](volume-021.json), [22](volume-022.json) |
| European electronic invoice import | [22](volume-022.json) |
| Event-triggered conversational messaging | [22](volume-022.json) |
| Exchange rate synchronization | [22](volume-022.json) |
| Export duty rebate claims | [22](volume-022.json) |
| Export letters of credit | [22](volume-022.json) |
| External editorial publishing | [22](volume-022.json) |
| External storage routing | [22](volume-022.json) |
| Fiscal device end-of-day records | [22](volume-022.json) |
| Fixed deposit management | [22](volume-022.json) |
| Garment reservation and rental | [22](volume-022.json) |
| Gate compliance and discrepancies | [23](volume-023.json) |
| Gate dispatch and returns | [23](volume-023.json) |
| German accounting export | [23](volume-023.json) |
| Group appointments and availability | [23](volume-023.json) |
| Holiday calendars | [23](volume-023.json) |
| Image-to-address transcription | [23](volume-023.json) |
| Import letters of credit | [23](volume-023.json) |
| Incoming material price controls | [24](volume-024.json) |
| Indian identity and signature verification | [24](volume-024.json) |
| Indian payroll | [24](volume-024.json) |
| Indian postal addresses | [24](volume-024.json) |
| Indonesian tax invoice import and export | [24](volume-024.json) |
| Installable mobile workspace | [24](volume-024.json) |
| Invoice image and document extraction | [24](volume-024.json) |
| Invoice payment links | [24](volume-024.json) |
| Invoice signing | [24](volume-024.json) |
| Job applicant résumé assessment | [24](volume-024.json) |
| Kenyan electronic tax reporting | [25](volume-025.json), [26](volume-026.json) |
| Kenyan fiscal device transmission | [26](volume-026.json) |
| Kenyan sales and workforce records | [26](volume-026.json), [27](volume-027.json) |
| Leave calendar | [27](volume-027.json) |
| Ledger and tax mapping synchronization | [27](volume-027.json) |
| Livestock activity and valuation | [27](volume-027.json) |
| Maker and checker audit reports | [27](volume-027.json) |
| Malaysian electronic invoicing | [27](volume-027.json) |
| Marketplace inquiry synchronization | [27](volume-027.json) |
| Meeting administration | [28](volume-028.json) |
| Metered utility and rental billing | [28](volume-028.json) |
| Mexican electronic invoice compliance | [28](volume-028.json) |
| Mobile business operations | [28](volume-028.json) |
| Mobile employee self-service | [29](volume-029.json) |
| Mobile employee workspace | [29](volume-029.json) |
| Mobile money collection | [30](volume-030.json) |
| Mobile record synchronization | [30](volume-030.json) |
| Multilevel production recipe design | [30](volume-030.json) |
| Multiple attachment storage destinations | [30](volume-030.json) |
| Nepali civil day conversion | [30](volume-030.json) |
| Nigerian electronic invoicing | [30](volume-030.json) |
| Obligatory charitable contribution accounting | [30](volume-030.json) |
| Offline till reconciliation | [31](volume-031.json) |
| Offsite backup management | [31](volume-031.json) |
| One-time identity challenges | [31](volume-031.json) |
| Online payment collection | [31](volume-031.json) |
| Outbound facsimile delivery | [31](volume-031.json) |
| Pakistani accounting workspace | [31](volume-031.json) |
| Pakistani electronic invoicing | [31](volume-031.json) |
| Participant messaging and conversation retention | [32](volume-032.json) |
| Party-specific item account selection | [32](volume-032.json) |
| Payment service routing | [32](volume-032.json) |
| Payment terminal transactions | [32](volume-032.json) |
| Payroll penalties and corrections | [32](volume-032.json) |
| Permission-scoped conversational assistance | [32](volume-032.json), [33](volume-033.json) |
| Personal notes and work items | [33](volume-033.json) |
| Personal work categorization | [33](volume-033.json) |
| Photo identification and tagging | [33](volume-033.json) |
| Piece-rate payroll pools | [33](volume-033.json) |
| Policy document and report assistance | [33](volume-033.json) |
| Portal presentation | [33](volume-033.json) |
| Portuguese tax codes and numbering | [33](volume-033.json) |
| Postal location lookup | [33](volume-033.json) |
| Product price lookup | [33](volume-033.json) |
| Product recommendations and featured items | [33](volume-033.json) |
| Product text translation | [33](volume-033.json) |
| Production job scheduling | [33](volume-033.json) |
| Production line stoppage and changeovers | [33](volume-033.json) |
| Project checklists and contacts | [33](volume-033.json) |
| Project documentation publishing | [33](volume-033.json) |
| Project member and field permissions | [34](volume-034.json) |
| Project payroll allocation | [34](volume-034.json) |
| Property inspections and occupancy | [34](volume-034.json) |
| Protected document rendition | [34](volume-034.json) |
| Public benefit scheme enrolment | [35](volume-035.json) |
| Public forms and team ownership | [35](volume-035.json) |
| Public search discovery | [35](volume-035.json) |
| Public service catalogue | [35](volume-035.json) |
| Purchase tax statement reconciliation | [35](volume-035.json) |
| Quotation and proposal synchronization | [35](volume-035.json) |
| Reception access and room booking | [36](volume-036.json) |
| Recipient template message campaigns | [36](volume-036.json) |
| Recurring item subscriptions | [36](volume-036.json) |
| Regional financial statement templates | [36](volume-036.json) |
| Restaurant orders and station routing | [36](volume-036.json), [37](volume-037.json) |
| Restaurant till settlement import | [37](volume-037.json) |
| Retail checkout | [37](volume-037.json), [38](volume-038.json) |
| Retail checkout permissions and payment links | [38](volume-038.json) |
| Reusable bulk import and export layouts | [38](volume-038.json) |
| Reusable form presets | [38](volume-038.json) |
| Reusable letterhead design | [38](volume-038.json) |
| Role and grant duplication | [38](volume-038.json) |
| Role assignment administration | [38](volume-038.json) |
| Role grant administration | [38](volume-038.json) |
| Role-restricted knowledge pages | [38](volume-038.json) |
| Sales inquiry and contact synchronization | [38](volume-038.json) |
| Saudi electronic invoicing | [38](volume-038.json) |
| Saudi invoice signing credentials | [39](volume-039.json) |
| Scannable document verification | [39](volume-039.json) |
| Scheduled report distribution | [39](volume-039.json) |
| Self-registration restrictions | [39](volume-039.json) |
| Service desk management | [39](volume-039.json) |
| Service operation directory | [39](volume-039.json) |
| Session activity and access notices | [39](volume-039.json) |
| Shared file workspaces | [39](volume-039.json) |
| Shared spreadsheet synchronization | [39](volume-039.json) |
| Shared whiteboards | [40](volume-040.json) |
| Sheet cutting and offcut reuse | [40](volume-040.json) |
| Shift allocation imports | [40](volume-040.json) |
| Short links and scannable destinations | [40](volume-040.json) |
| Singapore goods and services tax | [40](volume-040.json) |
| Small enterprise supplier registration | [40](volume-040.json) |
| South African filing and privacy obligations | [40](volume-040.json) |
| South African injury and payroll reporting | [41](volume-041.json), [42](volume-042.json) |
| Spanish value added tax register | [42](volume-042.json) |
| Sri Lankan accounting and tax | [42](volume-042.json) |
| Staffing projects and labour costs | [42](volume-042.json) |
| Statement rule reconciliation | [42](volume-042.json) |
| Stone lot picking and packing | [42](volume-042.json) |
| Storage utilization and query performance | [42](volume-042.json) |
| Storefront availability synchronization | [43](volume-043.json) |
| Storefront order synchronization | [43](volume-043.json) |
| Storefront tax and warehouse mapping | [43](volume-043.json) |
| Structured trade invoice generation | [43](volume-043.json) |
| Support portal and party address capture | [43](volume-043.json) |
| Support ticket and engineering issue synchronization | [43](volume-043.json) |
| Swiss accounting export | [43](volume-043.json) |
| Swiss coded payment slips | [43](volume-043.json) |
| Swiss hours and tax reporting | [43](volume-043.json) |
| Tanzanian maintenance and inspection | [44](volume-044.json), [45](volume-045.json), [46](volume-046.json), [47](volume-047.json) |
| Task board rules and checklists | [47](volume-047.json) |
| Team communication channels | [48](volume-048.json) |
| Team communication integration | [48](volume-048.json) |
| Team discussions and project collaboration | [48](volume-048.json) |
| Technology asset management | [49](volume-049.json) |
| Tenant and team administration | [49](volume-049.json) |
| Text message gateway | [49](volume-049.json) |
| Thai accounting and tax | [50](volume-050.json) |
| Till card payment reconciliation | [50](volume-050.json) |
| Till customer messaging | [50](volume-050.json) |
| Till fiscal transaction certification | [50](volume-050.json) |
| Till opening and closing | [50](volume-050.json) |
| Translated item descriptions | [50](volume-050.json) |
| Ugandan electronic tax reporting | [50](volume-050.json), [51](volume-051.json) |
| United Arab Emirates electronic invoicing | [51](volume-051.json) |
| United States payroll disbursement | [51](volume-051.json) |
| Visitor conversion and account activation | [52](volume-052.json) |
| Voice agent and call records | [52](volume-052.json) |
| Wallet balances and categories | [52](volume-052.json) |
| Warehouse pallet capacity and pick faces | [52](volume-052.json) |
| Warehouse product group restrictions | [52](volume-052.json) |
| Web content and enquiry management | [53](volume-053.json) |
| Web page composition | [53](volume-053.json) |
| Work activity records | [53](volume-053.json) |
| Workforce administration | [54](volume-054.json) |
| Working time and break policies | [54](volume-054.json) |
| Workplace facial attendance | [54](volume-054.json) |
| Workspace presentation | [54](volume-054.json) |
| Workspace presentation preferences | [54](volume-054.json) |
| Workspace sound and theme preferences | [54](volume-054.json) |
| Zambian fiscal inventory reporting | [54](volume-054.json) |
