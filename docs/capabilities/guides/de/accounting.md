# Rechnungswesen und Steuern

## Übermitteln Sie ägyptische elektronische Rechnungen und verfolgen Sie das Prüfergebnis der Steuerbehörde für jeden einzelnen Beleg

<a id="workflow-egyptian-electronic-tax-submission"></a>

Rechnungen sowie Gutschriften und Belastungsanzeigen lassen sich einzeln oder gemeinsam einreichen. Die erste Rückmeldung und das endgültige Prüfergebnis werden je Beleg getrennt geführt.

Antwortet der Testdienst auf eine signierte Sammelübermittlung mit HTTP 202, einer externen Kennung für INV-001 und einem Strukturfehler für INV-002, wartet nur INV-001 auf die abschließende Prüfung. INV-002 muss korrigiert werden, keiner der Belege gilt als endgültig genehmigt, und beide Sprachfassungen bewahren Kennungen, Fehlercode und signierte Anfrage.

[English](../accounting.md#egyptian-electronic-tax-submission) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/accounting.md#e-invoice-egypt).

## Ordnen Sie Zahlungen einem Devisentermingeschäft zu und buchen Sie den Gewinn oder Verlust aus der Auflösung des ungenutzten Teils

<a id="workflow-forward-exchange-contract-allocation"></a>

Jede Zahlung verweist auf die genutzten Teilbeträge ihrer Devisentermingeschäfte. Bei der gewinnbringenden Auflösung eines Exporttermingeschäfts stehen Bank im Soll und Kursgewinn im Haben.

Von einem Exporttermin über 1.000 USD zu 17,50 NAD je USD sind 600 USD genutzt. Nach Auflösung weiterer 100 USD zu 17,20 ohne Gebühren verbleiben 300 USD. In jeder Sprache stehen 30 NAD im Soll der Bank und 30 NAD Kursgewinn im Haben.

[English](../accounting.md#forward-exchange-contract-allocation) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/accounting.md#forward-contract).

## Lesen Sie eine Rechnung aus einer PDF-Datei aus und prüfen Sie Geschäftspartner, Datum, Währung und Positionsbeträge vor dem Anlegen des Entwurfs

<a id="workflow-invoice-image-and-document-extraction"></a>

Einkauf oder Verkauf auswählen, die PDF einlesen und den Rechnungsbetrag mit der Positionssumme vergleichen. Die geprüfte Entwurfsrechnung behält die ursprüngliche PDF als Anlage.

Lesen Sie das deutsche PDF mit Datum 14.07.2023 und einer Position über 1.234,50 EUR ein, prüfen Sie es auf Englisch und bestätigen Sie denselben Import zweimal. Es entsteht ein verknüpfter Entwurf mit dem Datum 2023-07-14 und dem Betrag von 1.234,50 EUR; Originaltext, Geschäftspartner und Werte bleiben nachvollziehbar.

[English](../accounting.md#invoice-image-and-document-extraction) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/accounting.md#ai-invoice-importer).

## Buchen Sie in der jemenitischen Lokalisierung einen Mitarbeitervorschuss und gleichen Sie die Rückzahlung in der bevorzugten Sprache des Prüfers ab

<a id="workflow-employee-advance-and-return-in-yemen"></a>

Vorschüsse belasten das Vorschusskonto und entlasten das Auszahlungskonto. Eine Rückzahlung verweist auf den ursprünglichen Vorschuss und kehrt Soll und Haben um.

Ein Vorschuss von 100 Einheiten Transaktionswährung zum Kurs von 2 Einheiten Firmenwährung je Einheit ergibt je 200 im Soll und Haben. Die vollständige Rückzahlung zum selben Kurs kehrt beide Buchungen um, und Konten und Beträge stimmen im arabischen und englischen Bericht überein.

[English](../accounting.md#employee-advance-and-return-in-yemen) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/accounting.md#pav).

## Erstellen Sie eine Anzahlungsrechnung und stellen Sie die übrigen Raten gemäß dem Zahlungsplan des Verkaufsauftrags in Rechnung

<a id="workflow-sales-order-advance-and-instalment-invoicing"></a>

Auf dem Auftrag Zahlungsbedingungen und ersten Ratenfälligkeitstag festlegen. Die Anzahlungsrechnung enthält vereinbarte Zuschläge. Weitere Rechnungen entstehen zwei Tage vor der jeweiligen Fälligkeit.

Bei einem Auftragswert von 1.000, 20 % Anzahlung, 50 Fracht und drei Raten ab 15. Januar beträgt die Anzahlungsrechnung 250. Zwei Planungsläufe am 13. Januar erzeugen zusammen nur eine erste Ratenrechnung über 266,67, deren Betrag ohne Zahlung unabhängig von der Sprache vollständig offen bleibt.

[English](../accounting.md#sales-order-advance-and-instalment-invoicing) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/accounting.md#payment-installments).

## Erstellen Sie die britische Umsatzsteuererklärung aus den zugeordneten Belegen, reichen Sie sie für den richtigen Zeitraum ein und gleichen Sie die Eingangsbestätigung ab

<a id="workflow-british-return-aggregation"></a>

Unternehmen oder bevollmächtigte Vertretungen prüfen Steuerbeträge, Journalanpassungen und Meldezeitraum. Verbindlichkeiten, Zahlungen und Abschlussbuchung bleiben einzeln nachvollziehbar.

Zwei Steuerpositionen betragen 12 und 8, ihre Summe auf der Rechnung beträgt 20 und eine gesonderte Korrektur −2. Sowohl die walisische als auch die englische Ansicht weist 18 im selben Meldefeld aus, ohne die Rechnungssumme als zusätzlichen Betrag einzurechnen.

[English](../accounting.md#british-return-aggregation) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/accounting.md#erpnext-united-kingdom).
