/**
 * 龙魂·DNA注册引擎 — HarmonyOS 原生
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-DNA-REGISTRY
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */
import { TimeStampEngine } from './TimeStampEngine';
import { SovereigntyVerifier } from './SovereigntyVerifier';
import { DatabaseHelper } from './DatabaseHelper';
import { DnaRecord, DnaGenerateRequest, SovereigntyProof } from '../models/DnaModels';

export class DnaRegistryEngine {
  private static instance: DnaRegistryEngine;
  private timeEngine: TimeStampEngine = new TimeStampEngine();
  private verifier: SovereigntyVerifier = new SovereigntyVerifier();
  private db: DatabaseHelper = new DatabaseHelper();

  private constructor() { this.init(); }
  static getInstance(): DnaRegistryEngine {
    if (!DnaRegistryEngine.instance) DnaRegistryEngine.instance = new DnaRegistryEngine();
    return DnaRegistryEngine.instance;
  }
  private async init(): Promise<void> { await this.db.initialize(); }

  async generate(request: DnaGenerateRequest): Promise<string> {
    const ganzhi = this.timeEngine.now();
    const gua = this.timeEngine.getCurrentGua();
    const hash = this.randomHash(8);
    const dna = `#龍芯⚡️${ganzhi}·${gua}-${request.module}-${request.action}-${hash}`;
    const record: DnaRecord = {
      dna, module: request.module, action: request.action, creator: 'UID9622',
      ganzhi, gua, hash, timestamp: new Date().toISOString(),
      metadata: request.metadata || {},
      sovereigntyProof: await this.verifier.generateProof(dna)
    };
    await this.db.insertDna(record);
    return dna;
  }

  async verify(dna: string): Promise<boolean> {
    if (!dna.startsWith('#龍芯⚡️')) return false;
    const record = await this.db.queryDna(dna);
    return record ? this.verifier.verifyProof(record.sovereigntyProof, dna) : false;
  }

  async queryByDna(dna: string): Promise<DnaRecord | null> { return this.db.queryDna(dna); }
  async queryByModule(module: string): Promise<DnaRecord[]> { return this.db.queryByModule(module); }
  async listAll(): Promise<DnaRecord[]> { return this.db.listAll(); }
  getCurrentTimestamp(): string { return `${this.timeEngine.now()}·${this.timeEngine.getCurrentGua()}`; }

  private randomHash(len: number): string {
    const c = '0123456789abcdef'; let r = '';
    for (let i = 0; i < len; i++) r += c[Math.floor(Math.random() * c.length)];
    return r;
  }
}
