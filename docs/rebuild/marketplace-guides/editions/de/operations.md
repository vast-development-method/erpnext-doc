# Projekte, Immobilien und Service

[English](../en/operations.md) · [Afrikaans](../af/operations.md) · Deutsch · [简体中文](../zh-Hans/operations.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## Zymmr

Verfolgen Sie Aufgaben, Statuswechsel und Zeitbuchungen in einem mehrsprachigen Projektteam.

**Dokumentierter Ablauf**

Das Anbieter-Image mit Manifest-Prüfsumme sha256:6c99d642d1d375fac8638cc1bf2132614eacf3db28ba1d23685b93418bf245ff weist Everest 0.0.1 mit Commit c4c72c85896ab0c0dbd9c9bd7843023505a481da aus. Beim Projektwechsel erhält eine Aufgabe einen neuen sichtbaren Schlüssel, der alte wird protokolliert und die interne UUID bleibt erhalten.

**Vorgeschlagener Abnahmetest**

Ein deutschsprachiges Teammitglied schließt OPS-7 ab und bucht 90 Minuten für Tests. Die afrikaanssprachige Projektleitung sieht dieselbe abgeschlossene Aufgabe und genau 90 Minuten mit übersetzten Bezeichnungen.

[Ausführliches Profil auf Englisch](../../apps/everest.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/everest)

## Green Checklist

Planen Sie wiederkehrende Gebäudekontrollen und erfassen Sie, wer jeden Messwert oder Ja-/Nein-Befund aufgenommen hat.

**Dokumentierter Ablauf**

Die Checkliste des Anbieters ordnet eine wiederkehrende Aufgabe einer Anlage oder einem Dienst in einem Gemeinschaftsbereich zu. Sie erfasst Datum, ausführende Person, Aufsicht und entweder einen Ja-/Nein-Befund oder einen Messwert mit zulässigem Bereich.

**Vorgeschlagener Abnahmetest**

Bei einem zulässigen Bereich von 2 bis einschließlich 8 °C erfasst der Mitarbeiter auf Deutsch 8,1 °C. Die Aufsicht sieht auf Afrikaans genau eine Grenzwertüberschreitung für denselben Ort und dieselbe Person.

[Ausführliches Profil auf Englisch](../../apps/green_checklist.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/green_checklist)

## Incident Management

Erfassen Sie einen Vorfall, weisen Sie ihn einer zuständigen Person zu und verfolgen Sie die Untersuchung bis zu den Vorbeugungsmaßnahmen.

**Dokumentierter Ablauf**

Laut Indictrans fügt das Personal dem Erstbericht ein Foto bei; E-Mails und SMS folgen dem Zuständigkeitsablauf des Standorts. In einer gesonderten Implementierung für Knight Frank gehören der 24-Stunden-Bericht, die Risikobewertung nach 48 Stunden und die Nachverfolgung der Korrekturmaßnahmen nach 30 Tagen zu derselben Vorfallakte; der Produkteintrag schreibt diese Fristen nicht vor.

**Vorgeschlagener Abnahmetest**

Reichen Sie denselben afrikaanssprachigen Vorfallbericht mit Foto zweimal unter derselben Anfrage-ID ein und wiederholen Sie die fehlgeschlagene Benachrichtigung an den deutschsprachigen Empfänger. Es bleiben eine Berichtsversion und ein Fotoverweis; jeder Zustellversuch wird separat protokolliert, Vorfall-ID und Originaltext bleiben erhalten.

[Ausführliches Profil auf Englisch](../../apps/incident_management.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/incident_management)

## Site Management

Verwalten Sie Anlagen und Beschwerden am Standort, bestätigen Sie Besucher per E-Mail und stellen Sie Besucherausweise aus.

**Dokumentierter Ablauf**

Laut Indictrans registriert und fotografiert der Empfang Besucher, bestätigt sie per E-Mail-Einmalpasswort und stellt einen Besucherausweis aus; hinzu kommen Anlagen- und Beschwerdemanagement. Eine gesonderte Anbieterbroschüre beschreibt Vorregistrierung, Mobilcode und QR-Prüfung für ein Besucherprodukt; diese Optionen sind für den vorliegenden Eintrag nicht belegt.

**Vorgeschlagener Abnahmetest**

Registrieren Sie einen Besucher mit arabischem Namen und englischer E-Mail-Präferenz; versuchen Sie zuerst einen abgelaufenen, dann einen gültigen Bestätigungscode. Der erste Versuch erzeugt keinen Ausweis, nach erfolgreicher Prüfung ergibt auch eine wiederholte Ausstellung nur einen Besucherausweis; Originalname und Ausweisnummer bleiben in beiden Schreibrichtungen erhalten.

[Ausführliches Profil auf Englisch](../../apps/kf_city_2.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/kf_city_2)

## Helpdesk Management

Erfassen Sie eine allgemeine oder anlagenbezogene Störung und messen Sie die Zeit bis zur Behebung.

**Dokumentierter Ablauf**

Indictrans beschreibt allgemeine und mit einer registrierten Anlage verknüpfte Tickets samt Bearbeitungsablauf, E-Mails und Zeitberichten. Eine separate Broschüre zu einem Supportprodukt nennt außerdem Übertragung, Weiterleitung und Service-Level-Vereinbarungen; deren Umsetzung und Fristberechnung in diesem Angebot sind nicht belegt.

**Vorgeschlagener Abnahmetest**

Öffnen Sie ein allgemeines Ticket um 08:00 UTC, lösen Sie es erstmals um 09:30, öffnen Sie es um 10:00 erneut und schließen Sie es um 11:00 UTC desselben Tages endgültig. Bei Messung der verstrichenen Zeit ergeben sich 90 Minuten bis zur ersten und 180 Minuten bis zur endgültigen Lösung; beide Sprachansichten zeigen dieselbe Ticketnummer und dieselben Statusübergänge.

[Ausführliches Profil auf Englisch](../../apps/kf_shell.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/kf_shell)

## EstateFlow

Ordnen Sie Mietzahlungen den Rechnungen des Mietvertrags zu und erstellen Sie Erinnerungen in der bevorzugten Sprache des Mieters.

**Dokumentierter Ablauf**

Laut Anbieter bündelt die Mietübersicht aktive Mietverträge und zugehörige Ausgangsrechnungen, zeigt offene Beträge und ermöglicht Zahlungsbuchungen gegen Mietrechnungen. Nach Prüfung der Telefonnummer öffnet eine Erinnerung einen WhatsApp-Chat mit vorgefertigtem Text, ohne dass ein Zustellnachweis beschrieben wird.

**Vorgeschlagener Abnahmetest**

Für eine Mietrechnung über 900 sind 350 als Zahlung zugeordnet. Erstellt ein deutschsprachiger Verwalter eine Erinnerung auf Afrikaans, weist sie 550 als offen aus. Das Öffnen des Chatlinks erfasst die Übergabe, ohne eine Zahlung zu buchen.

[Ausführliches Profil auf Englisch](../../apps/nexgen_pms.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/nexgen_pms)

## trello

Verfolgen Sie eine Trello-Karte als Vorgang im ERP und erhalten Sie bei Änderungen am Board die Verknüpfungen zu ihrer Checkliste und ihren Teilaufgaben.

**Dokumentierter Ablauf**

Das Handbuch des Anbieters zeigt, wie ein Board-Webhook beim Anlegen einer Trello-Karte einen Vorgang (Issue) im ERP erstellt. Eine Checkliste auf der Karte wird zur übergeordneten Aufgabe, ihre Einträge werden zu verknüpften Teilaufgaben.

**Vorgeschlagener Abnahmetest**

Ein Board sendet dasselbe Ereignis zweimal für eine Karte mit zwei arabischen Checklisteneinträgen. In der deutschen Oberfläche erscheinen ein Vorgang, eine übergeordnete Aufgabe und zwei Unteraufgaben mit ihren ursprünglichen Titeln und Verweisen.

[Ausführliches Profil auf Englisch](../../apps/trello.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/trello)

## Visitor Management

Melden Sie einen Besucher am Empfang an, drucken Sie einen Ausweis und erfassen Sie die Abmeldung unter derselben Besuchsnummer.

**Dokumentierter Ablauf**

Am Empfangsterminal wählen Besucher ihre Kategorie, geben die Ansprechperson an, nehmen ein Foto auf und unterschreiben, bevor sie einen druckbaren Ausweis erhalten. Beim Verlassen ist der Besuch über Besuchernummer oder Mobilnummer auffindbar, und Kunden können vier Aspekte der Betreuung bewerten.

**Vorgeschlagener Abnahmetest**

Ein afrikaanssprachiger Kunde meldet sich an einer deutschsprachigen Rezeption an und erhält einen Besucherausweis. Beim Auschecken über die gedruckte Ausweisnummer gibt er vier Bewertungen ab. Derselbe Besuch erhält eine Abgangszeit und vier Zahlenwerte, und für den nächsten Gast beginnt eine leere Sitzung.

[Ausführliches Profil auf Englisch](../../apps/visitor_management.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/visitor_management)
