# 数据分析、人工智能与日历

[English](../en/data.md) · [Afrikaans](../af/data.md) · [Deutsch](../de/data.md) · 简体中文

[全部主题](README.md)

## BigQuery Connector

发布者的导出表单可将源表映射到指定的目标表，示例将 tabUser 映射为 user，同时可选列并设置筛选条件。增量同步区显示间隔、上次同步时间、最后同步的 ID 和调度锁状态。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/data.md#workflow-analytical-dataset-export) · [来源说明](../../apps/frappe_bigquery.md)

## InstaGPT

根据 Brandimic 的说明，系统经理或管理员先设置密钥、模型，以及范围为 0 至 200 的温度，员工随后可通过导航栏聊天窗口发送消息。OpenAI 的 Chat Completions 温度参数文档给出的范围是 0 至 2；该应用实际使用的接口及其换算方式尚未核实。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/data.md#workflow-multilingual-chat-composition) · [来源说明](../../apps/instagpt.md)

## Islamic Calendar

Kanak 介绍，用户可在 ERP 表单中用伊斯兰历日期选择器输入日期，并与公历双向切换。一个注明由 Kanak 开发的公开副本分别设置显示格式和日期选择器格式，使用内置的乌姆库拉历月首日期表进行换算。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/data.md#workflow-hijri-civil-day-conversion) · [来源说明](../../apps/islamic_calendar.md)

## Nepali Calendar

Kanak 的指南显示，用户可在日期字段中选择尼泊尔历日期，并在同一表单内切换到对应的公历日期。发布者列出的使用场景包括销售、采购、人力资源和会计。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/data.md#workflow-nepali-civil-day-conversion) · [来源说明](../../apps/nepali_calendar.md)

## ChatNext

市场页面描述了用户针对当前 ERP 场景提问的功能。一份公开的历史代码将用户消息存入会话，把消息连同聊天记录及当前页面信息发送给另一项服务，再将返回的答案保存为机器人消息。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/data.md#workflow-multilingual-business-record-questions) · [来源说明](../../apps/nextai.md)
