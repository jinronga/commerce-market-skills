---
name: market-commerce
description: 电商运营总 skill，聚合图片上传、商品写回、类目匹配、采集、认领、发布、铺货编排等能力。用户要求把本地商品包、图片包、Excel 货盘或图片映射自动上到妙手 ERP / 公共采集箱时，也必须使用本 skill：资料齐全时采用已验证的直接上品流程，不要求用户在图片、定价、库存和创建之间反复确认。支持妙手及后续更多类似渠道。
compatibility: Python 3.10+；妙手开放平台 AppKey/AppSecret；图片上传需已登录妙手 ERP 的 Google Chrome 会话（内置流程目前支持 macOS Chrome）
---

# Market Commerce

电商运营能力聚合 skill，不局限于文件上传。

## 能力范围

- 商品采集与来源导入
- 公共采集箱查询、创建、编辑、删除
- 商品认领到目标渠道/店铺
- 店铺/仓库查询
- 图片清理、映射与写回
- 类目匹配
- 商品编辑、标题/详情/SKU/价格/图片维护
- 发布与上架
- 端到端铺货编排

## 输入

- 商品或图片包
- 商品映射关系
- 目标渠道 / 站点 / 店铺 / 采集箱
- 运营动作，例如采集、认领、编辑、发布、图片上传绑定、铺货

## 输出

- 运营结果摘要
- 商品状态
- 下一步建议

## 流程

1. 理解用户运营目标
2. 选择对应能力
3. 执行采集、认领、编辑、发布、图片绑定、铺货等操作
4. 根据请求选择“常规操作”或“本地包直接上品”模式
5. 回读实时结果并汇总商品状态

## 本地包直接上品模式

当用户明确要求“自动上品”“将本地图片包/货盘映射到 ERP”“上传到公共采集箱”或同义指令时，直接执行，不在以下已确定步骤之间反复索要确认：图片上传、定价、库存、创建公共采集箱记录、回读校验。用户的目标是获得可用草稿，不是逐项审阅执行细节。

适用于：本地图片包 + 货盘（Excel/CSV）+ 已登录妙手 Chrome 会话，或已有公开图片 URL。完整操作见 `references/miaoshou-local-pack-direct-upload.md`。

首次在新设备或交给新使用者时，先阅读 `README.md`，复制 `resources/config.json.example` 为本地 `resources/config.json`（该文件不会纳入版本控制），填写其本人妙手开放平台凭据，并运行 `python3 scripts/check_environment.py`。定价可用 `scripts/price_direct_upload.py` 复算；公共采集箱的查询、创建、编辑可用 `scripts/collectbox_client.py`。不要依赖本机其他未打包目录。

执行时：

1. 从货盘提取货号、品名、容量/规格、成本与可用物流字段；从图片目录按货号匹配。优先 `images/` 等已整理目录，不把原始包里重复、临时或未审查的图混入商品。
2. 查询公共采集箱，以货号判断是编辑已有记录还是创建新记录。已有记录只合并目标字段，绝不因补图覆盖 SKU、货源或其他已存在字段。
3. 通过已登录的妙手 Chrome 同源上传接口把本地图片上传为公开 URL；按目录或映射将前 9 张作为主图，其余作为详情图。保存每张返回 URL 和货号映射，失败时只重试失败图。
4. 为缺少价格和库存的新单品设置可追溯的默认值：库存 `500`；价格优先采用同品牌、同货盘或同类目中已验证商品的“ERP 价 / 货源成本”倍率，并向上取心理价尾数。若没有可比锚点，使用 `6.85x` 成本、向上取 `.9` 作为公共采集箱测试价，并将规则写入商品属性。这个价格是草稿测试价，不等于店铺最终售价。
5. 创建时写入完整可用字段：标题、货号、价格、库存、主图、详情图、来源属性和人工来源标识。不要虚构认证、仓库、包裹尺寸、SKU 或功效宣称。
6. 对每条创建或编辑结果重新查询实时详情，验证货号、价格、库存、主图数、详情图数以及图片是否属于对应商品。只在缺少图片映射、鉴权、货号冲突或 API 不可恢复错误时停止并说明原因。

直接上品模式只创建或更新妙手公共采集箱草稿。认领到店铺、修改平台商品、对外发布和广告投放仍须单独获得用户明确授权。

## 安全规则

- 常规写操作先确认；明确的本地包直接上品请求按上述流程执行，不重复确认中间步骤
- 店铺认领、平台发布、广告投放、删除和覆盖已有非目标字段必须确认
- 密钥不能放在对话里
- 不臆造销量、佣金、仓库、认证等数据

## 参考资料

- `references/source-import.md`
- `references/common-collectbox-manage.md`
- `references/product-claim.md`
- `references/shop-query.md`
- `references/tiktok-category-recommend.md`
- `references/tiktok-product-edit.md`
- `references/tiktok-product-publish.md`
- `references/image-sanitize-and-mapping.md`
- `references/tiktok-listing-pipeline.md`
- `references/miaoshou-local-pack-direct-upload.md`
- `README.md`
