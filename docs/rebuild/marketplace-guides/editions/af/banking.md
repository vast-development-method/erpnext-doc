# Betalings en bankwese

[English](../en/banking.md) · Afrikaans · [Deutsch](../de/banking.md) · [简体中文](../zh-Hans/banking.md)

[Alle onderwerpe](README.md)

## cheque

Wanneer ’n ontvangsbewys ingedien word, word die kliënt se tjek geskep, en ’n depositostrokie groepeer geskikte tjeks vir die bank. Die herwonne rekonsiliasiekode soek die gedeponeerde tjek volgens verwysing en vereis ’n gekoppelde joernaalinskrywing voordat dit invordering of terugstuur aanteken.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-cheque-approval-and-collection) · [Bronwaarnemings](../../apps/cheque.md)

## IPCONNEX Stripe Payment

Volgens die produkbeskrywing word die betaling van ’n faktuur beskikbaar nadat Stripe en die klant se betalingsbesonderhede opgestel is. Die historiese openbare kopie gebruik die gestoorde betaalmiddel en faktuurgeldeenheid, versoek ’n PaymentIntent by Stripe en stel ’n betalingsinskrywing met ’n toedeling aan die faktuur saam; werklike vereffening op ’n geïnstalleerde stelsel is nie bevestig nie.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-saved-payment-method-collections) · [Bronwaarnemings](../../apps/ipconnex_stripe_payment.md)

## PDC Cheque Management

Volgens die uitgewer skep die ontvangs van ’n klantetjek of die uitreiking van ’n tjek aan ’n verskaffer ’n betalingsinskrywing teen die toepaslike tussenrekening. In die openbare bronkopie wat die uitgewer as outeur aandui, skep die deposito ’n bankjoernaalinskrywing en word die vereffeningsdatum later daarop aangeteken.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-post-dated-cheque-settlement) · [Bronwaarnemings](../../apps/pdc_cheque_management.md)

## ProCredit Bank Statement Processing

Die uitgewer beskryf hoe CSV-bankstate van ProCredit Bank in Bosnië en Herzegowina ingevoer en vir herhaalde verwysings nagegaan word. Die skermgrepe wys ’n voorskou met die datum, deposito, onttrekking, verwysing en beskrywing van elke ry, gevolg deur banktransaksies wat nog gerekonsilieer moet word.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-bank-statement-import-and-duplicate-review) · [Bronwaarnemings](../../apps/procreditbank.md)

## Treasury Entry

Die uitgewer se skermgrepe wys afsonderlike rekeninge vir betalings en ontvangstes by elke betaalmetode van die kas. By ’n kasinskrywing kan die klerk rekening en bedrag per ry invoer, of die teenparty-opsie kies om uitstaande fakture op te roep en bedrae teen die betrokke fakture toe te wys.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-treasury-transaction-register) · [Bronwaarnemings](../../apps/safe_entry.md)

## Sanpra Easypay

Die produkbeskrywing noem invorderings en uitbetalings deur ICICI Bank. Vir verskafferbetalings beskryf die uitgewer hoe betalingsinskrywings opgeroep word, ’n groep met ’n eenmalige wagwoord gemagtig word en die bank se transaksiestatusse gevolg word, met ondersteuning vir RTGS en NEFT.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-supplier-payment-batch-authorization) · [Bronwaarnemings](../../apps/sanpra_easypay.md)

## Stripe2 Payment Integration

Nadat die maatskappy se kontakpersoon hul e-posadres bevestig en die Stripe-rekening gemagtig het, stel die handelaar die aanlyn en aflyn betaalmetodes in. ’n Ingediende betalingsversoek kan ’n aanlyn betaalblad oopmaak of ’n gestoorde betaalmetode vir ’n herhalende betaling gebruik, en ’n kassier kan ’n geregistreerde betaalterminaal gebruik.

[Werkvloei en toetsgeval](../../../../capabilities/guides/af/banking.md#workflow-online-and-terminal-payment-collection) · [Bronwaarnemings](../../apps/stripe2.md)
