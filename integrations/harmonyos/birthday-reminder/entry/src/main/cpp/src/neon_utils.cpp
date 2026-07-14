// 龍魂 · NEON工具集 · ARM向量加速
// DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-NEON-UTILS-v1.0
// 提供独立的NEON加速工具函数，供其他模块调用

#include <cstdint>
#include <cstddef>
#include <cstring>
#include <cmath>

#ifdef __ARM_NEON
#include <arm_neon.h>
#endif

namespace longhun {
namespace neon_utils {

// ============================================================================
// 向量加法: out = a + b
// ============================================================================
void vector_add(const float* a, const float* b, float* out, int n) {
#ifdef __ARM_NEON
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        vst1q_f32(out + i, vaddq_f32(va, vb));
    }
    for (; i < n; ++i) out[i] = a[i] + b[i];
#else
    for (int i = 0; i < n; ++i) out[i] = a[i] + b[i];
#endif
}

// ============================================================================
// 向量缩放: out = a * scalar
// ============================================================================
void vector_scale(const float* a, float scalar, float* out, int n) {
#ifdef __ARM_NEON
    float32x4_t vscalar = vdupq_n_f32(scalar);
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        vst1q_f32(out + i, vmulq_f32(va, vscalar));
    }
    for (; i < n; ++i) out[i] = a[i] * scalar;
#else
    for (int i = 0; i < n; ++i) out[i] = a[i] * scalar;
#endif
}

// ============================================================================
// L2距离: sqrt(sum((a-b)^2))
// ============================================================================
float l2_distance(const float* a, const float* b, int n) {
#ifdef __ARM_NEON
    float32x4_t sum = vdupq_n_f32(0.0f);
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        float32x4_t diff = vsubq_f32(va, vb);
        sum = vmlaq_f32(sum, diff, diff);
    }
    float result = vaddvq_f32(sum);
    for (; i < n; ++i) {
        float diff = a[i] - b[i];
        result += diff * diff;
    }
    return sqrtf(result);
#else
    float result = 0.0f;
    for (int i = 0; i < n; ++i) {
        float diff = a[i] - b[i];
        result += diff * diff;
    }
    return sqrtf(result);
#endif
}

// ============================================================================
// 余弦相似度: dot(a,b) / (|a|*|b|)
// ============================================================================
float cosine_similarity(const float* a, const float* b, int n) {
#ifdef __ARM_NEON
    float32x4_t dot = vdupq_n_f32(0.0f);
    float32x4_t norm_a = vdupq_n_f32(0.0f);
    float32x4_t norm_b = vdupq_n_f32(0.0f);
    int i = 0;

    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        dot    = vmlaq_f32(dot, va, vb);
        norm_a = vmlaq_f32(norm_a, va, va);
        norm_b = vmlaq_f32(norm_b, vb, vb);
    }

    float d = vaddvq_f32(dot);
    float na = vaddvq_f32(norm_a);
    float nb = vaddvq_f32(norm_b);

    for (; i < n; ++i) {
        d += a[i] * b[i];
        na += a[i] * a[i];
        nb += b[i] * b[i];
    }

    float den = sqrtf(na) * sqrtf(nb);
    return den > 0.0f ? d / den : 0.0f;
#else
    float d = 0.0f, na = 0.0f, nb = 0.0f;
    for (int i = 0; i < n; ++i) {
        d += a[i] * b[i];
        na += a[i] * a[i];
        nb += b[i] * b[i];
    }
    float den = sqrtf(na) * sqrtf(nb);
    return den > 0.0f ? d / den : 0.0f;
#endif
}

// ============================================================================
// 矩阵乘法: C[m][k] = A[m][n] x B[n][k]  (简化版，小矩阵)
// ============================================================================
void matrix_multiply(const float* a, const float* b, float* c,
                     int m, int n, int k) {
    std::memset(c, 0, m * k * sizeof(float));

    for (int i = 0; i < m; ++i) {
        for (int l = 0; l < n; ++l) {
            float a_val = a[i * n + l];
#ifdef __ARM_NEON
            int j = 0;
            float32x4_t va = vdupq_n_f32(a_val);
            for (; j <= k - 4; j += 4) {
                float32x4_t vb = vld1q_f32(b + l * k + j);
                float32x4_t vc = vld1q_f32(c + i * k + j);
                vst1q_f32(c + i * k + j, vmlaq_f32(vc, va, vb));
            }
            for (; j < k; ++j) {
                c[i * k + j] += a_val * b[l * k + j];
            }
#else
            for (int j = 0; j < k; ++j) {
                c[i * k + j] += a_val * b[l * k + j];
            }
#endif
        }
    }
}

// ============================================================================
// Softmax
// ============================================================================
void softmax(const float* input, float* output, int n) {
    // 找最大值（数值稳定性）
    float max_val = input[0];
    for (int i = 1; i < n; ++i) {
        if (input[i] > max_val) max_val = input[i];
    }

    // exp and sum
    float sum = 0.0f;
    for (int i = 0; i < n; ++i) {
        output[i] = expf(input[i] - max_val);
        sum += output[i];
    }

    // normalize
    float inv_sum = 1.0f / sum;
    vector_scale(output, inv_sum, output, n);
}

// ============================================================================
// ArgMax
// ============================================================================
int argmax(const float* vec, int n) {
    if (n <= 0) return -1;
    int idx = 0;
    float max_v = vec[0];
    for (int i = 1; i < n; ++i) {
        if (vec[i] > max_v) {
            max_v = vec[i];
            idx = i;
        }
    }
    return idx;
}

// ============================================================================
// TopK
// ============================================================================
void topk(const float* vec, int n, int k, int* indices, float* values) {
    // 简化实现：排序取topk
    struct Pair { float val; int idx; };
    Pair* pairs = new Pair[n];
    for (int i = 0; i < n; ++i) {
        pairs[i] = {vec[i], i};
    }

    std::sort(pairs, pairs + n, [](const Pair& a, const Pair& b) {
        return a.val > b.val;
    });

    for (int i = 0; i < k && i < n; ++i) {
        indices[i] = pairs[i].idx;
        values[i]  = pairs[i].val;
    }

    delete[] pairs;
}

// ============================================================================
// 快速哈希 (FNV-1a)
// ============================================================================
uint64_t fnv1a_hash(const void* data, size_t len) {
    const uint64_t FNV_OFFSET = 14695981039346656037ULL;
    const uint64_t FNV_PRIME  = 1099511628211ULL;

    uint64_t hash = FNV_OFFSET;
    const uint8_t* bytes = static_cast<const uint8_t*>(data);

    for (size_t i = 0; i < len; ++i) {
        hash ^= bytes[i];
        hash *= FNV_PRIME;
    }

    return hash;
}

// ============================================================================
// DNA签名生成
// ============================================================================
std::string generate_dna_signature(const void* data, size_t len) {
    uint64_t hash = fnv1a_hash(data, len);

    char buf[32];
    snprintf(buf, sizeof(buf), "#LH-%016llX-%s",
             static_cast<unsigned long long>(hash), MASTER_UID);

    return std::string(buf);
}

} // namespace neon_utils
} // namespace longhun
