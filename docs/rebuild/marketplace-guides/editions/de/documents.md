# Dokumente, Unterschriften und Druck

[English](../en/documents.md) · [Afrikaans](../af/documents.md) · Deutsch · [简体中文](../zh-Hans/documents.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## Dynamic Bulk PDF Downloader

Filtern Sie die zu druckenden Datensätze und laden Sie ihre PDFs nach dem gewählten Feld gruppiert als ZIP-Archiv herunter.

**Dokumentierter Ablauf**

Die Bedienperson wählt Dokumenttyp, Druckformat, Filter und bei Bedarf ein Gruppierungsfeld. Der Hintergrunddienst der untersuchten Version rendert die gefundenen Datensätze als PDFs, packt erfolgreiche Ausgaben in ein ZIP-Archiv und protokolliert Fehler je Dokument.

**Vorgeschlagener Abnahmetest**

Verteilen sich 55 berechtigte Dokumente auf mehrere Ergebnisseiten und scheitert die PDF-Erstellung einmal, enthält das Archiv 54 PDFs. Das Verzeichnis weist den Teilerfolg, den Fehler mit Dokumentkennung und die jeweilige PDF-Sprache aus und hält unterschiedliche Gruppen mit ähnlichen Unicode-Namen getrennt.

[Ausführliches Profil auf Englisch](../../apps/bulk_download.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/bulk_download)

## Document Progress Tracker

Verfolgen Sie die Meilensteine eines Dokuments und werten Sie die Zeit zwischen den einzelnen Schritten aus.

**Dokumentierter Ablauf**

Die Prozessverantwortlichen wählen Dokumenttyp, Datumsfeld, Meilensteine, Bedingungen und Prozentsätze. Bei erfüllter Bedingung aktualisiert die Anwendung den Fortschritt und erfasst unter anderem Meilenstein, Nutzer, Zeitstempel und verstrichene Minuten oder Tage.

**Vorgeschlagener Abnahmetest**

Bei festem absolutem Fortschrittswert je Meilenstein wird ein Dokument um 08:00 UTC genehmigt und am selben Tag um 15:03 UTC als geliefert markiert. Es zeigt dann 100 % Fortschritt und eine Dauer von 423 Minuten. Das erneut verarbeitete Lieferereignis erzeugt keinen weiteren Eintrag, und ein übersetzter Meilensteinname ändert die Dauer nicht.

[Ausführliches Profil auf Englisch](../../apps/document_progress_tracker.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/document_progress_tracker)

## Digital Signature

Weisen Sie dem Dokument eine unterzeichnende Person zu und senden Sie dem Empfänger genau die signierte PDF-Datei.

**Dokumentierter Ablauf**

Für die unterzeichnende Person wird ein DSC-User-Datensatz mit Unterschriftsbild und Passwort angelegt. In der Anleitung wird dieser Datensatz mit der Rechnung verknüpft. Über die Funktion „Signed PDF“ und das Passwort entsteht eine Datei zum Herunterladen oder zum Versand per E-Mail.

**Vorgeschlagener Abnahmetest**

Werden zwei E-Mails in verschiedenen Sprachen mit derselben signierten deutschen Rechnung versandt, müssen die Prüfsummen beider Anhänge mit der archivierten signierten PDF-Datei übereinstimmen. Die Sprache der E-Mail ändert weder Datei noch Unterzeichner und löst keinen weiteren Signaturvorgang aus.

[Ausführliches Profil auf Englisch](../../apps/dsc.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/dsc)

## Esign App

Weisen Sie jedem Unterzeichner die vorgesehenen Felder zu und bewahren Sie Sprache und Inhalt der unterzeichneten Vereinbarung.

**Dokumentierter Ablauf**

Der vom Anbieter verlinkte Quelltext kopiert das PDF-Layout aus der Vorlage, speichert die Zuweisungen an die Empfänger beim Versand und erfasst einen Ablehnungsgrund getrennt vom Abschluss und der PDF-Signatur.

**Vorgeschlagener Abnahmetest**

Zwei Personen unterzeichnen dieselbe afrikaanssprachige Vereinbarung, eine mit deutscher, die andere mit englischer Bedienoberfläche. Nach Abschluss ihrer jeweiligen Felder gibt es ein fertiges Dokument mit beiden Zuordnungen und demselben Prüfwert der Vereinbarung.

[Ausführliches Profil auf Englisch](../../apps/esign_app.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/esign_app)

## LumenPDF Studio

Gestalten Sie eine zweisprachige Rechnung, prüfen Sie die PDF-Vorschau und versenden Sie sie in der bevorzugten Sprache des Empfängers.

**Dokumentierter Ablauf**

Laut Anbieter kann die Systemverwaltung einen Standardentwurf anpassen, Rechnungs- oder Berichtsfelder einbinden und eine PDF-Vorschau öffnen. Beim Drucken lässt sich ein arabisches oder zweisprachiges Format wählen und das Dokument herunterladen oder als E-Mail-Anhang versenden.

**Vorgeschlagener Abnahmetest**

Eine englischsprachige Sachbearbeiterin druckt eine Rechnung mit einem Namen in zwei Schriftsystemen und zwei Steuerpositionen mit einer arabisch-englischen Vorlage. Beide Überschriften erscheinen, die Steuerbeträge stimmen mit der Buchung überein und der gescannte QR-Code liefert die ursprünglichen signierten Daten.

[Ausführliches Profil auf Englisch](../../apps/lumenpdf.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/lumenpdf)
