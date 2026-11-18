# Zahlungsverkehr und Banken

[English](../en/banking.md) · [Afrikaans](../af/banking.md) · Deutsch · [简体中文](../zh-Hans/banking.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## cheque

Verfolgen Sie jeden Scheck vom Eingang oder der Ausstellung bis zur Einlösung oder Rückgabe und gleichen Sie ihn mit Buchung und Bankumsatz ab.

**Dokumentierter Ablauf**

Beim Einreichen der Quittung entsteht der Kundenscheck, und ein Einreichungsbeleg fasst geeignete Schecks für die Bank zusammen. Der untersuchte Abgleich sucht den eingereichten Scheck anhand der Referenz und benötigt eine verknüpfte Buchung, bevor er Einlösung oder Rückgabe erfasst.

**Vorgeschlagener Abnahmetest**

Bei einer Freigabegrenze von 1.000 muss ein eingereichter Scheck über genau 1.000 auch in einer neuen Sitzung auf Freigabe warten, ohne dass schon eine Buchung vorliegt. Die Freigabe durch die Buchhaltungsleitung erzeugt genau eine Buchung, und arabische und englische Belege zeigen dieselbe Schecknummer, Freigabe und Summe.

[Ausführliches Profil auf Englisch](../../apps/cheque.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/cheque)

## IPCONNEX Stripe Payment

Ziehen Sie den offenen Betrag einer Ausgangsrechnung über Stripe ein und gleichen Sie die bestätigte Zahlung mit dem offenen Posten ab.

**Dokumentierter Ablauf**

Laut Produkteintrag lässt sich eine Rechnung bezahlen, sobald Stripe und die Zahlungsdaten des Kunden eingerichtet sind. Der historische öffentliche Quellstand verwendet die gespeicherte Zahlungsmethode und die Rechnungswährung, fordert einen PaymentIntent bei Stripe an und erstellt einen Zahlungsbeleg mit Rechnungszuordnung; eine tatsächliche Abrechnung auf einem installierten System wurde damit nicht nachgewiesen.

**Vorgeschlagener Abnahmetest**

Ein französischsprachiger Zahler sendet denselben Einzugsauftrag für eine englische Rechnung mit 40 EUR Restbetrag zweimal; verarbeiten Sie auch die Erfolgsmeldung des Zahlungsdienstes zweimal. Genau eine Belastung und eine Zuordnung über 40 EUR gleichen die Rechnung aus; die Sprache der Quittung ändert weder die Beteiligten noch Referenz, Währung oder Betrag.

[Ausführliches Profil auf Englisch](../../apps/ipconnex_stripe_payment.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/ipconnex_stripe_payment)

## PDC Cheque Management

Verfolgen Sie einen vordatierten Scheck vom Eingang oder der Ausstellung bis zur Einzahlung, Einlösung oder Rückgabe.

**Dokumentierter Ablauf**

Nach Angaben des Anbieters entsteht beim Eingang eines Kundenschecks oder bei der Ausstellung eines Lieferantenschecks eine Zahlungsbuchung auf dem vorgesehenen Zwischenkonto. In der öffentlichen Quellkopie mit Verweis auf den Anbieter erzeugt die Einzahlung einen Bankbeleg, auf dem bei der Einlösung das Einlösungsdatum erfasst wird.

**Vorgeschlagener Abnahmetest**

Buchen Sie Scheck 00072 über 400,00 auf die offene Kundenrechnung, zahlen Sie ihn ein und bestätigen Sie die Einlösung zweimal mit derselben Referenz. Der Bankbestand steigt einmal um 400,00, das Zwischenkonto steht wieder auf null und beide Sprachfassungen zeigen dieselben Belegnummern.

[Ausführliches Profil auf Englisch](../../apps/pdc_cheque_management.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management)

## ProCredit Bank Statement Processing

Importieren Sie einen CSV-Kontoauszug der ProCredit Bank in Bosnien und Herzegowina und prüfen Sie doppelte Transaktionsreferenzen vor dem Abgleich.

**Dokumentierter Ablauf**

Der Anbieter beschreibt den Import von CSV-Kontoauszügen der ProCredit Bank in Bosnien und Herzegowina mit Prüfung auf doppelte Referenzen. Die Bildschirmfotos zeigen eine Importvorschau mit Datum, Einzahlung, Auszahlung, Referenz und Beschreibung sowie anschließend die noch nicht abgeglichenen Bankbewegungen.

**Vorgeschlagener Abnahmetest**

Importieren Sie die Bankreferenz 00038 mit 1.234,50 zweimal und danach mit 1.234,55. Genau eine Transaktion wird gebucht, die identische Zeile als Duplikat verknüpft und der abweichende Betrag zur Prüfung vorgelegt. Ein Sprachwechsel ändert weder die führenden Nullen der Transaktionsreferenz noch die Auslegung des Zahlenformats der Quelldatei.

[Ausführliches Profil auf Englisch](../../apps/procreditbank.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/procreditbank)

## Treasury Entry

Erfassen Sie Ein- und Auszahlungen per Bargeld oder Scheck im Kassenbuch und prüfen Sie die Einträge für einzelne Geschäftspartner.

**Dokumentierter Ablauf**

Die Bildschirmfotos des Anbieters zeigen in der Kasse je Zahlungsart ein eigenes Konto für Verbindlichkeiten und eines für Forderungen. Beim Kasseneintrag kann der Sachbearbeiter Konto und Betrag je Zeile eingeben oder die geschäftspartnerbezogene Erfassung wählen, offene Rechnungen abrufen und Beträge zuordnen.

**Vorgeschlagener Abnahmetest**

Erfassen Sie in derselben Kasse einen Geldeingang von 250,00 mit Geschäftspartner und eine Auszahlung von 75,00 ohne Geschäftspartner. Deutsch und Afrikaans zeigen jeweils eine Nettozunahme von 175,00. Der Geschäftspartnerfilter lässt nur den Eingang von 250,00 übrig.

[Ausführliches Profil auf Englisch](../../apps/safe_entry.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/safe_entry)

## Sanpra Easypay

Autorisieren Sie einen Sammelauftrag für Lieferantenzahlungen über ICICI und gleichen Sie jeden Posten mit der Bankrückmeldung ab.

**Dokumentierter Ablauf**

Die Produktbeschreibung nennt Zahlungseingänge und Auszahlungen über die ICICI Bank. Bei Lieferantenzahlungen werden laut Anbieter Zahlungsbelege abgerufen, als Sammelauftrag per Einmalpasswort freigegeben und anhand der Bankmeldungen nachverfolgt. Unterstützt werden RTGS und NEFT.

**Vorgeschlagener Abnahmetest**

Verarbeiten Sie dieselbe Bankantwort für einen freigegebenen Sammelauftrag mit einer bestätigten und einer abgelehnten Lieferantenzahlung zweimal. Nur der bezahlte Lieferant erhält ein deutsches Zahlungsavis, der abgelehnte Posten bleibt offen und Hindi- sowie englischsprachige Mitarbeitende sehen dieselben Bankreferenzen und den ursprünglichen Ablehnungsgrund.

[Ausführliches Profil auf Englisch](../../apps/sanpra_easypay.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/sanpra_easypay)

## Stripe2 Payment Integration

Wickeln Sie eine Zahlung online, über ein gekoppeltes Terminal oder für eine wiederkehrende Zahlungsanforderung ab und gleichen Sie sie mit der Rechnung ab.

**Dokumentierter Ablauf**

Nachdem die Kontaktperson des Unternehmens ihre E-Mail-Adresse bestätigt und das Stripe-Konto autorisiert hat, richtet der Händler die Online- und Offline-Zahlungsarten ein. Eine eingereichte Zahlungsanforderung kann die Online-Kasse öffnen oder für eine wiederkehrende Zahlung auf ein gespeichertes Zahlungsmittel zugreifen, während an der Kasse ein registriertes Terminal zur Verfügung steht.

**Vorgeschlagener Abnahmetest**

Eine französischsprachige Person begleicht eine Rechnung über 35,70 EUR. Geht die Bestätigung zweimal ein, wird der Betrag nur einmal zugeordnet und die deutschsprachige Kassenkraft sieht dieselbe beglichene Rechnung.

[Ausführliches Profil auf Englisch](../../apps/stripe2.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/stripe2)
