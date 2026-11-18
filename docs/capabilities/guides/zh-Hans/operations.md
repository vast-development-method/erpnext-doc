# 服务与项目

## 在多语言项目团队中跟踪工作项、状态变更和工时记录

<a id="workflow-work-tracking-and-time-reporting"></a>

工作项转入另一项目时获得新的显示编号，内部 UUID 保持不变。变更日志保留原编号。

一名使用德语的成员完成 OPS-7 并登记 90 分钟测试工时。使用南非荷兰语的负责人查看报告时，应看到同一个已完成工作项和 90 分钟工时，显示标签按其语言呈现。

[English](../operations.md#work-tracking-and-time-reporting) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#zymmr).

## 安排设施巡检，并记录每项测量值或是非检查结果及其执行人

<a id="workflow-facility-inspection-measurements"></a>

将周期性检查关联到资产或服务，记录执行人、监督人、时间，以及是非判定或对照限值的实测值。

允许温度范围为 2 至 8 °C，含两端。操作员用德语输入 8,1 °C 后，使用南非荷兰语的主管应看到同一地点和执行人名下的一条 8.1 °C 超限记录。

截至 10:00 应完成三项检查。第一项为 8.0 °C，符合含边界的 8.0 °C 上限；第二项为 8.1 °C，已超限；第三项缺少读数。完成率为 2/3，已完成项中的合格率为 1/2。重复通知不会再次创建纠正任务。

[English](../operations.md#facility-inspection-measurements) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#green-checklist).

## 记录事故、指定处理人，并跟踪调查和预防措施的落实情况

<a id="workflow-incident-investigation"></a>

将照片、初报、风险评估及纠正措施归入同一事件，按该服务配置的时限升级处理。

使用相同的请求编号两次提交同一份南非荷兰语事故报告和照片，再重试一次发给德语收件人的失败通知。系统只保留一个报告版本和一个照片引用，分别记录各次投递，事故编号和原始叙述均不变。

[English](../operations.md#incident-investigation) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#incident-management).

## 管理场地资产和投诉，通过电子邮件核验访客身份并签发通行证

<a id="workflow-facility-access-and-visitor-verification"></a>

登记来访者及接待人，按规定拍照并核验一次性验证码。核验成功后签发通行证。

为一名使用阿拉伯语姓名、希望接收英语邮件的访客登记，先输入过期验证码，再用有效验证码核验并重复签发通行证。过期码不会生成通行证，成功后本次访问只有一张通行证；访客原名保留，在两种书写方向下证件编号一致。

[English](../operations.md#facility-access-and-visitor-verification) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#site-management).

## 登记普通工单或与资产相关的工单，并计算从创建到解决所用的时间

<a id="workflow-asset-and-service-ticket-resolution"></a>

适用时将服务工单关联至资产。保留负责人、状态和各次转换时间，重新打开后仍可分别统计首次和最终解决时间。

普通工单于同一天的 08:00 UTC 创建，09:30 首次解决，10:00 重新打开，11:00 UTC 最终解决。按实际经过时间计算，首次解决用时 90 分钟，从创建至最终解决用时 180 分钟；两种语言界面显示相同的工单编号和状态变化。

[English](../operations.md#asset-and-service-ticket-resolution) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#helpdesk-management).

## 按租约发票跟踪租金，并使用每位租户偏好的语言准备付款提醒

<a id="workflow-rent-collection-and-reminders"></a>

将租金发票关联到有效租约，并分配实际收款。根据这些记录计算未结余额，再向租户准备催款提醒。

一张金额为 900 的租金发票已核销 350。使用德语界面的管理员准备南非荷兰语提醒时，提醒显示尚欠 550，打开聊天链接只记录交接，不会生成付款记录。

[English](../operations.md#rent-collection-and-reminders) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#estateflow).

## 将 项目看板卡片作为 ERP 工单跟踪，更新看板时保留清单及其子任务之间的关联

<a id="workflow-board-issue-and-checklist-synchronization"></a>

将看板卡片映射到问题单，将检查清单映射到父任务，条目映射到子任务。重复事件复用原映射。

同一张卡片含有两个阿拉伯语清单项。看板两次发送同一事件后，德语界面应只显示一个问题、一项父任务和两项子任务，并保留原始标题及标识。

[English](../operations.md#board-issue-and-checklist-synchronization) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#trello).

## 在前台为访客办理登记、打印通行证，并使用同一到访编号记录离开时间

<a id="workflow-visitor-check-in-and-departure"></a>

按规定登记访客类别、接待人、照片和签名。离场时使用通行证号，并将评价保存在同一次访问记录下。

一名使用南非荷兰语的客户在德语前台登记并领取通行证。客户凭打印的通行证编号离场并完成四项接待评分，同一次访问只记录一个离场时间和四个分值，终端随后清除上一位访客的信息。

[English](../operations.md#visitor-check-in-and-departure) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/operations.md#visitor-management).
