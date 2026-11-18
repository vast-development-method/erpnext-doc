# Anrufe, Umfragen und Nachrichten

[English](../en/communications.md) · [Afrikaans](../af/communications.md) · Deutsch · [简体中文](../zh-Hans/communications.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## Tata Smartflo Call Integration

Starten Sie einen Smartflo-Anruf aus dem CRM und gleichen Sie die Verbindungsdaten mit der Aktivität des zuständigen Mitarbeiters ab.

**Dokumentierter Ablauf**

Mitarbeitende mit hinterlegter Telefonnummer starten Anrufe direkt aus dem ERP. Laut Anbieter ruft die Integration Smartflo-Verbindungsdaten und Aufzeichnungen ab, verknüpft Anrufe mit dem Geschäftsvorgang und filtert Berichte nach Datum, Status oder Anrufart.

**Vorgeschlagener Abnahmetest**

Erscheint derselbe ausgehende Anruf auf zwei überlappenden Protokollseiten des Anbieters, zeigt der Bericht nach dem Import genau einen angenommenen Anruf mit 48 Sekunden Dauer und CRM-Verknüpfung. Bei übersetztem Status bleiben Anrufkennung und gewählte Nummer gleich.

[Ausführliches Profil auf Englisch](../../apps/call_integration.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/call_integration)

## FCM Notification

Senden Sie ERP-Benachrichtigungen in der bevorzugten Sprache des Empfängers an registrierte Geräte mit aktivem Abonnement.

**Dokumentierter Ablauf**

Die Anleitung verknüpft den Versand mit dem Anlegen eines Notification-Log-Eintrags. Über User Device wird das Gerät dem Empfänger zugeordnet, damit bei dessen abonniertem Ereignis eine Benachrichtigung ausgelöst wird.

**Vorgeschlagener Abnahmetest**

Eine Person erhält den Hinweis zu PO-18 auf zwei Geräten auf Afrikaans und Deutsch. Bei erneuter Verarbeitung gibt es je Gerät einen Versandvorgang; die bestätigte Nachricht wird nicht erneut versendet, und beide verweisen auf PO-18.

[Ausführliches Profil auf Englisch](../../apps/fcm_notification.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/fcm_notification)

## Telenor Sms

Senden Sie einem Kontakt eine SMS über Telenor und unterscheiden Sie die Annahme durch das Gateway von der bestätigten Zustellung.

**Dokumentierter Ablauf**

Laut Anbieter können ERP-Benutzer über die Telenor-API SMS an ihre Kontakte senden. Das öffentliche Supportforum enthält keine Angaben zu Zustellbestätigungen, Zeichenkodierung oder Sprachauswahl.

**Vorgeschlagener Abnahmetest**

Eine englischsprachige Mitarbeiterin sendet die freigegebene Terminerinnerung auf Afrikaans an Kontakt C17. Bestätigt der Dienst lediglich die Annahme, erscheint eine eingereichte SMS mit Terminreferenz. Die Zustellung am Gerät bleibt unbestätigt.

[Ausführliches Profil auf Englisch](../../apps/telenor_sms.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/telenor_sms)

## Tripetto Survey Integration

Veröffentlichen Sie eine Umfrage mit Verzweigungen und werten Sie Antworten anhand der Fragen und der in der jeweiligen Sprache gewählten Optionen aus.

**Dokumentierter Ablauf**

Die verantwortliche Person öffnet den visuellen Editor aus der Umfrage, speichert Fragen und Verzweigungsregeln und veröffentlicht die Umfrage unter einer eigenen Formularadresse. Nach dem Absenden speichert das ERP die Antwort als Datensatz vom Typ Survey Answer.

**Vorgeschlagener Abnahmetest**

Zwei Personen wählen die Option mit der Kennung `delivery`, einmal auf Deutsch und einmal auf Afrikaans. Beide Antworten zählen unter derselben Kennung. Die jeweiligen Folgeantworten bleiben der richtigen Person zugeordnet und in ihrer ursprünglichen Sprache erhalten.

[Ausführliches Profil auf Englisch](../../apps/tripetto_survey.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/tripetto_survey)

## Ultramsg Whatsapp Integration

Versenden Sie über UltraMsg eine WhatsApp-Erinnerung als Klartext, wenn ein Geschäftsvorgang die konfigurierte Bedingung erfüllt.

**Dokumentierter Ablauf**

Ein Administrator richtet die UltraMsg-Instanz samt Token ein und legt Ereignisbedingungen sowie Nachrichtenvorlagen mit Platzhaltern fest. Der Anbieter beschreibt automatisch versandte WhatsApp-Klartextnachrichten etwa für überfällige Bestellungen und Zahlungserinnerungen.

**Vorgeschlagener Abnahmetest**

Für eine französischsprachige Kundin ist eine Bestellung überfällig. Wird das Ereignis zweimal verarbeitet und nimmt UltraMsg die erste Nachricht in die Warteschlange auf, bleibt genau eine französische Erinnerung mit der ursprünglichen Bestellnummer im Status „eingereiht“.

[Ausführliches Profil auf Englisch](../../apps/ultramsg_whatsapp_integration.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/ultramsg_whatsapp_integration)

## Whatsapp App

Senden Sie personalisierte WATI-Vorlagen an ausgewählte Leads, Verkaufschancen oder Lieferanten und prüfen Sie das Ergebnis je Empfänger.

**Dokumentierter Ablauf**

Ein Administrator aktiviert die WATI-Verbindung und ordnet die Parameter einer WATI-Vorlage den ERP-Feldern zu. Mitarbeitende wählen einen oder mehrere Empfänger aus Lead-, Verkaufschancen- oder Lieferantenlisten und können die Nachrichtenaktivität einsehen.

**Vorgeschlagener Abnahmetest**

Ein deutschsprachiger Mitarbeiter benachrichtigt einen afrikaanssprachigen Lieferanten mit einer bestätigten namibischen Telefonnummer. Die Warteschlange enthält genau eine Nachricht in der freigegebenen Fassung auf Afrikaans mit der Lieferantenreferenz und der gespeicherten internationalen Telefonnummer.

[Ausführliches Profil auf Englisch](../../apps/whatsapp_app.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/whatsapp_app)

## WhatsApp Integration

Versenden Sie eine genehmigte WhatsApp-Vorlage mit dem zugehörigen PDF, wenn sich ein konfiguriertes Feld oder der Belegstatus ändert.

**Dokumentierter Ablauf**

Ein Administrator legt im ERP und bei Meta eine übereinstimmende Vorlage an, wählt die Sprache und ordnet gegebenenfalls das PDF für den Vorlagenkopf zu. Laut Anbieter können Speichern, Einreichen oder Aktualisieren eines Belegs sowie Änderungen eines Feldwerts eine Text- oder PDF-Benachrichtigung auslösen.

**Vorgeschlagener Abnahmetest**

Eine Regel verlangt sowohl eine arabische Nachricht als auch ein arabisches PDF. Reicht eine englischsprachige Person die Rechnung ein und ist nur der Nachrichtentext verfügbar, bleibt die Benachrichtigung zurückgestellt. Das System weist das fehlende Layout aus und sendet keinen anderssprachigen Anhang.

[Ausführliches Profil auf Englisch](../../apps/whatsapp_integration.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/whatsapp_integration)

## Whatsapp Plus

Ordnen Sie eingehende WhatsApp-Nachrichten Kunden zu, antworten Sie im Gespräch und versenden Sie geprüfte Nachrichten an berechtigte Empfänger.

**Dokumentierter Ablauf**

Mitarbeitende können den hinterlegten Kunden zu einer eingehenden WhatsApp-Nachricht erkennen, antworten, Medien herunterladen oder Vorlagen an ausgewählte Kunden und Gruppen senden. Der Anbieter beschreibt die Anpassung der Oberfläche an die Sprache des Arbeitsplatzes und zeigt sie auf Italienisch.

**Vorgeschlagener Abnahmetest**

Ein Kunde sendet eine chinesische Nachricht mit einem Dokument. Nach der Antwort eines italienischsprachigen Mitarbeiters auf Chinesisch öffnet eine deutschsprachige Kollegin denselben Verlauf: Beide Originalnachrichten, der zugriffsgeschützte Anhang und die Kundenzuordnung bleiben erhalten.

[Ausführliches Profil auf Englisch](../../apps/whatsapp_plus.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/whatsapp_plus)
