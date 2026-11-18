# Kommunikasie met klante

## Begin ’n telefoonoproep vanuit ’n CRM-rekord en koppel die oproepbesonderhede aan die agent se aktiwiteit

<a id="workflow-outbound-calling-and-call-dispositions"></a>

Begin die oproep vanaf die sake-inskrywing met die agent se gekonfigureerde nommer. Koppel die oproepnommer, tyd, uitkoms en gemagtigde opname aan dieselfde inskrywing.

As dieselfde uitgaande oproep op twee oorvleuelende bladsye van die diensverskaffer se oproeplys verskyn, wys die verslag ná invoer een beantwoorde oproep van 48 sekondes wat aan die CRM-aktiwiteit gekoppel is. Die vertaalde status behou dieselfde oproep-ID en geskakelde nommer.

[English](../communications.md#outbound-calling-and-call-dispositions) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#tata-smartflo-call-integration).

## Stuur ERP-kennisgewings in die ontvanger se voorkeurtaal na toestelle waarvoor kennisgewings geaktiveer is

<a id="workflow-device-notification-delivery"></a>

Registreer die toestel vir die beoogde gebruiker. ’n Kennisgewing vir dié gebruiker skep ’n afleweringspoging per toepaslike toestel.

Een ontvanger kry die kennisgewing oor PO-18 op twee toestelle, in Afrikaans en Duits. Ná herverwerking bly daar een versending per toestel en verwys albei na PO-18.

[English](../communications.md#device-notification-delivery) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#fcm-notification).

## Stuur ’n SMS aan ’n kontak en onderskei tussen aanvaarding deur die SMS-diens en bevestigde aflewering

<a id="workflow-text-message-acceptance-and-delivery"></a>

Kies die kontak, telefoonnommer en boodskap. Hou die verskaffer se aanvaarding, afleweringsbewys en enige fout as aparte uitkomste.

’n Engelssprekende medewerker stuur die goedgekeurde Afrikaanse afspraakherinnering aan kontak C17. Sodra die diens die indiening bevestig, is daar een SMS met die afspraakverwysing. Aflewering op die foon wag nog op bevestiging.

[English](../communications.md#text-message-acceptance-and-delivery) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#telenor-sms).

## Publiseer ’n opname met vertakkende vrae en groepeer die antwoorde volgens die vraag en die keuse wat elke deelnemer in hul eie taal gemaak het

<a id="workflow-branching-surveys-and-response-aggregation"></a>

Stoor die vrae en vertakkingsreëls, publiseer die vorm en koppel elke ingediende antwoord aan die gepubliseerde weergawe.

Twee deelnemers kies die opsie met die kode `delivery`, een in Duits en een in Afrikaans. Hul antwoorde tel albei onder dié kode. Elke opvolgantwoord bly aan die regte deelnemer gekoppel, in die taal waarin dit geskryf is.

[English](../communications.md#branching-surveys-and-response-aggregation) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#tripetto-survey-integration).

## Stuur ’n herinnering in gewone teks wanneer ’n gebeurtenis aan die ingestelde reël voldoen

<a id="workflow-rule-based-text-reminders"></a>

Koppel ’n dokumentgebeurtenis aan voorwaardes, ontvanger en ’n goedgekeurde boodskapsjabloon. Vul die sjabloon met die waardes vir daardie gebeurtenis in.

’n Franssprekende klant se bestelling is agterstallig. As dieselfde gebeurtenis twee keer verwerk word en die diens die eerste boodskap in sy waglys plaas, bly daar een Franse herinnering met die oorspronklike bestelnommer en die status ‘in die waglys’.

[English](../communications.md#rule-based-text-reminders) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#ultramsg-whatsapp-integration).

## Stuur gepersonaliseerde sjablone aan gekose leidrade, verkoopsgeleenthede of verskaffers en gaan die uitslag vir elke ontvanger na

<a id="workflow-personalized-recipient-messaging"></a>

Koppel sjabloonparameters aan rekordvelde en kies ontvangers uit die lys van leidrade, verkoopsgeleenthede of verskaffers. Bewaar elke versending se uitkoms.

’n Duitssprekende medewerker stuur ’n kennisgewing aan ’n Afrikaanssprekende verskaffer met ’n geverifieerde Namibiese telefoonnommer. Die waglys bevat een goedgekeurde Afrikaanse boodskap met die verskaffer se verwysing en dieselfde gestoorde internasionale nommer.

[English](../communications.md#personalized-recipient-messaging) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#whatsapp-app).

## Stuur ’n goedgekeurde sjabloon met die regte PDF-dokument wanneer ’n gekose veld of dokumentstatus verander

<a id="workflow-translated-document-message-attachments"></a>

Koppel die goedgekeurde taalvariant en PDF-aanhangsel aan die dokumentreël. Die ooreengekome stoor-, indienings- of veldverandering skep die versendingsgebeurtenis.

’n Reël vereis ’n Arabiese boodskap én ’n Arabiese PDF. As ’n Engelssprekende gebruiker die faktuur indien en net die boodskap beskikbaar is, bly die kennisgewing teruggehou. Wys watter uitleg ontbreek en laat die aanhangsel ongestuur.

[English](../communications.md#translated-document-message-attachments) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#whatsapp-integration).

## Koppel inkomende boodskappe aan klante, antwoord binne dieselfde gesprek en stuur nagegane boodskappe aan toepaslike ontvangers

<a id="workflow-incoming-customer-conversations"></a>

Koppel die inkomende boodskap aan die kliënt, maak die gesprek vir die bevoegde bediener oop en bewaar die oorspronklike boodskap en media.

’n Klant stuur ’n Chinese boodskap met ’n dokument. ’n Italiaanssprekende medewerker antwoord in Chinees. Wanneer ’n Duitssprekende kollega dit oopmaak, bevat dieselfde gesprek albei boodskappe in hul oorspronklike taal en dieselfde aanhangsel met sy toegangsregte.

[English](../communications.md#incoming-customer-conversations) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/communications.md#whatsapp-plus).
