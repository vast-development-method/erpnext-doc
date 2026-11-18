# Sales, shops and restaurants

English · [Afrikaans](../af/sales.md) · [Deutsch](../de/sales.md) · [简体中文](../zh-Hans/sales.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## B2B Marketing

Build a calling campaign from selected contacts, check the do-not-call list and assign eligible calls to agents.

**Documented workflow**

The campaign manager filters contacts and defines a calling sequence and quality policy in Campaign Designer. Calls are scheduled across the agent pool, managers can review recordings, and campaign services can be billed through ERP invoicing.

**Proposed acceptance example**

A contact is selected for a campaign and joins the do-not-call list before dispatch. The scheduler attempts to assign the call with a different script language. The attempt is suppressed, no provider call is made and no billable unit is recorded. Suppression follows the dialling identity and applies to every script language.

[Detailed profile in English](../../apps/b2b_marketing.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/b2b_marketing)

## Follow Up

Schedule condition-based follow-ups and deliver due reminders in the responsible person’s language.

**Documented workflow**

The publisher’s collections screens show a second-level reminder after ten days, with a responsible caller, email and SMS options. A separate workspace records payment commitments and compares them with payments received.

**Proposed acceptance example**

A quotation sent Friday at 09:00 is due for follow-up two working days later in Windhoek, without an intervening holiday. The owner opens the task in Afrikaans and the manager views it in German. They see one follow-up due on Tuesday at 09:00 Windhoek time. Language changes the captions. The business calendar and zone determine the deadline.

[Detailed profile in English](../../apps/follow_up.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/follow_up)

## ERPNext IndiaMART Integration

Import IndiaMART inquiries, track their status and convert a selected inquiry into a lead.

**Documented workflow**

Sanskar’s setup guide has an administrator enable the connector with the IndiaMART service URL, authorization key and registered mobile number. Inquiries refresh every five minutes according to the publisher; staff can also fetch a seven-day historical window, review inquiry status and convert an inquiry into a lead.

**Proposed acceptance example**

The scheduled fetch and a historical window overlap for seller A and inquiry INQ-47. Import both windows, then request conversion in two different UI languages. Exactly one inquiry belongs to seller A and both conversion requests return the same lead ID. The original Hindi product name and provider inquiry ID remain unchanged.

[Detailed profile in English](../../apps/indiamart.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/indiamart)

## Insightly

Trace orders from a customer or purchases from a supplier from dashboard totals to the underlying documents.

**Documented workflow**

The publisher describes date-filtered customer and supplier dashboards with counts, amounts and drill-down to transactions. In the pinned public copy, submitted orders use the transaction date, invoices use the posting date and payment requests use the creation timestamp; invoice totals also distinguish outstanding from paid amounts.

**Proposed acceptance example**

Two visible submitted orders for one customer total EUR 140; a third order is a draft. Open the submitted-order count and drill down under the same period filter. The dashboard shows 2 and EUR 140, and the drill-down returns exactly the two submitted order IDs. Changing the display language leaves the amount, filter and document identities unchanged.

[Detailed profile in English](../../apps/insightly.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/insightly)

## Lumen Restaurants

Manage a table order across kitchen rounds and settle the final bill through the outlet's till.

**Documented workflow**

Lumen describes waiters keeping a table order open over several kitchen rounds, with free add-ons recorded as instructions and paid add-ons billed separately on the final POS Invoice. Its public copy checks whether the table already has an open order; the publisher advertises both English and Arabic in the restaurant screens, booking page and receipts.

**Proposed acceptance example**

A dish costs 60 and a billed add-on costs 5 before tax, with a free kitchen instruction. Dispatch the round twice with the same dispatch ID and pay the final order. One kitchen ticket is produced and one POS Invoice contains billable lines totaling 65 before tax. Arabic kitchen text and English checkout reference the same choice IDs and line amounts.

[Detailed profile in English](../../apps/lumen_restaurants.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/lumen_restaurants)

## LumenPOS

Run a retail shift in the cashier’s language and reconcile sales queued during a network outage.

**Documented workflow**

According to the guide, a cashier opens a shift, scans items and takes payment. The till tracks each eligible offline sale until the server acknowledges it, displays the invoice number or rejection reason, and requires queued sales to upload before closing the shift.

**Proposed acceptance example**

An Arabic-speaking cashier has one eligible offline sale for two units. The device switches to German and retries after losing the upload acknowledgement. There is one posted invoice, one stock movement for two units and a German upload status referencing that invoice. The client sale key, posted quantities and original receipt language survive the locale switch.

[Detailed profile in English](../../apps/lumenpos.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/lumenpos)

## ONDC Seller App

Publish a seller catalog for the ONDC network and reconcile buyer confirmations with ERP orders.

**Documented workflow**

mytra.money describes a version 14 prerelease for Frappe Cloud sellers offering goods or services through ONDC. The publisher presents self-hosted availability as planned and does not identify the retail protocol version or the messages the app handles.

**Proposed acceptance example**

An English/Hindi catalog exposes one SKU and one two-unit order confirmation. The network repeats the identical confirmation after the operator changes language. The gateway returns the same outcome and a single order reserves two units. Catalog text may vary; seller IDs, SKU, correlation IDs and signed messages remain identical.

[Detailed profile in English](../../apps/ondc_seller_app.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/ondc_seller_app)

## Retail Suite

Scan tracked items, complete sales or returns and reconcile each payment method when closing a shift.

**Documented workflow**

The publisher describes Arabic and English POS screens and shift closing by payment method. A historical fork computes each closing difference as counted minus expected and supplies an English/Urdu POS toggle with English fallback, followed by the message key when an English entry is also missing.

**Proposed acceptance example**

A shift opens with cash of 100.00, takes 200.00 in cash and 50.00 by card, and refunds 30.00 in cash. Close the shift with counted cash of 268.00 and card movement of 50.00. Expected cash is 270.00, the cash shortage is 2.00 and the card difference is zero. Arabic and English closing screens refer to the same shift, method identifiers, amounts and discrepancy.

[Detailed profile in English](../../apps/retail.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/retail)

## Sajha Menu

Send a table order to the kitchen and bar and settle the guest bill against the same visit.

**Documented workflow**

The publisher lists QR, tablet and POS ordering with table management and billing. In a public copy attributed to Tuna, an order service separates food from bar items by category, issues the corresponding tickets and adds the quantities to the table order.

**Proposed acceptance example**

A restaurant visit has two portions of a food item and one drink, each assigned to the corresponding preparation station. Submit the Nepali guest order twice with the same submission key. The English-speaking kitchen gets two portions, the German-speaking bar gets one drink, and the bill contains exactly three units. Station and item codes, quantities, modifiers and prices survive language changes. Preserve any original guest note.

[Detailed profile in English](../../apps/sajha_menu.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/sajha_menu)

## Sales AI

Review an assistant’s proposed quotation reminder in the recipient’s language and approve the exact text before dispatch.

**Documented workflow**

The publisher describes sales staff querying quotations, orders and invoices, and a separate portal assistant for each customer’s own documents. Playbooks can run on a schedule or document event, support dry runs and approval pauses, and expose runs and action logs for review.

**Proposed acceptance example**

A German-speaking manager selects an ageing quotation for an Afrikaans-speaking customer. Run a dry preview, approve the corresponding live reminder, replay the scheduler, then edit the originally approved wording. The preview sends nothing, one approved message is delivered, and the revised wording requires a new approval. Approval binds to the recipient-language content, record and recipient. Changing the manager’s interface language cannot authorize a different message.

[Detailed profile in English](../../apps/sales_ai.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/sales_ai)
