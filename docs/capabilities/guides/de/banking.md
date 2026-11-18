# Bankwesen und Zahlungsverkehr

## Verfolgen Sie jeden Scheck vom Eingang oder der Ausstellung bis zur Einlösung oder Rückgabe und gleichen Sie ihn mit Buchung und Bankumsatz ab

<a id="workflow-cheque-approval-and-collection"></a>

Aus dem Eingang den Kundenscheck anlegen, geeignete Schecks auf einem Einzahlungsbeleg bündeln und das Bankergebnis mit Scheck und Buchung abgleichen.

Bei einer Freigabegrenze von 1.000 muss ein eingereichter Scheck über genau 1.000 auch in einer neuen Sitzung auf Freigabe warten, ohne dass schon eine Buchung vorliegt. Die Freigabe durch die Buchhaltungsleitung erzeugt genau eine Buchung, und arabische und englische Belege zeigen dieselbe Schecknummer, Freigabe und Summe.

[English](../banking.md#cheque-approval-and-collection) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#cheque).

## Ziehen Sie den offenen Betrag einer Ausgangsrechnung über einen Zahlungsdienst ein und gleichen Sie die bestätigte Zahlung mit dem offenen Posten ab

<a id="workflow-saved-payment-method-collections"></a>

Mit dem autorisierten gespeicherten Zahlungsmittel in Rechnungswährung einziehen. Nach Bestätigung den Eingang der offenen Rechnung zuordnen und die Zahlungsreferenz bewahren.

Ein französischsprachiger Zahler sendet denselben Einzugsauftrag für eine englische Rechnung mit 40 EUR Restbetrag zweimal; verarbeiten Sie auch die Erfolgsmeldung des Zahlungsdienstes zweimal. Genau eine Belastung und eine Zuordnung über 40 EUR gleichen die Rechnung aus; die Sprache der Quittung ändert weder die Beteiligten noch Referenz, Währung oder Betrag.

[English](../banking.md#saved-payment-method-collections) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#ipconnex-stripe-payment).

## Verfolgen Sie einen vordatierten Scheck vom Eingang oder der Ausstellung bis zur Einzahlung, Einlösung oder Rückgabe

<a id="workflow-post-dated-cheque-settlement"></a>

Den Scheck auf dem zugehörigen Zwischenkonto erfassen. Die Einreichung erzeugt eine Bankbuchung, an der anschließend das Einlösungsdatum geführt wird.

Buchen Sie Scheck 00072 über 400,00 auf die offene Kundenrechnung, zahlen Sie ihn ein und bestätigen Sie die Einlösung zweimal mit derselben Referenz. Der Bankbestand steigt einmal um 400,00, das Zwischenkonto steht wieder auf null und beide Sprachfassungen zeigen dieselben Belegnummern.

[English](../banking.md#post-dated-cheque-settlement) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#pdc-cheque-management).

## Importieren Sie einen CSV-Kontoauszug einer Bank in Bosnien und Herzegowina und prüfen Sie doppelte Transaktionsreferenzen vor dem Abgleich

<a id="workflow-bank-statement-import-and-duplicate-review"></a>

Das CSV-Format der Bank einlesen und Datum, Einzahlung, Auszahlung, Referenz und Beschreibung anzeigen. Wiederholte Referenzen vor der Übernahme in die Bankabstimmung prüfen.

Importieren Sie die Bankreferenz 00038 mit 1.234,50 zweimal und danach mit 1.234,55. Genau eine Transaktion wird gebucht, die identische Zeile als Duplikat verknüpft und der abweichende Betrag zur Prüfung vorgelegt. Ein Sprachwechsel ändert weder die führenden Nullen der Transaktionsreferenz noch die Auslegung des Zahlenformats der Quelldatei.

[English](../banking.md#bank-statement-import-and-duplicate-review) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#procredit-bank-statement-processing).

## Erfassen Sie Ein- und Auszahlungen per Bargeld oder Scheck im Kassenbuch und prüfen Sie die Einträge für einzelne Geschäftspartner

<a id="workflow-treasury-transaction-register"></a>

Für jede Zahlungsart Forderungs- und Verbindlichkeitskonten festlegen. Im Kassenbeleg entweder direkt Konten bebuchen oder Beträge offenen Rechnungen des Geschäftspartners zuordnen.

Erfassen Sie in derselben Kasse einen Geldeingang von 250,00 mit Geschäftspartner und eine Auszahlung von 75,00 ohne Geschäftspartner. Deutsch und Afrikaans zeigen jeweils eine Nettozunahme von 175,00. Der Geschäftspartnerfilter lässt nur den Eingang von 250,00 übrig.

[English](../banking.md#treasury-transaction-register) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#treasury-entry).

## Autorisieren Sie einen Sammelauftrag für Lieferantenzahlungen über die Bank und gleichen Sie jeden Posten mit der Bankrückmeldung ab

<a id="workflow-supplier-payment-batch-authorization"></a>

Lieferantenzahlungen auswählen und den Sammelauftrag mit einem Einmalcode freigeben. Bankreferenz und Ergebnis je Einzelauftrag führen.

Verarbeiten Sie dieselbe Bankantwort für einen freigegebenen Sammelauftrag mit einer bestätigten und einer abgelehnten Lieferantenzahlung zweimal. Nur der bezahlte Lieferant erhält ein deutsches Zahlungsavis, der abgelehnte Posten bleibt offen und Hindi- sowie englischsprachige Mitarbeitende sehen dieselben Bankreferenzen und den ursprünglichen Ablehnungsgrund.

[English](../banking.md#supplier-payment-batch-authorization) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#sanpra-easypay).

## Wickeln Sie eine Zahlung online, über ein gekoppeltes Terminal oder für eine wiederkehrende Zahlungsanforderung ab und gleichen Sie sie mit der Rechnung ab

<a id="workflow-online-and-terminal-payment-collection"></a>

Nach Händlerfreigabe erhält jede Zahlungsart einen Einzugsweg. Eine Zahlungsanforderung kann einen Online-Checkout, ein gespeichertes Mandat oder eine Zahlung am registrierten Terminal auslösen.

Eine französischsprachige Person begleicht eine Rechnung über 35,70 EUR. Geht die Bestätigung zweimal ein, wird der Betrag nur einmal zugeordnet und die deutschsprachige Kassenkraft sieht dieselbe beglichene Rechnung.

[English](../banking.md#online-and-terminal-payment-collection) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/banking.md#stripe2-payment-integration).
