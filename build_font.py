#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fontforge
import glob
import os
import sys

SEARCH_DIR = "."
OUTPUT_TTF = "VeshuFont.ttf"
UNICODE_START = 0xE000
BEARING = 50
WIDTH = 1024

svg_files = sorted(glob.glob(os.path.join(SEARCH_DIR, "**/*.svg"), recursive=True))
if not svg_files:
    print("❌ SVGが見つかりません")
    sys.exit(1)

font = fontforge.font()
font.encoding = "UnicodeFull"
font.fontname = "VeshuFont"
font.fullname = "Veshu Font"
font.familyname = "VeshuFont"
font.ascent = 1024
font.descent = 0

font.addLookup("liga", "gsub_ligature", (), (("liga", (("latn", ("dflt")),)),))
font.addLookupSubtable("liga", "liga_subtable")

codepoint = UNICODE_START

for svg_file in svg_files:
    glyph_name = os.path.splitext(os.path.basename(svg_file))[0]
    lig_key = tuple(glyph_name)

    glyph = font.createChar(codepoint, glyph_name)
    glyph.importOutlines(svg_file)
    glyph.left_side_bearing = BEARING
    glyph.right_side_bearing = BEARING
    glyph.width = WIDTH

    if len(lig_key) > 1:  # 複数文字の場合のみリガチャ設定
        font[glyph_name].addPosSub("liga_subtable", lig_key)
        print(f"✔ {glyph_name} → リガチャ: {lig_key} (U+{codepoint:04X})")
    else:
        print(f"→ {glyph_name} 単文字 (U+{codepoint:04X})")

    codepoint += 1

font.generate(OUTPUT_TTF)
print(f"✅ フォント生成完了: {OUTPUT_TTF}")
