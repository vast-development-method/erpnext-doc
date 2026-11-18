# Analytics, AI and calendars

English · [Afrikaans](../af/data.md) · [Deutsch](../de/data.md) · [简体中文](../zh-Hans/data.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## BigQuery Connector

Export selected ERP fields to BigQuery and resume interrupted transfers from a confirmed checkpoint.

**Documented workflow**

The publisher’s export form maps a source table to a named destination, illustrated by tabUser mapped to user, and lets the operator choose columns and a filter. The incremental controls show the interval, last synchronization time, last synchronized ID and scheduler lock.

**Proposed acceptance example**

INV-001 and INV-002 share a modification timestamp and the export page size is one. The job stops after the first write before confirming its cursor, then restarts from a German interface. The destination contains exactly one row for each invoice ID. Translated captions never rename destination columns or change source row keys.

[Detailed profile in English](../../apps/frappe_bigquery.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## InstaGPT

Open a chat from the ERP navigation bar and send a message in the language you choose.

**Documented workflow**

Brandimic has a System Manager or Administrator configure the key, model and a temperature on a 0–200 scale before staff send messages from the navigation-bar chat. OpenAI documents a 0–2 scale for the Chat Completions temperature parameter; the app's conversion and endpoint remain unverified.

**Proposed acceptance example**

A user composing Chinese text has an active input-method composition in a German chat panel. Press Enter to confirm the character, finish the sentence and then explicitly send. Composition does not dispatch a turn; explicit send creates exactly one message with the composed text. The German UI and the requested answer language do not alter the user's original Chinese message.

[Detailed profile in English](../../apps/instagpt.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/instagpt)

## Islamic Calendar

Enter a date in the Hijri calendar and verify the same civil day in the Gregorian calendar.

**Documented workflow**

Kanak describes a Hijri date picker and two-way switching with Gregorian dates in ERP forms. A public copy credited to Kanak stores display and picker formats separately and uses a bundled Umm al-Qura month-start table for conversion.

**Proposed acceptance example**

The calendar converter uses the month-start table in the cited historical copy. Enter 1448-06-08 AH, switch to Gregorian, reopen the field and switch back. The canonical date is 2026-11-18 and the original Hijri day is restored. Changing language or numeral style does not change the selected day or calendar policy.

[Detailed profile in English](../../apps/islamic_calendar.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/islamic_calendar)

## Nepali Calendar

Enter a date in the Nepali calendar and find the same record by its Gregorian date.

**Documented workflow**

Kanak’s guide shows a user selecting a Nepali date in a Date field and switching to its Gregorian equivalent in the same form. The publisher lists sales, purchasing, HR and accounting among the areas using the picker.

**Proposed acceptance example**

A purchase record is entered with 1 Baisakh 2081. A different user filters on Gregorian date 2024-04-13 and changes the display language. The filter returns the same record and switching the calendar back restores 1 Baisakh 2081. Language, numeral style and calendar preferences never change the stored civil day.

[Detailed profile in English](../../apps/nepali_calendar.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/nepali_calendar)

## ChatNext

Ask an ERP question in one language and request an answer in another while preserving the original conversation.

**Documented workflow**

The listing describes a user asking a contextual ERP question. A public historical copy stores the user’s message under a conversation session, sends it with conversation history and route context to a separate service, and records the returned answer as a bot message.

**Proposed acceptance example**

A German-interface user may read an invoice and its outstanding amount. The user asks about that invoice in Afrikaans and requests an Afrikaans answer. The reply uses Afrikaans, cites the source field, preserves the original question and leaves the invoice unchanged. Language choice cannot broaden the user’s access to invoices or private chat history.

[Detailed profile in English](../../apps/nextai.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/nextai)
