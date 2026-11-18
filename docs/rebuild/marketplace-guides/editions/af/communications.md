# Oproepe, opnames en boodskappe

[English](../en/communications.md) · Afrikaans · [Deutsch](../de/communications.md) · [简体中文](../zh-Hans/communications.md)

[Alle onderwerpe](README.md)

Elke voorbeeld beskryf ’n verwagte uitkoms vir die nuwe stelsel. Die volledige profiel dui aan watter besonderhede die uitgewer beskryf, watter in die bronkode voorkom en watter in ’n werkende stelsel getoets is.

## Tata Smartflo Call Integration

Begin ’n Smartflo-oproep vanuit ’n CRM-rekord en koppel die oproepbesonderhede aan die agent se aktiwiteit.

**Gedokumenteerde werkvloei**

’n Agent met ’n opgestelde telefoonnommer begin oproepe vanuit die ERP. Volgens die verskaffer haal die toepassing Smartflo se oproeplogboeke en opnames op, koppel ’n oproep aan die betrokke besigheidsrekord en laat gebruikers verslae volgens datum, status of oproeptipe filtreer.

**Voorgestelde aanvaardingstoets**

As dieselfde uitgaande oproep op twee oorvleuelende bladsye van die diensverskaffer se oproeplys verskyn, wys die verslag ná invoer een beantwoorde oproep van 48 sekondes wat aan die CRM-aktiwiteit gekoppel is. Die vertaalde status behou dieselfde oproep-ID en geskakelde nommer.

[Volledige profiel in Engels](../../apps/call_integration.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/call_integration)

## FCM Notification

Stuur ERP-kennisgewings in die ontvanger se voorkeurtaal na toestelle waarvoor kennisgewings geaktiveer is.

**Gedokumenteerde werkvloei**

Volgens die uitgewer word die stuuraksie gekoppel aan die skep van ’n Notification Log-inskrywing. ’n Toestel word via User Device aan ’n gebruiker gekoppel en ontvang dan die kennisgewing vir daardie gebruiker se ingetekende gebeurtenis.

**Voorgestelde aanvaardingstoets**

Een ontvanger kry die kennisgewing oor PO-18 op twee toestelle, in Afrikaans en Duits. Ná herverwerking bly daar een versending per toestel en verwys albei na PO-18.

[Volledige profiel in Engels](../../apps/fcm_notification.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/fcm_notification)

## Telenor Sms

Stuur ’n SMS via Telenor aan ’n kontak en onderskei tussen aanvaarding deur die SMS-diens en bevestigde aflewering.

**Gedokumenteerde werkvloei**

Volgens die uitgewer kan ERP-gebruikers SMS-boodskappe via Telenor se API aan kontakte stuur. Die openbare ondersteuningsforum gee geen besonderhede oor afleweringsbevestigings, karakterkodering of taalkeuse nie.

**Voorgestelde aanvaardingstoets**

’n Engelssprekende medewerker stuur die goedgekeurde Afrikaanse afspraakherinnering aan kontak C17. Sodra die diens die indiening bevestig, is daar een SMS met die afspraakverwysing. Aflewering op die foon wag nog op bevestiging.

[Volledige profiel in Engels](../../apps/telenor_sms.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/telenor_sms)

## Tripetto Survey Integration

Publiseer ’n opname met vertakkende vrae en groepeer die antwoorde volgens die vraag en die keuse wat elke deelnemer in hul eie taal gemaak het.

**Gedokumenteerde werkvloei**

Die opsteller maak die visuele redigeerder vanuit ’n opname oop, stoor vrae en vertakkingsreëls en publiseer die opname om ’n vormskakel te skep. Wanneer ’n deelnemer die vorm indien, stoor die ERP-stelsel die antwoord as ’n Survey Answer-rekord.

**Voorgestelde aanvaardingstoets**

Twee deelnemers kies die opsie met die kode `delivery`, een in Duits en een in Afrikaans. Hul antwoorde tel albei onder dié kode. Elke opvolgantwoord bly aan die regte deelnemer gekoppel, in die taal waarin dit geskryf is.

[Volledige profiel in Engels](../../apps/tripetto_survey.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/tripetto_survey)

## Ultramsg Whatsapp Integration

Stuur ’n WhatsApp-herinnering in gewone teks via UltraMsg wanneer ’n gebeurtenis aan die ingestelde reël voldoen.

**Gedokumenteerde werkvloei**

’n Administrateur stel die UltraMsg-instansie en toegangsteken op, kies die voorwaardes vir elke gebeurtenis en stel boodskapsjablone met invulvelde saam. Volgens die uitgewer stuur die toepassing outomaties WhatsApp-boodskappe in gewone teks, byvoorbeeld vir agterstallige bestellings en betalingsherinnerings.

**Voorgestelde aanvaardingstoets**

’n Franssprekende klant se bestelling is agterstallig. As dieselfde gebeurtenis twee keer verwerk word en UltraMsg die eerste boodskap in sy waglys plaas, bly daar een Franse herinnering met die oorspronklike bestelnommer en die status ‘in die waglys’.

[Volledige profiel in Engels](../../apps/ultramsg_whatsapp_integration.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/ultramsg_whatsapp_integration)

## Whatsapp App

Stuur gepersonaliseerde WATI-sjablone aan gekose leidrade, verkoopsgeleenthede of verskaffers en gaan die uitslag vir elke ontvanger na.

**Gedokumenteerde werkvloei**

’n Administrateur aktiveer die WATI-verbinding en koppel die parameters van ’n WATI-sjabloon aan ERP-velde. Personeel kies een of meer ontvangers uit lyste van leidrade, verkoopsgeleenthede of verskaffers en kan die boodskapaktiwiteit nagaan.

**Voorgestelde aanvaardingstoets**

’n Duitssprekende medewerker stuur ’n kennisgewing aan ’n Afrikaanssprekende verskaffer met ’n geverifieerde Namibiese telefoonnommer. Die waglys bevat een goedgekeurde Afrikaanse boodskap met die verskaffer se verwysing en dieselfde gestoorde internasionale nommer.

[Volledige profiel in Engels](../../apps/whatsapp_app.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/whatsapp_app)

## WhatsApp Integration

Stuur ’n goedgekeurde WhatsApp-sjabloon met die regte PDF-dokument wanneer ’n gekose veld of dokumentstatus verander.

**Gedokumenteerde werkvloei**

’n Administrateur skep ooreenstemmende sjablone in die ERP-stelsel en by Meta, kies die taal en koppel die betrokke PDF aan die sjabloon se kopgedeelte. Die lysinskrywing beskryf reëls wat teks- of PDF-kennisgewings stuur wanneer ’n dokument gestoor, ingedien of bygewerk word, of wanneer ’n veld verander.

**Voorgestelde aanvaardingstoets**

’n Reël vereis ’n Arabiese boodskap én ’n Arabiese PDF. As ’n Engelssprekende gebruiker die faktuur indien en net die boodskap beskikbaar is, bly die kennisgewing teruggehou. Wys watter uitleg ontbreek en laat die aanhangsel ongestuur.

[Volledige profiel in Engels](../../apps/whatsapp_integration.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/whatsapp_integration)

## Whatsapp Plus

Koppel inkomende WhatsApp-boodskappe aan klante, antwoord binne dieselfde gesprek en stuur nagegane boodskappe aan toepaslike ontvangers.

**Gedokumenteerde werkvloei**

’n Personeellid kan die klant wat reeds op rekord is aan ’n inkomende WhatsApp-boodskap herken, antwoord, medialêers aflaai of sjablone aan gekose klante of groepe stuur. Volgens die uitgewer pas die koppelvlak by die werkstasie se taal aan, en die skermbeelde wys dit in Italiaans.

**Voorgestelde aanvaardingstoets**

’n Klant stuur ’n Chinese boodskap met ’n dokument. ’n Italiaanssprekende medewerker antwoord in Chinees. Wanneer ’n Duitssprekende kollega dit oopmaak, bevat dieselfde gesprek albei boodskappe in hul oorspronklike taal en dieselfde aanhangsel met sy toegangsregte.

[Volledige profiel in Engels](../../apps/whatsapp_plus.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/whatsapp_plus)
