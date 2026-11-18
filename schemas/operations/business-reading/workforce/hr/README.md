# Employment and attendance

Resolve the employee, assignment, effective period, reporting line and applicable workforce settings.

[Business workflow guide](../../../../../docs/people-and-services/workforce-and-employment.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

1,057 bindings across 95 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Appointment letter | 17 | [before insert … get working days](operations-001.md#op-b4c0e9bcfac5b9) |
| Record · Appointment letter template | 4 | [on update … create default template](operations-001.md#op-7f00d5a729ee57) |
| Record · Appraisal | 13 | [validate … set kra evaluation method](operations-001.md#op-edadb4a5a3cb89) · [set appraisal template … get kras for employee](operations-002.md#op-f1bff7b21b1c0e) |
| Record · Appraisal cycle | 15 | [onload … get employees without goals](operations-002.md#op-6fae56077772cc) · [get employees without feedback](operations-003.md#op-02919e20d6db14) |
| Report · Appraisal overview | 4 | [execute … get chart data](operations-003.md#op-9d6ebe81204fed) |
| Record · Appraisal template | 1 | [validate](operations-003.md#op-0a1e48f7a4abaa) |
| Record · Asset request | 10 | [onload … set missing values](operations-003.md#op-de52ce77ade062) |
| Service · Asset request decided | 1 | [get context](operations-003.md#op-10ce67d414af3a) |
| Record · Attendance | 25 | [before insert … validate overlapping shift attendance](operations-003.md#op-4e5e4a2a80b80a) · [get overlapping shift attendance … get data](operations-004.md#op-58c42fcf8ea604) |
| Record · Attendance request | 24 | [validate … get active shifts](operations-004.md#op-587034e906a211) · [get shifts by date … get data](operations-005.md#op-5f1356bfcbb55f) |
| Record · Bank details change request | 7 | [validate … on submit](operations-005.md#op-44dbaac1e1c15e) · [update employee](operations-006.md#op-ec088aacbc1f40) |
| Service · Bank details change request decided | 1 | [get context](operations-006.md#op-5ef142f0425beb) |
| Record · Compensatory leave request | 7 | [validate … create leave allocation](operations-006.md#op-fd3a8d4dffc6ea) |
| Record · Department approver | 2 | [get approvers … validate approver access](operations-006.md#op-81eea584736308) |
| Record · Employee advance | 21 | [validate … update claimed amount](operations-006.md#op-bb51f7ae7ce776) · [set pending amount … get data](operations-007.md#op-8f2f49f5756329) |
| Report · Employee advance summary | 3 | [execute … get advances](operations-007.md#op-040d04910aebf0) |
| Report · Employee analytics | 5 | [execute … get chart data](operations-007.md#op-72e3b043d19690) |
| Record · Employee attendance tool | 12 | [save … get employees](operations-007.md#op-57fb007cedf9e2) · [get unmarked attendance … mark employee attendance](operations-008.md#op-9d67e866f2b9fc) |
| Report · Employee birthday | 4 | [execute … get filtered month](operations-008.md#op-4d13e1e1b15140) |
| Record · Employee checkin | 21 | [before validate … find index in dict](operations-008.md#op-f9d73a5655e294) · [handle attendance exception … calculate time difference](operations-009.md#op-29051a521d1151) |
| Report · Employee exits | 6 | [execute … get report summary](operations-009.md#op-e75ff971c08f9d) |
| Record · Employee grade | 1 | [get data](operations-009.md#op-b44d28c5f0c62f) |
| Record · Employee grievance | 2 | [on submit … on discard](operations-009.md#op-cbc214872da576) |
| Report · Employee hours utilization based on timesheet | 14 | [execute … generate stats by employee](operations-009.md#op-3e1e37252de7bb) · [set employee department and name … generate chart data](operations-010.md#op-5e30789403d073) |
| Report · Employee leave balance | 15 | [execute … get dataset for chart](operations-010.md#op-265af70970c467) |
| Report · Employee leave balance summary | 4 | [execute … get data](operations-010.md#op-c327b000e2fbc5) |
| Record · Employee onboarding | 10 | [validate](operations-010.md#op-5749e75348c761) · [set employee … set missing values](operations-011.md#op-585233c5e91342) |
| Record · Employee onboarding template | 1 | [get data](operations-011.md#op-d0e53fed89aae5) |
| Record · Employee performance feedback | 8 | [validate … set feedback criteria](operations-011.md#op-6d8d695e83e76d) |
| Workspace · Employee profile | 41 | [get profile … get tenure](operations-011.md#op-56b7d413306ad7) · [get birthday … get own upload](operations-012.md#op-4c640f785647e5) · [attach file … get document row](operations-013.md#op-dca0796827ca4d) |
| Record · Employee promotion | 4 | [validate … on cancel](operations-013.md#op-f2aa35d9b631c0) |
| Record · Employee referral | 9 | [validate … get data](operations-013.md#op-4c548ec17da500) |
| Record · Employee separation | 4 | [validate … on cancel](operations-014.md#op-29ae5dbe52f4d5) |
| Record · Employee separation template | 1 | [get data](operations-014.md#op-1ec16ce96ae62c) |
| Record · Employee transfer | 4 | [before submit … validate user in details](operations-014.md#op-a2f95431d95c66) |
| Service · Employees by age | 4 | [get data … get employees by age](operations-014.md#op-26ce3b282959fa) |
| Report · Employees working on a holiday | 3 | [execute … get data](operations-014.md#op-7054950be505cd) |
| Record · Exit interview | 12 | [validate … update interview date in employee](operations-014.md#op-6fe6d29646d975) · [send exit questionnaire … show email summary](operations-015.md#op-ef0a6bdc8a0882) |
| Service · Exit interview scheduled | 1 | [get context](operations-015.md#op-1f1af687a97882) |
| Record · Expense claim | 51 | [onload … get linked projects](operations-015.md#op-0943b657a0597e) · [make gl entries … get expense claim](operations-016.md#op-47869cd80267a5) · [get default payable account … get data](operations-017.md#op-9a37ba116c77de) |
| Record · Expense claim type | 3 | [validate … validate accounts](operations-017.md#op-94177caceffd26) |
| Record · Full and final statement | 27 | [before insert … set totals](operations-017.md#op-bc0e420f0f6bd8) · [add withheld salary slips … cancel loan repayment](operations-018.md#op-25265f89ef1eb3) |
| Record · Goal | 17 | [before insert … update parent progress](operations-018.md#op-632fd48b302295) · [update goal progress in appraisal … add tree node](operations-019.md#op-9eb92afba6215b) |
| Service · Hiring vs attrition count | 2 | [get data … get records](operations-019.md#op-c630ee80bb3df4) |
| Record · Holiday list assignment | 5 | [holiday list start … validate assignment start date](operations-019.md#op-2d2965992cfee6) |
| Record · Hr settings | 7 | [validate … set proceed with frequency change](operations-019.md#op-a81083e478d9ba) |
| Record · Interview | 19 | [validate … validate duplicate interview](operations-019.md#op-e634b2328f1f09) · [validate designation … get events](operations-020.md#op-e95dd9777eb034) |
| Record · Interview feedback | 9 | [validate … update interview average rating](operations-020.md#op-96fb2b4e19fd65) · [get applicable interviewers](operations-021.md#op-2c62b03df86de0) |
| Record · Interview round | 1 | [create interview](operations-021.md#op-a775702c27dcb7) |
| Record · Interview type | 1 | [create interview](operations-021.md#op-aa3b6f34d503b1) |
| Record · Job applicant | 13 | [onload … get data](operations-021.md#op-06f09698e901a6) |
| Service · Job application | 1 | [get context](operations-021.md#op-90eeefbcc3bcf4) |
| Record · Job offer | 33 | [onload … holiday list changed](operations-021.md#op-3bc6398168a8f5) · [validate duplicate job offer … get offer acceptance rate](operations-022.md#op-d32a1914e8aea1) · [get leave allocations … get holiday summary](operations-023.md#op-c8fbd9510b54f1) |
| Record · Job opening | 12 | [autoname … get data](operations-023.md#op-9480f5a39da117) |
| Record · Job opening template | 2 | [create job opening from template … set missing values](operations-023.md#op-e3c0950ba38b1f) |
| Record · Job requisition | 7 | [validate … get avg time to fill](operations-023.md#op-e1a8c632e415ec) |
| Record · Leave adjustment | 13 | [before validate](operations-023.md#op-3094530aa94488) · [before save … get allocated leave types](operations-024.md#op-4654884e569eba) |
| Record · Leave allocation | 31 | [validate … validate lwp](operations-024.md#op-7a8fd4f4b3d929) · [validate allocation overlap … get data](operations-025.md#op-647d4f36d1c67d) |
| Record · Leave application | 73 | [get feed … on submit](operations-025.md#op-cc3b5f92bc87e3) · [before cancel … validate max days](operations-026.md#op-a9125a07799c03) · [get consecutive leave details … get remaining leaves](operations-027.md#op-490fe2cfcfc3dd) · [get remaining leaves … get data](operations-028.md#op-af5ad306d7f7eb) |
| Record · Leave block list | 8 | [validate … get applicable block dates](operations-028.md#op-8313e5b63ad9a4) · [get applicable block lists … get data](operations-029.md#op-e48f9b7224a0a2) |
| Record · Leave control panel | 9 | [validate fields … get filters](operations-029.md#op-d8bf8e8f438139) |
| Record · Leave encashment | 21 | [validate … create additional salary](operations-029.md#op-801e5c86069809) · [set encashed leaves in allocation … create leave encashment](operations-030.md#op-d6da9ebc7942e1) |
| Report · Leave ledger | 4 | [execute … add total row](operations-030.md#op-5c5fe37b38192c) |
| Record · Leave ledger entry | 12 | [validate … expire allocation](operations-030.md#op-45918843d02a41) · [expire carried forward allocation … on doctype update](operations-031.md#op-3dd18566c22b2c) |
| Record · Leave period | 3 | [validate … get data](operations-031.md#op-2339d3c0e175dd) |
| Record · Leave policy | 1 | [validate](operations-031.md#op-29531d1276522f) |
| Record · Leave policy assignment | 23 | [validate … calculate pro rated leaves](operations-031.md#op-26ee58af979ade) · [create assignment for multiple employees … get data](operations-032.md#op-ed95f08eda0701) |
| Record · Leave type | 6 | [validate … get data](operations-032.md#op-6a13527938fca4) |
| Report · Monthly attendance sheet | 24 | [execute … get employee holiday map](operations-032.md#op-07c898ad4a7aba) · [get date range from filters … get chart data](operations-033.md#op-ec546cff7fe45e) |
| Workspace · Organizational chart | 23 | [check access … get employees](operations-033.md#op-bbc305bff15e4a) · [get nodes … is on full leave](operations-034.md#op-f6fc4098f1dcf2) |
| Record · Overtime slip | 21 | [validate … calculate component based hourly rate](operations-034.md#op-20fdbfcce70cc7) · [make salary slip … submit overtime slips for employees](operations-035.md#op-83b092d099411d) |
| Record · Overtime type | 2 | [validate … validate applicable components](operations-035.md#op-a17f349f26a6c5) |
| Report · Project profitability | 7 | [execute … get columns](operations-035.md#op-d285e462c7e4a8) |
| Record · Pwa notification | 4 | [on update … get notification link](operations-035.md#op-e0d75209658bb5) |
| Report · Recruitment analytics | 9 | [execute … get parent row](operations-035.md#op-7972d8278126e3) · [get child row … get job offer](operations-036.md#op-5b6033fb5307cd) |
| Record · Shift assignment | 32 | [validate … is shift start before assignment](operations-036.md#op-a061724746d69d) · [is shift end after assignment … get shift timings](operations-037.md#op-59d423813e3245) |
| Record · Shift assignment tool | 12 | [get employees … create shift schedule assignment](operations-037.md#op-de972dd21f4c91) · [create shift assignment](operations-038.md#op-1a05ce294c177e) |
| Report · Shift attendance | 14 | [execute … update early exit](operations-038.md#op-0c3d19589f03dc) |
| Record · Shift location | 2 | [validate … set geolocation](operations-038.md#op-07f37bd5e1a61a) |
| Record · Shift request | 14 | [validate … on cancel](operations-038.md#op-a8785ec1d2b2ca) · [on discard … get data](operations-039.md#op-5be0ec485831cf) |
| Record · Shift schedule | 2 | [before validate … get or insert shift schedule](operations-039.md#op-1822b5a39048a0) |
| Record · Shift schedule assignment | 6 | [validate … process auto shift creation](operations-039.md#op-d82d528e58f97f) |
| Record · Shift type | 28 | [validate … unlinked checkins exist](operations-039.md#op-30d59120ecccc0) · [process auto attendance … get data](operations-040.md#op-d1ba1cae8d9adf) |
| Record · Staffing plan | 12 | [validate … set number of positions](operations-040.md#op-2e23438c532c98) · [validate overlap … get data](operations-041.md#op-58f880d107cd65) |
| Record · Training event | 6 | [validate … get data](operations-041.md#op-19cd793d9870e8) |
| Record · Training feedback | 3 | [validate … on cancel](operations-041.md#op-12f7bf7332affb) |
| Service · Training feedback | 1 | [get context](operations-041.md#op-d3f00f7285ce40) |
| Record · Training program | 1 | [get data](operations-041.md#op-f4077093d11e98) |
| Record · Training result | 4 | [validate … get employees](operations-041.md#op-0e948f65ad6af6) |
| Service · Training scheduled | 1 | [get context](operations-041.md#op-75465b2808d077) |
| Record · Travel request | 1 | [validate](operations-041.md#op-9a3164235b398f) |
| Report · Unpaid expense claim | 4 | [execute … get unclaimed expese claims](operations-042.md#op-d84281698e700c) |
| Service · Utils | 53 | [set employee name … update previous leave allocation](operations-042.md#op-df98da9b631e1a) · [log allocation error … notify bulk action status](operations-043.md#op-7c2de245597aab) · [set geolocation from coordinates … notify hr](operations-044.md#op-bd202b77c88470) |
| Report · Vehicle expenses | 6 | [execute … get chart data](operations-044.md#op-f00de3584c97fa) |
| Record · Vehicle log | 10 | [validate … get draft expense claim docs](operations-044.md#op-20abe4f0499c45) · [has non vehicle log expenses](operations-045.md#op-72d901b012f2bf) |
