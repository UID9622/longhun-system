/**
 * 龍魂面板 JS v3.6
 * DNA: #龍芯⚡️丙午·辛未·PANEL-JS-v3.6
 *
 * 新增:
 *  - 训练进度实时轮询（每2秒）
 *  - Canvas进化时间轴图表（准确率曲线+样本柱状图+耗时散点）
 *  - 训练完成通知
 *  - 鼠标悬停数据点交互
 *  - Alt+T 快捷键打开时间轴
 */

const VERIFY_API = '/training-api';
const POLL_INTERVAL = 2000;  // 2秒轮询
const DNA = 'UID9622-ONLY-ONCE🧬LK9X-772Z';

// ═══════════════════════════════════════════════════════
// 图表配置
// ═══════════════════════════════════════════════════════

const CHART_CONFIG = {
    colors: {
        primary: '#c41e3a',
        primaryGlow: '#ff2d55',
        secondary: '#d4af37',
        success: '#00c853',
        warning: '#ff9100',
        danger: '#ff1744',
        grid: '#2a2a3a',
        text: '#8a8a9a',
        textLight: '#e8e8f0',
        bg: '#12121a'
    },
    fonts: {
        mono: "'Courier New', monospace",
        sans: "-apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif"
    }
};

// ═══════════════════════════════════════════════════════
// 全局状态
// ═══════════════════════════════════════════════════════

let trainingPollInterval = null;
let currentModelVersion = null;
let timelineData = null;
let timelineModal = null;

// ═══════════════════════════════════════════════════════
// 训练状态轮询
// ═══════════════════════════════════════════════════════

function startTrainingPoll() {
    if (trainingPollInterval) return;

    trainingPollInterval = setInterval(async () => {
        await checkTrainingStatus();
    }, POLL_INTERVAL);

    checkTrainingStatus();
}

async function checkTrainingStatus() {
    try {
        const resp = await fetch(`${VERIFY_API}/training/status`);
        const status = await resp.json();
        updateTrainingDisplay(status);

        if (status.state === 'done' && status.to_version !== currentModelVersion) {
            showTrainingCompleteNotification(status);
            currentModelVersion = status.to_version;
            await updateModelVersionDisplay();
        }

        if (status.state === 'idle' && trainingPollInterval) {
            // 空闲时保持低频轮询，发现训练自动恢复高频
        }
    } catch (e) {
        console.log('训练状态查询失败:', e.message);
    }
}

async function updateModelVersionDisplay() {
    try {
        const resp = await fetch(`${VERIFY_API}/model/version`);
        const data = await resp.json();
        const modelEl = document.getElementById('lh-model-version');
        if (modelEl && data.version) {
            const acc = data.metrics?.accuracy ? (data.metrics.accuracy * 100).toFixed(0) : '--';
            const samples = data.training_samples ? (data.training_samples / 1000).toFixed(1) + 'k' : '--';
            modelEl.textContent = `AIv${data.version} | ${acc}% | ${samples}`;
            modelEl.title = '点击查看AI进化时间轴 (Alt+T)';
            modelEl.style.cursor = 'pointer';
            modelEl.onclick = async () => {
                await loadTimeline();
                showTimelineModal();
            };
        }
    } catch (e) {
        console.log('版本查询失败:', e.message);
    }
}

// ═══════════════════════════════════════════════════════
// 训练进度显示
// ═══════════════════════════════════════════════════════

function updateTrainingDisplay(status) {
    const modelEl = document.getElementById('lh-model-version');
    if (!modelEl) return;

    // 移除旧指示器
    const oldIndicator = document.getElementById('lh-training-indicator');
    if (oldIndicator) oldIndicator.remove();

    if (status.state === 'idle') {
        modelEl.style.opacity = '1';
        return;
    }

    // 训练中：淡化版本号，显示进度
    modelEl.style.opacity = '0.3';

    const indicator = document.createElement('div');
    indicator.id = 'lh-training-indicator';

    const progress = status.progress || 0;
    const stage = status.stage || '处理中...';
    const fromVer = status.from_version || '?';
    const toVer = status.to_version || '?';

    let progressColor = '#c41e3a';
    if (progress > 80) progressColor = '#00c853';
    else if (progress > 50) progressColor = '#d4af37';

    let timeInfo = '';
    if (status.remaining_formatted) {
        timeInfo = `预计剩余: ${status.remaining_formatted}`;
    } else if (status.elapsed_formatted) {
        timeInfo = `已用: ${status.elapsed_formatted}`;
    }

    if (status.state === 'error') {
        indicator.innerHTML = `
            <div style="text-align:center;">
                <div style="font-size:24px;margin-bottom:8px;">❌</div>
                <div style="color:#ff1744;font-weight:700;margin-bottom:8px;">训练失败</div>
                <div style="color:#8a8a9a;font-size:12px;">${status.error || '未知错误'}</div>
                <div style="color:#5a5a6a;font-size:10px;margin-top:8px;">已回滚至 AIv${fromVer}</div>
            </div>`;
        indicator.style.cssText = errorIndicatorStyle();
        document.body.appendChild(indicator);
        setTimeout(() => { indicator.remove(); modelEl.style.opacity = '1'; }, 8000);
        return;
    }

    indicator.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span class="lh-spin-anim" style="font-size:20px;">🐉</span>
                <span style="color:#c41e3a;font-weight:700;font-size:14px;letter-spacing:2px;">龍魂AI模型进化中</span>
            </div>
            <span style="color:#5a5a6a;font-size:11px;font-family:monospace;">${status.state.toUpperCase()}</span>
        </div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
            <span style="color:#8a8a9a;font-size:12px;">AIv${fromVer}</span>
            <span style="color:#c41e3a;font-size:16px;">→</span>
            <span style="color:#d4af37;font-size:12px;font-weight:700;">AIv${toVer}</span>
        </div>
        <div style="background:#1a1a24;border-radius:8px;height:8px;overflow:hidden;margin-bottom:8px;">
            <div class="lh-progress-bar" style="width:${progress}%;background:linear-gradient(90deg,${progressColor},${progressColor}88);box-shadow:0 0 8px ${progressColor}44;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="color:#8a8a9a;font-size:11px;">${stage}</span>
            <span style="color:#d4af37;font-family:monospace;font-size:12px;font-weight:700;">${progress.toFixed(1)}%</span>
        </div>
        <div style="color:#5a5a6a;font-size:10px;margin-top:8px;text-align:right;">${timeInfo}</div>
        ${status.metrics?.samples ? `
        <div style="color:#5a5a6a;font-size:10px;margin-top:4px;border-top:1px solid #2a2a3a;padding-top:8px;">
            训练样本: ${status.metrics.samples.toLocaleString()} | Epoch: ${status.metrics.epoch || '-'}/10
        </div>` : ''}
    `;

    indicator.style.cssText = trainingIndicatorStyle();
    document.body.appendChild(indicator);
}

function trainingIndicatorStyle() {
    return `
        position:fixed; bottom:50px; left:50%; transform:translateX(-50%);
        background:linear-gradient(135deg,rgba(10,10,15,0.98),rgba(26,10,10,0.98));
        border:1px solid #c41e3a; border-radius:16px; padding:20px 32px;
        z-index:10003; min-width:400px;
        box-shadow:0 8px 32px rgba(196,30,58,0.3);
        animation:lh-slide-up 0.5s ease;
    `;
}

function errorIndicatorStyle() {
    return `
        position:fixed; bottom:50px; left:50%; transform:translateX(-50%);
        background:linear-gradient(135deg,rgba(10,10,15,0.98),rgba(26,10,10,0.98));
        border:1px solid #ff1744; border-radius:16px; padding:20px 32px;
        z-index:10003; min-width:400px;
        box-shadow:0 8px 32px rgba(255,23,68,0.3);
        animation:lh-slide-up 0.5s ease;
    `;
}

function showTrainingCompleteNotification(status) {
    const metrics = status.metrics || {};
    const notification = document.createElement('div');
    notification.style.cssText = `
        position:fixed; top:80px; right:20px;
        background:linear-gradient(135deg,rgba(0,200,83,0.15),rgba(0,200,83,0.05));
        border:1px solid rgba(0,200,83,0.3); border-radius:12px;
        padding:16px 20px; z-index:10004; min-width:280px;
        animation:lh-notif-in 0.5s ease;
        box-shadow:0 4px 16px rgba(0,200,83,0.2);
    `;
    notification.innerHTML = `
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:20px;">✅</span>
            <span style="color:#00c853;font-weight:700;font-size:14px;">模型进化完成</span>
        </div>
        <div style="color:#e8e8f0;font-size:13px;margin-bottom:4px;">AIv${status.from_version} → AIv${status.to_version}</div>
        <div style="color:#8a8a9a;font-size:11px;">
            准确率: ${((metrics.accuracy || 0) * 100).toFixed(1)}% | 样本: ${(metrics.training_samples || 0).toLocaleString()}
        </div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'lh-notif-out 0.5s ease forwards';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

// ═══════════════════════════════════════════════════════
// 时间轴加载
// ═══════════════════════════════════════════════════════

async function loadTimeline() {
    try {
        const resp = await fetch(`${VERIFY_API}/training/timeline?limit=20`);
        timelineData = await resp.json();
        return timelineData;
    } catch (e) {
        console.log('时间轴加载失败:', e.message);
        return null;
    }
}

// ═══════════════════════════════════════════════════════
// Canvas 进化图表
// ═══════════════════════════════════════════════════════

function createEvolutionChart(container, timeline) {
    const canvas = document.createElement('canvas');
    canvas.id = 'lh-evolution-chart';
    canvas.style.cssText = 'width:100%;height:300px;margin-bottom:30px;';

    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = 300 * dpr;

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    drawAccuracyCurve(ctx, timeline, rect.width, 300);
    drawSamplesBars(ctx, timeline, rect.width, 300);
    drawTrainingScatter(ctx, timeline, rect.width, 300);
    addChartInteraction(canvas, timeline);

    container.insertBefore(canvas, container.firstChild);

    // 入场动画
    setTimeout(() => animateChart(canvas, timeline), 100);

    return canvas;
}

function drawAccuracyCurve(ctx, timeline, width, height) {
    const padding = { top: 40, right: 60, bottom: 40, left: 60 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;
    const { colors } = CHART_CONFIG;

    const versions = timeline.map((_, i) => i + 1);
    const accuracies = timeline.map(t => t.metrics.accuracy);
    const minAcc = Math.min(...accuracies) - 2;
    const maxAcc = Math.max(...accuracies) + 2;

    const xScale = (i) => padding.left + (i / Math.max(1, versions.length - 1)) * chartWidth;
    const yScale = (acc) => padding.top + chartHeight - ((acc - minAcc) / (maxAcc - minAcc)) * chartHeight;

    // 网格
    ctx.strokeStyle = colors.grid;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 5; i++) {
        const y = padding.top + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(padding.left + chartWidth, y);
        ctx.stroke();

        const acc = maxAcc - ((maxAcc - minAcc) / 5) * i;
        ctx.fillStyle = colors.text;
        ctx.font = `10px ${CHART_CONFIG.fonts.mono}`;
        ctx.textAlign = 'right';
        ctx.fillText(`${acc.toFixed(0)}%`, padding.left - 10, y + 3);
    }

    // X轴
    timeline.forEach((t, i) => {
        const x = xScale(i);
        ctx.fillStyle = i === timeline.length - 1 ? colors.primary : colors.text;
        ctx.font = `11px ${CHART_CONFIG.fonts.mono}`;
        ctx.textAlign = 'center';
        ctx.fillText(`v${t.version}`, x, padding.top + chartHeight + 20);
    });

    // 标题
    ctx.fillStyle = colors.textLight;
    ctx.font = `bold 12px ${CHART_CONFIG.fonts.sans}`;
    ctx.textAlign = 'left';
    ctx.fillText('准确率进化曲线', padding.left, 20);

    // 趋势线
    if (timeline.length > 1) {
        const n = timeline.length;
        const sumX = versions.reduce((a, b) => a + b, 0);
        const sumY = accuracies.reduce((a, b) => a + b, 0);
        const sumXY = versions.reduce((sum, x, i) => sum + x * accuracies[i], 0);
        const sumX2 = versions.reduce((sum, x) => sum + x * x, 0);
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        ctx.beginPath();
        ctx.strokeStyle = colors.success;
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        ctx.moveTo(xScale(0), yScale(slope * 1 + intercept));
        ctx.lineTo(xScale(n - 1), yScale(slope * n + intercept));
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = colors.success;
        ctx.font = `10px ${CHART_CONFIG.fonts.mono}`;
        ctx.textAlign = 'right';
        const trend = slope > 0 ? '↗' : slope < 0 ? '↘' : '→';
        ctx.fillText(`趋势: ${trend} ${(slope * 100).toFixed(2)}%/版本`, width - padding.right, 20);
    }

    // 曲线
    ctx.beginPath();
    ctx.strokeStyle = colors.primary;
    ctx.lineWidth = 2;
    timeline.forEach((t, i) => {
        const x = xScale(i), y = yScale(t.metrics.accuracy);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // 发光
    ctx.beginPath();
    ctx.strokeStyle = colors.primaryGlow;
    ctx.lineWidth = 4;
    ctx.globalAlpha = 0.3;
    timeline.forEach((t, i) => {
        const x = xScale(i), y = yScale(t.metrics.accuracy);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.globalAlpha = 1;

    // 数据点
    timeline.forEach((t, i) => {
        const x = xScale(i), y = yScale(t.metrics.accuracy);
        const isLatest = i === timeline.length - 1;

        if (isLatest) {
            ctx.beginPath();
            ctx.arc(x, y, 10, 0, Math.PI * 2);
            ctx.fillStyle = colors.primary;
            ctx.globalAlpha = 0.2;
            ctx.fill();
            ctx.globalAlpha = 1;
        }

        ctx.beginPath();
        ctx.arc(x, y, isLatest ? 6 : 4, 0, Math.PI * 2);
        ctx.fillStyle = isLatest ? colors.primary : colors.secondary;
        ctx.fill();
        ctx.strokeStyle = colors.bg;
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = isLatest ? colors.primary : colors.textLight;
        ctx.font = `bold ${isLatest ? 12 : 10}px ${CHART_CONFIG.fonts.mono}`;
        ctx.textAlign = 'center';
        ctx.fillText(`${t.metrics.accuracy}%`, x, y - 15);
    });
}

function drawSamplesBars(ctx, timeline, width, height) {
    const barHeight = 60;
    const barY = height - barHeight - 10;
    const padding = { left: 60, right: 60 };
    const chartWidth = width - padding.left - padding.right;
    const { colors } = CHART_CONFIG;
    const maxSamples = Math.max(...timeline.map(t => t.metrics.samples));

    timeline.forEach((t, i) => {
        const x = padding.left + (i / Math.max(1, timeline.length - 1)) * chartWidth;
        const barW = chartWidth / Math.max(1, timeline.length) * 0.6;
        const barH = maxSamples > 0 ? (t.metrics.samples / maxSamples) * barHeight : 0;

        ctx.fillStyle = i === timeline.length - 1 ? colors.primary : colors.secondary;
        ctx.globalAlpha = 0.3;
        ctx.fillRect(x - barW / 2, barY + barHeight - barH, barW, barH);
        ctx.globalAlpha = 1;

        ctx.fillStyle = colors.text;
        ctx.font = `9px ${CHART_CONFIG.fonts.mono}`;
        ctx.textAlign = 'center';
        ctx.fillText(`${t.metrics.samples_k}k`, x, barY + barHeight - barH - 5);
    });

    ctx.fillStyle = colors.text;
    ctx.font = `10px ${CHART_CONFIG.fonts.sans}`;
    ctx.textAlign = 'left';
    ctx.fillText('样本增长', padding.left, barY + barHeight + 15);
}

function drawTrainingScatter(ctx, timeline, width, height) {
    const scatterSize = 80;
    const scatterX = width - scatterSize - 20;
    const scatterY = 40;
    const { colors } = CHART_CONFIG;

    ctx.fillStyle = colors.bg;
    ctx.fillRect(scatterX, scatterY, scatterSize, scatterSize);
    ctx.strokeStyle = colors.grid;
    ctx.lineWidth = 0.5;
    ctx.strokeRect(scatterX, scatterY, scatterSize, scatterSize);

    ctx.fillStyle = colors.text;
    ctx.font = `9px ${CHART_CONFIG.fonts.sans}`;
    ctx.textAlign = 'left';
    ctx.fillText('训练耗时', scatterX, scatterY - 5);

    const maxDuration = Math.max(...timeline.map(t => t.metrics.duration_seconds || 1));

    timeline.forEach((t, i) => {
        const duration = t.metrics.duration_seconds || 0;
        const x = scatterX + (i / Math.max(1, timeline.length - 1)) * scatterSize;
        const y = scatterY + scatterSize - (maxDuration > 0 ? (duration / maxDuration) * scatterSize : 0);

        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = i === timeline.length - 1 ? colors.primary : colors.text;
        ctx.fill();
    });

    ctx.beginPath();
    ctx.strokeStyle = colors.grid;
    ctx.lineWidth = 0.5;
    timeline.forEach((t, i) => {
        const duration = t.metrics.duration_seconds || 0;
        const x = scatterX + (i / Math.max(1, timeline.length - 1)) * scatterSize;
        const y = scatterY + scatterSize - (maxDuration > 0 ? (duration / maxDuration) * scatterSize : 0);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

// ═══════════════════════════════════════════════════════
// 图表动画
// ═══════════════════════════════════════════════════════

function animateChart(canvas, timeline) {
    const dpr = window.devicePixelRatio || 1;
    const ctx = canvas.getContext('2d');
    const width = canvas.width / dpr;
    const height = canvas.height / dpr;

    let progress = 0;
    const duration = 1500;
    const startTime = Date.now();

    function frame() {
        const elapsed = Date.now() - startTime;
        progress = Math.min(1, elapsed / duration);
        const ease = 1 - Math.pow(1 - progress, 3);
        const visibleCount = Math.max(1, Math.floor(timeline.length * ease));
        const visibleData = timeline.slice(0, visibleCount);

        ctx.clearRect(0, 0, width, height);
        drawAccuracyCurve(ctx, visibleData, width, height);
        drawSamplesBars(ctx, visibleData, width, height);
        drawTrainingScatter(ctx, visibleData, width, height);

        if (progress < 1) {
            requestAnimationFrame(frame);
        } else {
            // 全部数据重绘一次确保完整
            ctx.clearRect(0, 0, width, height);
            drawAccuracyCurve(ctx, timeline, width, height);
            drawSamplesBars(ctx, timeline, width, height);
            drawTrainingScatter(ctx, timeline, width, height);
        }
    }

    requestAnimationFrame(frame);
}

// ═══════════════════════════════════════════════════════
// 图表交互
// ═══════════════════════════════════════════════════════

function addChartInteraction(canvas, timeline) {
    const tooltip = document.createElement('div');
    tooltip.className = 'lh-chart-tooltip';
    tooltip.style.cssText = `
        position:absolute; background:rgba(10,10,15,0.95);
        border:1px solid #c41e3a; border-radius:8px;
        padding:8px 12px; font-size:11px; color:#e8e8f0;
        pointer-events:none; z-index:100;
        font-family:'Courier New',monospace;
        box-shadow:0 4px 12px rgba(196,30,58,0.3);
        opacity:0; transition:opacity 0.2s;
    `;
    canvas.parentNode.appendChild(tooltip);

    const padding = { top: 40, right: 60, bottom: 40, left: 60 };
    const dpr = window.devicePixelRatio || 1;

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const chartWidth = rect.width - padding.left - padding.right;

        let closest = -1, minDist = Infinity;
        timeline.forEach((_, i) => {
            const px = padding.left + (i / Math.max(1, timeline.length - 1)) * chartWidth;
            const dist = Math.abs(x - px);
            if (dist < minDist && dist < 30) { minDist = dist; closest = i; }
        });

        if (closest >= 0) {
            const t = timeline[closest];
            const evo = t.evolution || {};
            tooltip.innerHTML = `
                <div style="color:#c41e3a;font-weight:700;margin-bottom:4px;">AIv${t.version}</div>
                <div>准确率: <span style="color:#d4af37;">${t.metrics.accuracy}%</span></div>
                <div>样本: <span style="color:#e8e8f0;">${t.metrics.samples_k}k</span></div>
                <div>耗时: <span style="color:#8a8a9a;">${t.metrics.duration_formatted}</span></div>
                ${evo.accuracy_delta ? `
                <div style="margin-top:4px;color:${evo.accuracy_delta > 0 ? '#00c853' : '#ff1744'};">
                    ${evo.accuracy_delta > 0 ? '↗' : '↘'} ${Math.abs(evo.accuracy_delta).toFixed(2)}%
                </div>` : ''}
            `;
            tooltip.style.left = `${e.clientX - rect.left + 10}px`;
            tooltip.style.top = `${e.clientY - rect.top - 10}px`;
            tooltip.style.opacity = '1';
            canvas.style.cursor = 'pointer';
        } else {
            tooltip.style.opacity = '0';
            canvas.style.cursor = 'default';
        }
    });

    canvas.addEventListener('mouseleave', () => { tooltip.style.opacity = '0'; });

    canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const chartWidth = rect.width - padding.left - padding.right;

        timeline.forEach((t, i) => {
            const px = padding.left + (i / Math.max(1, timeline.length - 1)) * chartWidth;
            if (Math.abs(x - px) < 30) {
                const card = document.querySelector(`.lh-timeline-card[data-version="${t.version}"]`);
                if (card) {
                    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    card.style.animation = 'lh-pulse 1s ease';
                    setTimeout(() => card.style.animation = '', 1000);
                }
            }
        });
    });
}

// ═══════════════════════════════════════════════════════
// 时间轴模态框
// ═══════════════════════════════════════════════════════

function showTimelineModal() {
    if (timelineModal) { timelineModal.remove(); timelineModal = null; return; }
    if (!timelineData) return;

    const timeline = timelineData.timeline || [];
    const stats = timelineData.stats || {};

    timelineModal = document.createElement('div');
    timelineModal.id = 'lh-timeline-modal';
    timelineModal.style.cssText = `
        position:fixed; top:0; left:0; right:0; bottom:0;
        background:rgba(10,10,15,0.95); z-index:10005;
        overflow-y:auto; padding:40px 20px;
        animation:lh-fade-in 0.3s ease;
    `;

    // 生成时间轴卡片
    let timelineHTML = '';
    timeline.forEach((item, index) => {
        const isLatest = index === timeline.length - 1;
        const isFirst = index === 0;
        const evo = item.evolution || {};

        let trendIcon = '➡️', trendColor = '#8a8a9a';
        if (evo.accuracy_trend === 'up') { trendIcon = '↗️'; trendColor = '#00c853'; }
        else if (evo.accuracy_trend === 'down') { trendIcon = '↘️'; trendColor = '#ff1744'; }

        timelineHTML += `
            <div style="display:flex;gap:20px;margin-bottom:${isLatest ? '0' : '30px'};position:relative;">
                ${!isLatest ? `<div style="position:absolute;left:24px;top:48px;bottom:-30px;width:2px;background:linear-gradient(180deg,#c41e3a,transparent);"></div>` : ''}
                <div style="width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;flex-shrink:0;z-index:1;
                    ${isLatest ? 'background:linear-gradient(135deg,#c41e3a,#ff2d55);box-shadow:0 0 20px rgba(196,30,58,0.5);border:2px solid #ff2d55;' : 'background:linear-gradient(135deg,#1a1a24,#2a2a3a);border:1px solid #3a3a4a;'}">
                    ${isLatest ? '👑' : item.version}
                </div>
                <div class="lh-timeline-card" data-version="${item.version}" style="
                    flex:1;background:linear-gradient(135deg,#12121a,#1a1a24);
                    border:1px solid ${isLatest ? 'rgba(196,30,58,0.3)' : '#2a2a3a'};
                    border-radius:12px;padding:16px 20px;transition:all 0.3s;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                        <div style="display:flex;align-items:center;gap:10px;">
                            <span style="padding:4px 12px;border-radius:20px;font-size:12px;font-family:'Courier New',monospace;
                                ${isLatest ? 'background:linear-gradient(135deg,#c41e3a,#ff2d55);color:white;font-weight:800;' : 'background:rgba(212,175,55,0.15);color:#d4af37;'}">
                                ${item.badge}</span>
                            ${isLatest ? '<span style="color:#c41e3a;font-size:11px;font-weight:600;">当前版本</span>' : ''}
                        </div>
                        <span style="color:#5a5a6a;font-size:11px;font-family:monospace;">${item.trained_at_formatted}</span>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px;">
                        <div style="text-align:center;padding:10px;background:rgba(0,0,0,0.2);border-radius:8px;">
                            <div style="color:#d4af37;font-size:20px;font-weight:700;font-family:monospace;">${item.metrics.accuracy}%</div>
                            <div style="color:#5a5a6a;font-size:10px;margin-top:4px;">准确率</div>
                            ${!isFirst ? `<div style="color:${trendColor};font-size:10px;margin-top:2px;">${trendIcon} ${Math.abs(evo.accuracy_delta).toFixed(2)}%</div>` : ''}
                        </div>
                        <div style="text-align:center;padding:10px;background:rgba(0,0,0,0.2);border-radius:8px;">
                            <div style="color:#e8e8f0;font-size:20px;font-weight:700;font-family:monospace;">${item.metrics.samples_k}k</div>
                            <div style="color:#5a5a6a;font-size:10px;margin-top:4px;">训练样本</div>
                            ${!isFirst ? `<div style="color:${evo.samples_delta > 0 ? '#00c853' : '#8a8a9a'};font-size:10px;margin-top:2px;">${evo.samples_delta > 0 ? '+' : ''}${evo.samples_delta}</div>` : ''}
                        </div>
                        <div style="text-align:center;padding:10px;background:rgba(0,0,0,0.2);border-radius:8px;">
                            <div style="color:#8a8a9a;font-size:20px;font-weight:700;font-family:monospace;">${item.metrics.duration_formatted}</div>
                            <div style="color:#5a5a6a;font-size:10px;margin-top:4px;">训练耗时</div>
                            ${!isFirst ? `<div style="color:#5a5a6a;font-size:10px;margin-top:2px;">间隔: ${evo.time_since_last_formatted}</div>` : ''}
                        </div>
                    </div>
                    <div class="timeline-detail" style="display:none;margin-top:12px;padding-top:12px;border-top:1px solid #2a2a3a;">
                        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:11px;color:#8a8a9a;">
                            <div>F1分数: <span style="color:#e8e8f0;">${item.metrics.f1}%</span></div>
                            <div>触发原因: <span style="color:#e8e8f0;">${item.trigger}</span></div>
                            <div>DNA: <span style="color:#c41e3a;font-family:monospace;">${(item.dna || '').substring(0, 20)}...</span></div>
                            <div>时间戳: <span style="color:#e8e8f0;font-family:monospace;">${item.trained_at}</span></div>
                        </div>
                    </div>
                    <div style="text-align:center;margin-top:8px;">
                        <button onclick="toggleTimelineDetail(${item.version})" style="background:transparent;border:1px solid #2a2a3a;color:#5a5a6a;padding:4px 16px;border-radius:12px;font-size:11px;cursor:pointer;">详情</button>
                    </div>
                </div>
            </div>`;
    });

    timelineModal.innerHTML = `
        <div style="max-width:800px;margin:0 auto;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:40px;padding-bottom:20px;border-bottom:1px solid #2a2a3a;">
                <div>
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                        <span style="font-size:32px;">🐉</span>
                        <span style="color:#c41e3a;font-size:24px;font-weight:800;letter-spacing:2px;">龍魂AI进化时间轴</span>
                    </div>
                    <div style="color:#5a5a6a;font-size:12px;font-family:monospace;">${timelineData.evolution_path || ''}</div>
                </div>
                <button onclick="closeTimelineModal()" style="background:transparent;border:1px solid #2a2a3a;color:#8a8a9a;width:40px;height:40px;border-radius:50%;font-size:20px;cursor:pointer;">×</button>
            </div>

            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:40px;">
                <div style="background:linear-gradient(135deg,#12121a,#1a0a0a);border:1px solid #2a2a3a;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#d4af37;font-size:28px;font-weight:700;font-family:monospace;">${stats.total_versions || 0}</div>
                    <div style="color:#5a5a6a;font-size:11px;margin-top:4px;">总版本数</div>
                </div>
                <div style="background:linear-gradient(135deg,#12121a,#1a0a0a);border:1px solid #2a2a3a;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#00c853;font-size:28px;font-weight:700;font-family:monospace;">${stats.best_accuracy || 0}%</div>
                    <div style="color:#5a5a6a;font-size:11px;margin-top:4px;">最高准确率</div>
                </div>
                <div style="background:linear-gradient(135deg,#12121a,#1a0a0a);border:1px solid #2a2a3a;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#e8e8f0;font-size:28px;font-weight:700;font-family:monospace;">${stats.avg_accuracy || 0}%</div>
                    <div style="color:#5a5a6a;font-size:11px;margin-top:4px;">平均准确率</div>
                </div>
                <div style="background:linear-gradient(135deg,#12121a,#1a0a0a);border:1px solid #2a2a3a;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#c41e3a;font-size:28px;font-weight:700;font-family:monospace;">+${stats.total_samples_growth || 0}</div>
                    <div style="color:#5a5a6a;font-size:11px;margin-top:4px;">样本增长</div>
                </div>
            </div>

            <div id="lh-chart-container" style="background:linear-gradient(135deg,#12121a,#1a1a24);border:1px solid #2a2a3a;border-radius:16px;padding:20px;margin-bottom:40px;overflow:hidden;position:relative;"></div>

            <div style="padding-left:20px;">${timelineHTML}</div>

            <div style="text-align:center;margin-top:40px;padding-top:20px;border-top:1px solid #2a2a3a;color:#5a5a6a;font-size:11px;">
                <span style="color:#c41e3a;">🐉</span> 龍魂系统 v1.7 | 龍芯北辰 UID9622 | 主权归人民
            </div>
        </div>
    `;

    // 注入动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes lh-fade-in { from{opacity:0;} to{opacity:1;} }
        @keyframes lh-slide-up { from{opacity:0;transform:translateX(-50%) translateY(20px);} to{opacity:1;transform:translateX(-50%) translateY(0);} }
        @keyframes lh-notif-in { from{opacity:0;transform:translateX(100px);} to{opacity:1;transform:translateX(0);} }
        @keyframes lh-notif-out { from{opacity:1;transform:translateX(0);} to{opacity:0;transform:translateX(100px);} }
        @keyframes lh-spin { from{transform:rotate(0deg);} to{transform:rotate(360deg);} }
        @keyframes lh-pulse { 0%,100%{box-shadow:0 0 0 rgba(196,30,58,0);} 50%{box-shadow:0 0 20px rgba(196,30,58,0.5);} }
        .lh-spin-anim { animation:lh-spin 2s linear infinite; }
        .lh-progress-bar { border-radius:8px;height:100%;transition:width 0.5s ease; }
        .lh-timeline-card:hover { border-color:rgba(196,30,58,0.3)!important; transform:translateX(4px); }
        #lh-evolution-chart { display:block;width:100%;image-rendering:crisp-edges; }
    `;
    timelineModal.appendChild(style);
    document.body.appendChild(timelineModal);

    // 绘制 Canvas 图表
    const chartContainer = document.getElementById('lh-chart-container');
    if (chartContainer) {
        createEvolutionChart(chartContainer, timeline);
    }
}

function closeTimelineModal() {
    if (timelineModal) {
        timelineModal.style.animation = 'lh-fade-out 0.3s ease forwards';
        setTimeout(() => { timelineModal.remove(); timelineModal = null; }, 300);
    }
}

function toggleTimelineDetail(version) {
    const card = document.querySelector(`.lh-timeline-card[data-version="${version}"]`);
    if (!card) return;
    const detail = card.querySelector('.timeline-detail');
    if (!detail) return;
    detail.style.display = detail.style.display === 'none' ? 'block' : 'none';
}

// ═══════════════════════════════════════════════════════
// 键盘快捷键
// ═══════════════════════════════════════════════════════

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && timelineModal) {
        closeTimelineModal();
    }
    if (e.key === 't' && e.altKey && !timelineModal) {
        loadTimeline().then(() => showTimelineModal());
    }
});

// ═══════════════════════════════════════════════════════
// 响应式重绘
// ═══════════════════════════════════════════════════════

window.addEventListener('resize', () => {
    const canvas = document.getElementById('lh-evolution-chart');
    if (canvas && timelineData) {
        const container = canvas.parentNode;
        canvas.remove();
        createEvolutionChart(container, timelineData.timeline);
    }
});

// ═══════════════════════════════════════════════════════
// 初始化
// ═══════════════════════════════════════════════════════

function init() {
    console.log('🐉 龍魂面板 v3.6 初始化');
    startTrainingPoll();
    updateModelVersionDisplay();
}

// DOM 加载完成后自动初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
