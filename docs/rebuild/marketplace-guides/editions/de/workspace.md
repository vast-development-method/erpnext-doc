# Arbeitsbereich, Zugriff und Navigation

[English](../en/workspace.md) · [Afrikaans](../af/workspace.md) · Deutsch · [简体中文](../zh-Hans/workspace.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## Branchy

Prüfen Sie vor einer rollenbasierten Berechtigungsänderung, auf welche Datensätze die einzelnen Nutzer zugreifen dürfen.

**Dokumentierter Ablauf**

In der abgebildeten Rollenmaske legt die Administration Modul, erlaubten Datensatztyp und zulässigen Wert fest. Die Berechtigungsliste bietet Funktionen zum Anlegen und Ändern, zum gesammelten Löschen sowie zum Erstellen einer Benutzerrolle.

**Vorgeschlagener Abnahmetest**

Zwei Niederlassungen verschiedener Unternehmen tragen den Anzeigenamen „Central“. Hat der Nutzer nur Leserechte für die erste, sieht er auch nach dem Sprachwechsel ausschließlich deren Aufträge und erhält kein Genehmigungsrecht.

[Ausführliches Profil auf Englisch](../../apps/branchy.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/branchy)

## Frappe System Monitor

Lesen Sie CPU-, Speicher- und Datenträgerwerte des Hosts mit Beschriftungen und Zahlenformaten in der Sprache des Betriebspersonals.

**Dokumentierter Ablauf**

Der Marktplatzeintrag nennt CPU-, Speicher-, Datenträger- und Systemdaten des ERP-Hosts. Ein verwandtes öffentliches Projekt zeigt denselben Bildschirm und misst die Belegung von Arbeitsspeicher und Root-Dateisystem.

**Vorgeschlagener Abnahmetest**

Dieselbe Messung zeigt auf Englisch 62.5 % und auf Deutsch 62,5 % Speicherauslastung. Kernelversion und Startzeitpunkt stimmen überein.

[Ausführliches Profil auf Englisch](../../apps/frappe_system_monitor.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/frappe_system_monitor)

## Lumen Theme

Suchen Sie sprachübergreifend nach Belegen und wechseln Sie zwischen der englischen und der arabischen Arbeitsoberfläche.

**Dokumentierter Ablauf**

Lumen zeigt eine arabische Arbeitsoberfläche mit Leserichtung von rechts nach links, auf der Mitarbeitende nach dem englischen Dokumentnamen suchen und die arabische Bezeichnung sehen können. Der Anbieter beschreibt rollenabhängige Startseiten, ein optionales Umm-al-Qura-Datum unter dem gespeicherten gregorianischen Datum und ein optionales arabisches Glossar, das standorteigene Formulierungen bewahrt.

**Vorgeschlagener Abnahmetest**

Suchen Sie in zwei arabischen Arbeitsoberflächen nach dem englischen Begriff „Sales Invoice“, einmal mit und einmal ohne Zugriffsrecht. Nur die berechtigte Person sieht den übersetzten Treffer und kann denselben Belegtyp öffnen; weder die Übersetzung noch die Schreibrichtung erweitert die Rechte.

[Ausführliches Profil auf Englisch](../../apps/lumen_theme.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/lumen_theme)

## Pane View

Bearbeiten Sie einen Datensatz neben der gefilterten Liste und behalten Sie beim Sprachwechsel ungespeicherte Änderungen bei.

**Dokumentierter Ablauf**

Laut Kanak kann man eine Zeile in der gefilterten Liste auswählen und das zugehörige Formular daneben bearbeiten und speichern. Die Bereiche sind in der Größe verstellbar, die Standardliste ist wieder aufrufbar und die Ansicht unterstützt laut Anbieter auch eigene Datensatztypen.

**Vorgeschlagener Abnahmetest**

Auftrag 42 enthält eine ungespeicherte arabische Notiz. Wählt die Nutzerin nach einem Sprachwechsel Auftrag 43 und entscheidet sich im übersetzten Hinweis fürs Bleiben, bleibt Auftrag 42 mit der ursprünglichen Notiz geöffnet.

[Ausführliches Profil auf Englisch](../../apps/paneview.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/paneview)

## Persona

Starten Sie eine autorisierte Support-Sitzung als anderer Benutzer und prüfen Sie, wer sie begonnen hat.

**Dokumentierter Ablauf**

Laut Beschreibung für Version 13 können der Administrator oder ein Systemmanager vom Benutzerformular aus die Identität eines anderen Benutzers für eine Sitzung übernehmen. Das Aktivitätsprotokoll erfasst die Handlung des Mitarbeiters und die Anmeldung des Zielbenutzers getrennt. Ein Systemmanager darf nicht als anderer Systemmanager auftreten.

**Vorgeschlagener Abnahmetest**

Ein berechtigter englischsprachiger Mitarbeiter beginnt mit Begründung eine Support-Sitzung als gewöhnlicher afrikaanssprachiger Benutzer. Das Protokoll verknüpft beide Benutzerkennungen mit der unveränderten Begründung. Der getrennte Versuch eines Systemmanagers, als ein anderer Systemmanager aufzutreten, wird in beiden Sprachen abgelehnt und erzeugt keine erfolgreiche Zielanmeldung.

[Ausführliches Profil auf Englisch](../../apps/persona.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/persona)

## PibiCut

Veröffentlichen Sie einen Kurzlink und einen QR-Code, die beide auf dieselbe Zieladresse verweisen.

**Dokumentierter Ablauf**

Laut Anbieter trägt der Benutzer die Zieladresse in einen Shortener-Datensatz ein und kann ein mittig platziertes PNG-Logo mit deckend weißem Hintergrund hinzufügen. Beim Speichern entstehen eine Kurzadresse mit fünfstelligem Code und ein QR-Code für diese Adresse.

**Vorgeschlagener Abnahmetest**

Veröffentlichen Sie einen Kurzlink auf eine Adresse mit kodiertem Akzentzeichen und geordneten Abfrageparametern. Das Scannen mit arabischer Oberfläche und die manuelle Eingabe mit deutscher Oberfläche öffnen exakt dieselbe Adresse samt Kodierung und Parameterreihenfolge. Die Groß- und Kleinschreibung des Kurzcodes bleibt erhalten.

[Ausführliches Profil auf Englisch](../../apps/pibicut.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/pibicut)

## Rukntheme

Gestalten Sie den Arbeitsbereich im Erscheinungsbild Ihres Unternehmens und nutzen Sie dieselben freigegebenen Verknüpfungen in verschiedenen Sprachen und Bildschirmgrößen.

**Dokumentierter Ablauf**

Der Anbieter beschreibt ein an Bildschirmgröße und Markenauftritt anpassbares Design für die Desk-Navigation. Die Bildschirmfotos zeigen im Benutzerarbeitsbereich Verknüpfungen zu Rollen und Berechtigungen sowie im Benutzerformular eine Auswahl für den Designtyp.

**Vorgeschlagener Abnahmetest**

Wechseln Sie auf einem schmalen Bildschirm von Englisch auf Arabisch und folgen Sie einer erlaubten Verknüpfung per Tastatur. Fokus und umbrochene Beschriftung bleiben sichtbar, das Routenziel ist dasselbe und die Verwaltungsseite verweigert der eingeschränkten Rolle weiterhin den Zugriff.

[Ausführliches Profil auf Englisch](../../apps/rukntheme.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/rukntheme)

## SND Tooltip

Veröffentlichen Sie feldbezogene Hilfetexte und zeigen Sie Überschrift und Erläuterung gemeinsam in der Sprache des Lesers an.

**Dokumentierter Ablauf**

Laut Anleitung wählt der Redakteur einen Dokumenttyp und hinterlegt pro Feld in einer Untertabelle Hilfetext, Anzeigeform (Tooltip oder Popover mit Überschrift), Auslöser und Position. Nach dem Speichern öffnet er das Zielformular und aktualisiert den Cache, um die Änderung zu sehen.

**Vorgeschlagener Abnahmetest**

Fokussieren Sie ein Lieferantenfeld mit englischer Standardhilfe und freigegebener arabischer Überschrift und Beschreibung. Auf Arabisch erscheinen beide arabischen Texte, auf Afrikaans zunächst beide englischen Texte und nach Veröffentlichung und Cache-Aktualisierung beide Texte auf Afrikaans. Der Feldwert bleibt unverändert.

[Ausführliches Profil auf Englisch](../../apps/snd_tooltip.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/snd_tooltip)
