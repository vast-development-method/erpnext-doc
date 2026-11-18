# Integrations and service calls · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Whatsapp

<a id="op-5a5764f818d138"></a>
### Parse template parameters

`operation_relationships_application_interface_whatsapp_business_behavior_parse_template_parameters`

**Inputs** string, parameters.

**Explicit results** string.

**Local steps**

- For each tuple(i, parameter) in enumerate(parameters, start = 1).
  - Set placeholder from ((“{{” + str(i)) + “}}”).
  - Set string from string.replace(placeholder, str(parameter)).
- Return string.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L3677) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L171) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L152)

<a id="op-3a44dfbdc5f4e6"></a>
### Get from name

`operation_relationships_application_interface_whatsapp_business_behavior_get_from_name`

**Inputs** message.

**Record and data access** resolve a document from message at “reference\_doctype” via get\_doc.

**Explicit results** from\_name.

**Local steps**

- Set doc from Platform.get\_doc(message at “reference\_doctype”, message at “reference\_name”).
- Set from\_name from empty text.
- If message at “reference\_doctype” equals “CRM Deal”.
  - If doc.get(“contacts”).
    - For each c in doc.get(“contacts”).
      - If c.is\_primary.
        - Set from\_name from (c.full\_name or c.mobile\_no).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.full\_name → c.mobile\_no.
        - Leave the innermost loop without its normal-exhaustion alternative.
  - Otherwise.
    - Set from\_name from doc.get(“lead\_name”).
- Otherwise.
  - Set from\_name from one space.join(generator of name for name drawn from list(doc.get(“first\_name”), doc.get(“last\_name”)) where name).
    - Draw name from list(doc.get(“first\_name”), doc.get(“last\_name”)), keep a combination only if (name).
- Return from\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L3853) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L165) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L146)

<a id="op-e697089b3b0b6b"></a>
### Add roles

`operation_relationships_application_interface_whatsapp_business_behavior_add_roles`

**Inputs** no declared parameters.

**Record and data access** read “Custom DocPerm” via exists.

**Explicit results** no value.

**Local steps**

- If “Platform\_whatsapp” does not belong to Platform.get\_installed\_apps().
  - Return no value.
- Set role\_list from list(“Sales Manager”, “Sales User”).
- Set doctypes from list(“WhatsApp Message”, “WhatsApp Templates”, “WhatsApp Settings”).
- For each doctype in doctypes.
  - For each role in role\_list.
    - If Platform.db.exists(“Custom DocPerm”, mapping(“parent” → doctype, “role” → role)).
      - Continue with the next iteration or loop test.
    - Evaluate add\_permission(doctype, role, 0, “write”).
    - Evaluate update\_permission\_property(doctype, role, 0, “create”, …).
    - Evaluate update\_permission\_property(doctype, role, 0, “delete”, …).
    - Evaluate update\_permission\_property(doctype, role, 0, “share”, …).
    - Evaluate update\_permission\_property(doctype, role, 0, “email”, …).
    - Evaluate update\_permission\_property(doctype, role, 0, “print”, …).
    - Evaluate update\_permission\_property(doctype, role, 0, “report”, …).
    - Evaluate update\_permission\_property(doctype, role, 0, “export”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L4250) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L163) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L144)
