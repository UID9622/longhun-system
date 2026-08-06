// 龍魂 DNA 生成 + 校验
// DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-DNA-ENGINE-v1.0-A7F3C2B1

use chrono::{Local, Datelike, Timelike};
use rand::Rng;
use sha2::{Sha256, Digest};

/// 天干地支数据
const TIAN_GAN: [&str; 10] = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
const DI_ZHI: [&str; 12] = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
const LIU_SI_GUA: [&str; 64] = [
    "䷀乾", "䷁坤", "䷂屯", "䷃蒙", "䷄需", "䷅讼", "䷆师", "䷇比",
    "䷈小畜", "䷉履", "䷊泰", "䷋否", "䷌同人", "䷍大有", "䷎谦", "䷏豫",
    "䷐随", "䷑蛊", "䷒临", "䷓观", "䷔噬嗑", "䷕贲", "䷖剥", "䷗复",
    "䷘无妄", "䷙大畜", "䷚颐", "䷛大过", "䷜坎", "䷝离", "䷞咸", "䷟恒",
    "䷠遁", "䷡大壮", "䷢晋", "䷣明夷", "䷤家人", "䷥睽", "䷦蹇", "䷧解",
    "䷨损", "䷩益", "䷪夬", "䷫姤", "䷬萃", "䷭升", "䷮困", "䷯井",
    "䷰革", "䷱鼎", "䷲震", "䷳艮", "䷴渐", "䷵归妹", "䷶丰", "䷷旅",
    "䷸巽", "䷹兑", "䷺涣", "䷻节", "䷼中孚", "䷽小过", "䷾既济", "䷿未济",
];

/// 生成完整的龍魂 DNA 追溯码
pub fn generate_dna(action: &str) -> String {
    let now = Local::now();
    
    // 天干地支计算
    let tg_idx = (now.year() - 4) % 10;
    let dz_idx = (now.year() - 4) % 12;
    let month_dz = (now.month() as i64 + 1) % 12; // 简化计算
    
    // 随机卦象
    let mut rng = rand::thread_rng();
    let gua = LIU_SI_GUA[rng.gen_range(0..64)];
    
    // 随机哈希
    let hash_input = format!("{}{}{}", action, now.timestamp(), rng.gen::<u64>());
    let mut hasher = Sha256::new();
    hasher.update(hash_input.as_bytes());
    let hash_result = hasher.finalize();
    let hash_hex = hex::encode(&hash_result[..4]);
    
    format!(
        "#龍芯⚡️{}·{}·{}·{}·{}-{}-{}-UID9622",
        TIAN_GAN[tg_idx as usize],
        DI_ZHI[dz_idx as usize],
        DI_ZHI[month_dz as usize],
        DI_ZHI[(now.hour() as usize / 2) % 12],
        gua,
        action.to_uppercase(),
        &hash_hex[..8]
    )
}

/// 检查文件中是否已有龍魂 DNA
pub fn has_dna(content: &str) -> bool {
    content.contains("#龍芯⚡️") || content.contains("#龍芯⚡")
}

/// 提取已有的 DNA
pub fn extract_dna(content: &str) -> Option<String> {
    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("#龍芯⚡️") || trimmed.starts_with("#龍芯⚡") {
            return Some(trimmed.to_string());
        }
    }
    None
}

/// 确认码
pub fn get_confirm_code() -> String {
    "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z".to_string()
}

/// GPG 指纹
pub fn get_gpg_fingerprint() -> String {
    "A2D0092CEE2E5BA87035600924C3704A8CC26D5F".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_dna() {
        let dna = generate_dna("TEST");
        assert!(dna.contains("#龍芯⚡️"));
        assert!(dna.contains("UID9622"));
        assert!(dna.len() > 20);
    }

    #[test]
    fn test_has_dna() {
        assert!(has_dna("#龍芯⚡️丙午·TEST"));
        assert!(!has_dna("normal code"));
    }

    #[test]
    fn test_extract_dna() {
        let content = "some code\n#龍芯⚡️丙午·TEST-ABC12345-UID9622\nmore code";
        let dna = extract_dna(content);
        assert!(dna.is_some());
        assert!(dna.unwrap().contains("TEST"));
    }
}
