#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VeshuFont 自動ビルドスクリプト
- リポジトリ内の全 *.svg を読み込み
- ファイル名をそのままリガチャキーにする
- Unicodeは私用領域(PUA)から順に割り当て
- GitHub Actionsで自動実行
"""

import fontforge
import glob
import os
import sys

# ===== 設定 =====
SEARCH_DIR = "."  # 検索開始ディレクトリ
OUTPUT_TTF = "VeshuFont.ttf"
UNICODE_START = 0xE000  # PUA開始位置
BEARING = 50
WIDTH = 1024
# ================

# SVG探索
svg_files = sorted(glob.glob(os.path.join(SEARCH_DIR, "**/*.svg"), recursive=True))
if not svg_files:
    print("❌ SVGが見つかりません")
    sys.exit(1)

# フォント作成
font = fontforge.font()
font.encoding = "UnicodeFull"
font.fontname = "VeshuFont"
font.fullname = "Veshu Font"
font.familyname = "VeshuFont"
font.ascent = 1024
font.descent = 0

# GSUBリガチャ用ルックアップ作成
font.addLookup("liga", "gsub_ligature", (), (("liga", (("latn", ("dflt")),)),))
font.addLookupSubtable("liga", "liga_subtable")

codepoint = UNICODE_START

for svg_file in svg_files:
    # グリフ名（ファイル名）
    glyph_name = os.path.splitext(os.path.basename(svg_file))[0]
    lig_key = tuple(glyph_name)  # 文字列→タプル

    # グリフ作成
    glyph = font.createChar(codepoint, glyph_name)
    glyph.importOutlines(svg_file)
    glyph.left_side_bearing = BEARING
    glyph.right_side_bearing = BEARING
    glyph.width = WIDTH

    # リガチャ登録
    font[glyph_name].addPosSub("liga_subtable", *lig_key)
    print(f"✔ {glyph_name} → リガチャ: {lig_key} (U+{codepoint:04X})")

    codepoint += 1

# フォント保存
font.generate(OUTPUT_TTF)
print(f"✅ フォント生成完了: {OUTPUT_TTF}")
