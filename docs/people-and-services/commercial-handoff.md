# Customer, opportunity and quotation handoff

A negotiating opportunity may belong to a sales team operating across a separate business unit. The company's quotation service owns prices actually offered, quoted tax, validity and terms. Persist the opportunity identity, selling party and item identities across this handoff. An opportunity's won stage, an order's submission and a customer invoice posting are independent events.

| Decision | One shared operation environment | Independently operated sales and quotation environments |
|---|---|---|
| Select the quotation party | Look for a customer already linked to the opportunity, then the customer reference on the opportunity. If neither exists, the working quotation can identify the negotiating opportunity as the party. | Resolve or create a prospect using the organisation or lead name and negotiating opportunity identity. Preparing the quotation may create that prospect even if the sales operator subsequently discards the quotation. |
| Read linked offers | Require access to the opportunity and to the quotation list. Return only readable linked offers with their state, currencies, totals, issue and expiry dates. | The remote integration principal needs access to the selling company's offers. An operator's local opportunity visibility is a separate gate. |
| Convert to customer | On a configured stage, resolve the customer. An order without a customer may discover its originating opportunity from quotation lines. Leave an explicit existing order customer intact. | Require customer synchronisation to be enabled and the authenticated integration principal to be authorized. Retain the returned customer identity at the originating opportunity. |
| Carry the sale forward | Preserve individual quotation-line origins on the order. A refresh of the opportunity's linked offers follows a committed quotation change. | Correlate offers and sales orders using durable identities. Independently operated environments need explicit acknowledgement or reconciliation of the remote result. |

## Select products and amounts

Iterate the opportunity's proposed products. Include only rows whose product has a resolved sellable-item reference. A missing or zero quantity defaults to one, a missing rate defaults to zero and a missing discount defaults to zero. Copy the proposed rate and percentage rather than replacing them with newly changed catalogue values. A linked product at quantity zero, rate 100 and 10% discount supplies a draft line of quantity one and rate 100. A second unlinked product at quantity four and rate 20 supplies no line. The outcome is a prefilled quotation for review. There is no order, receivable or stock commitment at this stage.

A product mirror has a separate lifecycle from a negotiated line. Resolve the sellable item's explicit price in preference to its standard rate, including a legitimate zero price. Update only changed mirrored values and mark the operation so a reciprocal update cannot loop. Links for user restrictions and document shares have their own lifecycle. Removing a share or changing its subject must also be reflected on its linked counterpart.

## Reconcile people and companies

Use organisation name for a corporate customer. Without it, prefer the primary contact's full name and then the lead name to establish an individual customer. Reject a nameless customer. Carry the explicit opportunity identity, contacts, address, territory, industry and transaction currency. Omit territory or industry values that do not exist at the destination.

An existing customer lookup may reuse a matching display name across two opportunities. A contact lookup may reuse a matching email, otherwise telephone. A contact acquires the typed party link only if that exact kind and identity pair is absent. Two unrelated buyers with the same trading name or shared switchboard need a reconciliation decision before using the match as proof of identity. Reconcile addresses and contacts separately from customer creation when a remote reply is lost. A customer identity alone does not prove that an address was saved.

For an order built from quotations for multiple opportunities, the convenience lookup chooses the first opportunity found in order-line sequence. Preserve each line's quotation and opportunity association in reporting. Assigning every line to the first opportunity overstates its commercial value.

## Service customers

An optional customer-care directory mirrors a commercial customer's name, category and image. Store explicit links in both directions, check for an existing mirror and suppress recursive calls while applying changes. Status reporting requires read access to customers on both sides. An actor missing either grant must receive no customer linkage counts. Bulk synchronisation requires write authority, a configured bridge and deduplicated work. An interrupted run resumes by inspecting reciprocal links.

Renaming into an unrelated existing name must fail. A merge with an existing linked counterpart may require a corresponding merge. If the survivor lacks a counterpart, preserve the link of the retired customer. Move only the associated customer restrictions and shares. A ticket assignment grants the handling rights defined by the support policy and cannot by itself expose the party's receivable balance.
