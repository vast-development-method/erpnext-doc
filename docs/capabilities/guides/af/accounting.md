# Rekeningkunde en belasting

## Dien Egiptiese elektroniese fakture in en volg die belastingowerheid se valideringsuitslag vir elke dokument

<a id="workflow-egyptian-electronic-tax-submission"></a>

Reik fakture, kredietnotas en debietnotas afsonderlik of in ’n groep uit. Hou die uitkoms vir elke dokument apart totdat die owerheid dit finaal valideer.

Die toetsdiens antwoord met HTTP 202 op ’n ondertekende bondel: INV-001 kry ’n eksterne ID en INV-002 ’n struktuurfout. Net INV-001 wag op finale validering, INV-002 moet reggestel word en geen faktuur is finaal goedgekeur nie. Die Arabiese en Duitse aansigte behou die oorspronklike ID’s, foutkode en ondertekende versoek.

Hou die groep se verwysing en elke faktuur se uitslag apart. Koppel die regstelling aan die afgekeurde reël. As ’n aanvanklik aanvaarde faktuur later validering druip, behou albei gebeurtenisse en hul tye. ’n Nuwe indiening van die ander faktuur verander geen vorige resultaat of geboekte faktuur nie.

[English](../accounting.md#egyptian-electronic-tax-submission) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/accounting.md#e-invoice-egypt).

## Verreken betalings teen ’n banktermynkontrak en boek die wins of verlies wanneer ’n ongebruikte gedeelte gekanselleer word

<a id="workflow-forward-exchange-contract-allocation"></a>

Koppel die gebruikte gedeelte van elke termynkontrak aan die betaling. Boek die wins en bankbedrag wanneer ’n winsgewende uitvoertermynkontrak gekanselleer word.

Van ’n uitvoertermynkontrak van USD 1 000 teen 17,50 NAD per USD is USD 600 benut. Wanneer USD 100 teen 17,20 sonder fooie gekanselleer word, bly USD 300 oor, met ’n bankdebiet en wisselkoerswins van NAD 30 elk in elke taalweergawe.

[English](../accounting.md#forward-exchange-contract-allocation) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/accounting.md#forward-contract).

## Lees ’n faktuur uit ’n PDF en kontroleer die betrokke party, datum, geldeenheid en reëlbedrae voordat jy ’n konsep skep

<a id="workflow-invoice-image-and-document-extraction"></a>

Kies aankoop of verkoop, laai die PDF op en vergelyk die verklaarde totaal met die som van die reëls. Heg die oorspronklike PDF aan die nagegane faktuurkonsep.

Lees die Duitse PDF met die datum 14.07.2023 en ’n enkele reël van 1.234,50 EUR in, kontroleer dit in Engels en keur dieselfde invoer twee keer goed. Daar ontstaan een gekoppelde konsep met die datum 2023-07-14 en EUR 1 234,50; die oorspronklike teks, party en waardes bly naspeurbaar.

[English](../accounting.md#invoice-image-and-document-extraction) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/accounting.md#ai-invoice-importer).

## Boek ’n werknemervoorskot in die Jemenitiese lokalisering en rekonsilieer die terugbetaling in die ouditeur se voorkeurtaal

<a id="workflow-employee-advance-and-return-in-yemen"></a>

Boek die voorskot teen die werknemer se voorskotrekening en die betaalrekening. Koppel die terugbetaling aan die oorspronklike voorskot en ruil die debiet- en kredietinskrywings om.

’n Voorskot van 100 transaksie-eenhede teen 2 eenhede van die maatskappy se geldeenheid per eenheid lewer ’n debiet en ’n krediet van 200 elk. ’n Volle terugbetaling teen dieselfde koers keer albei inskrywings om; die Arabiese en Engelse verslae wys dieselfde rekeninge en bedrae.

[English](../accounting.md#employee-advance-and-return-in-yemen) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/accounting.md#pav).

## Skep ’n faktuur vir die aanbetaling en faktureer die oorblywende paaiemente volgens die verkoopbestelling se skedule

<a id="workflow-sales-order-advance-and-instalment-invoicing"></a>

Kies die betalingsterme en eerste paaiementdatum op die verkoopsorder. By indiening sluit die depositofaktuur die gekose koste in. Latere fakture word twee dae voor die vervaldatum voorberei.

Op ’n bestelling van 1 000 met ’n aanbetaling van 20%, vragkoste van 50 en drie paaiemente vanaf 15 Januarie is die aanbetalingsfaktuur 250. As die skeduleerder op 13 Januarie twee keer loop, ontstaan net een eerste faktuur van 266,67 waarvan die volle bedrag sonder ’n betaling in elke taal uitstaande bly.

[English](../accounting.md#sales-order-advance-and-instalment-invoicing) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/accounting.md#payment-installments).

## Stel ’n Britse BTW-opgawe uit die toepaslike bewysstukke saam, dien dit vir die regte tydperk in en rekonsilieer dit met die belastingowerheid se ontvangsbewys

<a id="workflow-british-return-aggregation"></a>

Die onderneming of gemagtigde agent kontroleer die BTW, joernaalaanpassings en tydperk voordat die opgawe ingedien word. Hou betalings en verpligtinge vir dieselfde tydperk naspeurbaar.

Die belastingreëls is 12 en 8, die faktuuropsomming is 20 en die afsonderlike aanpassing is −2. Die Walliessprekende opsteller en Engelssprekende indiener sien albei 18 in dieselfde aangiftevak. Die opsomming word nie dubbel getel nie.

[English](../accounting.md#british-return-aggregation) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/accounting.md#erpnext-united-kingdom).
