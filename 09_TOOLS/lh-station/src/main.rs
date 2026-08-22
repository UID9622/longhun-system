// 龍魂代码中转站 CLI 主入口
// 任何代码进来 → 过龙魂 → 带主权标识出去
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-LH-STATION-MAIN-v1.0

mod commands;
mod core;
mod pipeline;

use clap::{Parser, Subcommand};
use std::path::PathBuf;

/// 🐉 龍魂代码中转站 — 任何代码进来，带主权出去
#[derive(Parser)]
#[command(
    name = "lh-station",
    version = "1.0.0",
    about = "龍魂代码中转站 — 代码进来，带主权标识出去",
    long_about = "转换管线: 检测 → 主权注入 → 芯片编译 → 安全审查 → GPG签名 → 打包输出\n\
                  输出代码在原始平台100%兼容，主权头仅作为注释注入。\
                  \n\n核心理念: 不是要做系统，只是要一个中转站。",
    author = "诸葛鑫 (UID9622)"
)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// 转换代码: 检测→注入→编译→审查→签名→输出
    Transform {
        /// 输入路径（文件或目录）
        input: PathBuf,

        /// 输出路径（默认 ./lh-output/）
        #[arg(short, long, default_value = "./lh-output")]
        output: PathBuf,

        /// 目标芯片 (auto/kunpeng/ascend/phytium/loongarch/sunway)
        #[arg(short, long, default_value = "auto")]
        chip: String,

        /// 是否交叉编译（默认 true）
        #[arg(long, default_value = "true")]
        cross: bool,

        /// 跳过 GPG 签名
        #[arg(long, default_value = "false")]
        no_sign: bool,
    },

    /// 初始化中转站配置
    Init,

    /// 检查代码主权状态
    Inspect {
        /// 要检查的路径
        path: PathBuf,
    },

    /// 验证已转换代码的完整性
    Verify {
        /// 要验证的路径
        path: PathBuf,
    },
}

fn main() {
    let cli = Cli::parse();

    let result = match cli.command {
        Commands::Transform { input, output, chip, cross, no_sign } => {
            commands::transform::run(input, output, chip, cross, no_sign)
        }
        Commands::Init => {
            commands::init::run()
        }
        Commands::Inspect { path } => {
            commands::inspect::run(path)
        }
        Commands::Verify { path } => {
            commands::verify::run(path)
        }
    };

    if let Err(e) = result {
        eprintln!("\n🔴 错误: {}", e);
        std::process::exit(1);
    }
}
