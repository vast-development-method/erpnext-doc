# Integrations and service calls

Identify the local document and the external party or service. A call to an adapter establishes a handoff and can finish independently of remote delivery.

[Business workflow guide](../../../../../docs/services/external-integrations.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

315 bindings across 29 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · Activities | 15 | [get activities … is translatable](operations-001.md#op-d8e30bf4cd7d25) |
| Service · Api | 38 | [get translations … get recording credentials](operations-001.md#op-68d78c56fb42f2) · [is call integration enabled … link](operations-002.md#op-d8880b66aad7be) · [update call log … get datetime from timestamp](operations-003.md#op-4ee50a6f339f1d) |
| Service · Assignment rule | 2 | [get assignment rules list … duplicate assignment rule](operations-003.md#op-2539f22d2331e1) |
| Service · Auth | 1 | [oauth providers](operations-003.md#op-543a0ab972156c) |
| Service · Availability | 5 | [validate user … get user categories](operations-003.md#op-8dbe956c348565) |
| Service · Command palette | 21 | [search … keywords](operations-003.md#op-cee5a7441e08a7) · [search activity … record](operations-004.md#op-b054abf6b820ce) |
| Service · Comment | 5 | [on update … add attachments](operations-004.md#op-a4c32de0aec94d) |
| Service · Contact | 6 | [validate … search emails](operations-004.md#op-ec325cc4f4fab7) |
| Service · Dashboard | 24 | [initialize … get dashboard](operations-004.md#op-ddc4870cafd788) · [get chart … get deal status change counts](operations-005.md#op-cd6c184a3b56f4) |
| Service · Doc | 26 | [sort options … get group by fields](operations-005.md#op-4de05fa5ec91cd) · [get quick filters … delete bulk docs](operations-006.md#op-7c5a1218b84cbe) |
| Service · Doc share | 7 | [sync](operations-006.md#op-4cd96bfc1e1621) · [before validate … mirror share](operations-007.md#op-a23510863fe0d0) |
| Service · Email | 4 | [cancel scheduled email … get scheduled email](operations-007.md#op-0cd2bc57ef19a9) |
| Service · Exchange rate | 7 | [get exchange rate … raise exchange rate error](operations-007.md#op-e9c9268c478f84) |
| Service · Form | 27 | [ensure form source … seed visible fields](operations-007.md#op-101ff7e0282351) · [break … apply hidden defaults](operations-008.md#op-4f989050bcc667) |
| Service · Handler | 15 | [handle request … get all exophones](operations-008.md#op-3a3bc700a62753) · [get status updater url … update call log](operations-009.md#op-971ecab72ba7f2) |
| Service · Item | 8 | [should sync … on trash](operations-009.md#op-ac6fdc4b2f35ab) |
| Service · Live demo | 3 | [login … validate user](operations-009.md#op-6c38e3706da9d2) |
| Service · Mirror sync | 12 | [initialize … sync active](operations-009.md#op-c0372ac2250c8a) · [should mirror … delete mirror for](operations-010.md#op-bcdc28432c1952) |
| Service · Notifications | 3 | [get notifications … get hash](operations-010.md#op-92f59276db1a3b) |
| Service · Onboarding | 8 | [complete setup for fc site … get first deal](operations-010.md#op-7a81dc17bd9c20) |
| Service · Session | 4 | [get session role flags … get user info](operations-010.md#op-54ac7c091e1750) · [get organizations](operations-011.md#op-3a7386319fad98) |
| Service · Settings | 1 | [create email account](operations-011.md#op-4d1b9fe425e186) |
| Service · Todo | 7 | [validate … get redirect to doc](operations-011.md#op-d5510e44b8f708) |
| Service · Twilio handler | 23 | [initialize … get twilio number owners](operations-011.md#op-e47cb1e56aa266) · [get active loggedin users … to dict](operations-012.md#op-b9f3887462729f) |
| Service · User | 9 | [change password … update module in user](operations-012.md#op-644676371b6941) |
| Service · User permission | 8 | [dedup extra … sync user permissions](operations-012.md#op-a9181b4b4f7903) · [mirror permission](operations-013.md#op-14770bf7f73158) |
| Service · Utils | 12 | [should sync … merge dicts](operations-013.md#op-bcdd50993a1056) |
| Service · Views | 1 | [get views](operations-013.md#op-53ccb8b3899ea0) |
| Service · Whatsapp | 13 | [validate access … react on whatsapp message](operations-013.md#op-ea1fb47bf331ba) · [parse template parameters … add roles](operations-014.md#op-5a5764f818d138) |
