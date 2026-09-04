// 龍魂中转站配置管理
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-CONFIG-v1.0

use serde::{Deserialize, Serialize};
use std::path::PathBuf;

/// 中转站配置
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationConfig {
    /// 版本号
    pub station_version: String,
    /// 创建者
    pub creator: String,
    /// GPG 密钥指纹
    pub gpg_fingerprint: String,
    /// 默认输出目录
    pub default_output: String,
    /// 默认目标芯片
    pub default_chip: String,
    /// 是否默认交叉编译
    pub default_cross: bool,
    /// 是否默认签名
    pub default_sign: bool,
    /// 支持的芯片清单
    pub supported_chips: Vec<ChipInfo>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChipInfo {
    pub name: String,
    pub arch: String,
    pub os: String,
    pub abi: String,
    pub rust_target: String,
}

impl Default for StationConfig {
    fn default() -> Self {
        Self {
            station_version: "1.0.0".to_string(),
            creator: "诸葛鑫（UID9622）".to_string(),
            gpg_fingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F".to_string(),
            default_output: "./lh-output".to_string(),
            default_chip: "auto".to_string(),
            default_cross: true,
            default_sign: true,
            supported_chips: vec![
                ChipInfo {
                    name: "鲲鹏".to_string(),
                    arch: "aarch64".to_string(),
                    os: "linux".to_string(),
                    abi: "gnu".to_string(),
                    rust_target: "aarch64-unknown-linux-gnu".to_string(),
                },
                ChipInfo {
                    name: "昇腾".to_string(),
                    arch: "aarch64".to_string(),
                    os: "linux".to_string(),
                    abi: "gnu".to_string(),
                    rust_target: "aarch64-unknown-linux-gnu".to_string(),
                },
                ChipInfo {
                    name: "飞腾".to_string(),
                    arch: "aarch64".to_string(),
                    os: "linux".to_string(),
                    abi: "gnu".to_string(),
                    rust_target: "aarch64-unknown-linux-gnu".to_string(),
                },
                ChipInfo {
                    name: "龙芯".to_string(),
                    arch: "loongarch64".to_string(),
                    os: "linux".to_string(),
                    abi: "gnu".to_string(),
                    rust_target: "loongarch64-unknown-linux-gnu".to_string(),
                },
                ChipInfo {
                    name: "申威".to_string(),
                    arch: "sw_64".to_string(),
                    os: "linux".to_string(),
                    abi: "gnu".to_string(),
                    rust_target: "sw_64-unknown-linux-gnu".to_string(),
                },
            ],
        }
    }
}

impl StationConfig {
    /// 保存配置到文件
    pub fn save(&self, path: &PathBuf) -> Result<(), String> {
        let content = toml::to_string_pretty(self)
            .map_err(|e| format!("序列化失败: {}", e))?;
        std::fs::write(path, content)
            .map_err(|e| format!("写入失败: {}", e))?;
        Ok(())
    }

    /// 从文件加载配置
    pub fn load(path: &PathBuf) -> Result<Self, String> {
        let content = std::fs::read_to_string(path)
            .map_err(|e| format!("读取失败: {}", e))?;
        toml::from_str(&content)
            .map_err(|e| format!("解析失败: {}", e))
    }

    /// 查找芯片信息
    pub fn find_chip(&self, name_or_arch: &str) -> Option<&ChipInfo> {
        let query = name_or_arch.to_lowercase();
        self.supported_chips.iter().find(|c| {
            c.name.to_lowercase() == query || c.arch.to_lowercase() == query
                || c.rust_target.to_lowercase() == query
        })
    }
}
