# Einkauf und Lager

## Prüfen Sie jede Rechnungsposition anhand der verbleibenden Menge und des Restwerts der zugehörigen Ein- oder Ausfuhrgenehmigung

<a id="workflow-import-and-export-licence-balances"></a>

Die Einfuhrrechnungsposition der Genehmigung zuordnen und CIF- sowie FOB-Werte erfassen. Vor der Buchung sowohl Restmenge als auch Restwert des Artikels prüfen.

Sind noch 50 kg und 450 Währungseinheiten verfügbar, muss eine Einfuhr von 40 kg im Wert von 451 abgelehnt werden. Beide Restbeträge bleiben unverändert, und die Meldungen auf Hindi und Englisch nennen dieselbe Genehmigung und Wertüberschreitung.

[English](../supply.md#import-and-export-licence-balances) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/supply.md#advance-authorisation-licence).

## Vergleichen Sie eine simulierte Bestellung mit der erwarteten Nachfrage, bevor Sie den Lieferanten beauftragen

<a id="workflow-demand-simulation-before-procurement"></a>

Prognosezeitraum auswählen und Bestand, erwartete Zugänge und Bedarf vergleichen. Menge und Eingangstermin vor der Lieferantenbestellung simulieren.

Bei 18 Einheiten Bestand, 6 rechtzeitig eintreffenden Einheiten und einer Nachfrage von 30 können ohne Nachlieferung 6 Einheiten nicht verkauft werden. Ein simulierter zusätzlicher Zugang von 10 senkt die Fehlmenge auf 0 und lässt 4 übrig, ohne eine Bestellung auszulösen oder beim Sprachwechsel Mengen und Termine zu verändern.

[English](../supply.md#demand-simulation-before-procurement) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/supply.md#procurementnext).

## Entscheiden Sie anhand des Stichprobenplans und der erfassten Fehler, wie das geprüfte Los weiterbehandelt wird

<a id="workflow-lot-acceptance-sampling"></a>

Die Stichproben gemäß Losprüfplan ziehen. Den genehmigten Entscheid auf die Wareneingangsposition anwenden und angenommene sowie abgewiesene Menge getrennt erfassen.

Sind 12 eingegangene Einheiten mit einer abgeschlossenen, abgelehnten Prüfung verknüpft, verbucht das System 0 als angenommen und 12 als zurückgewiesen. Im deutschen und englischen Bericht müssen Entscheidungscode, Probenkennungen und Mengen übereinstimmen.

[English](../supply.md#lot-acceptance-sampling) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/supply.md#aql-quality-assurance-by-havaratech).

## Berechnen Sie den Preis jeder Milchabholung anhand der Qualitätsmessungen und gleichen Sie die an der Annahmestelle gelieferte Menge ab

<a id="workflow-milk-collection-and-component-pricing"></a>

Den genehmigten Tarif nach Milchart, Sammelstelle und Datum wählen. Fett und fettfreie Trockenmasse mit den Komponententarifen und dem Volumen verrechnen.

Bei Fett- und Trockenmasse-Tarifen von 80 und 30, Messwerten von 4,0 % Fett und 8,5 % fettfreier Trockenmasse sowie einem Volumen von 100 ergeben sich ohne Abzüge oder Zuschläge ein Einzelpreis von 5,75 und insgesamt 575. Ein anderes Dezimaltrennzeichen ändert den Preis nicht, und ein erneut empfangener Messwert darf die Menge nicht verdoppeln.

[English](../supply.md#milk-collection-and-component-pricing) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/supply.md#dairy-management).

## Ordnen Sie Produkte und Lagerorte des Vertriebskanals den passenden ERP-Datensätzen zu, damit Bestellungen und Wareneingänge richtig verbucht werden

<a id="workflow-channel-receipt-synchronization"></a>

Kanalprodukte und Standorte internen Artikeln und Lagern zuordnen. Die externe Eingangsreferenz bewahren, damit eine erneute Bestätigung auf dieselbe Bestandsbewegung verweist.

Ein Lager erhält dasselbe Empfangsereignis für drei Stück zweimal. Auch nach einem Sprachwechsel verweisen beide Bestätigungen auf denselben Beleg, und der Bestand steigt nur um drei Stück.

[English](../supply.md#channel-receipt-synchronization) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/supply.md#official-easyecom-integration).

## Erfassen Sie Wareneingang, Inventur, Kommissionierung, Verpackung und Versand unter Beibehaltung der gescannten Artikel-, Lagerplatz- und Chargenkennungen

<a id="workflow-warehouse-scanning-and-transfers"></a>

Bei Eingang, Zählung, Umlagerung und Versand Artikel, Lagerplatz und Charge scannen. Packstücke und Etiketten den Einheiten zuordnen, ohne eine weitere Bestandsbewegung zu erzeugen.

Lagerplatz A enthält 20 Stück, B ist leer. Ein afrikaanssprachiger Kommissionierer bucht zwei Kartons zu je sechs Stück um. Die deutschsprachige Aufsicht sieht 8 Stück auf A und 12 auf B, auch wenn der Scanner denselben Vorgang erneut sendet.

[English](../supply.md#warehouse-scanning-and-transfers) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/supply.md#wms).
