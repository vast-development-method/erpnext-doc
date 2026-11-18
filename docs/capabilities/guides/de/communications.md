# Kundenkommunikation

## Starten Sie einen Anruf aus dem CRM und gleichen Sie die Verbindungsdaten mit der Aktivität des zuständigen Mitarbeiters ab

<a id="workflow-outbound-calling-and-call-dispositions"></a>

Den Anruf aus dem Geschäftsvorgang über die konfigurierte Nummer starten. Anrufkennung, Zeitpunkt, Ergebnis und berechtigten Zugriff auf die Aufzeichnung mit dem Vorgang verbinden.

Erscheint derselbe ausgehende Anruf auf zwei überlappenden Protokollseiten des Anbieters, zeigt der Bericht nach dem Import genau einen angenommenen Anruf mit 48 Sekunden Dauer und CRM-Verknüpfung. Bei übersetztem Status bleiben Anrufkennung und gewählte Nummer gleich.

[English](../communications.md#outbound-calling-and-call-dispositions) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#tata-smartflo-call-integration).

## Senden Sie ERP-Benachrichtigungen in der bevorzugten Sprache des Empfängers an registrierte Geräte mit aktivem Abonnement

<a id="workflow-device-notification-delivery"></a>

Das Gerät für die Zielperson registrieren. Ein Benachrichtigungsereignis löst je zutreffendem Gerät einen Zustellversuch aus.

Eine Person erhält den Hinweis zu PO-18 auf zwei Geräten auf Afrikaans und Deutsch. Bei erneuter Verarbeitung gibt es je Gerät einen Versandvorgang; die bestätigte Nachricht wird nicht erneut versendet, und beide verweisen auf PO-18.

[English](../communications.md#device-notification-delivery) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#fcm-notification).

## Senden Sie einem Kontakt eine SMS und unterscheiden Sie die Annahme durch das Gateway von der bestätigten Zustellung

<a id="workflow-text-message-acceptance-and-delivery"></a>

Kontakt, Rufnummer und Nachricht auswählen. Annahme beim Anbieter, Zustellbericht und mögliche Fehler getrennt protokollieren.

Eine englischsprachige Mitarbeiterin sendet die freigegebene Terminerinnerung auf Afrikaans an Kontakt C17. Bestätigt der Dienst lediglich die Annahme, erscheint eine eingereichte SMS mit Terminreferenz. Die Zustellung am Gerät bleibt unbestätigt.

[English](../communications.md#text-message-acceptance-and-delivery) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#telenor-sms).

## Veröffentlichen Sie eine Umfrage mit Verzweigungen und werten Sie Antworten anhand der Fragen und der in der jeweiligen Sprache gewählten Optionen aus

<a id="workflow-branching-surveys-and-response-aggregation"></a>

Fragen und Verzweigungsregeln speichern, das Formular veröffentlichen und jede Antwort der veröffentlichten Fassung zuordnen.

Zwei Personen wählen die Option mit der Kennung `delivery`, einmal auf Deutsch und einmal auf Afrikaans. Beide Antworten zählen unter derselben Kennung. Die jeweiligen Folgeantworten bleiben der richtigen Person zugeordnet und in ihrer ursprünglichen Sprache erhalten.

[English](../communications.md#branching-surveys-and-response-aggregation) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#tripetto-survey-integration).

## Versenden Sie eine Erinnerung als Klartext, wenn ein Geschäftsvorgang die konfigurierte Bedingung erfüllt

<a id="workflow-rule-based-text-reminders"></a>

Ein Dokumentereignis mit Bedingung, Empfänger und freigegebener Nachrichtenvorlage verbinden. Zum Versand die Werte dieses Ereignisses einsetzen.

Für eine französischsprachige Kundin ist eine Bestellung überfällig. Wird das Ereignis zweimal verarbeitet und nimmt der Nachrichtendienst die erste Nachricht in die Warteschlange auf, bleibt genau eine französische Erinnerung mit der ursprünglichen Bestellnummer im Status „eingereiht“.

[English](../communications.md#rule-based-text-reminders) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#ultramsg-whatsapp-integration).

## Senden Sie personalisierte Vorlagen an ausgewählte Leads, Verkaufschancen oder Lieferanten und prüfen Sie das Ergebnis je Empfänger

<a id="workflow-personalized-recipient-messaging"></a>

Vorlagenparameter mit Datenfeldern verknüpfen und Empfänger aus Interessenten, Verkaufschancen oder Lieferanten auswählen. Das Ergebnis für jeden Empfänger speichern.

Ein deutschsprachiger Mitarbeiter benachrichtigt einen afrikaanssprachigen Lieferanten mit einer bestätigten namibischen Telefonnummer. Die Warteschlange enthält genau eine Nachricht in der freigegebenen Fassung auf Afrikaans mit der Lieferantenreferenz und der gespeicherten internationalen Telefonnummer.

[English](../communications.md#personalized-recipient-messaging) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#whatsapp-app).

## Versenden Sie eine genehmigte Vorlage mit dem zugehörigen PDF, wenn sich ein konfiguriertes Feld oder der Belegstatus ändert

<a id="workflow-translated-document-message-attachments"></a>

Freigegebene Sprachvariante und PDF-Anlage mit der Dokumentregel verbinden. Das vereinbarte Speichern, Einreichen oder Ändern eines Feldes löst den Versand aus.

Eine Regel verlangt sowohl eine arabische Nachricht als auch ein arabisches PDF. Reicht eine englischsprachige Person die Rechnung ein und ist nur der Nachrichtentext verfügbar, bleibt die Benachrichtigung zurückgestellt. Das System weist das fehlende Layout aus und sendet keinen anderssprachigen Anhang.

[English](../communications.md#translated-document-message-attachments) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#whatsapp-integration).

## Ordnen Sie eingehende Nachrichten Kunden zu, antworten Sie im Gespräch und versenden Sie geprüfte Nachrichten an berechtigte Empfänger

<a id="workflow-incoming-customer-conversations"></a>

Eingehende Nachrichten dem Kunden zuordnen, die Unterhaltung berechtigten Personen anzeigen und Originaltext sowie Medien bewahren.

Ein Kunde sendet eine chinesische Nachricht mit einem Dokument. Nach der Antwort eines italienischsprachigen Mitarbeiters auf Chinesisch öffnet eine deutschsprachige Kollegin denselben Verlauf: Beide Originalnachrichten, der zugriffsgeschützte Anhang und die Kundenzuordnung bleiben erhalten.

[English](../communications.md#incoming-customer-conversations) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/communications.md#whatsapp-plus).
