# Persona

[Business workflow and acceptance cases](../../../capabilities/guides/workspace.md#delegated-support-sessions).

Omar Mohammed's version 13 listing describes support staff entering another user's session from the User form. Only an Administrator or System Manager can initiate the action. The listing describes two activity entries, identifying the operator's action and the target's login, and excludes a System Manager acting as another System Manager. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/persona)

## Source boundaries

The separately maintained, archived `iptelephony/persona` has the same form action and logging design. Its server-side role check rejects self-impersonation and targets that are Administrator or hold System Manager, even for a privileged caller. On success it records the original operator before changing the effective user and logs the target login. The form decides when to offer the action, while the server enforces the target restrictions. Its maintainer closed the project after a similar feature arrived in the platform. No distribution identity has been established between this archive and the marketplace's named repository. [Related handler](https://github.com/iptelephony/persona/blob/afaf93062062b16b752d79a2b72a38bf700c7e0a/persona/api/user.py) · [Form](https://github.com/iptelephony/persona/blob/afaf93062062b16b752d79a2b72a38bf700c7e0a/persona/public/js/user.js) · [Maintainer note](https://github.com/iptelephony/persona/blob/afaf93062062b16b752d79a2b72a38bf700c7e0a/README.md)

The pinned v16 platform already has a POST operation with a target-specific permission check, an explicit reason, an Activity Log, a notification to the target and conditional email. Its login manager marks the resulting session with the impersonator. A rebuild combining the two designs must select one owner for session transition and notification. [Platform operation](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/core/doctype/user/user.py#L1651) · [Session transition](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/auth.py#L361)

## Proposed support-session contract

**Qualification.** The historical marketplace build's session expiry, restoration, notifications, translation catalog and relationship to the related archive remain unverified. [Named publisher repository](https://github.com/aoaicompany/persona)

[Read the consolidated workflow](../../../capabilities/guides/workspace.md#delegated-support-sessions-2).
