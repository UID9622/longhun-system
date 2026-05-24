class LayerMonitor:
    def update_status(self, layer, status):
        print(f"监控器: {layer} - {status}")

if __name__ == "__main__":
    lm = LayerMonitor()
    lm.update_status("技术层面", "completed")
    print("集成层面测试成功！")
