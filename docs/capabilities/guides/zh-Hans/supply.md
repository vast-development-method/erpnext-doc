# 采购与库存

## 按关联的进口或出口许可证核对每张发票明细，检查剩余数量和金额

<a id="workflow-import-and-export-licence-balances"></a>

将进口发票行关联至许可证，登记 CIF、FOB 金额，过账前分别检查该物料的剩余数量和金额。

许可证还剩 50 千克和 450 个货币单位时，申报进口 40 千克、价值 451 的货物应被拒绝。两项余额保持不变，印地语和英语提示应指向同一许可证并说明超出的是金额。

[English](../supply.md#import-and-export-licence-balances) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/supply.md#advance-authorisation-licence).

## 先模拟采购订单，比较到货量与预计需求，再向供应商下单

<a id="workflow-demand-simulation-before-procurement"></a>

选择预测期，比较库存、预计到货与需求。正式采购前先模拟收货数量和日期。

现有库存为 18 件，需求发生前到货 6 件，需求为 30 件且不接受欠单，预计有 6 件无法售出。模拟再提前到货 10 件后，预计无法售出的数量降至 0，期末剩 4 件；系统不提交采购订单，切换语言也不改变数量和日期。

[English](../supply.md#demand-simulation-before-procurement) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/supply.md#procurementnext).

## 根据抽样方案和记录的缺陷，决定如何处理已检验的批次

<a id="workflow-lot-acceptance-sampling"></a>

按批次抽样方案取样。将批准的批次处置结论应用于收货行，分别记录接收数量和拒收数量。

收货行有 12 件，关联的检验记录已提交且判定为不合格；按批次判定处理后，合格数量为 0，不合格数量为 12。德语和英语报告中的判定代码、样本编号与数量应一致。

[English](../supply.md#lot-acceptance-sampling) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/supply.md#aql-quality-assurance-by-havaratech).

## 根据质量检测结果为每批收购的原奶计价，并核对收奶站的实际到货量

<a id="workflow-milk-collection-and-component-pricing"></a>

依奶类、收奶点和日期选择批准的费率，结合脂肪和非脂乳固体测量值、各成分单价及奶量计算收购金额。

乳脂和非脂乳固体的费率分别为 80 和 30，实测占比分别为 4.0% 和 8.5%，奶量为 100；在不扣款、不加奖的情况下，单价应为 5.75，总价为 575。切换小数分隔符不影响计价，重复收到同一条仪器读数也不能重复记入奶量或应付款。

[English](../supply.md#milk-collection-and-component-pricing) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/supply.md#dairy-management).

## 将销售渠道的商品和仓库映射到相应的 ERP 记录，以便正确处理订单和收货

<a id="workflow-channel-receipt-synchronization"></a>

将渠道商品及地点映射至内部物料和仓库，保留外部收货编号，使重复确认指向同一个库存变动。

仓库两次收到同一笔三件商品的收货完成事件。即使操作员在两次接收之间切换语言，两次回执也应指向同一张收货单，库存只增加三件。

[English](../supply.md#channel-receipt-synchronization) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/supply.md#official-easyecom-integration).

## 完成收货、盘点、拣货、包装和发运，并保留扫描所得的货品、库位和批次标识

<a id="workflow-warehouse-scanning-and-transfers"></a>

在收货、盘点、移库及发货时扫描物料、库位和批次。包装与标签关联到相应货物，不会额外产生库存变动。

货位 A 有 20 件，货位 B 为空。使用南非荷兰语的拣货员调拨两箱，每箱六件。即使扫描器重发同一笔调拨，德语主管仍应看到 A 有 8 件、B 有 12 件。

[English](../supply.md#warehouse-scanning-and-transfers) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/supply.md#wms).
