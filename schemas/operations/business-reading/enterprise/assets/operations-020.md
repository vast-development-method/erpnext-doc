# Asset management · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Location

[Record definition](../../../../data/record-types/location.json)

<a id="op-b898d6bc6cd078"></a>
### Location.validate coordinates

`operation_enterprise_binding_enterprise_assets_doctype_location_location_location_validate_coordinates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Latitude must be between -90 and 90” · validation helper — translated “Longitude must be between -180 and 180”.

**Local steps**

- If abs(flt(self.latitude)) &gt; 90.
  - Call the validation error handler Platform.throw(translated “Latitude must be between -90 and 90”).
- If abs(flt(self.longitude)) &gt; 180.
  - Call the validation error handler Platform.throw(translated “Longitude must be between -180 and 180”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L20)

<a id="op-44ff11e16cb4d8"></a>
### Location.calculate location area

`operation_enterprise_assets_record_definitions_location_business_behavior_location_calculate_location_area`

**Inputs** self.

**Local steps**

- Set self.area from compute\_area(self.get\_location\_features()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get location features](operations-020.md#op-005eea26490c92).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L717)

<a id="op-005eea26490c92"></a>
### Location.get location features

`operation_enterprise_assets_record_definitions_location_business_behavior_location_get_location_features`

**Inputs** self.

**Explicit results** list() · features.

**Local steps**

- If not self.location.
  - Return list().
- Set features from json.loads(self.location).get(“features”).
- If not isinstance(features, list).
  - Set features from json.loads(features).
- Return features.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0332.json#L7508) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L718)

<a id="op-f8197026efe6e6"></a>
### Location.set location features

`operation_enterprise_assets_record_definitions_location_business_behavior_location_set_location_features`

**Inputs** self, features.

**State and service calls** call db\_set on self.

**Local steps**

- If not self.location.
  - Set self.location from “{"type":"FeatureCollection","features":&#91;&#93;}”.
- Set location from json.loads(self.location).
- Set location at “features” from features.
- Evaluate self.db\_set(“location”, json.dumps(location)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0332.json#L7678) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L721)

<a id="op-80e46291000c47"></a>
### Location.after rename

`operation_enterprise_binding_enterprise_assets_doctype_location_location_location_after_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**Local steps**

- Evaluate NestedSet.after\_rename(self, old\_name, new\_name, merge).
- Evaluate self.update\_ancestor\_location\_features(old\_names = set(old\_name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update ancestor location features](operations-020.md#op-084ede4fb61d27).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L17)

<a id="op-084ede4fb61d27"></a>
### Location.update ancestor location features

`operation_enterprise_assets_record_definitions_location_business_behavior_location_update_ancestor_location_features`

**Inputs** self, old\_names = no value.

**Explicit results** no value.

**Local steps**

- Set ancestors from self.get\_ancestors().
- Set previous\_ancestors from (set((self.get(“previous\_ancestors”) or list())) − set(ancestors)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“previous\_ancestors”) → list().
- If (not ancestors and not previous\_ancestors).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ancestors → not previous\_ancestors.
  - Return no value.
- Set tuple(subtree, features) from self.get\_subtree\_features().
- For each ancestor in previous\_ancestors.
  - Evaluate set\_features\_in\_ancestor(ancestor, subtree, list()).
- For each ancestor in ancestors.
  - Evaluate set\_features\_in\_ancestor(ancestor, (subtree bitwise or (old\_names or set())), features).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_names → set().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get subtree features](operations-020.md#op-ebc779c07d3e89).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L722)

<a id="op-ebc779c07d3e89"></a>
### Location.get subtree features

`operation_enterprise_binding_enterprise_assets_doctype_location_location_location_get_subtree_features`

**Inputs** self.

**Declared result** tuple at tuple(set at str, list at dict).

**Record and data access** resolve a document from “Location” via get\_doc.

**Explicit results** tuple(subtree, features).

**Local steps**

- Set descendants from get\_descendants\_of(self.doctype, self.name, ignore\_permissions = true).
- Set subtree from set(self.name, expanded descendants).
- Set features from self.get\_own\_features(subtree).
- For each descendant in descendants.
  - Evaluate features.extend(Platform.get\_doc(“Location”, descendant).get\_own\_features(subtree)).
- Return tuple(subtree, features).

**Methods declared on this owner** [get own features](operations-020.md#op-03207202462ddb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L19)

<a id="op-03207202462ddb"></a>
### Location.get own features

`operation_enterprise_binding_enterprise_assets_doctype_location_location_location_get_own_features`

**Inputs** self, subtree.

**Declared result** list at dict.

**Explicit results** features.

**Local steps**

- Set features from list().
- For each feature in self.get\_location\_features().
  - If feature.get(“properties”).get(“feature\_of”) belongs to (subtree − set(self.name)).
    - Continue with the next iteration or loop test.
  - Evaluate feature at “properties”.update(mapping(“child\_feature” → true, “feature\_of” → self.location\_name)).
  - Evaluate features.append(feature).
- Return features.

**Methods declared on this owner** [get location features](operations-020.md#op-005eea26490c92).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L778) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L18)

<a id="op-dbec03e39afefc"></a>
### Set features in ancestor

`operation_enterprise_binding_enterprise_assets_doctype_location_location_set_features_in_ancestor`

**Inputs** ancestor, subtree, features.

**Record and data access** resolve a document from “Location” via get\_doc.

**State and service calls** call db\_set on ancestor\_doc.

**Local steps**

- Set ancestor\_doc from Platform.get\_doc(“Location”, ancestor).
- Set ancestor\_features from list of feature for feature drawn from ancestor\_doc.get\_location\_features() where feature.get(“properties”).get(“feature\_of”) does not belong to subtree.
  - Draw feature from ancestor\_doc.get\_location\_features(), keep a combination only if (feature.get(“properties”).get(“feature\_of”) does not belong to subtree).
- Evaluate ancestor\_features.extend(features).
- Evaluate ancestor\_doc.set\_location\_features(features = ancestor\_features).
- Evaluate ancestor\_doc.db\_set(“area”, compute\_area(ancestor\_features)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L21)

<a id="op-1ec6345cec365a"></a>
### Compute area

`operation_enterprise_assets_record_definitions_location_business_behavior_compute_area`

**Inputs** features.

**Explicit results** layer\_area.

**Local steps**

- Set layer\_area from 0.0.
- For each feature in features.
  - Set feature\_type from feature.get(“geometry”, mapping()).get(“type”).
  - If feature\_type equals “Polygon”.
    - Update layer\_area using + \_polygon\_area(coords = feature.get(“geometry”).get(“coordinates”)).
  - Otherwise.
    - If (feature\_type equals “Point” and feature.get(“properties”).get(“point\_type”) equals “circle”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in feature\_type equals “Point” → feature.get(“properties”).get(“point\_type”) equals “circle”.
      - Update layer\_area using + (math.pi × math.pow(feature.get(“properties”).get(“radius”), 2)).
- Return layer\_area.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L1423) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L715)

<a id="op-84185b4033a7f4"></a>
### Polygon area

`operation_enterprise_assets_record_definitions_location_business_behavior_polygon_area`

**Inputs** coords.

**Explicit results** 0 · area.

**Local steps**

- If not coords.
  - Return 0.
- Set area from abs(\_ring\_area(coords at 0)).
- For each i in range(1, len(coords)).
  - Update area using − abs(\_ring\_area(coords at i)).
- Return area.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L1787) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L725)

<a id="op-27211cb798f10b"></a>
### Ring area

`operation_enterprise_assets_record_definitions_location_business_behavior_ring_area`

**Inputs** coords.

**Explicit results** area.

**Local steps**

- Set area from 0.0.
- Set coords\_length from len(coords).
- If coords\_length &gt; 2.
  - For each i in range(coords\_length).
    - If i equals (coords\_length − 2).
      - Set lower\_index from (coords\_length − 2).
      - Set middle\_index from (coords\_length − 1).
      - Set upper\_index from 0.
    - Otherwise.
      - If i equals (coords\_length − 1).
        - Set lower\_index from (coords\_length − 1).
        - Set middle\_index from 0.
        - Set upper\_index from 1.
      - Otherwise.
        - Set lower\_index from i.
        - Set middle\_index from (i + 1).
        - Set upper\_index from (i + 2).
    - Set p1 from coords at lower\_index.
    - Set p2 from coords at middle\_index.
    - Set p3 from coords at upper\_index.
    - Update area using + ((math.radians(p3 at 0) − math.radians(p1 at 0)) × math.sin(math.radians(p2 at 1))).
  - Set area from (((area × EARTH\_RADIUS) × EARTH\_RADIUS) ÷ 2).
- Return area.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L1979) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L726)

<a id="op-fdc97cbd4013cc"></a>
### Get children

`operation_enterprise_assets_record_definitions_location_business_behavior_get_children`

**Inputs** doctype, parent = no value, location = no value, is\_root = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Location” via get\_list.

**Explicit results** Platform.get\_list(“Location”, filters = filters, fields = list(“name as value”, “is\_group as expandable”)).

**Local steps**

- If (parent is identical to no value or parent equals “All Locations”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent is identical to no value → parent equals “All Locations”.
  - Set parent from empty text.
- Evaluate Platform.has\_permission(“Location”, throw = true).
- Set filters from mapping(“parent\_location” → parent) when parent, otherwise mapping(“parent\_location” → list(“is”, “not set”)).
  - Value choice on parent — true gives mapping(“parent\_location” → parent), false gives mapping(“parent\_location” → list(“is”, “not set”)).
- Return Platform.get\_list(“Location”, filters = filters, fields = list(“name as value”, “is\_group as expandable”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Location”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L716)

<a id="op-b448254378938e"></a>
### Add node

`operation_enterprise_assets_record_definitions_location_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from Platform.form\_dict.
- Set args from make\_tree\_args(expanded names args).
- If args.parent\_location equals “All Locations”.
  - Set args.parent\_location from no value.
- Evaluate Platform.get\_doc(args).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L2828) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L714)

<a id="op-61b259c66b2fbd"></a>
### On doctype update

`operation_enterprise_assets_record_definitions_location_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Location”.

**Local steps**

- Evaluate Platform.db.add\_index(“Location”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L3018) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L724)
