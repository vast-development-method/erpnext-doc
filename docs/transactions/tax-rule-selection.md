# Selecting a tax template before calculating tax

Tax classification resolves one ordered template before the [tax and pricing engine](taxation-and-pricing.md) calculates line taxes, included amounts and invoice totals. The request carries a posting date and explicitly supplied selection keys. Relevant keys are sales/purchase side, company, tax category, party or party group, item or item group, billing and shipping geography and optionally the shopping-cart flag. The result is one template identity or no template. The lookup posts no journal.

##

For a sales rule, clear supplier fields and purchase template. A specific customer clears its group. Apply the symmetric transformation for purchase. Require the corresponding template and validate the validity dates. Conflict detection compares the normalized selector fields (empty and null treated the same) and excludes the edited row. It uses strict interior date tests and an explicit identical-interval check for two bounded intervals, a strict end/start comparison for one-sided input, and no date predicate for a rule with neither bound. An existing rule ending on the new rule's start can therefore pass this write check even though both can apply that day. The first matching conflict candidate is compared with the new priority. This check supplies neither a universal overlap test nor a deterministic tiebreak for records already present. The shopping-cart flag is absent from this conflict key.

## Rule selection

| Step | Decision |
|---|---|
| Time | On a supplied date require `start ≤ date ≤ end`, treating a missing endpoint as open. Without a posting date permit only rules with both endpoints absent. |
| Category and cart | Add an empty tax category if missing. Require exact normalized category equality. A generic empty category does **not** match a specified category. If the request includes the shopping-cart flag, require exact equality for it. |
| Groups | For a supplied customer or supplier group accept that group, any ancestor, or an empty group. If supplied as empty, use the hierarchy root in the ancestor lookup. The item-group key follows the ordinary matching branch here. |
| Other supplied keys | Accept equality or an empty rule value. A key absent from the request does not constrain the query or contribute to its ranking. An explicitly empty ordinary key matches an empty rule field. |
| Rank | Count the truthy, nonempty rule fields among the supplied keys (including the defaulted category). More matched keys wins. On equal score the **larger numeric priority** wins. A group ancestor and an exact group each count as one matched key. A false cart flag does not add a point. |
| Resolve | Choose the first ranked rule and resolve its template. If that template is disabled, return no template. There is no search for a lower ranked enabled rule. No candidate also returns no template. Equal score and priority lack a final explicit ordering; record the ambiguity in an implementation profile. |

Example: common fields are `Sales`, company `A`, empty category. Rule A additionally matches a customer and has priority 100. Rule B matches the customer and billing city and has priority 1. B wins for that city. Rule C with the same selectors as B and priority 3 wins over B. Disabling C's template leaves the transaction without a selected template. Supplying category `Exports` drops A, B and C unless an `Exports` rule exists. See `FIN-011`–`FIN-013` in the [vectors](examples/financial-decisions.json).

The externally callable address helper separately checks access to the named party and the selected billing and shipping addresses before it returns geography. Explicit address identifiers must refer to single addresses. Missing arguments trigger the party's default billing and shipping address lookups. Copy billing and shipping city, county, state, postal code and country under separate keys. Keep this lookup read-only and apply the same authority checks to integrations. A selected template expresses configured business policy; jurisdictional compliance requires its own verified rate and effective dates.
