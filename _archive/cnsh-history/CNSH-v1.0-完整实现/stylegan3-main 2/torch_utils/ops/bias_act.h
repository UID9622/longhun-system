// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: bias_act.h | 标记时间: 2026-06-03T07:46:00+0800
// Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

//------------------------------------------------------------------------
// CUDA kernel parameters.

struct bias_act_kernel_params
{
    const void* x;      // [sizeX]
    const void* b;      // [sizeB] or NULL
    const void* xref;   // [sizeX] or NULL
    const void* yref;   // [sizeX] or NULL
    const void* dy;     // [sizeX] or NULL
    void*       y;      // [sizeX]

    int         grad;
    int         act;
    float       alpha;
    float       gain;
    float       clamp;

    int         sizeX;
    int         sizeB;
    int         stepB;
    int         loopX;
};

//------------------------------------------------------------------------
// CUDA kernel selection.

template <class T> void* choose_bias_act_kernel(const bias_act_kernel_params& p);

//------------------------------------------------------------------------
