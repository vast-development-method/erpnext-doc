# Analysen, KI und Kalender

[English](../en/data.md) · [Afrikaans](../af/data.md) · Deutsch · [简体中文](../zh-Hans/data.md)

[Alle Themen](README.md)

## BigQuery Connector

Das Exportformular des Anbieters ordnet eine Quelltabelle einer benannten Zieltabelle zu, im Beispiel tabUser zu user, und bietet eine Spaltenauswahl sowie einen Filter. Für inkrementelle Läufe zeigt es Intervall, letzten Abgleich, zuletzt synchronisierte ID und die Sperre des Zeitplaners.

[Ablauf und Prüffall](../../../../capabilities/guides/de/data.md#workflow-analytical-dataset-export) · [Quellenbelege](../../apps/frappe_bigquery.md)

## InstaGPT

Laut Brandimic hinterlegt ein System Manager oder Administrator Schlüssel, Modell und Temperatur auf einer Skala von 0 bis 200, bevor Mitarbeitende über den Chat in der Navigationsleiste Nachrichten senden. OpenAI dokumentiert für die Temperatur von Chat Completions eine Skala von 0 bis 2; die Umrechnung und der tatsächlich vom Modul verwendete Endpunkt sind nicht belegt.

[Ablauf und Prüffall](../../../../capabilities/guides/de/data.md#workflow-multilingual-chat-composition) · [Quellenbelege](../../apps/instagpt.md)

## Islamic Calendar

Kanak beschreibt eine Hijri-Datumsauswahl mit Umrechnung in beide Richtungen zwischen islamischem und gregorianischem Kalender in ERP-Formularen. Ein Kanak zugeschriebener öffentlicher Quellstand führt getrennte Formate für Anzeige und Datumsauswahl und rechnet anhand einer mitgelieferten Umm-al-Qura-Tabelle der Monatsanfänge um.

[Ablauf und Prüffall](../../../../capabilities/guides/de/data.md#workflow-hijri-civil-day-conversion) · [Quellenbelege](../../apps/islamic_calendar.md)

## Nepali Calendar

Kanaks Anleitung zeigt, wie man in einem Datumsfeld ein nepalesisches Datum auswählt und im selben Formular zur gregorianischen Entsprechung wechselt. Der Anbieter nennt unter anderem Vertrieb, Einkauf, Personalwesen und Buchhaltung als Einsatzbereiche.

[Ablauf und Prüffall](../../../../capabilities/guides/de/data.md#workflow-nepali-civil-day-conversion) · [Quellenbelege](../../apps/nepali_calendar.md)

## ChatNext

Der Marktplatzeintrag beschreibt kontextbezogene Fragen zum ERP. Eine öffentliche historische Fassung speichert die Nutzernachricht in einer Gesprächssitzung, sendet sie mit Verlauf und Kontext der geöffneten Ansicht an einen gesonderten Dienst und erfasst die Antwort als Bot-Nachricht.

[Ablauf und Prüffall](../../../../capabilities/guides/de/data.md#workflow-multilingual-business-record-questions) · [Quellenbelege](../../apps/nextai.md)
