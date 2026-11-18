# Workflow, automation and dispatch · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Socket

<a id="op-2497803cef2fee"></a>
### Socket.installed apps

`operation_foundation_realtime_socket_business_behavior_realtime_transport_installed_apps`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at str.

**Explicit results** self.\_session.installed\_apps.

**Local steps**

- Return self.\_session.installed\_apps.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L751) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L319)

<a id="op-4b15dab8b6f6d0"></a>
### Socket.connected

`operation_foundation_realtime_socket_business_behavior_realtime_transport_connected`

**Inputs** self.

**Declared result** bool.

**Explicit results** self.\_sio.manager.is\_connected(self.sid, self.namespace).

**Local steps**

- Return self.\_sio.manager.is\_connected(self.sid, self.namespace).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L813) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L314)

<a id="op-3a69ea2ef543a9"></a>
### Socket.join

`operation_foundation_realtime_socket_business_behavior_realtime_transport_join`

**Inputs** self, room.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not self.\_connected().
  - Return no value.
- Evaluate await self.\_sio.enter\_room(self.sid, room, namespace = self.namespace).

If control reaches the end, it returns no value.

**Methods declared on this owner** [connected](operations-048.md#op-4b15dab8b6f6d0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L889) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L320)

<a id="op-ceb2c180046842"></a>
### Socket.leave

`operation_foundation_realtime_socket_business_behavior_realtime_transport_leave`

**Inputs** self, room.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not self.\_connected().
  - Return no value.
- Evaluate await self.\_sio.leave\_room(self.sid, room, namespace = self.namespace).

If control reaches the end, it returns no value.

**Methods declared on this owner** [connected](operations-048.md#op-4b15dab8b6f6d0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1018) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L321)

<a id="op-a1d74318d88c8c"></a>
### Socket.emit

`operation_foundation_realtime_socket_business_behavior_realtime_transport_emit`

**Inputs** self, event, data = no value, room = no value.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Evaluate await self.\_sio.emit(event, data, to = (room or self.sid), namespace = self.namespace).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in room → self.sid.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1147) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L315)

<a id="op-af852b22cadd79"></a>
### Socket.get

`operation_foundation_realtime_socket_business_behavior_realtime_transport_get`

**Inputs** self, key, default = no value.

**Declared result** object.

**Explicit results** self.\_session.data.get(key, default).

**Local steps**

- Return self.\_session.data.get(key, default).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1307) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L316)

<a id="op-99d6072e1ac86d"></a>
### Socket.set

`operation_foundation_realtime_socket_business_behavior_realtime_transport_set`

**Inputs** self, key, value.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set self.\_session.data at key from value.
- If not self.\_connected().
  - Return no value.
- Evaluate await self.\_sio.save\_session(self.sid, self.\_session, namespace = self.namespace).

If control reaches the end, it returns no value.

**Methods declared on this owner** [connected](operations-048.md#op-4b15dab8b6f6d0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1402) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L323)

<a id="op-d168cdcdf07d93"></a>
### Socket.participants

`operation_foundation_realtime_socket_business_behavior_realtime_transport_participants`

**Inputs** self, room.

**Declared result** list at str.

**Explicit results** sids.

**Local steps**

- Set sids from list().
- For each item in self.\_sio.manager.get\_participants(self.namespace, room).
  - Evaluate sids.append(item at 0 when isinstance(item, tuple), otherwise item).
    - Value choice on isinstance(item, tuple) — true gives item at 0, false gives item.
- Return sids.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1575) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L322)

<a id="op-9a058489cd43ff"></a>
### Socket.user of

`operation_foundation_realtime_socket_business_behavior_realtime_transport_user_of`

**Inputs** self, sid.

The declaration is asynchronous.

**Declared result** (str bitwise or no value).

**Explicit results** await self.\_sio.get\_session(sid, namespace = self.namespace).user · no value.

**Local steps**

- Attempt the following.
  - Return await self.\_sio.get\_session(sid, namespace = self.namespace).user.
- On failure (KeyError).
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1754) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L326)

<a id="op-b8d41062ca5a54"></a>
### Socket.has permission

`operation_foundation_realtime_socket_business_behavior_realtime_transport_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, name.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1881) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L317)

<a id="op-d1d0e2095980fe"></a>
### Sync Socket.initialize

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_initialize`

**Inputs** self, socket, loop.

**Local steps**

- Set self.\_socket from socket.
- Set self.\_loop from loop.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L1983) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L331)

<a id="op-f209469b6e442b"></a>
### Sync Socket.sid

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_session_identifier`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_socket.sid.

**Local steps**

- Return self.\_socket.sid.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2071) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L338)

<a id="op-c6f97827b61106"></a>
### Sync Socket.namespace

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_namespace`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_socket.namespace.

**Local steps**

- Return self.\_socket.namespace.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2123) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L335)

<a id="op-a434b54d4f9ef8"></a>
### Sync Socket.site

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_site`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_socket.site.

**Local steps**

- Return self.\_socket.site.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L340)

<a id="op-d0a49b4d28fc84"></a>
### Sync Socket.user

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_user`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_socket.user.

**Local steps**

- Return self.\_socket.user.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2227) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L341)

<a id="op-893e17330afe27"></a>
### Sync Socket.user type

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_user_type`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.\_socket.user\_type.

**Local steps**

- Return self.\_socket.user\_type.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2279) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L343)

<a id="op-a08334bfbaa702"></a>
### Sync Socket.installed apps

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_installed_apps`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at str.

**Explicit results** self.\_socket.installed\_apps.

**Local steps**

- Return self.\_socket.installed\_apps.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2331) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L332)

<a id="op-3e90da68c50118"></a>
### Sync Socket.join

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_join`

**Inputs** self, room.

**Declared result** no value.

**Local steps**

- Evaluate self.\_run(self.\_socket.join(room)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run](operations-049.md#op-42200e600376f7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2393) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L333)

<a id="op-18a2aaaac9e0bf"></a>
### Sync Socket.leave

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_leave`

**Inputs** self, room.

**Declared result** no value.

**Local steps**

- Evaluate self.\_run(self.\_socket.leave(room)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run](operations-049.md#op-42200e600376f7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2482) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L334)

<a id="op-17004edbfbf092"></a>
### Sync Socket.emit

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_emit`

**Inputs** self, event, data = no value, room = no value.

**Declared result** no value.

**Local steps**

- Evaluate self.\_run(self.\_socket.emit(event, data, room)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run](operations-049.md#op-42200e600376f7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2571) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L328)

<a id="op-fadf120ba6641e"></a>
### Sync Socket.get

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_get`

**Inputs** self, key, default = no value.

**Declared result** object.

**Explicit results** self.\_socket.get(key, default).

**Local steps**

- Return self.\_socket.get(key, default).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2714) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L329)

<a id="op-68f8ea6a3347c9"></a>
### Sync Socket.set

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_set`

**Inputs** self, key, value.

**Declared result** no value.

**Local steps**

- Evaluate self.\_run(self.\_socket.set(key, value)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run](operations-049.md#op-42200e600376f7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2805) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L339)

<a id="op-fba0c28bb3afd9"></a>
### Sync Socket.participants

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_participants`

**Inputs** self, room.

**Declared result** list at str.

**Explicit results** self.\_socket.participants(room).

**Local steps**

- Return self.\_socket.participants(room).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2910) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L336)

<a id="op-1b71c9255c025b"></a>
### Sync Socket.user of

`operation_foundation_realtime_socket_business_behavior_sync_realtime_transport_user_of`

**Inputs** self, sid.

**Declared result** (str bitwise or no value).

**Explicit results** self.\_run(self.\_socket.user\_of(sid)).

**Local steps**

- Return self.\_run(self.\_socket.user\_of(sid)).

**Methods declared on this owner** [run](operations-049.md#op-42200e600376f7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L2992) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L342)
