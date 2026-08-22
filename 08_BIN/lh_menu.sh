#!/bin/bash
# -*- coding: utf-8 -*-
# =============================================================================
# 🐉 龍魂 · 全能终端菜单启动器 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁未·丙午·䷱鼎-MENU-LAUNCHER-v1.0-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 大白话: 一个菜单, 按数字键就能启动龍魂系统的各种能力。
# 多语言: 自动识别终端语言, 也支持 --lang 手动切换。
#
# 用法:
#   lh-menu                    # 自动识别语言
#   lh-menu --lang en          # 强制英文
#   lh-menu --lang zh          # 强制中文
# =============================================================================

set -euo pipefail

# ============================================================
# 多语言翻译函数
# 添加语言: 在 t() 函数里加一个 case 分支即可
# ============================================================
t() {
    local lang="$LANG_CODE"
    local key="$1"
    # DNA / 确认码 按语言显示
    case "$key" in
        dna) echo "DNA"; return ;;
        confirm)
            case "$lang" in
                zh) echo "确认码" ;;
                ja) echo "確認コード" ;;
                ko) echo "확인 코드" ;;
                fr) echo "Code de confirmation" ;;
                de) echo "Bestätigungscode" ;;
                es) echo "Código de confirmación" ;;
                ru) echo "Код подтверждения" ;;
                ar) echo "رمز التأكيد" ;;
                *) echo "Confirm Code" ;;
            esac
            return ;;
    esac

    # 中文
    if [[ "$lang" == "zh" ]]; then
        case "$key" in
            title) echo "🐉 龍魂系统 · 终端控制中心" ;;
            choose) echo "请输入选项编号" ;;
            invalid) echo "无效选项, 请重新输入" ;;
            press_any) echo "按回车键继续..." ;;
            goodbye) echo "👋 已退出龍魂控制中心" ;;
            not_implemented) echo "该功能尚未实现或暂不可用" ;;
            language_set) echo "当前语言" ;;
            opt_glyph) echo "龍字规范化守护" ;;
            opt_glyph_desc) echo $'扫描文件, 简体字形→繁体龍, 保护龍芯⚡️' ;;
            opt_search) echo "龍魂搜索底座" ;;
            opt_search_desc) echo "本地优先搜索知识图谱、认知索引、本地文件" ;;
            opt_ai) echo "本地 AI 执行" ;;
            opt_ai_desc) echo "零成本调用 Ollama / 龍魂本地模型" ;;
            opt_dashboard) echo "透明看板" ;;
            opt_dashboard_desc) echo "启动 Web 看板, 实时查看史官记录" ;;
            opt_test) echo "运行测试" ;;
            opt_test_desc) echo "跑 smoke + audit 测试, 验证底座健康" ;;
            opt_pyright) echo "类型检查" ;;
            opt_pyright_desc) echo "运行 basedpyright 检查代码" ;;
            opt_gitlens) echo "GitLens 配置" ;;
            opt_gitlens_desc) echo "查看已写入的 VSCode/GitLens 设置" ;;
            opt_exit) echo "退出" ;;
            *) echo "$key" ;;
        esac
        return
    fi

    # English
    if [[ "$lang" == "en" ]]; then
        case "$key" in
            title) echo "🐉 LongHun System · Terminal Control Center" ;;
            choose) echo "Enter option number" ;;
            invalid) echo "Invalid option, please try again" ;;
            press_any) echo "Press Enter to continue..." ;;
            goodbye) echo "👋 Exited LongHun Control Center" ;;
            not_implemented) echo "Feature not yet implemented or unavailable" ;;
            language_set) echo "Current language" ;;
            opt_glyph) echo "LongHun Glyph Guard" ;;
            opt_glyph_desc) echo $'Scan files, normalize simplified → traditional 龍, protect 龍芯⚡️' ;;
            opt_search) echo "LongHun Search Base" ;;
            opt_search_desc) echo "Local-first search over KG, cognitive index, local files" ;;
            opt_ai) echo "Local AI Exec" ;;
            opt_ai_desc) echo "Zero-cost Ollama / LongHun local model inference" ;;
            opt_dashboard) echo "Transparent Dashboard" ;;
            opt_dashboard_desc) echo "Launch Web dashboard for historian records" ;;
            opt_test) echo "Run Tests" ;;
            opt_test_desc) echo "Run smoke + audit tests to verify base health" ;;
            opt_pyright) echo "Type Check" ;;
            opt_pyright_desc) echo "Run basedpyright code checks" ;;
            opt_gitlens) echo "GitLens Config" ;;
            opt_gitlens_desc) echo "Show written VSCode/GitLens settings" ;;
            opt_exit) echo "Exit" ;;
            *) echo "$key" ;;
        esac
        return
    fi

    # 日语
    if [[ "$lang" == "ja" ]]; then
        case "$key" in
            title) echo "🐉 龍魂システム · ターミナルコントロールセンター" ;;
            choose) echo "オプション番号を入力してください" ;;
            invalid) echo "無効なオプションです。もう一度お試しください" ;;
            press_any) echo "Enterキーを押して続行..." ;;
            goodbye) echo "👋 龍魂コントロールセンターを終了しました" ;;
            opt_exit) echo "終了" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 韩语
    if [[ "$lang" == "ko" ]]; then
        case "$key" in
            title) echo "🐉 용혼 시스템 · 터미널 제어 센터" ;;
            choose) echo "옵션 번호를 입력하세요" ;;
            invalid) echo "잘못된 옵션입니다. 다시 시도하세요" ;;
            press_any) echo "Enter를 눌러 계속..." ;;
            goodbye) echo "👋 용혼 제어 센터 종료" ;;
            opt_exit) echo "종료" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 法语
    if [[ "$lang" == "fr" ]]; then
        case "$key" in
            title) echo "🐉 Système LongHun · Centre de contrôle terminal" ;;
            choose) echo "Entrez le numéro de l'option" ;;
            invalid) echo "Option invalide, veuillez réessayer" ;;
            press_any) echo "Appuyez sur Entrée pour continuer..." ;;
            goodbye) echo "👋 Centre de contrôle LongHun fermé" ;;
            opt_exit) echo "Quitter" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 西班牙语
    if [[ "$lang" == "es" ]]; then
        case "$key" in
            title) echo "🐉 Sistema LongHun · Centro de control de terminal" ;;
            choose) echo "Ingrese el número de opción" ;;
            invalid) echo "Opción inválida, intente de nuevo" ;;
            press_any) echo "Presione Enter para continuar..." ;;
            goodbye) echo "👋 Centro de control LongHun cerrado" ;;
            opt_exit) echo "Salir" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 德语
    if [[ "$lang" == "de" ]]; then
        case "$key" in
            title) echo "🐉 LongHun System · Terminal-Kontrollzentrum" ;;
            choose) echo "Optionnummer eingeben" ;;
            invalid) echo "Ungültige Option, bitte erneut versuchen" ;;
            press_any) echo "Enter drücken zum Fortfahren..." ;;
            goodbye) echo "👋 LongHun-Kontrollzentrum beendet" ;;
            opt_exit) echo "Beenden" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 俄语
    if [[ "$lang" == "ru" ]]; then
        case "$key" in
            title) echo "🐉 Система LongHun · Терминальный центр управления" ;;
            choose) echo "Введите номер опции" ;;
            invalid) echo "Неверная опция, попробуйте снова" ;;
            press_any) echo "Нажмите Enter для продолжения..." ;;
            goodbye) echo "👋 Центр управления LongHun закрыт" ;;
            opt_exit) echo "Выход" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 阿拉伯语(RTL 显示依赖终端)
    if [[ "$lang" == "ar" ]]; then
        case "$key" in
            title) echo "🐉 نظام LongHun · مركز تحكم الطرفية" ;;
            choose) echo "أدخل رقم الخيار" ;;
            invalid) echo "خيار غير صالح, يرجى المحاولة مرة أخرى" ;;
            press_any) echo "اضغط Enter للمتابعة..." ;;
            goodbye) echo "👋 تم إغلاق مركز تحكم LongHun" ;;
            opt_exit) echo "خروج" ;;
            *) t_en "$key" ;;
        esac
        return
    fi

    # 默认回退英文
    t_en "$key"
}

# 英文回退
t_en() {
    case "$1" in
        title) echo "🐉 LongHun System · Terminal Control Center" ;;
        choose) echo "Enter option number" ;;
        invalid) echo "Invalid option, please try again" ;;
        press_any) echo "Press Enter to continue..." ;;
        goodbye) echo "👋 Exited LongHun Control Center" ;;
        not_implemented) echo "Feature not yet implemented or unavailable" ;;
        language_set) echo "Current language" ;;
        opt_glyph) echo "LongHun Glyph Guard" ;;
        opt_glyph_desc) echo $'Scan files, normalize simplified → traditional 龍, protect 龍芯⚡️' ;;
        opt_search) echo "LongHun Search Base" ;;
        opt_search_desc) echo "Local-first search over KG, cognitive index, local files" ;;
        opt_ai) echo "Local AI Exec" ;;
        opt_ai_desc) echo "Zero-cost Ollama / LongHun local model inference" ;;
        opt_dashboard) echo "Transparent Dashboard" ;;
        opt_dashboard_desc) echo "Launch Web dashboard for historian records" ;;
        opt_test) echo "Run Tests" ;;
        opt_test_desc) echo "Run smoke + audit tests to verify base health" ;;
        opt_pyright) echo "Type Check" ;;
        opt_pyright_desc) echo "Run basedpyright code checks" ;;
        opt_gitlens) echo "GitLens Config" ;;
        opt_gitlens_desc) echo "Show written VSCode/GitLens settings" ;;
        opt_exit) echo "Exit" ;;
        *) echo "$1" ;;
    esac
}


# ============================================================
# 常量
# ============================================================
DNA="#龍芯⚡️丙午·丙申·丁未·丙午·䷱鼎-MENU-LAUNCHER-v1.0-UID9622"
CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
PROJECT_ROOT="$HOME/longhun-system"


# ============================================================
# 语言检测
# ============================================================
LANG_CODE="zh"
LANG_FORCED=false

_detect_lang() {
    local raw="${LANG:-zh_CN.UTF-8}"
    raw="${raw%%.*}"
    raw="${raw%%_*}"
    case "$raw" in
        en|ja|ko|fr|de|es|ru|ar) LANG_CODE="$raw" ;;
        *) LANG_CODE="zh" ;;
    esac
}

# 允许命令行强制指定
while [[ $# -gt 0 ]]; do
    case "$1" in
        --lang|-l)
            # 空值保护: set -u 下 "$2" 未设置会直接崩溃
            if [[ $# -lt 2 || -z "$2" ]]; then
                echo "❌ --lang 需要一个语言值: zh|en|ja|ko|fr|de|es|ru|ar" >&2
                exit 2
            fi
            case "$2" in
                zh|en|ja|ko|fr|de|es|ru|ar)
                    LANG_CODE="$2"
                    ;;
                *)
                    echo "⚠️ 未知语言 '$2', 回退英文" >&2
                    LANG_CODE="en"
                    ;;
            esac
            LANG_FORCED=true
            shift 2
            ;;
        --help|-h)
            echo "Usage: lh-menu [--lang zh|en|ja|ko|fr|de|es|ru|ar]"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ "$LANG_FORCED" != true ]]; then
    _detect_lang
fi


# ============================================================
# 菜单绘制
# ============================================================
_draw_menu() {
    clear 2>/dev/null || true
    echo ""
    echo "$(t title)"
    echo "============================================================"
    echo "$(t dna): $DNA"
    echo "$(t confirm): $CONFIRM"
    echo "$(t language_set): $LANG_CODE"
    echo "============================================================"
    echo ""
    echo "  1) $(t opt_glyph)      - $(t opt_glyph_desc)"
    echo "  2) $(t opt_search)     - $(t opt_search_desc)"
    echo "  3) $(t opt_ai)         - $(t opt_ai_desc)"
    echo "  4) $(t opt_dashboard)  - $(t opt_dashboard_desc)"
    echo "  5) $(t opt_test)       - $(t opt_test_desc)"
    echo "  6) $(t opt_pyright)    - $(t opt_pyright_desc)"
    echo "  7) $(t opt_gitlens)    - $(t opt_gitlens_desc)"
    echo "  0) $(t opt_exit)"
    echo ""
    echo "============================================================"
}


# ============================================================
# 能力封装
# ============================================================

_run_glyph_guard() {
    echo "🐉 $(t opt_glyph)..."
    cd "$PROJECT_ROOT" || exit 1
    python3 08_BIN/lh_dragon_glyph_guard.py --scan . --report 03_KNOWLEDGE_GRAPH/03_龍字规范化审计报告_☯UID9622-MENU.json
}

_run_search() {
    echo "🔍 $(t opt_search)..."
    local query
    read -rp "请输入搜索词 / Enter query: " query
    if [[ -z "$query" ]]; then
        echo "❌ 搜索词不能为空"
        return
    fi
    cd "$PROJECT_ROOT" || exit 1
    ./bin/lh search "$query" --n 5 --output text
}

_run_ai() {
    echo "🧠 $(t opt_ai)..."
    local prompt
    read -rp "请输入提示词 / Enter prompt: " prompt
    if [[ -z "$prompt" ]]; then
        echo "❌ 提示词不能为空"
        return
    fi
    lh-ollama "$prompt"
}

_run_dashboard() {
    echo "📊 $(t opt_dashboard)..."
    cd "$PROJECT_ROOT" || exit 1
    if [[ ! -f "08_BIN/lh_transparent_dashboard.py" ]]; then
        echo "⚠️ 08_BIN/lh_transparent_dashboard.py 不存在"
        return
    fi

    # 找可用端口, 默认 8080 被占用则递增
    local port=8080
    while nc -z 127.0.0.1 "$port" 2>/dev/null; do
        ((port++))
        if [[ "$port" -gt 8100 ]]; then
            echo "❌ 找不到可用端口 (8080-8100)"
            return
        fi
    done

    nohup python3 08_BIN/lh_transparent_dashboard.py --port "$port" > /tmp/lh_dashboard_${port}.log 2>&1 &
    local waited=0
    while [[ "$waited" -lt 5 ]]; do
        sleep 1
        if nc -z 127.0.0.1 "$port" 2>/dev/null; then
            echo "✅ 透明看板已后台启动: http://127.0.0.1:${port}"
            return
        fi
        ((waited++))
    done
    echo "⚠️ 看板进程已启动但端口 ${port} 未响应, 日志: /tmp/lh_dashboard_${port}.log"
}

_run_tests() {
    echo "🧪 $(t opt_test)..."
    cd "$PROJECT_ROOT" || exit 1
    if [[ ! -f ".venv/bin/activate" ]]; then
        echo "⚠️ 未找到 .venv/bin/activate, 请先创建虚拟环境: python3 -m venv .venv"
        return 1
    fi
    source .venv/bin/activate
    python3 -m pytest tests/test_smoke.py tests/test_code_audit.py -v
}

_run_pyright() {
    echo "🔬 $(t opt_pyright)..."
    cd "$PROJECT_ROOT" || exit 1
    local pyright_cmd=""
    if command -v basedpyright >/dev/null 2>&1; then
        pyright_cmd="basedpyright"
    elif [[ -x ".venv/bin/basedpyright" ]]; then
        pyright_cmd=".venv/bin/basedpyright"
    else
        echo "⚠️ basedpyright 未安装 (全局 PATH 或 .venv/bin/basedpyright)"
        return 1
    fi
    "$pyright_cmd" bin/lh_base_trace_collector.py tests/test_code_audit.py tests/test_smoke.py
}

_show_gitlens_config() {
    echo "🔧 $(t opt_gitlens)..."
    local cfg="$HOME/Library/Application Support/Code/User/settings.json"
    if [[ -f "$cfg" ]]; then
        echo "✅ 已写入 $cfg"
        grep -A1 -B1 "gitlens" "$cfg" || true
    else
        echo "⚠️ 未找到 VSCode 用户设置"
    fi
}


# ============================================================
# 主循环
# ============================================================
main() {
    while true; do
        _draw_menu
        # EOF(Ctrl+D) 优雅退出, 不因 set -e 直接崩
        read -rp "$(t choose): " choice || { echo ""; echo "$(t goodbye)"; exit 0; }
        echo ""

        # 每个功能用 || 兜底: set -e 下子命令返回非零时回到菜单而非退出
        case "$choice" in
            1) _run_glyph_guard || echo "⚠️ $(t opt_glyph) 异常 (退出码 $?)" ;;
            2) _run_search || echo "⚠️ $(t opt_search) 异常 (退出码 $?)" ;;
            3) _run_ai || echo "⚠️ $(t opt_ai) 异常 (退出码 $?)" ;;
            4) _run_dashboard || echo "⚠️ $(t opt_dashboard) 异常 (退出码 $?)" ;;
            5) _run_tests || echo "⚠️ $(t opt_test) 异常 (退出码 $?)" ;;
            6) _run_pyright || echo "⚠️ $(t opt_pyright) 异常 (退出码 $?)" ;;
            7) _show_gitlens_config || echo "⚠️ $(t opt_gitlens) 异常 (退出码 $?)" ;;
            0)
                echo "$(t goodbye)"
                exit 0
                ;;
            *)
                echo "❌ $(t invalid)"
                ;;
        esac

        echo ""
        read -rp "$(t press_any)" _ || { echo ""; break; }
    done
}

main
