# Ontleding, KI en kalenders

[English](../en/data.md) · Afrikaans · [Deutsch](../de/data.md) · [简体中文](../zh-Hans/data.md)

[Alle onderwerpe](README.md)

Elke voorbeeld beskryf ’n verwagte uitkoms vir die nuwe stelsel. Die volledige profiel dui aan watter besonderhede die uitgewer beskryf, watter in die bronkode voorkom en watter in ’n werkende stelsel getoets is.

## BigQuery Connector

Voer geselekteerde ERP-velde na BigQuery uit en hervat ’n onderbroke oordrag vanaf die laaste bevestigde kontrolepunt.

**Gedokumenteerde werkvloei**

Die uitgewer se uitvoervorm koppel ’n brontabel aan ’n benoemde bestemming, byvoorbeeld tabUser aan user, en laat die operateur kolomme en ’n filter kies. Die inkrementele instellings wys die interval, laaste sinchronisasietyd, laaste gesinchroniseerde ID en skeduleerderslot.

**Voorgestelde aanvaardingstoets**

INV-001 en INV-002 het dieselfde wysigingstyd en die bladsygrootte is een. Herbegin die uitvoer in Duits nadat die eerste ry geskryf is maar voordat die kontrolepunt gestoor is. Elke faktuurnommer verskyn presies een keer en die kolomname bly dieselfde.

[Volledige profiel in Engels](../../apps/frappe_bigquery.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/frappe_bigquery)

## InstaGPT

Maak ’n kletsvenster vanaf die ERP se navigasiebalk oop en stuur ’n boodskap in die taal van jou keuse.

**Gedokumenteerde werkvloei**

Volgens Brandimic stel ’n System Manager of Administrator die sleutel, model en temperatuur op ’n skaal van 0–200 op voordat personeel vanaf die kletsvenster in die navigasiebalk boodskappe stuur. OpenAI dokumenteer ’n skaal van 0–2 vir die temperatuurparameter van Chat Completions; die toepassing se omskakeling en die dienspunte wat dit gebruik, is nie bevestig nie.

**Voorgestelde aanvaardingstoets**

Druk in die Duitse kletsvenster op Enter terwyl jy met die Chinese invoermetode ’n karakter saamstel, voltooi die sin en kies dan Stuur. Die eerste Enter bevestig net die karakter; slegs een boodskap word gestuur en die oorspronklike Chinese teks bly behoue ongeag die versoekte antwoordtaal.

[Volledige profiel in Engels](../../apps/instagpt.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/instagpt)

## Islamic Calendar

Voer ’n datum volgens die Hidjri-kalender in en kontroleer dieselfde dag op die Gregoriaanse kalender.

**Gedokumenteerde werkvloei**

Kanak beskryf ’n Hidjri-datumkieser waarmee gebruikers in ERP-vorms tussen Hidjri- en Gregoriaanse datums kan wissel. ’n Openbare kopie wat Kanak as ontwikkelaar vermeld, hou die vertoon- en datumkieserformate apart en gebruik ’n ingeslote Umm al-Qura-tabel van maandbegindatums vir omskakeling.

**Voorgestelde aanvaardingstoets**

Voer 1448-06-08 AH volgens die aangehaalde Umm al-Qura-tabel in en wissel na die Gregoriaanse kalender: die datum is 2026-11-18. Maak die veld weer oop en wissel terug; ’n ander taal of syferstyl moet steeds dieselfde dag, 1448-06-08 AH, oplewer.

[Volledige profiel in Engels](../../apps/islamic_calendar.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/islamic_calendar)

## Nepali Calendar

Voer ’n datum volgens die Nepalese kalender in en vind dieselfde rekord met die Gregoriaanse datum.

**Gedokumenteerde werkvloei**

Kanak se handleiding wys hoe ’n gebruiker ’n Nepalese datum in ’n datumveld kies en in dieselfde vorm na die ooreenstemmende Gregoriaanse datum oorskakel. Die uitgewer noem verkope, aankope, menslike hulpbronne en rekeningkunde as toepassingsgebiede.

**Voorgestelde aanvaardingstoets**

Een gebruiker teken die aankoopdatum as 1 Baisakh 2081 aan en ’n ander soek volgens die Gregoriaanse datum 13 April 2024. Dieselfde rekord verskyn, en wanneer die kalender teruggeskakel word, wys dit weer 1 Baisakh 2081, ongeag die koppelvlaktaal.

[Volledige profiel in Engels](../../apps/nepali_calendar.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/nepali_calendar)

## ChatNext

Vra ’n ERP-vraag in een taal en versoek ’n antwoord in ’n ander taal terwyl die oorspronklike gesprek behoue bly.

**Gedokumenteerde werkvloei**

Die lysinskrywing beskryf hoe ’n gebruiker ’n ERP-vraag binne ’n bepaalde konteks stel. ’n Openbare historiese kopie stoor die gebruiker se boodskap in die gespreksessie, stuur dit saam met die gesprekgeskiedenis en die huidige skermkonteks na ’n afsonderlike diens en teken die antwoord as ’n kletsbotboodskap aan.

**Voorgestelde aanvaardingstoets**

’n Gebruiker met ’n Duitse koppelvlak vra in Afrikaans na die uitstaande bedrag op ’n faktuur wat hulle mag sien. Die Afrikaanse antwoord verwys na die bronveld, die oorspronklike vraag bly in die gesprek en die faktuur verander nie.

[Volledige profiel in Engels](../../apps/nextai.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/nextai)
