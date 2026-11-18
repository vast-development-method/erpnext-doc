# Sales AI

Admionix Solutions describes a sales assistant for version 16 that works with Leads, Opportunities, Quotations, Sales Orders, Sales Invoices, Customers and Items. Sales and accounts staff can ask for a record summary or comparison and draft follow-ups. A System Manager configures providers, models, agents and their permissions. A separate portal agent is documented for customers' own quotations, orders and invoices. The vendor identifies event-driven, five-minute and daily triggers, dry runs, approval pauses, model budgets, background execution and streamed replies. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/sales_ai)

The published workspace shows separate records for sessions, runs, action logs, policies, evaluations, playbooks and triggers. These records distinguish the user's question, execution history, approval policy and automation definitions. The listing also advertises lead and churn scoring, targets, pipeline health, forecasting and daily briefs. Thresholds, training sets and the formulas behind those indicators are unspecified. [Publisher workspace](https://cloud.frappe.io/files/image%20(2)9c94c1.webp)

## Proposed approval and delivery contract

1. A scheduled playbook selects quotations satisfying its configured age and status. Constrain the query to its company and authorized records. Identify a run by the trigger, business record and evaluation window.
2. Create a proposed reminder with recipient, source quotations, contact language, template version and a stable message preview. Record any generated content as a proposal. The approving manager sees exactly what the recipient will receive.
3. Bind approval to the proposal digest. Recheck record access, recipient, quote status and action permission before sending. A changed proposal or newly accepted quotation requires reevaluation. Persist one dispatch outcome and delivery reference per approved operation.
4. The customer portal uses its own tools and identity. A translated question or quoted record name cannot expand the authenticated customer's scope. A model budget stop returns the run status and any unsent proposal.

## Multilingual acceptance

A German-speaking manager starts a dry run for a seven-day-old quotation for an Afrikaans-speaking contact. The interface explains the proposal in German and shows the exact Afrikaans customer message. The dry run sends zero messages. Approve a live proposal once and deliver precisely one reminder, even if the scheduler repeats. If someone edits its Afrikaans text after approval, require approval of the new version. Preserve original customer names, quoted amounts and identifiers across prompts and outputs.

From another customer's portal account, request the quotation in English and Simplified Chinese. In both languages return the same access outcome without disclosing the amount, identity or existence of the record. Log the decision code and masked record context consistently.

**Qualification.** The vendor's linked guide required sign-in at review. Exact provider retention, budget accounting, approval rules, supported languages and evaluation results remain unverified. A model's ability to generate a language does not establish human-reviewed translation coverage. [Linked guide](https://docs.google.com/document/d/1FXJdNhu2s8DzgYr0wxNU6cYbQuv6moSiHQ_nZ_tApPE/edit) · [Named repository](https://github.com/devadmionix/sales_ai)
