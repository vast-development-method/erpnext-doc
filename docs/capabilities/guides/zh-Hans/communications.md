# 客户沟通

## 从 CRM 记录发起 呼叫，将通话明细与坐席的活动记录核对

<a id="workflow-outbound-calling-and-call-dispositions"></a>

使用坐席配置的号码从业务记录发起呼叫，将通话标识、时间、处置结果和受权限限制的录音关联至该记录。

服务商两个有重叠的日志页包含同一次外呼；导入后，报告中只应有一通已接听的外呼，时长 48 秒，并关联到对应的 CRM 活动。翻译通话状态不能改变服务商的通话编号或所拨号码。

[English](../communications.md#outbound-calling-and-call-dispositions) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#tata-smartflo-call-integration).

## 按接收方的语言偏好向已订阅的设备发送 ERP 通知

<a id="workflow-device-notification-delivery"></a>

将设备登记在目标用户名下。发生该用户订阅的通知事件时，按符合条件的设备分别记录推送尝试。

同一接收人的两台设备分别以南非荷兰语和德语显示 PO-18 的审批通知。重复处理已确认的发送记录时不再推送，每台设备各有一条发送记录，指向的单据均为 PO-18。

[English](../communications.md#device-notification-delivery) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#fcm-notification).

## 通过 短信网关 向联系人发送短信，并区分网关已受理和已确认送达两种状态

<a id="workflow-text-message-acceptance-and-delivery"></a>

选择联系人、电话号码和短信内容，分别记录服务商受理、送达回执和失败结果。

一名使用英语的员工向联系人 C17 发送已获批准的南非荷兰语预约提醒。网关接受后应记录一条含预约编号的已提交短信，手机端送达状态仍待确认。

[English](../communications.md#text-message-acceptance-and-delivery) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#telenor-sms).

## 发布可按回答跳转的问卷，并按问题和选项汇总使用不同语言填写的答卷

<a id="workflow-branching-surveys-and-response-aggregation"></a>

保存问题和分支规则，发布问卷，并将每份答卷关联到相应的已发布问卷版本。

两名受访者分别用德语和南非荷兰语选择标识为 `delivery` 的选项。两份答卷应归入同一选项，各自的后续回答保留原文，并与正确的答卷关联。

[English](../communications.md#branching-surveys-and-response-aggregation) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#tripetto-survey-integration).

## 当业务事件满足已配置的条件时，通过 消息服务 发送纯文本 提醒

<a id="workflow-rule-based-text-reminders"></a>

将单据事件与触发条件、接收人和已获批准的消息模板关联，发送时填入本次事件的字段值。

一位使用法语的客户有一张逾期订单。同一事件处理两次，而 消息服务 已将首次提交排入队列时，应只保留一条带原订单号的法语提醒，状态仍为排队中。

[English](../communications.md#rule-based-text-reminders) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#ultramsg-whatsapp-integration).

## 向选定的线索、商机或供应商联系人发送个性化 模板消息，并查看各收件人的发送结果

<a id="workflow-personalized-recipient-messaging"></a>

将模板参数映射至业务字段，从线索、商机或供应商列表选择收件人，逐一记录发送结果。

德语操作员向一名使用南非荷兰语、留有已核实纳米比亚电话号码的供应商发送通知。队列中应只有一条采用已批准南非荷兰语模板的消息，并保留供应商编号和已存储的国际电话号码。

[English](../communications.md#personalized-recipient-messaging) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#whatsapp-app).

## 当指定字段或单据状态变更时，使用获批的 模板发送消息并附上对应的 PDF

<a id="workflow-translated-document-message-attachments"></a>

为单据规则配置已批准的语言模板及 PDF 附件。保存、提交或指定字段变更时按规则触发发送。

一条规则要求消息与 PDF 均使用阿拉伯语。英语操作员提交发票时，如果只有阿拉伯语消息模板，系统应暂缓通知、指出缺少的 PDF 版式，并避免发送语言不符的附件。

[English](../communications.md#translated-document-message-attachments) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#whatsapp-integration).

## 将收到的 消息关联到客户，在原对话中回复，并向符合条件的收件人发送经审核的消息

<a id="workflow-incoming-customer-conversations"></a>

将收到的消息关联至客户，授权工作人员可查看会话、回复并获取媒体文件。保留原始文本和媒体。

一位客户用中文发送消息并附上文档，使用意大利语的客服用中文回复。德语同事重新打开会话时，应看到同一客户的两条原文消息，并按原有权限访问同一附件。

[English](../communications.md#incoming-customer-conversations) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/communications.md#whatsapp-plus).
