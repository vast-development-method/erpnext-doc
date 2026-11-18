# 销售与客户管理

## 用选定的联系人创建电话营销活动，核对禁呼名单，再把可拨打的电话分配给坐席

<a id="workflow-calling-campaigns-and-contact-suppression"></a>

筛选联系人并向坐席分配呼叫顺序，将处置结果、获准保留的录音及可计费服务归入活动。

联系人在入选活动后、分配呼叫前将号码加入禁呼名单。即使改用另一种语言的话术，也应阻止拨号，不向服务商发起呼叫，也不产生计费记录。

[English](../sales.md#calling-campaigns-and-contact-suppression) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#b2b-marketing).

## 根据条件安排跟进任务，并以负责人的语言发送到期提醒

<a id="workflow-business-calendar-follow-up"></a>

将每次提醒与发票、负责人及跟进日期关联，将客户承诺的付款与实际到账核对。

报价单在周五 09:00 发出，规定两个工作日后跟进，期间没有节假日。使用南非荷兰语和德语的用户看到的是同一项任务，截止时间均为温得和克时间周二 09:00。

[English](../sales.md#business-calendar-follow-up) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#follow-up).

## 导入 交易平台 询盘，跟踪其状态，并将选定的询盘转为销售线索

<a id="workflow-marketplace-inquiry-conversion"></a>

按计划或指定时间段抓取询盘。重叠抓取范围内依据外部询盘标识识别重复，并只创建一次线索。

让定时同步和历史补录同时覆盖卖家 A 的询盘 INQ-47，再用两种界面语言各执行一次线索转换。系统只保存一条询盘，两次返回同一销售线索编号，商品的印地语名称和来源编号保持不变。

[English](../sales.md#marketplace-inquiry-conversion) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#erpnext-indiamart-integration).

## 从汇总面板查看客户订单或向供应商采购的总额，并下钻到原始单据

<a id="workflow-party-order-dashboard"></a>

选择公司、往来方和期间，按各类单据适用日期统计已提交记录，并按币种查看金额及其明细。

某客户有两张可见的已提交订单，合计 140 欧元，另有一张草稿。在相同日期筛选条件下打开订单统计，结果应为 2 张、140 欧元；切换界面语言后，下钻仍只显示原来的两个订单编号。

[English](../sales.md#party-order-dashboard) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#insightly).

## 管理同一桌分次送往厨房的点单，并在门店收银台结算最终账单

<a id="workflow-restaurant-orders-and-kitchen-rounds"></a>

同一餐桌订单可保持开启并分轮下厨。免费附加项作为备注，收费附加项单列计价。

点一份价格为 60 的菜，加一项收费 5 的配料和一条免费厨房备注；使用相同发送编号重复派单后结账。只能生成一张厨房单和一张税前合计 65 的销售点发票；阿拉伯语厨房界面和英语收银界面使用相同的选项编号和行金额。

[English](../sales.md#restaurant-orders-and-kitchen-rounds) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#lumen-restaurants).

## 使用收银员的语言完成当班收银，并在网络恢复后核对排队等待上传的销售记录

<a id="workflow-offline-till-sales"></a>

开班后扫描商品并收款。离线销售在服务器确认前保留于队列中，交班前处理全部待同步项目。

收银员在阿拉伯语界面离线售出两件商品后切换到德语。上传确认丢失后重试，系统仅生成一张发票和一笔数量为二的库存变动，德语状态显示该发票号，收据仍保留原来的语言。

[English](../sales.md#offline-till-sales) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#lumenpos).

## 向 开放商务 网络发布卖家商品目录，并将买方确认与 ERP 订单核对

<a id="workflow-open-commerce-order-confirmations"></a>

卖家通过 ONDC 网络提供商品或服务。可处理的消息由实际采用的零售协议决定。

英语和印地语目录使用同一商品编号。操作员切换语言后，网络重复发送同一笔两件商品的确认时，系统返回原结果，仅一张订单预留两件商品。

报价为两件商品，每件 120，另加运费 30。一次有效确认生成金额 270 的订单并预留两件。重复回调沿用原标识。同一消息键若改为三件，须标记冲突，订单与预留数量均保持原值。

[English](../sales.md#open-commerce-order-confirmations) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#ondc-seller-app).

## 扫描带序列号或批号的商品，办理销售或退货，并在交班时按付款方式对账

<a id="workflow-retail-shift-settlement"></a>

按支付方式登记开班金额和销售款。结班时将实点金额与计入退款后的预期金额核对。

交班前，现金期初为 100.00，收到现金 200.00、刷卡款 50.00，并以现金退款 30.00。若实点现金为 268.00、卡款为 50.00，阿拉伯语和英语界面均应显示应有现金 270.00、现金短少 2.00、卡款差额为零。

[English](../sales.md#retail-shift-settlement) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#retail-suite).

## 把同一桌的餐饮订单分送厨房和吧台，并按该次就餐记录结账

<a id="workflow-restaurant-multi-station-fulfilment"></a>

将订单归入餐桌，按品类分派到各制作工位，厨房及吧台小票关联到同一账单。

同一桌客人用尼泊尔语点两份相同菜品和一杯饮料，再用同一提交标识重发订单。英语厨房应只收到两份菜品，德语吧台只收到一杯饮料；账单恰有三件，商品编码与原单一致。

[English](../sales.md#restaurant-multi-station-fulfilment) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#sajha-menu).

## 用收件人的语言审阅助手拟写的报价提醒，并在发送前批准最终文本

<a id="workflow-reviewed-sales-reminders"></a>

只读取有权访问的报价、订单和发票。复核拟采取的跟进操作，分别记录批准与执行。

让使用德语的经理先预演发给南非荷兰语客户的报价提醒，再批准面向收件人的确切措辞。预演不发送任何消息，重复运行调度也只投递一次已批准的提醒，之后修改措辞必须重新审批。

[English](../sales.md#reviewed-sales-reminders) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/sales.md#sales-ai).
