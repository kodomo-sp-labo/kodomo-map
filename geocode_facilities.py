#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
療育施設393件を番地レベルでジオコーディングするスクリプト。

方法：国土地理院（GSI）の住所検索API（無料・APIキー不要・国の公式データ）を使用。
  https://msearch.gsi.go.jp/address-search/AddressSearch?q=<住所>
公式サービスなので信頼性が高く、街区レベル位置参照情報や住居表示住所を基にした
ジオコーダーです。Google Places のような「店舗検索」ではなく「住所→座標」に
特化しているため、この用途（施設名で引っかからない小規模事業所の住所を
そのまま座標化する）に向いています。

前提：
  pip install requests

使い方：
  python3 geocode_facilities.py

入力：ryoiku_facilities_393.csv（同じフォルダに置いてください）
出力：ryoiku_facilities_geocoded.csv（lat, lng, 状態を追加したもの）

このスクリプトは Claude の実行環境（サンドボックス）からは
msearch.gsi.go.jp にネットワークアクセスできないため実行できません。
先生のPC（またはネット接続のある環境）で実行してください。
"""

import csv
import re
import sys
import time
import unicodedata
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("requests が必要です。先に `pip install requests` を実行してください。")

INPUT_CSV = "ryoiku_facilities_393.csv"
OUTPUT_CSV = "ryoiku_facilities_geocoded.csv"
GSI_URL = "https://msearch.gsi.go.jp/address-search/AddressSearch"
SLEEP_SEC = 0.5          # 1リクエストごとの待機（サーバへの配慮。短くしすぎない）
TIMEOUT_SEC = 10
MAX_RETRIES = 3


def normalize_address(addr: str) -> str:
    """全角数字・記号を半角化し、GSIが認識しやすい形に整える。"""
    a = unicodedata.normalize("NFKC", addr)  # 全角数字→半角、全角ハイフン等も正規化
    a = a.replace("番地", "-").replace("番", "-").replace("号", "")
    a = re.sub(r"\s+", "", a)
    return a


def strip_building_info(addr: str) -> str:
    """
    ビル名・部屋番号などを落として再検索するためのフォールバック。
    例:「...１丁目２－１３メゾン旭１０１」→「...１丁目２－１３」
    最後の「-数字」または「番地」までを残し、それ以降のカタカナ/漢字ビル名を削る。
    完全ではないが、GSIでヒットしない場合の再試行用。
    """
    # 数字の後にカタカナ・漢字・アルファベットが続くパターンで切る
    m = re.search(r"(\d+(-\d+)*)[^\d\-]+$", addr)
    if m:
        return addr[: m.end(1)]
    return addr


def geocode(query: str):
    """GSI住所検索APIを叩いて (lat, lng, matched_title, n_results) を返す。ヒットなしは None。"""
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(GSI_URL, params={"q": query}, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            data = resp.json()
            if data:
                # 先頭が最も一致度の高い候補（GSIは適合順で返す）
                lng, lat = data[0]["geometry"]["coordinates"]
                title = data[0]["properties"].get("title", "")
                return lat, lng, title, len(data)
            return None
        except requests.RequestException:
            time.sleep(1.5 * (attempt + 1))
    return None


def main():
    in_path = Path(INPUT_CSV)
    if not in_path.exists():
        sys.exit(f"{INPUT_CSV} が見つかりません。CSVを同じフォルダに置いてください。")

    # 途中再開に対応：出力ファイルがあれば既にジオコード済みの行をスキップ
    done = {}
    out_path = Path(OUTPUT_CSV)
    if out_path.exists():
        with out_path.open(encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if row.get("geocode_status") in ("matched", "matched_fallback"):
                    done[row["name"] + "|" + row["postal"]] = row

    with in_path.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    fieldnames = list(rows[0].keys()) + [
        "geocode_query", "geocode_status", "lat", "lng", "matched_title", "n_candidates"
    ]

    results = []
    for i, row in enumerate(rows, 1):
        key = row["name"] + "|" + row["postal"]
        if key in done:
            results.append(done[key])
            continue

        query = normalize_address(row["full_address"])
        print(f"[{i}/{len(rows)}] {row['name']} -> {query}")

        hit = geocode(query)
        status = "matched"
        if hit is None:
            # フォールバック：ビル名・部屋番号を落として再試行
            fallback_query = strip_building_info(query)
            if fallback_query != query:
                time.sleep(SLEEP_SEC)
                hit = geocode(fallback_query)
                status = "matched_fallback"

        if hit is None:
            row.update({
                "geocode_query": query, "geocode_status": "no_match",
                "lat": "", "lng": "", "matched_title": "", "n_candidates": 0,
            })
        else:
            lat, lng, title, n = hit
            row.update({
                "geocode_query": query, "geocode_status": status,
                "lat": lat, "lng": lng, "matched_title": title, "n_candidates": n,
            })

        results.append(row)
        time.sleep(SLEEP_SEC)

        # 20件ごとに途中経過を保存（中断してもやり直しやすいように）
        if i % 20 == 0:
            with out_path.open("w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()
                w.writerows(results)

    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(results)

    matched = sum(1 for r in results if r["geocode_status"] in ("matched", "matched_fallback"))
    print(f"\n完了: {matched}/{len(results)} 件が番地レベルでマッチしました。")
    print(f"出力: {OUTPUT_CSV}")
    print("no_match の行は matched_title が空欄です。目視で個別確認してください。")


if __name__ == "__main__":
    main()
