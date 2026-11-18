# Record lifecycle and persistence · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-d9bba948775069"></a>
### Database.get default

`operation_foundation_database_business_behavior_database_get_default`

**Inputs** self, key, parent = “\_\_default”.

**Explicit results** ((isinstance(d, list) and d at 0) or d).

**Local steps**

- Set d from self.get\_defaults(key, parent).
- Return ((isinstance(d, list) and d at 0) or d).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (isinstance(d, list) and d at 0) → d.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(d, list) → d at 0.

**Methods declared on this owner** [get defaults](operations-019.md#op-bd7becb2118a2e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L7770) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1068)

<a id="op-dc820da7a7a9aa"></a>
### Database.set default

`operation_foundation_database_business_behavior_database_set_default`

**Inputs** key, val, parent = “\_\_default”, parenttype = no value.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Evaluate Platform.defaults.set\_default(key, val, parent, parenttype).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L7905) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1106)

<a id="op-61f846618b0870"></a>
### Database.add default

`operation_foundation_database_business_behavior_database_add_default`

**Inputs** key, val, parent = “\_\_default”, parenttype = no value.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Evaluate Platform.defaults.add\_default(key, val, parent, parenttype).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L8008) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1031)

<a id="op-bd7becb2118a2e"></a>
### Database.get defaults

`operation_foundation_database_business_behavior_database_get_defaults`

**Inputs** key = no value, parent = “\_\_default”.

**Wrappers, in declaration order** staticmethod.

**Explicit results** defaults · defaults at key · defaults.get(Platform.scrub(key)).

**Local steps**

- Set defaults from Platform.defaults.get\_defaults\_for(parent).
- If not key.
  - Return defaults.
- If key belongs to defaults.
  - Return defaults at key.
- Return defaults.get(Platform.scrub(key)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L8111) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1069)

<a id="op-572c679dd95d6b"></a>
### Database.begin

`operation_foundation_database_business_behavior_database_begin`

**Inputs** self, read\_only (named only, default false).

**Local steps**

- Set read\_only from (read\_only or Platform.flags.read\_only or self.in\_read\_only\_transaction).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in read\_only → Platform.flags.read\_only → self.in\_read\_only\_transaction.
- Set mode from “READ ONLY” when read\_only, otherwise empty text.
  - Value choice on read\_only — true gives “READ ONLY”, false gives empty text.
- Evaluate self.sql(formatted text START TRANSACTION {mode}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L73) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1034)

<a id="op-039c9a4dcf3a59"></a>
### Database.read only

`operation_foundation_binding_foundation_database_database_database_read_only`

**Inputs** self.

**Wrappers, in declaration order** contextmanager.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Commit or roll back the open transaction before starting a read-only one.”.

**Local steps**

- If self.in\_read\_only\_transaction.
  - yield no value.
  - Return no value.
- If (self.transaction\_writes or len(self.after\_commit) or self.\_disable\_transaction\_control).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.transaction\_writes → len(self.after\_commit) → self.\_disable\_transaction\_control.
  - Call the validation error handler Platform.throw(translated “Commit or roll back the open transaction before starting a read-only one.”, title = translated “Open Transaction”).
- Set self.in\_read\_only\_transaction from true.
- Attempt the following.
  - Evaluate self.\_set\_session\_read\_only(true).
  - Evaluate self.rollback().
  - yield no value.
- On exit, including pending return or failure.
  - Set self.in\_read\_only\_transaction from false.
  - Evaluate self.\_set\_session\_read\_only(false).
  - Evaluate self.rollback().

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [set session read only](operations-019.md#op-962df2e1f44164), [rollback](operations-019.md#op-c621cf7be536bc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L655)

<a id="op-962df2e1f44164"></a>
### Database.set session read only

`operation_foundation_binding_foundation_database_database_database_set_session_read_only`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, read\_only.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L656)

<a id="op-618c1b0592a4e5"></a>
### Database.commit

`operation_foundation_database_business_behavior_database_commit`

**Inputs** self, chain (named only, default false).

**Explicit results** self.rollback(chain = chain) · no value.

**Local steps**

- If self.in\_read\_only\_transaction.
  - Return self.rollback(chain = chain).
- If self.\_disable\_transaction\_control.
  - Evaluate warnings.warn(message = TRANSACTION\_DISABLED\_MSG, stacklevel = 2).
  - Return no value.
- Evaluate self.before\_rollback.reset().
- Evaluate self.after\_rollback.reset().
- Evaluate self.before\_commit.run().
- If chain.
  - Evaluate self.sql(“commit and chain”).
- Otherwise.
  - Evaluate self.sql(“commit”).
  - Evaluate self.begin().
- Evaluate self.value\_cache.clear().
- Evaluate self.after\_commit.run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [rollback](operations-019.md#op-c621cf7be536bc), [sql](operations-017.md#op-eb3702e2fa04e7), [begin](operations-019.md#op-572c679dd95d6b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L75) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1043)

<a id="op-c621cf7be536bc"></a>
### Database.rollback

`operation_foundation_database_business_behavior_database_rollback`

**Inputs** self, save\_point (named only, default no value), chain (named only, default false).

**Local steps**

- If save\_point.
  - Evaluate self.sql(formatted text rollback to savepoint {save\_point}).
  - Evaluate self.value\_cache.clear().
- Otherwise.
  - If not self.\_disable\_transaction\_control.
    - Evaluate self.before\_commit.reset().
    - Evaluate self.after\_commit.reset().
    - Evaluate self.before\_rollback.run().
    - If chain.
      - Evaluate self.sql(“rollback and chain”).
      - Evaluate self.value\_cache.clear().
    - Otherwise.
      - Evaluate self.sql(“rollback”).
      - Evaluate self.begin().
    - Evaluate self.value\_cache.clear().
    - Evaluate self.after\_rollback.run().
  - Otherwise.
    - Evaluate warnings.warn(message = TRANSACTION\_DISABLED\_MSG, stacklevel = 2).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7), [begin](operations-019.md#op-572c679dd95d6b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L439) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1104)

<a id="op-480917d53e565d"></a>
### Database.savepoint

`operation_foundation_database_business_behavior_database_savepoint`

**Inputs** self, save\_point.

**Local steps**

- Evaluate self.sql(formatted text savepoint {save\_point}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L831) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1105)

<a id="op-e5a47d42daf01e"></a>
### Database.release savepoint

`operation_foundation_database_business_behavior_database_release_savepoint`

**Inputs** self, save\_point.

**Local steps**

- Evaluate self.sql(formatted text release savepoint {save\_point}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L910) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1101)

<a id="op-7f9b0ae413d0bd"></a>
### Database.field exists

`operation_foundation_database_business_behavior_database_field_exists`

**Inputs** self, dt, fn.

**Explicit results** self.exists(“DocField”, mapping(“fieldname” → fn, “parent” → dt)).

**Local steps**

- Return self.exists(“DocField”, mapping(“fieldname” → fn, “parent” → dt)).

**Methods declared on this owner** [exists](operations-019.md#op-fa83a01978f7fd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L989) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1059)

<a id="op-9bc570a059c7a3"></a>
### Database.table exists

`operation_foundation_database_business_behavior_database_table_exists`

**Inputs** self, doctype, cached = true.

**Explicit results** formatted text tab{doctype} belongs to self.get\_tables(cached = cached).

**Local steps**

- Return formatted text tab{doctype} belongs to self.get\_tables(cached = cached).

**Methods declared on this owner** [get tables](operations-019.md#op-58beaa41b500a9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L1101) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1113)

<a id="op-972619bfffc5d2"></a>
### Database.has table

`operation_foundation_database_business_behavior_database_has_table`

**Inputs** self, doctype.

**Explicit results** self.table\_exists(doctype).

**Local steps**

- Return self.table\_exists(doctype).

**Methods declared on this owner** [table exists](operations-019.md#op-9bc570a059c7a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L1209) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1092)

<a id="op-58beaa41b500a9"></a>
### Database.get tables

`operation_foundation_database_business_behavior_database_get_tables`

**Inputs** self, cached = true.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L1272) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1084)

<a id="op-a64e6ee217a51a"></a>
### Database.a row exists

`operation_foundation_database_business_behavior_database_a_row_exists`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_all.

**Explicit results** Platform.get\_all(doctype, limit = 1, order\_by = no value, as\_list = true).

**Local steps**

- Return Platform.get\_all(doctype, limit = 1, order\_by = no value, as\_list = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L1325) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1030)

<a id="op-fa83a01978f7fd"></a>
### Database.exists

`operation_foundation_database_business_behavior_database_exists`

**Inputs** self, dt, dn = no value, cache = false, debug (named only, default false).

**Explicit results** dn · self.get\_value(dt, dn, ignore = true, cache = cache, order\_by = no value, debug = debug).

**Local steps**

- If (dt differs from “DocType” and dt equals dn).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt differs from “DocType” → dt equals dn.
  - Return dn.
- If isinstance(dt, dict).
  - Set dt from dt.copy().
  - Set tuple(dt, dn) from tuple(dt.pop(“doctype”), dt).
- Return self.get\_value(dt, dn, ignore = true, cache = cache, order\_by = no value, debug = debug).

**Methods declared on this owner** [get value](operations-018.md#op-5d85ba3f12ad2b).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L1413) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1056)

<a id="op-989999b6291ef8"></a>
### Database.count

`operation_foundation_database_business_behavior_database_count`

**Inputs** self, dt, filters = no value, debug = false, cache = false, distinct = true.

**Explicit results** self.value\_cache at dt at cache\_key · count.

**Local steps**

- Set cache\_key from “COUNT(\*)”.
- If (cache and not filters and cache\_key belongs to self.value\_cache at dt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cache → not filters → cache\_key belongs to self.value\_cache at dt.
  - Return self.value\_cache at dt at cache\_key.
- Set count from nested operand in the contract.qb.get\_query(table = dt, filters = filters, fields = Count(“\*”), distinct = distinct).run(debug = debug) at 0 at 0.
- If (not filters and cache).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters → cache.
  - Set self.value\_cache at dt at cache\_key from count.
- Return count.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L1711) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1046)

<a id="op-f29c8ad5de9fb9"></a>
### Database.estimate count

`operation_foundation_database_business_behavior_database_estimate_count`

**Inputs** self, table.

**Declared result** int.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L2060) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1053)

<a id="op-b9a021274c65b6"></a>
### Database.estimate count

`operation_foundation_database_business_behavior_database_estimate_count_2`

**Inputs** self, doctype.

**Declared result** int.

**Explicit results** count.

**Local steps**

- Set table from get\_table\_name(doctype).
- Set cache\_key from formatted text estimate\_count::{table}.
- Set count from Platform.cache.get\_value(cache\_key).
- If count is identical to no value.
  - Set count from self.\_estimate\_count(table).
  - Evaluate Platform.cache.set\_value(cache\_key, count, expires\_in\_sec = (60 × 60)).
- Return count.

**Methods declared on this owner** [estimate count](operations-019.md#op-f29c8ad5de9fb9).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L2116) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1054)

<a id="op-1db25ab5d6f184"></a>
### Database.format date

`operation_foundation_database_business_behavior_database_format_date`

**Inputs** date.

**Wrappers, in declaration order** staticmethod.

**Explicit results** getdate(date).strftime(“%Y-%m-%d”).

**Local steps**

- Return getdate(date).strftime(“%Y-%m-%d”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L2359) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1060)

<a id="op-0cb948606c56d1"></a>
### Database.format datetime

`operation_foundation_database_business_behavior_database_format_datetime`

**Inputs** datetime.

**Wrappers, in declaration order** staticmethod.

**Explicit results** FallBackDateTimeStr · get\_datetime(datetime).strftime(“%Y-%m-%d %H:%M:%S.%f”).

**Local steps**

- If not datetime.
  - Return FallBackDateTimeStr.
- Return get\_datetime(datetime).strftime(“%Y-%m-%d %H:%M:%S.%f”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L2433) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1061)

<a id="op-b525ac0c37bc1d"></a>
### Database.get creation count

`operation_foundation_database_business_behavior_database_get_creation_count`

**Inputs** self, doctype, minutes.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.creation ≥ (nested operand in the contract − nested operand in the contract)).run() at 0 at 0.

**Local steps**

- Bind dependencies relativedelta.
- Bind dependencies now\_datetime.
- Set dt from Platform.qb.DocType(doctype).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.creation ≥ (nested operand in the contract − nested operand in the contract)).run() at 0 at 0.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L2528) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1065)

<a id="op-b7ff16cdf13339"></a>
### Database.get db table columns

`operation_foundation_database_business_behavior_database_get_database_table_columns`

**Inputs** self, table.

**Declared result** list at str.

**Explicit results** columns.

**Local steps**

- Set key from formatted text table\_columns::{table}.
- Set columns from Platform.client\_cache.get\_value(key).
- If columns is identical to no value.
  - Set information\_schema from Platform.qb.Schema(“information\_schema”).
  - Set columns from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.columns.column\_name).where((nested operand in the contract.columns.table\_name equals table bitwise and n ….
  - If columns.
    - Evaluate Platform.client\_cache.set\_value(key, columns).
- Return columns.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L78) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1067)
