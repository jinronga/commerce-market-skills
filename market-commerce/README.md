# market-commerce

可分发的电商运营 skill。它把本地图片包、Excel/CSV 货盘映射到妙手 ERP 公共采集箱草稿，并内置库存 `500` 与可追溯的默认定价规则。

## 安装

1. 克隆本仓库，并将 `market-commerce/` 目录安装或复制到 Codex 的 skills 目录。
2. 在该目录中复制配置模板：`cp resources/config.json.example resources/config.json`。
3. 在 `resources/config.json` 填入使用者自己的妙手开放平台 `app_key` 和 `app_secret`。该文件已被 Git 忽略，绝不能提交或共享。
4. 在 Google Chrome 登录 `erp.91miaoshou.com`，并运行 `python3 scripts/check_environment.py`。

## 使用

直接给安装了此 skill 的 Codex 下达“将本地图片包和货盘自动上品到妙手公共采集箱”的任务即可。它会按 `SKILL.md` 中的直接上品模式执行：精选图优先、前 9 张主图、其余详情图、库存 500、创建/更新后回读验证。

定价复算：

```bash
python3 scripts/price_direct_upload.py 2.645
# cost=2.645 multiplier=6.85 price=18.9 stock=500
```

公共采集箱 API（不包含删除、认领或发布）：

```bash
python3 scripts/collectbox_client.py list --keyword HC0540
python3 scripts/collectbox_client.py detail --id 3948039485
python3 scripts/collectbox_client.py add --file product.json
```

## 依赖和边界

- Python 3.10+，无第三方 Python 依赖。
- 妙手 OpenAPI 凭据与已登录 ERP 会话由每位使用者独立提供；它们不能随包迁移。
- 当前随流程提供的浏览器图片上传方法依赖 macOS 上已登录的 Google Chrome。Windows/Linux 使用者需要接入等价的浏览器自动化适配器后才能上传本地图片；已有公开图片 URL 时不受此限制。
- 该 skill 只处理公共采集箱草稿。店铺认领、平台发布、广告投放、删除或覆盖非目标字段仍需要明确授权。
