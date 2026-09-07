#!/usr/bin/env python3
"""Minimal portable Miaoshou public collect-box client.

This tool intentionally exposes no delete command. Publishing and product claiming
remain separate, explicitly authorized operations.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict:
    path = ROOT / "resources" / "config.json"
    if not path.exists():
        raise SystemExit("Missing resources/config.json; copy resources/config.json.example and configure your own credentials.")
    try:
        config = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid resources/config.json: {exc}") from exc
    missing = [key for key in ("app_key", "app_secret") if not str(config.get(key, "")).strip() or str(config.get(key, "")).startswith("your_")]
    if missing:
        raise SystemExit("Configure " + ", ".join(missing) + " in resources/config.json.")
    return {"base_url": config.get("base_url", "https://openapi-erp.91miaoshou.com").rstrip("/"), "timeout": int(config.get("timeout", 30)), **config}


def post(config: dict, path: str, body: dict) -> dict:
    timestamp = str(int(time.time()))
    payload = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    signed = f"{config['app_secret']}{path}{timestamp}{config['app_key']}{payload}{config['app_secret']}"
    signature = hmac.new(config["app_secret"].encode(), signed.encode(), hashlib.sha256).hexdigest()
    request = Request(
        f"{config['base_url']}{path}", data=payload.encode(), method="POST",
        headers={"Content-Type": "application/json", "x-app-key": config["app_key"], "x-timestamp": timestamp, "x-sign": signature},
    )
    with urlopen(request, timeout=config["timeout"]) as response:
        return json.loads(response.read().decode())


def read_json(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read JSON file {path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Miaoshou common collect-box read/create/edit client")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--keyword", default="")
    listing.add_argument("--page", type=int, default=1)
    listing.add_argument("--size", type=int, default=20)
    detail = commands.add_parser("detail")
    detail.add_argument("--id", required=True, type=int)
    add = commands.add_parser("add")
    add.add_argument("--file", required=True, help="product JSON payload")
    edit = commands.add_parser("edit")
    edit.add_argument("--id", required=True, type=int)
    edit.add_argument("--file", required=True, help="editCommonCollectBoxDetail JSON payload")
    args = parser.parse_args()
    config = load_config()
    prefix = "/open/v1/product/common_collect_box/common_collect_box"
    if args.command == "list":
        body = {"pageNo": args.page, "pageSize": args.size, "filter": {"tabPaneName": "all"}}
        if args.keyword:
            body["filter"]["sourceItemIdKeyword"] = args.keyword
        result = post(config, f"{prefix}/get_common_collect_box_list", body)
    elif args.command == "detail":
        result = post(config, f"{prefix}/get_common_collect_box_detail", {"commonCollectBoxDetailId": args.id})
    elif args.command == "add":
        result = post(config, f"{prefix}/add_common_collect_box_detail", read_json(args.file))
    else:
        current = post(config, f"{prefix}/get_common_collect_box_detail", {"commonCollectBoxDetailId": args.id})
        if current.get("result") != "success":
            print(json.dumps(current, ensure_ascii=False, indent=2))
            return 1
        existing = current.get("data", {}).get("editCommonCollectBoxDetail", {})
        if not isinstance(existing, dict):
            existing = {}
        existing.update(read_json(args.file))
        result = post(
            config,
            f"{prefix}/edit_common_collect_box_detail",
            {
                "commonCollectBoxDetailId": args.id,
                "editCommonCollectBoxDetail": existing,
                "ossMd5": current.get("data", {}).get("ossMd5", ""),
            },
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("result") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
