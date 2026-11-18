# Personal, Entgeltabrechnung und Lernen

[English](../en/people.md) · [Afrikaans](../af/people.md) · Deutsch · [简体中文](../zh-Hans/people.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## PCAT Exam

Werten Sie den Fragebogen anhand stabiler Antwortkennungen aus und zeigen Sie dieselbe Rangfolge der Interessen in jeder Sprache.

**Dokumentierter Ablauf**

Der Anbieter beschreibt sechs Interessenkategorien und eine Auswertung mit den drei führenden Kategorien. Ein erhaltener Programmstand sucht das Gewicht anhand des eingesandten Antworttextes und vergibt null Punkte, falls der Wortlaut nicht gefunden wird.

**Vorgeschlagener Abnahmetest**

Gleichwertige Antworten auf Englisch und Chinesisch ergeben S=6, A=4 und I=2, alle anderen Kategorien null. Beide Fassungen müssen bei übersetzten Bezeichnungen dieselbe Reihenfolge S, A, I und insgesamt 12 Punkte zeigen.

[Ausführliches Profil auf Englisch](../../apps/frappe_pcat_exam.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/frappe_pcat_exam)

## Gym Pro

Weisen Sie Mitgliedern Trainings- und Ernährungspläne zu und erfassen Sie Messwerte mit Datum und Einheit.

**Dokumentierter Ablauf**

Laut Anbieterhandbuch lässt sich aus einem bestätigten Angebot eine Mitgliedschaft anlegen. Trainer erstellen Ernährungs- und Trainingspläne, Mitglieder sehen ihre Pläne und früheren Messwerte ein, und das Unternehmen kann Standardmaßeinheiten festlegen.

**Vorgeschlagener Abnahmetest**

Bei 180 cm und 80 kg zeigt die deutsche Oberfläche einen BMI von 24,690 und die englische 24.690. Messwerte, Einheiten und Berechnung sind identisch.

[Ausführliches Profil auf Englisch](../../apps/gympro.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/gympro)

## HR Forms

Erstellen Sie Personalformulare aus freigegebenen Sprachfassungen wiederverwendbarer Vorlagen und bewahren Sie die ausgestellte Fassung auf.

**Dokumentierter Ablauf**

Im gezeigten Dienstauftragsformular enthält die Vorlage Variablen für Mitarbeiter, Stellenbezeichnung, Abteilung und Datum. Im Entwurf sind Mitarbeiterkennung, Stelle und Abteilung bereits eingesetzt, während der Datumsausdruck noch sichtbar ist.

**Vorgeschlagener Abnahmetest**

Eine englischsprachige Personalsachbearbeiterin stellt ein deutsches Formular mit Vorlagenrevision 4 aus. Nach einer geänderten Feldbeschriftung in Revision 5 zeigt das ausgestellte Formular weiterhin den deutschen Text aus Revision 4 und die ursprünglichen Mitarbeiterdaten.

[Ausführliches Profil auf Englisch](../../apps/hr_forms.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/hr_forms)

## Labor Management System

Ordnen Sie Aushilfskräfte Projekten zu und erstellen Sie Lohnabrechnungen aus genehmigten Arbeitszeiten und Korrekturen.

**Dokumentierter Ablauf**

In Micro Solutions Ablauf werden aus Einsatz und Zeitbuchungen Anwesenheit und daraus Überstunden ermittelt; Anwesenheit, Überstunden und Korrekturen fließen vor der Auszahlung in die Abrechnung ein. Der abgebildete Bericht gliedert Beträge nach Zahlungsart, Projekt und Profitcenter: Für P101 zeigt er 120 für Stundennachweise und 80 für Überstunden, ohne Währung oder Lohnformel anzugeben.

**Vorgeschlagener Abnahmetest**

Rechnen Sie acht reguläre Stunden zu je 30, zwei Überstunden zu je 45 und einen Abzug von 20 in derselben Währung ab. Auch wenn eine bereits importierte Stempelung erneut verarbeitet und die Abrechnung in der Sprache der Arbeitskraft gedruckt wird, bleibt genau eine Abrechnung mit 240 Grundlohn, 90 Überstundenvergütung und 310 Auszahlungsbetrag; Personalnummer, Kostenstelle und Stunden ändern sich nicht.

[Ausführliches Profil auf Englisch](../../apps/laborers_management.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/laborers_management)

## NextArrear

Berechnen Sie rückwirkende Gehaltsanpassungen anhand der Abrechnungen und zeigen Sie Beschäftigten Bezüge und Abzüge in ihrer bevorzugten Sprache.

**Dokumentierter Ablauf**

Laut Anbieter legt die Lohnbuchhaltung einen Eintrag in „Salary Arrear“ an und füllt die Pflichtfelder aus. Die Anwendung ruft Abrechnungen mit Bezügen und Abzügen ab, berechnet beim Speichern die Nettonachzahlung und erlaubt vor der Genehmigung eine Prüfung und Anpassung.

**Vorgeschlagener Abnahmetest**

Auf einer Abrechnung steigen die Bezüge von 2.000 auf 2.150 und die Abzüge von 250 auf 280. Ein Sprachwechsel ergibt weiterhin 150 zusätzliche Bezüge, 30 zusätzliche Abzüge und 120 netto nachzuzahlen, jeweils mit denselben Komponentenkennungen.

[Ausführliches Profil auf Englisch](../../apps/nextarrear.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/nextarrear)

## Organization Chart Advance

Suchen Sie Beschäftigte in der Unternehmenshierarchie und exportieren Sie das Organigramm in der gewählten Sprache.

**Dokumentierter Ablauf**

Kanak beschreibt, wie die Personalabteilung das Organigramm nach Unternehmen filtert, nach Beschäftigten sucht und die Hierarchie exportiert. Eine öffentliche historische Fassung baut den Baum aus den Vorgesetztenbeziehungen auf und liefert Personalkennung, Name, Bild und Funktion, wobei das Gesamtdiagramm beim ersten Wurzelknoten beginnt.

**Vorgeschlagener Abnahmetest**

Ein Unternehmen hat zwei Führungskräfte auf oberster Ebene und zwei Beschäftigte mit demselben Anzeigenamen. Bei der Suche nach Personalnummer und dem anschließenden PDF-Export auf Arabisch ist die richtige Person markiert, während beide Führungskräfte, die sichtbaren Berichtswege und die korrekte arabische Schrift erhalten bleiben.

[Ausführliches Profil auf Englisch](../../apps/organizational_chart_knk.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/organizational_chart_knk)
