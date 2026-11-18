# Arbeitsplatz und Berechtigungen

## Prüfen Sie vor einer rollenbasierten Berechtigungsänderung, auf welche Datensätze die einzelnen Nutzer zugreifen dürfen

<a id="workflow-branch-scoped-access-review"></a>

Ein Profil nach Aktion, Datensatzart und zugelassenem Datensatzwert begrenzen. Die resultierenden Berechtigungen vor Übernahme der genehmigten Änderung prüfen.

Zwei Niederlassungen verschiedener Unternehmen tragen den Anzeigenamen „Central“. Hat der Nutzer nur Leserechte für die erste, sieht er auch nach dem Sprachwechsel ausschließlich deren Aufträge und erhält kein Genehmigungsrecht.

[English](../workspace.md#branch-scoped-access-review) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#branchy).

## Lesen Sie CPU-, Speicher- und Datenträgerwerte des Hosts mit Beschriftungen und Zahlenformaten in der Sprache des Betriebspersonals

<a id="workflow-system-resource-monitoring"></a>

CPU-, Speicher- und Datenträgerauslastung für den zulässigen Host abfragen. Werte anhand von Messzeit, Einheit und Umfang vergleichen.

Dieselbe Messung zeigt auf Englisch 62.5 % und auf Deutsch 62,5 % Speicherauslastung. Kernelversion und Startzeitpunkt stimmen überein.

[English](../workspace.md#system-resource-monitoring) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#frappe-system-monitor).

## Suchen Sie sprachübergreifend nach Belegen und wechseln Sie zwischen der englischen und der arabischen Arbeitsoberfläche

<a id="workflow-multilingual-workspace-search"></a>

Nach lokaler Bezeichnung oder zulässigem Alias suchen und das Ziel über seine stabile Typkennung öffnen. Leserichtung und Rollenbeschränkungen beibehalten.

Suchen Sie in zwei arabischen Arbeitsoberflächen nach dem englischen Begriff „Sales Invoice“, einmal mit und einmal ohne Zugriffsrecht. Nur die berechtigte Person sieht den übersetzten Treffer und kann denselben Belegtyp öffnen; weder die Übersetzung noch die Schreibrichtung erweitert die Rechte.

[English](../workspace.md#multilingual-workspace-search) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#lumen-theme).

## Bearbeiten Sie einen Datensatz neben der gefilterten Liste und behalten Sie beim Sprachwechsel ungespeicherte Änderungen bei

<a id="workflow-split-view-record-editing"></a>

Eine gefilterte Listenzeile auswählen und das berechtigte Formular daneben öffnen. Den gewählten Datensatz speichern und den Filter bei der Rückkehr erhalten.

Auftrag 42 enthält eine ungespeicherte arabische Notiz. Wählt die Nutzerin nach einem Sprachwechsel Auftrag 43 und entscheidet sich im übersetzten Hinweis fürs Bleiben, bleibt Auftrag 42 mit der ursprünglichen Notiz geöffnet.

[English](../workspace.md#split-view-record-editing) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#pane-view).

## Starten Sie eine autorisierte Support-Sitzung als anderer Benutzer und prüfen Sie, wer sie begonnen hat

<a id="workflow-delegated-support-sessions"></a>

Eine berechtigte Person startet eine Support-Sitzung im Benutzerkonto. Das Auditprotokoll erfasst die handelnde Person und das Zielkonto getrennt. Wer die Rolle System Manager hat, darf kein anderes Konto mit dieser Rolle übernehmen.

Ein berechtigter englischsprachiger Mitarbeiter beginnt mit Begründung eine Support-Sitzung als gewöhnlicher afrikaanssprachiger Benutzer. Das Protokoll verknüpft beide Benutzerkennungen mit der unveränderten Begründung. Der getrennte Versuch eines Systemmanagers, als ein anderer Systemmanager aufzutreten, wird in beiden Sprachen abgelehnt und erzeugt keine erfolgreiche Zielanmeldung.

[English](../workspace.md#delegated-support-sessions) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#persona).

## Veröffentlichen Sie einen Kurzlink und einen QR-Code, die beide auf dieselbe Zieladresse verweisen

<a id="workflow-short-links-and-scannable-destinations"></a>

Das Ziel einem Kurzcode zuordnen und einen scannbaren Code für dieselbe Adresse erzeugen. Bei der Auflösung Ziel und Zugriffsrichtlinie prüfen.

Veröffentlichen Sie einen Kurzlink auf eine Adresse mit kodiertem Akzentzeichen und geordneten Abfrageparametern. Das Scannen mit arabischer Oberfläche und die manuelle Eingabe mit deutscher Oberfläche öffnen exakt dieselbe Adresse samt Kodierung und Parameterreihenfolge. Die Groß- und Kleinschreibung des Kurzcodes bleibt erhalten.

[English](../workspace.md#short-links-and-scannable-destinations) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#pibicut).

## Gestalten Sie den Arbeitsbereich im Erscheinungsbild Ihres Unternehmens und nutzen Sie dieselben freigegebenen Verknüpfungen in verschiedenen Sprachen und Bildschirmgrößen

<a id="workflow-accessible-workspace-navigation"></a>

Das passende Design und zulässige Verknüpfungen anwenden. Bei Tastatur-, Touch- und Screenreader-Navigation gelten dieselben Ziele und Berechtigungen.

Wechseln Sie auf einem schmalen Bildschirm von Englisch auf Arabisch und folgen Sie einer erlaubten Verknüpfung per Tastatur. Fokus und umbrochene Beschriftung bleiben sichtbar, das Routenziel ist dasselbe und die Verwaltungsseite verweigert der eingeschränkten Rolle weiterhin den Zugriff.

[English](../workspace.md#accessible-workspace-navigation) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#rukntheme).

## Veröffentlichen Sie feldbezogene Hilfetexte und zeigen Sie Überschrift und Erläuterung gemeinsam in der Sprache des Lesers an

<a id="workflow-translated-field-guidance"></a>

Hilfetext an das stabile Feld der Datensatzart binden. Auslöser, Position, Sprache und Darstellungsform einstellen und das tatsächliche Formular nach Veröffentlichung prüfen.

Fokussieren Sie ein Lieferantenfeld mit englischer Standardhilfe und freigegebener arabischer Überschrift und Beschreibung. Auf Arabisch erscheinen beide arabischen Texte, auf Afrikaans zunächst beide englischen Texte und nach Veröffentlichung und Cache-Aktualisierung beide Texte auf Afrikaans. Der Feldwert bleibt unverändert.

[English](../workspace.md#translated-field-guidance) · [Quellenbelege](../../../rebuild/marketplace-guides/editions/de/workspace.md#snd-tooltip).
