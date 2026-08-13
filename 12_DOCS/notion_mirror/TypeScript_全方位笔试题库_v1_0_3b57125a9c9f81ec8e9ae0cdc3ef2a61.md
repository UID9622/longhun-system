# 🐉 TypeScript 全方位笔试题库 v1.0

> Notion URL: https://app.notion.com/p/TypeScript-v1-0-3b57125a9c9f81ec8e9ae0cdc3ef2a61
> Created: 2026-08-07T15:41:00.000Z
> Last edited: 2026-08-07T15:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 🐉 TypeScript 全方位笔试题库 v1.0

> DNA: #龍芯⚡️丙午·甲申·壬寅·坤卦-LEARNING-TYPESCRIPT-EXAM-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 三色: 🟢 通过
> 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 📋 试卷结构

| 部分 | 题型 | 题量 | 分值 |
|---|---|---|---|
| 第一部分：TypeScript基础语法 | 选择题、填空题、判断题、简答题、程序分析题 | 15 | 27 |
| 第二部分：数据结构与容器 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 12 | 24 |
| 第三部分：函数/方法/模块 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 14 | 29 |
| 第四部分：面向对象/类型系统 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 20 | 41 |
| 第五部分：高级特性 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 18 | 37 |
| 第六部分：标准库与工程实践 | 选择题、填空题、判断题、简答题、编程题、程序分析题、综合应用题 | 14 | 35 |
| 第七部分：智力与逻辑 | 智力与逻辑题 | 10 | 20 |
| 第八部分：实战演练 | 编程题、综合应用题、代码调试题、系统设计题 | 12 | 34 |
| 合计 | - | 115 | 247 |

---

## 📊 详细题型分布

| 题型 | 题量 | 每题分值 | 小计 |
|---|---|---|---|
| 选择题 | 25 | 2 | 50 |
| 填空题 | 12 | 2 | 24 |
| 判断题 | 15 | 1 | 15 |
| 简答题 | 12 | 2 | 24 |
| 编程题 | 20 | 3 | 60 |
| 程序分析题 | 10 | 2 | 20 |
| 智力与逻辑题 | 10 | 2 | 20 |
| 综合应用题 | 5 | 4 | 20 |
| 代码调试题 | 4 | 2 | 8 |
| 系统设计题 | 2 | 3 | 6 |
| 合计 | 115 | - | 247 |

---

## 🎯 知识点分布与难度标注

| 知识点 | 难度 | 分值 |
|---|---|---|
| 基础语法 | ⭐⭐ | 27 |
| 数据类型 | ⭐⭐ | 12 |
| 数据结构 | ⭐⭐⭐ | 20 |
| 函数与模块 | ⭐⭐⭐ | 28 |
| 面向对象 | ⭐⭐⭐⭐ | 38 |
| 高级特性 | ⭐⭐⭐⭐ | 35 |
| 标准库 | ⭐⭐⭐ | 15 |
| 工程实践 | ⭐⭐⭐⭐ | 20 |
| 逻辑思维 | ⭐⭐⭐ | 18 |
| 实战演练 | ⭐⭐⭐⭐⭐ | 34 |
| 合计 | - | 247 |

---

# 第一部分：TypeScript基础语法

### 1. 在 TypeScript 中，以下哪个变量声明使用了正确的显式类型注解？
A. `let x = 5;`
B. `const x: number = "5";`
C. `let x: string;`
D. `var x: bool = true;`

**答案：C**

**解析：** C 使用 `let x: string` 是合法的显式类型注解；B 中 `number` 与字符串值不匹配；D 中 `bool` 不是 TS 类型，应为 `boolean`；A 依赖类型推断，没有显式注解。

### 2. 下面哪个类型是 TypeScript 在 JavaScript 基础上新增、用于表示“没有返回值”的类型？
A. `number`
B. `string`
C. `void`
D. `object`

**答案：C**

**解析：** `void` 表示函数没有返回值；`number/string/object` 均来自 JavaScript 运行时类型。

### 3. 执行以下代码后输出什么？
```ts
let a: any = 4;
a = "4";
console.log(a);
```
A. `4`
B. `"4"`
C. 编译错误
D. `undefined`

**答案：B**

**解析：** `any` 允许任意赋值，最终 `a` 为字符串 `"4"`。

### 4. 对于可能为 `null` 的字符串变量，最合适的类型是？
A. `any`
B. `unknown`
C. `string | null`
D. `void`

**答案：C**

**解析：** 联合类型 `string | null` 精确表达“字符串或 null”。

### 5. `let x: never;` 中的 `never` 表示什么？
A. 空字符串
B. 永远不会出现的值
C. 可为 null 的值
D. 未知类型

**答案：B**

**解析：** `never` 用于表示不可能存在的值，如抛出异常的函数返回类型或穷尽性检查。

### 6. TypeScript 的编译器命令是 _____。

**答案：** `tsc`

**解析：** `tsc` 调用 TypeScript 编译器，将 TS 源码转译为 JS。

### 7. 在 `tsconfig.json` 中，开启全部严格类型检查选项应设置 _____ 为 `true`。

**答案：** `strict`

**解析：** `strict: true` 同时启用 `strictNullChecks`、`noImplicitAny` 等严格选项。

### 8. 使用关键字 _____ 可以声明类型别名。

**答案：** `type`

**解析：** `type Alias = ...` 为现有类型创建别名，与 `interface` 不同。

### 9. 语句 `let x: unknown = 1; console.log(x + 1);` 可以正常编译。

**答案：** ❌错误

**解析：** `unknown` 类型不能直接参与运算，需先进行类型收窄或类型断言。

### 10. 语句 `const p: readonly [number, string] = [1, 'a']; p[0] = 2;` 可以正常编译。

**答案：** ❌错误

**解析：** `readonly` 元组禁止修改元素，赋值会报错。

### 11. 类型断言（`as`）会在运行时进行真正的类型转换。

**答案：** ❌错误

**解析：** 类型断言只在编译时生效，编译后会被擦除，不会改变运行时值。

### 12. 简述 TypeScript 中 `null` 与 `undefined` 的区别，并各举一个使用场景。

**参考答案：**
- `null` 表示“有意为空”的值，常用于显式标记对象缺失。
- `undefined` 表示“未初始化”或“未返回”，如可选参数未传、变量声明未赋值。

**解析：** 两者在严格模式下是不同类型，联合类型可显式声明 `string | null | undefined`。

### 13. `tsconfig.json` 的作用是什么？请列举两个常用配置项。

**参考答案：**
- 指定编译选项、包含文件、输出目录等。
- 常用项：`target`、`module`、`strict`、`outDir`、`include`。

**解析：** 集中管理项目编译行为，确保团队环境一致。

### 14. 分析以下代码的输出：
```ts
let x: number = 10;
function f(): void {
  let x: number = 5;
  console.log(x);
}
f();
console.log(x);
```

**答案：** 输出 `5` 然后 `10`。

**解析：** 函数内部的 `x` 遮蔽外部同名变量；`f()` 内输出局部 `5`，外部输出全局 `10`。

### 15. 分析以下代码的输出：
```ts
const obj: { a: number; b?: string } = { a: 1 };
console.log(obj.b?.length);
```

**答案：** 输出 `undefined`。

**解析：** `b` 是可选属性，未赋值时为 `undefined`；可选链 `?.` 避免运行时错误。

---

# 第二部分：数据结构与容器

### 16. 下列哪种语法正确声明了一个元组类型？
A. `let t = [string, number];`
B. `let t: [string, number];`
C. `let t: string[];`
D. `let t: (string, number);`

**答案：B**

**解析：** 元组使用方括号内按位置声明各元素类型。

### 17. 在启用 `noImplicitAny` 的情况下，`let arr = [1, 'a'];` 的推断类型最可能是？
A. `(string | number)[]`
B. `any[]`
C. `never[]`
D. 编译错误

**答案：A**

**解析：** TS 会推断为联合类型数组 `(string | number)[]`。

### 18. 哪个内置工具类型可将对象的所有属性变为可选？
A. `Required<T>`
B. `Partial<T>`
C. `Readonly<T>`
D. `Pick<T, K>`

**答案：B**

**解析：** `Partial<T>` 将 `T` 的每个属性标记为可选。

### 19. 声明数字数组的类型可写为 `_____`。

**答案：** `number[]`（或 `Array<number>`）

**解析：** 两种写法等价，数组元素均为 `number`。

### 20. 在 TypeScript 中，`Set<T>` 的 `T` 代表集合中元素的 _____。

**答案：** 类型

**解析：** 泛型参数 `T` 约束集合只能存放该类型的值。

### 21. `let m = new Map<string, number>();` 允许使用任意类型的键。

**答案：** ❌错误

**解析：** `Map<K, V>` 的键类型被 `K` 约束，此处只能为 `string`。

### 22. `const s: Set<string> = new Set(['a', 'a', 'b']); s.size === 2`。

**答案：** ✅正确

**解析：** `Set` 自动去重，插入两个 `'a'` 后实际只有一条。

### 23. 简述 TypeScript 中数组与元组的主要区别。

**参考答案：**
- 数组元素类型相同、长度可变。
- 元组长度固定，各位置类型可不同，如 `[string, number]`。

**解析：** 元组提供对长度和位置的精确类型约束。

### 24. 与用普通对象做映射相比，`Map<K, V>` 在键类型上有什么优势？

**参考答案：**
- `Map` 的键可以是任意类型（包括对象、NaN）。
- 普通对象键会被强制转换为字符串。

**解析：** `Map` 保留键的原始类型与引用身份。

### 25. 编程题：编写一个泛型函数 `unique<T>`，返回数组中不重复的元素。

**参考答案：**
```ts
function unique<T>(arr: T[]): T[] {
  return [...new Set(arr)];
}

console.log(unique<number>([1, 2, 2, 3])); // [1, 2, 3]
```

**解析：** 利用 `Set` 去重后展开为新数组，泛型保证元素类型不变。

### 26. 编程题：定义元组类型 `Point` 并编写计算两点欧氏距离的函数。

**参考答案：**
```ts
type Point = [number, number];

function distance(a: Point, b: Point): number {
  const dx = a[0] - b[0];
  const dy = a[1] - b[1];
  return Math.sqrt(dx * dx + dy * dy);
}
```

**解析：** 元组确保每个点恰好有两个 `number`；函数返回 `number`。

### 27. 程序分析题：
```ts
const arr: (number | string)[] = [1, '2', 3];
const nums = arr.filter((x): x is number => typeof x === 'number');
console.log(nums.map(n => n * 2));
```
输出是什么？为什么？

**答案：** 输出 `[2, 6]`。

**解析：** 使用类型谓词 `x is number` 后，`filter` 返回 `number[]`，可直接做数值运算。

---

# 第三部分：函数/方法/模块

### 28. 下列哪个声明定义了一个函数类型？
A. `type F = (x: number) => string;`
B. `function F(x: number): string {}`
C. `interface F { (x: number): string; }`
D. A 和 C

**答案：D**

**解析：** 函数类型可通过类型别名或接口调用签名声明；B 是函数实现。

### 29. 函数可选参数 `x?: number` 在调用未传入时，其值为？
A. `undefined`
B. `null`
C. `0`
D. `never`

**答案：A**

**解析：** 可选参数省略后值为 `undefined`，不是 `null`。

### 30. 以下哪个是正确的默认参数写法？
A. `function f(x: number = 1) {}`
B. `function f(x?: number = 1) {}`
C. `function f(x = 1: number) {}`
D. 以上都可以

**答案：A**

**解析：** 默认参数直接写在形参后；可选参数与默认值不能同时用于同一参数。

### 31. 如何从一个模块中导出命名函数？
A. `export default function f`
B. `export function f`
C. `public function f`
D. `module.exports.f`

**答案：B**

**解析：** `export function f` 导出命名成员；`export default` 导出默认成员。

### 32. 没有 `return` 语句的函数，其隐式返回类型为 _____。

**答案：** `void`

**解析：** `void` 表示函数没有有意义的返回值。

### 33. 从 `./utils` 导入默认导出应使用 `import _____ from './utils';`。

**答案：** `<标识符>`（如 `import utils from './utils';`）

**解析：** 默认导出在导入时可使用任意合法标识符。

### 34. 箭头函数与外层作用域共享词法 `this`。

**答案：** ✅正确

**解析：** 箭头函数没有自己的 `this`，会捕获定义时的外层 `this`。

### 35. `function f(x: number | string): void {}` 可以调用 `f(true)`。

**答案：** ❌错误

**解析：** `true` 不在参数类型 `number | string` 范围内。

### 36. 简述 TypeScript 函数重载的作用与使用方式。

**参考答案：**
- 允许同一函数名有多种参数/返回类型签名。
- 先写重载签名，再写实现签名，实现签名需兼容所有重载。

**解析：** 重载为调用者提供精确类型提示，编译时检查参数组合。

### 37. `export default` 与 `export` 有何区别？

**参考答案：**
- `export` 导出命名成员，导入时须使用相同名称或别名。
- `export default` 每个模块只能有一个，导入时可任意命名。

**解析：** 默认导出适合单一入口，命名导出适合工具函数集合。

### 38. 编程题：实现一个带类型的防抖函数。

**参考答案：**
```ts
function debounce<T extends any[]>(
  fn: (...args: T) => void,
  wait: number
): (...args: T) => void {
  let timer: ReturnType<typeof setTimeout> | undefined;
  return (...args: T) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}
```

**解析：** 通过泛型保留原函数参数类型；每次触发重置定时器。

### 39. 编程题：编写并导入一个数学模块 `math.ts`。

**参考答案：**
```ts
// math.ts
export const add = (a: number, b: number): number => a + b;
export const multiply = (a: number, b: number): number => a * b;
const pi = 3.14159;
export default pi;

// main.ts
import pi, { add, multiply } from './math';
console.log(add(2, 3), multiply(2, 3), pi);
```

**解析：** 展示命名导出与默认导出的组合使用。

### 40. 编程题：实现一个泛型柯里化函数，接收两个参数的函数并返回链式调用。

**参考答案：**
```ts
function curry<A, B, C>(fn: (a: A, b: B) => C): (a: A) => (b: B) => C {
  return (a: A) => (b: B) => fn(a, b);
}

const add = curry((x: number, y: number) => x + y);
console.log(add(2)(3)); // 5
```

**解析：** 通过泛型保留原函数参数与返回类型。

### 41. 程序分析题：
```ts
function wrap(val: number) {
  return {
    get: () => val,
    set: (v: number) => { val = v; }
  };
}
const w = wrap(1);
w.set(2);
console.log(w.get());
```
输出是什么？为什么？

**答案：** 输出 `2`。

**解析：** `get`/`set` 闭包共享局部变量 `val`，修改后再次读取得到 `2`。

---

# 第四部分：面向对象/类型系统

### 42. 下列哪个正确声明了一个接口？
A. `type IPerson = { name: string };`
B. `interface IPerson { name: string; }`
C. `class IPerson { name: string; }`
D. B 和 C

**答案：B**

**解析：** `interface` 关键字用于声明接口；A 是类型别名，C 是类。

### 43. 关于接口与类型别名的声明合并，正确的是？
A. 只有 `interface` 支持同名合并
B. 只有 `type` 支持
C. 两者都支持
D. 两者都不支持

**答案：A**

**解析：** 同作用域内同名 `interface` 会自动合并；`type` 重复声明会报错。

### 44. TypeScript 类成员的默认访问修饰符是？
A. `public`
B. `private`
C. `protected`
D. `readonly`

**答案：A**

**解析：** 未指定修饰符时，成员默认为 `public`。

### 45. `abstract class` 的主要含义是？
A. 不能实例化，可包含抽象方法
B. 可以实例化
C. 不能包含方法
D. 等价于接口

**答案：A**

**解析：** 抽象类不能直接 `new`，子类必须实现抽象方法。

### 46. 下列哪项使用了交叉类型？
A. `type A = B | C`
B. `type A = B & C`
C. `type A = B extends C`
D. `type A = keyof B`

**答案：B**

**解析：** `&` 构造交叉类型，要求同时具有两边的成员。

### 47. `keyof { a: 1; b: 2 }` 的结果类型是？
A. `['a', 'b']`
B. `'a' | 'b'`
C. `string`
D. `{ a: string; b: string }`

**答案：B**

**解析：** `keyof` 返回对象键的联合字符串字面量类型。

### 48. 类中 `constructor(public name: string) {}` 会自动声明一个 _____ 属性。

**答案：** `public name: string`

**解析：** 参数属性简写，自动创建同名公共属性并赋值。

### 49. `type User = { name: string } & { age: number };` 是 _____ 类型的示例。

**答案：** 交叉

**解析：** `&` 将多个类型合并为一个必须同时满足的类型。

### 50. 同一作用域内，同名的 `type` 别名可以被声明多次。

**答案：** ❌错误

**解析：** `type` 别名不支持声明合并，重复声明会产生编译错误。

### 51. `implements` 关键字既可以用于 `interface`，也可以用于对象形式的 `type` 别名。

**答案：** ✅正确

**解析：** 类 `implements` 的对象类型 Shape 可用接口或类型别名定义。

### 52. `private` 成员可以在子类中访问。

**答案：** ❌错误

**解析：** `private` 仅能在声明它的类内部访问；子类需用 `protected`。

### 53. 解释结构类型与名义类型的区别，TypeScript 使用哪一种？

**参考答案：**
- 结构类型：只要结构兼容即可赋值，不依赖显式继承。
- 名义类型：类型等价性由显式声明决定。
- TypeScript 使用结构类型系统。

**解析：** 因此两个具有相同字段的独立接口可以互相赋值。

### 54. 什么是声明合并？请用 `interface` 举例。

**参考答案：**
```ts
interface Animal { name: string; }
interface Animal { age: number; }
// 等价于 interface Animal { name: string; age: number; }
```

**解析：** TypeScript 将同名的多个接口声明合并为一个，便于扩展第三方类型。

### 55. 类中的 `abstract` 方法有什么作用？

**参考答案：**
- 只声明签名，不实现。
- 强制派生类提供实现。

**解析：** 用于定义子类必须遵循的接口契约。

### 56. 编程题：定义 `Animal` 接口，并让 `Dog` 类实现它。

**参考答案：**
```ts
interface Animal {
  name: string;
  makeSound(): void;
}

class Dog implements Animal {
  constructor(public name: string) {}
  makeSound() {
    console.log('Woof!');
  }
}
```

**解析：** `implements` 要求类包含接口声明的所有成员。

### 57. 编程题：使用交叉类型与类型谓词实现 `Admin` 判定。

**参考答案：**
```ts
type User = { name: string; };
type Admin = User & { role: 'admin'; };

function isAdmin(user: User | Admin): user is Admin {
  return (user as Admin).role === 'admin';
}
```

**解析：** `&` 组合基础类型与扩展字段；类型谓词收窄联合类型。

### 58. 编程题：实现一个带余额保护的 `BankAccount` 类。

**参考答案：**
```ts
class BankAccount {
  private _balance: number = 0;

  deposit(amount: number): void {
    if (amount <= 0) throw new Error('Invalid deposit');
    this._balance += amount;
  }

  withdraw(amount: number): void {
    if (amount > this._balance) throw new Error('Insufficient funds');
    this._balance -= amount;
  }

  get balance(): number {
    return this._balance;
  }
}
```

**解析：** `private` 封装余额，getter 提供只读访问。

### 59. 编程题：实现泛型栈 `Stack<T>`。

**参考答案：**
```ts
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }
}
```

**解析：** 泛型参数 `T` 保证栈元素类型一致。

### 60. 程序分析题：
```ts
interface Box<T> {
  value: T;
}
const b: Box<string> = { value: 1 };
console.log(b.value);
```
有什么编译错误？为什么？

**答案：** 编译报错，`Box<string>` 的 `value` 应为 `string`，但赋值了 `1`。

**解析：** 泛型参数 `T` 被实例化为 `string`，类型不匹配。

### 61. 程序分析题：
```ts
class A {
  private x = 1;
}
class B extends A {
  show() {
    console.log(this.x);
  }
}
new B().show();
```
会出现什么错误？为什么？

**答案：** 编译报错 `Property 'x' is private and only accessible within class 'A'`。

**解析：** `private` 成员不能被子类访问，应改为 `protected` 或提供公共访问器。

---

# 第五部分：高级特性

### 62. 下列哪个是泛型函数的正确定义？
A. `function f<T>(x: T): T`
B. `function f(x: T): T`
C. `function f<T>(x)`
D. A 和 C

**答案：A**

**解析：** 泛型参数 `<T>` 必须声明在函数名之后，并用于参数/返回类型。

### 63. `ReturnType<typeof f>` 的作用是？
A. 提取参数类型
B. 提取函数 `f` 的返回类型
C. 提取参数名称
D. 返回 `never`

**答案：B**

**解析：** `ReturnType<T>` 是内置工具类型，返回函数类型的返回值类型。

### 64. 应用于类方法的装饰器写法是？
A. `@log`
B. `@:log`
C. `@@log`
D. `log@`

**答案：A**

**解析：** TypeScript 装饰器使用 `@expression` 语法，放在方法前。

### 65. `typeof Array.isArray` 的类型最接近？
A. `boolean`
B. `(arg: any) => arg is any[]`
C. `any`
D. `never`

**答案：B**

**解析：** `Array.isArray` 的声明为类型谓词，返回参数是否为数组。

### 66. 在条件类型中，`infer` 的作用是？
A. 推断出一个类型变量
B. 执行运行时逻辑
C. 进行类型断言
D. 声明接口

**答案：A**

**解析：** `infer R` 在 `extends` 子句中引入一个待推断的类型变量。

### 67. 条件类型 `T extends U ? X : Y` 在 `T` 可赋值给 `U` 时选择 _____。

**答案：** `X`

**解析：** 条件类型根据 `extends` 判断选取两个分支之一。

### 68. 映射类型 `{ [K in keyof T]-?: T[K] }` 会将 `T` 的所有属性变为 _____。

**答案：** 必填（非可选）

**解析：** `-?` 移除可选修饰符，等价于 `Required<T>` 的手写实现。

### 69. `type Foo<T> = T extends string ? 'yes' : 'no';` 在运行时执行类型分支选择。

**答案：** ❌错误

**解析：** 条件类型在编译期求值，生成静态类型，不会生成运行时代码。

### 70. 装饰器目前处于 ECMAScript Stage 3，TypeScript 通过实验性选项支持。

**答案：** ✅正确

**解析：** 需启用 `experimentalDecorators`（及旧版选项）才能在 TS 中使用装饰器。

### 71. `keyof any` 等价于 `string | number | symbol`。

**答案：** ✅正确

**解析：** `keyof any` 捕获可作为对象键的所有类型。

### 72. 解释 TypeScript 函数参数类型的逆变（contravariance）是什么意思。

**参考答案：**
- 若 `Dog extends Animal`，则 `(x: Animal) => void` 可赋值给 `(x: Dog) => void`。
- 函数参数方向与继承方向相反，故称逆变。

**解析：** TS 在 `--strictFunctionTypes` 下对函数参数启用逆变检查，提高类型安全。

### 73. 什么是模板字面量类型？举一个用途。

**参考答案：**
- 模板字面量类型 `${T}-${U}` 可构造新的字符串字面量类型。
- 用途：生成事件名类型，如 `clickHandler`、`hoverHandler`。

**解析：** 增强对字符串模式的静态检查能力。

### 74. 编程题：实现泛型 `identity` 函数并展示显式调用。

**参考答案：**
```ts
function identity<T>(arg: T): T {
  return arg;
}

const n = identity<number>(42);
const s = identity('hello'); // 类型推断为 string
```

**解析：** 泛型 `T` 由调用者显式指定或类型推断得到。

### 75. 编程题：使用映射类型手写 `MyPick<T, K>`。

**参考答案：**
```ts
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};

interface User {
  id: number;
  name: string;
  age: number;
}

type UserPreview = MyPick<User, 'id' | 'name'>;
```

**解析：** 遍历 `K` 中的键，从 `T` 中拾取对应属性类型。

### 76. 编程题：编写方法装饰器 `@log` 记录方法调用。

**参考答案：**
```ts
function log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const original = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with`, args);
    return original.apply(this, args);
  };
  return descriptor;
}

class Greeter {
  @log
  greet(name: string) {
    return `Hello, ${name}`;
  }
}
```

**解析：** 方法装饰器接收原型、属性名与描述符；修改描述符可拦截调用。启用 `experimentalDecorators`。

### 77. 编程题：定义条件类型 `IsString<T>` 并验证。

**参考答案：**
```ts
type IsString<T> = T extends string ? true : false;

type A = IsString<'hello'>; // true
type B = IsString<123>;     // false
```

**解析：** 条件类型根据 `T` 是否为 `string` 的子类型返回 `true` 或 `false`。

### 78. 程序分析题：
```ts
function process<T extends { length: number }>(x: T): number {
  return x.length;
}
console.log(process('abc'));
console.log(process([1, 2, 3]));
console.log(process(123));
```
哪些调用能通过编译？为什么？

**答案：** 前两个通过，第三个报错。

**解析：** 泛型约束要求 `T` 具有 `length` 属性；字符串和数组满足，`number` 不满足。

### 79. 程序分析题：
```ts
type A = 'a' | 'b';
type B = 'b' | 'c';
type C = A & B;
const x: C = 'b';
```
是否合法？为什么？

**答案：** 合法。

**解析：** 字符串字面量联合类型的交集是共同字面量 `'b'`，因此 `C` 为 `'b'`。

---

# 第六部分：标准库与工程实践

### 80. `document.getElementById('x')` 在 TypeScript 中的返回类型是？
A. `HTMLElement`
B. `HTMLElement | null`
C. `Element`
D. `never`

**答案：B**

**解析：** DOM API 可能找不到元素，因此返回类型包含 `null`。

### 81. 哪个 `tsconfig.json` 的 `lib` 选项包含 `Promise`？
A. `es2015.promise`
B. `es2020`
C. `dom`
D. A 和 B

**答案：D**

**解析：** `Promise` 定义在 ES2015+ 的 lib 中；`es2020` 包含更早的定义。

### 82. 在 `tsconfig.json` 中，`"module": "ESNext"` 表示输出 _____ 模块。

**答案：** `ECMAScript`（或 `ES`）

**解析：** `ESNext` 让编译器按 ES 模块语法生成导入导出。

### 83. `strictNullChecks` 要求在使用可空值前先检查 `null`/`undefined`。

**答案：** ✅正确

**解析：** 开启后，`string | null` 不能直接当作 `string` 使用，必须进行收窄。

### 84. `tsconfig.json` 的 `include` 字段使用 glob 模式指定源文件。

**答案：** ✅正确

**解析：** `include` 通过通配符如 `src/**/*` 告诉编译器哪些文件参与编译。

### 85. 简述开启 `strict` 模式对项目的三个好处。

**参考答案：**
- 更早发现空值与隐式 `any` 导致的错误。
- 提高代码可维护性与重构安全性。
- 增强 IDE 类型推断与自动补全体验。

**解析：** `strict` 是多个严格检查选项的总开关。

### 86. 编程题：编写带类型的 `fetchJSON<T>` 包装函数。

**参考答案：**
```ts
async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  }
  return (await res.json()) as T;
}

interface User {
  id: number;
  name: string;
}

fetchJSON<User[]>('/api/users').then(users => console.log(users[0].name));
```

**解析：** 泛型指定响应结构；`as T` 在运行时无法校验，应配合验证库生产环境使用。

### 87. 编程题：为全局函数 `greet` 编写声明文件 `mylib.d.ts`。

**参考答案：**
```ts
// mylib.d.ts
declare function greet(name: string): string;
```

**解析：** `.d.ts` 文件只包含类型声明，不产生 JS 输出，用于为无类型的库提供类型。

### 88. 编程题：编写一个适合 Node 项目的 `tsconfig.json`，目标 ES2020 并开启严格模式。

**参考答案：**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

**解析：** 指定目标、模块、严格选项与输出目录，是 Node 项目的常见配置。

### 89. 程序分析题：
```ts
type Colors = 'red' | 'green' | 'blue';
const c: Colors = 'yellow';
```
是否会编译通过？为什么？

**答案：** 不会，编译报错。

**解析：** `'yellow'` 不是 `'red' | 'green' | 'blue'` 联合类型中的成员。

### 90. 程序分析题：
```ts
namespace App {
  export const version = '1.0';
}
console.log(App.version);
```
输出是什么？

**答案：** 输出 `1.0`。

**解析：** `namespace` 将相关代码组织到同一作用域，导出的成员可通过命名空间访问。

### 91. 综合应用题：设计一个类型安全的 JSON 配置加载器，支持必填/默认值与类型推断。

**参考答案：**
```ts
interface Config {
  port: number;
  debug: boolean;
  host?: string;
}

function loadConfig(raw: unknown): Config {
  if (typeof raw !== 'object' || raw === null) {
    throw new Error('Invalid config');
  }
  const r = raw as Record<string, unknown>;
  const port = typeof r.port === 'number' ? r.port : 3000;
  const debug = typeof r.debug === 'boolean' ? r.debug : false;
  const host = typeof r.host === 'string' ? r.host : 'localhost';
  return { port, debug, host };
}
```

**解析：** 使用 `unknown` 接收外部输入，运行时逐项校验并赋默认值，最终返回 `Config` 类型。

### 92. 综合应用题：为类型安全函数 `sum(a: number, b: number)` 编写 Jest 单元测试。

**参考答案：**
```ts
// sum.ts
export const sum = (a: number, b: number): number => a + b;

// sum.test.ts
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});

test('adds negative numbers', () => {
  expect(sum(-1, -2)).toBe(-3);
});
```

**解析：** 测试覆盖正数与负数，验证类型约束下的运行时行为。

### 93. 综合应用题：列出搭建一个最小 TypeScript 项目所需的 `package.json` 关键脚本与依赖。

**参考答案：**
```json
{
  "name": "ts-demo",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

**解析：** `typescript` 为必需 devDependency；`build` 调用 `tsc` 编译，`dev` 启用监听。

---

# 第七部分：智力与逻辑

### 94. 智力与逻辑题：实现一个类型标注完善的字符串反转函数。

**参考答案：**
```ts
function reverseString(s: string): string {
  return s.split('').reverse().join('');
}

console.log(reverseString('TypeScript')); // tpircSepyT
```

**解析：** 利用数组反转；类型约束确保输入输出均为字符串。

### 95. 智力与逻辑题：在 0..n 的数组中找出缺失的那个数字。

**参考答案：**
```ts
function missingNumber(nums: number[]): number {
  const n = nums.length;
  const expected = (n * (n + 1)) / 2;
  const actual = nums.reduce((sum, v) => sum + v, 0);
  return expected - actual;
}

console.log(missingNumber([0, 1, 3])); // 2
```

**解析：** 利用数学求和公式，时间复杂度 O(n)。

### 96. 智力与逻辑题：实现带类型标注的 FizzBuzz。

**参考答案：**
```ts
function fizzBuzz(n: number): void {
  for (let i = 1; i <= n; i++) {
    let out = '';
    if (i % 3 === 0) out += 'Fizz';
    if (i % 5 === 0) out += 'Buzz';
    console.log(out || i);
  }
}

fizzBuzz(15);
```

**解析：** 循环中根据倍数拼接字符串，无输出时打印数字。

### 97. 智力与逻辑题：判断一个整数是否为回文数。

**参考答案：**
```ts
function isPalindrome(n: number): boolean {
  const s = String(n);
  return s === s.split('').reverse().join('');
}

console.log(isPalindrome(12321)); // true
```

**解析：** 转为字符串后比较正序与反序。

### 98. 智力与逻辑题：实现深相等判断 `deepEqual`，支持基本类型与对象。

**参考答案：**
```ts
function deepEqual(a: unknown, b: unknown): boolean {
  if (a === b) return true;
  if (
    typeof a !== 'object' ||
    typeof b !== 'object' ||
    a === null ||
    b === null
  ) {
    return false;
  }
  const ka = Object.keys(a as object);
  const kb = Object.keys(b as object);
  if (ka.length !== kb.length) return false;
  return ka.every(
    k => kb.includes(k) && deepEqual((a as any)[k], (b as any)[k])
  );
}
```

**解析：** 递归比较对象键值；先处理基本类型与 null。

### 99. 智力与逻辑题：找出字符串中第一个不重复的字符。

**参考答案：**
```ts
function firstUniqueChar(s: string): string | null {
  const map = new Map<string, number>();
  for (const c of s) {
    map.set(c, (map.get(c) || 0) + 1);
  }
  for (const c of s) {
    if (map.get(c) === 1) return c;
  }
  return null;
}

console.log(firstUniqueChar('typescript')); // 'y'
```

**解析：** 先统计频次，再按原顺序查找频次为 1 的字符。

### 100. 智力与逻辑题：实现一个类型安全的通用记忆化函数。

**参考答案：**
```ts
function memoize<T extends any[], R>(
  fn: (...args: T) => R
): (...args: T) => R {
  const cache = new Map<string, R>();
  return (...args: T) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key)!;
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const fib = memoize((n: number): number =>
  n <= 1 ? n : fib(n - 1) + fib(n - 2)
);
console.log(fib(10)); // 55
```

**解析：** 缓存参数到结果的映射；使用 `JSON.stringify` 作键适用于可序列化参数。

### 101. 智力与逻辑题：给定有限字面量联合类型 `type Color = 'red' | 'green' | 'blue'`，若再与 `'blue' | 'yellow'` 取交集，结果类型是什么？

**答案：** `'blue'`

**解析：** 联合类型的交集只保留共同成员，因此结果为 `'blue'`。

### 102. 智力与逻辑题：实现二分查找并返回目标索引，不存在返回 -1。

**参考答案：**
```ts
function binarySearch(arr: number[], target: number): number {
  let left = 0;
  let right = arr.length - 1;
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
```

**解析：** 每次折半查找，时间复杂度 O(log n)。

### 103. 智力与逻辑题：实现最大子数组和（Kadane 算法）。

**参考答案：**
```ts
function maxSubArray(arr: number[]): number {
  let max = arr[0];
  let current = arr[0];
  for (let i = 1; i < arr.length; i++) {
    current = Math.max(arr[i], current + arr[i]);
    max = Math.max(max, current);
  }
  return max;
}

console.log(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4])); // 6
```

**解析：** 动态维护以当前元素结尾的最大子数组和。

---

# 第八部分：实战演练

### 104. 综合应用题：实现一个类型安全的事件发射器 `EventEmitter<Events>`。

**参考答案：**
```ts
type Listener<T> = (data: T) => void;

class EventEmitter<Events extends Record<string, any>> {
  private listeners: { [K in keyof Events]?: Listener<Events[K]>[] } = {};

  on<K extends keyof Events>(
    event: K,
    listener: Listener<Events[K]>
  ): void {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event]!.push(listener);
  }

  off<K extends keyof Events>(
    event: K,
    listener: Listener<Events[K]>
  ): void {
    this.listeners[event] = this.listeners[event]?.filter(l => l !== listener);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.listeners[event]?.forEach(l => l(data));
  }
}

type MyEvents = { message: string; count: number };
const emitter = new EventEmitter<MyEvents>();
emitter.on('message', msg => console.log(msg));
emitter.emit('message', 'hello');
```

**解析：** 使用映射类型将事件名映射到对应数据类型，实现编译期类型检查。

### 105. 综合应用题：手写一个简化版 `Promise.all`，接收 Promise 数组并返回结果数组。

**参考答案：**
```ts
function all<T>(promises: Promise<T>[]): Promise<T[]> {
  return new Promise((resolve, reject) => {
    if (promises.length === 0) {
      resolve([]);
      return;
    }
    const results: T[] = new Array(promises.length);
    let completed = 0;
    promises.forEach((p, i) => {
      p.then(value => {
        results[i] = value;
        completed++;
        if (completed === promises.length) resolve(results);
      }).catch(reject);
    });
  });
}
```

**解析：** 使用计数器判断全部完成，保持结果顺序；任一失败立即 reject。

### 106. 综合应用题：实现一个泛型 LRU 缓存。

**参考答案：**
```ts
class LRUCache<K, V> {
  private cache = new Map<K, V>();

  constructor(private capacity: number) {}

  get(key: K): V | undefined {
    if (!this.cache.has(key)) return undefined;
    const value = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  put(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      const oldest = this.cache.keys().next().value;
      this.cache.delete(oldest);
    }
    this.cache.set(key, value);
  }
}
```

**解析：** `Map` 按插入顺序维护键，访问时删除再插入可刷新位置。

### 107. 综合应用题：实现类型安全的函数管道 `pipe`。

**参考答案：**
```ts
function pipe<T>(...fns: Array<(arg: T) => T>): (arg: T) => T {
  return (arg: T) => fns.reduce((v, f) => f(v), arg);
}

const addOne = (x: number) => x + 1;
const double = (x: number) => x * 2;
const transform = pipe(addOne, double);
console.log(transform(3)); // 8
```

**解析：** `reduce` 依次应用函数；类型约束保证每步输入输出类型一致。

### 108. 综合应用题：设计一个类型安全的 REST API 客户端，支持 GET/POST 与统一错误处理。

**参考答案：**
```ts
class ApiClient {
  constructor(private baseURL: string) {}

  async get<T>(path: string): Promise<T> {
    const res = await fetch(`${this.baseURL}${path}`);
    return this.handleResponse<T>(res);
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    const res = await fetch(`${this.baseURL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return this.handleResponse<T>(res);
  }

  private async handleResponse<T>(res: Response): Promise<T> {
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return (await res.json()) as T;
  }
}
```

**解析：** 泛型方法让调用方指定返回结构；统一处理 HTTP 错误与 JSON 解析。

### 109. 综合应用题：设计一个带类型约束的表单校验器，返回字段错误信息。

**参考答案：**
```ts
type Rule<T> = {
  field: keyof T;
  validate: (value: unknown) => string | null;
};

function validate<T extends Record<string, any>>(
  data: T,
  rules: Rule<T>[]
): Partial<Record<keyof T, string>> {
  const errors: Partial<Record<keyof T, string>> = {};
  for (const rule of rules) {
    const msg = rule.validate(data[rule.field]);
    if (msg) errors[rule.field] = msg;
  }
  return errors;
}

interface LoginForm {
  email: string;
  password: string;
}

const errors = validate<LoginForm>(
  { email: 'a', password: '123' },
  [
    {
      field: 'email',
      validate: v => ((v as string).includes('@') ? null : 'Invalid email'),
    },
    {
      field: 'password',
      validate: v => ((v as string).length >= 6 ? null : 'Too short'),
    },
  ]
);
```

**解析：** `Rule` 的 `field` 使用 `keyof T` 保证只能校验表单已有字段。

### 110. 代码调试题：以下代码有何错误？如何修正？
```ts
let age: number = "25";
console.log(age + 5);
```

**答案：** 类型不匹配；应将字符串转为数字或修改初始值。

**修正：**
```ts
let age: number = Number("25");
console.log(age + 5); // 30
```

**解析：** `number` 变量不能直接赋值 `string`，需用 `Number()` 或字面量。

### 111. 代码调试题：以下代码中 `this` 的值为何不符合预期？如何修正？
```ts
class Counter {
  count = 0;
  increment() {
    setTimeout(function () {
      this.count++;
      console.log(this.count);
    }, 100);
  }
}
```

**答案：** `function` 回调会创建自己的 `this`，应改用箭头函数。

**修正：**
```ts
class Counter {
  count = 0;
  increment() {
    setTimeout(() => {
      this.count++;
      console.log(this.count);
    }, 100);
  }
}
```

**解析：** 箭头函数捕获外层词法 `this`，即 `Counter` 实例。

### 112. 代码调试题：以下泛型函数编译失败，原因是什么？如何修正？
```ts
function logLength<T>(x: T): number {
  return x.length;
}
```

**答案：** `T` 不一定有 `length` 属性，应添加约束。

**修正：**
```ts
function logLength<T extends { length: number }>(x: T): number {
  return x.length;
}
```

**解析：** 通过 `extends` 约束泛型参数必须具备 `length`。

### 113. 代码调试题：以下导入为何会失败？如何修正？
```ts
import { helper } from './utils';
```
假设 `./utils.ts` 存在且使用 ESM 导出。

**答案：** 可能是模块解析未包含 `.ts` 扩展名或 `moduleResolution` 配置不当。

**修正：** 确保 `tsconfig.json` 中 `"moduleResolution": "node"`，Node ESM 中可显式使用 `./utils.js`（TS 编译后）；CommonJS 下通常省略扩展名即可。

**解析：** TypeScript 模块解析策略决定了路径解析方式。

### 114. 系统设计题：为微前端架构设计一个类型安全的事件总线，要求支持跨应用事件订阅、类型校验与命名空间隔离。

**参考答案：**
- 定义全局事件映射 `GlobalEvents = { 'app1:update': PayloadA; 'app2:notify': PayloadB }`。
- 事件总线核心接口：`on<K extends keyof GlobalEvents>(event: K, listener: (payload: GlobalEvents[K]) => void)`。
- 使用命名空间前缀（如 `app1:`）隔离不同微应用，避免事件名冲突。
- 通过 `EventEmitter` 或 `BroadcastChannel` 在窗口间通信；TypeScript 在编译期校验事件名与载荷类型。
- 提供 `emit` 与 `off` 方法，并在卸载应用时自动清理订阅。

**解析：** 类型映射保证只有已注册事件可被订阅，命名空间降低耦合。

### 115. 系统设计题：设计一个类型安全的依赖注入容器，支持服务注册与解析。

**参考答案：**
```ts
type Constructor<T> = new (...args: any[]) => T;

class Container {
  private registry = new Map<string | symbol, Constructor<any>>();

  register<T>(token: string | symbol, impl: Constructor<T>): void {
    this.registry.set(token, impl);
  }

  resolve<T>(token: string | symbol): T {
    const Impl = this.registry.get(token);
    if (!Impl) throw new Error(`No provider for ${String(token)}`);
    return new Impl() as T;
  }
}

interface Logger {
  log(msg: string): void;
}

class ConsoleLogger implements Logger {
  log(msg: string) {
    console.log(msg);
  }
}

const container = new Container();
container.register<Logger>(Symbol('Logger'), ConsoleLogger);
const logger = container.resolve<Logger>(Symbol('Logger'));
logger.log('DI works');
```

**解析：** 通过 token（字符串或 symbol）解耦接口与实现；泛型确保解析返回指定接口类型。可扩展生命周期作用域（singleton / transient）。

---

## 📊 参考答案汇总

| 题号 | 答案 | 题号 | 答案 | 题号 | 答案 |
|:---:|:---|:---:|:---|:---:|:---|
| 1 | C | 2 | C | 3 | B |
| 4 | C | 5 | B | 6 | `tsc` |
| 7 | `strict` | 8 | `type` | 9 | ❌错误 |
| 10 | ❌错误 | 11 | ❌错误 | 12 | 见解析 |
| 13 | 见解析 | 14 | `5` 然后 `10` | 15 | `undefined` |
| 16 | B | 17 | A | 18 | B |
| 19 | `number[]` | 20 | 类型 | 21 | ❌错误 |
| 22 | ✅正确 | 23 | 见解析 | 24 | 见解析 |
| 25 | 见代码 | 26 | 见代码 | 27 | `[2, 6]` |
| 28 | D | 29 | A | 30 | A |
| 31 | B | 32 | `void` | 33 | 标识符 |
| 34 | ✅正确 | 35 | ❌错误 | 36 | 见解析 |
| 37 | 见解析 | 38 | 见代码 | 39 | 见代码 |
| 40 | 见代码 | 41 | `2` | 42 | B |
| 43 | A | 44 | A | 45 | A |
| 46 | B | 47 | B | 48 | `public name: string` |
| 49 | 交叉 | 50 | ❌错误 | 51 | ✅正确 |
| 52 | ❌错误 | 53 | 见解析 | 54 | 见解析 |
| 55 | 见解析 | 56 | 见代码 | 57 | 见代码 |
| 58 | 见代码 | 59 | 见代码 | 60 | 类型不匹配错误 |
| 61 | private 访问错误 | 62 | A | 63 | B |
| 64 | A | 65 | B | 66 | A |
| 67 | `X` | 68 | 必填 | 69 | ❌错误 |
| 70 | ✅正确 | 71 | ✅正确 | 72 | 见解析 |
| 73 | 见解析 | 74 | 见代码 | 75 | 见代码 |
| 76 | 见代码 | 77 | 见代码 | 78 | 前两个通过，第三个失败 |
| 79 | 合法 | 80 | B | 81 | D |
| 82 | ECMAScript | 83 | ✅正确 | 84 | ✅正确 |
| 85 | 见解析 | 86 | 见代码 | 87 | 见代码 |
| 88 | 见配置 | 89 | 编译报错 | 90 | `1.0` |
| 91 | 见代码 | 92 | 见代码 | 93 | 见配置 |
| 94 | 见代码 | 95 | 见代码 | 96 | 见代码 |
| 97 | 见代码 | 98 | 见代码 | 99 | 见代码 |
| 100 | 见代码 | 101 | `'blue'` | 102 | 见代码 |
| 103 | 见代码 | 104 | 见代码 | 105 | 见代码 |
| 106 | 见代码 | 107 | 见代码 | 108 | 见代码 |
| 109 | 见代码 | 110 | `Number("25")` | 111 | 箭头函数 |
| 112 | `extends { length: number }` | 113 | 检查 `moduleResolution` | 114 | 见设计 |
| 115 | 见代码 |  |  |  |  |

## 🔐 最终签名

**DNA:** #龍芯⚡️丙午·甲申·壬寅·坤卦-LEARNING-TYPESCRIPT-EXAM-v1.0-UID9622
**GPG:** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**确认码:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**创建者:** 诸葛鑫（UID9622）
**三色审计:** 🟢 通过


