// entry/src/main/ets/components/AgentRegistryDialog.ets
// 龍魂 · 智能体注册弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { AgentProfile, AgentType, PermissionLevel, Capability, IntentPattern, IntentType, AgentState, agentState } from '../models/AgentProtocol';

@CustomDialog
export struct AgentRegistryDialog {
  controller: CustomDialogController;
  @StorageLink('agentState') agentState: AgentState = agentState;
  @State private name: string = '';
  @State private agentType: AgentType = AgentType.USER;
  @State private endpoint: string = '';
  @State private deviceType: string = 'phone';
  @State private version: string = '1.0.0';
  @State private permissionLevel: PermissionLevel = PermissionLevel.READ;
  @State private capabilities: string = '';
  @State private isEditMode: boolean = false;
  @State private editAgentId: string = '';
  @Prop agent: AgentProfile | null = null;

  aboutToAppear() {
    if (this.agent) {
      this.isEditMode = true;
      this.editAgentId = this.agent.id;
      this.name = this.agent.name;
      this.agentType = this.agent.type;
      this.endpoint = this.agent.endpoint;
      this.deviceType = this.agent.deviceType;
      this.version = this.agent.version;
      this.permissionLevel = this.agent.permissionLevel;
      this.capabilities = this.agent.capabilities.map(c => c.name).join(', ');
    }
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.isEditMode ? '编辑智能体' : '注册智能体')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Blank()
        Button() { Text('✕').fontSize(18).fontColor('#888') }
          .type(ButtonType.Normal).backgroundColor(Color.Transparent)
          .onClick(() => { this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 表单
      Scroll() {
        Column() {
          // 名称
          this.FormField('名称', () => {
            TextInput({ text: this.name, placeholder: '智能体名称' })
              .onChange((value: string) => { this.name = value; })
              .backgroundColor('#0a0a0a')
              .borderRadius(8)
          })

          // 类型选择
          this.FormField('类型', () => {
            Row() {
              ForEach([
                { type: AgentType.SYSTEM, label: '🔧 系统' },
                { type: AgentType.USER, label: '👤 用户' },
                { type: AgentType.SERVICE, label: '⚙️ 服务' },
                { type: AgentType.DEVICE, label: '📱 设备' },
                { type: AgentType.EXTERNAL, label: '🌐 外部' }
              ], (item: {type: AgentType, label: string}) => {
                Text(item.label)
                  .fontSize(12)
                  .fontColor(this.agentType === item.type ? '#fff' : '#888')
                  .backgroundColor(this.agentType === item.type ? '#c41e3a' : '#1a1a1a')
                  .borderRadius(4)
                  .padding({ left: 8, right: 8, top: 4, bottom: 4 })
                  .margin({ right: 8 })
                  .onClick(() => { this.agentType = item.type; })
              })
            }
          })

          // 端口
          this.FormField('通信端点', () => {
            TextInput({ text: this.endpoint, placeholder: 'http://host:port 或本地' })
              .onChange((value: string) => { this.endpoint = value; })
              .backgroundColor('#0a0a0a')
              .borderRadius(8)
          })

          // 设备类型
          this.FormField('设备类型', () => {
            Row() {
              ForEach(['phone', 'tablet', 'watch', 'car', 'tv', 'iot'], (dt: string) => {
                Text(dt)
                  .fontSize(12)
                  .fontColor(this.deviceType === dt ? '#fff' : '#888')
                  .backgroundColor(this.deviceType === dt ? '#c41e3a' : '#1a1a1a')
                  .borderRadius(4)
                  .padding({ left: 8, right: 8, top: 4, bottom: 4 })
                  .margin({ right: 8 })
                  .onClick(() => { this.deviceType = dt; })
              })
            }
          })

          // 版本
          this.FormField('版本', () => {
            TextInput({ text: this.version, placeholder: '1.0.0' })
              .onChange((value: string) => { this.version = value; })
              .backgroundColor('#0a0a0a')
              .borderRadius(8)
          })

          // 权限等级
          this.FormField('权限等级', () => {
            Row() {
              ForEach([
                { level: PermissionLevel.READ, label: '只读' },
                { level: PermissionLevel.WRITE, label: '读写' },
                { level: PermissionLevel.ADMIN, label: '管理' },
                { level: PermissionLevel.ROOT, label: '根权限' }
              ], (item: {level: PermissionLevel, label: string}) => {
                Text(item.label)
                  .fontSize(12)
                  .fontColor(this.permissionLevel === item.level ? '#fff' : '#888')
                  .backgroundColor(this.permissionLevel === item.level ? '#c41e3a' : '#1a1a1a')
                  .borderRadius(4)
                  .padding({ left: 8, right: 8, top: 4, bottom: 4 })
                  .margin({ right: 8 })
                  .onClick(() => { this.permissionLevel = item.level; })
              })
            }
          })

          // 能力
          this.FormField('能力声明', () => {
            TextInput({ text: this.capabilities, placeholder: '逗号分隔: 查询,分析,报告' })
              .onChange((value: string) => { this.capabilities = value; })
              .backgroundColor('#0a0a0a')
              .borderRadius(8)
          })
        }
        .padding(16)
      }
      .layoutWeight(1)

      // 操作按钮
      Row() {
        if (this.isEditMode) {
          Button() {
            Text('注销').fontSize(14).fontColor('#ff0000')
          }
          .type(ButtonType.Normal).backgroundColor('rgba(255,0,0,0.1)').borderRadius(8)
          .padding({ left: 24, right: 24, top: 10, bottom: 10 }).margin({ right: 12 })
          .onClick(() => { this.unregisterAgent(); })
        }
        Button() {
          Text(this.isEditMode ? '保存' : '注册').fontSize(14).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#c41e3a').borderRadius(8)
        .padding({ left: 24, right: 24, top: 10, bottom: 10 })
        .onClick(() => { this.onSubmit(); })
      }
      .width('100%').padding(16).justifyContent(FlexAlign.End)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%')
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
  }

  @Builder
  FormField(label: string, @BuilderParam content: () => void) {
    Column() {
      Text(label)
        .fontSize(13)
        .fontWeight(FontWeight.Medium)
        .fontColor('#aaa')
        .margin({ bottom: 8 })
      content()
    }
    .width('100%')
    .margin({ bottom: 16 })
    .alignItems(HorizontalAlign.Start)
  }

  onSubmit(): void {
    if (!this.name.trim()) {
      console.warn('[龍魂] 智能体名称为空');
      return;
    }

    const capList: Capability[] = this.capabilities
      .split(',')
      .filter(c => c.trim())
      .map(c => ({
        name: c.trim(),
        description: c.trim(),
        version: '1.0.0',
        enabled: true,
        params: [],
        returns: { type: 'any', description: '' }
      }));

    const agent = new AgentProfile({
      id: this.isEditMode ? this.editAgentId : undefined,
      name: this.name.trim(),
      type: this.agentType,
      endpoint: this.endpoint.trim(),
      deviceType: this.deviceType,
      version: this.version,
      permissionLevel: this.permissionLevel,
      capabilities: capList,
      status: this.isEditMode ? undefined : 'online',
      allowedScopes: ['*']
    });

    if (this.isEditMode) {
      this.agentState.agents.set(agent.id, agent);
    } else {
      this.agentState.registerAgent(agent);
    }

    this.agentState.persist();
    this.controller.close();
    console.info(`[龍魂] 智能体${this.isEditMode ? '更新' : '注册'}: ${agent.name}`);
  }

  unregisterAgent(): void {
    this.agentState.unregisterAgent(this.editAgentId);
    this.agentState.persist();
    this.controller.close();
    console.info('[龍魂] 智能体已注销');
  }
}
