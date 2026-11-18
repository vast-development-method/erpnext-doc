# Einkauf, Qualität und Lager

[English](../en/supply.md) · [Afrikaans](../af/supply.md) · Deutsch · [简体中文](../zh-Hans/supply.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## Advance Authorisation Licence

Prüfen Sie jede Rechnungsposition anhand der verbleibenden Menge und des Restwerts der zugehörigen Ein- oder Ausfuhrgenehmigung.

**Dokumentierter Ablauf**

Die zuständige Person verknüpft eine Position der Einfuhrrechnung mit der Genehmigung und erfasst den CIF- und den FOB-Wert. Die Buchung aktualisiert die verfügbare Menge und den Restwert für diesen Artikel, während eine Ausfuhrrechnung die exportierte Menge und den Ausfuhrwert der Genehmigung zuordnet.

**Vorgeschlagener Abnahmetest**

Sind noch 50 kg und 450 Währungseinheiten verfügbar, muss eine Einfuhr von 40 kg im Wert von 451 abgelehnt werden. Beide Restbeträge bleiben unverändert, und die Meldungen auf Hindi und Englisch nennen dieselbe Genehmigung und Wertüberschreitung.

[Ausführliches Profil auf Englisch](../../apps/advance_authorisation_licence.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence)

## ProcurementNext

Vergleichen Sie eine simulierte Bestellung mit der erwarteten Nachfrage, bevor Sie den Lieferanten beauftragen.

**Dokumentierter Ablauf**

Die Planung legt Zeitraum und Prognoseverfahren fest, vergleicht je Artikel Bestand, erwartete Zugänge, Bedarf und ungedeckten Bedarf und kann Set-Bestandteile einbeziehen. In derselben Planungsmaske kann der Einkauf Lieferant und Bedarfstermin angeben.

**Vorgeschlagener Abnahmetest**

Bei 18 Einheiten Bestand, 6 rechtzeitig eintreffenden Einheiten und einer Nachfrage von 30 können ohne Nachlieferung 6 Einheiten nicht verkauft werden. Ein simulierter zusätzlicher Zugang von 10 senkt die Fehlmenge auf 0 und lässt 4 übrig, ohne eine Bestellung auszulösen oder beim Sprachwechsel Mengen und Termine zu verändern.

[Ausführliches Profil auf Englisch](../../apps/advanced_procurement.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

## AQL Quality Assurance By HavaraTech

Entscheiden Sie anhand des Stichprobenplans und der erfassten Fehler, wie das geprüfte Los weiterbehandelt wird.

**Dokumentierter Ablauf**

Die Prüfkraft erfasst die Messwerte für eine Stichprobe aus dem Los. Ist ein Wareneingang mit einer abgelehnten Prüfung verknüpft, weist die untersuchte Quellversion die gesamte Eingangsmenge als zurückgewiesen und null Einheiten als angenommen aus.

**Vorgeschlagener Abnahmetest**

Sind 12 eingegangene Einheiten mit einer abgeschlossenen, abgelehnten Prüfung verknüpft, verbucht die untersuchte Version 0 als angenommen und 12 als zurückgewiesen. Im deutschen und englischen Bericht müssen Entscheidungscode, Probenkennungen und Mengen übereinstimmen.

[Ausführliches Profil auf Englisch](../../apps/aql_quality_assurance.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/aql_quality_assurance)

## Dairy Management

Berechnen Sie den Preis jeder Milchabholung anhand der Qualitätsmessungen und gleichen Sie die an der Annahmestelle gelieferte Menge ab.

**Dokumentierter Ablauf**

Beim Speichern eines Milcheintrags wählt die untersuchte Version einen gebuchten Tarif für Milchart, Sammellager und Datum. Im vereinfachten Modell errechnet sie den Wert aus Fettanteil, Anteil fettfreier Trockenmasse, den beiden Komponentensätzen und dem erfassten Volumen.

**Vorgeschlagener Abnahmetest**

Bei Fett- und Trockenmasse-Tarifen von 80 und 30, Messwerten von 4,0 % Fett und 8,5 % fettfreier Trockenmasse sowie einem Volumen von 100 ergeben sich ohne Abzüge oder Zuschläge ein Einzelpreis von 5,75 und insgesamt 575. Ein anderes Dezimaltrennzeichen ändert den Preis nicht, und ein erneut empfangener Messwert darf die Menge nicht verdoppeln.

[Ausführliches Profil auf Englisch](../../apps/dairy.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/dairy)

## Official EasyEcom Integration

Ordnen Sie Produkte und Lagerorte des Vertriebskanals den passenden ERP-Datensätzen zu, damit Bestellungen und Wareneingänge richtig verbucht werden.

**Dokumentierter Ablauf**

Laut Incircos Anleitung beginnen Geschäftskundenaufträge im ERP und Endkundenaufträge in EasyEcom. Das Lager ordnet den EasyEcom-Standort dem ERP-Lager zu, damit der abgeschlossene Empfang am richtigen Ort verbucht wird.

**Vorgeschlagener Abnahmetest**

Ein Lager erhält dasselbe Empfangsereignis für drei Stück zweimal. Auch nach einem Sprachwechsel verweisen beide Bestätigungen auf denselben Beleg, und der Bestand steigt nur um drei Stück.

[Ausführliches Profil auf Englisch](../../apps/erpnext_easyecom.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/erpnext_easyecom)

## WMS

Erfassen Sie Wareneingang, Inventur, Kommissionierung, Verpackung und Versand unter Beibehaltung der gescannten Artikel-, Lagerplatz- und Chargenkennungen.

**Dokumentierter Ablauf**

Dexciss beschreibt, wie Lagerpersonal mit mobilen Geräten Artikel und Lagerplätze abfragt, Bestände zählt und Wareneingänge erfasst. Es kann außerdem Materialanforderungen und Lagerbuchungen bearbeiten, Waren für den Versand kommissionieren und verpacken, Etiketten drucken und Qualitätsprüfungen dokumentieren.

**Vorgeschlagener Abnahmetest**

Lagerplatz A enthält 20 Stück, B ist leer. Ein afrikaanssprachiger Kommissionierer bucht zwei Kartons zu je sechs Stück um. Die deutschsprachige Aufsicht sieht 8 Stück auf A und 12 auf B, auch wenn der Scanner denselben Vorgang erneut sendet.

[Ausführliches Profil auf Englisch](../../apps/wms.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/wms)
