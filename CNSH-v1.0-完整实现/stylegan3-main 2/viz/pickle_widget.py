#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
pickle_widget.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260310-pickle_widget-v1.0
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

import glob
import os
import re

import dnnlib
import imgui
import numpy as np
from gui_utils import imgui_utils

from . import renderer

#----------------------------------------------------------------------------

def _locate_results(pattern):
    return pattern

#----------------------------------------------------------------------------

class PickleWidget:
    def __init__(self, viz):
        self.viz            = viz
        self.search_dirs    = []
        self.cur_pkl        = None
        self.user_pkl       = ''
        self.recent_pkls    = []
        self.browse_cache   = dict() # {tuple(path, ...): [dnnlib.EasyDict(), ...], ...}
        self.browse_refocus = False
        self.load('', ignore_errors=True)

    def add_recent(self, pkl, ignore_errors=False):
        try:
            resolved = self.resolve_pkl(pkl)
            if resolved not in self.recent_pkls:
                self.recent_pkls.append(resolved)
        except:
            if not ignore_errors:
                raise

    def load(self, pkl, ignore_errors=False):
        viz = self.viz
        viz.clear_result()
        viz.skip_frame() # The input field will change on next frame.
        try:
            resolved = self.resolve_pkl(pkl)
            name = resolved.replace('\\', '/').split('/')[-1]
            self.cur_pkl = resolved
            self.user_pkl = resolved
            viz.result.message = f'Loading {name}...'
            viz.defer_rendering()
            if resolved in self.recent_pkls:
                self.recent_pkls.remove(resolved)
            self.recent_pkls.insert(0, resolved)
        except:
            self.cur_pkl = None
            self.user_pkl = pkl
            if pkl == '':
                viz.result = dnnlib.EasyDict(message='No network pickle loaded')
            else:
                viz.result = dnnlib.EasyDict(error=renderer.CapturedException())
            if not ignore_errors:
                raise

    @imgui_utils.scoped_by_object_id
    def __call__(self, show=True):
        viz = self.viz
        recent_pkls = [pkl for pkl in self.recent_pkls if pkl != self.user_pkl]
        if show:
            imgui.text('Pickle')
            imgui.same_line(viz.label_w)
            changed, self.user_pkl = imgui_utils.input_text('##pkl', self.user_pkl, 1024,
                flags=(imgui.INPUT_TEXT_AUTO_SELECT_ALL | imgui.INPUT_TEXT_ENTER_RETURNS_TRUE),
                width=(-1 - viz.button_w * 2 - viz.spacing * 2),
                help_text='<PATH> | <URL> | <RUN_DIR> | <RUN_ID> | <RUN_ID>/<KIMG>.pkl')
            if changed:
                self.load(self.user_pkl, ignore_errors=True)
            if imgui.is_item_hovered() and not imgui.is_item_active() and self.user_pkl != '':
                imgui.set_tooltip(self.user_pkl)
            imgui.same_line()
            if imgui_utils.button('Recent...', width=viz.button_w, enabled=(len(recent_pkls) != 0)):
                imgui.open_popup('recent_pkls_popup')
            imgui.same_line()
            if imgui_utils.button('Browse...', enabled=len(self.search_dirs) > 0, width=-1):
                imgui.open_popup('browse_pkls_popup')
                self.browse_cache.clear()
                self.browse_refocus = True

        if imgui.begin_popup('recent_pkls_popup'):
            for pkl in recent_pkls:
                clicked, _state = imgui.menu_item(pkl)
                if clicked:
                    self.load(pkl, ignore_errors=True)
            imgui.end_popup()

        if imgui.begin_popup('browse_pkls_popup'):
            def recurse(parents):
                key = tuple(parents)
                items = self.browse_cache.get(key, None)
                if items is None:
                    items = self.list_runs_and_pkls(parents)
                    self.browse_cache[key] = items
                for item in items:
                    if item.type == 'run' and imgui.begin_menu(item.name):
                        recurse([item.path])
                        imgui.end_menu()
                    if item.type == 'pkl':
                        clicked, _state = imgui.menu_item(item.name)
                        if clicked:
                            self.load(item.path, ignore_errors=True)
                if len(items) == 0:
                    with imgui_utils.grayed_out():
                        imgui.menu_item('No results found')
            recurse(self.search_dirs)
            if self.browse_refocus:
                imgui.set_scroll_here()
                viz.skip_frame() # Focus will change on next frame.
                self.browse_refocus = False
            imgui.end_popup()

        paths = viz.pop_drag_and_drop_paths()
        if paths is not None and len(paths) >= 1:
            self.load(paths[0], ignore_errors=True)

        viz.args.pkl = self.cur_pkl

    def list_runs_and_pkls(self, parents):
        items = []
        run_regex = re.compile(r'\d+-.*')
        pkl_regex = re.compile(r'network-snapshot-\d+\.pkl')
        for parent in set(parents):
            if os.path.isdir(parent):
                for entry in os.scandir(parent):
                    if entry.is_dir() and run_regex.fullmatch(entry.name):
                        items.append(dnnlib.EasyDict(type='run', name=entry.name, path=os.path.join(parent, entry.name)))
                    if entry.is_file() and pkl_regex.fullmatch(entry.name):
                        items.append(dnnlib.EasyDict(type='pkl', name=entry.name, path=os.path.join(parent, entry.name)))

        items = sorted(items, key=lambda item: (item.name.replace('_', ' '), item.path))
        return items

    def resolve_pkl(self, pattern):
        assert isinstance(pattern, str)
        assert pattern != ''

        # URL => return as is.
        if dnnlib.util.is_url(pattern):
            return pattern

        # Short-hand pattern => locate.
        path = _locate_results(pattern)

        # Run dir => pick the last saved snapshot.
        if os.path.isdir(path):
            pkl_files = sorted(glob.glob(os.path.join(path, 'network-snapshot-*.pkl')))
            if len(pkl_files) == 0:
                raise IOError(f'No network pickle found in "{path}"')
            path = pkl_files[-1]

        # Normalize.
        path = os.path.abspath(path)
        return path

#----------------------------------------------------------------------------
