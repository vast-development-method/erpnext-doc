# Evaluate the bounded examples in decisions.json. Amounts use integer cents.
# This optional test oracle is independent of the replacement implementation.
def failure($code): {error: $code};

def resize_delivery:
  . as $input |
  reduce .promised[] as $promised
    ({left: .revised, kept: [], stock: []};
     ([$promised, .left] | min) as $kept |
     if $kept > 0 then
       .left -= $kept | .kept += [$kept] | .stock += [$kept * $input.stockFactor]
     else . end)
  | del(.left);

def remaining_qty:
  ([.ordered, ([.ordered - .returned + .qualifiedCredit, .delivered] | max)] | min) as $ceiling |
  {ceiling: $ceiling, pending: ([0, $ceiling - .netBilled - .mapped] | max)};

def proforma:
  if (.enabled | not) then failure("feature-disabled")
  elif (.submitted | not) then failure("order-unsubmitted")
  elif .qty <= 0 then failure("invalid-quantity")
  elif .lineCents <= 0 then failure("invalid-amount")
  else
    (if .originalTotalCents == 0 then 1 else .lineCents / .originalTotalCents end) as $share |
    (.lineCents + (.freightCents * $share | round) - (.discountCents * $share | round)) as $total |
    if $total < 0 then failure("negative-total")
    else {totalCents: $total, issued: true, ledgerRows: 0} end
  end;

def fixed_plan:
  (.unitCents * (if .prepaid then 1 else .elapsedDays / .days end) | round) as $unit |
  {rateCents: $unit, extendedCents: ($unit * .qty)};

def cash_count:
  (.floatCents + .cashCents - .changeCents + .signedCashRefund) as $cash |
  {expectedCash: $cash, expectedCard: .cardCents, difference: (.countedCash - $cash)};

def rewards:
  (.paid - .threshold) as $excess |
  if $excess <= 0 then {free: .reward}
  else {free: ((($excess / .block | floor) * .reward) +
               (if .minimum == .threshold and .threshold > 0 then .reward else 0 end))}
  end;

def trunc: if . < 0 then ceil else floor end;
def earnings:
  (.grandCents - (.redeemedCents / 100 | trunc) * 100 - .returnsCents) as $eligible |
  {eligibleCents: $eligible, points: ($eligible / .centsPerPoint | trunc)};

def lots:
  if .request > (.first + .second + .priorFirst) then failure("insufficient-points")
  else
    ([.request, .first - .priorFirst] | min) as $first |
    {firstAllocation: $first, secondAllocation: (.request - $first)}
  end;

def time_billing:
  if .billableHours == 0 then failure("no-billable-hours")
  elif .billableHours == .billedHours then failure("hours-fully-billed")
  else
    (.billableHours - .billedHours) as $hours |
    (.billableCents - .billedCents) as $amount |
    {hours: $hours, rateCents: ($amount / $hours), amountCents: $amount}
  end;

def admission:
  . as $slot |
  ([.existing[] | select(.status == "Open" and
    (.start < $slot.start + $slot.duration) and (.start > $slot.start - $slot.duration))] | length) as $count |
  if $slot.capacity > 0 and $count >= $slot.capacity then failure("capacity-full")
  else {accepted: true} end;

def evaluate:
  .operation as $op | .input |
  if $op == "resize-delivery-promises" then resize_delivery
  elif $op == "remaining-invoice-quantity" then remaining_qty
  elif $op == "issue-proforma" then proforma
  elif $op == "price-fixed-plan" then fixed_plan
  elif $op == "session-cash" then cash_count
  elif $op == "close-session-membership" then
    if ((.eligibleNow - .included) | length) == 0 then {complete: true} else failure("receipt-missing") end
  elif $op == "repeat-free-units" then rewards
  elif $op == "earn-points" then earnings
  elif $op == "allocate-redeemed-lots" then lots
  elif $op == "service-invoice" then time_billing
  elif $op == "admit-appointment" then admission
  elif $op == "select-service-agreement" then
    .already as $selected | {selected: (if (.eligible | index($selected)) != null then $selected else .eligible[0] end)}
  elif $op == "retry-bulk-conversion" then
    {tasksStarted: (if .laterSuccess then 0 else 1 end),
     status: (if (.laterSuccess | not) and .workerSucceeds then "Success" else "Failed" end), retried: true}
  elif $op == "resolve-code-version" then
    {version: (.pinned // (.versions | max_by(tonumber)))}
  elif $op == "campaign-efficiency" then
    {opportunitiesPerLeadPct: (.opportunities * 100 / .leads),
     quotesPerLeadPct: (.submittedQuotes * 100 / .leads),
     orderedQuotesPct: (.orderedQuotes * 100 / ([.submittedQuotes,1] | max))}
  elif $op == "weighted-approval-discount" then
    ([.lines[] | .qty * (if .listCents != 0 then .listCents else .actualCents end)] | add // 0) as $list |
    (([.lines[] | .qty * .actualCents] | add // 0) - .extraDiscountCents) as $actual |
    {discountBasisPoints: (if $list == 0 then 0 else 10000 - $actual * 10000 / $list end)}
  elif $op == "quote-choice-set" then
    . as $q |
    ([{need: .mainQty, got: .mainOrdered}, {need: .alternativeQty, got: .alternativeOrdered}] |
     map(select(.got > 0))) as $selected |
    (if ($selected | length) > 0 then $selected else [{need: .mainQty, got: .mainOrdered}] end) as $choice |
    {status: (if (.mainOrdered + .alternativeOrdered + .serviceOrdered) == 0 then "Open"
              elif (all($choice[]; .got >= .need)) and $q.serviceOrdered >= $q.serviceQty then "Ordered"
              else "Partially Ordered" end)}
  else error("Unknown operation " + $op) end;

[.cases[] | . as $case | evaluate as $actual |
 select($actual != $case.expected) | {id: $case.id, actual: $actual, expected: $case.expected}] as $failures |
if ($failures | length) > 0 then error($failures | tojson)
else {passed: (.cases | length), operations: ([.cases[].operation] | unique | length)} end
