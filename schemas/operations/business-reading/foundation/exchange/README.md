# Integration and transport

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/services/remote-transport-contracts.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

808 bindings across 61 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · Api | 2 | [handle … get api version](operations-001.md#op-a0bdebb30297b1) |
| Service · App | 17 | [get after response callbacks … application with statics](operations-001.md#op-ba521cb361eeb8) |
| Record · Auto email report | 22 | [autoname … validate report count](operations-001.md#op-98c50b75c6c520) · [validate report format … get half year start](operations-002.md#op-8f175e3ab9a80e) |
| Service · Cloud billing | 18 | [summary … add payment method](operations-002.md#op-1b1f43d3918497) · [confirm payment method … path](operations-003.md#op-9771e2a5aa3ef9) |
| Service · Cloud marketplace | 11 | [list apps … clean](operations-003.md#op-b65d8d24397a1e) |
| Service · Cloud settings | 50 | [initialize … get](operations-003.md#op-b42f977b0cd91a) · [post … install app](operations-004.md#op-90523f8b526c39) · [uninstall app … domain row](operations-005.md#op-e2e913c593f85f) |
| Record · Connected app | 13 | [get openid configuration … has token](operations-006.md#op-bf5146a735de2b) |
| Service · Discover | 7 | [search doctypes … without](operations-006.md#op-b839436edf561f) |
| Service · Discovery | 41 | [root … method](operations-006.md#op-9064a31faab99e) · [doctype methods … get doctype methods](operations-007.md#op-891804eab75b08) · [unwrap method … without none](operations-008.md#op-c9c9b0050c15ae) |
| Record · Document follow | 2 | [get permission query conditions … has permission](operations-008.md#op-ae73aca9daf5e7) |
| Service · Documents | 6 | [get document … delete document](operations-008.md#op-944d1695aaa373) |
| Service · Email | 7 | [sendmail to system managers … get recipient avatars](operations-008.md#op-4606470ed6b70d) · [get system managers … sendmail](operations-009.md#op-75a54e3c0be8e5) |
| Record · Email account | 67 | [cache email account … is exists in db](operations-009.md#op-cca57ba9a7e7c0) · [from record … process mail](operations-010.md#op-19459a94e29c04) · [handle bad emails … on doctype update](operations-011.md#op-e398e36c3a7b86) |
| Service · Email body | 33 | [get email](operations-011.md#op-3c169e9767d633) · [initialize … get message id](operations-012.md#op-efbe4a5c3be847) · [get signature … get brand name](operations-013.md#op-88d68f5802342d) |
| Record · Email domain | 8 | [get error message … validate outgoing server conn](operations-013.md#op-ea5ca292140bda) |
| Record · Email group | 11 | [onload … import from](operations-013.md#op-314e88c54ae6ce) · [add subscribers … add query params](operations-014.md#op-d11921d93377e6) |
| Record · Email group member | 3 | [after delete … after doctype insert](operations-014.md#op-fbff77ef471c4f) |
| Service · Email oauth | 13 | [get one click services … redirect](operations-014.md#op-58006ad6263ee5) |
| Record · Email queue | 64 | [onload … get duplicate](operations-014.md#op-20f244adcb631f) · [new … message placeholder](operations-015.md#op-318154cd1ae2f5) · [build message … should include unsubscribe link](operations-016.md#op-f5158a555a19d1) · [unsubscribe message … as dict](operations-017.md#op-a03021bbc12e2d) |
| Record · Email queue recipient | 4 | [is mail to be sent … on doctype update](operations-017.md#op-97f1a287b87a95) |
| Record · Email template | 8 | [response … get email templates](operations-017.md#op-46b3afaa3cc67e) |
| Record · Email unsubscribe | 2 | [validate](operations-017.md#op-b04137eb89b45b) · [on update](operations-018.md#op-4d22957a40eb4d) |
| Record · Geolocation settings | 7 | [autocomplete … autocomplete](operations-018.md#op-8542f47ef7b066) |
| Record · Google calendar | 24 | [validate … parse google calendar date](operations-018.md#op-aa0cd57973af62) · [google calendar to repeat on … get attendees](operations-019.md#op-686a2cafbf1481) |
| Record · Google contacts | 9 | [validate … get indexed value](operations-019.md#op-76e56e1518f67f) |
| Service · Google oauth | 11 | [create google oauth state … get authentication url](operations-019.md#op-e513af14b2e512) · [get google service object … callback](operations-020.md#op-9674e7df885276) |
| Record · Google settings | 1 | [get file picker settings](operations-020.md#op-acc20f1e41f535) |
| Service · Handler | 11 | [handle … run doc method](operations-020.md#op-482660bbc46881) |
| Service · Inbox | 8 | [get email accounts … link communication to document](operations-020.md#op-092d5de9a555e4) |
| Record · Integration request | 5 | [autoname … handle failure](operations-021.md#op-ae48139e68d6db) |
| Record · Ldap settings | 13 | [validate … reset password](operations-021.md#op-3b17314f9ca270) |
| Service · Mcp | 1 | [handle](operations-021.md#op-4ad3f0e87f60c5) |
| Service · Methods | 5 | [call method … document function](operations-021.md#op-99d4d7c877c93e) |
| Service · Middlewares | 4 | [invoke … loader](operations-022.md#op-c148a81e95fee1) |
| Record · Notification | 51 | [onload … get email template content](operations-022.md#op-0167841579d85a) · [create system notification … get assignees](operations-023.md#op-2d9cea56c99a4c) · [get emails from template … install notification templates](operations-024.md#op-6f6b738940e76e) |
| Service · Oauth | 7 | [initialize … connect smtp](operations-024.md#op-ea047d23963bf4) |
| Record · Oauth bearer token | 2 | [validate … clear old logs](operations-024.md#op-67fcc8fe823a93) |
| Record · Oauth client | 6 | [validate … client id issued at](operations-024.md#op-d42fffaf3afdac) |
| Service · Oauth2 | 21 | [get oauth server … sanitize kwargs](operations-024.md#op-15915b42b53cba) · [encode params … set allowed cors](operations-025.md#op-e169c2c4c65294) |
| Service · Oauth2 logins | 10 | [login via google … login via office365](operations-025.md#op-e403f57743883e) · [login via salesforce … decoder compat](operations-026.md#op-a0c911e2feca94) |
| Service · Platform providers | 1 | [migrate to](operations-026.md#op-e73f6ff10d1bfc) |
| Service · Platformcloud | 2 | [get remote script … Platformcloud migrator](operations-026.md#op-847b7b7b52c216) |
| Service · Platformcloud billing | 12 | [get base url … verify verification code](operations-026.md#op-12835289c84310) |
| Service · Platformmail | 8 | [initialize … validate](operations-026.md#op-f031306d13a0b5) · [send raw … raise for status](operations-027.md#op-ff7b67553344bf) |
| Service · Protocol | 6 | [initialize … error envelope](operations-027.md#op-72a65afb4097ca) |
| Record · Push notification settings | 2 | [validate … validate relay server setup](operations-027.md#op-39f7e6d36b30d1) |
| Service · Queue | 9 | [get emails sent this month … retry sending emails](operations-027.md#op-e9444c70974073) |
| Service · Receive | 54 | [initialize … connect imap](operations-027.md#op-e5696fdf1b657d) · [connect pop … get charset](operations-028.md#op-0dbc3366ea8710) · [get payload … clean subject](operations-029.md#op-31d6c9a8b75565) · [get email fields … as dict](operations-030.md#op-62709fdc724efa) |
| Service · Server | 4 | [dispatch … valid identity](operations-030.md#op-7430d9d3d7789d) |
| Record · Slack webhook url | 1 | [send slack message](operations-030.md#op-cc382384a8c76a) |
| Service · Smtp | 9 | [initialize … throw invalid credentials exception](operations-030.md#op-bc1c2a094b14ba) |
| Record · Social login key | 5 | [autoname … provider allows signup](operations-030.md#op-3f1ce063e073c7) |
| Record · Token cache | 5 | [get auth header … update data](operations-030.md#op-8af1aba157fd0b) · [get expires in … get json](operations-031.md#op-8b5e4285373ac3) |
| Service · Tools | 15 | [generate … error result](operations-031.md#op-7ae762df5091c2) |
| Service · Transport | 9 | [handle request … check metadata](operations-031.md#op-a009da5323e173) · [check origin … json response](operations-032.md#op-bc362d84496f5e) |
| Record · Unhandled email | 1 | [clear old logs](operations-032.md#op-dd4cd524d76f97) |
| Service · Utils | 14 | [get port … get oauth settings](operations-032.md#op-5270e90ce51d6a) |
| Service · V1 | 10 | [document list … read doc](operations-032.md#op-6c5080b7b99663) · [get values for link and dynamic link fields … get request form data](operations-033.md#op-ce38ff2aa30687) |
| Service · V2 | 13 | [handle rpc call … run doc method](operations-033.md#op-2405a50ad9c8dc) |
| Record · Webhook | 22 | [get all webhooks … after delete](operations-033.md#op-a2e95bd46226d8) · [execute for doc … get all queues](operations-034.md#op-5d292535da7f80) |
| Record · Webhook request log | 1 | [clear old logs](operations-034.md#op-87596841e51a03) |
