// harmony_sdk/entry/src/main/ets/longhun/LonghunClient.ets
// 🐉 龙魂鸿蒙SDK v1.0
// DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-HARMONY-SDK-UID9622

import { http, util } from '@kit.NetworkKit';

export class LonghunClient {
  private gatewayUrl: string = '';
  private proxyId: string = 'harmony';
  private dna: string = '';
  private deviceId: string = '';

  constructor(gatewayUrl: string, dna: string, deviceId: string) {
    this.gatewayUrl = gatewayUrl;
    this.dna = dna;
    this.deviceId = deviceId;
  }

  private async request(url: string, method: http.RequestMethod, body?: Object, extraHeaders?: Record<string, string>): Promise<Object> {
    const request = http.createHttp();
    const payload = body ? JSON.stringify(body) : '';
    const options: http.HttpRequestOptions = {
      method: method,
      header: {
        'Content-Type': 'application/json',
        'X-Dragon-DNA': this.dna,
        'X-Proxy-ID': this.proxyId,
        'X-Device-ID': this.deviceId,
        'X-Dragon-Signature': await this.signRequest(payload),
        ...(extraHeaders || {})
      },
      extraData: payload
    };
    return new Promise((resolve, reject) => {
      request.request(url, options, (err, data) => {
        if (err) {
          reject(err);
        } else {
          try {
            resolve(JSON.parse(data.result as string));
          } catch (e) {
            resolve({ raw: data.result });
          }
        }
      });
    });
  }

  private async signRequest(data: string): Promise<string> {
    const encoder = new util.TextEncoder();
    const key = encoder.encodeInto(this.dna);
    const msg = encoder.encodeInto(data + this.dna);
    const hmac = cryptoFramework.createHmac('SHA256');
    await hmac.init({ algoName: 'HMAC', key: { format: 'RAW', data: key.data } });
    await hmac.update({ data: msg.data });
    const result = await hmac.doFinal();
    return this.bufToHex(result.data);
  }

  private bufToHex(buffer: Uint8Array): string {
    return Array.from(buffer).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  public async registerDevice(deviceInfo?: { device_name?: string; model?: string; harmony_version?: string }): Promise<Object> {
    const url = `${this.gatewayUrl}/api/harmony/register`;
    return this.request(url, http.RequestMethod.POST, {
      device_id: this.deviceId,
      device_name: deviceInfo?.device_name || '华为鸿蒙设备',
      model: deviceInfo?.model || '未知型号',
      harmony_version: deviceInfo?.harmony_version || 'HarmonyOS NEXT'
    });
  }

  public async callService(target: string, method: 'GET' | 'POST', body?: Object): Promise<Object> {
    const url = `${this.gatewayUrl}/api/proxy/${target}`;
    return this.request(url, method === 'GET' ? http.RequestMethod.GET : http.RequestMethod.POST, body);
  }

  public async queryMemory(query: string): Promise<Object> {
    return this.callService('memory', 'POST', { query });
  }

  public async executeCommand(cmd: string): Promise<Object> {
    return this.callService('task', 'POST', { command: cmd });
  }

  public async editCNSCode(code: string): Promise<Object> {
    return this.callService('cnsheditor', 'POST', { code });
  }
}
