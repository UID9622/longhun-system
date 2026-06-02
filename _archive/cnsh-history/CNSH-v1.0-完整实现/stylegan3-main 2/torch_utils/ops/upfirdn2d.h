// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: upfirdn2d.h | 标记时间: 2026-06-03T07:46:00+0800
// Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#include <cuda_runtime.h>

//------------------------------------------------------------------------
// CUDA kernel parameters.

struct upfirdn2d_kernel_params
{
    const void*     x;
    const float*    f;
    void*           y;

    int2            up;
    int2            down;
    int2            pad0;
    int             flip;
    float           gain;

    int4            inSize;         // [width, height, channel, batch]
    int4            inStride;
    int2            filterSize;     // [width, height]
    int2            filterStride;
    int4            outSize;        // [width, height, channel, batch]
    int4            outStride;
    int             sizeMinor;
    int             sizeMajor;

    int             loopMinor;
    int             loopMajor;
    int             loopX;
    int             launchMinor;
    int             launchMajor;
};

//------------------------------------------------------------------------
// CUDA kernel specialization.

struct upfirdn2d_kernel_spec
{
    void*   kernel;
    int     tileOutW;
    int     tileOutH;
    int     loopMinor;
    int     loopX;
};

//------------------------------------------------------------------------
// CUDA kernel selection.

template <class T> upfirdn2d_kernel_spec choose_upfirdn2d_kernel(const upfirdn2d_kernel_params& p);

//------------------------------------------------------------------------
