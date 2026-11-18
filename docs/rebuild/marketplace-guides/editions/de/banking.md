# Zahlungsverkehr und Banken

[English](../en/banking.md) · [Afrikaans](../af/banking.md) · Deutsch · [简体中文](../zh-Hans/banking.md)

[Alle Themen](README.md)

## cheque

Beim Einreichen der Quittung entsteht der Kundenscheck, und ein Einreichungsbeleg fasst geeignete Schecks für die Bank zusammen. Der untersuchte Abgleich sucht den eingereichten Scheck anhand der Referenz und benötigt eine verknüpfte Buchung, bevor er Einlösung oder Rückgabe erfasst.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-cheque-approval-and-collection) · [Quellenbelege](../../apps/cheque.md)

## IPCONNEX Stripe Payment

Laut Produkteintrag lässt sich eine Rechnung bezahlen, sobald Stripe und die Zahlungsdaten des Kunden eingerichtet sind. Der historische öffentliche Quellstand verwendet die gespeicherte Zahlungsmethode und die Rechnungswährung, fordert einen PaymentIntent bei Stripe an und erstellt einen Zahlungsbeleg mit Rechnungszuordnung; eine tatsächliche Abrechnung auf einem installierten System wurde damit nicht nachgewiesen.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-saved-payment-method-collections) · [Quellenbelege](../../apps/ipconnex_stripe_payment.md)

## PDC Cheque Management

Nach Angaben des Anbieters entsteht beim Eingang eines Kundenschecks oder bei der Ausstellung eines Lieferantenschecks eine Zahlungsbuchung auf dem vorgesehenen Zwischenkonto. In der öffentlichen Quellkopie mit Verweis auf den Anbieter erzeugt die Einzahlung einen Bankbeleg, auf dem bei der Einlösung das Einlösungsdatum erfasst wird.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-post-dated-cheque-settlement) · [Quellenbelege](../../apps/pdc_cheque_management.md)

## ProCredit Bank Statement Processing

Der Anbieter beschreibt den Import von CSV-Kontoauszügen der ProCredit Bank in Bosnien und Herzegowina mit Prüfung auf doppelte Referenzen. Die Bildschirmfotos zeigen eine Importvorschau mit Datum, Einzahlung, Auszahlung, Referenz und Beschreibung sowie anschließend die noch nicht abgeglichenen Bankbewegungen.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-bank-statement-import-and-duplicate-review) · [Quellenbelege](../../apps/procreditbank.md)

## Treasury Entry

Die Bildschirmfotos des Anbieters zeigen in der Kasse je Zahlungsart ein eigenes Konto für Verbindlichkeiten und eines für Forderungen. Beim Kasseneintrag kann der Sachbearbeiter Konto und Betrag je Zeile eingeben oder die geschäftspartnerbezogene Erfassung wählen, offene Rechnungen abrufen und Beträge zuordnen.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-treasury-transaction-register) · [Quellenbelege](../../apps/safe_entry.md)

## Sanpra Easypay

Die Produktbeschreibung nennt Zahlungseingänge und Auszahlungen über die ICICI Bank. Bei Lieferantenzahlungen werden laut Anbieter Zahlungsbelege abgerufen, als Sammelauftrag per Einmalpasswort freigegeben und anhand der Bankmeldungen nachverfolgt. Unterstützt werden RTGS und NEFT.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-supplier-payment-batch-authorization) · [Quellenbelege](../../apps/sanpra_easypay.md)

## Stripe2 Payment Integration

Nachdem die Kontaktperson des Unternehmens ihre E-Mail-Adresse bestätigt und das Stripe-Konto autorisiert hat, richtet der Händler die Online- und Offline-Zahlungsarten ein. Eine eingereichte Zahlungsanforderung kann die Online-Kasse öffnen oder für eine wiederkehrende Zahlung auf ein gespeichertes Zahlungsmittel zugreifen, während an der Kasse ein registriertes Terminal zur Verfügung steht.

[Ablauf und Prüffall](../../../../capabilities/guides/de/banking.md#workflow-online-and-terminal-payment-collection) · [Quellenbelege](../../apps/stripe2.md)
