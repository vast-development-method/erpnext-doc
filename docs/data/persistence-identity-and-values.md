# Persistence, identity, and values

This specification defines the common record contract used by the business domains. It separates logical meaning from a particular storage engine. A replacement can choose its physical organization, but records must retain their identity, relationships, value semantics, order, and financial precision. All linked definitions and worked decision procedures are included in this repository.

## Record kinds and ownership

A normal document is a named root record with a declared document type, creator, creation time, last modification time, last modifying user, document state, and ordering index. Its type and identifier form the complete reference. A name is not globally unique across all document types. Business fields extend this common envelope; arbitrary submitted properties do not automatically become persistent columns.

An owned child row has its own identifier and business fields, plus parent identifier, parent document type, parent field, and row position. All three parent-reference components matter: two tables on the same parent may contain the same child record type. Loading one table filters on all three components and orders rows by position. A child table cannot itself own another child table in the base model. Model deeper structures as linked root aggregates or a separately specified hierarchy. Parent creation and modification information is propagated to children during normal saves; document state is propagated as well.

A singleton document has one logical instance per tenant, conventionally identified by its document type. The reviewed implementation stores its values as document-type, field, value records. It supplies default values when the singleton has no persisted values. Saving replaces the singleton's stored field set. Its logical contract is one complete settings object; an implementation need not reproduce that physical layout.

A virtual document has metadata and document operations but provides its own retrieval, creation, update, deletion, listing, counting, and statistics. A virtual document is not evidence of a missing table. The base persistence layer does not independently save its children. Computed fields and computed child tables also have no ordinary stored column or owned-row persistence requirement; their values are recalculated through declared providers. Computed child caches are reset after saves.

The ownership key is therefore the complete parent tuple plus child identity, and the storage provider must select the appropriate record family before saving. The [common storage families](physical-data-catalog.md#common-storage-families) describe the corresponding persistence obligations.

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

Implement field-kind normalization separately from business validation. The [absence and normalization table](#absence-empty-values-and-normalization) specifies the cases where blank text, null, zero, arrays, and masked values differ.

## Identity generation and amendment lineage

Naming executes a before-naming event, then applies type-specific identity policy. A declared integer sequence and a declared time-ordered universally unique identifier are special modes. Otherwise amendment naming and singleton naming are considered, followed by enabled naming rules in descending priority, the document naming behavior, the declared field/prompt/format/series policy, and a generated fallback. The first applicable naming rule that supplies a name wins. A field-based name requires that field's value. A prompted name must be supplied. Format rules can combine literal text, date components, field values, and one advancing number segment.

A number series is scoped by its resolved prefix. Reading its current value takes a write lock; an existing counter advances by one, while an absent counter begins at one. The formatted numeric segment is left-padded to the configured width. Width is formatting, not a maximum lifetime count. Concurrent callers must not obtain the same identity. Do not promise gapless statutory numbering merely because a series exists: deletion, amendment, transaction rollback, and any domain-specific numbering process must be considered separately.

An amendment references a cancelled predecessor. Its naming policy can use the normal naming rules or a predecessor-based suffix; successive amendments advance that suffix. The predecessor remains a separate record. Amendment creation validates predecessor cancellation and copies attachment references into new attachment records. A document identifier and its human-facing title must remain separate when the title can change. Renaming is an explicit identity operation with reference maintenance, not an ordinary edit of a display label.

Identity allocation is a transactional operation with explicit concurrency and amendment rules. An identity change additionally follows the [rename and merge contract](#identity-change-and-merge); changing a label alone does not migrate references.

## References and value validation

A fixed reference resolves the declared target type. A dynamic reference first requires its target-type selector, then resolves the named record in that type. Normal save validates parent and child references. When both the referring aggregate and target are submittable, a cancelled target is rejected except for the amendment-predecessor reference. This is narrower than an unconditional ban on every reference to every cancelled record. Link validation can populate fetched fields from the target; fields marked fetch-only-when-empty preserve an existing value. For a submitted record, fetched-field replacement is limited to fields allowed to change after submission.

Required text is checked for meaningful content. Formatted text containing an image can satisfy required content even without plain text. A required table must contain rows. Child records require parent identity and parent type. Required Boolean fields are treated as having a value even when false. Selection values are stripped and compared with declared options where selection checking applies. Validation also includes data formats, nonnegative and minimum/maximum constraints, length, rating normalization, constant fields, content sanitization, and protected secret persistence. Import invokes its own value preparation and therefore must be specified separately from interactive field validation.

A reference is valid only after its selected type, actual identity, applicable lifecycle state, and fetched-value policy have been evaluated. Permission evaluation remains independent under [identity and permissions](../runtime/identity-permissions-and-tenancy.md).

## Numeric precision resolution

Let a field's rounding precision be the count of decimal places used at a specified calculation boundary. An explicitly configured, truthy field precision takes precedence. For money fields, the tenant currency-precision setting is considered next; a zero or absent setting falls back to the applicable number format's precision. That format is the global number format unless currency-specific formatting is enabled and a currency format exists. Other supported fractional fields use the global fractional precision, falling back to three. The exact truthiness treatment matters: an explicit textual zero may be interpreted differently from an absent numeric setting. Normalize metadata consistently before choosing a precision.

Storage precision, calculation precision, and display precision are distinct. Domain algorithms sometimes round a rate, extended amount, converted amount, tax, or final total at separate points. Rounding every intermediate value to two places or postponing every rounding operation until the final total changes business outcomes. A replacement must preserve the calculation sequence documented in each domain.

The generic numeric coercion helper removes commas from strings, interprets a valid number, treats an absent or unconvertible value as zero, and rounds only when precision is supplied. An unknown rounding policy raises an error rather than silently yielding zero. This helper is not a universal authorization to accept malformed financial input: a caller can perform stricter validation before invoking it. The conversion of `1,500.5` to 1500.5 is a tested behavior; it is not locale-aware interpretation of all punctuation conventions.

For each amount or quantity, record its currency or unit, effective precision, conversion direction, and rounding boundary. The [worked quantity and currency examples](#exact-quantities-and-currency-examples) demonstrate why a universal two-place rounding step is insufficient.

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

The table above defines concrete expected outputs for the three policies. Preserve the selected policy with the test configuration, then verify idempotence, signed half ties, and large values before using the implementation in financial calculations.

## Smallest currency fraction and guarded arithmetic

For a configured smallest fraction \(f\), compute remainder \(r\) at the requested precision. If \(r>f/2\), increase the amount by \(f-r\); otherwise decrease it by \(r\). Equality therefore chooses the lower step under this helper. If no smallest fraction exists, use whole-unit rounding under the configured policy. Finally round to the requested precision. For positive values and fraction 0.05, 1.02 becomes 1.00 and 1.03 becomes 1.05; a precisely represented half remainder chooses the lower step.

For positive fraction \(f\), the remainder uses the divisor's sign: before precision rounding, \(r_0=x-f\lfloor x/f\rfloor\) lies in \([0,f)\), including when amount \(x\) is negative. The calculation scales both operands by \(10^p\) before taking the remainder when precision \(p\ne0\), unscales it, then applies the configured rounding to \(p\) places. Use that rounded remainder for the half-fraction comparison. At fraction 0.05 and precision three, the exact-decimal cases 1.025 and −1.025 become 1.000 and −1.050 respectively; 1.020 and −1.020 become 1.000 and −1.000. Thus exact half ties in this helper are not a sign-symmetric operation. At coarser precision, rounding the remainder can change the comparison, so the requested precision is a required input.

The guarded division helper returns zero when its denominator is zero and otherwise rounds the quotient to the requested precision. Callers that require a nonzero conversion factor must reject zero before using it. A zero result from this helper does not mean that a zero conversion factor is a valid business input.

A zero-denominator helper result is not a valid unit conversion. The consuming command must first reject any zero factor forbidden by its business rules, as explained in the [quantity examples](#exact-quantities-and-currency-examples).

## Acceptance obligations

1. Save a parent with two independently named child tables of the same type; reload each table with only its own ordered rows.
2. Remove one existing child from a submitted aggregate where that table is immutable; reject the change. Perform the permitted equivalent on a draft and delete precisely the omitted stored child.
3. Reject a dynamic reference lacking its target-type selector and reject an unknown target without converting it into an empty valid link.
4. Allocate the same number series concurrently and verify distinct identifiers and correct counter advancement.
5. Recreate each rounding-table outcome, large-value regression, precision-precedence case, and smallest-fraction boundary. Compare persisted amounts as well as displayed totals.
6. Read and save a record through a user who sees a masked secret or field; the placeholder must not replace the stored real value.
7. Create a new amendment only from a cancelled predecessor and retain both records and their lineage.

These are foundation obligations. The domain catalogues must additionally supply every domain-specific uniqueness constraint, conversion factor, rounding boundary, and numeric tolerance; a field inventory alone cannot establish those rules.

## Absence, empty values, and normalization

The operation first resolves effective metadata and its own stricter input rules; persistence normalization then prepares only declared values. Normalization is not a substitute for financial validation.

| Input or field condition | Normal persistence behavior | Required distinction |
| --- | --- | --- |
| Boolean choice containing an integral truthy value | Store one; otherwise zero | False satisfies ordinary Boolean requiredness |
| Integer value needing coercion | Apply integral coercion | A specialized business command can reject malformed input before this stage |
| Fractional numeric value needing coercion | Apply numeric coercion | Absence or invalid numeric text can become zero in this generic helper |
| Empty date, date-time, or time text | Store absence | Do not silently substitute today's date |
| Unique field with blank or whitespace-only text | Store absence | Blank uniqueness differs from uniqueness of meaningful text |
| Nonnullable field still absent after coercion | Use declared nonempty default, otherwise the field-kind nonnull default | This is storage fallback, not a domain-approved financial default |
| Structured field supplied as object or list | Serialize valid structure compactly | A structured array is valid only for a structured or collection field |
| List supplied to an ordinary scalar field | Reject | Do not stringify the list into a plausible scalar |
| Computed field | Evaluate only when requested and permitted; omit from ordinary persistence | Cached evaluation does not become a stored business fact |
| Mask placeholder in a permitted representation | Preserve its display type during serialization; restore the real value for save | Numeric masked fields must not become numeric zero |
| Absent owned collection on initialized new document | Initialize an empty collection | Update overlay omission and explicit collection replacement remain different |

Serialization can explicitly omit null values. That option changes the representation, not the meaning of stored absence. A copied unsaved document can therefore omit a field that a normal read returns as null. Consumers must not infer that every missing field is unknown metadata; it can be withheld by permissions, omitted by serialization, or absent by value.

The generic nonnull fallback is empty text for text-like, reference, date, date-time, and time fields, and zero for numeric and Boolean kinds. Collections do not obtain a meaningful scalar fallback from this helper. A domain requiring a real posting date must still reject an empty date instead of treating the storage fallback as a valid date.

## New-document defaults

For eligible linked fields other than the user-identity link, a default allowed record from user restrictions takes priority. Otherwise an allowed user default is considered. A linked user default is populated only if its target exists. If no user default is selected, a field's static default is considered, except that the title field is excluded from ordinary static default population.

A declared current-user default resolves to the acting principal. A declared current-date default resolves to today's calendar date. A selection without another applicable default uses its first declared option, which can be an intentionally blank option. A referenced-record default resolves a value from the designated parent or default reference, subject to user restrictions; it only fills an unpopulated destination. Current time and current date-time defaults are evaluated for the new document, not frozen in a reusable template. Child construction also receives its parent type, parent identity, and collection identity.

Defaults are initial proposals. The [creation lifecycle](../runtime/document-lifecycle-and-transactions.md#creation-order) still applies permission, link, required-value, state, and business validation. A selected default company cannot override a user restriction on that company. Changing a default tomorrow does not alter a saved invoice today.

## Exact quantities and currency examples

Let \(q\) be commercial quantity, \(c\) stock units per commercial unit, and \(s\) stock quantity. Then \(s=q c\). The inverse \(q=s/c\) requires \(c\ne0\), and a business operation that requires a positive factor must enforce \(c>0\). A pack of six has \(c=6\): five packs produce thirty stock units. A return of one pack is six returned stock units and retains its original row, valuation, and rate context. A size label alone supplies no conversion factor.

Let \(a\) be an amount in transaction currency, \(r\) company-currency units per transaction-currency unit, and \(b\) its company-currency value. The direction is \(b=a r\), followed by the domain's prescribed rounding boundary. If \(a=125.50\) and \(r=18.40\), the unrounded product is 2309.20. An inverse quotation uses \(1/r\); substituting that inverse without changing the formula is incorrect. Taxes, discounts, and rounded totals can add additional separately documented boundaries.

For \(R_p\), the configured rounding operation to \(p\) decimal places, generally \(R_p(x)+R_p(y)\ne R_p(x+y)\). At two places with away-from-zero half rounding, 0.005 and 0.005 round individually to 0.01 and 0.01, whose sum is 0.02; rounding their sum yields 0.01. The operation contract must therefore declare whether rounding occurs at row level, tax level, account-currency conversion, or final total. Mathematical precision does not eliminate the need to preserve those business boundaries.

## Identity change and merge

An ordinary rename changes the root identifier, child parent references, fixed references, matching dynamic references, attachment associations, version references, and protected-secret association. It executes before-rename and after-rename behavior and publishes an identity-change notification after commit. A title change can be a normal document save when the title field is distinct from identity.

A merge is an explicit operation into an existing surviving identity. It reassigns references and assignments, invokes domain merge behavior, records a merge comment, and deletes the old record through its deletion contract. It is not an instruction to concatenate arbitrary financial rows, add unrelated balances, or silently overwrite a coincidentally matching name. Domain validation determines which types can merge and what happens to overlapping business attributes.

Queued rename can return the old identity while work remains pending. A client must observe completion and reload the resulting identity. Distinguish a successfully queued change from a completed reference migration. Concurrent rename, a conflicting destination, a dynamic reference with another selected type, a linked child, and a protected secret all require explicit regression cases.

## Calendar dates and local timestamps

A calendar date, a local date-time, a time of day, and a duration have different semantics. The common current-date-time helper resolves the configured system timezone and returns its local wall-clock date-time without an embedded timezone offset. The replacement must therefore retain the effective timezone context instead of silently interpreting every stored timestamp as universal time. This distinction affects modification timestamps, scheduled eligibility, attendance, service deadlines, and report cut-offs.

Keep fractional seconds where the field and transport support them, particularly for optimistic modification checks. A posting date is a business calendar date and is not obtained by shifting midnight through a user's display timezone. For exchanges requiring unambiguous instants, an adapter may attach the resolved offset or another explicit timezone representation; that mapping must preserve the original local-time business meaning. Time arithmetic must separately state whether it measures wall-clock elapsed time, actual elapsed time, or a working calendar.
