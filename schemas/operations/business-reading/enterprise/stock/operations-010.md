# Inventory and warehouses · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Delivery trip

[Record definition](../../../../data/record-types/delivery_trip.json)

<a id="op-136cd3943f4e42"></a>
### Delivery Trip.validate driver

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_deliverytrip_validate_driver`

**Inputs** self.

**Record and data access** read “Driver” via get\_value.

**Explicit failure paths** validation helper — translated “The driver must be active to submit a Delivery Trip.” · validation helper — translated “The driver's licence must be valid on the departure date.”.

**Local steps**

- Set tuple(status, expiry\_date) from Platform.db.get\_value(“Driver”, self.driver, list(“status”, “expiry\_date”)).
- If status differs from “Active”.
  - Call the validation error handler Platform.throw(translated “The driver must be active to submit a Delivery Trip.”).
- If (expiry\_date and getdate(expiry\_date) &lt; getdate(self.departure\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expiry\_date → getdate(expiry\_date) &lt; getdate(self.departure\_time).
  - Call the validation error handler Platform.throw(translated “The driver's licence must be valid on the departure date.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L263)

<a id="op-2fb7c7808c3552"></a>
### Delivery Trip.validate delivery note not draft

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_validate_delivery_note_not_draft`

**Inputs** self.

**Record and data access** read “Delivery Note” via get\_all.

**Explicit failure paths** validation helper — translated “Delivery Notes should not be in draft state when submitting a Delivery Trip. The following Delivery Notes ar …”.format(“, ”.join(draft\_delivery\_notes)).

**Local steps**

- Set delivery\_notes from list(set(generator of stop.delivery\_note for stop drawn from self.delivery\_stops where stop.delivery\_note)).
  - Draw stop from self.delivery\_stops, keep a combination only if (stop.delivery\_note).
- Set draft\_delivery\_notes from Platform.get\_all(“Delivery Note”, mapping(“docstatus” → 0, “name” → list(“in”, delivery\_notes)), pluck = “name”).
- If draft\_delivery\_notes.
  - Call the validation error handler Platform.throw(translated “Delivery Notes should not be in draft state when submitting a Delivery Trip. The following Delivery Notes ar …”.format(“, ”.join(draft\_delivery\_notes))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2944) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L982)

<a id="op-7320c44914e1c9"></a>
### Delivery Trip.validate delivery notes not on other trips

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_deliverytrip_validate_delivery_notes_not_on_other_trips`

**Inputs** self.

**Record and data access** read “Delivery Trip” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Delivery Notes {0} do not belong to Company {1}”.format(“, ”.join(other\_company), Platform.bold(self.company)) · validation helper — translated “Delivery Notes are already on another Delivery Trip: {0}”.format(“, ”.join(generator of formatted text {d.name} ({d.delivery\_trip}) for d drawn from linked)).

**Local steps**

- Set delivery\_notes from set of stop.delivery\_note for stop drawn from self.delivery\_stops where stop.delivery\_note.
  - Draw stop from self.delivery\_stops, keep a combination only if (stop.delivery\_note).
- If not delivery\_notes.
  - Return no value.
- Set delivery\_note from Platform.qb.DocType(“Delivery Note”).
- Set notes from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(delivery\_notes)).for\_update().run(as ….
- If other\_company bound to list of d.name for d drawn from notes where (self.company and d.company differs from self.company).
  - Draw d from notes, keep a combination only if ((self.company and d.company differs from self.company)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → d.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Delivery Notes {0} do not belong to Company {1}”.format(“, ”.join(other\_company), Platform.bold(self.company))).
- Set other\_trips from set of d.delivery\_trip for d drawn from notes where (d.delivery\_trip and d.delivery\_trip differs from self.name).
  - Draw d from notes, keep a combination only if ((d.delivery\_trip and d.delivery\_trip differs from self.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.delivery\_trip → d.delivery\_trip differs from self.name.
- Set open\_trips from (other\_trips and set(Platform.get\_all(“Delivery Trip”, filters = mapping(“name” → tuple(“in”, list(other\_trips)), “docstatus” → tuple(“&lt;”, 2)), pluck = “name”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in other\_trips → set(Platform.get\_all(“Delivery Trip”, filters = mapping(“name” → tuple(“in”, list(other\_trips)), “docstatus” → tuple(“&lt;”, 2)), pluck = “name”)).
- If linked bound to list of d for d drawn from notes where (open\_trips and d.delivery\_trip belongs to open\_trips).
  - Draw d from notes, keep a combination only if ((open\_trips and d.delivery\_trip belongs to open\_trips)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in open\_trips → d.delivery\_trip belongs to open\_trips.
  - Call the validation error handler Platform.throw(translated “Delivery Notes are already on another Delivery Trip: {0}”.format(“, ”.join(generator of formatted text {d.name} ({d.delivery\_trip}) for d drawn from linked))).
    - Draw d from linked.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L262)

<a id="op-a4f8e6794f2c38"></a>
### Delivery Trip.update status

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_update_status`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set status from mapping(0 → “Draft”, 1 → “Scheduled”, 2 → “Cancelled”) at self.docstatus.
- If self.docstatus equals 1.
  - Set visited\_stops from list of stop.visited for stop drawn from self.delivery\_stops.
    - Draw stop from self.delivery\_stops.
  - If all(visited\_stops).
    - Set status from “Completed”.
  - Otherwise.
    - If any(visited\_stops).
      - Set status from “In Transit”.
- Evaluate self.db\_set(“status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L3226) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L980)

<a id="op-59bdfb429d9e4c"></a>
### Delivery Trip.release removed delivery notes

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_deliverytrip_release_removed_delivery_notes`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- Set current from set of stop.delivery\_note for stop drawn from self.delivery\_stops.
  - Draw stop from self.delivery\_stops.
- Set removed from set of stop.delivery\_note for stop drawn from doc\_before\_save.delivery\_stops where stop.delivery\_note.
  - Draw stop from doc\_before\_save.delivery\_stops, keep a combination only if (stop.delivery\_note).
- If (removed − current).
  - Evaluate self.update\_delivery\_notes(delete = true, delivery\_notes = (removed − current)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update delivery notes](operations-010.md#op-ce086a65ec0526).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L261)

<a id="op-ce086a65ec0526"></a>
### Delivery Trip.update delivery notes

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_update_delivery_notes`

**Inputs** self, delete = false, delivery\_notes = no value.

**Record and data access** read “Delivery Note” via get\_all.

**State and service calls** request set\_value on “Delivery Note” · msgprint with translated “Delivery Notes {0} updated”.format(“, ”.join(updated)).

**Explicit results** no value.

**Local steps**

- If delivery\_notes is identical to no value.
  - Set delivery\_notes from set of stop.delivery\_note for stop drawn from self.delivery\_stops where stop.delivery\_note.
    - Draw stop from self.delivery\_stops, keep a combination only if (stop.delivery\_note).
- If not delivery\_notes.
  - Return no value.
- Set trip\_values from list(self.get\_delivery\_note\_values()).
- If doc\_before\_save bound to self.get\_doc\_before\_save().
  - Evaluate trip\_values.append(doc\_before\_save.get\_delivery\_note\_values()).
- Set updated from list().
- For each note in Platform.get\_all(“Delivery Note”, filters = mapping(“name” → tuple(“in”, list(delivery\_notes))), fields = list(“name”, “delivery\_trip”, expanded trip\_values at 0)).
  - Set update from release\_delivery\_note when delete, otherwise link\_delivery\_note.
    - Value choice on delete — true gives release\_delivery\_note, false gives link\_delivery\_note.
  - If values bound to update(note, self.name, trip\_values).
    - Evaluate Platform.db.set\_value(“Delivery Note”, note.name, values).
    - Evaluate updated.append(get\_link\_to\_form(“Delivery Note”, note.name)).
- If updated.
  - Evaluate Platform.msgprint(translated “Delivery Notes {0} updated”.format(“, ”.join(updated))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get delivery note values](operations-010.md#op-bb5bfe056a3e96).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L979)

<a id="op-bb5bfe056a3e96"></a>
### Delivery Trip.get delivery note values

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_deliverytrip_get_delivery_note_values`

**Inputs** self.

**Explicit results** mapping(“driver” → self.driver, “driver\_name” → self.driver\_name, “vehicle\_no” → self.vehicle, “lr\_no” → self.name, …).

**Local steps**

- Return mapping(“driver” → self.driver, “driver\_name” → self.driver\_name, “vehicle\_no” → self.vehicle, “lr\_no” → self.name, …).
  - Value choice on self.departure\_time — true gives getdate(self.departure\_time), false gives no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L260)

<a id="op-ff62620e0ca540"></a>
### Delivery Trip.process route

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_process_route`

**Inputs** self, optimize.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Delivery Settings” via get\_single\_value.

**State and service calls** call save on self.

**Local steps**

- Set departure\_datetime from get\_datetime(self.departure\_time).
- Set route\_list from self.form\_route\_list(optimize).
- Set ends\_at\_home from not (optimize and self.delivery\_stops and self.delivery\_stops at negative 1.locked).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in optimize → self.delivery\_stops → self.delivery\_stops at negative 1.locked.
- Set total\_distance from no value.
- Set idx from 0.
- For each tuple(route\_idx, route) in enumerate(route\_list).
  - Set directions from self.get\_directions(route, optimize).
  - If directions.
    - If (optimize and len(directions.get(“waypoint\_order”)) &gt; 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in optimize → len(directions.get(“waypoint\_order”)) &gt; 1.
      - Evaluate self.rearrange\_stops(directions.get(“waypoint\_order”), start = idx).
    - Set legs from directions.get(“legs”).
    - If (ends\_at\_home and route\_idx equals (len(route\_list) − 1)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ends\_at\_home → route\_idx equals (len(route\_list) − 1).
      - Set legs from legs at slice no value to negative 1.
    - For each leg in legs.
      - Set delivery\_stop from self.delivery\_stops at idx.
      - Set tuple(delivery\_stop.lat, delivery\_stop.lng) from leg.get(“end\_location”, mapping()).values().
      - Set delivery\_stop.uom from self.default\_distance\_uom.
      - Set distance from leg.get(“distance”, mapping()).get(“value”, 0.0).
      - Set delivery\_stop.distance from (distance × self.uom\_conversion\_factor).
      - Set duration from leg.get(“duration”, mapping()).get(“value”, 0).
      - Set estimated\_arrival from (departure\_datetime + datetime.timedelta(seconds = duration)).
      - Set delivery\_stop.estimated\_arrival from estimated\_arrival.
      - Set stop\_delay from Platform.db.get\_single\_value(“Delivery Settings”, “stop\_delay”).
      - Set departure\_datetime from (estimated\_arrival + datetime.timedelta(minutes = cint(stop\_delay))).
      - Update idx using + 1.
    - Set total\_distance from (flt(total\_distance) + sum(generator of nested operand in the contract.get(“distance”, mapping()).get(“value”, 0.0) for leg drawn from directions.get(“legs”))).
      - Draw leg from directions.get(“legs”).
  - Otherwise.
    - Update idx using + (len(route) − 1).
- If total\_distance is distinct from no value.
  - Set self.uom from self.default\_distance\_uom.
  - Set self.total\_distance from (total\_distance × self.uom\_conversion\_factor).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [form route list](operations-010.md#op-064d0cb3c2368c), [get directions](operations-010.md#op-5cd0801f12be9f), [rearrange stops](operations-010.md#op-78240d9769dc54).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Delivery Settings”, “stop\_delay”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L977)

<a id="op-064d0cb3c2368c"></a>
### Delivery Trip.form route list

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_form_route_list`

**Inputs** self, optimize.

**Record and data access** resolve a document from “Address” via get\_doc.

**Explicit results** route\_list.

**Explicit failure paths** validation helper — translated “Cannot Calculate Arrival Time as Driver Address is Missing.”.

**Local steps**

- If not self.driver\_address.
  - Call the validation error handler Platform.throw(translated “Cannot Calculate Arrival Time as Driver Address is Missing.”).
- Set home\_address from get\_address\_display(Platform.get\_doc(“Address”, self.driver\_address).as\_dict()).
- Set route\_list from list().
- Set leg from list(home\_address).
- For each stop in self.delivery\_stops.
  - Evaluate leg.append(stop.customer\_address).
  - If (optimize and stop.locked).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in optimize → stop.locked.
    - Evaluate route\_list.append(leg).
    - Set leg from list(stop.customer\_address).
- If len(leg) &gt; 1.
  - Evaluate leg.append(home\_address).
  - Evaluate route\_list.append(leg).
- Set route\_list from list of list of sanitize\_address(address) for address drawn from route for route drawn from route\_list.
  - Draw route from route\_list.
  - Draw address from route.
- Return route\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L968)

<a id="op-78240d9769dc54"></a>
### Delivery Trip.rearrange stops

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_rearrange_stops`

**Inputs** self, optimized\_order, start.

**Local steps**

- Set stops\_order from list().
- For each tuple(new\_idx, old\_idx) in enumerate(optimized\_order, 1).
  - Set new\_idx from (start + new\_idx).
  - Set old\_idx from (start + old\_idx).
  - Set self.delivery\_stops at old\_idx.idx from new\_idx.
  - Evaluate stops\_order.append(self.delivery\_stops at old\_idx).
- Set self.delivery\_stops at slice start to (start + len(stops\_order)) from stops\_order.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L5667) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L978)

<a id="op-5cd0801f12be9f"></a>
### Delivery Trip.get directions

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_get_directions`

**Inputs** self, route, optimize.

**Record and data access** read “Google Settings” via get\_single\_value.

**Explicit results** directions at 0 when directions, otherwise false.

**Explicit failure paths** validation helper — translated “Enter API key in Google Settings.” · validation helper — e · validation helper — translated str(e).

**Local steps**

- If not Platform.db.get\_single\_value(“Google Settings”, “api\_key”).
  - Call the validation error handler Platform.throw(translated “Enter API key in Google Settings.”).
- Bind dependencies googlemaps.
- Attempt the following.
  - Set maps\_client from googlemaps.Client(key = Platform.db.get\_single\_value(“Google Settings”, “api\_key”)).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(e).
- Set directions\_data from mapping(“origin” → route at 0, “destination” → route at negative 1, “waypoints” → route at slice 1 to negative 1, “optimize\_waypoints” → optimize).
- Attempt the following.
  - Set directions from maps\_client.directions(expanded names directions\_data).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated str(e)).
- Return directions at 0 when directions, otherwise false.
  - Value choice on directions — true gives directions at 0, false gives false.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Google Settings”, “api\_key”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L5925) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L969)

<a id="op-ed55b7bd203be9"></a>
### Is trip value

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_is_trip_value`

**Inputs** note, field, trip\_values.

**Explicit results** any(generator of cstr(note.get(field)) equals cstr(values at field) for values drawn from trip\_values).

**Local steps**

- Return any(generator of cstr(note.get(field)) equals cstr(values at field) for values drawn from trip\_values).
  - Draw values from trip\_values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L265)

<a id="op-31130da9a504b5"></a>
### Link delivery note

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_link_delivery_note`

**Inputs** note, trip\_name, trip\_values.

**Explicit results** values.

**Local steps**

- Set values from mapping() when note.delivery\_trip equals trip\_name, otherwise mapping(“delivery\_trip” → trip\_name).
  - Value choice on note.delivery\_trip equals trip\_name — true gives mapping(), false gives mapping(“delivery\_trip” → trip\_name).
- For each tuple(field, value) in trip\_values at 0.items().
  - If (note.get(field) differs from value and (not note.get(field) or is\_trip\_value(note, field, trip\_values))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in note.get(field) differs from value → (not note.get(field) or is\_trip\_value(note, field, trip\_values)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not note.get(field) → is\_trip\_value(note, field, trip\_values).
    - Set values at field from value.
- Return values.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L266)

<a id="op-2055d493c73943"></a>
### Release delivery note

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_release_delivery_note`

**Inputs** note, trip\_name, trip\_values.

**Explicit results** mapping() · values.

**Local steps**

- If note.delivery\_trip differs from trip\_name.
  - Return mapping().
- Set values from mapping(“delivery\_trip” → no value).
- For each field in trip\_values at 0.
  - If (note.get(field) and is\_trip\_value(note, field, trip\_values)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in note.get(field) → is\_trip\_value(note, field, trip\_values).
    - Set values at field from no value.
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L267)

<a id="op-6f72fa33aea576"></a>
### Get contact and address

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_get_contact_and_address`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** out.

**Local steps**

- Evaluate Platform.has\_permission(“Customer”, ptype = “select”, doc = name, throw = true).
- Set out from Platform.\_dict().
- Evaluate get\_default\_contact(out, name).
- Evaluate get\_default\_address(out, name).
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, ptype = “select”, doc = name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L985)

<a id="op-843666c2a704de"></a>
### Get default contact

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_get_default_contact`

**Inputs** out, name.

**Record and data access** execute query text (SELECT, Contact c, Dynamic Link).

**Explicit results** out.contact\_person.

**Local steps**

- Set contact\_persons from Platform.db.sql(query text (SELECT, Contact c, Dynamic Link), name, as\_dict = 1).
- If contact\_persons.
  - For each out.contact\_person in contact\_persons.
    - If out.contact\_person.is\_primary\_contact.
      - Return out.contact\_person.
  - Set out.contact\_person from contact\_persons at 0.
  - Return out.contact\_person.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L988)

<a id="op-4d678e519c8d73"></a>
### Get default address

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_get_default_address`

**Inputs** out, name.

**Record and data access** execute query text (SELECT, Address a, Dynamic Link).

**Explicit results** out.shipping\_address.

**Local steps**

- Set shipping\_addresses from Platform.db.sql(query text (SELECT, Address a, Dynamic Link), name, as\_dict = 1).
- If shipping\_addresses.
  - For each out.shipping\_address in shipping\_addresses.
    - If out.shipping\_address.is\_shipping\_address.
      - Return out.shipping\_address.
  - Set out.shipping\_address from shipping\_addresses at 0.
  - Return out.shipping\_address.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L987)

<a id="op-b1f559a5a7b859"></a>
### Get contact display

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_get_contact_display`

**Inputs** contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Contact” via get\_value.

**Explicit results** contact\_info.html.

**Local steps**

- If not Platform.has\_permission(“Contact”, “read”, doc = contact).
  - Evaluate check\_contact\_customer\_permission(contact).
- Set contact\_info from Platform.db.get\_value(“Contact”, contact, list(“first\_name”, “last\_name”, “phone”, “mobile\_no”), as\_dict = 1).
- Set contact\_info.html from “ &lt;b&gt;{first\_name} {last\_name}&lt;/b&gt; &lt;br&gt; {phone} &lt;br&gt; {mobile\_no}”.format(first\_name = contact\_info.first\_name, last\_name = (contact\_info.last\_name or empty text), phone = (contact\_info.phone or empty text), ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact\_info.last\_name → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact\_info.phone → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact\_info.mobile\_no → empty text.
- Return contact\_info.html.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”, “read”, doc = contact).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L986)

<a id="op-7c2dfd5c3afa1f"></a>
### Check contact customer permission

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_check_contact_customer_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** contact.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L259)

<a id="op-6fed48b4a53294"></a>
### Sanitize address

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_sanitize_address`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** address.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0727.json#L340) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L991)

<a id="op-3136c8c6642ea0"></a>
### Notify customers

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_notify_customers`

**Inputs** delivery\_trip.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Delivery Trip” via get\_doc · read “Delivery Settings” via get\_single\_value · resolve a document from “Email Template” via get\_doc · read “Driver” via get\_value · read “Contact” via get\_value · 1 additional forms in the steps below.

**State and service calls** sendmail · call db\_set on stop · msgprint with translated “Email sent to {0}”.format(“, ”.join(email\_recipients)) · call db\_set on delivery\_trip · msgprint with translated “No contacts with email IDs found.”.

**Explicit failure paths** validation helper — translated “Customers can be notified only for a submitted Delivery Trip” · validation helper — translated “Missing email template for dispatch. Please set one in Delivery Settings.”.

**Local steps**

- Set delivery\_trip from Platform.get\_doc(“Delivery Trip”, delivery\_trip).
- Evaluate delivery\_trip.check\_permission().
- <a id="op-3136c8c6642ea0-guard-4"></a>If delivery\_trip.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Customers can be notified only for a submitted Delivery Trip”).
- For each delivery\_note in set of stop.delivery\_note for stop drawn from delivery\_trip.delivery\_stops where stop.delivery\_note.
  - Draw stop from delivery\_trip.delivery\_stops, keep a combination only if (stop.delivery\_note).
  - Evaluate Platform.has\_permission(“Delivery Note”, “read”, doc = delivery\_note, throw = true).
- Set dispatch\_template\_name from Platform.db.get\_single\_value(“Delivery Settings”, “dispatch\_template”).
- If not dispatch\_template\_name.
  - Call the validation error handler Platform.throw(translated “Missing email template for dispatch. Please set one in Delivery Settings.”).
- Set dispatch\_template from Platform.get\_doc(“Email Template”, dispatch\_template\_name).
- Set context from delivery\_trip.as\_dict().
- If delivery\_trip.driver.
  - Evaluate context.update(Platform.db.get\_value(“Driver”, delivery\_trip.driver, “cell\_number”, as\_dict = 1)).
- Set email\_recipients from list().
- For each stop in delivery\_trip.delivery\_stops.
  - Set contact\_info from Platform.db.get\_value(“Contact”, stop.contact, list(“first\_name”, “last\_name”, “email\_id”), as\_dict = 1).
  - Evaluate context.update(mapping(“items” → list())).
  - If stop.delivery\_note.
    - Set items from Platform.get\_all(“Delivery Note Item”, filters = mapping(“parent” → stop.delivery\_note, “docstatus” → 1), fields = list(“\*”)).
    - Evaluate context.update(mapping(“items” → items)).
  - If (contact\_info and contact\_info.email\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact\_info → contact\_info.email\_id.
    - Evaluate context.update(stop.as\_dict()).
    - Evaluate context.update(contact\_info).
    - Evaluate Platform.sendmail(recipients = contact\_info.email\_id, subject = dispatch\_template.get\_formatted\_subject(context), message = dispatch\_template.get\_formatted\_response(context), attachments = get\_attachments(stop)).
    - Evaluate stop.db\_set(“email\_sent\_to”, contact\_info.email\_id).
    - Evaluate email\_recipients.append(contact\_info.email\_id).
- If email\_recipients.
  - Evaluate Platform.msgprint(translated “Email sent to {0}”.format(“, ”.join(email\_recipients))).
  - Evaluate delivery\_trip.db\_set(“email\_notification\_sent”, 1).
- Otherwise.
  - Evaluate Platform.msgprint(translated “No contacts with email IDs found.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison delivery\_trip.docstatus differs from 1, delivery\_trip.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Customers can be notified only for a submitted Delivery Trip”. With delivery\_trip.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3136c8c6642ea0-guard-4)

**Values supplied outside this operation** effective access from delivery\_trip.check\_permission(), Platform.has\_permission(“Delivery Note”, “read”, doc = delivery\_note, throw = true) · configured or stored value from Platform.db.get\_single\_value(“Delivery Settings”, “dispatch\_template”) · service or queued work from Platform.sendmail(recipients = contact\_info.email\_id, subject = dispatch\_template.get\_formatted\_subject(context), message = dispatch\_template.get\_formatted\_response(context), attachments = get\_attachments(stop)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L990)

<a id="op-ff5318b4ed4df9"></a>
### Get attachments

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_get_attachments`

**Inputs** delivery\_stop.

**Record and data access** read “Delivery Settings” via get\_single\_value.

**Explicit results** list() · list(attachments).

**Local steps**

- If not (Platform.db.get\_single\_value(“Delivery Settings”, “send\_with\_attachment”) and delivery\_stop.delivery\_note).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Delivery Settings”, “send\_with\_attachment”) → delivery\_stop.delivery\_note.
  - Return list().
- Set dispatch\_attachment from Platform.db.get\_single\_value(“Delivery Settings”, “dispatch\_attachment”).
- Set attachments from Platform.attach\_print(“Delivery Note”, delivery\_stop.delivery\_note, file\_name = “Delivery Note”, print\_format = dispatch\_attachment).
- Return list(attachments).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Delivery Settings”, “send\_with\_attachment”), Platform.db.get\_single\_value(“Delivery Settings”, “dispatch\_attachment”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0727.json#L1482) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L984)

<a id="op-d72eb309572126"></a>
### Get driver email

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_get_driver_email`

**Inputs** driver.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Driver” via get\_value · read “Employee” via get\_value.

**Explicit results** mapping(“email” → email).

**Local steps**

- Evaluate Platform.has\_permission(“Driver”, “select”, doc = driver, throw = true).
- Set driver\_data from Platform.db.get\_value(“Driver”, driver, list(“user”, “employee”), as\_dict = true).
- Set email from driver\_data.user.
- If (not email and driver\_data.employee and Platform.has\_permission(“Employee”, “read”, doc = driver\_data.employee)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not email → driver\_data.employee → Platform.has\_permission(“Employee”, “read”, doc = driver\_data.employee).
  - Set employee from Platform.db.get\_value(“Employee”, driver\_data.employee, list(“company\_email”, “prefered\_email”), as\_dict = true).
  - Set email from (employee.company\_email or employee.prefered\_email).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee.company\_email → employee.prefered\_email.
- Return mapping(“email” → email).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Driver”, “select”, doc = driver, throw = true), Platform.has\_permission(“Employee”, “read”, doc = driver\_data.employee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L989)

## Service · Deprecated serial batch

<a id="op-5b41b541970966"></a>
### Has legacy batch ledgers

`operation_enterprise_binding_enterprise_stock_deprecated_serial_batch_has_legacy_batch_ledgers`

**Inputs** item\_code, warehouse.

**Wrappers, in declaration order** Platform.request\_cache.

**Declared result** bool.

**Explicit results** bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Return bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L196)
