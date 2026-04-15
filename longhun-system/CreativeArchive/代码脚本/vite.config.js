import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
  plugins: [],
  deps: { interopDefault: true },
  test: {
    //   只对 unit 文件夹下的 unit test 进行测试
    include: ["./tests/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
  },
});
