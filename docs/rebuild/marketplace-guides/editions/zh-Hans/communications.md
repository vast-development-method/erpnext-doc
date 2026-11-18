# 通话、调查与消息

[English](../en/communications.md) · [Afrikaans](../af/communications.md) · [Deutsch](../de/communications.md) · 简体中文

[全部主题](README.md)

验收示例描述的是新系统应达到的结果。英文详细说明会区分发布者的描述、源代码中的实现与运行环境中的实测结果。

## Tata Smartflo Call Integration

从 CRM 记录发起 Smartflo 呼叫，将通话明细与坐席的活动记录核对。

**有资料可查的工作流程**

配置了电话号码的坐席可直接从 ERP 发起呼叫。发布方说明，集成可获取 Smartflo 通话日志和录音，关联业务单据，并按日期、状态或呼叫类型筛选报表。

**建议的验收示例**

服务商两个有重叠的日志页包含同一次外呼；导入后，报告中只应有一通已接听的外呼，时长 48 秒，并关联到对应的 CRM 活动。翻译通话状态不能改变服务商的通话编号或所拨号码。

[英文详细说明](../../apps/call_integration.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/call_integration)

## FCM Notification

按接收方的语言偏好向已订阅的设备发送 ERP 通知。

**有资料可查的工作流程**

发布者说明将推送动作与新建 Notification Log 记录关联。先通过 User Device 把设备关联到目标用户，再在该用户已订阅的事件发生时发送通知。

**建议的验收示例**

同一接收人的两台设备分别以南非荷兰语和德语显示 PO-18 的审批通知。重复处理已确认的发送记录时不再推送，每台设备各有一条发送记录，指向的单据均为 PO-18。

[英文详细说明](../../apps/fcm_notification.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/fcm_notification)

## Telenor Sms

通过 Telenor 向联系人发送短信，并区分网关已受理和已确认送达两种状态。

**有资料可查的工作流程**

发布方说明，ERP 用户可通过 Telenor 接口向联系人发送短信。其公开支持论坛未说明送达回执、字符编码或语言选择机制。

**建议的验收示例**

一名使用英语的员工向联系人 C17 发送已获批准的南非荷兰语预约提醒。网关接受后应记录一条含预约编号的已提交短信，手机端送达状态仍待确认。

[英文详细说明](../../apps/telenor_sms.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/telenor_sms)

## Tripetto Survey Integration

发布可按回答跳转的问卷，并按问题和选项汇总使用不同语言填写的答卷。

**有资料可查的工作流程**

问卷设计人员从问卷记录打开可视化编辑器，保存问题和跳转规则，再发布问卷以生成表单链接。参与者提交表单后，ERP 会保存一条答卷记录（Survey Answer）。

**建议的验收示例**

两名受访者分别用德语和南非荷兰语选择标识为 `delivery` 的选项。两份答卷应归入同一选项，各自的后续回答保留原文，并与正确的答卷关联。

[英文详细说明](../../apps/tripetto_survey.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/tripetto_survey)

## Ultramsg Whatsapp Integration

当业务事件满足已配置的条件时，通过 UltraMsg 发送纯文本 WhatsApp 提醒。

**有资料可查的工作流程**

管理员配置 UltraMsg 实例、令牌、事件条件和带占位符的消息模板。发布方说明，应用可自动发送纯文本 WhatsApp 消息，例如逾期订单通知或付款提醒。

**建议的验收示例**

一位使用法语的客户有一张逾期订单。同一事件处理两次，而 UltraMsg 已将首次提交排入队列时，应只保留一条带原订单号的法语提醒，状态仍为排队中。

[英文详细说明](../../apps/ultramsg_whatsapp_integration.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/ultramsg_whatsapp_integration)

## Whatsapp App

向选定的线索、商机或供应商联系人发送个性化 WATI 模板消息，并查看各收件人的发送结果。

**有资料可查的工作流程**

管理员启用 WATI 连接，并将 WATI 模板的参数映射到 ERP 字段。操作人员可从线索、商机或供应商列表中选择一个或多个收件人，并查看消息往来记录。

**建议的验收示例**

德语操作员向一名使用南非荷兰语、留有已核实纳米比亚电话号码的供应商发送通知。队列中应只有一条采用已批准南非荷兰语模板的消息，并保留供应商编号和已存储的国际电话号码。

[英文详细说明](../../apps/whatsapp_app.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/whatsapp_app)

## WhatsApp Integration

当指定字段或单据状态变更时，使用获批的 WhatsApp 模板发送消息并附上对应的 PDF。

**有资料可查的工作流程**

管理员在 ERP 和 Meta 中创建匹配的模板，选择语言，并按需将 PDF 映射到模板的媒体标头。根据产品介绍，保存、提交或更新单据，或变更字段值时，均可按规则发送文本或 PDF 通知。

**建议的验收示例**

一条规则要求消息与 PDF 均使用阿拉伯语。英语操作员提交发票时，如果只有阿拉伯语消息模板，系统应暂缓通知、指出缺少的 PDF 版式，并避免发送语言不符的附件。

[英文详细说明](../../apps/whatsapp_integration.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/whatsapp_integration)

## Whatsapp Plus

将收到的 WhatsApp 消息关联到客户，在原对话中回复，并向符合条件的收件人发送经审核的消息。

**有资料可查的工作流程**

操作人员可通过收到的 WhatsApp 消息识别已建档客户，回复消息、下载媒体文件，或向选定客户和群组发送模板消息。发布方表示，界面会适应工作站所用语言，示例截图使用意大利语。

**建议的验收示例**

一位客户用中文发送消息并附上文档，使用意大利语的客服用中文回复。德语同事重新打开会话时，应看到同一客户的两条原文消息，并按原有权限访问同一附件。

[英文详细说明](../../apps/whatsapp_plus.md) · [发布者的市场页面](https://cloud.frappe.io/marketplace/apps/whatsapp_plus)
