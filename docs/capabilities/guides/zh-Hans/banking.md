# 银行与资金管理

## 跟踪每张支票从收取或签发到兑付或退票的过程，并与会计分录和银行流水核对

<a id="workflow-cheque-approval-and-collection"></a>

根据收款记录生成客户支票，用存款单汇集可存入的支票，再将银行结果与对应的支票和凭证匹配。

审批门槛为 1,000 时，金额恰好为 1,000 的支票提交后，在新会话中应仍为待审批，且尚无会计分录。会计经理批准后只生成一笔分录，阿拉伯语和英语凭证引用同一支票号码、审批记录和金额。

[English](../banking.md#cheque-approval-and-collection) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#cheque).

## 通过 支付服务商 收取销售发票款项，并用已确认的付款核销该发票的未结余额

<a id="workflow-saved-payment-method-collections"></a>

按发票币种使用客户授权保存的支付方式发起收款。确认后将收款分配至未结发票，并保留支付服务商的交易编号。

法语付款人对一张尚欠 40 欧元的英语发票重复提交同一笔收款请求，再重复处理支付服务商的成功事件。只能扣款并核销一次 40 欧元，发票余额归零；收据语言不会改变付款人、商户、支付参考号、币种或金额。

[English](../banking.md#saved-payment-method-collections) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#ipconnex-stripe-payment).

## 跟踪远期支票从收取或签发到存入银行、结清或退票的全过程

<a id="workflow-post-dated-cheque-settlement"></a>

将支票记入对应的过渡账户。交存时生成银行凭证，兑现后在同一凭证上登记清算日期。

用支票 00072 核销一张金额为 400.00 的客户发票，存入银行后以相同参考号确认两次。银行余额只增加 400.00，过渡账户归零，德语和南非荷兰语界面显示相同的支票号及凭证号。

[English](../banking.md#post-dated-cheque-settlement) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#pdc-cheque-management).

## 导入波斯尼亚和黑塞哥维那 银行的 CSV 对账单，并在对账前核查重复的交易参考号

<a id="workflow-bank-statement-import-and-duplicate-review"></a>

按银行的 CSV 格式预览日期、存入、支出、参考号和摘要。先审核重复参考号，再将通过的流水用于对账。

把参考号 00038、金额写作 1.234,50 的银行交易导入两次，再导入同一参考号但金额为 1.234,55 的记录。系统只登记一笔交易，标明重复项，并将金额冲突交给人工复核；切换界面语言不会改变小数解析规则或参考号的前导零。

[English](../banking.md#bank-statement-import-and-duplicate-review) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#procredit-bank-statement-processing).

## 在资金台账中登记现金或支票收付款，并查看与特定交易方关联的记录

<a id="workflow-treasury-transaction-register"></a>

按支付方式设置应收及应付账户。资金登记可直接录入账户行，也可选择往来方，将款项分配到其未结发票。

在同一资金台账中登记一笔关联交易方的现金收入 250.00，以及一笔未关联交易方的现金支出 75.00。无论使用德语还是南非荷兰语，台账净增加额都是 175.00；筛选关联交易方的记录后只显示 250.00 的收入。

[English](../banking.md#treasury-transaction-register) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#treasury-entry).

## 授权通过 银行批量支付供应商款项，并逐笔核对银行回执

<a id="workflow-supplier-payment-batch-authorization"></a>

选取供应商付款记录，用一次性验证码授权批次。分别跟踪每条付款指令的银行参考号和处理结果。

一批两笔已获批准的供应商付款收到银行回执，其中一笔确认、一笔被拒；将该回执处理两次。已付款供应商只收到一份德语付款通知，另一笔仍未付；印地语操作员和英语审批人看到相同的银行参考号和拒付原因原文。

[English](../banking.md#supplier-payment-batch-authorization) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#sanpra-easypay).

## 通过线上结账、已配对的终端或定期付款请求收款，并将收款结果与发票核对

<a id="workflow-online-and-terminal-payment-collection"></a>

商户获批后为各种支付方式配置收款路径。支付请求可使用线上收银台、已授权的重复扣款或已登记的终端。

一名使用法语的付款人结清一张 35.70 欧元的发票。支付平台重复发送成功通知时，系统只核销一次；使用德语的收银员看到的是同一张已结清的发票。

[English](../banking.md#online-and-terminal-payment-collection) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/banking.md#stripe2-payment-integration).
