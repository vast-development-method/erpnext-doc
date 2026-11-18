# Record lifecycle and persistence · operations 62

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Meta

<a id="op-f518a7fe820a9b"></a>
### Meta.check if large table

`operation_foundation_model_meta_business_behavior_meta_check_if_large_table`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- Set self.is\_large\_table from false.
- If (self.istable or not Platform.db.table\_exists(self.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.istable → not Platform.db.table\_exists(self.name).
  - Return no value.
- If Platform.db.estimate\_count(self.name) &gt; LARGE\_TABLE\_SIZE\_THRESHOLD.
  - Set recent\_change from Platform.db.sql(formatted text SELECT ′creation′ FROM ′tab{self.name}′ ORDER BY ′creation′ DESC LIMIT 1).
  - If (recent\_change and get\_datetime(recent\_change at 0 at 0) &gt; (datetime.now() + timedelta(days = (negative 1 × LARGE\_TABLE\_RECENCY\_THRESHOLD)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in recent\_change → get\_datetime(recent\_change at 0 at 0) &gt; (datetime.now() + timedelta(days = (negative 1 × LARGE\_TABLE\_RECENCY\_THRESHOLD))).
    - Set self.is\_large\_table from true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L106) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1114)

<a id="op-61e8eb4e8b5b64"></a>
### Meta.fields

`operation_foundation_model_meta_business_behavior_meta_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** mapping of field.fieldname → field for field drawn from self.fields.

**Local steps**

- Return mapping of field.fieldname → field for field drawn from self.fields.
  - Draw field from self.fields.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L1868) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1116)

<a id="op-b857bea7a6ba11"></a>
### Meta.table fields

`operation_foundation_model_meta_business_behavior_meta_table_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** DOCTYPE\_TABLE\_FIELDS · self.get(“fields”, mapping(“fieldtype” → list(“in”, table\_fields))).

**Local steps**

- If self.name equals “DocType”.
  - Return DOCTYPE\_TABLE\_FIELDS.
- Return self.get(“fields”, mapping(“fieldtype” → list(“in”, table\_fields))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L1940) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1167)

<a id="op-3df7fe9cbe291b"></a>
### Meta.non computed table fields

`operation_foundation_model_meta_business_behavior_meta_non_computed_table_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** self.\_table\_fields · self.get(“fields”, mapping(“fieldtype” → list(“in”, table\_fields), “is\_virtual” → 0)).

**Local steps**

- If self.name equals “DocType”.
  - Return self.\_table\_fields.
- Return self.get(“fields”, mapping(“fieldtype” → list(“in”, table\_fields), “is\_virtual” → 0)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L2074) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1161)

<a id="op-03123cfdbc8ff7"></a>
### Meta.table doctypes

`operation_foundation_model_meta_business_behavior_meta_table_record_types`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** mapping of field.fieldname → field.options for field drawn from self.\_table\_fields.

**Local steps**

- Return mapping of field.fieldname → field.options for field drawn from self.\_table\_fields.
  - Draw field from self.\_table\_fields.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L2228) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1168)

<a id="op-91b3bb87564570"></a>
### Meta.non computed table doctypes

`operation_foundation_model_meta_business_behavior_meta_non_computed_table_record_types`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** mapping of field.fieldname → field.options for field drawn from self.\_non\_computed\_table\_fields.

**Local steps**

- Return mapping of field.fieldname → field.options for field drawn from self.\_non\_computed\_table\_fields.
  - Draw field from self.\_non\_computed\_table\_fields.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L2304) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1162)

<a id="op-e086c0ff8396cb"></a>
### Meta.init field caches

`operation_foundation_model_meta_business_behavior_meta_initialize_field_caches`

**Inputs** self.

**Local steps**

- Evaluate self.\_fields.
- Evaluate self.\_table\_fields.
- Evaluate self.\_non\_computed\_table\_fields.
- Evaluate self.\_table\_doctypes.
- Evaluate self.\_non\_computed\_table\_doctypes.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L2380) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1157)

<a id="op-16efbf0e54d8e3"></a>
### Meta.sort fields

`operation_foundation_model_meta_business_behavior_meta_sort_fields`

**Inputs** self.

**State and service calls** call insert on field\_order.

**Explicit results** no value.

**Local steps**

- If field\_order bound to getattr(self, “field\_order”, list()).
  - Set field\_order from list of fieldname for fieldname drawn from json.loads(field\_order) where fieldname belongs to self.\_fields.
    - Draw fieldname from json.loads(field\_order), keep a combination only if (fieldname belongs to self.\_fields).
  - If len(field\_order) equals len(self.fields).
    - Evaluate self.\_update\_fields\_based\_on\_order(field\_order).
    - Return no value.
  - If self.fields at 0.fieldname does not belong to field\_order.
    - Set fields\_to\_prepend from list().
    - Set standard\_field\_found from false.
    - For each tuple(fieldname, field) in self.\_fields.items().
      - If getattr(field, “is\_custom\_field”, false).
        - Leave the innermost loop without its normal-exhaustion alternative.
      - If fieldname belongs to field\_order.
        - Set standard\_field\_found from true.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Evaluate fields\_to\_prepend.append(fieldname).
    - If standard\_field\_found.
      - Set field\_order from (fields\_to\_prepend + field\_order).
    - Otherwise.
      - Set field\_order from fields\_to\_prepend.
- Set existing\_fields from set(field\_order) when field\_order, otherwise false.
  - Value choice on field\_order — true gives set(field\_order), false gives false.
- Set insertion\_map from mapping().
- For each tuple(index, field) in enumerate(self.fields).
  - If (existing\_fields and field.fieldname belongs to existing\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing\_fields → field.fieldname belongs to existing\_fields.
    - Continue with the next iteration or loop test.
  - If not getattr(field, “is\_custom\_field”, false).
    - If existing\_fields.
      - Evaluate insertion\_map.setdefault(self.fields at (index − 1).fieldname, list()).append(field.fieldname).
    - Otherwise.
      - Evaluate field\_order.append(field.fieldname).
  - Otherwise.
    - If target\_position bound to getattr(field, “insert\_after”, no value).
      - Set original\_target from target\_position.
      - If (field.fieldtype belongs to list(“Section Break”, “Column Break”) and target\_position belongs to field\_order).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype belongs to list(“Section Break”, “Column Break”) → target\_position belongs to field\_order.
        - For each current\_field in field\_order at slice (field\_order.index(target\_position) + 1) to no value.
          - If (self.\_fields at current\_field.fieldtype equals “Section Break” or self.\_fields at current\_field.fieldtype equals self.\_fields at original\_target.fieldtype).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_fields at current\_field.fieldtype equals “Section Break” → self.\_fields at current\_field.fieldtype equals self.\_fields at original\_target.fieldtype.
            - Leave the innermost loop without its normal-exhaustion alternative.
          - Set target\_position from current\_field.
      - Otherwise.
        - If (field.fieldtype equals “Tab Break” and target\_position belongs to field\_order).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Tab Break” → target\_position belongs to field\_order.
          - For each current\_field in field\_order at slice (field\_order.index(target\_position) + 1) to no value.
            - If self.\_fields at current\_field.fieldtype equals “Tab Break”.
              - Leave the innermost loop without its normal-exhaustion alternative.
            - Set target\_position from current\_field.
      - Evaluate insertion\_map.setdefault(target\_position, list()).append(field.fieldname).
    - Otherwise.
      - Evaluate field\_order.insert(0, field.fieldname).
- If insertion\_map.
  - Evaluate \_update\_field\_order\_based\_on\_insert\_after(field\_order, insertion\_map).
- Evaluate self.\_update\_fields\_based\_on\_order(field\_order).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update fields based on order](operations-062.md#op-4bddf42766b35e).

**Values supplied outside this operation** selected callable from getattr(self, “field\_order”, list()), getattr(field, “is\_custom\_field”, false) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L2465) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1166)

<a id="op-4bddf42766b35e"></a>
### Meta.update fields based on order

`operation_foundation_model_meta_business_behavior_meta_update_fields_based_on_order`

**Inputs** self, field\_order.

**Local steps**

- Set sorted\_fields from list().
- For each tuple(idx, fieldname) in enumerate(field\_order, 1).
  - Set field from self.\_fields at fieldname.
  - Set field.idx from idx.
  - Evaluate sorted\_fields.append(field).
- Set self.fields from sorted\_fields.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L114) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1169)

<a id="op-caf4fb982100c9"></a>
### Meta.set custom permissions

`operation_foundation_model_meta_business_behavior_meta_set_custom_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L113) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1164)

<a id="op-ca84fbc3fa3111"></a>
### Meta.get fieldnames with value

`operation_foundation_model_meta_business_behavior_meta_get_fieldnames_with_value`

**Inputs** self, with\_field\_meta = false, with\_virtual\_fields = false.

**Explicit results** list of df for df drawn from self.fields where is\_value\_field(df) · list of df.fieldname for df drawn from self.fields where is\_value\_field(df).

**Local steps**

- Bind local operation is\_value\_field for subsequent calls.
- If with\_field\_meta.
  - Return list of df for df drawn from self.fields where is\_value\_field(df).
    - Draw df from self.fields, keep a combination only if (is\_value\_field(df)).
- Return list of df.fieldname for df drawn from self.fields where is\_value\_field(df).
  - Draw df from self.fields, keep a combination only if (is\_value\_field(df)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L4387) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1123)

<a id="op-b51e526f3d8154"></a>
### Meta.get fieldnames with value.is value field

`operation_foundation_model_meta_business_behavior_meta_get_fieldnames_with_value_is_value_field`

**Inputs** df.

**Explicit results** (df.fieldtype does not belong to NO\_VALUE\_FIELDS and (with\_virtual\_fields or not getattr(df, “is\_virtual”, false))).

**Local steps**

- Return (df.fieldtype does not belong to NO\_VALUE\_FIELDS and (with\_virtual\_fields or not getattr(df, “is\_virtual”, false))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to NO\_VALUE\_FIELDS → (with\_virtual\_fields or not getattr(df, “is\_virtual”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in with\_virtual\_fields → not getattr(df, “is\_virtual”, false).

**Values supplied outside this operation** selected callable from getattr(df, “is\_virtual”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L4639) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1124)

<a id="op-35deae97f3eb4a"></a>
### Meta.get fields to check permissions

`operation_foundation_model_meta_business_behavior_meta_get_fields_to_check_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, user\_permission\_doctypes.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L4742) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1125)

<a id="op-b3cfd90710eeb1"></a>
### Meta.get high permlevel fields

`operation_foundation_model_meta_business_behavior_meta_get_high_permission_level_fields`

**Inputs** self.

**Explicit results** self.high\_permlevel\_fields.

**Local steps**

- Return self.high\_permlevel\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L5041) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1128)

<a id="op-0bd07bfce41e9f"></a>
### Meta.high permlevel fields

`operation_foundation_model_meta_business_behavior_meta_high_permission_level_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** list of df for df drawn from self.fields where (df.permlevel or 0) &gt; 0.

**Local steps**

- Return list of df for df drawn from self.fields where (df.permlevel or 0) &gt; 0.
  - Draw df from self.fields, keep a combination only if ((df.permlevel or 0) &gt; 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.permlevel → 0.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L5082) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1155)

<a id="op-a58eafc00cde2c"></a>
### Meta.get permitted fieldnames

`operation_foundation_model_meta_business_behavior_meta_get_permitted_fieldnames`

**Inputs** self, parenttype = no value, user (named only, default no value), permission\_type (named only, default “read”), with\_virtual\_fields (named only, default true).

**Explicit results** permitted\_fieldnames · self.get\_select\_fieldnames(with\_virtual\_fields) · self.get\_fieldnames\_with\_value().

**Local steps**

- Set permitted\_fieldnames from list().
- If (self.istable and not parenttype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.istable → not parenttype.
  - Return permitted\_fieldnames.
- If not permission\_type.
  - Set permission\_type from “select” when Platform.only\_has\_select\_perm(self.name, user = user), otherwise “read”.
    - Value choice on Platform.only\_has\_select\_perm(self.name, user = user) — true gives “select”, false gives “read”.
- If permission\_type equals “select”.
  - Return self.get\_select\_fieldnames(with\_virtual\_fields).
- If not self.get\_permissions(parenttype = parenttype).
  - Return self.get\_fieldnames\_with\_value().
- Set permlevel\_access from set(self.get\_permlevel\_access(permission\_type = permission\_type, parenttype = parenttype, user = user)).
- If (0 does not belong to permlevel\_access and permission\_type belongs to tuple(“read”, “select”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in 0 does not belong to permlevel\_access → permission\_type belongs to tuple(“read”, “select”).
  - Set check\_doctype from parenttype when (self.istable and parenttype), otherwise self.name.
    - Value choice on (self.istable and parenttype) — true gives parenttype, false gives self.name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.istable → parenttype.
  - If Platform.share.get\_shared(check\_doctype, user, rights = list(“read”), limit = 1).
    - Evaluate permlevel\_access.add(0).
- Evaluate permitted\_fieldnames.extend(generator of df.fieldname for df drawn from self.get\_fieldnames\_with\_value(with\_field\_meta = true, with\_virtual\_fields = with\_virtual\_fields) where df.permlevel belongs to perml ….
  - Draw df from self.get\_fieldnames\_with\_value(with\_field\_meta = true, with\_virtual\_fields = with\_virtual\_fields), keep a combination only if (df.permlevel belongs to permlevel\_access).
- Return permitted\_fieldnames.

**Methods declared on this owner** [get select fieldnames](operations-062.md#op-d1d5e8b1c9f381), [get permissions](operations-062.md#op-784501afb18aa6), [get fieldnames with value](operations-062.md#op-ca84fbc3fa3111), [get permlevel access](operations-062.md#op-f464954bf55dd3).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L109) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1140)

<a id="op-d1d5e8b1c9f381"></a>
### Meta.get select fieldnames

`operation_foundation_binding_foundation_model_meta_meta_get_select_fieldnames`

**Inputs** self, with\_virtual\_fields = true.

**Explicit results** fieldnames · list of fieldname for fieldname drawn from fieldnames where fieldname differs from title.fieldname.

**Local steps**

- Set fieldnames from self.get\_search\_fields().
- Set title from self.get\_field(self.title\_field) when (self.show\_title\_field\_in\_link and self.title\_field), otherwise no value.
  - Value choice on (self.show\_title\_field\_in\_link and self.title\_field) — true gives self.get\_field(self.title\_field), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.show\_title\_field\_in\_link → self.title\_field.
- If not title.
  - Return fieldnames.
- If (title.permlevel or (title.is\_virtual and not with\_virtual\_fields)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title.permlevel → (title.is\_virtual and not with\_virtual\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in title.is\_virtual → not with\_virtual\_fields.
  - Return list of fieldname for fieldname drawn from fieldnames where fieldname differs from title.fieldname.
    - Draw fieldname from fieldnames, keep a combination only if (fieldname differs from title.fieldname).
- If title.fieldname does not belong to fieldnames.
  - Evaluate fieldnames.append(title.fieldname).
- Return fieldnames.

**Methods declared on this owner** [get search fields](operations-061.md#op-8796f7f09f3b61), [get field](operations-061.md#op-d0eff0d3504376).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L209) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1641)

<a id="op-f464954bf55dd3"></a>
### Meta.get permlevel access

`operation_foundation_model_meta_business_behavior_meta_get_permission_level_access`

**Inputs** self, permission\_type = “read”, parenttype = no value, user (named only, default no value).

**Explicit results** has\_access\_to.

**Local steps**

- Set has\_access\_to from list().
- Set roles from set(Platform.get\_roles(user)).
- For each perm in self.get\_permissions(parenttype).
  - If (perm.role belongs to roles and perm.get(permission\_type)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.role belongs to roles → perm.get(permission\_type).
    - If perm.permlevel does not belong to has\_access\_to.
      - Evaluate has\_access\_to.append(perm.permlevel).
- Return has\_access\_to.

**Methods declared on this owner** [get permissions](operations-062.md#op-784501afb18aa6).

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L108) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1138)

<a id="op-784501afb18aa6"></a>
### Meta.get permissions

`operation_foundation_model_meta_business_behavior_meta_get_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, parenttype.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L6119) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1139)

<a id="op-b88d92cccb7693"></a>
### Meta.get dashboard data

`operation_foundation_model_meta_business_behavior_meta_get_dashboard_data`

**Inputs** self.

**Explicit results** data.

**Local steps**

- Set data from Platform.\_dict().
- If not self.custom.
  - Attempt the following.
    - Set module from load\_doctype\_module(self.name, suffix = “\_dashboard”).
    - If hasattr(module, “get\_data”).
      - Set data from Platform.\_dict(module.get\_data()).
  - On failure (ImportError).
    - Take no action here.
- Evaluate self.add\_doctype\_links(data).
- If not self.custom.
  - For each hook in Platform.get\_hooks(“override\_doctype\_dashboards”, mapping()).get(self.name, list()).
    - Set data from Platform.\_dict(Platform.get\_attr(hook)(data = data)).
- Return data.

**Methods declared on this owner** [add doctype links](operations-062.md#op-df7379908ce5a0).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“override\_doctype\_dashboards”, mapping()), Platform.get\_attr(hook).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L6263) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1119)

<a id="op-df7379908ce5a0"></a>
### Meta.add doctype links

`operation_foundation_model_meta_business_behavior_meta_add_record_type_links`

**Inputs** self, data.

**Local steps**

- Set dashboard\_links from list().
- If getattr(self, “links”, no value).
  - Evaluate dashboard\_links.extend(self.links).
- If not data.transactions.
  - Set data.transactions from list().
- If not data.non\_standard\_fieldnames.
  - Set data.non\_standard\_fieldnames from mapping().
- If not data.internal\_links.
  - Set data.internal\_links from mapping().
- For each link in dashboard\_links.
  - Set link.added from false.
  - If link.hidden.
    - Continue with the next iteration or loop test.
  - For each group in data.transactions.
    - Set group from Platform.\_dict(group).
    - Set doctype from (link.parent\_doctype or link.link\_doctype).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in link.parent\_doctype → link.link\_doctype.
    - If (link.group and translated group.label equals translated link.group).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.group → translated group.label equals translated link.group.
      - If doctype does not belong to group.get(“items”).
        - Evaluate group.get(“items”).append(doctype).
      - Set link.added from true.
      - If not link.is\_child\_table.
        - If “fieldnames” does not belong to group.
          - Set group at “fieldnames” from mapping().
        - Set group at “fieldnames” at link.link\_doctype from link.link\_fieldname.
  - If not link.added.
    - Set new\_group from dict(label = link.group, items = list((link.parent\_doctype or link.link\_doctype))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in link.parent\_doctype → link.link\_doctype.
    - If not link.is\_child\_table.
      - Set new\_group at “fieldnames” from mapping(link.link\_doctype → link.link\_fieldname).
    - Evaluate data.transactions.append(new\_group).
  - If (not data.fieldname and link.link\_fieldname).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not data.fieldname → link.link\_fieldname.
    - Set data.fieldname from link.link\_fieldname.
  - If not link.is\_child\_table.
    - Set data.non\_standard\_fieldnames at link.link\_doctype from link.link\_fieldname.
  - Otherwise.
    - If link.is\_child\_table.
      - Set data.internal\_links at link.parent\_doctype from list(link.table\_fieldname, link.link\_fieldname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “links”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1111)

<a id="op-8f948c8e38d1ab"></a>
### Meta.get row template

`operation_foundation_model_meta_business_behavior_meta_get_row_template`

**Inputs** self.

**Explicit results** self.get\_web\_template(suffix = “\_row”).

**Local steps**

- Return self.get\_web\_template(suffix = “\_row”).

**Methods declared on this owner** [get web template](operations-062.md#op-9ef3826bcd97c3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L953) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1142)

<a id="op-40a58c048e8c4f"></a>
### Meta.get list template

`operation_foundation_model_meta_business_behavior_meta_get_list_template`

**Inputs** self.

**Explicit results** self.get\_web\_template(suffix = “\_list”).

**Local steps**

- Return self.get\_web\_template(suffix = “\_list”).

**Methods declared on this owner** [get web template](operations-062.md#op-9ef3826bcd97c3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L1015) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1134)

<a id="op-9ef3826bcd97c3"></a>
### Meta.get web template

`operation_foundation_model_meta_business_behavior_meta_get_web_template`

**Inputs** self, suffix = empty text.

**Explicit results** formatted text {module\_name}/doctype/{doctype}/templates/{doctype}{suffix}.html · no value.

**Local steps**

- Set module\_name from Platform.scrub(self.module).
- Set doctype from Platform.scrub(self.name).
- Set template\_path from Platform.get\_module\_path(module\_name, “doctype”, doctype, “templates”, …).
- If os.path.exists(template\_path).
  - Return formatted text {module\_name}/doctype/{doctype}/templates/{doctype}{suffix}.html.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L1077) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1152)
