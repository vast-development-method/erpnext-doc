# 工作区与权限

## 按角色变更权限前，先核对每位用户可访问哪些记录

<a id="workflow-branch-scoped-access-review"></a>

按操作、记录类型和允许的记录值限定权限范围。在应用已批准的变更前预览结果。

两家公司的分支机构都显示为“Central”，用户仅有权查看第一家分支的订单。切换语言后仍只能看到该分支的订单，也不能审批。

[English](../workspace.md#branch-scoped-access-review) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#branchy).

## 用运维人员所选语言的标签和数字格式查看主机的 CPU、内存和磁盘指标

<a id="workflow-system-resource-monitoring"></a>

读取获准主机的处理器、内存和磁盘用量。比较数值时使用采样时间、计量单位及监测范围。

同一份主机采样以英文显示 62.5% 内存使用率，以德文显示 62,5%。除格式和标签以外，内核版本与启动时刻保持一致。

[English](../workspace.md#system-resource-monitoring) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#frappe-system-monitor).

## 跨语言搜索单据，并在英语与阿拉伯语工作台布局之间切换

<a id="workflow-multilingual-workspace-search"></a>

可按本地化标签或允许的别名检索，使用稳定的类型标识打开目标。遵循阅读方向和角色权限。

在两个阿拉伯语工作台上搜索英语名称“Sales Invoice”，一个用户有销售发票访问权限，另一个没有。只有获授权的用户能看到翻译后的结果并打开同一单据类型；标签翻译和书写方向不会增加权限。

[English](../workspace.md#multilingual-workspace-search) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#lumen-theme).

## 在筛选列表旁编辑所选记录，切换界面语言时保留尚未保存的更改

<a id="workflow-split-view-record-editing"></a>

从筛选列表选中一行，在旁边打开获准访问的表单。保存选中记录，返回列表时保留筛选条件。

订单 42 中有尚未保存的阿拉伯语备注。用户切换界面语言后选择订单 43，但在新语言显示的提示框中选择留在当前订单，订单 42 仍被选中，备注原文保留。

[English](../workspace.md#split-view-record-editing) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#pane-view).

## 在获得授权后以另一位用户的身份启动支持会话，并追溯发起人

<a id="workflow-delegated-support-sessions"></a>

授权管理员可在目标用户的账户中启动支持会话。审计日志分别记录操作者和目标用户。系统经理不能以另一位系统经理的身份发起会话。

让获得授权的英语操作员填写原因，以一名使用南非荷兰语的普通用户身份启动支持会话。日志应关联双方的用户标识并保留原因原文；若一名系统管理员尝试以另一名系统管理员的身份登录，无论界面语言如何，系统都应拒绝且不记录目标用户登录成功。

[English](../workspace.md#delegated-support-sessions) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#persona).

## 发布短链接和可扫描的二维码，让读者通过两种方式访问同一目标网址

<a id="workflow-short-links-and-scannable-destinations"></a>

将目标地址绑定到短码，并为同一地址生成可扫描的二维码。访问时重新检查目标与访问策略。

发布一个短链接，目标网址包含经过编码的重音字符和按指定顺序排列的查询参数。在阿拉伯语界面扫码、在德语界面手动输入短链接，两种方式都应使用相同的区分大小写的短码，打开原始编码和参数顺序完全一致的网址。

[English](../workspace.md#short-links-and-scannable-destinations) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#pibicut).

## 为工作区应用品牌主题，并在不同屏幕尺寸和界面语言下使用同一组已授权的快捷入口

<a id="workflow-accessible-workspace-navigation"></a>

为用户应用相应的主题和已授权的快捷入口。键盘、触控及屏幕阅读器导航使用相同目标及权限。

在窄屏上把界面从英语切换为阿拉伯语，并用键盘打开有权访问的快捷入口。焦点应清晰可见，长标签正常换行，入口仍指向同一路由；受限角色在两种语言下都无法进入管理页面。

[English](../workspace.md#accessible-workspace-navigation) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#rukntheme).

## 为表单字段发布帮助内容，并用读者选择的语言同时显示标题和说明

<a id="workflow-translated-field-guidance"></a>

将帮助文本绑定到记录类型中的稳定字段，配置触发方式、位置、语言和显示形式，发布后在实际表单上验证。

将焦点移到一个供应商字段上，该字段有英语默认帮助及审核通过的阿拉伯语标题和正文。选择阿拉伯语时显示完整阿拉伯语帮助；选择南非荷兰语时先回退至完整英语帮助，等该语言译文发布并刷新缓存后再同时切换标题和正文，字段值保持不变。

[English](../workspace.md#translated-field-guidance) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/workspace.md#snd-tooltip).
