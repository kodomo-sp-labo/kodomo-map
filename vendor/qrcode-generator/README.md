# qrcode-generator（ベンダリング）

- 取得元: https://github.com/kazuhikoarase/qrcode-generator （`js/dist/qrcode.js`）
- ライセンス: MIT（`LICENSE`参照）
- 取得日: 2026-07-27
- 用途: `concerns.html` の印刷面で、地図へのディープリンクをQRコードに変換するため。
- 外部CDNを使わず本リポジトリに同梱し、実行時に外部へ通信しない方針
  （CLAUDE.md・利用者のプライバシー方針に合わせるため）。
- UTF-8拡張（`qrcode_UTF8.js`）は同梱していない。QRに変換するのは自サイトの
  URL（ASCII文字のみ）に限定しているため不要。
