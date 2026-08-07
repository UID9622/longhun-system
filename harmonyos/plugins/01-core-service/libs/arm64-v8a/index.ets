/**
 * DNA:   #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-LIBS-INDEX-v1.0-UID9622
 * 確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * 分層許可: 工程層 MulanPSL v2
 *
 * libs/arm64-v8a/ 目錄導出
 * 本目錄存放編譯好的 .so 文件，開發期可用 ArkTS Mock 替代
 */

// 開發期 Mock（實機部署時替換為 liblonghun_napi.so 原生模塊）
export { 
  governanceCheck,
  checkBlackhole,
  detectVeto,
  detectForbidden,
  runSupervision,
  queryMemory,
  createMemory,
  getHealth,
  triggerMeltdown,
  gateCheck,
  getVersion,
  fullSelfCheck,
  preWriteAudit,
} from '../../entry/src/main/ets/service/LonghunNapiBridge';
