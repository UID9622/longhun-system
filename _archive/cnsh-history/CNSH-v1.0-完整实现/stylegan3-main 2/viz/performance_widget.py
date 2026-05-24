#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
performance_widget.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260310-performance_widget-v1.0
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

import array
import numpy as np
import imgui
from gui_utils import imgui_utils

#----------------------------------------------------------------------------

class PerformanceWidget:
    def __init__(self, viz):
        self.viz            = viz
        self.gui_times      = [float('nan')] * 60
        self.render_times   = [float('nan')] * 30
        self.fps_limit      = 60
        self.use_vsync      = False
        self.is_async       = False
        self.force_fp32     = False

    @imgui_utils.scoped_by_object_id
    def __call__(self, show=True):
        viz = self.viz
        self.gui_times = self.gui_times[1:] + [viz.frame_delta]
        if 'render_time' in viz.result:
            self.render_times = self.render_times[1:] + [viz.result.render_time]
            del viz.result.render_time

        if show:
            imgui.text('GUI')
            imgui.same_line(viz.label_w)
            with imgui_utils.item_width(viz.font_size * 8):
                imgui.plot_lines('##gui_times', array.array('f', self.gui_times), scale_min=0)
            imgui.same_line(viz.label_w + viz.font_size * 9)
            t = [x for x in self.gui_times if x > 0]
            t = np.mean(t) if len(t) > 0 else 0
            imgui.text(f'{t*1e3:.1f} ms' if t > 0 else 'N/A')
            imgui.same_line(viz.label_w + viz.font_size * 14)
            imgui.text(f'{1/t:.1f} FPS' if t > 0 else 'N/A')
            imgui.same_line(viz.label_w + viz.font_size * 18 + viz.spacing * 3)
            with imgui_utils.item_width(viz.font_size * 6):
                _changed, self.fps_limit = imgui.input_int('FPS limit', self.fps_limit, flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
                self.fps_limit = min(max(self.fps_limit, 5), 1000)
            imgui.same_line(imgui.get_content_region_max()[0] - 1 - viz.button_w * 2 - viz.spacing)
            _clicked, self.use_vsync = imgui.checkbox('Vertical sync', self.use_vsync)

        if show:
            imgui.text('Render')
            imgui.same_line(viz.label_w)
            with imgui_utils.item_width(viz.font_size * 8):
                imgui.plot_lines('##render_times', array.array('f', self.render_times), scale_min=0)
            imgui.same_line(viz.label_w + viz.font_size * 9)
            t = [x for x in self.render_times if x > 0]
            t = np.mean(t) if len(t) > 0 else 0
            imgui.text(f'{t*1e3:.1f} ms' if t > 0 else 'N/A')
            imgui.same_line(viz.label_w + viz.font_size * 14)
            imgui.text(f'{1/t:.1f} FPS' if t > 0 else 'N/A')
            imgui.same_line(viz.label_w + viz.font_size * 18 + viz.spacing * 3)
            _clicked, self.is_async = imgui.checkbox('Separate process', self.is_async)
            imgui.same_line(imgui.get_content_region_max()[0] - 1 - viz.button_w * 2 - viz.spacing)
            _clicked, self.force_fp32 = imgui.checkbox('Force FP32', self.force_fp32)

        viz.set_fps_limit(self.fps_limit)
        viz.set_vsync(self.use_vsync)
        viz.set_async(self.is_async)
        viz.args.force_fp32 = self.force_fp32

#----------------------------------------------------------------------------
