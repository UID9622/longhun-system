// entry/src/main/ets/pages/NavigationContainer.ets
// 龍魂 · Navigation容器页面

import { navController } from '../navigation/NavigationController';
import { RouterUtils, RouteConfig } from '../router/RouterConfig';

@Entry
@Component
struct NavigationContainer {
  @State private selectedIndex: number = 0;
  @State private navStack: NavPathStack = navController.getStack();

  // 页面映射
  @Builder
  pageMap(name: string, params: Record<string, Object>) {
    if (name === 'Index') {
      IndexPage();
    } else if (name === 'Login') {
      LoginPage();
    } else if (name === 'ProjectList') {
      ProjectListPage();
    } else if (name === 'ProjectDetail') {
      ProjectDetailPage({ id: params?.['id'] as string });
    } else if (name === 'ProjectEdit') {
      ProjectEditPage({ id: params?.['id'] as string });
    } else if (name === 'MilestoneTimeline') {
      MilestoneTimelinePage();
    } else if (name === 'WeeklyReview') {
      WeeklyReviewPage();
    } else if (name === 'StampManagement') {
      StampManagementPage();
    } else if (name === 'Settings') {
      SettingsPage();
    } else if (name === 'Profile') {
      ProfilePage();
    } else {
      Text(`页面未找到: ${name}`)
        .fontSize(16)
        .fontColor('#ff4444');
    }
  }

  // TabBar路由
  getTabRoutes(): RouteConfig[] {
    return RouterUtils.getTabBarRoutes();
  }

  // 获取当前目标名称
  getCurrentDestName(): string {
    const destInfo = this.navStack.getDestinationInfos();
    if (destInfo.length > 0) {
      return destInfo[destInfo.length - 1].name || 'Index';
    }
    return 'Index';
  }

  build() {
    Navigation(this.navStack) {
      // 主内容区
      this.pageMap(this.getCurrentDestName(), {})
    }
    .hideTitleBar(true)
    .hideBackButton(false)
    .navDestination(this.pageMap)
    .mode(NavigationMode.Stack)
    .onAppear(() => {
      console.info('[龍魂] Navigation容器已挂载');
    })
    .onDisAppear(() => {
      console.info('[龍魂] Navigation容器已卸载');
    })
    // TabBar（底部导航）
    .toolbarConfiguration(this.ToolbarBuilder())
  }

  // TabBar构建
  @Builder
  ToolbarBuilder() {
    Row() {
      ForEach(this.getTabRoutes(), (route: RouteConfig, index: number) => {
        Column() {
          Text(route.icon || '📄')
            .fontSize(this.selectedIndex === index ? 24 : 20)
            .fontColor(this.selectedIndex === index ? '#c41e3a' : '#666')
          Text(route.title)
            .fontSize(11)
            .fontColor(this.selectedIndex === index ? '#c41e3a' : '#666')
            .margin({ top: 2 })
        }
        .width(`${100 / this.getTabRoutes().length}%`)
        .height('100%')
        .justifyContent(FlexAlign.Center)
        .onClick(() => {
          this.selectedIndex = index;
          navController.push(route.name);
        })
      })
    }
    .width('100%')
    .height(56)
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }
}
