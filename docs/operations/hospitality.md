# Room inventory, restaurant orders and guest billing

## Room products and nightly pricing

A room belongs to one room type. Its occupant capacity and extra-bed capacity describe accommodation within that physical room. A room package links a room type to a saleable product and its included or billable amenities. Multiple packages may sell the same type of room. A reservation holds a guest, customer, arrival, departure, state and one or more package–room-count rows. Keep customer identity distinct from guest name so one organisation can pay for several stays.

For each package row, iterate the nights from arrival inclusive to departure exclusive. For each night, find a rate for its product in a pricing interval whose start and end include that night. A missing rate rejects the reservation and identifies the affected night. The stay rate is the sum of nightly rates. Multiply by the number of rooms on that row. Reservation net amount is the sum of the row amounts. An enabled flag exists on a tariff, but this particular lookup selects by interval and product. Overlapping tariffs offer more than one candidate without a documented tie-break. Use nonoverlapping intervals when a unique price is required.

Two rooms for two nights, with nightly prices 900 and 1,100, have a stay rate of 2,000 and a line amount of 4,000. The last morning contributes no nightly charge. Quoting dates returns the priced rows. Quoting alone creates neither occupancy nor a receivable.

## Availability and occupancy reporting

For each night to be reserved and each requested package, count physical rooms of its type. Sum quantities on submitted reservation lines for that room type and day, excluding the reservation under edit. **The existing reservation's date interval includes its departure day** in this count. A new reservation with arrival on a sold-out stay's departure day can therefore fail even though the earlier stay collects no charge for that night.

Keep a running counter per package within each day of the new reservation. If $B$ rooms are occupied on persisted reservations, $q$ rooms are requested on the current row and the running counter is $R$, compare $B+q+R$ to physical rooms of that type. Excess rejects. After passing, increase $R$ by the entire tested amount. For two identical package rows, one already booked room and one room requested on each row, the first comparison is 2 and the second 4. A capacity of three rejects the second row. Two different packages for the same room type have separate in-document counters even though their existing occupancies come from the same room type. Split package rows can accordingly behave differently from a consolidated request. Reconcile room-type totals when reviewing availability.

The occupancy report groups by room type. For each day in the report interval, start inclusive and end exclusive, add the submitted reserved-room quantity using the same inclusive existing-reservation occupancy rule. Its output is **summed booked room-days**, including zero for a type with none. It is neither a count of distinct rooms nor a percentage. A one-room stay from day 1 to day 3 contributes three room-days to a report covering days 1, 2 and 3 although its tariff charges for two nights.

The reservation operator manages guest reservations. The hotel manager manages room types, physical rooms and rates. A system administrator manages package master data. Reading reservation totals does not by itself authorise posting an invoice, recording payment or changing the master room count.

## Restaurant menu and table workflow

| Step | Record decisions and consequences |
|---|---|
| Publish the menu | A restaurant selects an active menu, default customer, company and tax template. A menu owns product and rate rows. A zero or missing menu rate falls back to the product's standard rate. Saving gets or creates a selling price list associated with the menu, enables it, clears its previous prices and installs one current price per menu row. Deleting the menu clears its prices. An issued invoice retains its price. |
| Reserve a table service time | Record the restaurant, party size, customer and contact, start time and reservation status. When no end is entered, the end defaults to one hour after the start. Store restaurant table seating separately. A service reservation alone has no payment or posting effect. |
| Open a table | Resolve the table's restaurant and active menu. Missing table or active menu stops the operation. Reuse the draft invoice linked to that table, otherwise open a point-of-sale invoice with the restaurant's numbering policy and default customer. Missing default customer prevents opening a new invoice. Read the current tax template and enabled menu price list. |
| Record the order | Search for products from the active menu. Send the complete current order for the selected table. Replace the draft's item lines with the supplied products and quantities, retain the table linkage and save. A second identical save is replacement of the same draft. Concurrent independent edits need a common draft identity and conflict handling to preserve both users' intentions. |
| Settle | Resolve the active table invoice, set the actual customer and restaurant, calculate tax and total, add a payment for the grand total using the selected payment mode, then save and submit. The submitted invoice is the financial event. After settlement it is outside the table's open-draft search. Distinguish recovery of that issued invoice from opening a fresh order for later guests. |

A table ordering two dishes at 50 and one at 30 has a pretax total of 130. With a separately applied, exclusive 10% tax and no other adjustments, the invoice total is 143 and the selected settlement amount is 143. A prior save of the table draft must produce no duplicate sale. The restaurant manager's access to menus, tables and order entry is separate from any cashier rights needed to submit the invoice.
