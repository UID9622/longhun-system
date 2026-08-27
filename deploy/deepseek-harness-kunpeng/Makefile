# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-MAKEFILE-v1.0

GLYPHS = glyphs/龍魂字元库_v0019_龍纹书法版.json
OTF = output/LonghunFont-Regular.otf
COLOR_OTF = output/LonghunFont-WuwuColor.otf
SVG_DIR = output/all_glyphs_v0019
SAMPLE = output/sample_v0019.html

.PHONY: all build build-v3 render check release install demo demo-color clean

all: build render check

build:
	python3 scripts/build_font.py $(GLYPHS) $(OTF)

build-v3:
	python3 scripts/build_font_v3.py $(GLYPHS) output/LonghunFont-Regular-v3.otf

render:
	python3 scripts/batch_render.py $(GLYPHS) $(SVG_DIR) $(SAMPLE)

check:
	python3 scripts/check_font.py $(GLYPHS)

release:
	./scripts/release.sh

install:
	./install_macos.sh

demo:
	@echo "用浏览器打开 output/demo.html"

demo-color:
	python3 scripts/build_wuwu_color_font.py $(GLYPHS) $(COLOR_OTF)

clean:
	rm -rf output/all_glyphs_v0019
	rm -f output/sample_v0019.html
	rm -f $(OTF)
	rm -f $(COLOR_OTF)
	rm -f output/LonghunFont-Regular-v3.otf
