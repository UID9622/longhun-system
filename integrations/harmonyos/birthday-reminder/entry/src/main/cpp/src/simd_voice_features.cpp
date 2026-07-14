// 龍魂 · SIMD 声纹特征提取实现
// DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-SIMD-VOICE-IMPL-v1.0

#include "simd_voice_features.h"
#include <cstring>
#include <algorithm>

// ARM NEON intrinsics
#ifdef __ARM_NEON
#include <arm_neon.h>
#endif

namespace longhun {

// ============================================================================
// SimdFFT 实现
// ============================================================================

SimdFFT::SimdFFT(int size) : size_(size) {
    log2_size_ = 0;
    int s = size;
    while (s > 1) { s >>= 1; log2_size_++; }

    twiddle_real_ = new float[size_ / 2];
    twiddle_imag_ = new float[size_ / 2];
    bit_reverse_  = new int[size_];

    init_twiddle_factors();
    init_bit_reverse_table();
}

SimdFFT::~SimdFFT() {
    delete[] twiddle_real_;
    delete[] twiddle_imag_;
    delete[] bit_reverse_;
}

void SimdFFT::init_twiddle_factors() {
    for (int i = 0; i < size_ / 2; ++i) {
        double angle = -2.0 * M_PI * i / size_;
        twiddle_real_[i] = static_cast<float>(cos(angle));
        twiddle_imag_[i] = static_cast<float>(sin(angle));
    }
}

void SimdFFT::init_bit_reverse_table() {
    for (int i = 0; i < size_; ++i) {
        int rev = 0;
        int val = i;
        for (int j = 0; j < log2_size_; ++j) {
            rev = (rev << 1) | (val & 1);
            val >>= 1;
        }
        bit_reverse_[i] = rev;
    }
}

void SimdFFT::forward(float* real, float* imag) {
    // 位反转重排
    for (int i = 0; i < size_; ++i) {
        int j = bit_reverse_[i];
        if (i < j) {
            std::swap(real[i], real[j]);
            if (imag) std::swap(imag[i], imag[j]);
        }
    }

    // Cooley-Tukey FFT
    for (int len = 2; len <= size_; len <<= 1) {
        int half = len >> 1;
        int step = size_ / len;

        for (int i = 0; i < size_; i += len) {
            for (int j = 0; j < half; ++j) {
                float wr = twiddle_real_[j * step];
                float wi = twiddle_imag_[j * step];

                int even_idx = i + j;
                int odd_idx  = i + j + half;

                float tr = wr * real[odd_idx] - wi * (imag ? imag[odd_idx] : 0.0f);
                float ti = wr * (imag ? imag[odd_idx] : 0.0f) + wi * real[odd_idx];

                real[odd_idx] = real[even_idx] - tr;
                real[even_idx] = real[even_idx] + tr;

                if (imag) {
                    imag[odd_idx] = imag[even_idx] - ti;
                    imag[even_idx] = imag[even_idx] + ti;
                }
            }
        }
    }
}

void SimdFFT::power_spectrum(const float* input, int n, float* output) {
    // 拷贝输入
    float* real = new float[size_];
    float* imag = new float[size_];
    std::memset(real, 0, size_ * sizeof(float));
    std::memset(imag, 0, size_ * sizeof(float));

    int copy_n = std::min(n, size_);
    std::memcpy(real, input, copy_n * sizeof(float));

    forward(real, imag);

    for (int i = 0; i <= size_ / 2; ++i) {
        output[i] = real[i] * real[i] + imag[i] * imag[i];
    }

    delete[] real;
    delete[] imag;
}

// ============================================================================
// MelFilterBank 实现
// ============================================================================

MelFilterBank::MelFilterBank(int fft_size, int num_filters,
                             float sample_rate, float low_freq, float high_freq)
    : fft_size_(fft_size), num_filters_(num_filters), sample_rate_(sample_rate) {
    filters_ = new Filter[num_filters_];
    build_filters(low_freq, high_freq);
}

MelFilterBank::~MelFilterBank() {
    for (int i = 0; i < num_filters_; ++i) {
        delete[] filters_[i].weights;
    }
    delete[] filters_;
}

float MelFilterBank::hz_to_mel(float hz) {
    return 2595.0f * log10f(1.0f + hz / 700.0f);
}

float MelFilterBank::mel_to_hz(float mel) {
    return 700.0f * (powf(10.0f, mel / 2595.0f) - 1.0f);
}

void MelFilterBank::build_filters(float low_freq, float high_freq) {
    float low_mel  = hz_to_mel(low_freq);
    float high_mel = hz_to_mel(high_freq);

    // Mel等间距点
    std::vector<float> mel_points(num_filters_ + 2);
    float mel_step = (high_mel - low_mel) / (num_filters_ + 1);
    for (int i = 0; i < num_filters_ + 2; ++i) {
        mel_points[i] = low_mel + i * mel_step;
    }

    // 转回Hz并映射到FFT bin
    std::vector<int> bins(num_filters_ + 2);
    for (int i = 0; i < num_filters_ + 2; ++i) {
        float hz = mel_to_hz(mel_points[i]);
        bins[i] = static_cast<int>((fft_size_ + 1) * hz / sample_rate_);
    }

    // 构建三角滤波器
    for (int i = 0; i < num_filters_; ++i) {
        filters_[i].start_bin = bins[i];
        filters_[i].end_bin   = bins[i + 2];
        int width = filters_[i].end_bin - filters_[i].start_bin;
        filters_[i].weights = new float[width];

        for (int j = 0; j < width; ++j) {
            int bin = filters_[i].start_bin + j;
            if (bin < bins[i + 1]) {
                filters_[i].weights[j] = static_cast<float>(bin - bins[i])
                    / (bins[i + 1] - bins[i]);
            } else {
                filters_[i].weights[j] = static_cast<float>(bins[i + 2] - bin)
                    / (bins[i + 2] - bins[i + 1]);
            }
        }
    }
}

void MelFilterBank::apply(const float* power_spectrum, float* mel_energies) const {
    for (int i = 0; i < num_filters_; ++i) {
        float energy = 0.0f;
        int width = filters_[i].end_bin - filters_[i].start_bin;
        for (int j = 0; j < width; ++j) {
            energy += power_spectrum[filters_[i].start_bin + j] * filters_[i].weights[j];
        }
        // 防止log(0)
        mel_energies[i] = energy > 1e-10f ? energy : 1e-10f;
    }
}

// ============================================================================
// NeonMFCC 实现
// ============================================================================

NeonMFCC::NeonMFCC(int sample_rate) : sample_rate_(sample_rate) {
    fft_      = std::make_unique<SimdFFT>(FFT_SIZE);
    mel_bank_ = std::make_unique<MelFilterBank>(FFT_SIZE, NUM_FILTERS,
                                                 sample_rate_, 300.0f, 8000.0f);

    frame_buffer_ = new float[FRAME_LEN];
    fft_real_     = new float[FFT_SIZE];
    fft_imag_     = new float[FFT_SIZE];
    power_buffer_ = new float[FFT_SIZE / 2 + 1];
    mel_buffer_   = new float[NUM_FILTERS];
    mfcc_buffer_  = new float[NUM_MFCC];
}

NeonMFCC::~NeonMFCC() {
    delete[] frame_buffer_;
    delete[] fft_real_;
    delete[] fft_imag_;
    delete[] power_buffer_;
    delete[] mel_buffer_;
    delete[] mfcc_buffer_;
}

void NeonMFCC::pre_emphasis(const float* input, float* output, int n) {
    output[0] = input[0];
    for (int i = 1; i < n; ++i) {
        output[i] = input[i] - PRE_EMPHASIS_COEFF * input[i - 1];
    }
}

void NeonMFCC::apply_hamming_window(float* frame, int len) {
    for (int i = 0; i < len; ++i) {
        float w = 0.54f - 0.46f * cosf(2.0f * M_PI * i / (len - 1));
        frame[i] *= w;
    }
}

float NeonMFCC::neon_frame_energy(const float* frame, int len) {
#ifdef __ARM_NEON
    float32x4_t sum = vdupq_n_f32(0.0f);
    int i = 0;

    for (; i <= len - 4; i += 4) {
        float32x4_t v = vld1q_f32(frame + i);
        sum = vmlaq_f32(sum, v, v);
    }

    float result = vaddvq_f32(sum);

    // 剩余元素
    for (; i < len; ++i) {
        result += frame[i] * frame[i];
    }

    return result;
#else
    float energy = 0.0f;
    for (int i = 0; i < len; ++i) {
        energy += frame[i] * frame[i];
    }
    return energy;
#endif
}

float NeonMFCC::zero_crossing_rate(const float* frame, int len) {
    int crossings = 0;
    for (int i = 1; i < len; ++i) {
        if (frame[i] * frame[i - 1] < 0) crossings++;
    }
    return static_cast<float>(crossings) / (len - 1);
}

float NeonMFCC::spectral_centroid(const float* power, int n) {
    float num = 0.0f, den = 0.0f;
    for (int i = 0; i < n; ++i) {
        num += i * power[i];
        den += power[i];
    }
    return den > 0 ? num / den : 0.0f;
}

void NeonMFCC::dct_type2(const float* input, float* output, int n) {
    for (int k = 0; k < n; ++k) {
        float sum = 0.0f;
        for (int i = 0; i < n; ++i) {
            sum += input[i] * cosf(M_PI * k * (2.0f * i + 1) / (2.0f * n));
        }
        output[k] = sum;
    }
}

void NeonMFCC::log_energy(const float* input, float* output, int n) {
    for (int i = 0; i < n; ++i) {
        output[i] = logf(input[i] + 1e-10f);
    }
}

void NeonMFCC::compute_delta(const float* mfcc_matrix, int n_frames,
                              int n_coeffs, float* delta_matrix, int delta_window) {
    for (int f = 0; f < n_frames; ++f) {
        float den = 0.0f;
        for (int k = 1; k <= delta_window; ++k) {
            den += 2.0f * k * k;
        }

        for (int c = 0; c < n_coeffs; ++c) {
            float num = 0.0f;
            for (int k = 1; k <= delta_window; ++k) {
                float forward  = (f + k < n_frames)  ? mfcc_matrix[(f + k) * n_coeffs + c] : 0.0f;
                float backward = (f - k >= 0)         ? mfcc_matrix[(f - k) * n_coeffs + c] : 0.0f;
                num += k * (forward - backward);
            }
            delta_matrix[f * n_coeffs + c] = num / den;
        }
    }
}

void NeonMFCC::compute_statistics(const float* values, int n,
                                   float& mean_val, float& std_val,
                                   float& min_val, float& max_val) {
    if (n == 0) { mean_val = std_val = min_val = max_val = 0.0f; return; }

    float sum = 0.0f;
    min_val = values[0];
    max_val = values[0];

    for (int i = 0; i < n; ++i) {
        sum += values[i];
        if (values[i] < min_val) min_val = values[i];
        if (values[i] > max_val) max_val = values[i];
    }

    mean_val = sum / n;

    float sq_sum = 0.0f;
    for (int i = 0; i < n; ++i) {
        float diff = values[i] - mean_val;
        sq_sum += diff * diff;
    }
    std_val = sqrtf(sq_sum / n);
}

int NeonMFCC::extract(const float* input, int n_samples, float* output) {
    int n_frames = (n_samples - FRAME_LEN) / FRAME_HOP + 1;
    if (n_frames <= 0) return 0;

    for (int f = 0; f < n_frames; ++f) {
        // 分帧
        int offset = f * FRAME_HOP;
        std::memcpy(frame_buffer_, input + offset, FRAME_LEN * sizeof(float));

        // 预加重
        float pre_emph[FRAME_LEN];
        pre_emphasis(frame_buffer_, pre_emph, FRAME_LEN);

        // 加窗
        apply_hamming_window(pre_emph, FRAME_LEN);

        // FFT
        std::memset(fft_real_, 0, FFT_SIZE * sizeof(float));
        std::memset(fft_imag_, 0, FFT_SIZE * sizeof(float));
        std::memcpy(fft_real_, pre_emph, FRAME_LEN * sizeof(float));
        fft_->forward(fft_real_, fft_imag_);

        // 功率谱
        for (int i = 0; i <= FFT_SIZE / 2; ++i) {
            power_buffer_[i] = fft_real_[i] * fft_real_[i] + fft_imag_[i] * fft_imag_[i];
        }

        // Mel滤波器
        mel_bank_->apply(power_buffer_, mel_buffer_);

        // Log
        log_energy(mel_buffer_, mel_buffer_, NUM_FILTERS);

        // DCT
        dct_type2(mel_buffer_, mfcc_buffer_, NUM_MFCC);

        // 输出
        std::memcpy(output + f * NUM_MFCC, mfcc_buffer_, NUM_MFCC * sizeof(float));
    }

    return n_frames;
}

int NeonMFCC::extract_longhun_voiceprint(const float* input, int n_samples, float* output) {
    int n_frames = (n_samples - FRAME_LEN) / FRAME_HOP + 1;
    if (n_frames <= 0) {
        std::memset(output, 0, VOICE_DIM * sizeof(float));
        return 0;
    }

    // 分配MFCC矩阵
    float* mfcc_matrix = new float[n_frames * NUM_MFCC];
    int actual_frames = extract(input, n_samples, mfcc_matrix);

    int offset = 0;

    // 1. MFCC均值 (13维)
    for (int c = 0; c < NUM_MFCC; ++c) {
        float sum = 0.0f;
        for (int f = 0; f < actual_frames; ++f) {
            sum += mfcc_matrix[f * NUM_MFCC + c];
        }
        output[offset++] = sum / actual_frames;
    }

    // 2. Delta MFCC均值 (13维)
    float* delta = new float[actual_frames * NUM_MFCC];
    compute_delta(mfcc_matrix, actual_frames, NUM_MFCC, delta);
    for (int c = 0; c < NUM_MFCC; ++c) {
        float sum = 0.0f;
        for (int f = 0; f < actual_frames; ++f) {
            sum += delta[f * NUM_MFCC + c];
        }
        output[offset++] = sum / actual_frames;
    }
    delete[] delta;

    // 3. Delta-Delta MFCC均值 (13维)
    float* delta2 = new float[actual_frames * NUM_MFCC];
    compute_delta(mfcc_matrix, actual_frames, NUM_MFCC, delta2, 3);
    for (int c = 0; c < NUM_MFCC; ++c) {
        float sum = 0.0f;
        for (int f = 0; f < actual_frames; ++f) {
            sum += delta2[f * NUM_MFCC + c];
        }
        output[offset++] = sum / actual_frames;
    }
    delete[] delta2;

    // 4. 频谱质心统计 (32维)
    {
        float* centroids = new float[actual_frames];
        for (int f = 0; f < actual_frames; ++f) {
            int sample_offset = f * FRAME_HOP;
            std::memcpy(frame_buffer_, input + sample_offset, FRAME_LEN * sizeof(float));
            fft_->power_spectrum(frame_buffer_, FRAME_LEN, power_buffer_);
            centroids[f] = spectral_centroid(power_buffer_, FFT_SIZE / 2 + 1);
        }
        float mean_v, std_v, min_v, max_v;
        compute_statistics(centroids, actual_frames, mean_v, std_v, min_v, max_v);
        for (int i = 0; i < 8; ++i) output[offset++] = centroids[i % actual_frames];
        output[offset++] = mean_v; output[offset++] = std_v;
        output[offset++] = min_v; output[offset++] = max_v;
        for (int i = 0; i < 8; ++i) output[offset++] = centroids[(actual_frames / 2 + i) % actual_frames];
        for (int i = 0; i < 8; ++i) output[offset++] = centroids[(actual_frames - 8 + i) % actual_frames];
        delete[] centroids;
    }

    // 5. 时域统计 (32维)
    {
        float* energies = new float[actual_frames];
        for (int f = 0; f < actual_frames; ++f) {
            int sample_offset = f * FRAME_HOP;
            energies[f] = neon_frame_energy(input + sample_offset, FRAME_LEN);
        }
        float mean_v, std_v, min_v, max_v;
        compute_statistics(energies, actual_frames, mean_v, std_v, min_v, max_v);
        for (int i = 0; i < 8; ++i) output[offset++] = energies[i % actual_frames];
        output[offset++] = mean_v; output[offset++] = std_v;
        output[offset++] = min_v; output[offset++] = max_v;
        for (int i = 0; i < 8; ++i) output[offset++] = energies[(actual_frames / 2 + i) % actual_frames];
        for (int i = 0; i < 8; ++i) output[offset++] = energies[(actual_frames - 8 + i) % actual_frames];
        delete[] energies;
    }

    // 6. 过零率统计 (32维)
    {
        float* zcrs = new float[actual_frames];
        for (int f = 0; f < actual_frames; ++f) {
            int sample_offset = f * FRAME_HOP;
            zcrs[f] = zero_crossing_rate(input + sample_offset, FRAME_LEN);
        }
        float mean_v, std_v, min_v, max_v;
        compute_statistics(zcrs, actual_frames, mean_v, std_v, min_v, max_v);
        for (int i = 0; i < 8; ++i) output[offset++] = zcrs[i % actual_frames];
        output[offset++] = mean_v; output[offset++] = std_v;
        output[offset++] = min_v; output[offset++] = max_v;
        for (int i = 0; i < 8; ++i) output[offset++] = zcrs[(actual_frames / 2 + i) % actual_frames];
        for (int i = 0; i < 8; ++i) output[offset++] = zcrs[(actual_frames - 8 + i) % actual_frames];
        delete[] zcrs;
    }

    // 7. 能量包络统计 (32维)
    {
        float* envelopes = new float[actual_frames];
        for (int f = 0; f < actual_frames; ++f) {
            int sample_offset = f * FRAME_HOP;
            envelopes[f] = logf(neon_frame_energy(input + sample_offset, FRAME_LEN) + 1e-10f);
        }
        float mean_v, std_v, min_v, max_v;
        compute_statistics(envelopes, actual_frames, mean_v, std_v, min_v, max_v);
        for (int i = 0; i < 8; ++i) output[offset++] = envelopes[i % actual_frames];
        output[offset++] = mean_v; output[offset++] = std_v;
        output[offset++] = min_v; output[offset++] = max_v;
        for (int i = 0; i < 8; ++i) output[offset++] = envelopes[(actual_frames / 2 + i) % actual_frames];
        for (int i = 0; i < 8; ++i) output[offset++] = envelopes[(actual_frames - 8 + i) % actual_frames];
        delete[] envelopes;
    }

    // 8. 基频统计 (32维)
    {
        float* pitches = new float[actual_frames];
        for (int f = 0; f < actual_frames; ++f) {
            int sample_offset = f * FRAME_HOP;
            pitches[f] = estimate_pitch(input + sample_offset, FRAME_LEN);
        }
        float mean_v, std_v, min_v, max_v;
        compute_statistics(pitches, actual_frames, mean_v, std_v, min_v, max_v);
        for (int i = 0; i < 8; ++i) output[offset++] = pitches[i % actual_frames];
        output[offset++] = mean_v; output[offset++] = std_v;
        output[offset++] = min_v; output[offset++] = max_v;
        for (int i = 0; i < 8; ++i) output[offset++] = pitches[(actual_frames / 2 + i) % actual_frames];
        for (int i = 0; i < 8; ++i) output[offset++] = pitches[(actual_frames - 8 + i) % actual_frames];
        delete[] pitches;
    }

    // 9. DNA填充 (剩余57维)
    // 用MASTER_DNA的ASCII码+UID数字组合填充
    const char* dna = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-9622";
    int dna_len = strlen(dna);
    while (offset < VOICE_DIM) {
        for (int i = 0; i < dna_len && offset < VOICE_DIM; ++i) {
            output[offset++] = static_cast<float>(dna[i]) / 255.0f;
        }
    }

    delete[] mfcc_matrix;
    return actual_frames;
}

float NeonMFCC::estimate_pitch(const float* input, int n_samples) {
    // 自相关法估算基频
    if (n_samples < PITCH_BUF_SIZE / 2) return 0.0f;

    const int min_lag = static_cast<int>(sample_rate_ / 400.0f);  // 400Hz
    const int max_lag = static_cast<int>(sample_rate_ / 80.0f);   // 80Hz

    float best_corr = -1.0f;
    int best_lag = min_lag;

    for (int lag = min_lag; lag < max_lag && lag < n_samples; ++lag) {
        float corr = 0.0f;
        for (int i = 0; i < n_samples - lag; ++i) {
            corr += input[i] * input[i + lag];
        }
        if (corr > best_corr) {
            best_corr = corr;
            best_lag = lag;
        }
    }

    return best_lag > 0 ? static_cast<float>(sample_rate_) / best_lag : 0.0f;
}

int NeonMFCC::batch_extract(const float* const* inputs, const int* lengths,
                             int batch_size, float** outputs) {
    int total_frames = 0;
    for (int i = 0; i < batch_size; ++i) {
        total_frames += extract(inputs[i], lengths[i], outputs[i]);
    }
    return total_frames;
}

// ============================================================================
// NEON 向量操作实现
// ============================================================================

namespace neon {

float dot_product(const float* a, const float* b, int n) {
#ifdef __ARM_NEON
    float32x4_t sum = vdupq_n_f32(0.0f);
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        sum = vmlaq_f32(sum, va, vb);
    }
    float result = vaddvq_f32(sum);
    for (; i < n; ++i) result += a[i] * b[i];
    return result;
#else
    float result = 0.0f;
    for (int i = 0; i < n; ++i) result += a[i] * b[i];
    return result;
#endif
}

void normalize(float* vec, int n) {
    float sum_sq = dot_product(vec, vec, n);
    float scale = sum_sq > 0.0f ? 1.0f / sqrtf(sum_sq) : 1.0f;
#ifdef __ARM_NEON
    float32x4_t vscale = vdupq_n_f32(scale);
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t v = vld1q_f32(vec + i);
        vst1q_f32(vec + i, vmulq_f32(v, vscale));
    }
    for (; i < n; ++i) vec[i] *= scale;
#else
    for (int i = 0; i < n; ++i) vec[i] *= scale;
#endif
}

void subtract(const float* a, const float* b, float* out, int n) {
#ifdef __ARM_NEON
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        vst1q_f32(out + i, vsubq_f32(va, vb));
    }
    for (; i < n; ++i) out[i] = a[i] - b[i];
#else
    for (int i = 0; i < n; ++i) out[i] = a[i] - b[i];
#endif
}

void multiply_add(const float* a, float scale, const float* b, float* out, int n) {
#ifdef __ARM_NEON
    float32x4_t vscale = vdupq_n_f32(scale);
    int i = 0;
    for (; i <= n - 4; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        vst1q_f32(out + i, vmlaq_f32(vb, va, vscale));
    }
    for (; i < n; ++i) out[i] = a[i] * scale + b[i];
#else
    for (int i = 0; i < n; ++i) out[i] = a[i] * scale + b[i];
#endif
}

float sum(const float* vec, int n) {
#ifdef __ARM_NEON
    float32x4_t s = vdupq_n_f32(0.0f);
    int i = 0;
    for (; i <= n - 4; i += 4) {
        s = vaddq_f32(s, vld1q_f32(vec + i));
    }
    float result = vaddvq_f32(s);
    for (; i < n; ++i) result += vec[i];
    return result;
#else
    float result = 0.0f;
    for (int i = 0; i < n; ++i) result += vec[i];
    return result;
#endif
}

float max_val(const float* vec, int n) {
    if (n <= 0) return 0.0f;
    float m = vec[0];
    for (int i = 1; i < n; ++i) {
        if (vec[i] > m) m = vec[i];
    }
    return m;
}

float min_val(const float* vec, int n) {
    if (n <= 0) return 0.0f;
    float m = vec[0];
    for (int i = 1; i < n; ++i) {
        if (vec[i] < m) m = vec[i];
    }
    return m;
}

float mean(const float* vec, int n) {
    if (n <= 0) return 0.0f;
    return sum(vec, n) / n;
}

float std_dev(const float* vec, int n, float mean_val) {
    if (n <= 1) return 0.0f;
    float sq_sum = 0.0f;
    for (int i = 0; i < n; ++i) {
        float diff = vec[i] - mean_val;
        sq_sum += diff * diff;
    }
    return sqrtf(sq_sum / n);
}

void copy(const float* src, float* dst, int n) {
#ifdef __ARM_NEON
    int i = 0;
    for (; i <= n - 16; i += 16) {
        float32x4_t v0 = vld1q_f32(src + i);
        float32x4_t v1 = vld1q_f32(src + i + 4);
        float32x4_t v2 = vld1q_f32(src + i + 8);
        float32x4_t v3 = vld1q_f32(src + i + 12);
        vst1q_f32(dst + i, v0);
        vst1q_f32(dst + i + 4, v1);
        vst1q_f32(dst + i + 8, v2);
        vst1q_f32(dst + i + 12, v3);
    }
    for (; i < n; ++i) dst[i] = src[i];
#else
    std::memcpy(dst, src, n * sizeof(float));
#endif
}

} // namespace neon
} // namespace longhun
