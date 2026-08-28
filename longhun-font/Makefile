# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-07-25-LONGHUN-FONT-MAKEFILE-v2.0

VERSION = v0019
GLYPHS = glyphs/龍魂字元库_$(VERSION)_龍纹书法版.json
OTF = output/龙魂字体-Regular.otf
OTF_LEGACY = output/LonghunFont-Regular.otf
WOFF2 = output/龙魂字体-Regular.woff2
SVG_DIR = output/all_glyphs
SAMPLE = output/sample_$(VERSION).html

.PHONY: all build render check optimize release install demo clean

all: optimize render check

build:
	python3 scripts/build_font.py $(GLYPHS) $(OTF_LEGACY)

render:
	python3 scripts/batch_render.py $(GLYPHS) $(SVG_DIR) $(SAMPLE)

check:
	python3 scripts/check_font.py $(GLYPHS)

optimize:
	python3 scripts/rename_and_optimize.py

release:
	./scripts/release.sh $(VERSION)

install:
	./install_macos.sh

demo:
	@echo "用浏览器打开 output/demo.html 或 wuwu_demo.html"

clean:
	rm -rf output/all_glyphs_*
	rm -f output/sample_*.html
	rm -f $(OTF) $(OTF_LEGACY) $(WOFF2)
