# 文件与签署

## 筛选需要打印的记录，按所选字段分组，将 PDF 文件打包为 ZIP 下载

<a id="workflow-bulk-document-rendition"></a>

选定记录类型、筛选条件、打印格式和分组。将成功生成的 PDF 打包，逐份记录生成失败的单据。

55 份有权访问的单据跨越多个结果页，其中 1 份生成 PDF 失败；任务应报告部分成功，交付 54 份 PDF，并在清单中列出失败单据的编号。清单应记录每份 PDF 的语言，不同分组也不能因 Unicode 名称相似而合并。

[English](../documents.md#bulk-document-rendition) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/documents.md#dynamic-bulk-pdf-downloader).

## 跟踪单据的各个里程碑，并统计相邻里程碑之间的耗时

<a id="workflow-milestone-progress-measurement"></a>

定义日期字段、里程碑、条件和进度值。单据达到里程碑时记录转换时间及操作者。

单据在 UTC 08:00 获批，并于当天 UTC 15:03 标记为已交付；在绝对进度规则下，当前进度应为 100%，间隔为 423 分钟。重复处理交付事件不应增加日志，翻译里程碑名称也不改变耗时。

[English](../documents.md#milestone-progress-measurement) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/documents.md#document-progress-tracker).

## 为单据指定签署人，并将签署后的 PDF 原样发送给收件人

<a id="workflow-signed-document-dispatch"></a>

将授权签署人关联到发票。已签名文件使用独立标识，可再次下载或作为附件发送。

用两种语言分别发送同一份已签名的德语发票时，两封邮件所附文件的摘要都应与归档的已签名 PDF 一致。邮件语言不改变文件内容或签署人，也不触发再次签名。

[English](../documents.md#signed-document-dispatch) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/documents.md#digital-signature).

## 为每位签署人分配填写字段，并保留协议签署时的语言和内容

<a id="workflow-multiple-signer-agreement-completion"></a>

根据模板创建协议，为接收人分配待填字段。分别记录拒签及原因、签署完成和最终文件签名。

两位签署人分别使用德语和英语界面签署同一份南非荷兰语协议。各自完成指定字段后，系统只生成一份最终文件，记录两项签署任务及同一协议摘要值。

[English](../documents.md#multiple-signer-agreement-completion) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/documents.md#esign-app).

## 设计双语发票，预览 PDF，并按收件人偏好的语言发送

<a id="workflow-bilingual-document-layout"></a>

将版式绑定到单据字段并检查预览。签发 PDF 前选定已批准的单语或双语格式。

一名使用英语界面的职员通过阿拉伯语和英语双语模板打印发票，客户姓名包含两种文字，另有两行税额。两种语言的标题均正确显示，两行税额与入账金额一致，扫描二维码得到原始签名数据。

[English](../documents.md#bilingual-document-layout) · [来源说明](../../../rebuild/marketplace-guides/editions/zh-Hans/documents.md#lumenpdf-studio).
