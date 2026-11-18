# ERPNext IndiaMART Integration

## Publisher evidence

Sanskar Technolab lists versions 14 and 15. An administrator enables the integration and enters the IndiaMART service URL, authorization key and registered mobile number. The publisher describes a five-minute refresh and a historical fetch with start and end dates covering seven days. Users filter inquiries by buyer, contact, product and status. The dashboard groups them by period and by status, including repeat inquiries and contact suppression. The product can update inquiry type from customer behaviour and create a lead on conversion. The vendor identifies the CRM integration menu as the place to generate the key. [Marketplace description](https://cloud.frappe.io/marketplace/apps/indiamart) · [Publisher setup and product guide](https://sanskartechnolab.com/erpnext-apps-marketplace/erpnext-indiamart-integration) · [Listed source](https://github.com/Sanskar-Technolab/indiamart_app)

## Proposed rebuild contract

| Operation | Input, state and result |
|---|---|
| Retrieve a window | Scope by tenant and seller account. Record window boundaries and provider time zone, identify each inquiry by its upstream ID within the account, preserve original contact details and product description. Record the last completed window only after its rows persist. |
| Reconcile the result | A replay updates the same inquiry. A second upstream ID from the same buyer remains a second inquiry and can receive a repeat classification. A changed email address is not a reason to create another copy of the first inquiry. |
| Convert | An authorized CRM user requests conversion for one inquiry. Atomically return its linked lead or create one and save that link. Keep the original upstream ID and the status history for reporting. |
| Report | Aggregate inquiries by event date in the seller's reporting zone and by stable status code. Counts of inquiries and converted leads answer different questions. Keep the contact-suppression reason through subsequent imports. |

## Multilingual operation and acceptance

- During overlapping scheduled and historical imports, inquiry INQ-47 containing the Hindi product name “कपड़ा” appears twice. The expected result is one inquiry. The French-speaking sales user sees localized filters and can search the original product text. Language detection must not change buyer identity, email or telephone.
- Two agents request conversion of INQ-47 using different UI languages. Both receive the same lead ID and the dashboard shows one converted inquiry. Source messages stay in their original script with an optional separately identified translation.
- If authentication fails halfway through a historical fetch, retain previously committed rows and the last completed boundary, return a localizable failure code, and keep the key out of user messages. Replay the window after credential recovery.
- When the account marks a buyer as do not contact, a same-buyer inquiry in a second language stays attributable to that buyer. A change in localized display wording cannot clear the suppression decision.

## Remaining evidence

The exact upstream payload, behaviour-to-type mapping, provider time-window semantics, version-specific data model and translation catalogs require a source revision or authorized provider replay. The deduplication key, transactional boundary and permission policy above are proposed.
