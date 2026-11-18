# 会计与税务

## 提交埃及电子发票，并逐张跟踪税务机关的验证结果

<a id="workflow-egyptian-electronic-tax-submission"></a>

发票、贷项和借项通知单可逐张或批量提交。每份单据分别记录初步受理结果和最终核验结果。

测试服务对同一批已签名单据返回 HTTP 202，INV-001 获得外部编号，INV-002 返回结构错误。只有 INV-001 等待最终验证，INV-002 需要修正，两张发票均不能标记为已通过最终审核；阿拉伯语和德语界面应保留原始编号、错误代码及已签名的请求。

分别保存批次编号和每张发票的结果。更正版本关联到被拒的成员。若已初步受理的发票后来未通过校验，保留两个事件及其时间。重新提交另一张更正发票不会改动原先的校验轨迹或已过账发票。

[English](../accounting.md#egyptian-electronic-tax-submission) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/accounting.md#e-invoice-egypt).

## 将款项分配到银行远期外汇合约，并在撤销未使用的合约金额时记录损益

<a id="workflow-forward-exchange-contract-allocation"></a>

将每笔付款关联到各远期合约的实际使用额。取消获利的出口远期合约时，借记银行，贷记汇兑收益。

出口远期合约金额为 1,000 USD，约定汇率为每美元 17.50 NAD，已使用 600 USD。以 17.20 撤销 100 USD 且无手续费后，余额为 300 USD；无论界面语言如何，银行账户借记 30 NAD，汇兑收益贷记 30 NAD。

[English](../accounting.md#forward-exchange-contract-allocation) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/accounting.md#forward-contract).

## 从 PDF 中提取发票内容，核对交易方、日期、币种和各行金额后再创建草稿

<a id="workflow-invoice-image-and-document-extraction"></a>

选择采购或销售方向，读取 PDF，将票面总额与行项目合计核对。审核后的发票草稿保留原始 PDF 附件。

将日期为 14.07.2023、唯一明细金额写作 1.234,50 EUR 的德语 PDF 导入，用英语复核并重复确认同一次导入。系统只生成一份关联草稿，日期为 2023-07-14，金额为 1234.50 欧元；可回查原文，交易方、币种和数值不变。

[English](../accounting.md#invoice-image-and-document-extraction) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/accounting.md#ai-invoice-importer).

## 在也门本地化模块中登记员工预支款，并按审计人员偏好的语言核对还款

<a id="workflow-employee-advance-and-return-in-yemen"></a>

发放预支款时借记员工预支账户，贷记付款账户。归还时关联原预支凭证，并对调借贷分录。

预支款为 100 个交易币种单位，汇率为每单位折合 2 个公司本位币单位，因此借方和贷方各为 200。按相同汇率全额归还时借贷方向互换，两边余额抵消，阿拉伯语和英语报表中的科目及金额相同。

[English](../accounting.md#employee-advance-and-return-in-yemen) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/accounting.md#pav).

## 开具首付款发票，并按销售订单的付款计划为剩余各期分别开票

<a id="workflow-sales-order-advance-and-instalment-invoicing"></a>

在销售订单上指定付款条款及首期日期。首付款发票包含约定费用，其余各期在到期前两天开票。

订单本金为 1,000，首付 20%，另有运费 50，余款自 1 月 15 日起分三期支付，首付款发票为 250。1 月 13 日重复运行计划任务只会生成一张金额为 266.67 的首期发票，未收款时更改客户语言也不会改变全额未结状态。

[English](../accounting.md#sales-order-advance-and-instalment-invoicing) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/accounting.md#payment-installments).

## 根据已映射的凭证编制英国增值税申报表，按所属期间申报并核对税务机关的回执

<a id="workflow-british-return-aggregation"></a>

企业或授权代理人核对税额、调整分录和申报期间后提交申报。各期间的应纳税额、缴款及期末结转凭证分别留痕。

两条税额分别为 12 和 8，发票小计为 20，另有一笔 −2 的调整。威尔士语编制界面与英语申报界面应在同一栏显示 18；汇总行不重复计入。

[English](../accounting.md#british-return-aggregation) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/accounting.md#erpnext-united-kingdom).
