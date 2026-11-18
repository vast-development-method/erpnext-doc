# Aankope, gehalte en voorraad

[English](../en/supply.md) · Afrikaans · [Deutsch](../de/supply.md) · [简体中文](../zh-Hans/supply.md)

[Alle onderwerpe](README.md)

Elke voorbeeld beskryf ’n verwagte uitkoms vir die nuwe stelsel. Die volledige profiel dui aan watter besonderhede die uitgewer beskryf, watter in die bronkode voorkom en watter in ’n werkende stelsel getoets is.

## Advance Authorisation Licence

Toets elke faktuurreël aan die oorblywende hoeveelheid en waarde op die betrokke invoer- of uitvoerlisensie.

**Gedokumenteerde werkvloei**

Die gebruiker koppel ’n invoerfaktuurreël aan ’n lisensie en teken die CIF- en FOB-waardes aan. Boeking werk die beskikbare toekenning vir daardie item by, terwyl ’n uitvoerverkoopsfaktuur die uitgevoerde hoeveelheid en waarde teen die lisensie aanteken.

**Voorgestelde aanvaardingstoets**

Met 50 kg en 450 geldeenhede op die lisensie beskikbaar, moet ’n invoer van 40 kg ter waarde van 451 geweier word. Die saldo bly 50 kg en 450, en die Hindi- en Engelse boodskappe dui dieselfde lisensie en oorskryding aan.

[Volledige profiel in Engels](../../apps/advance_authorisation_licence.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/advance_authorisation_licence)

## ProcurementNext

Vergelyk ’n gesimuleerde bestelorder met die verwagte vraag voordat jy die bestelling by die verskaffer plaas.

**Gedokumenteerde werkvloei**

Die beplanner kies die voorspellingstydperk en -metode, vergelyk voorraad, verwagte ontvangste, vraag en onvervulde vraag per item en kan bondelkomponente insluit. In dieselfde beplanningskerm kan die aankoper die verskaffer kies en aandui teen wanneer die goedere benodig word.

**Voorgestelde aanvaardingstoets**

Met 18 eenhede op hande, 6 wat betyds aankom en ’n vraag van 30 is daar sonder agterstallige bestellings 6 eenhede se verlore verkope. Simuleer ’n verdere ontvangs van 10 voor die vraagdatum: die verwagte verlore verkope daal tot nul en die eindvoorraad is 4. Geen bestelorder word ingedien nie en ’n taalwisseling verander geen hoeveelhede of datums nie.

[Volledige profiel in Engels](../../apps/advanced_procurement.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

## AQL Quality Assurance By HavaraTech

Gebruik die steekproefplan en aangetekende gebreke om te besluit hoe die geïnspekteerde lot hanteer moet word.

**Gedokumenteerde werkvloei**

Die inspekteur teken lesings vir ’n steekproef uit die lot aan. In die herwonne bronkode word die hele ontvangde hoeveelheid as afgekeur geboek wanneer die aankoopontvangs aan ’n afgekeurde inspeksie gekoppel is, en die aanvaarde hoeveelheid is nul.

**Voorgestelde aanvaardingstoets**

Wanneer ’n ontvangsreël vir 12 eenhede aan ’n ingediende, afgekeurde inspeksie gekoppel is, boek die herwonne weergawe 0 as aanvaar en 12 as afgekeur. Die Duitse en Engelse verslae moet dieselfde uitkomskode, steekproefverwysings en hoeveelhede toon.

[Volledige profiel in Engels](../../apps/aql_quality_assurance.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/aql_quality_assurance)

## Dairy Management

Bereken die prys van elke melkinsameling uit die gehaltemetings en rekonsilieer die hoeveelheid wat by die ontvangspunt afgelewer is.

**Gedokumenteerde werkvloei**

Wanneer ’n melkinskrywing in die herwonne weergawe gestoor word, kies die stelsel ’n ingediende tarief vir die melktipe, insamelingsmagasyn en datum. Die vereenvoudigde plan bereken die waarde uit die vet- en vetvrye-vastestofpersentasies, die twee komponenttariewe en die aangetekende volume.

**Voorgestelde aanvaardingstoets**

Met vet- en vetvrye-vastestof-tariewe van 80 en 30, lesings van 4,0% en 8,5% en ’n volume van 100, is die eenheidsprys 5,75 en die totaal 575 voor enige aftrekkings of aansporings. Die desimaalteken mag met die taal verander, maar die bedrag bly dieselfde en ’n herhaalde toestellesing mag nie die insameling verdubbel nie.

[Volledige profiel in Engels](../../apps/dairy.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/dairy)

## Official EasyEcom Integration

Koppel kanaalprodukte en liggings aan die regte artikels en pakhuise sodat ontvangste en bestellings korrek geboek word.

**Gedokumenteerde werkvloei**

Volgens Incirco se gids begin bestellings tussen ondernemings in die ERP en verbruikersbestellings in EasyEcom. Pakhuispersoneel koppel die EasyEcom-ligging aan die ERP-pakhuis sodat die voltooide ontvangs by die regte bestemming aangeteken word.

**Voorgestelde aanvaardingstoets**

Die pakhuis ontvang twee keer dieselfde bevestiging vir drie eenhede. Al verander die gebruiker intussen van taal, verwys albei bevestigings na dieselfde ontvangsbewys en word slegs drie eenhede geboek.

[Volledige profiel in Engels](../../apps/erpnext_easyecom.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/erpnext_easyecom)

## WMS

Ontvang en tel voorraad, versamel bestellings, pak dit en versend dit met behoud van die geskandeerde item-, vak- en lotnommers.

**Gedokumenteerde werkvloei**

Dexciss beskryf hoe pakhuispersoneel mobiele toestelle gebruik om items en stoorvakke op te soek, voorraad te tel en aankope te ontvang. Hulle kan ook materiaalversoeke en voorraadinskrywings hanteer, goedere vir versending bymekaarmaak en pak, voorraadetikette druk en gehaltekontroles aanteken.

**Voorgestelde aanvaardingstoets**

Vak A bevat 20 eenhede en vak B is leeg. ’n Afrikaanssprekende orderversamelaar skuif twee kartonne van ses eenhede elk na B. Die Duitssprekende toesighouer sien 8 eenhede in A, 12 in B en slegs een geboekte oorplasing, selfs wanneer die skandeerder dit weer indien.

[Volledige profiel in Engels](../../apps/wms.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/wms)
