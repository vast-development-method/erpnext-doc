# HR Forms

Brandimic lists HR Forms for major versions 12, 13 and 14. Users build a form template, create a submission for a named employee, supply dynamic values, and produce a print-ready form. The guide names System Manager, HR User and HR Manager as roles that can begin its walkthrough. It does not specify separate permissions for authoring, completing or printing individual employee records. [Marketplace listing and instructions](https://cloud.frappe.io/marketplace/apps/hr_forms)

## What the publisher documents

The template editor accepts a form name and content. The publisher describes sections, fields, title and description as elements of a customer-specific form. The submission links the form template to an Employee and supplies content. The instructions spell the template entry “Form Templete”. Keep that wording as a source lookup alias when mapping legacy data. It is separate from the localized title a staff member sees on a form. The listing shows a print workflow without specifying an approval, signature or payroll posting. [Publisher workflow](https://cloud.frappe.io/marketplace/apps/hr_forms)

## Mission Request example shown by the publisher

The template editor shows rich text and double-brace variables for date, employee, designation and department. On a sample Mission Request submission, the header shows company, employee, date of joining, full name, date of birth, designation and department. Its editable content contains an employee identifier, designation and department where those variables appeared. The date expression is still visible in the draft body even though a date appears in the header. Validate the final rendition separately; a populated header does not prove that every variable was substituted in the document. [Template editor](https://cloud.frappe.io/files/Screenshot%20from%202023-07-11%2015-39-09.webp) · [Submission editor](https://cloud.frappe.io/files/Screenshot%20from%202023-07-11%2015-38-46.webp)

## Proposed rebuild contract

An authorized HR author publishes a versioned template with an organization scope, stable field IDs, required flags and localized captions. A submission records the employee, template revision, rendering language, entered values and creator. Validate all required values before issuing a printable rendition. Freeze the resolved language and content revision on issue; a later template change cannot rewrite an already issued form. Retain the original names and employee-supplied answers, including their script.

Use the employee or recipient's selected language for printed content and the operator's preference for the editor. Human resources can review missing translated wording before issue. If an approved translation is mandatory for the form, keep it in draft until that variant exists or an authorized recipient chooses an approved alternative. For a right-to-left template, render paragraphs, tables and field layout appropriately while isolating identifiers such as `EMP-42` in their own text direction.

| Acceptance example | Expected result |
|---|---|
| An English-speaking HR user issues a German employee form from revision 4; revision 5 later changes a caption. | The saved issue still uses the German revision-4 content, recorded ID values and original employee name. A later issue can use revision 5. |
| An employee's answer includes Chinese text and a newline. An Afrikaans-speaking HR reviewer prints the form. | The stored answer and line boundaries are preserved; the print uses the approved recipient language and renders its glyphs. |
| A user authorized to manage templates requests a completed submission for an employee outside their allowed company. | The request yields no entered values or printable file. Translating the editor cannot expand the employee scope. |

The full substitution vocabulary, historical rendering, downstream approval and the exact permission matrix remain unverified for the linked marketplace build.
