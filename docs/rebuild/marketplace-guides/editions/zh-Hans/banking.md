# 支付与银行业务

[English](../en/banking.md) · [Afrikaans](../af/banking.md) · [Deutsch](../de/banking.md) · 简体中文

[全部主题](README.md)

## cheque

提交收款凭证后生成客户支票，再用送存单把符合条件的支票合并送交银行。查阅到的对账代码先按参考号查找已送存的支票，并确认有关联的会计分录，之后才记录收妥或退票。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-cheque-approval-and-collection) · [来源说明](../../apps/cheque.md)

## IPCONNEX Stripe Payment

产品条目说明，配置 Stripe 和客户付款资料后，销售发票上即可使用付款操作。历史公开副本使用客户保存的付款方式和发票币种，向 Stripe 请求创建 PaymentIntent，并生成分配到该发票的客户付款记录；此处描述的是代码路径，未验证实际部署中的到账结果。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-saved-payment-method-collections) · [来源说明](../../apps/ipconnex_stripe_payment.md)

## PDC Cheque Management

据发布者介绍，收取客户支票或向供应商签发支票时，系统会通过相应的过渡账户生成付款或收款凭证。在一份注明发布者信息的公开代码副本中，存入银行时生成银行日记账凭证，结清时再将清算日期记入该凭证。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-post-dated-cheque-settlement) · [来源说明](../../apps/pdc_cheque_management.md)

## ProCredit Bank Statement Processing

据发布者介绍，导入波斯尼亚和黑塞哥维那 ProCredit 银行的 CSV 对账单时，系统会检查重复参考号。发布者的截图先显示日期、存入金额、支取金额、参考号和说明的导入预览，随后显示尚未对账的银行交易。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-bank-statement-import-and-duplicate-review) · [来源说明](../../apps/procreditbank.md)

## Treasury Entry

发布者的截图显示，在资金台账中，每种付款方式分别配置应付账户和应收账户。登记资金流水时，经办人可以逐行输入账户和金额，也可以选择按交易方登记，调取未结清发票并填写每笔发票的核销金额。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-treasury-transaction-register) · [来源说明](../../apps/safe_entry.md)

## Sanpra Easypay

商品说明列出通过 ICICI 银行办理收款和付款的功能。对于供应商付款，发布者介绍了调取付款凭证、通过一次性密码授权批量支付及跟踪银行交易状态的流程，并明确列出 RTGS 和 NEFT 两种转账方式。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-supplier-payment-batch-authorization) · [来源说明](../../apps/sanpra_easypay.md)

## Stripe2 Payment Integration

公司联系人验证邮箱并授权 Stripe 账户后，商户设置线上和线下支付方式。已提交的付款请求可以打开在线收银台，定期收款可使用已保存的付款方式，收银员也可使用已注册的终端。

[工作流程与验收案例](../../../../capabilities/guides/zh-Hans/banking.md#workflow-online-and-terminal-payment-collection) · [来源说明](../../apps/stripe2.md)
