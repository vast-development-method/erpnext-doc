# Persistence, identity, and values

This specification defines the common record contract used by the business domains. It separates logical meaning from a particular storage engine. A replacement can choose its physical organization, but records must retain their identity, relationships, value semantics, order, and financial precision. References identify the reviewed source artifacts without requiring source-specific names in the implementation vocabulary.

## Record kinds and ownership

A normal document is a named root record with a declared document type, creator, creation time, last modification time, last modifying user, document state, and ordering index. Its type and identifier form the complete reference. A name is not globally unique across all document types. Business fields extend this common envelope; arbitrary submitted properties do not automatically become persistent columns.

An owned child row has its own identifier and business fields, plus parent identifier, parent document type, parent field, and row position. All three parent-reference components matter: two tables on the same parent may contain the same child record type. Loading one table filters on all three components and orders rows by position. A child table cannot itself own another child table in the base model. Model deeper structures as linked root aggregates or a separately specified hierarchy. Parent creation and modification information is propagated to children during normal saves; document state is propagated as well.

A singleton document has one logical instance per tenant, conventionally identified by its document type. The reviewed implementation stores its values as document-type, field, value records. It supplies default values when the singleton has no persisted values. Saving replaces the singleton's stored field set. Its logical contract is one complete settings object; an implementation need not reproduce that physical layout.

A virtual document has metadata and document operations but provides its own retrieval, creation, update, deletion, listing, counting, and statistics. A virtual document is not evidence of a missing table. The base persistence layer does not independently save its children. Computed fields and computed child tables also have no ordinary stored column or owned-row persistence requirement; their values are recalculated through declared providers. Computed child caches are reset after saves.

Evidence: source-artifact-1fd0d520ab1c4b24593c lines 8–96; source-artifact-1c79c95fe9c8ab1bc9d4 lines 812–944; source-artifact-1369c9744914030ba553 lines 10–93; source-artifact-0f25eaf4b484dd77cdbb lines 90–255.

## Field catalogue interpretation

Each field declaration must preserve its full semantic name, label, storage role, value kind, requiredness, default, option set, target type or target-type selector, numeric precision, maximum length, minimum and maximum, nonnegative restriction, field permission level, uniqueness, search indexing, copy policy, allowed change after submission, constant-after-first-save policy, and computed status when declared. Some properties control the form only; a hidden or read-only display flag is not automatically a server permission.

| Logical kind | Required interpretation |
| --- | --- |
| Short text and selection | Text value, optional declared length, with ordered permitted values for a selection |
| Integer and large integer | Integral numeric value; preserve the declared range and source coercion behavior |
| Quantity, money, percentage, duration | Numeric value with separate storage scale and operation-specific rounding precision |
| Date | Calendar date without inventing a time of day |
| Date and time | Timestamp, retaining microsecond-capable precision where present |
| Time | Time value; normalize adapter representations before comparison |
| Boolean choice | False by default where defined; requiredness does not mean it must be true |
| Fixed reference | Target document type from field metadata and target identifier from the record |
| Dynamic reference | Target document type taken from another field, plus target identifier |
| Long text and formatted content | Preserve content and declared sanitization policy; do not impose short-text limits |
| Secret | Stored protected value separated from its masked document representation |
| Structured object | Valid structured value with a declared serialization contract |
| Owned table | Ordered collection of child records, not an ordinary parent scalar column |
| Layout or action control | Presentation or behavior metadata, with no business value column |

The reviewed primary storage mapping uses precision 21 and scale 9 for money, quantity-like fractional values, percentages, and duration: at most twelve digits before and nine after the decimal point. Rating uses precision 3 and scale 2. Default short text and references are 140 characters. These are observed storage defaults, not proof that all domain values use nine decimal places in calculations. Explicit field lengths and supported storage adapters can alter physical details. The catalogue must distinguish adapter-specific facts from logical requirements. The ordinary numeric length validator uses a symmetric absolute-value limit of 2,147,483,647 for a standard integer and 9,223,372,036,854,775,807 for a large integer. It rejects the extra negative endpoint that a signed storage type might otherwise represent. A declared integer length above eleven selects the large-integer validation range. Singleton values bypass this length validator, so these are normal-record validation limits rather than an unconditional limit on every setting.

Evidence: source-artifact-1fd0d520ab1c4b24593c lines 8–96; source-artifact-82fc1279b9f86a256be5 lines 171–223; source-artifact-67374161a6df47b4eb7f lines 88–110; source-artifact-0f25eaf4b484dd77cdbb lines 45–49; source-artifact-0f25eaf4b484dd77cdbb lines 1284–1320.

## Identity generation and amendment lineage

Naming executes a before-naming event, then applies type-specific identity policy. A declared integer sequence and a declared time-ordered universally unique identifier are special modes. Otherwise amendment naming and singleton naming are considered, followed by enabled naming rules in descending priority, the document naming behavior, the declared field/prompt/format/series policy, and a generated fallback. The first applicable naming rule that supplies a name wins. A field-based name requires that field's value. A prompted name must be supplied. Format rules can combine literal text, date components, field values, and one advancing number segment.

A number series is scoped by its resolved prefix. Reading its current value takes a write lock; an existing counter advances by one, while an absent counter begins at one. The formatted numeric segment is left-padded to the configured width. Width is formatting, not a maximum lifetime count. Concurrent callers must not obtain the same identity. Do not promise gapless statutory numbering merely because a series exists: deletion, amendment, transaction rollback, and any domain-specific numbering process must be considered separately.

An amendment references a cancelled predecessor. Its naming policy can use the normal naming rules or a predecessor-based suffix; successive amendments advance that suffix. The predecessor remains a separate record. Amendment creation validates predecessor cancellation and copies attachment references into new attachment records. A document identifier and its human-facing title must remain separate when the title can change. Renaming is an explicit identity operation with reference maintenance, not an ordinary edit of a display label.

Evidence: source-artifact-c869f513562448905114 lines 144–286; source-artifact-c869f513562448905114 lines 289–445; source-artifact-c869f513562448905114 lines 512–592; source-artifact-1c79c95fe9c8ab1bc9d4 lines 812–944.

## References and value validation

A fixed reference resolves the declared target type. A dynamic reference first requires its target-type selector, then resolves the named record in that type. Normal save validates parent and child references. When both the referring aggregate and target are submittable, a cancelled target is rejected except for the amendment-predecessor reference. This is narrower than an unconditional ban on every reference to every cancelled record. Link validation can populate fetched fields from the target; fields marked fetch-only-when-empty preserve an existing value. For a submitted record, fetched-field replacement is limited to fields allowed to change after submission.

Required text is checked for meaningful content. Formatted text containing an image can satisfy required content even without plain text. A required table must contain rows. Child records require parent identity and parent type. Required Boolean fields are treated as having a value even when false. Selection values are stripped and compared with declared options where selection checking applies. Validation also includes data formats, nonnegative and minimum/maximum constraints, length, rating normalization, constant fields, content sanitization, and protected secret persistence. Import invokes its own value preparation and therefore must be specified separately from interactive field validation.

Evidence: source-artifact-0f25eaf4b484dd77cdbb lines 979–1190; source-artifact-1c79c95fe9c8ab1bc9d4 lines 1082–1198.

## Numeric precision resolution

Let a field's rounding precision be the count of decimal places used at a specified calculation boundary. An explicitly configured, truthy field precision takes precedence. For money fields, the tenant currency-precision setting is considered next; a zero or absent setting falls back to the applicable number format's precision. That format is the global number format unless currency-specific formatting is enabled and a currency format exists. Other supported fractional fields use the global fractional precision, falling back to three. The exact truthiness treatment matters: an explicit textual zero may be interpreted differently from an absent numeric setting. Normalize metadata consistently before choosing a precision.

Storage precision, calculation precision, and display precision are distinct. Domain algorithms sometimes round a rate, extended amount, converted amount, tax, or final total at separate points. Rounding every intermediate value to two places or postponing every rounding operation until the final total changes business outcomes. A replacement must preserve the calculation sequence documented in each domain.

The generic numeric coercion helper removes commas from strings, interprets a valid number, treats an absent or unconvertible value as zero, and rounds only when precision is supplied. An unknown rounding policy raises an error rather than silently yielding zero. This helper is not a universal authorization to accept malformed financial input: a caller can perform stricter validation before invoking it. The conversion of `1,500.5` to 1500.5 is a tested behavior; it is not locale-aware interpretation of all punctuation conventions.

Evidence: source-artifact-444b5a1f4b08e77b3ae8 lines 960–985; source-artifact-0f25eaf4b484dd77cdbb lines 1431–1490; source-artifact-91eb5c3685f0ea77eecb lines 1134–1174; source-artifact-d73c03767a0981db604f lines 1710–1800.

## Exact rounding policies

All three actively selectable rounding policies are retained. Their descriptive names below are neutral names for current behaviors, including the configured fallback. An implementation must store which policy applies instead of assuming a universal industry convention.

**Nearest even rounding.** For decimal precision \(p\), scale the magnitude by \(10^p\), stabilize the scaled magnitude to twelve decimal places, and round to the nearest integer, taking exact half ties to the even integer. Restore the original sign and divide by \(10^p\). The source also treats a value sufficiently close to a half as a tie using a magnitude-sensitive tolerance \(2^{\log_2(y)-52}\), but only while that tolerance is below one half. Zero remains zero. The tolerance reflects the source's numeric representation; preserve demonstrated numerical outcomes rather than mechanically introducing the same error into another numeric representation.

**Away-from-zero half rounding.** Round to the nearest multiple of \(10^{-p}\), taking a half tie away from zero. The source compensates for representation error by adding one representable step with the number's sign. When that step reaches one quarter of the rounding interval, it switches to high-precision half-up quantization to avoid inflating large, exactly representable amounts. A replacement with exact decimal arithmetic must still match all boundary examples and large-value cases.

**Scale-sensitive half rounding.** Multiply by \(10^p\) when precision is nonzero, stabilize to eight decimal places, and inspect the fractional part relative to its floor. At zero precision, a half tie goes to the even integer. At nonzero precision, a half tie goes to the floor plus one. Other cases use nearest rounding. Divide by the multiplier. This policy is not sign-symmetric at all half ties. It is still selectable and is the fallback in the reviewed metadata and helper. A test fixture uses nearest-even as its configured default; that does not override the metadata fact.

| Value and decimal places | Nearest even | Away-from-zero half | Scale-sensitive half |
| --- | ---: | ---: | ---: |
| 2.5 at zero | 2 | 3 | 2 |
| −2.5 at zero | −2 | −3 | −2 |
| 1.225 at two | 1.22 | 1.23 | 1.23 |
| −1.225 at two | −1.22 | −1.23 | −1.22 |
| 2.675 at two | 2.68 | 2.68 | 2.68 |

The first two policies must be idempotent at a fixed precision and sign-symmetric over their supported finite inputs. The reviewed tests include 9,750,000 at nine places remaining unchanged and half ties above \(2^{50}\). These cases prevent an apparently reasonable numerical correction from creating money.

Evidence: source-artifact-91eb5c3685f0ea77eecb lines 1253–1392; source-artifact-6e027c5d8c38cd20566f lines 551–557; source-artifact-d73c03767a0981db604f lines 1710–1800.

## Smallest currency fraction and guarded arithmetic

For a configured smallest fraction \(f\), compute remainder \(r\) at the requested precision. If \(r>f/2\), increase the amount by \(f-r\); otherwise decrease it by \(r\). Equality therefore chooses the lower step under this helper. If no smallest fraction exists, use whole-unit rounding under the configured policy. Finally round to the requested precision. For positive values and fraction 0.05, 1.02 becomes 1.00 and 1.03 becomes 1.05; a precisely represented half remainder chooses the lower step. Negative values require the documented remainder convention, not an assumed mirror of positive values.

The guarded division helper returns zero when its denominator is zero and otherwise rounds the quotient to the requested precision. Callers that require a nonzero conversion factor must reject zero before using it. A zero result from this helper does not mean that a zero conversion factor is a valid business input.

Evidence: source-artifact-91eb5c3685f0ea77eecb lines 1253–1392.

## Acceptance obligations

1. Save a parent with two independently named child tables of the same type; reload each table with only its own ordered rows.
2. Remove one existing child from a submitted aggregate where that table is immutable; reject the change. Perform the permitted equivalent on a draft and delete precisely the omitted stored child.
3. Reject a dynamic reference lacking its target-type selector and reject an unknown target without converting it into an empty valid link.
4. Allocate the same number series concurrently and verify distinct identifiers and correct counter advancement.
5. Recreate each rounding-table outcome, large-value regression, precision-precedence case, and smallest-fraction boundary. Compare persisted amounts as well as displayed totals.
6. Read and save a record through a user who sees a masked secret or field; the placeholder must not replace the stored real value.
7. Create a new amendment only from a cancelled predecessor and retain both records and their lineage.

These are foundation obligations. The domain catalogues must additionally supply every domain-specific uniqueness constraint, conversion factor, rounding boundary, and numeric tolerance; a field inventory alone cannot establish those rules.
