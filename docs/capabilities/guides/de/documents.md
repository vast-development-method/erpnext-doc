# Dokumente und Unterschriften

## Filtern Sie die zu druckenden Datensätze und laden Sie ihre PDFs nach dem gewählten Feld gruppiert als ZIP-Archiv herunter

<a id="workflow-bulk-document-rendition"></a>

Datensatzart, Filter, Druckformat und Gruppierung wählen. Erfolgreiche PDFs bündeln und Fehler je Einzeldokument erfassen.

Verteilen sich 55 berechtigte Dokumente auf mehrere Ergebnisseiten und scheitert die PDF-Erstellung einmal, enthält das Archiv 54 PDFs. Das Verzeichnis weist den Teilerfolg, den Fehler mit Dokumentkennung und die jeweilige PDF-Sprache aus und hält unterschiedliche Gruppen mit ähnlichen Unicode-Namen getrennt.

[English](../documents.md#bulk-document-rendition) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/documents.md#dynamic-bulk-pdf-downloader).

## Verfolgen Sie die Meilensteine eines Dokuments und werten Sie die Zeit zwischen den einzelnen Schritten aus

<a id="workflow-milestone-progress-measurement"></a>

Datumsfeld, Meilensteine, Bedingungen und Fortschrittswerte festlegen. Beim Erreichen eines Meilensteins Zeitpunkt und verantwortliche Person erfassen.

Bei festem absolutem Fortschrittswert je Meilenstein wird ein Dokument um 08:00 UTC genehmigt und am selben Tag um 15:03 UTC als geliefert markiert. Es zeigt dann 100 % Fortschritt und eine Dauer von 423 Minuten. Das erneut verarbeitete Lieferereignis erzeugt keinen weiteren Eintrag, und ein übersetzter Meilensteinname ändert die Dauer nicht.

[English](../documents.md#milestone-progress-measurement) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/documents.md#document-progress-tracker).

## Weisen Sie dem Dokument eine unterzeichnende Person zu und senden Sie dem Empfänger genau die signierte PDF-Datei

<a id="workflow-signed-document-dispatch"></a>

Die berechtigte unterzeichnende Person mit der Rechnung verbinden. Die signierte Datei erhält eine eigene Identität und kann erneut heruntergeladen oder versandt werden.

Werden zwei E-Mails in verschiedenen Sprachen mit derselben signierten deutschen Rechnung versandt, müssen die Prüfsummen beider Anhänge mit der archivierten signierten PDF-Datei übereinstimmen. Die Sprache der E-Mail ändert weder Datei noch Unterzeichner und löst keinen weiteren Signaturvorgang aus.

Nach einer Zeitüberschreitung kann die Signatur bereits erstellt sein. Zuerst die ursprüngliche Anfrage abgleichen. Ist die signierte Fassung unverändert, die Vertrauenskette aber ungeklärt, bleiben Datei und Prüfergebnis erhalten. Verlangt die Freigaberegel eine vertrauenswürdige Signatur, wartet der Versand auf die Bestätigung. Ein erneuter E-Mail-Versand verwendet dieselbe freigegebene Datei.

[English](../documents.md#signed-document-dispatch) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/documents.md#digital-signature).

## Weisen Sie jedem Unterzeichner die vorgesehenen Felder zu und bewahren Sie Sprache und Inhalt der unterzeichneten Vereinbarung

<a id="workflow-multiple-signer-agreement-completion"></a>

Die Vereinbarung aus der Vorlage erstellen und Felder den Empfängern zuweisen. Ablehnung mit Grund getrennt von der abgeschlossenen Unterzeichnung führen.

Zwei Personen unterzeichnen dieselbe afrikaanssprachige Vereinbarung, eine mit deutscher, die andere mit englischer Bedienoberfläche. Nach Abschluss ihrer jeweiligen Felder gibt es ein fertiges Dokument mit beiden Zuordnungen und demselben Prüfwert der Vereinbarung.

[English](../documents.md#multiple-signer-agreement-completion) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/documents.md#esign-app).

## Gestalten Sie eine zweisprachige Rechnung, prüfen Sie die PDF-Vorschau und versenden Sie sie in der bevorzugten Sprache des Empfängers

<a id="workflow-bilingual-document-layout"></a>

Das Layout an Belegfelder binden und die Vorschau prüfen. Vor der Ausgabe das freigegebene ein- oder zweisprachige Format wählen.

Eine englischsprachige Sachbearbeiterin druckt eine Rechnung mit einem Namen in zwei Schriftsystemen und zwei Steuerpositionen mit einer arabisch-englischen Vorlage. Beide Überschriften erscheinen, die Steuerbeträge stimmen mit der Buchung überein und der gescannte QR-Code liefert die ursprünglichen signierten Daten.

[English](../documents.md#bilingual-document-layout) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/documents.md#lumenpdf-studio).
