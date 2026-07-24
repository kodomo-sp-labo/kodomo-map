# -*- coding: utf-8 -*-
"""
WAMNET 障害児通所系サービスCSV(コード63-67) → 都道府県別 hattatsu.json 変換スクリプト
"""
import csv, json, os
from collections import defaultdict

SOURCE_DIR = "/mnt/user-data/uploads"
OUTPUT_DIR = "/home/claude/wamnet_build/data"

# サービス種別 → catコードの対応（WAMNET CSVコードと1対1）
FILE_TO_CAT = {
    "csvdownload063.csv": "jidou_hattatsu",       # 児童発達支援
    "csvdownload064.csv": "iryo_jidou_hattatsu",  # 医療型児童発達支援
    "csvdownload065.csv": "hokago_day",           # 放課後等デイサービス
    "csvdownload066.csv": "homon_jidou_hattatsu", # 居宅訪問型児童発達支援
    "csvdownload067.csv": "hoikusho_homon",       # 保育所等訪問支援
}

# 全国地方公共団体コード（先頭2桁）→ 都道府県ローマ字フォルダ名
PREF_CODE_TO_ROMAJI = {
    "01":"hokkaido","02":"aomori","03":"iwate","04":"miyagi","05":"akita",
    "06":"yamagata","07":"fukushima","08":"ibaraki","09":"tochigi","10":"gunma",
    "11":"saitama","12":"chiba","13":"tokyo","14":"kanagawa","15":"niigata",
    "16":"toyama","17":"ishikawa","18":"fukui","19":"yamanashi","20":"nagano",
    "21":"gifu","22":"shizuoka","23":"aichi","24":"mie","25":"shiga",
    "26":"kyoto","27":"osaka","28":"hyogo","29":"nara","30":"wakayama",
    "31":"tottori","32":"shimane","33":"okayama","34":"hiroshima","35":"yamaguchi",
    "36":"tokushima","37":"kagawa","38":"ehime","39":"kochi","40":"fukuoka",
    "41":"saga","42":"nagasaki","43":"kumamoto","44":"oita","45":"miyazaki",
    "46":"kagoshima","47":"okinawa",
}

def load_all():
    """5ファイルを読み込み、事業所番号でまとめる"""
    facilities = {}  # 事業所番号 -> facility dict
    for fname, cat in FILE_TO_CAT.items():
        path = os.path.join(SOURCE_DIR, fname)
        with open(path, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                no = row["事業所番号"]
                pref_code5 = row["都道府県コード又は市区町村コード"]
                pref_code2 = pref_code5[:2]
                if no not in facilities:
                    lat = row.get("事業所緯度","").strip()
                    lng = row.get("事業所経度","").strip()
                    facilities[no] = {
                        "n": row["事業所の名称"].strip(),
                        "a": (row.get("事業所住所（市区町村）","").strip()
                              + row.get("事業所住所（番地以降）","").strip()),
                        "t": row.get("事業所電話番号","").strip(),
                        "c": row.get("定員","").strip(),
                        "cat": [],
                        "area": row.get("事業所住所（市区町村）","").strip(),
                        "lat": float(lat) if lat else None,
                        "lng": float(lng) if lng else None,
                        "prec": "address",
                        "pref_code": pref_code2,
                        "src": "wamnet",
                    }
                if cat not in facilities[no]["cat"]:
                    facilities[no]["cat"].append(cat)
    return facilities

def main():
    facilities = load_all()
    print(f"全国ユニーク施設数: {len(facilities)}")

    by_pref = defaultdict(list)
    missing_latlng = 0
    unknown_pref = 0
    for no, fac in facilities.items():
        if fac["lat"] is None or fac["lng"] is None:
            missing_latlng += 1
        pref_romaji = PREF_CODE_TO_ROMAJI.get(fac["pref_code"])
        if not pref_romaji:
            unknown_pref += 1
            continue
        out = {k: v for k, v in fac.items() if k not in ("pref_code",)}
        by_pref[pref_romaji].append(out)

    print(f"緯度経度欠損: {missing_latlng}件")
    print(f"都道府県コード不明で除外: {unknown_pref}件")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_written = 0
    for pref, items in sorted(by_pref.items()):
        outpath = os.path.join(OUTPUT_DIR, pref, "hattatsu_wamnet.json")
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=0)
        total_written += len(items)
        print(f"{pref}: {len(items)}件 → {outpath}")

    print()
    print(f"合計出力件数: {total_written}")

if __name__ == "__main__":
    main()
