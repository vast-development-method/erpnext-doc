# Bankwese en tesourie

## Volg elke tjek vanaf ontvangs of uitreiking tot vereffening of terugstuur, en rekonsilieer dit met die joernaalinskrywing en banktransaksie

<a id="workflow-cheque-approval-and-collection"></a>

Skep die tjek uit die ontvangs, groepeer toepaslike tjeks op ’n depositostrokie en pas die bank se uitkoms by die gedeponeerde instrument en sy joernaal.

Met ’n goedkeuringsdrempel van 1 000 moet ’n ingediende tjek van presies 1 000 in ’n nuwe sessie steeds op goedkeuring wag, sonder enige joernaalinskrywing. Sodra die rekeningebestuurder dit goedkeur, word een joernaalinskrywing geskep, en die Arabiese en Engelse kwitansies verwys na dieselfde tjeknommer, goedkeuring en bedrag.

[English](../banking.md#cheque-approval-and-collection) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#cheque).

## Vorder betaling vir ’n verkoopsfaktuur deur ’n betaaldiens in en rekonsilieer die bevestigde betaling met die uitstaande saldo

<a id="workflow-saved-payment-method-collections"></a>

Versoek invordering in die faktuurgeldeenheid met die kliënt se gemagtigde betaalmetode. Verdeel die ontvangs ná bevestiging en hou die verskaffer se verwysing by die toedeling.

Laat ’n Franssprekende betaler dieselfde invorderingsversoek twee keer vir ’n Engelse faktuur met EUR 40 uitstaande stuur en verwerk die sukseskennisgewing twee keer. Die betalingsdiens hef EUR 40 een keer, die bedrag word een keer toegedeel en die saldo is nul; die kwitansietaal verander geen party, verwysing of bedrag nie.

[English](../banking.md#saved-payment-method-collections) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#ipconnex-stripe-payment).

## Volg ’n nagedateerde tjek vanaf ontvangs of uitreiking totdat dit gedeponeer, vereffen of onbetaald teruggestuur word

<a id="workflow-post-dated-cheque-settlement"></a>

Teken die tjek teen die toepaslike tussenrekening aan. Deponeer dit met ’n bankjoernaal en boek die uiteindelike vereffeningsdatum teen dieselfde joernaal.

Boek tjek 00072 teen ’n uitstaande kliëntfaktuur van 400,00, deponeer dit en bevestig vereffening twee keer met dieselfde verwysing. Die bank neem met 400,00 toe, die tussenrekening staan weer op nul en die Duitse en Afrikaanse skerms wys dieselfde tjek en boekstukke.

[English](../banking.md#post-dated-cheque-settlement) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#pdc-cheque-management).

## Voer ’n CSV-bankstaat van ’n bank in Bosnië en Herzegowina in en kontroleer herhaalde transaksiereferensies voor rekonsiliasie

<a id="workflow-bank-statement-import-and-duplicate-review"></a>

Lees die bank se CSV-uitleg en vertoon datum, deposito, onttrekking, verwysing en beskrywing. Beoordeel herhalings voordat die aanvaarde reëls vir rekonsiliasie beskikbaar word.

Voer bankverwysing 00038 met 1.234,50 twee keer in en ontvang dit daarna met 1.234,55. Slegs een transaksie word geboek, die identiese ry word as duplikaat aangedui en die verskil gaan vir hersiening, ongeag die operateur se taal of desimale vertoonformaat.

[English](../banking.md#bank-statement-import-and-duplicate-review) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#procredit-bank-statement-processing).

## Teken kontant- of tjekontvangste en -betalings in die kasboek aan en gaan inskrywings vir bepaalde teenpartye na

<a id="workflow-treasury-transaction-register"></a>

Stel debiteure- en krediteure-rekeninge per betaalmetode op. ’n Tesourie-inskrywing kan rekeningreëls direk bevat of bedrae aan ’n party se oop fakture toedeel.

Teken by dieselfde kas ’n kontantontvangs van 250,00 vir ’n teenparty en ’n kontantbetaling van 75,00 sonder ’n teenparty aan. Sowel die Afrikaanse as die Duitse register toon ’n netto toename van 175,00; die filter vir teenparty-inskrywings laat net die ontvangs van 250,00 oor.

[English](../banking.md#treasury-transaction-register) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#treasury-entry).

## Magtig ’n groep verskafferbetalings deur die bank en rekonsilieer elke betaalopdrag met die bank se antwoord

<a id="workflow-supplier-payment-batch-authorization"></a>

Kies die verskafferbetalings en magtig die groep met ’n eenmalige kode. Volg die bankverwysing en uitslag vir elke betalingsopdrag afsonderlik.

Verwerk dieselfde bankantwoord twee keer vir ’n goedgekeurde groep van twee verskafferbetalings waarvan een bevestig en een afgekeur is. Slegs die betaalde verskaffer kry ’n Duitse betalingsadvies, die afgekeurde betaling bly uitstaande, en die Hindi- en Engelssprekende personeel sien dieselfde bankverwysings en oorspronklike afkeuringsrede.

Die bank bevestig 600 en weier 400 uit ’n gemagtigde groep van 1 000. Rekonsilieer die bankdebiet van 600 en stuur net daardie betalingsadvies. Die 400 bly oop met sy oorspronklike rede. By ’n verbreekte verbinding word die oorspronklike verwysings nagegaan voordat die opdrag weer gestuur word.

[English](../banking.md#supplier-payment-batch-authorization) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#sanpra-easypay).

## Vorder ’n betaling aanlyn, met ’n gekoppelde betaalterminaal of vir ’n herhalende betalingsversoek in en rekonsilieer dit met die faktuur

<a id="workflow-online-and-terminal-payment-collection"></a>

Ná handelaargoedkeuring verbind die onderneming elke betaalmetode aan die betrokke invorderingsroete. Die betaalversoek kan ’n webbetaling, gemagtigde herhalende invordering of terminale betaling gebruik.

’n Franssprekende betaler vereffen ’n faktuur van EUR 35,70. As die betaaldiens dieselfde bevestiging twee keer stuur, word die bedrag net een keer toegedeel en sien die Duitssprekende kassier dieselfde vereffende faktuur.

[English](../banking.md#online-and-terminal-payment-collection) · [Bronwaarnemings](../../../rebuild/marketplace-guides/editions/af/banking.md#stripe2-payment-integration).
