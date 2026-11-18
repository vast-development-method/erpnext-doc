# Functions and reports for optional business capabilities

Select a business purpose in the table to open its ordered function inputs, caller admission, record actions and report definitions. Each purpose may have several independently selectable configurations. Use the configuration number within the same purpose to cross-reference its [record definitions](../records/README.md). The [capability directory](../directory.md) links each activity to its worked business rules where available.

## How to read a function

- **Operation and subject** name the business action and, for a record-owned operation, its subject. Inputs appear in calling order. A required named input must be supplied by purpose. An optional input may be omitted. The two additional-input forms accept further positional values or named values. An empty list means the operation declares no caller-supplied inputs.
- **Default descriptors** distinguish an exact scalar or empty collection from a named business choice and a contextual default. Named choices use neutral identifiers. A contextual default must be resolved by the operating configuration, expression or environment. Distinguish an omitted input, an explicit empty value and a zero amount.
- **Caller admission** records public admission, explicit authentication, ordinary service admission or a configurable entry condition. The caller remains subject to record, company, role, ownership and operation-specific rights. A public entry point can require a valid payment confirmation, invitation or receipt of authority before changing anything. Request modes describe permitted invocation forms.
- **Record operations** identify direct uses of a named record, such as reading a value, preparing a new record, evaluating a permission, changing a field or submitting a transaction. They are possible effects across reachable conditions, not a required sequence for every request. “Load or prepare” leaves the persistence decision open. Related financial and stock effects follow the relevant posting contract.
- **Declarations** counts distinct registrations with the same represented configuration, input, admission and action details. Its default is one. An operation with a different input list or default retains its own entry.

## How to read a report

The subject is the primary record associated with the report. Reader roles are the granted roles declared for the report. Apply the caller's effective company, row and protected-field policies when selecting data. An omitted role list leaves authorization to the applicable report policy.

Each output or filter lists its name and semantic value kind. Filters also record whether selection is required. Record-reference entries may identify the target. Selectable filters and outputs come from known configuration or layout choices and can depend on the report arguments. An omitted output or filter list means its exact layout or criteria need a separate business description. A total-row flag requests an aggregate display. Background preparation is separate from the time to which balances or quantities refer.

The 250 purposes below account for **8,207 operation declarations** with 15,711 declared input positions and **605 reports**. Direct record actions are described for 4,693 operations. 582 reports declare reader roles, 468 have identified filters and 342 have identified output columns. These counts describe different properties and must not be added together.

| Business purpose | Operations | Reports | Contracts |
|---|---:|---:|---|
| Accommodation reservations | 592 | 0 | [Open dictionary](a-01.json) |
| Account balance feed reconciliation | 8 | 0 | [Open dictionary](a-02.json) |
| Accounting daybook migration and reversal | 24 | 0 | [Open dictionary](a-02.json) |
| Accounting master data migration | 39 | 1 | [Open dictionary](a-02.json) |
| Accounting system synchronization | 29 | 0 | [Open dictionary](a-02.json) |
| Advertising lead capture | 7 | 0 | [Open dictionary](a-02.json) |
| Analytical report design | 17 | 0 | [Open dictionary](a-02.json) |
| Analytical reporting | 57 | 0 | [Open dictionary](a-02.json) |
| Appointment capacity and coupons | 85 | 5 | [Open dictionary](a-02.json) |
| Argentine electronic invoicing | 5 | 0 | [Open dictionary](a-02.json) |
| Assisted business operations | 1 | 0 | [Open dictionary](a-02.json) |
| Assisted business record lookup | 9 | 1 | [Open dictionary](a-02.json) |
| Assisted operations approval | 503 | 1 | [Open dictionary](a-03.json) |
| Assisted text generation | 4 | 0 | [Open dictionary](a-03.json) |
| Attachment object storage | 8 | 0 | [Open dictionary](a-03.json) |
| Attachment routing by storage folder | 2 | 0 | [Open dictionary](a-03.json) |
| Attachment selection | 5 | 0 | [Open dictionary](a-03.json) |
| Attendance and overtime time sheets | 2 | 0 | [Open dictionary](a-03.json) |
| Attendance device collection | 2 | 0 | [Open dictionary](a-03.json) |
| Audience-specific alerts | 5 | 1 | [Open dictionary](a-03.json) |
| Australian accounting and tax | 18 | 0 | [Open dictionary](a-03.json) |
| Balance sheet reconciliation | 6 | 0 | [Open dictionary](b-01.json) |
| Bangladeshi value added tax invoices | 24 | 10 | [Open dictionary](b-01.json) |
| Bank account feed synchronization | 10 | 0 | [Open dictionary](b-01.json) |
| Bank messaging and account reconciliation | 41 | 0 | [Open dictionary](b-01.json) |
| Bank payout integration | 5 | 1 | [Open dictionary](b-01.json) |
| Barcode label printing | 18 | 0 | [Open dictionary](b-01.json) |
| Batch and document traceability | 5 | 0 | [Open dictionary](b-01.json) |
| Batch payments and remittance advice | 9 | 0 | [Open dictionary](b-01.json) |
| Billable time capture | 10 | 0 | [Open dictionary](b-01.json) |
| Biometric attendance and leave | 10 | 4 | [Open dictionary](b-01.json) |
| Biometric attendance device import | 15 | 0 | [Open dictionary](b-01.json) |
| British value added tax filing | 76 | 3 | [Open dictionary](b-01.json) |
| Brokerage statement accounting | 3 | 0 | [Open dictionary](b-01.json) |
| Bulk task unassignment | 1 | 0 | [Open dictionary](b-01.json) |
| Burundian electronic sales reporting | 7 | 9 | [Open dictionary](b-01.json) |
| Business messaging campaigns | 12 | 0 | [Open dictionary](b-01.json) |
| Business messaging dispatch | 23 | 1 | [Open dictionary](b-01.json) |
| Business messaging notifications | 12 | 0 | [Open dictionary](b-01.json) |
| Cargo bookings and container movements | 22 | 13 | [Open dictionary](c-01.json) |
| Carrier dispatch automation | 7 | 0 | [Open dictionary](c-01.json) |
| Carrier service and parcel booking | 12 | 0 | [Open dictionary](c-01.json) |
| Carrier tracking and shipment registration | 44 | 0 | [Open dictionary](c-01.json) |
| Cashbook and treasury categories | 1 | 2 | [Open dictionary](c-01.json) |
| Certificate-based document signing | 30 | 6 | [Open dictionary](c-01.json) |
| Cheque payment runs | 24 | 3 | [Open dictionary](c-01.json) |
| Collaborative diagramming | 17 | 0 | [Open dictionary](c-01.json) |
| Collaborative document spaces | 40 | 0 | [Open dictionary](c-01.json) |
| Collaborative knowledge publishing | 77 | 1 | [Open dictionary](c-01.json) |
| Combining document attachments | 2 | 0 | [Open dictionary](c-01.json) |
| Committee opening of supplier quotations | 3 | 0 | [Open dictionary](c-01.json) |
| Company-scoped navigation | 9 | 0 | [Open dictionary](c-01.json) |
| Compliance obligations and client cases | 228 | 26 | [Open dictionary](c-01.json) |
| Congregational care and events | 241 | 95 | [Open dictionary](c-02.json) |
| Consignment delivery management | 25 | 0 | [Open dictionary](c-02.json) |
| Construction quantities and budgets | 13 | 3 | [Open dictionary](c-02.json) |
| Contact data quality checks | 1 | 0 | [Open dictionary](c-02.json) |
| Contract dues and settlement | 5 | 0 | [Open dictionary](c-02.json) |
| Contribution points and reviews | 14 | 0 | [Open dictionary](c-02.json) |
| Control evidence and risk assessment | 55 | 2 | [Open dictionary](c-02.json) |
| Controlled credential sharing | 73 | 0 | [Open dictionary](c-02.json) |
| Controlled external file distribution | 15 | 0 | [Open dictionary](c-02.json) |
| Conversation campaigns and notes | 62 | 0 | [Open dictionary](c-02.json) |
| Conversation history and usage | 18 | 2 | [Open dictionary](c-02.json) |
| Conversational business record lookup | 18 | 0 | [Open dictionary](c-02.json) |
| Conversational messaging rules | 5 | 0 | [Open dictionary](c-02.json) |
| Counterparty due diligence | 9 | 0 | [Open dictionary](c-02.json) |
| Course delivery and learning assessment | 192 | 1 | [Open dictionary](c-03.json) |
| Customer messaging contacts | 6 | 0 | [Open dictionary](c-03.json) |
| Delivery charges and mobile money at tills | 59 | 1 | [Open dictionary](d-01.json) |
| Device-bound authentication | 59 | 0 | [Open dictionary](d-01.json) |
| Digital signage content | 2 | 0 | [Open dictionary](d-01.json) |
| Document clauses and templates | 8 | 0 | [Open dictionary](d-01.json) |
| Document email reminders | 5 | 0 | [Open dictionary](d-01.json) |
| Document event messaging | 2 | 0 | [Open dictionary](d-01.json) |
| Document intake and extraction | 24 | 1 | [Open dictionary](d-01.json) |
| Document layout design | 8 | 0 | [Open dictionary](d-01.json) |
| Document limits and usage quotas | 1 | 0 | [Open dictionary](d-01.json) |
| Document rendition on submission | 1 | 0 | [Open dictionary](d-01.json) |
| Document signing field mapping | 3 | 0 | [Open dictionary](d-01.json) |
| Earnest money deposit accounting | 6 | 0 | [Open dictionary](e-01.json) |
| Ecuadorian electronic invoicing | 56 | 0 | [Open dictionary](e-01.json) |
| Editorial publishing | 3 | 0 | [Open dictionary](e-01.json) |
| Egyptian electronic receipts and invoices | 17 | 1 | [Open dictionary](e-01.json) |
| Electronic invoice interchange | 30 | 2 | [Open dictionary](e-01.json) |
| Electronic invoice network delivery | 3 | 0 | [Open dictionary](e-01.json) |
| Email broadcast and delivery tracking | 4 | 0 | [Open dictionary](e-01.json) |
| Email delivery reporting | 1 | 1 | [Open dictionary](e-01.json) |
| Employee advance repayments | 2 | 0 | [Open dictionary](e-01.json) |
| Employee project assignment instructions | 12 | 0 | [Open dictionary](e-01.json) |
| European electronic invoice import | 12 | 0 | [Open dictionary](e-01.json) |
| Event-triggered conversational messaging | 2 | 0 | [Open dictionary](e-01.json) |
| Exchange rate synchronization | 3 | 0 | [Open dictionary](e-01.json) |
| Export duty rebate claims | 4 | 0 | [Open dictionary](e-01.json) |
| Export letters of credit | 8 | 0 | [Open dictionary](e-01.json) |
| External editorial publishing | 1 | 0 | [Open dictionary](e-01.json) |
| External storage routing | 1 | 0 | [Open dictionary](e-01.json) |
| Field workbook export | 3 | 0 | [Open dictionary](f-01.json) |
| Fiscal device end-of-day records | 1 | 0 | [Open dictionary](f-01.json) |
| Garment reservation and rental | 4 | 5 | [Open dictionary](g-01.json) |
| Gate compliance and discrepancies | 21 | 9 | [Open dictionary](g-01.json) |
| Gate dispatch and returns | 9 | 3 | [Open dictionary](g-01.json) |
| Geographic address hierarchy | 6 | 0 | [Open dictionary](g-01.json) |
| German accounting export | 1 | 1 | [Open dictionary](g-01.json) |
| Group appointments and availability | 27 | 0 | [Open dictionary](g-01.json) |
| Group financial reporting | 0 | 3 | [Open dictionary](g-01.json) |
| Holiday calendars | 2 | 0 | [Open dictionary](h-01.json) |
| Image-to-address transcription | 2 | 0 | [Open dictionary](i-01.json) |
| Import letters of credit | 12 | 0 | [Open dictionary](i-01.json) |
| Incoming material price controls | 11 | 2 | [Open dictionary](i-01.json) |
| Indian identity and signature verification | 2 | 0 | [Open dictionary](i-01.json) |
| Indian payroll | 24 | 6 | [Open dictionary](i-01.json) |
| Indian postal addresses | 4 | 0 | [Open dictionary](i-01.json) |
| Indonesian tax invoice import and export | 19 | 1 | [Open dictionary](i-01.json) |
| Installable mobile workspace | 6 | 0 | [Open dictionary](i-01.json) |
| Invoice image and document extraction | 3 | 0 | [Open dictionary](i-01.json) |
| Invoice payment links | 1 | 0 | [Open dictionary](i-01.json) |
| Invoice signing | 7 | 0 | [Open dictionary](i-01.json) |
| Job applicant résumé assessment | 7 | 0 | [Open dictionary](j-01.json) |
| Kenyan electronic tax reporting | 128 | 5 | [Open dictionary](k-01.json) |
| Kenyan fiscal device transmission | 4 | 0 | [Open dictionary](k-01.json) |
| Kenyan sales and workforce records | 18 | 23 | [Open dictionary](k-01.json) |
| Last sale price lookup | 1 | 0 | [Open dictionary](l-01.json) |
| Ledger and tax mapping synchronization | 74 | 0 | [Open dictionary](l-01.json) |
| Livestock activity and valuation | 9 | 8 | [Open dictionary](l-01.json) |
| Maker and checker audit reports | 0 | 1 | [Open dictionary](m-01.json) |
| Malaysian electronic invoicing | 10 | 3 | [Open dictionary](m-01.json) |
| Marketplace inquiry synchronization | 11 | 0 | [Open dictionary](m-01.json) |
| Meeting administration | 8 | 0 | [Open dictionary](m-01.json) |
| Metered utility and rental billing | 75 | 6 | [Open dictionary](m-01.json) |
| Mexican electronic invoice compliance | 20 | 1 | [Open dictionary](m-01.json) |
| Mobile business operations | 56 | 0 | [Open dictionary](m-01.json) |
| Mobile employee self-service | 302 | 0 | [Open dictionary](m-01.json) |
| Mobile employee workspace | 86 | 0 | [Open dictionary](m-01.json) |
| Mobile money collection | 45 | 4 | [Open dictionary](m-01.json) |
| Mobile record synchronization | 16 | 0 | [Open dictionary](m-01.json) |
| Multilevel production recipe design | 11 | 0 | [Open dictionary](m-01.json) |
| Multiple attachment storage destinations | 9 | 0 | [Open dictionary](m-01.json) |
| Nigerian electronic invoicing | 15 | 1 | [Open dictionary](n-01.json) |
| Obligatory charitable contribution accounting | 0 | 1 | [Open dictionary](o-01.json) |
| Offline till reconciliation | 158 | 6 | [Open dictionary](o-01.json) |
| Offsite backup management | 7 | 0 | [Open dictionary](o-01.json) |
| One-time identity challenges | 1 | 0 | [Open dictionary](o-01.json) |
| Online payment collection | 23 | 5 | [Open dictionary](o-01.json) |
| Outbound facsimile delivery | 1 | 0 | [Open dictionary](o-01.json) |
| Pakistani accounting workspace | 0 | 2 | [Open dictionary](p-01.json) |
| Pakistani electronic invoicing | 24 | 7 | [Open dictionary](p-01.json) |
| Participant messaging and conversation retention | 612 | 0 | [Open dictionary](p-01.json) |
| Party-specific item account selection | 2 | 0 | [Open dictionary](p-01.json) |
| Payment confirmation challenges | 4 | 0 | [Open dictionary](p-01.json) |
| Payment service routing | 0 | 1 | [Open dictionary](p-01.json) |
| Payment terminal transactions | 46 | 0 | [Open dictionary](p-01.json) |
| Payroll penalties and corrections | 5 | 0 | [Open dictionary](p-01.json) |
| Permission-scoped conversational assistance | 348 | 0 | [Open dictionary](p-01.json) |
| Personal notes and work items | 1 | 0 | [Open dictionary](p-01.json) |
| Personal work categorization | 12 | 0 | [Open dictionary](p-01.json) |
| Photo identification and tagging | 4 | 0 | [Open dictionary](p-01.json) |
| Piece-rate payroll pools | 4 | 0 | [Open dictionary](p-02.json) |
| Policy document and report assistance | 13 | 0 | [Open dictionary](p-02.json) |
| Portal presentation | 4 | 0 | [Open dictionary](p-02.json) |
| Portal sign-in links | 3 | 0 | [Open dictionary](p-02.json) |
| Product price lookup | 6 | 0 | [Open dictionary](p-02.json) |
| Product recommendations and featured items | 50 | 0 | [Open dictionary](p-02.json) |
| Product text translation | 14 | 0 | [Open dictionary](p-02.json) |
| Production job scheduling | 2 | 0 | [Open dictionary](p-02.json) |
| Production line stoppage and changeovers | 10 | 1 | [Open dictionary](p-02.json) |
| Project checklists and contacts | 13 | 0 | [Open dictionary](p-02.json) |
| Project documentation publishing | 41 | 0 | [Open dictionary](p-02.json) |
| Project member and field permissions | 43 | 7 | [Open dictionary](p-02.json) |
| Property inspections and occupancy | 44 | 21 | [Open dictionary](p-02.json) |
| Protected document rendition | 1 | 0 | [Open dictionary](p-02.json) |
| Public benefit scheme enrolment | 28 | 39 | [Open dictionary](p-02.json) |
| Public forms and team ownership | 36 | 0 | [Open dictionary](p-02.json) |
| Public search discovery | 1 | 1 | [Open dictionary](p-02.json) |
| Purchase tax statement reconciliation | 12 | 2 | [Open dictionary](p-02.json) |
| Quotation and proposal synchronization | 9 | 0 | [Open dictionary](q-01.json) |
| Reception access and room booking | 17 | 7 | [Open dictionary](r-01.json) |
| Recipient template message campaigns | 4 | 0 | [Open dictionary](r-01.json) |
| Recurring item subscriptions | 1 | 0 | [Open dictionary](r-01.json) |
| Regional financial statement templates | 5 | 5 | [Open dictionary](r-01.json) |
| Restaurant orders and station routing | 162 | 16 | [Open dictionary](r-01.json) |
| Restaurant till settlement import | 2 | 3 | [Open dictionary](r-01.json) |
| Retail checkout | 80 | 0 | [Open dictionary](r-01.json) |
| Retail checkout permissions and payment links | 66 | 0 | [Open dictionary](r-01.json) |
| Reusable form presets | 6 | 0 | [Open dictionary](r-01.json) |
| Role and grant duplication | 20 | 0 | [Open dictionary](r-01.json) |
| Role assignment administration | 1 | 0 | [Open dictionary](r-01.json) |
| Role grant administration | 2 | 0 | [Open dictionary](r-01.json) |
| Role-restricted knowledge pages | 9 | 0 | [Open dictionary](r-01.json) |
| Sales inquiry and contact synchronization | 9 | 0 | [Open dictionary](s-01.json) |
| Sales order warehouse selection | 1 | 0 | [Open dictionary](s-01.json) |
| Saudi electronic invoicing | 43 | 7 | [Open dictionary](s-01.json) |
| Saudi invoice signing credentials | 46 | 6 | [Open dictionary](s-01.json) |
| Scannable document verification | 22 | 0 | [Open dictionary](s-01.json) |
| Scheduled report distribution | 36 | 0 | [Open dictionary](s-01.json) |
| Service desk management | 142 | 5 | [Open dictionary](s-01.json) |
| Service operation directory | 1 | 0 | [Open dictionary](s-01.json) |
| Session activity and access notices | 2 | 0 | [Open dictionary](s-01.json) |
| Shared file workspaces | 68 | 0 | [Open dictionary](s-01.json) |
| Shared spreadsheet synchronization | 3 | 0 | [Open dictionary](s-01.json) |
| Shared whiteboards | 1 | 0 | [Open dictionary](s-01.json) |
| Shift allocation imports | 4 | 0 | [Open dictionary](s-01.json) |
| Short links and scannable destinations | 1 | 0 | [Open dictionary](s-01.json) |
| Singapore goods and services tax | 4 | 3 | [Open dictionary](s-01.json) |
| Small enterprise supplier registration | 0 | 1 | [Open dictionary](s-01.json) |
| South African filing and privacy obligations | 18 | 3 | [Open dictionary](s-01.json) |
| South African injury and payroll reporting | 62 | 9 | [Open dictionary](s-01.json) |
| Spanish value added tax register | 16 | 0 | [Open dictionary](s-01.json) |
| Sri Lankan accounting and tax | 0 | 2 | [Open dictionary](s-01.json) |
| Staffing projects and labour costs | 14 | 8 | [Open dictionary](s-01.json) |
| Statement rule reconciliation | 26 | 0 | [Open dictionary](s-01.json) |
| Stone lot picking and packing | 25 | 2 | [Open dictionary](s-01.json) |
| Storage utilization and query performance | 7 | 1 | [Open dictionary](s-01.json) |
| Storefront availability synchronization | 21 | 1 | [Open dictionary](s-02.json) |
| Storefront order synchronization | 9 | 0 | [Open dictionary](s-02.json) |
| Storefront presentation | 6 | 0 | [Open dictionary](s-02.json) |
| Storefront tax and warehouse mapping | 7 | 0 | [Open dictionary](s-02.json) |
| Structured trade invoice generation | 9 | 0 | [Open dictionary](s-02.json) |
| Support portal and party address capture | 5 | 0 | [Open dictionary](s-02.json) |
| Support ticket and engineering issue synchronization | 18 | 7 | [Open dictionary](s-02.json) |
| Swiss accounting export | 2 | 0 | [Open dictionary](s-02.json) |
| Swiss hours and tax reporting | 4 | 0 | [Open dictionary](s-02.json) |
| Tanzanian maintenance and inspection | 175 | 124 | [Open dictionary](t-01.json) |
| Task board rules and checklists | 4 | 1 | [Open dictionary](t-01.json) |
| Team communication channels | 127 | 0 | [Open dictionary](t-01.json) |
| Team communication integration | 7 | 0 | [Open dictionary](t-01.json) |
| Team discussions and project collaboration | 94 | 0 | [Open dictionary](t-01.json) |
| Technology asset management | 22 | 0 | [Open dictionary](t-01.json) |
| Tenant and team administration | 24 | 0 | [Open dictionary](t-01.json) |
| Text message gateway | 5 | 0 | [Open dictionary](t-01.json) |
| Thai accounting and tax | 23 | 5 | [Open dictionary](t-02.json) |
| Till card payment reconciliation | 15 | 0 | [Open dictionary](t-02.json) |
| Till customer messaging | 11 | 0 | [Open dictionary](t-02.json) |
| Till fiscal transaction certification | 22 | 0 | [Open dictionary](t-02.json) |
| Till opening and closing | 35 | 0 | [Open dictionary](t-02.json) |
| Ugandan electronic tax reporting | 27 | 0 | [Open dictionary](u-01.json) |
| United Arab Emirates electronic invoicing | 23 | 2 | [Open dictionary](u-01.json) |
| United States payroll disbursement | 51 | 9 | [Open dictionary](u-01.json) |
| Visitor conversion and account activation | 14 | 0 | [Open dictionary](v-01.json) |
| Voice agent and call records | 21 | 0 | [Open dictionary](v-01.json) |
| Warehouse pallet capacity and pick faces | 84 | 0 | [Open dictionary](w-01.json) |
| Web content and enquiry management | 212 | 0 | [Open dictionary](w-01.json) |
| Web page composition | 96 | 0 | [Open dictionary](w-01.json) |
| Workforce administration | 23 | 3 | [Open dictionary](w-01.json) |
| Working time and break policies | 7 | 2 | [Open dictionary](w-01.json) |
| Workplace facial attendance | 6 | 1 | [Open dictionary](w-01.json) |
| Workspace presentation | 35 | 0 | [Open dictionary](w-01.json) |
| Workspace presentation preferences | 35 | 0 | [Open dictionary](w-01.json) |
| Workspace sound and theme preferences | 24 | 0 | [Open dictionary](w-01.json) |
| Zambian fiscal inventory reporting | 12 | 0 | [Open dictionary](z-01.json) |
