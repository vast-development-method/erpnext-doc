# Organization, approval and localized transactions

Company membership, approval responsibility, fiscal-year scope and master data constrain which operations an actor can perform. The certificate rules below refer to companies using that withholding profile.

## Authorization rule

Logical record `organization.authorization_rule`. [Field definitions and declared grants](../../schema/entities/organization.json)

| Operation | Refuse when |
|---|---|
| Define an approval rule | Neither an approving role nor an approving individual is named. |
| Separate requester and approver | The designated individual subject to the rule is also its designated approving individual. |
| Separate approval roles | The subject role and approving role are identical. |
| Select a basis for a threshold approval | A purchase order, purchase receipt, supplier invoice or stock movement uses average, customer, item or item-group discount as its approval criterion. |
| Set a discount approval threshold | A discount-based rule specifies a value below zero or above 100 percent. |
| Limit a customer’s discount authority | The rule uses a customer-specific discount and no customer is specified. |

## Department

Logical record `organization.department`. [Field definitions and declared grants](../../schema/entities/organization.json)

| Operation | Refuse when |
|---|---|
| Reassign a department | An existing department’s company is changed. |
| Nest a department | The resolved parent department is not a group. |
| Nest a department in a company | The resolved parent has a company different from the child’s company. |

## Employee

Logical record `organization.employee`. [Field definitions and declared grants](../../schema/entities/organization.json)

| Operation | Refuse when |
|---|---|
| Create the employee’s user automatically | No preferred, company or personal email address is available. |
| Create an employee login | The employee already has a linked user. |

## Unit of measure conversion factor

Logical record `organization.unit_of_measure_conversion_factor`. [Field definitions and declared grants](../../schema/entities/organization.json)

| Operation | Refuse when |
|---|---|
| Define a unit conversion | The conversion factor is zero or negative. |
| Define a unit conversion | The source and destination units are the same identity. |

## Vehicle

Logical record `organization.vehicle`. [Field definitions and declared grants](../../schema/entities/organization.json)

| Operation | Refuse when |
|---|---|
| Record vehicle insurance | Both policy dates exist and the coverage start is later than its end. |
| Date a completed vehicle emissions check | The recorded check date is later than the current business date. |

## Lower deduction certificate

Logical record `regional_accounting.lower_deduction_certificate`. [Field definitions and declared grants](../../schema/entities/regional-accounting.json)

| Operation | Refuse when |
|---|---|
| Set a reduced-withholding certificate period | Its last valid date precedes its first valid date. |
| Assign a withholding certificate to a fiscal year | The validity start lies outside the year’s inclusive bounds. |
| Assign a withholding certificate to a fiscal year | The validity end lies outside the year’s inclusive bounds. |
| Set a certificate rate | The percentage is negative or reaches 100. Zero is allowed. |
| Set the certificate monetary ceiling | Its amount is zero or negative. |

## Import supplier invoice

Logical record `regional_accounting.import_supplier_invoice`. [Field definitions and declared grants](../../schema/entities/regional-accounting.json)

| Operation | Refuse when |
|---|---|
| Import a supplier bill | The import contains no supplier bill number. |
| Resolve the supplier’s country during import | The supplied country code does not match a configured country. |
