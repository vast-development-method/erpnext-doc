# Durable event automation

The [Durable event automation](../../services/automation.md) chapter defines the business rules, calculations and worked outcomes.

## Stored model and temporal identity

- [Trigger identity and indexing](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation/doctype/automation_trigger_queue/automation_trigger_queue.py#L16-L81)
- [Run and snapshot](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/runner.py#L43-L195)
- [Marker](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/queue.py#L13-L48)

## From a business edit to runnable work

- [Dispatch and coalescing](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/dispatch.py#L23-L184)
- [Claims and stale recovery](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/drainer.py#L225-L337)
- [Defaults](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/settings.py#L9-L59)

## Plan execution and effects

- [Run and identity](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/runner.py#L43-L222)
- [Step boundary](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/runner.py#L361-L400)
- [Finalization](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/runner.py#L507-L576)
- [Group recovery](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/drainer.py#L105-L224)

## Event rendezvous

- [Emission and wait](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/events.py#L16-L82)
- [Subject selection and claim](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/events.py#L156-L228)
- [Reference event tests](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/tests/test_events.py)
- [Recovery tests](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/automation_engine/tests/test_drainer.py)
