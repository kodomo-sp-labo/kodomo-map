# こども支援資源マップ

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22004201.svg)](https://doi.org/10.5281/zenodo.22004201)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ja)

不登校・発達支援等に関する**公的な支援資源**（学びの多様化学校、教育支援センター、こどもの居場所、教育相談窓口、地域子育て支援拠点、児童発達支援・放課後等デイサービス等）を、地図上で探せるようにした静的ウェブサイトです。社会的処方（social prescribing）の考え方に基づき、こども・保護者・支援者が「地域にどんな資源があるか」を一目で把握できることを目的とした、非営利の取り組みです。

- **サイト**: https://kodomo-sp-labo.github.io/kodomo-map/
- **困りごとから探す**: https://kodomo-sp-labo.github.io/kodomo-map/concerns.html
- **運営**: こどもウェルビーイングlabo（松本尚美・岡山大学）
- **連絡先**: kodomo.sp.lab@gmail.com（掲載のご希望・掲載情報の訂正・自治体等からの公式データのご提供）

## 収録内容

地図は次の5つのタブと、背景レイヤーとしての小学校区界で構成されています。

| タブ | 内容 | 主な出典 |
|---|---|---|
| ①学び・出席扱い系 | 学びの多様化学校（不登校特例校）、教育支援センター、フリースクール等 | 文部科学省、都道府県・市町村の公表資料 |
| ②居場所系 | 児童館・児童遊園、子ども食堂・プレーパーク等のこどもの居場所 | 国土数値情報（P14）、都道府県・市町村・社会福祉協議会の公表資料 |
| ③相談・伴走系 | 市区町村の教育相談・子育て相談等の窓口 | こども家庭庁の公表資料 |
| ④親・家族支援系 | 地域子育て支援拠点、親の会 等 | 都道府県の公表資料、独自調査 |
| ⑤発達・医療連携系 | 児童発達支援・放課後等デイサービス等の障害児通所支援事業所 | WAM NET（独立行政法人福祉医療機構） |
| 小学校区界 | 小学校の通学区域ポリゴン | 国土数値情報（A27） |

対応地域は都道府県単位で順次拡大しています。現在の対応状況・各データの件数・出典と確認日は、サイト上の地域選択とフッターの出典表示（`sources.json` から自動生成）をご確認ください。本READMEには変動する数値を記載していません。

## データの考え方

- **公的一次資料主義**: 出典は国・都道府県・市区町村・公的機関の公表資料に限定し、民間の集約サイトは使いません。
- **推測で埋めない**: 取得できなかった住所・座標・電話番号等は `null` のままにし、「それらしく」補完することはしません。
- **精度の明示**: 座標が市区町村レベルの概算であるものには `prec: "area"` を付け、番地精度を主張しません。
- **出典と確認日の保持**: 各レコードは出典ID（`src`）を持ち、出典のラベル・URL・確認日は `sources.json`（出典台帳）で一元管理しています。
- **利用条件の記録**: 出典ごとに利用条件（ライセンス、出典表示・編集加工表示の要否、確認日）を `sources.json` に記録し、条件上収録できなかった自治体は「収録できなかった」ことを明示します（推測で穴埋めしない）。
- **編集・加工の明示**: 本サイトのデータはすべて、原資料からの抽出・都道府県別への分割・座標の付与・図形の簡略化等の編集・加工を経ています。この事実と加工主体はフッターの出典表示に明記しています。

## リポジトリ構成

```
index.html                 地図本体（単一ページアプリケーション）
concerns.html              困りごとから資源を探すページ
kodomo-concerns.json       困りごと→資源の対応データ
parent_guide_*.html        保護者向けガイド（不登校・発達）
data/<都道府県コード>_<ローマ字>/   都道府県別データ（例: data/33_okayama/）
  manabi.json              ①学び・出席扱い系
  ibasho.json              ②居場所（子ども食堂・プレーパーク等）
  jidoukan.json            ②居場所／④親家族（児童館・児童遊園）
  sodan.json               ③相談・伴走系（市区町村の相談窓口）
  kyoten.json              ④親家族（地域子育て支援拠点）
  oyanokai.json            ④親家族（親の会）
  hattatsu.json            ⑤発達・医療連携系（障害児通所支援事業所）
  districts.json           小学校区界（GeoJSON）
sources.json               出典台帳（出典ID・URL・確認日・利用条件・データセット定義）
vendor/qrcode-generator/   QRコード生成ライブラリ（MIT License、同梱）
CITATION.cff               引用情報
LICENSE                    ライセンス
CLAUDE.md                  データ収集・更新の運用ルール（AIコーディングアシスタント用の作業規範）
```

データ収集・変換に用いたスクリプトや中間ファイルは、公開サイトに不要なためこのリポジトリには含めていません。

## ライセンス

本リポジトリのコンテンツ（コード、統合・編集されたデータ、文章等）は、特に注記がない限り [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ja) の下で提供します（詳細は [LICENSE](LICENSE)）。このライセンスは、出典資料を選定・統合・検証・実装した**編集物としての本サイト・本リポジトリ**に適用されるものです。

個別の出典データ（文部科学省・こども家庭庁・国土数値情報・WAM NET・各自治体の公表資料等）の利用条件は、それぞれの原典に従います。出典ごとの利用条件は `sources.json` の各出典エントリ（`license` / `license_url` / `credit` / `modified_note` / `terms_checked`）に記録しています。同梱の `vendor/qrcode-generator` は MIT License です。

## 引用

本サイト・データを研究等で利用・参照される場合は、以下のように引用してください（GitHubの「Cite this repository」からも取得できます。書式は [CITATION.cff](CITATION.cff) を参照）。

> 松本尚美 (2026). こども支援資源マップ [Software/Data]. Zenodo. https://doi.org/10.5281/zenodo.22004201

上記のDOIは全バージョン共通のもので、常に最新版に解決されます。特定のバージョンを引用する場合は、Zenodoの各バージョンのDOIをご利用ください。

## 制作について

収録データは公的一次資料に基づき、松本尚美（岡山大学）が出典確認・分類・検証を行いました。実装にはAIコーディングアシスタント（Claude Code）を使用しています。運用上の判断基準は [CLAUDE.md](CLAUDE.md) に記録しています。

## 免責事項

本サイトの情報は公的機関の公表資料に基づいていますが、公表後の変更（廃止・移転・名称変更等）が反映されていない場合があります。実際に利用される際は、必ず各機関・施設に直接ご確認ください。本サイトの利用により生じた損害について、運営者は責任を負いません。

---

## English summary

**Kodomo Support Resource Map** is a static web application (GitHub Pages) that visualises publicly provided support resources for children in Japan—particularly around school non-attendance (*futoko*) and developmental support—on an interactive map: alternative and support schools, children's places (*ibasho*), municipal counselling desks, community parenting hubs, and developmental support services. It is a non-profit project grounded in the idea of social prescribing.

All records derive from primary sources published by national or local government bodies (MEXT, the Children and Families Agency, the National Land Numerical Information, WAM NET, prefectures and municipalities). Missing values are left as `null` rather than inferred; coordinate precision is flagged explicitly; and every record carries a source identifier resolved through `sources.json`, which also records the licence terms of each source and the fact that the data have been edited and processed. The compilation is licensed under CC BY-NC-ND 4.0; individual sources retain their own terms. Data curation and verification were performed by Naomi Matsumoto (Okayama University); an AI coding assistant (Claude Code) was used for implementation.
