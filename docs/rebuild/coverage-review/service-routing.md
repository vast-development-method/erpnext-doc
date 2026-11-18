# Call routing and handover observations

The [call-routing contract](../../people-and-services/incoming-calls.md) gives the six decisions and the Monday noon handover example. The noon-to-12:01 example combines separately exercised schedule, recipient, transfer and completion behavior. The [execution receipt](reference-tests.md) identifies the 13 call-log, three communication-medium and two incoming-call-settings tests. Classification and personal settings have additional suites. The [language contract](../../services/languages-and-issuance.md) governs how the same call appears to different operators.

## Sources by operation

### Incoming call, agent transfer and service history

- [Medium validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/communication/doctype/communication_medium/communication_medium.py#L32-L42)
- [Incoming schedule](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/incoming_call_settings/incoming_call_settings.py#L33-L84)
- [Group and time lookup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/utils.py#L20-L61)
- [Insertion and party links](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L55-L76)
- [Recipient selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L108-L153)
- [Status transitions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L78-L104)
- [Status constants](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L21-L23)
- [Notification recipients](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L83-L100)
- [Summary and access rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L156-L206)
- [Timeline](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/telephony/doctype/call_log/call_log.py#L295-L329)
