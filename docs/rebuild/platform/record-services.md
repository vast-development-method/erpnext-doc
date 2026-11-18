# Requests, documents and policy

The [Requests, documents and policy](../../services/record-services.md) chapter defines the business rules, calculations and worked outcomes.

## Request identity, tenancy and admission

- [Request entry](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/app.py#L189-L239)
- [Transaction control](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/database/database.py#L1227-L1279)
- [Capacity accounting](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/rate_limiter.py#L15-L102)
- [Boundary tests](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/tests/test_rate_limiter.py)

## Record shape and ownership

- [Patch](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/api/v2.py#L173-L216)
- [Save and membership](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/document.py#L797-L925)
- [Revision and state](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/model/document.py#L1355-L1451)

## Read and mutation admission

- [Child permission](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/permissions.py#L823-L918)
- [Permission tests](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/tests/test_permissions.py)
- [Read and list](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/api/v2.py#L66-L163)
- [Method admission](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/api/v2.py#L224-L244)
- [Transport tests](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/tests/test_api_v2.py)

## Transaction lifetime and observations

- [Request result](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/app.py#L110-L180)
- [Request finalization](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/app.py#L438-L453)
- [Database manual](https://docs.frappe.io/framework/user/en/api/database)
