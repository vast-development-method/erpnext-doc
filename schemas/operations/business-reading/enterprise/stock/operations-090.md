# Inventory and warehouses · operations 90

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock ledger

<a id="op-a5278f4a553f43"></a>
### Update entries after.initialize reposting

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_initialize_reposting`

**Inputs** self.

**Local steps**

- Set self.\_sles from RepostQueue().
- Set self.pending\_item\_wh from deque(sorted((self.args.get(“pending\_item\_wh”) or list()), key = deferred anonymous expression)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.args.get(“pending\_item\_wh”) → list().
- Set self.\_sle\_batch from mapping().
- Set self.distinct\_sles from set().
- Set self.distinct\_dependant\_item\_wh from set().
- Set self.reposted\_dependant\_item\_wh from mapping().
- Set self.prev\_sle\_dict from Platform.\_dict(mapping()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L767)

<a id="op-435610859d0a07"></a>
### Update entries after.get item wh wise last posted sle

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_item_warehouse_wise_last_posted_stock_ledger_entry`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L3611) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L754)

<a id="op-3a58fcfc448e7b"></a>
### Update entries after.get future entries to repost

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_future_entries_to_repost`

**Inputs** self, item\_wh\_sles.

**Explicit results** sles.

**Local steps**

- Set sles from RepostQueue().
- For each sle in item\_wh\_sles.
  - If tuple(sle.item\_code, sle.warehouse) does not belong to self.distinct\_dependant\_item\_wh.
    - Evaluate self.distinct\_dependant\_item\_wh.add(tuple(sle.item\_code, sle.warehouse)).
  - Evaluate sles.extend(self.get\_future\_entries\_to\_repost(sle)).
- Return sles.

**Methods declared on this owner** [get future entries to repost](operations-090.md#op-5e4eda253c55e5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L750)

<a id="op-593540cd75c01d"></a>
### Update entries after.repost stock ledgers

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_repost_stock_ledgers`

**Inputs** self, item\_wh\_sles = no value.

**Local steps**

- Set self.\_sles from self.\_get\_future\_entries\_to\_repost(item\_wh\_sles).
- Set i from 0.
- While (self.\_sles or self.pending\_item\_wh).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_sles → self.pending\_item\_wh.
  - Evaluate self.start\_pending\_item\_wh().
  - If not self.\_sles.
    - Continue with the next iteration or loop test.
  - Set queued\_sle from self.\_sles.popleft().
  - If tuple(queued\_sle.item\_code, queued\_sle.warehouse) does not belong to self.distinct\_dependant\_item\_wh.
    - Evaluate self.distinct\_dependant\_item\_wh.add(tuple(queued\_sle.item\_code, queued\_sle.warehouse)).
  - If queued\_sle.name belongs to self.distinct\_sles.
    - Continue with the next iteration or loop test.
  - Update i using + 1.
  - Set item\_wh\_key from tuple(queued\_sle.item\_code, queued\_sle.warehouse).
  - If item\_wh\_key does not belong to self.prev\_sle\_dict.
    - Set self.prev\_sle\_dict at item\_wh\_key from get\_previous\_sle\_of\_current\_voucher(queued\_sle).
  - Set sle from self.get\_sle\_to\_repost(queued\_sle).
  - If not sle.
    - Evaluate Platform.logger(“stock\_ledger”).info(formatted text Skipped {queued\_sle.name} while reposting {self.item\_code}, entry is no longer active).
    - Continue with the next iteration or loop test.
  - Evaluate self.repost\_stock\_ledger\_entry(sle).
  - Evaluate self.distinct\_sles.add(sle.name).
  - If sle.dependant\_sle\_voucher\_detail\_no.
    - Evaluate self.include\_dependant\_sle\_in\_reposting(sle).
    - Evaluate self.update\_item\_wh\_wise\_last\_posted\_sle(sle).
  - If (i modulo or format 2000) equals 0.
    - Evaluate self.update\_data\_in\_repost(len(self.\_sles), i).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get future entries to repost](operations-090.md#op-3a58fcfc448e7b), [start pending item wh](operations-090.md#op-8d2529c8ae67ed), [get sle to repost](operations-090.md#op-6ce81ce2e1b7dd), [repost stock ledger entry](operations-090.md#op-a7b2def0efdc16), [include dependant sle in reposting](operations-090.md#op-db8f1fb337d6c4), [update item wh wise last posted sle](operations-090.md#op-384f824f54166c), [update data in repost](operations-090.md#op-eb4dadf43af862).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L775)

<a id="op-8d2529c8ae67ed"></a>
### Update entries after.start pending item wh

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_start_pending_item_wh`

**Inputs** self.

**Local steps**

- Set started from false.
- While (self.pending\_item\_wh and (not self.\_sles or get\_datetime(nested operand in the contract.pending\_item\_wh at 0.posting\_datetime) ≤ get\_datetime(nested operand in the contract.first().posting\_datetime))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pending\_item\_wh → (not self.\_sles or get\_datetime(self.pending\_item\_wh at 0.posting\_datetime) ≤ get\_datetime(nested operand in the contract.\_sles.first().posting\_datetime)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.\_sles → get\_datetime(self.pending\_item\_wh at 0.posting\_datetime) ≤ get\_datetime(self.\_sles.first().posting\_datetime).
  - Set pending from self.pending\_item\_wh.popleft().
  - Set item\_wh\_key from tuple(pending.item\_code, pending.warehouse).
  - If item\_wh\_key belongs to self.distinct\_dependant\_item\_wh.
    - Continue with the next iteration or loop test.
  - Evaluate self.distinct\_dependant\_item\_wh.add(item\_wh\_key).
  - Evaluate self.\_sles.extend(self.get\_future\_entries\_to\_repost(pending)).
  - Set self.item\_wh\_wise\_last\_posted\_sle at item\_wh\_key from pending.
  - Set started from true.
- If started.
  - Set self.\_sle\_batch from mapping().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get future entries to repost](operations-090.md#op-5e4eda253c55e5).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1126)

<a id="op-6ce81ce2e1b7dd"></a>
### Update entries after.get sle to repost

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_sle_to_repost`

**Inputs** self, queued\_sle.

**Explicit results** sle · self.\_sle\_batch.pop(queued\_sle.name, no value).

**Local steps**

- If sle bound to self.\_sle\_batch.pop(queued\_sle.name, no value).
  - Return sle.
- Set names from list(queued\_sle.name).
- For each row in self.\_sles.peek((REPOST\_SLE\_BATCH\_SIZE − 1)).
  - If row.name does not belong to self.distinct\_sles.
    - Evaluate names.append(row.name).
- Set missing from list of name for name drawn from names where name does not belong to self.\_sle\_batch.
  - Draw name from names, keep a combination only if (name does not belong to self.\_sle\_batch).
- Evaluate self.\_sle\_batch.update(mapping of row.name → row for row drawn from get\_sle\_entries\_by\_names(missing)).
  - Draw row from get\_sle\_entries\_by\_names(missing).
- Set self.\_sle\_batch from mapping of name → self.\_sle\_batch at name for name drawn from names where name belongs to self.\_sle\_batch.
  - Draw name from names, keep a combination only if (name belongs to self.\_sle\_batch).
- Return self.\_sle\_batch.pop(queued\_sle.name, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1116)

<a id="op-5c39223d127579"></a>
### Update entries after.sort sles

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_sort_stock_ledger_entries`

**Inputs** self, sles.

**Explicit results** sorted(sles, key = deferred anonymous expression).

**Local steps**

- Return sorted(sles, key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L5062) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L780)

<a id="op-db8f1fb337d6c4"></a>
### Update entries after.include dependant sle in reposting

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_include_dependant_stock_ledger_entry_in_reposting`

**Inputs** self, sle.

**Local steps**

- Set produced\_by\_manufacture from (sle.voucher\_type equals “Stock Entry” and is\_manufacture\_or\_repack\_entry(sle.voucher\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Entry” → is\_manufacture\_or\_repack\_entry(sle.voucher\_no).
- If produced\_by\_manufacture.
  - Set dependant\_sles from self.get\_incoming\_sles\_of\_entry(sle).
- Otherwise.
  - Set dependant\_sles from get\_sle\_by\_voucher\_detail\_no(sle.dependant\_sle\_voucher\_detail\_no).
- For each depend\_sle in dependant\_sles.
  - Set item\_wh\_key from tuple(depend\_sle.item\_code, depend\_sle.warehouse).
  - If item\_wh\_key belongs to self.distinct\_dependant\_item\_wh.
    - Continue with the next iteration or loop test.
  - Evaluate self.distinct\_dependant\_item\_wh.add(item\_wh\_key).
  - Evaluate self.\_sles.extend(self.get\_future\_entries\_to\_repost(depend\_sle)).
  - If produced\_by\_manufacture.
    - Evaluate self.reposted\_dependant\_item\_wh.setdefault(item\_wh\_key, (depend\_sle.posting\_datetime or get\_combine\_datetime(depend\_sle.posting\_date, depend\_sle.posting\_time))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in depend\_sle.posting\_datetime → get\_combine\_datetime(depend\_sle.posting\_date, depend\_sle.posting\_time).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get incoming sles of entry](operations-090.md#op-03df35c97f1c8c), [get future entries to repost](operations-090.md#op-5e4eda253c55e5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L764)

<a id="op-a7b2def0efdc16"></a>
### Update entries after.repost stock ledger entry

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_repost_stock_ledger_entry`

**Inputs** self, sle.

**Local steps**

- If isinstance(sle, dict).
  - Set sle from Platform.\_dict(sle).
- Evaluate self.process\_sle(sle).
- Evaluate self.update\_item\_wh\_wise\_last\_posted\_sle(sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process sle](operations-090.md#op-c79370ebede7c6), [update item wh wise last posted sle](operations-090.md#op-384f824f54166c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L5746) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L774)

<a id="op-384f824f54166c"></a>
### Update entries after.update item wh wise last posted sle

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_item_warehouse_wise_last_posted_stock_ledger_entry`

**Inputs** self, sle.

**Explicit results** no value.

**Local steps**

- If (not self.\_sles and not self.pending\_item\_wh).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.\_sles → not self.pending\_item\_wh.
  - Set self.item\_wh\_wise\_last\_posted\_sle from Platform.\_dict().
  - Return no value.
- Set self.item\_wh\_wise\_last\_posted\_sle at tuple(sle.item\_code, sle.warehouse) from Platform.\_dict(mapping(“item\_code” → sle.item\_code, “warehouse” → sle.warehouse, “posting\_date” → sle.posting\_date, “posting\_time” → sle.posting\_time, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.posting\_datetime → get\_combine\_datetime(sle.posting\_date, sle.posting\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L784)

<a id="op-5c392ed17aa5f6"></a>
### Update entries after.reset vouchers and idx

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_reset_vouchers_and_position`

**Inputs** self.

**Local steps**

- Set self.stock\_ledgers\_to\_repost from list().
- Set self.\_sle\_batch from mapping().
- Set self.prev\_sle\_dict from Platform.\_dict().
- Set self.item\_wh\_wise\_last\_posted\_sle from Platform.\_dict().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L777)

<a id="op-eb4dadf43af862"></a>
### Update entries after.update data in repost

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_data_in_repost`

**Inputs** self, total\_sles = no value, index = no value.

**State and service calls** call db\_set on self.repost\_doc · commit.

**Explicit results** no value.

**Local steps**

- If not self.repost\_doc.
  - Return no value.
- Set values\_to\_update from mapping(“total\_vouchers” → (cint(total\_sles) + cint(index)), “vouchers\_posted” → (index or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in index → 0.
- Evaluate self.repost\_doc.db\_set(values\_to\_update).
- Evaluate update\_args\_in\_repost\_item\_valuation(self.repost\_doc, self.current\_idx, self.items\_to\_be\_repost, self.repost\_affected\_transaction, …).
- If not Platform.in\_test.
  - Evaluate Platform.db.commit().
- Evaluate release\_reposting\_memory().
- Evaluate self.publish\_real\_time\_progress(total\_sles = total\_sles, index = index).

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish real time progress](operations-090.md#op-bf6f2b5e1498a8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L783)

<a id="op-bf6f2b5e1498a8"></a>
### Update entries after.publish real time progress

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_publish_real_time_progress`

**Inputs** self, total\_sles = no value, index = no value.

**State and service calls** publish realtime with “item\_reposting\_progress”.

**Local steps**

- Evaluate Platform.publish\_realtime(“item\_reposting\_progress”, mapping(“name” → self.repost\_doc.name, “total\_vouchers” → (cint(total\_sles) + cint(index)), “vouchers\_posted” → (index or 0)), doctype = self.repost\_doc ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in index → 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“item\_reposting\_progress”, mapping(“name” → self.repost\_doc.name, “total\_vouchers” → (cint(total\_sles) + cint(index)), “vouchers\_posted” → (index or 0)), doctype = self.repost\_doc ….

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L6639) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L771)

<a id="op-5e4eda253c55e5"></a>
### Update entries after.get future entries to repost

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_future_entries_to_repost_2`

**Inputs** self, kwargs.

**Explicit results** get\_stock\_ledger\_entries(kwargs, “&gt;=”, “asc”, check\_serial\_no = false, fields = REPOST\_SLE\_QUEUE\_FIELDS).

**Local steps**

- Return get\_stock\_ledger\_entries(kwargs, “&gt;=”, “asc”, check\_serial\_no = false, fields = REPOST\_SLE\_QUEUE\_FIELDS).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L751)

<a id="op-03df35c97f1c8c"></a>
### Update entries after.get incoming sles of entry

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_get_incoming_sles_of_entry`

**Inputs** self, sle.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** (Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → “Stock Entry”, “voucher\_no” → sle.voucher\_no, “actual\_qty” → tuple(“&gt;”, 0), “is\_cancelled” → 0, …), fields = list(“item\_code”, “wa ….

**Local steps**

- Return (Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → “Stock Entry”, “voucher\_no” → sle.voucher\_no, “actual\_qty” → tuple(“&gt;”, 0), “is\_cancelled” → 0, …), fields = list(“item\_code”, “wa ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → “Stock Entry”, “voucher\_no” → sle.voucher\_no, “actual\_qty” → tuple(“&gt;”, 0), “is\_cancelled” → 0, …), fields = list(“item\_code”, “war … → list().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1111)

<a id="op-56660f772c0aa9"></a>
### Update entries after.has stock reco with serial batch

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_has_stock_reco_with_serial_batch`

**Inputs** self, sle.

**Record and data access** read sle.voucher\_type via get\_value.

**Explicit results** not (sle.batch\_no or sle.serial\_no or sle.serial\_and\_batch\_bundle) · false.

**Local steps**

- If (sle.voucher\_type equals “Stock Reconciliation” and Platform.db.get\_value(sle.voucher\_type, sle.voucher\_no, “set\_posting\_time”) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → Platform.db.get\_value(sle.voucher\_type, sle.voucher\_no, “set\_posting\_time”) equals 1.
  - Return not (sle.batch\_no or sle.serial\_no or sle.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.batch\_no → sle.serial\_no → sle.serial\_and\_batch\_bundle.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L7211) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L763)

<a id="op-31e8ca5a4a1ad3"></a>
### Update entries after.process sle against current timestamp

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_process_stock_ledger_entry_against_current_timestamp`

**Inputs** self.

**Local steps**

- Set sl\_entries from get\_sle\_against\_current\_voucher(self.args).
- If self.args.get(“cancelled”).
  - Evaluate self.seed\_previous\_sle\_for\_cancellation(sl\_entries at 0 when sl\_entries, otherwise self.args).
    - Value choice on sl\_entries — true gives sl\_entries at 0, false gives self.args.
- For each sle in sl\_entries.
  - Set sle at “timestamp” from sle.posting\_datetime.
  - Evaluate self.process\_sle(sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [seed previous sle for cancellation](operations-090.md#op-9671c69c43cd48), [process sle](operations-090.md#op-c79370ebede7c6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L770)

<a id="op-9671c69c43cd48"></a>
### Update entries after.seed previous sle for cancellation

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_seed_previous_stock_ledger_entry_for_cancellation`

**Inputs** self, anchor\_sle.

**Explicit results** no value.

**Local steps**

- Set key from tuple(anchor\_sle.item\_code, anchor\_sle.warehouse).
- If key belongs to self.prev\_sle\_dict.
  - Return no value.
- Set args from Platform.\_dict(anchor\_sle).
- Set args at “sle\_id” from args.get(“name”).
- Set prev\_sle from get\_previous\_sle\_of\_current\_voucher(args).
- If prev\_sle.
  - Set self.prev\_sle\_dict at key from prev\_sle.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L778)

<a id="op-88ab9ec7f04862"></a>
### Update entries after.get future entries to fix

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_future_entries_to_fix`

**Inputs** self.

**Explicit results** list(self.get\_sle\_after\_datetime(args)).

**Local steps**

- Set args from (self.data at self.args.warehouse.previous\_sle or Platform.\_dict(mapping(“item\_code” → self.item\_code, “warehouse” → self.args.warehouse))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.data at self.args.warehouse.previous\_sle → Platform.\_dict(mapping(“item\_code” → self.item\_code, “warehouse” → self.args.warehouse)).
- Return list(self.get\_sle\_after\_datetime(args)).

**Methods declared on this owner** [get sle after datetime](operations-092.md#op-d73225efb22102).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0938.json#L427) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L749)

<a id="op-0e2fec662d0410"></a>
### Update entries after.validate previous sle qty

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_validate_previous_stock_ledger_entry_quantity`

**Inputs** self, sle.

**State and service calls** msgprint with translated text in the contract.format(bold(sle.item\_code), bold(sle.warehouse), bold(format\_date(previous\_sle.posting\_date)), sle.voucher\_no, …).

**Local steps**

- Set previous\_sle from self.prev\_sle\_dict.get(tuple(sle.item\_code, sle.warehouse)).
- If (previous\_sle and previous\_sle.get(“qty\_after\_transaction”) &lt; 0 and sle.get(“actual\_qty”) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_sle → previous\_sle.get(“qty\_after\_transaction”) &lt; 0 → sle.get(“actual\_qty”) &gt; 0.
  - Evaluate Platform.msgprint(translated text in the contract.format(bold(sle.item\_code), bold(sle.warehouse), bold(format\_date(previous\_sle.posting\_date)), sle.voucher\_no, …), title = translated “Warning on Negative  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L795)

<a id="op-c79370ebede7c6"></a>
### Update entries after.process sle

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_process_stock_ledger_entry`

**Inputs** self, sle.

**Record and data access** read “Batch” via get\_value.

**Explicit results** no value.

**Local steps**

- Evaluate self.set\_item\_settings(sle.item\_code).
- Set key from tuple(sle.item\_code, sle.warehouse).
- If key does not belong to self.prev\_sle\_dict.
  - Set prev\_sle from get\_previous\_sle\_of\_current\_voucher(sle).
  - If prev\_sle.
    - Set self.prev\_sle\_dict at key from prev\_sle.
- If not self.prev\_sle\_dict.get(key).
  - Set self.prev\_sle\_dict at key from Platform.\_dict(mapping(“qty\_after\_transaction” → 0.0, “valuation\_rate” → 0.0, “stock\_value” → 0.0, “prev\_stock\_value” → 0.0, …)).
- Set self.wh\_data from self.prev\_sle\_dict.get(key).
- If (self.wh\_data.stock\_queue and isinstance(self.wh\_data.stock\_queue, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.wh\_data.stock\_queue → isinstance(self.wh\_data.stock\_queue, str).
  - Set self.wh\_data.stock\_queue from json.loads(self.wh\_data.stock\_queue).
- If not self.wh\_data.prev\_stock\_value.
  - Set self.wh\_data.prev\_stock\_value from self.wh\_data.stock\_value.
- Evaluate self.validate\_previous\_sle\_qty(sle).
- If ((sle.serial\_no and not self.via\_landed\_cost\_voucher) or not cint(self.allow\_negative\_stock)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sle.serial\_no and not self.via\_landed\_cost\_voucher) → not cint(self.allow\_negative\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.serial\_no → not self.via\_landed\_cost\_voucher.
  - If not self.validate\_negative\_stock(sle).
    - Update self.wh\_data.qty\_after\_transaction using + flt(sle.actual\_qty).
    - Return no value.
- If not self.args.get(“sle\_id”).
  - Evaluate self.get\_dynamic\_incoming\_outgoing\_rate(sle).
- If (self.is\_inward\_transfer\_leg(sle) and not self.has\_bundle\_valuation(sle)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_inward\_transfer\_leg(sle) → not self.has\_bundle\_valuation(sle).
  - Set sle.incoming\_rate from self.get\_incoming\_rate\_from\_outward\_leg(sle).
- If (self.is\_produced\_row(sle) and not self.has\_bundle\_valuation(sle)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_produced\_row(sle) → not self.has\_bundle\_valuation(sle).
  - Set sle.incoming\_rate from self.get\_produced\_row\_rate(sle).
- If (sle.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) and sle.voucher\_detail\_no and is\_internal\_transfer(sle)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) → sle.voucher\_detail\_no → is\_internal\_transfer(sle).
  - Set rate from get\_incoming\_rate\_for\_inter\_company\_transfer(sle).
  - If sle.actual\_qty &lt; 0.
    - Set sle.outgoing\_rate from rate.
  - Otherwise.
    - If rate.
      - Set sle.incoming\_rate from rate.
- Set dimensions from get\_inventory\_dimensions().
- Set has\_dimensions from false.
- If dimensions.
  - For each dimension in dimensions.
    - If sle.get(dimension.get(“fieldname”)).
      - Set has\_dimensions from true.
- If self.has\_bundle\_valuation(sle).
  - Evaluate self.calculate\_valuation\_for\_serial\_batch\_bundle(sle).
- Otherwise.
  - If (sle.serial\_no and not self.skip\_serial\_batch\_valuation and not self.args.get(“sle\_id”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.serial\_no → not self.skip\_serial\_batch\_valuation → not self.args.get(“sle\_id”).
    - Evaluate self.get\_serialized\_values(sle).
    - Update self.wh\_data.qty\_after\_transaction using + flt(sle.actual\_qty).
    - If (sle.voucher\_type equals “Stock Reconciliation” and not sle.batch\_no and has\_correct\_data(sle)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → not sle.batch\_no → has\_correct\_data(sle).
      - Set self.wh\_data.qty\_after\_transaction from sle.qty\_after\_transaction.
    - Set self.wh\_data.stock\_value from (flt(self.wh\_data.qty\_after\_transaction) × flt(self.wh\_data.valuation\_rate)).
  - Otherwise.
    - If (sle.batch\_no and not self.skip\_serial\_batch\_valuation and Platform.db.get\_value(“Batch”, sle.batch\_no, “use\_batchwise\_valuation”, cache = true) and not self.args.get(“sle\_id”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.batch\_no → not self.skip\_serial\_batch\_valuation → Platform.db.get\_value(“Batch”, sle.batch\_no, “use\_batchwise\_valuation”, cache = true) → not self.args.get(“sle\_id”).
      - Evaluate self.update\_batched\_values(sle).
    - Otherwise.
      - If (sle.voucher\_type equals “Stock Reconciliation” and not sle.is\_adjustment\_entry and not sle.batch\_no and not sle.has\_batch\_no and not has\_dimensions).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → not sle.is\_adjustment\_entry → not sle.batch\_no → not sle.has\_batch\_no → not has\_dimensions.
        - Set self.wh\_data.valuation\_rate from sle.valuation\_rate.
        - Set self.wh\_data.qty\_after\_transaction from sle.qty\_after\_transaction.
        - Set self.wh\_data.stock\_value from (flt(self.wh\_data.qty\_after\_transaction) × flt(self.wh\_data.valuation\_rate)).
        - If self.valuation\_method differs from “Moving Average”.
          - Set self.wh\_data.stock\_queue from list(list(self.wh\_data.qty\_after\_transaction, self.wh\_data.valuation\_rate)).
      - Otherwise.
        - If self.valuation\_method equals “Moving Average”.
          - Evaluate self.get\_moving\_average\_values(sle).
          - Update self.wh\_data.qty\_after\_transaction using + flt(sle.actual\_qty).
          - Set self.wh\_data.stock\_value from (flt(self.wh\_data.qty\_after\_transaction) × flt(self.wh\_data.valuation\_rate)).
          - If flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision) differs from 0.
            - Set self.wh\_data.valuation\_rate from (flt(self.wh\_data.stock\_value, self.currency\_precision) ÷ flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision)).
        - Otherwise.
          - Evaluate self.update\_queue\_values(sle).
- Set self.wh\_data.stock\_value from flt(self.wh\_data.stock\_value, self.currency\_precision).
- If not flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision).
  - Set self.wh\_data.stock\_value from 0.0.
- If sle.actual\_qty &lt; 0.
  - Set sle.incoming\_rate from 0.
- Set stock\_value\_difference from (self.wh\_data.stock\_value − self.wh\_data.prev\_stock\_value).
- Set self.wh\_data.prev\_stock\_value from self.wh\_data.stock\_value.
- Set sle.qty\_after\_transaction from flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision).
- Set sle.valuation\_rate from self.wh\_data.valuation\_rate.
- Set sle.stock\_value from self.wh\_data.stock\_value.
- Set sle.stock\_queue from json.dumps(self.wh\_data.stock\_queue).
- Set old\_stock\_value\_difference from sle.stock\_value\_difference.
- Set sle.stock\_value\_difference from stock\_value\_difference.
- If (sle.is\_adjustment\_entry and flt(sle.stock\_value\_difference, self.currency\_precision) equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.is\_adjustment\_entry → flt(sle.stock\_value\_difference, self.currency\_precision) equals 0.
  - Set value\_till\_now from get\_stock\_value\_difference(sle.item\_code, sle.warehouse, sle.posting\_date, sle.posting\_time, voucher\_detail\_no = sle.voucher\_detail\_no, creation = sle.creation).
  - Set sle.stock\_value\_difference from flt((flt(sle.stock\_value) − value\_till\_now), self.currency\_precision).
- Set sle.doctype from “Stock Ledger Entry”.
- Set sle.modified from now().
- Evaluate self.update\_sle\_valuation\_fields(sle).
- Set self.prev\_sle\_dict at key from sle.
- If (not self.args.get(“sle\_id”) or (sle.serial\_and\_batch\_bundle and sle.auto\_created\_serial\_and\_batch\_bundle) or self.is\_outward\_internal\_transfer\_leg(sle)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.args.get(“sle\_id”) → (sle.serial\_and\_batch\_bundle and sle.auto\_created\_serial\_and\_batch\_bundle) → self.is\_outward\_internal\_transfer\_leg(sle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.serial\_and\_batch\_bundle → sle.auto\_created\_serial\_and\_batch\_bundle.
  - Evaluate self.update\_outgoing\_rate\_on\_transaction(sle).
- If flt(old\_stock\_value\_difference, self.currency\_precision) equals flt(sle.stock\_value\_difference, self.currency\_precision).
  - Return no value.
- If not cint(Enterprise.is\_perpetual\_inventory\_enabled(sle.company)).
  - Return no value.
- If (self.args.item\_code differs from sle.item\_code or self.args.warehouse differs from sle.warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.args.item\_code differs from sle.item\_code → self.args.warehouse differs from sle.warehouse.
  - Evaluate self.repost\_affected\_transaction.add(tuple(sle.voucher\_type, sle.voucher\_no)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set item settings](operations-089.md#op-1fa6c84a31bec4), [validate previous sle qty](operations-090.md#op-0e2fec662d0410), [validate negative stock](operations-091.md#op-ee296855de420e), [get dynamic incoming outgoing rate](operations-091.md#op-08efb4406b4dd4), [is inward transfer leg](operations-091.md#op-99e99108f16a17), [has bundle valuation](operations-091.md#op-66c12673ec7e33), [get incoming rate from outward leg](operations-091.md#op-ee95f96a3d18d9), [is produced row](operations-091.md#op-ff4cbc12d2cdef), [get produced row rate](operations-091.md#op-af41d2f32f7a6b), [calculate valuation for serial batch bundle](operations-090.md#op-8c0bae7a52e156), [get serialized values](operations-090.md#op-1b2b031d4970bb), [update batched values](operations-092.md#op-d7b590ac92fe50), [get moving average values](operations-092.md#op-622b9691585cd9), [update queue values](operations-092.md#op-a3554f03c91f3c), [update sle valuation fields](operations-090.md#op-43a07f4762fa53), [is outward internal transfer leg](operations-091.md#op-39744cade41828), [update outgoing rate on transaction](operations-091.md#op-6c550a94b91e06).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L769)

<a id="op-43a07f4762fa53"></a>
### Update entries after.update sle valuation fields

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_update_sle_valuation_fields`

**Inputs** self, sle.

**Local steps**

- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from Platform.qb.update(table).
- For each fieldname in tuple(“incoming\_rate”, “outgoing\_rate”, “valuation\_rate”, “qty\_after\_transaction”, …).
  - Set query from query.set(table at fieldname, sle.get(fieldname)).
- Evaluate query.where((table.name equals sle.name bitwise and table.is\_cancelled equals 0)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1129)

<a id="op-1b2b031d4970bb"></a>
### Update entries after.get serialized values

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_serialized_values`

**Inputs** self, sle.

**Local steps**

- Bind dependencies SerialNoValuation.
- Set incoming\_rate from flt(sle.incoming\_rate).
- Set actual\_qty from flt(sle.actual\_qty).
- If incoming\_rate &lt; 0.
  - Set incoming\_rate from self.wh\_data.valuation\_rate.
- Set stock\_value\_change from 0.
- If actual\_qty &gt; 0.
  - Set stock\_value\_change from (actual\_qty × incoming\_rate).
- Otherwise.
  - If not sle.is\_cancelled.
    - Set new\_sle from copy.deepcopy(sle).
    - Set new\_sle.qty from new\_sle.actual\_qty.
    - Set new\_sle.serial\_nos from get\_serial\_nos\_data(new\_sle.get(“serial\_no”)).
    - Set sn\_obj from SerialNoValuation(sle = new\_sle, warehouse = new\_sle.get(“warehouse”), item\_code = new\_sle.get(“item\_code”)).
    - Set outgoing\_value from sn\_obj.get\_incoming\_rate().
    - Set stock\_value\_change from (actual\_qty × outgoing\_value).
  - Otherwise.
    - Set stock\_value\_change from (actual\_qty × sle.outgoing\_rate).
- Set new\_stock\_qty from (self.wh\_data.qty\_after\_transaction + actual\_qty).
- If new\_stock\_qty &gt; 0.
  - Set new\_stock\_value from ((self.wh\_data.qty\_after\_transaction × self.wh\_data.valuation\_rate) + stock\_value\_change).
  - If new\_stock\_value ≥ 0.
    - Set self.wh\_data.valuation\_rate from (new\_stock\_value ÷ new\_stock\_qty).
- If (self.wh\_data.valuation\_rate is identical to no value and sle.voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.wh\_data.valuation\_rate is identical to no value → sle.voucher\_detail\_no.
  - Set allow\_zero\_rate from self.check\_if\_allow\_zero\_valuation\_rate(sle.voucher\_type, sle.voucher\_detail\_no).
  - If not allow\_zero\_rate.
    - Set self.wh\_data.valuation\_rate from self.get\_fallback\_rate(sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if allow zero valuation rate](operations-092.md#op-bd33fbdbf3b4f2), [get fallback rate](operations-092.md#op-c1ee762e31f9b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0938.json#L4816) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L759)

<a id="op-8c0bae7a52e156"></a>
### Update entries after.calculate valuation for serial batch bundle

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_calculate_valuation_for_serial_batch_bundle`

**Inputs** self, sle.

**Record and data access** read “Serial and Batch Bundle” via exists · read sle.voucher\_type via get\_value · resolve a document from “Serial and Batch Bundle” via get\_doc · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value.

**Local steps**

- If not Platform.db.exists(“Serial and Batch Bundle”, sle.serial\_and\_batch\_bundle).
  - Return no value.
- If (sle.actual\_qty &lt; 0 and (sle.voucher\_type belongs to list(“Stock Reconciliation”, “Asset Capitalization”) or not Platform.db.get\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.actual\_qty &lt; 0 → (sle.voucher\_type belongs to list(“Stock Reconciliation”, “Asset Capitalization”) or not Platform.db.get\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.voucher\_type belongs to list(“Stock Reconciliation”, “Asset Capitalization”) → not Platform.db.get\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”).
  - Set doc from Platform.\_dict(mapping()).
  - Evaluate self.update\_serial\_batch\_no\_valuation(sle, doc, prev\_sle = self.wh\_data).
- Otherwise.
  - Set doc from Platform.get\_doc(“Serial and Batch Bundle”, sle.serial\_and\_batch\_bundle).
  - Evaluate doc.set\_incoming\_rate(save = true, allow\_negative\_stock = self.allow\_negative\_stock, prev\_sle = self.wh\_data).
  - Evaluate doc.calculate\_qty\_and\_amount(save = true).
- If stock\_queue bound to Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → sle.serial\_and\_batch\_bundle, “stock\_queue” → tuple(“is”, “set”)), pluck = “stock\_queue”, order\_by = “idx desc”, limit = 1).
  - Set self.wh\_data.stock\_queue from json.loads(stock\_queue at 0) when stock\_queue, otherwise list().
    - Value choice on stock\_queue — true gives json.loads(stock\_queue at 0), false gives list().
- Set amount from doc.total\_amount.
- If self.is\_inward\_transfer\_leg(sle).
  - Set outward\_value from self.get\_outward\_leg\_value(sle).
  - If outward\_value is distinct from no value.
    - Set amount from outward\_value.
    - Set sle.incoming\_rate from (outward\_value ÷ flt(sle.actual\_qty)).
- If self.is\_produced\_row(sle).
  - Set sle.incoming\_rate from self.get\_produced\_row\_rate(sle).
  - Evaluate self.update\_bundle\_rate(doc, sle.incoming\_rate).
  - Set amount from (sle.incoming\_rate × flt(sle.actual\_qty)).
- Set self.wh\_data.stock\_value from round\_off\_if\_near\_zero((self.wh\_data.stock\_value + amount)).
- Update self.wh\_data.qty\_after\_transaction using + flt(sle.actual\_qty, self.flt\_precision).
- If flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision).
  - Set self.wh\_data.valuation\_rate from (flt(self.wh\_data.stock\_value, self.flt\_precision) ÷ flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update serial batch no valuation](operations-091.md#op-036cb973ba0fad), [is inward transfer leg](operations-091.md#op-99e99108f16a17), [get outward leg value](operations-091.md#op-71dc4eb93aee5d), [is produced row](operations-091.md#op-ff4cbc12d2cdef), [get produced row rate](operations-091.md#op-af41d2f32f7a6b), [update bundle rate](operations-091.md#op-f8f7b80aa14e1d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L745)
