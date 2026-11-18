# 数据传输与录入

## 将选定的 ERP 字段导出到 分析数据仓库，并从已确认的检查点恢复中断的传输

<a id="workflow-analytical-dataset-export"></a>

选择源表、允许导出的列、筛选条件及目标数据集。保存最后处理的标识和时间，以便中断后续传。

INV-001 和 INV-002 的修改时间相同，每页只导出一条。第一条写入后、保存检查点前作业中断；用德语界面恢复后，每张发票仍只有一行，目标表列名不变。

[English](../data.md#analytical-dataset-export) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/data.md#bigquery-connector).

## 从 ERP 导航栏打开聊天窗口，用所选语言发送消息

<a id="workflow-multilingual-chat-composition"></a>

管理员配置模型及服务允许的参数。分别记录会话语言、用户输入值和实际发送给服务的参数。

在德语聊天界面用中文输入法组字时，先按回车确认选字，写完句子后再点发送。确认选字不会发送消息；系统只发送一条消息，原始中文内容不受界面语言或所要求的回复语言影响。

[English](../data.md#multilingual-chat-composition) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/data.md#instagpt).

## 使用伊斯兰历输入日期，并在公历中核对对应的同一天

<a id="workflow-hijri-civil-day-conversion"></a>

选择回历日期，按批准的乌姆古拉历表换算出对应的民用日期。切换显示格式时保持同一天。

按乌姆库拉历表输入伊斯兰历 1445-09-01，切换至公历后应为 2024-03-11。重新打开字段并切回伊斯兰历，仍应为 1445-09-01；更改语言或数字字形不能改变日期或换算规则。

[English](../data.md#hijri-civil-day-conversion) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/data.md#islamic-calendar).

## 按尼泊尔历输入日期，并用对应的公历日期查找同一条记录

<a id="workflow-nepali-civil-day-conversion"></a>

在表单中选择尼泊尔历日期，保存对应的民用日期。同一天可在尼泊尔历和公历之间切换显示。

采购记录使用尼泊尔历 2081 年拜萨克月 1 日登记，另一位用户用公历 2024 年 4 月 13 日筛选时能找到同一条记录。切回尼泊尔历仍显示原日期，更改语言或数字样式不会改变实际日期。

[English](../data.md#nepali-civil-day-conversion) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/data.md#nepali-calendar).

## 用一种语言提问，并要求 ERP 助手用另一种语言回答，同时保留原始对话

<a id="workflow-multilingual-business-record-questions"></a>

将问题绑定到提问者及会话，仅向回答服务提供获准使用的记录上下文，并在原会话中保存答复。

一名使用德语界面的用户用南非荷兰语查询自己有权查看的发票未结金额。助手用南非荷兰语回答并指明来源字段，保留原始问题，不修改发票，也不扩大用户权限。

[English](../data.md#multilingual-business-record-questions) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/data.md#chatnext).
