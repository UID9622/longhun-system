#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
stylemix_widget.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260310-stylemix_widget-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import imgui
from gui_utils import imgui_utils

#----------------------------------------------------------------------------

class StyleMixingWidget:
    def __init__(self, viz):
        self.viz        = viz
        self.seed_def   = 1000
        self.seed       = self.seed_def
        self.animate    = False
        self.enables    = []

    @imgui_utils.scoped_by_object_id
    def __call__(self, show=True):
        viz = self.viz
        num_ws = viz.result.get('num_ws', 0)
        num_enables = viz.result.get('num_ws', 18)
        self.enables += [False] * max(num_enables - len(self.enables), 0)

        if show:
            imgui.text('Stylemix')
            imgui.same_line(viz.label_w)
            with imgui_utils.item_width(viz.font_size * 8), imgui_utils.grayed_out(num_ws == 0):
                _changed, self.seed = imgui.input_int('##seed', self.seed)
            imgui.same_line(viz.label_w + viz.font_size * 8 + viz.spacing)
            with imgui_utils.grayed_out(num_ws == 0):
                _clicked, self.animate = imgui.checkbox('Anim', self.animate)

            pos2 = imgui.get_content_region_max()[0] - 1 - viz.button_w
            pos1 = pos2 - imgui.get_text_line_height() - viz.spacing
            pos0 = viz.label_w + viz.font_size * 12
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, [0, 0])
            for idx in range(num_enables):
                imgui.same_line(round(pos0 + (pos1 - pos0) * (idx / (num_enables - 1))))
                if idx == 0:
                    imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3)
                with imgui_utils.grayed_out(num_ws == 0):
                    _clicked, self.enables[idx] = imgui.checkbox(f'##{idx}', self.enables[idx])
                if imgui.is_item_hovered():
                    imgui.set_tooltip(f'{idx}')
            imgui.pop_style_var(1)

            imgui.same_line(pos2)
            imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 3)
            with imgui_utils.grayed_out(num_ws == 0):
                if imgui_utils.button('Reset', width=-1, enabled=(self.seed != self.seed_def or self.animate or any(self.enables[:num_enables]))):
                    self.seed = self.seed_def
                    self.animate = False
                    self.enables = [False] * num_enables

        if any(self.enables[:num_ws]):
            viz.args.stylemix_idx = [idx for idx, enable in enumerate(self.enables) if enable]
            viz.args.stylemix_seed = self.seed & ((1 << 32) - 1)
        if self.animate:
            self.seed += 1

#----------------------------------------------------------------------------
