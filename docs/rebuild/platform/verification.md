# Verifying platform decisions

The [contract catalog](contracts.json) models small decision points at the pinned revision. Each contract has a precise scope, a source permalink, an input schema, an outcome vocabulary and ordered rules. All predicates in a rule must hold. Read predicates left to right and stop on a mismatch. Return the outcome of the first matching rule. The final rule has an empty predicate list and covers the remainder. Equality is typed scalar equality. Ordered comparisons operate on nonnegative integers in the units stated in the contract. A right operand has either a literal value or a named input field. Input facts describe the boundary **after** prerequisites in the scope have been evaluated.

The [cases](acceptance.json) contain positive, rejection and equality-boundary observations. To test a replacement, set up the prerequisites, submit the normal operation, observe the durable state and map that observation to the specified outcome. For example, a request racing a timeout requires locking and rereading the stored subscription before deriving its status and time. Calling a lookup table with precomputed facts proves only the decision point. Concurrency, transport admission, permission derivation, database commit and external delivery each need their own observations.

## Reproduce the local checks

The compact verifier below uses a standard interpreter as a convenience. The schemas, rules and cases are the portable contract. Run from this directory. It checks rule evaluation, error vocabulary, default ordering, unique identities, predicate/input references, valid input shapes and complete rule-branch exercise. It exits with an error on a disagreement.

```sh
python3 - <<'PY'
import json
import operator
from pathlib import Path

def load(name):
    return json.loads(Path(name).read_text())

def require(condition, message):
    if not condition:
        raise SystemExit(message)

def valid_scalar(value, schema):
    expected = {"boolean": bool, "integer": int, "string": str}
    return (type(value) is expected[schema["type"]]
            and ("minimum" not in schema or value >= schema["minimum"])
            and ("enum" not in schema or value in schema["enum"]))

ops = {"equal": operator.eq, "less": operator.lt, "atMost": operator.le,
       "greater": operator.gt, "atLeast": operator.ge}
catalog = load("contracts.json")
suite = load("acceptance.json")
require(catalog["revision"] == suite["revision"], "revision mismatch")
contracts = {item["id"]: item for item in catalog["contracts"]}
require(len(contracts) == len(catalog["contracts"]), "duplicate contract")
covered = set()
expected_branches = set()
case_ids = set()
for name, contract in contracts.items():
    fields = contract["inputSchema"]["properties"]
    rules = contract["rules"]
    for i, rule in enumerate(rules):
        expected_branches.add((name, i))
        require(bool(rule["whenAll"]) == (i + 1 < len(rules)), name + ": default ordering")
        require(rule["outcome"] in contract["outcomes"], name + ": undeclared outcome")
        for p in rule["whenAll"]:
            require(p["field"] in fields and p["op"] in ops, name + ": invalid predicate")
            require(("value" in p) != ("otherField" in p), name + ": operand count")
            if "otherField" in p:
                require(p["otherField"] in fields, name + ": invalid field")
                require(fields[p["field"]]["type"] == fields[p["otherField"]]["type"],
                        name + ": operand types")
            else:
                require(valid_scalar(p["value"], fields[p["field"]]), name + ": invalid operand")
for case in suite["cases"]:
    label = case["id"]
    require(label not in case_ids, label + ": duplicate case")
    case_ids.add(label)
    name = case["contract"]
    contract = contracts[name]
    data = case["input"]
    fields = contract["inputSchema"]["properties"]
    require(data.keys() == fields.keys(), label + ": input fields")
    require(all(valid_scalar(data[k], schema) for k, schema in fields.items()), label + ": input type")
    for i, rule in enumerate(contract["rules"]):
        def matches(p):
            right = data[p["otherField"]] if "otherField" in p else p["value"]
            return ops[p["op"]](data[p["field"]], right)
        if all(matches(p) for p in rule["whenAll"]):
            require(rule["outcome"] == case["expected"], label + ": unexpected outcome")
            covered.add((name, i))
            break
require(covered == expected_branches, "unexercised rule branches")
print(f"{len(contracts)} decisions, {len(case_ids)} cases, {len(covered)} rule branches passed")
PY
```

A JSON Schema Draft 2020-12 validator can also check [the catalog](contracts.schema.json) and [the typed suite](acceptance.schema.json). Schema validation checks document structure. An implementation qualification report should separately record reference build, installed applications and configuration, input facts and actor, observed persistence and effects, elapsed time, errors, and any intentional divergence.
