# Worked document conversions

## One supplier order can have different amounts left to receive and to bill

Order twelve cases of six at 20 transaction-currency units per case, with an exchange rate of 1.5 company units per transaction unit. Five cases have been received. Two more cases from the same order line have already been mapped into the receiving draft. For a new allocation into that draft, the open receipt quantity is $12-5-2=5$ cases, or 30 stock pieces. Its initial line amount is 100, or 150 company units. Identify the purchase order line on the receiving row so another product row on that order cannot consume this entitlement.

If nine cases are already billed and no quantity is present in the destination billing draft, the ordinary quantity remaining to invoice from the order is three cases. The receiving calculation and billing calculation use different predecessor measures. A separate path also admits a row whose billing quantity has been covered but whose amount remains below the original order value. Inspect posted invoices and their amounts before making a new billing proposal. [Purchasing and receiving](purchasing-and-receiving.md)

## Return between preparing and submitting a service document

Five units are delivered. Prepare an installation note for five and leave it in draft. A return of two against that same delivery row reduces the maximum installable quantity to three. Refreshing a new installation proposal gives three. Submitting the stale five-unit draft must reject the excess. If two units are subsequently installed, the next proposal is one. Repeating the lookup does not install that unit, move it from a warehouse or charge it to the customer. [Installation and linked service work](service-and-projects.md)

## A manufacture plan releases separate service and material documents

A plan subassembly classified as subcontracted requires eight finished units. If three units are already covered by an effective purchase-order line against the same plan row and no other commitments apply, the remaining outsourced demand is five finished units. The purchase row identifies the plan, subassembly and receiving location. The service product and its commercial unit can differ from the finished product. A different subassembly classified for internal manufacture follows the work-order path and receives its own component and work-in-progress requirements.

For a planned component request measured in cases of six, ten cases planned, three cases already submitted and 24 pieces in linked drafts leave $10-3-24/6=3$ cases. An immediate repeat after saving those additional three draft cases leaves zero. Purchase order, work order and material request must each retain the source row that justifies its quantity. [Production and subcontracting](production-and-subcontracting.md)

## Journal reversal in two currencies

A submitted journal entry debits a foreign-currency account 40 account-currency units at 2.5 company units per foreign unit and credits its company-currency counterpart 100. The reversal credits the foreign account 40 in its currency and 100 in company currency, then debits the counterpart 100. It retains original account, exchange rate, relevant party or document references and the identifier of the journal being reversed. It receives a separate journal identifier. Until submitted, the proposed reversal leaves the original posted balances intact. [Journal reversal fields](accounting-reversals.md)

## A return carries both a sales quantity and a physical identity

A customer invoice for two cases of six refers to one delivery row. One case has been returned. A return of the remaining case proposes −1 case and −6 stock units. For serial-controlled goods the selectable physical identities are the original units less those already effectively returned. The customer credit line retains the original invoice line, delivery line and order line where present. Stock moves on the document whose stock-update policy authorises the receipt. A separate financial credit tied to a posted goods return must not create a second inward stock movement. [Returns and counterparties](reversals-and-counterparties.md)
