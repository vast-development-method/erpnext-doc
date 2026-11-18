# Vertrieb und Kundenverwaltung

## Erstellen Sie eine Telefonkampagne aus ausgewählten Kontakten, prüfen Sie die Sperrliste und verteilen Sie zulässige Anrufe auf die Mitarbeitenden

<a id="workflow-calling-campaigns-and-contact-suppression"></a>

Kontakte filtern und die Anrufreihenfolge auf das Team verteilen. Ergebnisse, zulässige Aufzeichnungen und abrechenbare Leistungen der Kampagne zuordnen.

Lässt ein Kontakt seine Rufnummer nach der Kampagnenauswahl und vor der Zuweisung sperren, muss der Anruf auch mit einem anderssprachigen Gesprächsleitfaden unterbleiben. Es erfolgt weder ein Anruf über den Anbieter noch die Erfassung einer abrechenbaren Einheit.

[English](../sales.md#calling-campaigns-and-contact-suppression) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#b2b-marketing).

## Planen Sie bedingte Wiedervorlagen und versenden Sie fällige Erinnerungen in der Sprache der zuständigen Person

<a id="workflow-business-calendar-follow-up"></a>

Jede Erinnerung mit Rechnung, zuständiger Person und Wiedervorlagedatum verbinden. Zahlungszusagen mit tatsächlichen Zahlungseingängen vergleichen.

Ein am Freitag um 09:00 Uhr versandtes Angebot ist nach zwei Arbeitstagen nachzufassen. Ohne Feiertag sehen beide Nutzer auf Afrikaans und Deutsch genau eine Wiedervorlage für Dienstag, 09:00 Uhr Windhoeker Zeit.

[English](../sales.md#business-calendar-follow-up) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#follow-up).

## Importieren Sie Anfragen vom Marktplatz, verfolgen Sie ihren Status und übernehmen Sie eine ausgewählte Anfrage als Lead

<a id="workflow-marketplace-inquiry-conversion"></a>

Anfragen planmäßig oder für einen Zeitraum abrufen. Überlappende Abrufe anhand der externen Anfragekennung erkennen und den Interessentendatensatz einmalig anlegen.

Importieren Sie INQ-47 für Verkäufer A über den planmäßigen Abruf und rückwirkend für den überlappenden Zeitraum. Wird die Anfrage in zwei Oberflächensprachen in einen Lead umgewandelt, bleibt genau eine Anfrage mit demselben Lead bestehen; der Hindi-Produktname und die externe Anfrage-ID bleiben erhalten.

[English](../sales.md#marketplace-inquiry-conversion) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#erpnext-indiamart-integration).

## Verfolgen Sie Aufträge eines Kunden oder Einkäufe bei einem Lieferanten von den Summen im Dashboard bis zu den einzelnen Belegen

<a id="workflow-party-order-dashboard"></a>

Unternehmen, Geschäftspartner und Zeitraum auswählen. Eingereichte Belege anhand ihres maßgeblichen Datums zählen und Belege sowie Beträge je Währung aufschlüsseln.

Öffnen Sie die Auftragskachel für einen Kunden mit zwei sichtbaren, bestätigten Aufträgen über zusammen 140 EUR und einem dritten Auftrag im Entwurf. Mit demselben Datumsfilter zeigt sie 2 und 140 EUR; auch nach einem Sprachwechsel erscheinen in der Detailansicht genau dieselben beiden Auftragsnummern.

[English](../sales.md#party-order-dashboard) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#insightly).

## Führen Sie eine Tischbestellung über mehrere Küchenbons hinweg und rechnen Sie sie an der Kasse des Standorts ab

<a id="workflow-restaurant-orders-and-kitchen-rounds"></a>

Die Tischbestellung über mehrere Küchenrunden offen halten. Kostenlose Zusätze als Anweisungen erfassen und kostenpflichtige Extras als eigene Positionen abrechnen.

Bestellen Sie ein Gericht für 60 mit einer kostenpflichtigen Beilage für 5 und einem kostenlosen Küchenhinweis; senden Sie die Runde zweimal mit derselben Versand-ID und kassieren Sie die Bestellung ab. Es entstehen ein Küchenbon und eine Kassenrechnung mit 65 vor Steuern; die arabische Küchenanzeige und die englische Kasse verwenden dieselben Optionskennungen und Positionsbeträge.

[English](../sales.md#restaurant-orders-and-kitchen-rounds) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#lumen-restaurants).

## Führen Sie eine Kassenschicht in der Sprache des Kassenpersonals und gleichen Sie die während eines Netzausfalls gespeicherten Verkäufe ab

<a id="workflow-offline-till-sales"></a>

Schicht öffnen, Artikel scannen und Zahlung erfassen. Offline-Verkäufe bis zur Serverbestätigung vorhalten und vor Schichtschluss alle ausstehenden Übertragungen klären.

Eine Kassiererin verkauft offline zwei Einheiten auf Arabisch und wechselt auf Deutsch. Geht die Upload-Bestätigung verloren, erzeugt ein erneuter Versuch insgesamt nur eine Rechnung und eine Lagerbewegung über zwei Einheiten, und der deutsche Status verweist auf diese Rechnung bei unveränderter Belegsprache.

[English](../sales.md#offline-till-sales) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#lumenpos).

## Veröffentlichen Sie einen Verkäuferkatalog in einem offenen Handelsnetz und gleichen Sie Käuferbestätigungen mit den ERP-Aufträgen ab

<a id="workflow-open-commerce-order-confirmations"></a>

Der Händler bietet Waren oder Dienstleistungen im ONDC-Netzwerk an. Das verwendete Einzelhandelsprotokoll bestimmt, welche Nachrichten der Händler verarbeiten kann.

Im englischen und im Hindi-Katalog steht dieselbe Artikelkennung. Wird die Bestätigung für zwei Einheiten nach einem Sprachwechsel erneut zugestellt, bleibt das Ergebnis identisch und genau ein Auftrag reserviert die zwei Einheiten.

Ein Angebot enthält zwei Einheiten zu je 120 und Versandkosten von 30. Eine gültige Bestätigung erzeugt einen Auftrag über 270 und reserviert zwei Einheiten. Der wiederholte Rückruf verwendet dieselbe Kennung. Eine dritte Einheit unter demselben Nachrichtenschlüssel führt zu einem Konflikt.

[English](../sales.md#open-commerce-order-confirmations) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#ondc-seller-app).

## Scannen Sie Artikel mit Serien- oder Chargennummer, erfassen Sie Verkäufe und Retouren und gleichen Sie jede Zahlungsart beim Schichtabschluss ab

<a id="workflow-retail-shift-settlement"></a>

Eröffnung und Verkäufe je Zahlungsart erfassen. Beim Abschluss den gezählten Betrag mit dem erwarteten Betrag nach Erstattungen vergleichen.

Eröffnen Sie die Schicht mit 100,00 in bar, nehmen Sie 200,00 bar und 50,00 per Karte ein und erstatten Sie 30,00 in bar. Bei gezählten 268,00 in bar und bestätigten 50,00 per Karte zeigen die arabische und englische Ansicht denselben Sollbestand von 270,00, eine Kassendifferenz von −2,00 und keine Kartendifferenz.

[English](../sales.md#retail-shift-settlement) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#retail-suite).

## Leiten Sie eine Tischbestellung an Küche und Bar und rechnen Sie den Besuch mit der zugehörigen Gästerechnung ab

<a id="workflow-restaurant-multi-station-fulfilment"></a>

Die Bestellung dem Tisch zuordnen, Artikel an ihre Zubereitungsstation leiten und Küchen- sowie Barbelege mit derselben Rechnung verbinden.

Geben Sie für einen Tisch auf Nepali zwei Portionen desselben Gerichts und ein Getränk auf und übermitteln Sie die Bestellung zweimal mit derselben Vorgangskennung. Die englischsprachige Küche erhält zwei Portionen, die deutschsprachige Bar ein Getränk und die Rechnung umfasst genau drei Einheiten mit den ursprünglichen Artikelcodes.

[English](../sales.md#restaurant-multi-station-fulfilment) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#sajha-menu).

## Prüfen Sie die vorgeschlagene Angebotserinnerung in der Sprache des Empfängers und geben Sie den genauen Wortlaut vor dem Versand frei

<a id="workflow-reviewed-sales-reminders"></a>

Nur zulässige Angebote, Aufträge und Rechnungen abrufen. Die vorgeschlagene Folgeaktion prüfen und Freigabe sowie Ausführung getrennt protokollieren.

Ein deutschsprachiger Vertriebsleiter prüft eine Angebotserinnerung für einen afrikaanssprachigen Kunden im Probelauf und gibt anschließend den genauen Text auf Afrikaans frei. Der Probelauf versendet nichts, auch bei erneutem Zeitplanlauf wird die freigegebene Nachricht nur einmal zugestellt und jede Textänderung benötigt eine neue Freigabe.

[English](../sales.md#reviewed-sales-reminders) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/sales.md#sales-ai).
