# Analysen, KI und Kalender

[English](../en/data.md) · [Afrikaans](../af/data.md) · Deutsch · [简体中文](../zh-Hans/data.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## BigQuery Connector

Exportieren Sie ausgewählte ERP-Felder nach BigQuery und setzen Sie unterbrochene Übertragungen am letzten bestätigten Stand fort.

**Dokumentierter Ablauf**

Das Exportformular des Anbieters ordnet eine Quelltabelle einer benannten Zieltabelle zu, im Beispiel tabUser zu user, und bietet eine Spaltenauswahl sowie einen Filter. Für inkrementelle Läufe zeigt es Intervall, letzten Abgleich, zuletzt synchronisierte ID und die Sperre des Zeitplaners.

**Vorgeschlagener Abnahmetest**

INV-001 und INV-002 haben denselben Änderungszeitpunkt, die Seitengröße beträgt eins. Wird der Export nach dem ersten Schreibvorgang, aber vor dem Speichern des Prüfpunkts unterbrochen, ergibt der Neustart über die deutsche Oberfläche genau eine Zeile pro Rechnung mit unveränderten Spaltennamen.

[Ausführliches Profil auf Englisch](../../apps/frappe_bigquery.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## InstaGPT

Öffnen Sie den Chat über die ERP-Navigationsleiste und senden Sie eine Nachricht in der gewünschten Sprache.

**Dokumentierter Ablauf**

Laut Brandimic hinterlegt ein System Manager oder Administrator Schlüssel, Modell und Temperatur auf einer Skala von 0 bis 200, bevor Mitarbeitende über den Chat in der Navigationsleiste Nachrichten senden. OpenAI dokumentiert für die Temperatur von Chat Completions eine Skala von 0 bis 2; die Umrechnung und der tatsächlich vom Modul verwendete Endpunkt sind nicht belegt.

**Vorgeschlagener Abnahmetest**

Bestätigen Sie bei der chinesischen Zeicheneingabe im deutschen Chatfenster zunächst das Zeichen mit Enter, schließen Sie den Satz ab und wählen Sie erst dann Senden. Die Zeichenbestätigung löst keinen Versand aus; genau eine Nachricht enthält den ursprünglichen chinesischen Text, unabhängig von der gewünschten Antwortsprache.

[Ausführliches Profil auf Englisch](../../apps/instagpt.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/instagpt)

## Islamic Calendar

Geben Sie ein Datum im islamischen Kalender ein und prüfen Sie den entsprechenden Tag im gregorianischen Kalender.

**Dokumentierter Ablauf**

Kanak beschreibt eine Hijri-Datumsauswahl mit Umrechnung in beide Richtungen zwischen islamischem und gregorianischem Kalender in ERP-Formularen. Ein Kanak zugeschriebener öffentlicher Quellstand führt getrennte Formate für Anzeige und Datumsauswahl und rechnet anhand einer mitgelieferten Umm-al-Qura-Tabelle der Monatsanfänge um.

**Vorgeschlagener Abnahmetest**

Geben Sie nach der angegebenen Umm-al-Qura-Tabelle den 08.06.1448 AH ein und wechseln Sie zum gregorianischen Kalender: Der gespeicherte Tag ist 2026-11-18. Nach erneutem Öffnen und Zurückschalten erscheint wieder der 08.06.1448 AH, auch bei anderer Sprache oder Zifferndarstellung.

[Ausführliches Profil auf Englisch](../../apps/islamic_calendar.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/islamic_calendar)

## Nepali Calendar

Erfassen Sie ein Datum im nepalesischen Kalender und finden Sie denselben Beleg über sein gregorianisches Datum.

**Dokumentierter Ablauf**

Kanaks Anleitung zeigt, wie man in einem Datumsfeld ein nepalesisches Datum auswählt und im selben Formular zur gregorianischen Entsprechung wechselt. Der Anbieter nennt unter anderem Vertrieb, Einkauf, Personalwesen und Buchhaltung als Einsatzbereiche.

**Vorgeschlagener Abnahmetest**

Eine Person erfasst einen Einkauf am 1. Baisakh 2081, eine andere sucht ihn über den 13. April 2024. Der Filter findet denselben Beleg, und der Kalenderwechsel zeigt unabhängig von der Sprache wieder den 1. Baisakh 2081.

[Ausführliches Profil auf Englisch](../../apps/nepali_calendar.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/nepali_calendar)

## ChatNext

Stellen Sie eine ERP-Frage in einer Sprache und lassen Sie sich in einer anderen antworten, während die ursprüngliche Unterhaltung erhalten bleibt.

**Dokumentierter Ablauf**

Der Marktplatzeintrag beschreibt kontextbezogene Fragen zum ERP. Eine öffentliche historische Fassung speichert die Nutzernachricht in einer Gesprächssitzung, sendet sie mit Verlauf und Kontext der geöffneten Ansicht an einen gesonderten Dienst und erfasst die Antwort als Bot-Nachricht.

**Vorgeschlagener Abnahmetest**

Eine Person mit deutscher Oberfläche fragt auf Afrikaans nach dem offenen Betrag einer für sie lesbaren Rechnung. Die Antwort erscheint auf Afrikaans und nennt das Quellfeld, während die ursprüngliche Frage erhalten und die Rechnung unverändert bleibt.

[Ausführliches Profil auf Englisch](../../apps/nextai.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/nextai)
