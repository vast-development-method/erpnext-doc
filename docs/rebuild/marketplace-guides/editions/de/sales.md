# Vertrieb, Einzelhandel und Gastronomie

[English](../en/sales.md) · [Afrikaans](../af/sales.md) · Deutsch · [简体中文](../zh-Hans/sales.md)

[Alle Themen](README.md)

Jedes Beispiel beschreibt ein erwartetes Ergebnis für die Neuimplementierung. Das ausführliche Profil weist aus, welche Angaben vom Anbieter stammen, sich im Quellcode nachvollziehen lassen oder in einem laufenden System beobachtet wurden.

## B2B Marketing

Erstellen Sie eine Telefonkampagne aus ausgewählten Kontakten, prüfen Sie die Sperrliste und verteilen Sie zulässige Anrufe auf die Mitarbeitenden.

**Dokumentierter Ablauf**

Die Kampagnenleitung filtert Kontakte und legt im Campaign Designer die Anrufabfolge und Regeln für die Qualitätsprüfung fest. Die Anrufe werden auf Mitarbeitende verteilt, die Leitung kann Aufzeichnungen prüfen und Kampagnenleistungen über die ERP-Fakturierung abrechnen.

**Vorgeschlagener Abnahmetest**

Lässt ein Kontakt seine Rufnummer nach der Kampagnenauswahl und vor der Zuweisung sperren, muss der Anruf auch mit einem anderssprachigen Gesprächsleitfaden unterbleiben. Es erfolgt weder ein Anruf über den Anbieter noch die Erfassung einer abrechenbaren Einheit.

[Ausführliches Profil auf Englisch](../../apps/b2b_marketing.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/b2b_marketing)

## Follow Up

Planen Sie bedingte Wiedervorlagen und versenden Sie fällige Erinnerungen in der Sprache der zuständigen Person.

**Dokumentierter Ablauf**

Die Inkassoansicht des Anbieters zeigt eine zweite Mahnstufe nach zehn Tagen, eine zuständige Person für den Anruf sowie E-Mail- und SMS-Optionen. Zahlungszusagen werden separat erfasst und mit eingegangenen Zahlungen verglichen.

**Vorgeschlagener Abnahmetest**

Ein am Freitag um 09:00 Uhr versandtes Angebot ist nach zwei Arbeitstagen nachzufassen. Ohne Feiertag sehen beide Nutzer auf Afrikaans und Deutsch genau eine Wiedervorlage für Dienstag, 09:00 Uhr Windhoeker Zeit.

[Ausführliches Profil auf Englisch](../../apps/follow_up.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/follow_up)

## ERPNext IndiaMART Integration

Importieren Sie Anfragen von IndiaMART, verfolgen Sie ihren Status und übernehmen Sie eine ausgewählte Anfrage als Lead.

**Dokumentierter Ablauf**

Laut Sanskars Anleitung aktiviert die Administration die Anbindung mit der IndiaMART-Dienstadresse, dem Autorisierungsschlüssel und der registrierten Mobilnummer. Nach Anbieterangaben werden Anfragen alle fünf Minuten aktualisiert; das Vertriebsteam kann auch historische Anfragen für einen Siebentageszeitraum abrufen, den Status prüfen und eine Anfrage in einen Lead umwandeln.

**Vorgeschlagener Abnahmetest**

Importieren Sie INQ-47 für Verkäufer A über den planmäßigen Abruf und rückwirkend für den überlappenden Zeitraum. Wird die Anfrage in zwei Oberflächensprachen in einen Lead umgewandelt, bleibt genau eine Anfrage mit demselben Lead bestehen; der Hindi-Produktname und die externe Anfrage-ID bleiben erhalten.

[Ausführliches Profil auf Englisch](../../apps/indiamart.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/indiamart)

## Insightly

Verfolgen Sie Aufträge eines Kunden oder Einkäufe bei einem Lieferanten von den Summen im Dashboard bis zu den einzelnen Belegen.

**Dokumentierter Ablauf**

Der Anbieter beschreibt Kunden- und Lieferantenübersichten mit Datumsfiltern, Belegzahlen, Beträgen und Zugriff auf die zugehörigen Einzelvorgänge. Im untersuchten öffentlichen Quellstand zählen bei bestätigten Aufträgen das Transaktionsdatum, bei Rechnungen das Buchungsdatum und bei Zahlungsanforderungen der Erstellungszeitpunkt; die Rechnungsübersicht unterscheidet offene und bezahlte Beträge.

**Vorgeschlagener Abnahmetest**

Öffnen Sie die Auftragskachel für einen Kunden mit zwei sichtbaren, bestätigten Aufträgen über zusammen 140 EUR und einem dritten Auftrag im Entwurf. Mit demselben Datumsfilter zeigt sie 2 und 140 EUR; auch nach einem Sprachwechsel erscheinen in der Detailansicht genau dieselben beiden Auftragsnummern.

[Ausführliches Profil auf Englisch](../../apps/insightly.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/insightly)

## Lumen Restaurants

Führen Sie eine Tischbestellung über mehrere Küchenbons hinweg und rechnen Sie sie an der Kasse des Standorts ab.

**Dokumentierter Ablauf**

Lumen beschreibt offene Tischbestellungen über mehrere Küchenbons hinweg: Kostenlose Optionen werden als Küchenanweisung erfasst, kostenpflichtige Zusätze erscheinen als eigene Position auf der abschließenden Kassenrechnung. Der öffentliche Quellstand prüft auf bereits offene Tischbestellungen; laut Anbieter sind Restaurantansichten, Reservierungsseite und Kassenbelege auf Englisch und Arabisch verfügbar.

**Vorgeschlagener Abnahmetest**

Bestellen Sie ein Gericht für 60 mit einer kostenpflichtigen Beilage für 5 und einem kostenlosen Küchenhinweis; senden Sie die Runde zweimal mit derselben Versand-ID und kassieren Sie die Bestellung ab. Es entstehen ein Küchenbon und eine Kassenrechnung mit 65 vor Steuern; die arabische Küchenanzeige und die englische Kasse verwenden dieselben Optionskennungen und Positionsbeträge.

[Ausführliches Profil auf Englisch](../../apps/lumen_restaurants.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/lumen_restaurants)

## LumenPOS

Führen Sie eine Kassenschicht in der Sprache des Kassenpersonals und gleichen Sie die während eines Netzausfalls gespeicherten Verkäufe ab.

**Dokumentierter Ablauf**

Laut Handbuch eröffnet das Kassenpersonal eine Schicht, scannt Artikel und nimmt die Zahlung entgegen. Die Kasse verfolgt zulässige Offline-Verkäufe bis zur Bestätigung, zeigt die gebuchte Rechnungsnummer oder den Ablehnungsgrund und verlangt vor Schichtabschluss den Upload ausstehender Verkäufe.

**Vorgeschlagener Abnahmetest**

Eine Kassiererin verkauft offline zwei Einheiten auf Arabisch und wechselt auf Deutsch. Geht die Upload-Bestätigung verloren, erzeugt ein erneuter Versuch insgesamt nur eine Rechnung und eine Lagerbewegung über zwei Einheiten, und der deutsche Status verweist auf diese Rechnung bei unveränderter Belegsprache.

[Ausführliches Profil auf Englisch](../../apps/lumenpos.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/lumenpos)

## ONDC Seller App

Veröffentlichen Sie einen Verkäuferkatalog im ONDC-Netz und gleichen Sie Käuferbestätigungen mit den ERP-Aufträgen ab.

**Dokumentierter Ablauf**

mytra.money beschreibt eine Vorabfassung für Version 14, mit der Verkäufer auf Frappe Cloud Waren oder Dienstleistungen über ONDC anbieten können. Eigenbetrieb ist als geplant aufgeführt, während Angaben zur Version des Einzelhandelsprotokolls und den verarbeiteten Nachrichten fehlen.

**Vorgeschlagener Abnahmetest**

Im englischen und im Hindi-Katalog steht dieselbe Artikelkennung. Wird die Bestätigung für zwei Einheiten nach einem Sprachwechsel erneut zugestellt, bleibt das Ergebnis identisch und genau ein Auftrag reserviert die zwei Einheiten.

[Ausführliches Profil auf Englisch](../../apps/ondc_seller_app.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/ondc_seller_app)

## Retail Suite

Scannen Sie Artikel mit Serien- oder Chargennummer, erfassen Sie Verkäufe und Retouren und gleichen Sie jede Zahlungsart beim Schichtabschluss ab.

**Dokumentierter Ablauf**

Der Anbieter beschreibt arabische und englische Kassenoberflächen und einen Schichtabschluss je Zahlungsart. Eine historische Quellkopie berechnet die Differenz als gezählten Betrag abzüglich Sollbetrag und schaltet an der Kasse zwischen Englisch und Urdu um. Bei fehlender Übersetzung erscheint zunächst der englische Text, ersatzweise der Meldungsschlüssel.

**Vorgeschlagener Abnahmetest**

Eröffnen Sie die Schicht mit 100,00 in bar, nehmen Sie 200,00 bar und 50,00 per Karte ein und erstatten Sie 30,00 in bar. Bei gezählten 268,00 in bar und bestätigten 50,00 per Karte zeigen die arabische und englische Ansicht denselben Sollbestand von 270,00, eine Kassendifferenz von −2,00 und keine Kartendifferenz.

[Ausführliches Profil auf Englisch](../../apps/retail.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/retail)

## Sajha Menu

Leiten Sie eine Tischbestellung an Küche und Bar und rechnen Sie den Besuch mit der zugehörigen Gästerechnung ab.

**Dokumentierter Ablauf**

Der Anbieter nennt Bestellungen per QR-Code, Tablet oder Kasse sowie Tischverwaltung und Abrechnung. In einer öffentlichen Quellkopie mit Tuna als angegebenem Herausgeber trennt der Bestelldienst Speisen und Barartikel nach Kategorie, erstellt die entsprechenden Bons und ergänzt die Mengen auf der Tischbestellung.

**Vorgeschlagener Abnahmetest**

Geben Sie für einen Tisch auf Nepali zwei Portionen desselben Gerichts und ein Getränk auf und übermitteln Sie die Bestellung zweimal mit derselben Vorgangskennung. Die englischsprachige Küche erhält zwei Portionen, die deutschsprachige Bar ein Getränk und die Rechnung umfasst genau drei Einheiten mit den ursprünglichen Artikelcodes.

[Ausführliches Profil auf Englisch](../../apps/sajha_menu.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/sajha_menu)

## Sales AI

Prüfen Sie die vorgeschlagene Angebotserinnerung in der Sprache des Empfängers und geben Sie den genauen Wortlaut vor dem Versand frei.

**Dokumentierter Ablauf**

Der Anbieter beschreibt Abfragen zu Angeboten, Aufträgen und Rechnungen für den Vertrieb sowie einen getrennten Portalassistenten für die eigenen Belege des jeweiligen Kunden. Automatisierte Abläufe lassen sich zeit- oder ereignisgesteuert starten, vorab testen und zur Freigabe anhalten. Ausführungen und Aktionen sind protokolliert.

**Vorgeschlagener Abnahmetest**

Ein deutschsprachiger Vertriebsleiter prüft eine Angebotserinnerung für einen afrikaanssprachigen Kunden im Probelauf und gibt anschließend den genauen Text auf Afrikaans frei. Der Probelauf versendet nichts, auch bei erneutem Zeitplanlauf wird die freigegebene Nachricht nur einmal zugestellt und jede Textänderung benötigt eine neue Freigabe.

[Ausführliches Profil auf Englisch](../../apps/sales_ai.md) · [Marktplatzseite des Anbieters](https://cloud.frappe.io/marketplace/apps/sales_ai)
