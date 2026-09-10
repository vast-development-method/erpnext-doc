# Recruitment and performance

## Capability and record map

Recruitment starts with requested positions and staffing budgets, publishes openings, retains applicants and referrals, records interview evidence and issues offers. Performance development starts with appraisal cycles and goal definitions, collects self-assessment and reviewer evidence and records resulting scores. Training, skills and grievances are related workforce capabilities with their own records and completion gates. None of these records should silently become a wage, expense or employee record without the corresponding explicit business action.

| Capability | Records and essential relationships |
| --- | --- |
| Hiring demand | Job requisition, requester, company, department, designation, position count, expected compensation, expected date, completion date and duration |
| Staffing budget | Company and date-bounded plan, designation rows, active employee count, vacancies, projected positions and cost per vacancy |
| Advertising and intake | Job opening, requisition and staffing-plan links, publication choices, salary range, application route, close dates; applicant identity, email, opening, source and resume |
| Selection | Interview type, expected skills, scheduled interview, interviewers, individual feedback, skill ratings, result and aggregated rating |
| Offer and employment conversion | Offer terms, applicant, email, company, designation, offer date, response status and later employee or onboarding link |
| Performance | Appraisal cycle, employee, template, result-area weights, hierarchical goals, self ratings, reviewer feedback and final score |
| Development and conduct | Training program and event, participant rows, training results and feedback, employee skills, grievance evidence and resolution |

## Staffing counts and budgets

Each staffing row sets planned positions to current active employees plus vacancies. Active counts include the selected company and its descendants. Current openings count open job-opening records in the same company tree; it is not a sum of every opening's vacancy field. The estimated cost for a row is vacancy count times estimated cost per position when the inspected conditions permit it; total plan budget sums those row costs. With twelve active employees, three vacancies and estimated 40,000 per vacancy, planned positions are fifteen and incremental estimated budget is 120,000. Existing employees do not receive another estimated vacancy cost.

Submitted staffing plans cannot overlap for the same company, designation and intersecting date interval. A subsidiary plan must respect an applicable parent's vacancy and cost ceilings, including allocations already made among related companies. A parent cannot be reduced below its subsidiaries' planned vacancies or cost. Parent-plan lookup can climb the company hierarchy when no local plan is found. These constraints are planning controls, not general-ledger budget entries: publishing a staffing plan itself does not book salary expense.

A job requisition retains states pending, open and approved, rejected, filled, on hold and cancelled. When filled with a completion date, time to fill equals elapsed seconds from posting to completion. The aggregate metric averages filled requisitions, filtered by company, department or designation when selected. Associating an existing opening requires permission to write it and sets its requisition link and vacancy count. Mapping a requisition to a new opening transfers designation and requested positions and prepares company currency and advertised compensation.

## Opening and applicant decisions

An opening can be open or closed, independently of its publication flag. Closing an open record clears the planned closing date and sets an actual closing date if absent; reopening clears actual closure. Date validation uses the applicable closing field. A linked requisition is marked filled with today's completion date when the opening becomes closed. Scheduled expiry closes open advertisements whose planned closing date is before today, rather than at equality. This linkage means a closure for another business reason can still mark the requisition filled in the inspected path; a replacement must decide explicitly whether to preserve that behaviour.

When a staffing plan applies, opening validation compares allowed positions with active employees plus other open opening records. Creating an applicant against a closed opening is rejected. Duplicate applicants for the same email and opening are rejected only when the opening's duplicate-prevention flag is enabled. Otherwise the applicant identity can receive a distinguishing suffix, permitting the same person to apply for another role or reapply. Email validity is checked, and a missing display name may be derived from the address. Applicant states include open, replied, shortlisted, rejected, hold and accepted.

Applicant-to-employee conversion prepares a separate employee record, copies personal email and phone, and fetches company, department and employment type from the opening. It does not mean an application being accepted automatically creates payroll membership. The recruiting record remains linked evidence of origin. Applicant source and resume attachments require access controls independent of publication: advertising a job does not publish its candidates' records.

## Referrals, interviews and offers

A referral requires an active employee referrer and rejects another non-cancelled referral for the same candidate email. It retains candidate contact, designation, resume and bonus eligibility, with a separate bonus-payment status. The inspected validation resets referral status to pending; applicant updates can subsequently set in-process, accepted or rejected state. Re-saving a progressed referral therefore warrants a status-regression conformance case rather than assuming a monotonic state machine. Referrals can prepare job applications and have a separate bonus action; referral acceptance alone is not a booked payroll payment.

An interview validates the applicant's designation and rejects an already submitted interview for that applicant and interview type. Submission requires cleared or rejected result. The expected average rating does not automatically decide the result in the inspected controller. Instead, submission offers a separate action to update the applicant to accepted or rejected. Preserve the difference between computed evidence, human decision and optional applicant update.

Feedback can be submitted only by an interviewer assigned to the interview. A submitted feedback before the scheduled date is rejected. Another submitted feedback from the same interviewer for that interview is rejected until the prior one is cancelled. Average feedback rating equals the sum of the skill ratings divided by the number of assessment rows; unrated rows therefore still affect the denominator. The interview average is the arithmetic mean of submitted feedback averages and is recalculated on both submission and cancellation. Interviewers with different numbers of skill rows have equal weight in that second-stage average.

Before rating-field storage rounding, one interviewer with skill ratings 0.8, 0.6 and zero has a mathematical average of approximately 0.4666667. Another with a single rating of 1.0 has average one. Averaging those unrounded results gives approximately 0.7333333; pooling all skill rows would give 0.6 and is a different algorithm. The actual overall query uses saved feedback values: with two-decimal rating storage, the first average can be stored as 0.47, so the next aggregation starts from 0.47 and 1.00 and yields 0.735 before destination storage rounding. Conformance must check both the calculation stages and the saved scale described in [Persistence identity and values](../data/persistence-identity-and-values.md). A human result may still be rejected despite a high numerical average; preserve result and evidence separately.

A job offer retains awaiting-response, accepted, rejected or cancelled business status and a separate document state. Another non-cancelled offer for the same applicant email is blocked unless its status is rejected or cancelled. When vacancy checking is enabled and a staffing plan applies, submitted offers during its date interval consume vacancy capacity according to the inspected query. An accepted or rejected offer updates the linked applicant to the same status. Preparing an employee from an offer copies contact and employment context but still creates a distinct record. Offer acceptance rate is submitted accepted offers divided by all submitted offers times one hundred, or zero if there are no submitted offers.

## Goals and appraisal mathematics

Goals are hierarchical and belong to one employee, result area and appraisal cycle. A child must match its parent's employee, result area and cycle. Group progress begins at zero and is subsequently the arithmetic mean of its direct, non-archived children. Moving a goal recalculates both the old parent and new parent. Changing a group's result area propagates that area to immediate children. Archived goals do not contribute to the averages. Closed goals remain distinct from archived goals; only archived status is excluded by the inspected averaging query.

Progress over one hundred is rejected. Progress zero maps to pending, exactly one hundred to completed, and lower nonzero values to in progress unless the goal is already archived or closed. The inspected upper-bound check does not reject negative progress; negative-value handling is a known validation boundary requiring an explicit compatibility decision. A replacement must not claim a fully bounded zero-to-one-hundred domain based on this controller alone.

An appraisal is unique for an employee and cycle or overlapping evaluation interval among non-cancelled records. The employee and cycle must be active. Templates populate result areas and self-rating criteria. In goal-derived mode, each result area's completion is the mean of the employee's top-level, non-archived goals in that area and cycle. Multiply that completion percentage by the area weight divided by one hundred, sum across areas and divide by twenty to obtain a five-point goal score. In manual mode, sum each manually supplied goal score times its weight divided by one hundred. Nonzero total weights must equal one hundred at the validated precision.

Self-assessment multiplies the normalised rating by the configured star count and criterion weight divided by one hundred, then sums and rounds to the score field's precision. Peer feedback similarly multiplies normalised ratings by five and by criterion weight. A reviewer cannot be the employee being reviewed, both employees must be active, and feedback must reference that employee's appraisal. Only submitted feedback enters the appraisal's average reviewer score. Cancellation recomputes the average and final result.

The default final score is the arithmetic mean of goal score, average reviewer score and self-assessment score, always divided by three. A missing category contributing zero is not automatically dropped from the denominator. A configured final-score expression is an alternative and receives the documented employee, cycle and appraisal context. For two result areas completed eighty and sixty percent with weights sixty and forty, weighted completion is seventy-two percent and goal score is 3.6. Reviewer score 4.2 and self score 3.9 then yield final score 3.9. With no reviewer score, the same default calculation gives 2.5, not 3.75.

## Training, skills and grievances

Training events hold program, course, provider, location, dates, employees, participation state and certificate choice. End timestamp must be strictly later than start. Updating a submitted event to completed marks present attendees completed unless they already submitted feedback; returning the event to scheduled reopens attendee statuses. Training result submission requires a submitted event and updates matching participant rows to completed. The inspected result controller writes a completion property whose name differs from the event's declared event-state property, so full event-header transition equivalence needs runtime verification. Do not infer this operation creates a supplier invoice or wage expense.

Employee skills and skill maps retain competencies and evaluation evidence alongside training. A grievance retains reporting employee, subject, category, description, the party complained about, responsible person, associated business document and resolution evidence. Only resolved or invalid grievances may be submitted; an open or investigated grievance remains unsubmitted. Resolution is a personnel decision, not an automatic financial adjustment.

## Acceptance criteria and access

Test parent and subsidiary staffing limits; overlapping plans; position counts across company descendants; closed-job application denial; configurable duplicate application prevention; offer duplication by email; vacancy consumption; interview-type duplication; reviewer assignment; future feedback submission; unfilled rating rows; feedback cancellation; optional applicant decision updates; goal ownership and cycle mismatch; archived goal exclusion; weighted score precision; final-score missing categories; reviewer self-feedback denial; and training completion and reopening. The reference metadata grants interviewer feedback submission to the interviewer role while workforce managers can read it. Employee permissions and field-level restrictions are necessary for self-appraisals; a broadly visible employee directory must not imply broadly visible peer feedback or candidate attachments.

No complete interview, appraisal or training runtime was executed here. Rules above are established by inspected decision and calculation routines. The acceptance catalog below records the negative-progress, referral-state and training-header cases explicitly; they remain compatibility decisions requiring transaction-level validation.

## Self-contained contracts and conformance

The [workforce calculations](../../schemas/mathematics/workforce-calculations.json) define named inputs, calculation order, boundary conditions and numerical examples. The [workforce acceptance cases](../../schemas/mathematics/workforce-acceptance-cases.json) define arrangements, actions, expected records, accounting consequences and rejection conditions. These files and the linked record definitions are part of this specification; no external implementation or unavailable evidence identifier is required to interpret a rule. A verification label distinguishes inspected transaction behavior from calculations exercised in isolation.

## Persistent recruiting and development contracts

| Record definitions | Meaning and relationship constraints |
| --- | --- |
| [Staffing plan](../../schemas/data/record-types/staffing_plan.json), [job requisition](../../schemas/data/record-types/job_requisition.json) | Effective company position capacity, vacancy budget and approved demand; distinguish total allowed positions from incremental new-hire cost |
| [Job opening](../../schemas/data/record-types/job_opening.json), [job applicant](../../schemas/data/record-types/job_applicant.json) | Opening status/publication/dates and application identity; applicant contact and resume access remain private |
| [Interview](../../schemas/data/record-types/interview.json), [interview feedback](../../schemas/data/record-types/interview_feedback.json) | Applicant, round/type, schedule, assigned interviewer roster, skill ratings, submitted feedback and independently chosen interview outcome |
| [Job offer](../../schemas/data/record-types/job_offer.json), [employee referral](../../schemas/data/record-types/employee_referral.json) | Offer terms and response; originating application and referral; bonus eligibility and payroll preparation remain separate from acceptance |
| [Goal](../../schemas/data/record-types/goal.json), [appraisal](../../schemas/data/record-types/appraisal.json), [appraisal cycle](../../schemas/data/record-types/appraisal_cycle.json) | Employee-owned goal hierarchy, cycle, result areas, weights, completion, self-ratings, peer-score aggregation and final expression |
| [Training event](../../schemas/data/record-types/training_event.json), [training result](../../schemas/data/record-types/training_result.json) | Scheduled teaching, participants, presence, result and completion evidence |
| [Employee grievance](../../schemas/data/record-types/employee_grievance.json) | Confidential reported issue, parties, investigation, associated business records and resolved/invalid submission decision |

## Selection workflow and capacity example

A staffing row with eight active employees and three vacancies plans eleven positions. At estimated cost 40,000 per vacancy, incremental budget is 120,000. Cost is not eleven times 40,000. Opening-capacity validation and offer-capacity validation are distinct checks with their own date and submitted-state filters; generating an opening does not create an employee.

The operational order is demand approval, capacity check, opening publication, private application intake, interview scheduling, assigned-interviewer feedback, human interview result, offer response and explicit onboarding or employment conversion. The optional action updating an applicant after interview submission must remain optional; numerical feedback alone cannot silently accept an applicant. Likewise, accepted application or offer does not create a submitted salary assignment.

A rejected or cancelled prior offer can stop reserving its email-based duplicate slot according to its business state; an awaiting or accepted non-cancelled offer blocks another. An opening's publication flag and open/closed state must be evaluated separately: an unpublished but open role is not equivalent to a closed one. Scheduled expiry compares planned close strictly before the current date, so an opening dated to close today is not closed by that check until the next day.

## Scoring, hierarchy and cancellation examples

For direct non-archived child goals completed 100, 50 and 0 percent, parent completion is 50 percent. Archiving the zero child changes the parent to 75 percent. Closing that child without archiving keeps it in the calculation. A move between parents recomputes both aggregates; retaining the old parent's average would leave a stale appraisal input.

An appraisal result-area completion of 80 percent at weight 60 and another of 60 percent at weight 40 produces weighted completion 72 and five-point score 3.6. Reviewer score 4.2 and self score 3.9 produce final 3.9. Cancelling the only submitted reviewer feedback resets that category's contribution to zero and produces final 2.5 under the unchanged default expression. It does not change the denominator to two.

Feedback skill rows average per interviewer before interview-wide aggregation. With one reviewer saved at 0.47 and another at 1.00, the aggregate begins from those stored values and yields 0.735 before storage rounding. A replacement must not recalculate the first review from unsaved full precision unless its record contract explicitly changes the outcome. Preserve each score, its rating scale, weights and submitted status.

## Permission and compatibility decisions

Only an assigned interviewer may submit interview feedback for that interview. The scheduled date and duplicate submitted-feedback check both apply. Cancelling feedback removes it from the submitted average; it does not delete the original rating evidence. The peer-review employee must differ from the appraised employee, both must be active, and the linked appraisal must belong to the employee being reviewed. Personnel manager read permission and interviewer submission permission are separate capabilities.

Negative goal progress, referral status reset on save, training-result header completion and opening closure marking requisitions filled are explicit compatibility cases. They are not silently normalized into preferred business behavior. Candidate attachments, peer feedback, grievances and compensation data require record-specific access beyond a public directory or public job advertisement. Concurrent capacity consumption by two offers requires a transaction-level test before claiming the capacity checks prevent all overhiring.
