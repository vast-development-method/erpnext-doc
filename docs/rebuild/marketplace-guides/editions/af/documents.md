# Dokumente, handtekeninge en drukwerk

[English](../en/documents.md) · Afrikaans · [Deutsch](../de/documents.md) · [简体中文](../zh-Hans/documents.md)

[Alle onderwerpe](README.md)

Elke voorbeeld beskryf ’n verwagte uitkoms vir die nuwe stelsel. Die volledige profiel dui aan watter besonderhede die uitgewer beskryf, watter in die bronkode voorkom en watter in ’n werkende stelsel getoets is.

## Dynamic Bulk PDF Downloader

Filter die rekords wat gedruk moet word en laai die PDF-lêers as ’n ZIP-argief af, gegroepeer volgens die gekose veld.

**Gedokumenteerde werkvloei**

Die gebruiker kies die dokumenttipe, drukformaat, filters en, indien nodig, ’n groeperingsveld. Die agtergrondtaak in die herwonne weergawe skep PDF-lêers vir die ooreenstemmende rekords, pak suksesvolle lêers in ’n ZIP-argief en teken drukfoute per dokument aan.

**Voorgestelde aanvaardingstoets**

As 55 toeganklike dokumente oor verskeie soekbladsye versprei is en een PDF nie geskep kan word nie, word die taak as gedeeltelik voltooi gemerk. Die argief bevat 54 PDF-lêers en die manifest identifiseer die mislukte dokument, teken elke PDF se taal aan en hou groepe met soortgelyke Unicode-name apart.

[Volledige profiel in Engels](../../apps/bulk_download.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/bulk_download)

## Document Progress Tracker

Volg ’n dokument se mylpale en rapporteer hoeveel tyd tussen hulle verloop.

**Gedokumenteerde werkvloei**

Die prosesverantwoordelike kies die dokumenttipe, datumveld, mylpale, voorwaardes en persentasies. Wanneer ’n voorwaarde nagekom word, werk die stelsel die dokument se vordering by en skep ’n inskrywing met onder meer die mylpaal, gebruiker, tydstempel en verloopte minute of dae.

**Voorgestelde aanvaardingstoets**

By ’n vaste vorderingspersentasie per mylpaal word die dokument om 08:00 UTC goedgekeur en dieselfde dag om 15:03 UTC as afgelewer gemerk. Die vordering is dan 100% en die verloopte tyd 423 minute. ’n Herhaalde afleweringsgebeurtenis voeg geen inskrywing by nie, en ’n vertaalde mylpaalnaam verander nie die tydsduur nie.

[Volledige profiel in Engels](../../apps/document_progress_tracker.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/document_progress_tracker)

## Digital Signature

Wys ’n ondertekenaar aan en stuur die ondertekende PDF onveranderd aan die ontvanger.

**Gedokumenteerde werkvloei**

Die ondertekenaar het ’n DSC User-rekord met ’n handtekeningbeeld en wagwoord. Die verskaffer se handleiding wys hoe die gebruiker aan die faktuur gekoppel word en hoe die wagwoord en die Signed PDF-knoppie gebruik word om ’n lêer te skep wat afgelaai of per e-pos gestuur kan word.

**Voorgestelde aanvaardingstoets**

As twee e-posse in verskillende tale na dieselfde ondertekende Duitse faktuur verwys, moet albei aanhangsels se kontrolesomme met dié van die bewaarde, ondertekende PDF ooreenstem. Die taal van die e-pos verander nie die lêer of die ondertekenaar nie, en geen tweede ondertekening vind plaas nie.

[Volledige profiel in Engels](../../apps/dsc.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/dsc)

## Esign App

Wys elke ondertekenaar se velde toe en bewaar die taal en inhoud van die ondertekende ooreenkoms.

**Gedokumenteerde werkvloei**

Die kode waarna die uitgewer verwys, kopieer die PDF-uitleg uit die sjabloon, stoor elke ontvanger se toegewese velde by versending en teken ’n rede vir afkeuring afsonderlik van voltooiing en ondertekening aan.

**Voorgestelde aanvaardingstoets**

Twee mense onderteken dieselfde Afrikaanse ooreenkoms, die een met Duitse en die ander met Engelse skermteks. Wanneer albei hul eie velde voltooi het, verwys hul handtekeninge na een afgehandelde dokument met dieselfde dokumentvingerafdruk.

[Volledige profiel in Engels](../../apps/esign_app.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/esign_app)

## LumenPDF Studio

Ontwerp ’n tweetalige faktuur, bekyk die PDF vooraf en stuur dit in die ontvanger se voorkeurtaal.

**Gedokumenteerde werkvloei**

Volgens die uitgewer kan ’n stelselbestuurder ’n standaardontwerp aanpas, faktuur- of verslagvelde daaraan koppel en die PDF vooraf bekyk. Die gebruiker wat druk, kan ’n Arabiese of tweetalige formaat kies en die dokument aflaai of dit as ’n e-posaanhangsel stuur.

**Voorgestelde aanvaardingstoets**

’n Engelssprekende klerk druk ’n faktuur met ’n naam in twee skrifstelsels en twee belastingreëls met ’n Arabies-Engelse sjabloon. Albei opskrifte verskyn, die belastingbedrae stem met die geboekte bedrae ooreen en die QR-kode bevat steeds die oorspronklike ondertekende data.

[Volledige profiel in Engels](../../apps/lumenpdf.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/lumenpdf)
