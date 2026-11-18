# Betalings en bankwese

[English](../en/banking.md) · Afrikaans · [Deutsch](../de/banking.md) · [简体中文](../zh-Hans/banking.md)

[Alle onderwerpe](README.md)

Elke voorbeeld beskryf ’n verwagte uitkoms vir die nuwe stelsel. Die volledige profiel dui aan watter besonderhede die uitgewer beskryf, watter in die bronkode voorkom en watter in ’n werkende stelsel getoets is.

## cheque

Volg elke tjek vanaf ontvangs of uitreiking tot vereffening of terugstuur, en rekonsilieer dit met die joernaalinskrywing en banktransaksie.

**Gedokumenteerde werkvloei**

Wanneer ’n ontvangsbewys ingedien word, word die kliënt se tjek geskep, en ’n depositostrokie groepeer geskikte tjeks vir die bank. Die herwonne rekonsiliasiekode soek die gedeponeerde tjek volgens verwysing en vereis ’n gekoppelde joernaalinskrywing voordat dit invordering of terugstuur aanteken.

**Voorgestelde aanvaardingstoets**

Met ’n goedkeuringsdrempel van 1 000 moet ’n ingediende tjek van presies 1 000 in ’n nuwe sessie steeds op goedkeuring wag, sonder enige joernaalinskrywing. Sodra die rekeningebestuurder dit goedkeur, word een joernaalinskrywing geskep, en die Arabiese en Engelse kwitansies verwys na dieselfde tjeknommer, goedkeuring en bedrag.

[Volledige profiel in Engels](../../apps/cheque.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/cheque)

## IPCONNEX Stripe Payment

Vorder betaling vir ’n verkoopsfaktuur deur Stripe in en rekonsilieer die bevestigde betaling met die uitstaande saldo.

**Gedokumenteerde werkvloei**

Volgens die produkbeskrywing word die betaling van ’n faktuur beskikbaar nadat Stripe en die klant se betalingsbesonderhede opgestel is. Die historiese openbare kopie gebruik die gestoorde betaalmiddel en faktuurgeldeenheid, versoek ’n PaymentIntent by Stripe en stel ’n betalingsinskrywing met ’n toedeling aan die faktuur saam; werklike vereffening op ’n geïnstalleerde stelsel is nie bevestig nie.

**Voorgestelde aanvaardingstoets**

Laat ’n Franssprekende betaler dieselfde invorderingsversoek twee keer vir ’n Engelse faktuur met EUR 40 uitstaande stuur en verwerk die sukseskennisgewing twee keer. Die betalingsdiens hef EUR 40 een keer, die bedrag word een keer toegedeel en die saldo is nul; die kwitansietaal verander geen party, verwysing of bedrag nie.

[Volledige profiel in Engels](../../apps/ipconnex_stripe_payment.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/ipconnex_stripe_payment)

## PDC Cheque Management

Volg ’n nagedateerde tjek vanaf ontvangs of uitreiking totdat dit gedeponeer, vereffen of onbetaald teruggestuur word.

**Gedokumenteerde werkvloei**

Volgens die uitgewer skep die ontvangs van ’n klantetjek of die uitreiking van ’n tjek aan ’n verskaffer ’n betalingsinskrywing teen die toepaslike tussenrekening. In die openbare bronkopie wat die uitgewer as outeur aandui, skep die deposito ’n bankjoernaalinskrywing en word die vereffeningsdatum later daarop aangeteken.

**Voorgestelde aanvaardingstoets**

Boek tjek 00072 teen ’n uitstaande kliëntfaktuur van 400,00, deponeer dit en bevestig vereffening twee keer met dieselfde verwysing. Die bank neem met 400,00 toe, die tussenrekening staan weer op nul en die Duitse en Afrikaanse skerms wys dieselfde tjek en boekstukke.

[Volledige profiel in Engels](../../apps/pdc_cheque_management.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management)

## ProCredit Bank Statement Processing

Voer ’n CSV-bankstaat van ProCredit in Bosnië en Herzegowina in en kontroleer herhaalde transaksiereferensies voor rekonsiliasie.

**Gedokumenteerde werkvloei**

Die uitgewer beskryf hoe CSV-bankstate van ProCredit Bank in Bosnië en Herzegowina ingevoer en vir herhaalde verwysings nagegaan word. Die skermgrepe wys ’n voorskou met die datum, deposito, onttrekking, verwysing en beskrywing van elke ry, gevolg deur banktransaksies wat nog gerekonsilieer moet word.

**Voorgestelde aanvaardingstoets**

Voer bankverwysing 00038 met 1.234,50 twee keer in en ontvang dit daarna met 1.234,55. Slegs een transaksie word geboek, die identiese ry word as duplikaat aangedui en die verskil gaan vir hersiening, ongeag die operateur se taal of desimale vertoonformaat.

[Volledige profiel in Engels](../../apps/procreditbank.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/procreditbank)

## Treasury Entry

Teken kontant- of tjekontvangste en -betalings in die kasboek aan en gaan inskrywings vir bepaalde teenpartye na.

**Gedokumenteerde werkvloei**

Die uitgewer se skermgrepe wys afsonderlike rekeninge vir betalings en ontvangstes by elke betaalmetode van die kas. By ’n kasinskrywing kan die klerk rekening en bedrag per ry invoer, of die teenparty-opsie kies om uitstaande fakture op te roep en bedrae teen die betrokke fakture toe te wys.

**Voorgestelde aanvaardingstoets**

Teken by dieselfde kas ’n kontantontvangs van 250,00 vir ’n teenparty en ’n kontantbetaling van 75,00 sonder ’n teenparty aan. Sowel die Afrikaanse as die Duitse register toon ’n netto toename van 175,00; die filter vir teenparty-inskrywings laat net die ontvangs van 250,00 oor.

[Volledige profiel in Engels](../../apps/safe_entry.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/safe_entry)

## Sanpra Easypay

Magtig ’n groep verskafferbetalings deur ICICI en rekonsilieer elke betaalopdrag met die bank se antwoord.

**Gedokumenteerde werkvloei**

Die produkbeskrywing noem invorderings en uitbetalings deur ICICI Bank. Vir verskafferbetalings beskryf die uitgewer hoe betalingsinskrywings opgeroep word, ’n groep met ’n eenmalige wagwoord gemagtig word en die bank se transaksiestatusse gevolg word, met ondersteuning vir RTGS en NEFT.

**Voorgestelde aanvaardingstoets**

Verwerk dieselfde bankantwoord twee keer vir ’n goedgekeurde groep van twee verskafferbetalings waarvan een bevestig en een afgekeur is. Slegs die betaalde verskaffer kry ’n Duitse betalingsadvies, die afgekeurde betaling bly uitstaande, en die Hindi- en Engelssprekende personeel sien dieselfde bankverwysings en oorspronklike afkeuringsrede.

[Volledige profiel in Engels](../../apps/sanpra_easypay.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/sanpra_easypay)

## Stripe2 Payment Integration

Vorder ’n betaling aanlyn, met ’n gekoppelde betaalterminaal of vir ’n herhalende betalingsversoek in en rekonsilieer dit met die faktuur.

**Gedokumenteerde werkvloei**

Nadat die maatskappy se kontakpersoon hul e-posadres bevestig en die Stripe-rekening gemagtig het, stel die handelaar die aanlyn en aflyn betaalmetodes in. ’n Ingediende betalingsversoek kan ’n aanlyn betaalblad oopmaak of ’n gestoorde betaalmetode vir ’n herhalende betaling gebruik, en ’n kassier kan ’n geregistreerde betaalterminaal gebruik.

**Voorgestelde aanvaardingstoets**

’n Franssprekende betaler vereffen ’n faktuur van EUR 35,70. As die betaaldiens dieselfde bevestiging twee keer stuur, word die bedrag net een keer toegedeel en sien die Duitssprekende kassier dieselfde vereffende faktuur.

[Volledige profiel in Engels](../../apps/stripe2.md) · [Uitgewer se markplekblad](https://cloud.frappe.io/marketplace/apps/stripe2)
