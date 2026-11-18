# Datenübertragung und Erfassung

## Exportieren Sie ausgewählte ERP-Felder in ein analytisches Datenlager und setzen Sie unterbrochene Übertragungen am letzten bestätigten Stand fort

<a id="workflow-analytical-dataset-export"></a>

Quelltabelle, zulässige Spalten, Filter und Ziel festlegen. Letzten verarbeiteten Schlüssel und Zeitpunkt speichern, damit der Export fortgesetzt werden kann.

INV-001 und INV-002 haben denselben Änderungszeitpunkt, die Seitengröße beträgt eins. Wird der Export nach dem ersten Schreibvorgang, aber vor dem Speichern des Prüfpunkts unterbrochen, ergibt der Neustart über die deutsche Oberfläche genau eine Zeile pro Rechnung mit unveränderten Spaltennamen.

[English](../data.md#analytical-dataset-export) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/data.md#bigquery-connector).

## Öffnen Sie den Chat über die ERP-Navigationsleiste und senden Sie eine Nachricht in der gewünschten Sprache

<a id="workflow-multilingual-chat-composition"></a>

Die Administration richtet Modell und zulässige Parameter des Dienstes ein. Gesprächssprache, Eingabewert und tatsächlich übermittelter Parameter bleiben nachvollziehbar.

Bestätigen Sie bei der chinesischen Zeicheneingabe im deutschen Chatfenster zunächst das Zeichen mit Enter, schließen Sie den Satz ab und wählen Sie erst dann Senden. Die Zeichenbestätigung löst keinen Versand aus; genau eine Nachricht enthält den ursprünglichen chinesischen Text, unabhängig von der gewünschten Antwortsprache.

[English](../data.md#multilingual-chat-composition) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/data.md#instagpt).

## Geben Sie ein Datum im islamischen Kalender ein und prüfen Sie den entsprechenden Tag im gregorianischen Kalender

<a id="workflow-hijri-civil-day-conversion"></a>

Das Hidschra-Datum wählen und anhand der freigegebenen Umm-al-Qura-Tabelle dem entsprechenden Kalendertag zuordnen. Ein Darstellungswechsel bewahrt diesen Tag.

Geben Sie nach der Umm-al-Qura-Tabelle den 01.09.1445 AH ein und wechseln Sie zum gregorianischen Kalender: Der gespeicherte Tag ist 2024-03-11. Nach erneutem Öffnen und Zurückschalten erscheint wieder der 01.09.1445 AH, auch bei anderer Sprache oder Zifferndarstellung.

[English](../data.md#hijri-civil-day-conversion) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/data.md#islamic-calendar).

## Erfassen Sie ein Datum im nepalesischen Kalender und finden Sie denselben Beleg über sein gregorianisches Datum

<a id="workflow-nepali-civil-day-conversion"></a>

Das nepalesische Datum im Formular wählen und den entsprechenden Kalendertag speichern. Danach lässt sich derselbe Tag in beiden Kalendern anzeigen.

Eine Person erfasst einen Einkauf am 1. Baisakh 2081, eine andere sucht ihn über den 13. April 2024. Der Filter findet denselben Beleg, und der Kalenderwechsel zeigt unabhängig von der Sprache wieder den 1. Baisakh 2081.

[English](../data.md#nepali-civil-day-conversion) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/data.md#nepali-calendar).

## Stellen Sie eine ERP-Frage in einer Sprache und lassen Sie sich in einer anderen antworten, während die ursprüngliche Unterhaltung erhalten bleibt

<a id="workflow-multilingual-business-record-questions"></a>

Die Frage an Person und Gespräch binden. Dem Antwortdienst nur zulässigen Datensatzkontext übergeben und seine Antwort im selben Gespräch speichern.

Eine Person mit deutscher Oberfläche fragt auf Afrikaans nach dem offenen Betrag einer für sie lesbaren Rechnung. Die Antwort erscheint auf Afrikaans und nennt das Quellfeld, während die ursprüngliche Frage erhalten und die Rechnung unverändert bleibt.

[English](../data.md#multilingual-business-record-questions) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/data.md#chatnext).
