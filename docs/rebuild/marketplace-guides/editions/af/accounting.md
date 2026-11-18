# Fakture, belasting en rekeningkunde

[English](../en/accounting.md) · Afrikaans · [Deutsch](../de/accounting.md) · [简体中文](../zh-Hans/accounting.md)

[Alle onderwerpe](README.md)

Elke voorbeeld beskryf ’n verwagte uitkoms vir die nuwe stelsel. Die volledige profiel dui aan watter besonderhede die uitgewer beskryf, watter in die bronkode voorkom en watter in ’n werkende stelsel getoets is.

## E Invoice Egypt

Dien Egiptiese elektroniese fakture in en volg die belastingowerheid se valideringsuitslag vir elke dokument.

**Gedokumenteerde werkvloei**

Die verskaffer bied individuele en bondelverwerking vir fakture, kredietnotas, debietnotas, kansellasie en validering. Die Egiptiese belastingowerheid se koppelvlak lys aanvaarde en verwerpte dokumente afsonderlik in die aanvanklike antwoord, met finale validering wat daarna volg.

**Voorgestelde aanvaardingstoets**

Die toetsdiens antwoord met HTTP 202 op ’n ondertekende bondel: INV-001 kry ’n eksterne ID en INV-002 ’n struktuurfout. Net INV-001 wag op finale validering, INV-002 moet reggestel word en geen faktuur is finaal goedgekeur nie. Die Arabiese en Duitse aansigte behou die oorspronklike ID’s, foutkode en ondertekende versoek.

[Volledige profiel in Engels](../../apps/e_invoice.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/e_invoice)

## Forward Contract

Verreken betalings teen ’n banktermynkontrak en boek die wins of verlies wanneer ’n ongebruikte gedeelte gekanselleer word.

**Gedokumenteerde werkvloei**

Volgens die uitgewer se gids kan ’n betaling ’n deel van een termynkontrak of bedrae van verskeie kontrakte gebruik. ’n Bewaarde kodeweergawe wat FinByz as outeur noem, krediteer wisselkoerswins en debiteer die bank by ’n winsgewende kansellasie.

**Voorgestelde aanvaardingstoets**

Van ’n uitvoertermynkontrak van USD 1 000 teen 17,50 NAD per USD is USD 600 benut. Wanneer USD 100 teen 17,20 sonder fooie gekanselleer word, bly USD 300 oor, met ’n bankdebiet en wisselkoerswins van NAD 30 elk in elke taalweergawe.

[Volledige profiel in Engels](../../apps/forward_contract.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/forward_contract)

## AI Invoice Importer

Lees ’n faktuur uit ’n PDF en kontroleer die betrokke party, datum, geldeenheid en reëlbedrae voordat jy ’n konsep skep.

**Gedokumenteerde werkvloei**

IPCONNEX beskryf ’n hulpmiddel wat faktuurdata met ChatGPT uit ’n PDF onttrek. In die vasgelegde openbare kopie kies die klerk aankoop of verkoop en verskaf die PDF; die invoerhulpmiddel vergelyk die faktuurtotaal met die berekende reëlbedrae en kan die toepaslike aankoop- of verkoopsfaktuur met die bronlêer as aanhangsel skep.

**Voorgestelde aanvaardingstoets**

Lees die Duitse PDF met die datum 18.11.2026 en ’n enkele reël van 1.234,50 EUR in, kontroleer dit in Engels en keur dieselfde invoer twee keer goed. Daar ontstaan een gekoppelde konsep met die datum 2026-11-18 en EUR 1 234,50; die oorspronklike teks, party en waardes bly naspeurbaar.

[Volledige profiel in Engels](../../apps/ipconnex_ai_invoice.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/ipconnex_ai_invoice)

## PAV

Boek ’n werknemervoorskot in die Jemenitiese lokalisering en rekonsilieer die terugbetaling in die ouditeur se voorkeurtaal.

**Gedokumenteerde werkvloei**

Die lysinskrywing vir Jemen dek werknemersvoorskotte, rekeningkundige verslae en bywoningsverslae. In ’n openbare historiese kopie word die aangewese rekening gedebiteer en die finansieringsrekening gekrediteer wanneer ’n gewone voorskot ingedien word, terwyl ’n terugbetaling die twee inskrywings omruil.

**Voorgestelde aanvaardingstoets**

’n Voorskot van 100 transaksie-eenhede teen 2 eenhede van die maatskappy se geldeenheid per eenheid lewer ’n debiet en ’n krediet van 200 elk. ’n Volle terugbetaling teen dieselfde koers keer albei inskrywings om; die Arabiese en Engelse verslae wys dieselfde rekeninge en bedrae.

[Volledige profiel in Engels](../../apps/pav.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/pav)

## Payment Installments

Skep ’n faktuur vir die aanbetaling en faktureer die oorblywende paaiemente volgens die verkoopbestelling se skedule.

**Gedokumenteerde werkvloei**

Volgens Kanak kies verkoopspersoneel die betalingsvoorwaardes, stel die eerste paaiementdatum vas en voeg, indien nodig, koste op die verkoopbestelling by. Wanneer die bestelling ingedien word, word die skedule en die aanbetalingsfaktuur met die bykomende koste geskep, en ’n geskeduleerde proses skep elke daaropvolgende faktuur twee dae voor die vervaldatum.

**Voorgestelde aanvaardingstoets**

Op ’n bestelling van 1 000 met ’n aanbetaling van 20%, vragkoste van 50 en drie paaiemente vanaf 15 Januarie is die aanbetalingsfaktuur 250. As die skeduleerder op 13 Januarie twee keer loop, ontstaan net een eerste faktuur van 266,67 waarvan die volle bedrag sonder ’n betaling in elke taal uitstaande bly.

[Volledige profiel in Engels](../../apps/payment_installment_kanak.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/payment_installment_kanak)

## ERPNext United Kingdom

Stel ’n Britse BTW-opgawe uit die toepaslike bewysstukke saam, dien dit vir die regte tydperk in en rekonsilieer dit met die belastingowerheid se ontvangsbewys.

**Gedokumenteerde werkvloei**

Case Solved se handleiding beskryf hoe ondernemings of hul agente BTW-opgawes nagaan en indien en verskuldigde en betaalde bedrae besigtig. Dit beskryf ook BTW-koerse per faktuur of faktuurreël, joernaalaanpassings en ’n afsluitingsinskrywing vir die verslagtydperk.

**Voorgestelde aanvaardingstoets**

Die belastingreëls is 12 en 8, die faktuuropsomming is 20 en die afsonderlike aanpassing is −2. Die Walliessprekende opsteller en Engelssprekende indiener sien albei 18 in dieselfde aangiftevak. Die opsomming word nie dubbel getel nie.

[Volledige profiel in Engels](../../apps/uk.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/uk)
