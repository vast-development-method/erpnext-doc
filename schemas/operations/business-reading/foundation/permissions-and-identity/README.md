# Identity and access

Begin with the service caller, effective identity and stored site state. The individual operation gives the bound values and local control paths.

[Business workflow guide](../../../../../docs/runtime/identity-permissions-and-tenancy.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

235 bindings across 8 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Service · Auth | 53 | [initialize … login as guest](operations-001.md#op-bcb383f2218565) · [login as … validate auth](operations-002.md#op-24ca6545a6d2c3) · [validate oauth … check request ip](operations-003.md#op-98e663210e5d29) |
| Service · Concurrency limiter | 9 | [web tier concurrency … get stats](operations-003.md#op-f2727c4af2975c) |
| Service · Oauth | 36 | [validate client id … validate code](operations-003.md#op-c701cae2333894) · [confirm redirect uri … get url delimiter](operations-004.md#op-b7e28ab0a7935e) · [generate json error response … get server url](operations-005.md#op-86220fe11101de) |
| Service · Permissions | 48 | [print has permission check logs … get doctype roles](operations-005.md#op-cbc644612cd649) · [get perms for … wrapper](operations-006.md#op-d71faf9b2b47f7) · [get parent and ancestors … check app permission](operations-007.md#op-cb3577480283b6) |
| Service · Rate limiter | 13 | [apply … wrapper](operations-007.md#op-a6dc16f63ee45b) |
| Service · Sessions | 31 | [hash sid … get](operations-007.md#op-2dbbf9d4eaa6bd) · [get boot assets json … get expiry period](operations-008.md#op-fa101c83888cdc) |
| Service · Share | 13 | [add … validate user access](operations-008.md#op-4f6a68f1e20c3b) · [add docshare … notify assignment](operations-009.md#op-ce370e23eb7786) |
| Service · Twofactor | 32 | [get default … confirm otp token](operations-009.md#op-f35c146637615e) · [get verification obj … reset otp secret](operations-010.md#op-d10f33d9c865a4) |
