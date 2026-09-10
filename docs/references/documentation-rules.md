# Documentation rules

This repository must supply the knowledge needed to implement each specified behaviour. A reader must not need research archives, a previous conversation, private identifiers, a particular programming language, or an existing application to understand a rule.

## Scope and terminology

Use comprehensive full names for business concepts, identifiers and machine-readable keys. Avoid acronyms and source product or implementation names. The required navigation filename and machine-readable file extension are repository format conventions; the preserved license is not rewritten. Do not replace a precise concept with a vague generic label simply to avoid an abbreviation.

Distinguish a stored record, the neutral business concept, a derived projection and a proposed replacement policy. Neutral names must remain stable after publication. Before combining similar concepts, compare their fields, lifecycle, calculations, permissions and side effects. An employee, a user identity and a contact remain distinct even when they describe one person.

## Self-contained references

Link to a document, named section, record definition, calculation, operation or acceptance case that is actually present in the repository. Every link must resolve from the file containing it. A structured reference must identify both the catalog path and the entry or structured pointer when the file contains several definitions. Explain the referenced entry's role in the surrounding text.

A reference is navigation, not a substitute for the rule. State the consequential decision where it is used. Put shared detailed algorithms in a canonical linked document rather than duplicating incompatible summaries. The canonical document must define its own inputs and dependencies.

Never require an unavailable file, archive position, source line range, private evidence identifier or digest to discover the implementation rule. A digest can establish byte equality; it cannot tell an implementer what a condition means. When replacing an inaccessible reference, inspect its underlying information and supply the missing explanation, operands, decision order, record effects and examples before removing the reference.

## Behavioural rule template

Each consequential rule needs the following information, either inline or through precise repository-local definitions.

| Element | Required information |
|---|---|
| Purpose and owner | Business objective and the operation that owns the decision |
| Inputs | Authoritative records, selected rows, caller identity, company, effective time and configuration |
| Value interpretation | Units, currency, signs, missing values, defaults, ordering and allowed ranges |
| Preconditions | Required lifecycle, eligibility, permissions, prerequisites and conflicts |
| Decision procedure | Ordered conditions, selection and tie-breaking, calculations, iteration and stopping rules |
| Precision | Stored and displayed precision, rounding policy, tolerance and residual allocation |
| Persisted effects | Created, amended, deleted or reversed records and their linking identities |
| Completion | Synchronous transaction boundary, queued work and what the caller can rely on |
| Failure | Rejection conditions, warnings, partial completion where applicable and retry behaviour |
| Reversal | Cancellation, amendment, historical record retention and dependencies that prevent reversal |
| Acceptance | Concrete inputs, intermediate values, final records, amounts and expected failure cases |

Do not reproduce implementation source code or depend on source-language expressions. Write independent explanations, mathematics, decision tables and neutral data structures. Explain the evaluation semantics of any structured algorithm, including short-circuit conditions, empty collections and null values.

## Mathematics

Define every operand, currency or unit, sign convention, valid range and rounding point. Specify zero-denominator behaviour, negative and return cases, boundary inclusivity and residual allocation. Separate a displayed rounded amount from a stored intermediate when they differ. State whether an example is independently derived or a declared acceptance requirement.

Every numerical fixture must have an exact expected answer and the governing policy. For example, a pack factor of six means one transaction pack represents six base units; a rate per pack is divided by six to obtain the corresponding rate per base unit. A fixture must compare both quantity and value so a double conversion cannot appear correct merely because one total coincides.

Arithmetic checks establish the stated example. They do not establish end-to-end posting, permission enforcement, concurrency behaviour or external settlement.

## Knowledge and verification levels

| Level | Meaning | What it does not establish |
|---|---|---|
| Structural definition | Fields, parameters, choices or relationships are enumerated | All consequential business decisions |
| Specified behaviour | Inputs, decisions, effects and exceptions are explained | Successful execution in a configured system |
| Independently checked example | The stated arithmetic or decision fixture has been checked | Every branch or integration outcome |
| Reference execution | A recorded scenario was run with a fixed reference configuration | Every untested configuration |
| Replacement execution | An independent implementation passed the recorded scenario | Features outside that scenario's boundary |

A function name, comment, test name, generated file or large line count is not proof of semantic completeness. State real unresolved behaviour precisely: the affected operation, missing decision, potential consequence and acceptance case required to settle it. Do not mask a gap with a generic instruction to consult unavailable material. Never invent a rule to make a coverage table look complete.

## Navigation and presentation

The main README explains objectives, the system boundary, compatibility, the directory structure and role-specific reading paths. Every folder has a README that describes its contents and links its documents, catalogs and child folders. Tables should explain what an entry contains rather than label every entry merely as a specification.

Use descriptive headings, readable paragraphs, compact tables and correctly labelled mathematics. Introduce a diagram before relying on it. Define terms before using them. Split a long catalog at semantic boundaries and publish an index listing every partition and how entries are selected; readers must never need to guess a filename. Keep individual structured files below 400,000 bytes.

## Changes and consistency

A calculation change must update its worked cases and dependent financial effects. A state change must update service contracts, screens, permission expectations and acceptance cases. A record change must update relationships and persistence notes. A renamed catalog must update all inbound links, partition indexes and consumer instructions in the same review.

Validate document links and headings, structured references and partitions, data preservation, numerical fixtures, and the absence of inaccessible dependencies. Preserve known warnings until their underlying decision is resolved. Keep research scripts, temporary checkpoints, source archives and external implementation assumptions out of the deliverable.

Retain the repository license unchanged: [Apache License, Version 2.0](../../LICENSE).
