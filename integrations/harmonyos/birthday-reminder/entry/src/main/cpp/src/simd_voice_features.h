// 龍魂 · SIMD 声纹特征提取 · ARM NEON 优化
// DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-SIMD-VOICE-v1.0
// 联动: 生日提醒v2.0 · 情感协议声纹识别 · 人格路由声纹匹配

#ifndef LONGHUN_SIMD_VOICE_H
#define LONGHUN_SIMD_VOICE_H

#include <cstdint>
#include <cstddef>
#include <vector>
#include <memory>
#include <cmath>

namespace longhun {

// === 音频参数 ===
constexpr int FRAME_LEN       = 512;   // 帧长（样本数）
constexpr int FRAME_HOP       = 256;   // 帧移（50%重叠）
constexpr int FFT_SIZE        = 512;   // FFT大小
constexpr int NUM_FILTERS     = 20;    // Mel滤波器组数量
constexpr int NUM_MFCC        = 13;    // MFCC系数数量
constexpr int VOICE_DIM       = 256;   // 龍魂声纹维度
constexpr int PITCH_BUF_SIZE  = 1024;  // 基频检测缓冲

// === 预加重系数 ===
constexpr float PRE_EMPHASIS_COEFF = 0.97f;

// ============================================================================
// SIMD优化的FFT
// ============================================================================
class SimdFFT {
public:
    explicit SimdFFT(int size);
    ~SimdFFT();

    // 复数FFT（就地变换）
    void forward(float* real, float* imag);

    // 功率谱
    void power_spectrum(const float* input, int n, float* output);

    // 获取大小
    int size() const { return size_; }

private:
    int size_;
    int log2_size_;
    float* twiddle_real_;
    float* twiddle_imag_;
    int* bit_reverse_;

    void init_twiddle_factors();
    void init_bit_reverse_table();
};

// ============================================================================
// Mel滤波器组
// ============================================================================
class MelFilterBank {
public:
    MelFilterBank(int fft_size, int num_filters, float sample_rate,
                  float low_freq, float high_freq);
    ~MelFilterBank();

    // 应用滤波器
    void apply(const float* power_spectrum, float* mel_energies) const;

    int num_filters() const { return num_filters_; }

private:
    int fft_size_;
    int num_filters_;
    float sample_rate_;

    struct Filter {
        int start_bin;
        int end_bin;
        float* weights;
    };

    Filter* filters_;

    static float hz_to_mel(float hz);
    static float mel_to_hz(float mel);
    void build_filters(float low_freq, float high_freq);
};

// ============================================================================
// NEON加速的MFCC提取器
// ============================================================================
class NeonMFCC {
public:
    explicit NeonMFCC(int sample_rate = 16000);
    ~NeonMFCC();

    // 提取MFCC特征
    // input:  音频采样 [0, n_samples)
    // output: MFCC矩阵 [n_frames x NUM_MFCC] 行主序
    // 返回:   帧数
    int extract(const float* input, int n_samples, float* output);

    // 提取龍魂256维声纹特征
    // 组合: MFCC(13帧均值→13) + Delta(13) + DeltaDelta(13)
    //      + 频谱质心(32) + 时域统计(32) + 过零率(32)
    //      + 能量包络(32) + 基频统计(32) + DNA填充(57)
    // → 总计 256维
    int extract_longhun_voiceprint(const float* input, int n_samples, float* output);

    // 估算基频 (Hz)
    float estimate_pitch(const float* input, int n_samples);

    // 批量提取（多线程友好）
    int batch_extract(const float* const* inputs, const int* lengths,
                      int batch_size, float** outputs);

private:
    int sample_rate_;

    // 子模块
    std::unique_ptr<SimdFFT> fft_;
    std::unique_ptr<MelFilterBank> mel_bank_;

    // 工作缓冲
    float* frame_buffer_;      // FRAME_LEN
    float* fft_real_;          // FFT_SIZE
    float* fft_imag_;          // FFT_SIZE
    float* power_buffer_;      // FFT_SIZE/2+1
    float* mel_buffer_;        // NUM_FILTERS
    float* mfcc_buffer_;       // NUM_MFCC

    // 预加重
    void pre_emphasis(const float* input, float* output, int n);

    // 加窗（汉明窗）
    void apply_hamming_window(float* frame, int len);

    // NEON加速的帧能量计算
    float neon_frame_energy(const float* frame, int len);

    // 过零率
    float zero_crossing_rate(const float* frame, int len);

    // 频谱质心
    float spectral_centroid(const float* power, int n);

    // DCT Type-II
    void dct_type2(const float* input, float* output, int n);

    // 对数能量
    void log_energy(const float* input, float* output, int n);

    // 计算Delta特征
    void compute_delta(const float* mfcc_matrix, int n_frames, int n_coeffs,
                       float* delta_matrix, int delta_window = 2);

    // 统计特征
    void compute_statistics(const float* values, int n, float& mean,
                           float& std_dev, float& min_val, float& max_val);
};

// ============================================================================
// NEON向量操作工具
// ============================================================================
namespace neon {

// 向量点积（NEON加速）
float dot_product(const float* a, const float* b, int n);

// 向量归一化
void normalize(float* vec, int n);

// 向量差
void subtract(const float* a, const float* b, float* out, int n);

// 向量乘加: out = a * scale + b
void multiply_add(const float* a, float scale, const float* b, float* out, int n);

// 向量求和
float sum(const float* vec, int n);

// 向量最大值
float max_val(const float* vec, int n);

// 向量最小值
float min_val(const float* vec, int n);

// 均值
float mean(const float* vec, int n);

// 标准差
float std_dev(const float* vec, int n, float mean_val);

// 复制（NEON加速大块复制）
void copy(const float* src, float* dst, int n);

} // namespace neon

} // namespace longhun

#endif // LONGHUN_SIMD_VOICE_H
