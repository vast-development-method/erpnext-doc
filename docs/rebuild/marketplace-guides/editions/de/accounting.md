# Rechnungen, Steuern und Buchhaltung

[English](../en/accounting.md) · [Afrikaans](../af/accounting.md) · Deutsch · [简体中文](../zh-Hans/accounting.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## E Invoice Egypt

Übermitteln Sie ägyptische elektronische Rechnungen und verfolgen Sie das Prüfergebnis der Steuerbehörde für jeden einzelnen Beleg.

**Dokumentierter Ablauf**

Der Anbieter unterstützt Einzel- und Sammelvorgänge für Rechnungen, Gutschriften, Belastungsanzeigen, Stornierungen und Prüfungen. Die Schnittstelle der ägyptischen Steuerbehörde meldet angenommene und zurückgewiesene Belege getrennt, bevor die abschließende Prüfung erfolgt.

**Vorgeschlagener Abnahmetest**

Antwortet der Testdienst auf eine signierte Sammelübermittlung mit HTTP 202, einer externen Kennung für INV-001 und einem Strukturfehler für INV-002, wartet nur INV-001 auf die abschließende Prüfung. INV-002 muss korrigiert werden, keiner der Belege gilt als endgültig genehmigt, und beide Sprachfassungen bewahren Kennungen, Fehlercode und signierte Anfrage.

[Ausführliches Profil auf Englisch](../../apps/e_invoice.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/e_invoice)

## Forward Contract

Ordnen Sie Zahlungen einem Devisentermingeschäft zu und buchen Sie den Gewinn oder Verlust aus der Auflösung des ungenutzten Teils.

**Dokumentierter Ablauf**

Laut Anbieter lassen sich Teilbeträge aus einem oder mehreren Termingeschäften einer Zahlung zuordnen. Ein erhaltener, FinByz zugeschriebener Programmstand bucht bei einer gewinnbringenden Auflösung Kursgewinn im Haben und Bank im Soll.

**Vorgeschlagener Abnahmetest**

Von einem Exporttermin über 1.000 USD zu 17,50 NAD je USD sind 600 USD genutzt. Nach Auflösung weiterer 100 USD zu 17,20 ohne Gebühren verbleiben 300 USD. In jeder Sprache stehen 30 NAD im Soll der Bank und 30 NAD Kursgewinn im Haben.

[Ausführliches Profil auf Englisch](../../apps/forward_contract.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/forward_contract)

## AI Invoice Importer

Lesen Sie eine Rechnung aus einer PDF-Datei aus und prüfen Sie Geschäftspartner, Datum, Währung und Positionsbeträge vor dem Anlegen des Entwurfs.

**Dokumentierter Ablauf**

IPCONNEX beschreibt die Extraktion von Rechnungsdaten aus PDF-Dateien mithilfe von ChatGPT. Im untersuchten öffentlichen Quellstand wählt die Sachbearbeitung Einkauf oder Verkauf und hinterlegt das PDF; der Import vergleicht den Gesamtbetrag mit den errechneten Positionsbeträgen und kann die entsprechende Eingangs- oder Ausgangsrechnung samt Quelldatei anlegen.

**Vorgeschlagener Abnahmetest**

Lesen Sie das deutsche PDF mit Datum 18.11.2026 und einer Position über 1.234,50 EUR ein, prüfen Sie es auf Englisch und bestätigen Sie denselben Import zweimal. Es entsteht ein verknüpfter Entwurf mit dem Datum 2026-11-18 und dem Betrag von 1.234,50 EUR; Originaltext, Geschäftspartner und Werte bleiben nachvollziehbar.

[Ausführliches Profil auf Englisch](../../apps/ipconnex_ai_invoice.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/ipconnex_ai_invoice)

## PAV

Buchen Sie in der jemenitischen Lokalisierung einen Mitarbeitervorschuss und gleichen Sie die Rückzahlung in der bevorzugten Sprache des Prüfers ab.

**Dokumentierter Ablauf**

Der Marktplatzeintrag für Jemen führt Mitarbeitervorschüsse sowie Buchhaltungs- und Anwesenheitsberichte auf. In einer öffentlichen historischen Fassung wird beim normalen Vorschuss das angegebene Konto im Soll und das Finanzierungskonto im Haben gebucht, bei einer Rückzahlung umgekehrt.

**Vorgeschlagener Abnahmetest**

Ein Vorschuss von 100 Einheiten Transaktionswährung zum Kurs von 2 Einheiten Firmenwährung je Einheit ergibt je 200 im Soll und Haben. Die vollständige Rückzahlung zum selben Kurs kehrt beide Buchungen um, und Konten und Beträge stimmen im arabischen und englischen Bericht überein.

[Ausführliches Profil auf Englisch](../../apps/pav.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/pav)

## Payment Installments

Erstellen Sie eine Anzahlungsrechnung und stellen Sie die übrigen Raten gemäß dem Zahlungsplan des Verkaufsauftrags in Rechnung.

**Dokumentierter Ablauf**

Laut Kanak wählt der Vertrieb im Auftrag die Zahlungsbedingungen, setzt den ersten Ratentermin und ergänzt bei Bedarf Nebenkosten. Mit dem Einreichen entstehen der Ratenplan und die Anzahlungsrechnung einschließlich Nebenkosten, und die weiteren Rechnungen werden jeweils zwei Tage vor Fälligkeit erstellt.

**Vorgeschlagener Abnahmetest**

Bei einem Auftragswert von 1.000, 20 % Anzahlung, 50 Fracht und drei Raten ab 15. Januar beträgt die Anzahlungsrechnung 250. Zwei Planungsläufe am 13. Januar erzeugen zusammen nur eine erste Ratenrechnung über 266,67, deren Betrag ohne Zahlung unabhängig von der Sprache vollständig offen bleibt.

[Ausführliches Profil auf Englisch](../../apps/payment_installment_kanak.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/payment_installment_kanak)

## ERPNext United Kingdom

Erstellen Sie die britische Umsatzsteuererklärung aus den zugeordneten Belegen, reichen Sie sie für den richtigen Zeitraum ein und gleichen Sie die Eingangsbestätigung ab.

**Dokumentierter Ablauf**

Das Handbuch von Case Solved beschreibt, wie Unternehmen oder Bevollmächtigte Umsatzsteuererklärungen prüfen und einreichen sowie offene Beträge und Zahlungen einsehen. Es nennt außerdem Steuersätze je Rechnung oder Position, Korrekturbuchungen und eine Abschlussbuchung für den Meldezeitraum.

**Vorgeschlagener Abnahmetest**

Zwei Steuerpositionen betragen 12 und 8, ihre Summe auf der Rechnung beträgt 20 und eine gesonderte Korrektur −2. Sowohl die walisische als auch die englische Ansicht weist 18 im selben Meldefeld aus, ohne die Rechnungssumme als zusätzlichen Betrag einzurechnen.

[Ausführliches Profil auf Englisch](../../apps/uk.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/uk)
