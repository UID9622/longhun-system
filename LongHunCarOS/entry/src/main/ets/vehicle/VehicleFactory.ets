/**
 * 🐉 龍魂 · 车辆工厂
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-VEHICLE-FACTORY-v2.0-UID9622
 */
import { HuaweiAdapter, HuaweiVehicleInfo } from './HuaweiAdapter';

export enum VehicleBrand {
  HUAWEI = 'huawei',
  BYD = 'byd',
  NIO = 'nio',
  XPENG = 'xpeng',
  OTHER = 'other'
}

export class VehicleFactory {
  static createAdapter(brand: VehicleBrand, vehicleInfo: object): object | null {
    switch (brand) {
      case VehicleBrand.HUAWEI:
        return new HuaweiAdapter(vehicleInfo as HuaweiVehicleInfo);
      // P1: BYD/NIO/Xpeng adapters
      default:
        return null;
    }
  }

  static getSupportedBrands(): string[] {
    return Object.values(VehicleBrand);
  }
}
