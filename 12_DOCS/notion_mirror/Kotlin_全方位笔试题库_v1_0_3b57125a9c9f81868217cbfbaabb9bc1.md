# 🐉 Kotlin 全方位笔试题库 v1.0

> Notion URL: https://app.notion.com/p/Kotlin-v1-0-3b57125a9c9f81868217cbfbaabb9bc1
> Created: 2026-08-07T15:41:00.000Z
> Last edited: 2026-08-07T15:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 🐉 Kotlin 全方位笔试题库 v1.0

> DNA: #龍芯⚡️丙午·甲申·壬寅·坤卦-LEARNING-KOTLIN-EXAM-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 三色: 🟢 通过
> 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 📋 试卷结构

| 部分 | 题型 | 题量 | 分值 |
|------|------|------|------|
| 基础语法 | 选择题、填空题、判断题、简答题、程序分析题 | 12 | 16 |
| 数据结构与容器 | 选择题、填空题、判断题、编程题、程序分析题 | 10 | 18 |
| 函数/方法/模块 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 12 | 26 |
| 面向对象/类型系统 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 12 | 22 |
| 高级特性 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 16 | 33 |
| 标准库与工程实践 | 选择题、填空题、判断题、简答题、编程题、程序分析题 | 10 | 21 |
| 智力与逻辑 | 智力与逻辑题 | 8 | 16 |
| 实战演练 | 综合应用题、代码调试题、系统设计题 | 10 | 44 |
| **合计** | — | **90** | **196** |

---

## 📊 详细题型分布

| 题型 | 题量 | 每题分值 | 小计 |
|------|------|----------|------|
| 选择题 | 22 | 1 | 22 |
| 填空题 | 10 | 1 | 10 |
| 判断题 | 10 | 1 | 10 |
| 简答题 | 8 | 2 | 16 |
| 编程题 | 12 | 4 | 48 |
| 程序分析题 | 10 | 3 | 30 |
| 智力与逻辑题 | 8 | 2 | 16 |
| 综合应用题 | 5 | 4 | 20 |
| 代码调试题 | 3 | 4 | 12 |
| 系统设计题 | 2 | 6 | 12 |
| **合计** | **90** | — | **196** |

---

## 🎯 知识点分布与难度标注

| 知识点 | 难度 | 分值 |
|--------|------|------|
| 基础语法 | ⭐⭐ | 16 |
| 数据类型 | ⭐⭐ | 10 |
| 数据结构 | ⭐⭐⭐ | 18 |
| 函数与模块 | ⭐⭐⭐ | 26 |
| 面向对象 | ⭐⭐⭐ | 22 |
| 高级特性 | ⭐⭐⭐⭐ | 33 |
| 标准库 | ⭐⭐⭐ | 12 |
| 工程实践 | ⭐⭐⭐⭐ | 9 |
| 逻辑思维 | ⭐⭐⭐⭐ | 16 |
| 实战演练 | ⭐⭐⭐⭐⭐ | 44 |

---

# 第一部分：Kotlin基础语法

### 1. 在 Kotlin 中，以下声明方式正确且表示不可变引用的是？
A. `var name: String = "Kotlin"`  
B. `val name: String = "Kotlin"`  
C. `const name = "Kotlin"`  
D. `name := "Kotlin"`

**答案：B**

**解析：** `val` 声明只读引用，变量本身不可重新赋值；`var` 声明可变引用；`const` 需配合 `val` 且只能用于顶层或伴生对象中的基本类型/String；`:=` 不是 Kotlin 语法。

### 2. 以下代码的输出是？
```kotlin
val version = 2
println("Kotlin $version.x")
```
A. `Kotlin $version.x`  
B. `Kotlin 2.x`  
C. 编译错误  
D. `Kotlin 2`

**答案：B**

**解析：** `$version` 是字符串模板，会替换为变量值，因此输出 `Kotlin 2.x`。

### 3. `for (i in 1..4)` 会迭代几次？
A. 3  
B. 4  
C. 5  
D. 0

**答案：B**

**解析：** `1..4` 表示闭区间 [1,4]，包含 1、2、3、4 共 4 次。

### 4. 下列关于 `when` 的说法错误的是？
A. `when` 可以作为表达式使用  
B. `when` 的分支条件可以是范围判断  
C. `when` 必须包含 `else` 分支  
D. `when` 可以对多个条件用逗号分隔

**答案：C**

**解析：** `when` 作为完整表达式且分支不覆盖所有可能值时才需要 `else`；如果是语句或分支已穷尽，则不需要。

### 5. Kotlin 支持类型推断，写出下面变量的推断类型：`val count = 100L` 推断为 ______。

**答案：** `Long`

**解析：** 字面量带 `L` 后缀表示 `Long`，编译器据此推断 `count` 类型为 `Long`。

### 6. 使用原始字符串表示包含换行的多行文本，应使用 ______ 包裹。

**答案：** `"""..."""`

**解析：** Kotlin 使用三个双引号定义原始字符串（raw string），内部无需转义 `\n`。

### 7. 写出从 10 递减到 1、步长为 2 的范围表达式：______。

**答案：** `10 downTo 1 step 2`

**解析：** `downTo` 生成降序范围，`step` 指定步长；该表达式产生 10、8、6、4、2。

### 8. Kotlin 只能编译成 JVM 字节码，不能用于前端或 Native 开发。

**答案：** ❌错误

**解析：** Kotlin 可编译为 JVM 字节码、JavaScript 以及 Kotlin/Native，因此可用于后端、前端与原生开发。

### 9. 在 Kotlin 中，`==` 比较的是引用地址，`===` 比较的是结构相等性。

**答案：** ❌错误

**解析：** 恰恰相反：`==` 调用 `equals()` 比较结构相等性；`===` 比较两个引用是否指向同一对象。

### 10. 简述 `val`、`var` 与 `const val` 的区别。

**参考答案：**
- `val`：只读变量，运行期赋值，引用不可变。
- `var`：可变变量，引用和值都可以重新赋值（除非值本身不可变）。
- `const val`：编译期常量，只能是顶层或伴生对象中的 `String` 或基本类型，值在编译时确定。

### 11. 简述 Kotlin 中 `when` 相较于传统 `switch` 的优势。

**参考答案：**
- `when` 可以是表达式，直接返回结果。
- 分支条件支持任意表达式、范围、类型判断、组合条件等。
- 当作为表达式且未覆盖所有可能时，编译器会要求 `else`，增强安全性。

### 12. 阅读以下代码，写出输出。
```kotlin
fun main() {
    val s: String? = null
    println(s?.uppercase()?.takeIf { it.length > 3 } ?: "fallback")
}
```

**答案：** `fallback`

**解析：** `s?.uppercase()` 因 `s` 为 `null` 直接返回 `null`；Elvis 运算符 `?:` 在左侧为 `null` 时返回 `"fallback"`。`takeIf` 不会被执行。

---

# 第二部分：数据结构与容器

### 13. 下列哪个函数用于创建不可变 List？
A. `mutableListOf()`  
B. `arrayListOf()`  
C. `listOf()`  
D. `arrayOf()`

**答案：C**

**解析：** `listOf()` 创建只读 `List`；`mutableListOf()` 与 `arrayListOf()` 创建可变列表；`arrayOf()` 创建数组。

### 14. 以下代码执行后 `m` 的内容是？
```kotlin
val m = mapOf("a" to 1, "a" to 2, "b" to 3)
```
A. `{a=1, b=3}`  
B. `{a=2, b=3}`  
C. `{a=1, a=2, b=3}`  
D. 编译错误

**答案：B**

**解析：** `mapOf` 中后出现的键会覆盖先出现的键，因此 `a` 最终为 2。

### 15. 以下哪个操作在只读 `List<Int>` 上调用会导致编译错误？
A. `list[0]`  
B. `list.size`  
C. `list.add(1)`  
D. `list.indexOf(1)`

**答案：C**

**解析：** 只读 `List` 没有 `add` 方法，调用会编译错误；其他操作均可在只读集合上执行。

### 16. 对 `List<Int>` 保留偶数，应调用 ______。

**答案：** `filter { it % 2 == 0 }`

**解析：** `filter` 接收谓词并返回满足条件的元素集合；`it` 表示集合中的每个元素。

### 17. 使用 ______ 方法可以在 Map 中键不存在时返回自定义值，而不是抛出异常。

**答案：** `getOrElse`

**解析：** `map.getOrElse(key) { defaultValue }` 在键不存在时执行 lambda 返回默认值，比 `getValue` 更安全。

### 18. `Array<Int>` 与 `List<Int>` 在 Kotlin 中是完全相同的类型。

**答案：** ❌错误

**解析：** `Array<Int>` 是固定大小的 JVM 数组类型，可变元素；`List<Int>` 是只读集合接口，二者 API 与语义均不同。

### 19. 编写一个 Kotlin 函数，统计字符串列表中每个单词出现的次数，返回 `Map<String, Int>`。

**答案：**
```kotlin
fun countWords(words: List<String>): Map<String, Int> =
    words.groupingBy { it }.eachCount()
```

**解析：** `groupingBy` 按单词分组，`eachCount()` 统计每组的元素个数，简洁且高效。

### 20. 编写函数，将字符串列表按长度分组，返回 `Map<Int, List<String>>`。

**答案：**
```kotlin
fun groupByLength(words: List<String>): Map<Int, List<String>> =
    words.groupBy { it.length }
```

**解析：** `groupBy` 根据 lambda 返回值将元素分组为 `Map<key, List<T>>`，此处 key 为字符串长度。

### 21. 阅读代码，写出输出。
```kotlin
fun main() {
    val nums = listOf(1, 2, 3, 4, 5)
    val r = nums.filter { it > 2 }.map { it * it }.take(2)
    println(r)
}
```

**答案：** `[9, 16]`

**解析：** 先过滤出 3、4、5，再映射为平方 9、16、25，最后 `take(2)` 取前两个。

### 22. 阅读代码，写出 `m` 的内容。
```kotlin
data class User(val id: Int, val name: String)
val users = listOf(User(1, "A"), User(2, "B"))
val m = users.associate { it.id to it.name }
```

**答案：** `{1=A, 2=B}`

**解析：** `associate` 将每个元素转换为 `Pair`，以 `Pair.first` 为键、`Pair.second` 为值构建 Map。

---

# 第三部分：函数/方法/模块

### 23. 以下函数调用结果是？
```kotlin
fun greet(name: String = "World", prefix: String = "Hello") = "$prefix, $name!"
println(greet(prefix = "Hi"))
```
A. `Hello, World!`  
B. `Hi, World!`  
C. `Hello, !`  
D. 编译错误

**答案：B**

**解析：** `name` 使用默认值 `"World"`，`prefix` 通过命名参数传 `"Hi"`，结果为 `Hi, World!`。

### 24. 哪个调用方式在 Kotlin 中是合法的？
```kotlin
fun copy(from: String, to: String, overwrite: Boolean = false)
```
A. `copy("a", "b", true)`  
B. `copy(to = "b", from = "a")`  
C. `copy("a", overwrite = true)`  
D. 以上全部

**答案：D**

**解析：** Kotlin 支持位置参数、命名参数及默认值混合使用，只要所有非默认参数都被覆盖即可。

### 25. 对于声明 `fun printAll(vararg items: String)`，以下调用正确的是？
A. `printAll("a", "b")`  
B. `printAll(arrayOf("a", "b"))`  
C. `printAll(*arrayOf("a", "b"))`  
D. A 和 C

**答案：D**

**解析：** `vararg` 可直接传入多个实参，也可以用展开运算符 `*` 传入数组；直接传数组会导致类型不匹配。

### 26. 下面哪个是 Kotlin 中 `(Int, Int) -> Int` 的正确实现？
A. `fun(a: Int, b: Int) = a + b`  
B. `val sum: (Int, Int) -> Int = { a, b -> a + b }`  
C. `fun sum(a Int, b Int): Int { return a+b }`  
D. `val sum = { a, b -> a + b }`

**答案：B**

**解析：** `(Int, Int) -> Int` 是函数类型，lambda 需显式声明参数类型或让编译器推断；B 显式标注函数类型，正确。

### 27. 将以下函数改写为单表达式函数：`fun square(x: Int): Int { return x * x }` → `fun square(x: Int) = ______`。

**答案：** `x * x`

**解析：** 单表达式函数可省略返回类型与大括号，直接用 `=` 后跟表达式。

### 28. 使用尾随 lambda 语法，写出 `listOf(1,2,3).fold(0, { acc, i -> acc + i })` 的等价写法：______。

**答案：** `listOf(1,2,3).fold(0) { acc, i -> acc + i }`

**解析：** 当函数的最后一个参数是 lambda 时，可将其写在圆括号之外，形成更清晰的 DSL 风格。

### 29. Kotlin 文件中的顶层函数编译后会在对应文件名加 `Kt` 的类中生成静态方法。

**答案：** ✅正确

**解析：** 顶层函数会被编译成以文件名+`Kt` 为名的 Java 类中的静态方法，例如 `Utils.kt` 中的函数位于 `UtilsKt`。

### 30. 简述 `noinline` 与 `crossinline` 的作用。

**参考答案：**
- `noinline`：禁用某个 lambda 参数的内联，允许它作为对象被传递或多次引用。
- `crossinline`：禁止 lambda 参数中使用非局部返回（`return`），同时仍允许该 lambda 被内联到调用处。

### 31. 简述函数引用 `::max` 与 lambda `{ a, b -> max(a, b) }` 在使用上的主要区别。

**参考答案：**
- `::max` 直接引用已有函数，简洁且无额外 lambda 开销。
- lambda 更灵活，可包含任意表达式；若 lambda 只是转发调用，优先使用函数引用。

### 32. 实现一个高阶函数 `retry`，接受重试次数 `times` 和 lambda，失败时最多重试 `times` 次并返回结果。

**答案：**
```kotlin
fun <T> retry(times: Int, block: () -> T): T {
    var last: Throwable? = null
    repeat(times) {
        try {
            return block()
        } catch (e: Throwable) {
            last = e
        }
    }
    throw last ?: IllegalStateException("Retry failed")
}
```

**解析：** 使用 `repeat` 循环执行 lambda，成功立即返回，失败记录异常，全部失败时抛出最后一次异常。

### 33. 使用尾递归实现阶乘函数 `factorial(n: Int): Int`。

**答案：**
```kotlin
tailrec fun factorial(n: Int, acc: Int = 1): Int =
    if (n <= 1) acc else factorial(n - 1, n * acc)
```

**解析：** `tailrec` 告诉编译器优化为循环，避免栈溢出；递归调用必须是函数的最后一个操作。

### 34. 阅读代码，写出输出。
```kotlin
fun join(a: String = "A", b: String = "B", sep: String = "-") = a + sep + b
fun main() {
    println(join(b = "X"))
    println(join(sep = ":", a = "Y"))
}
```

**答案：**
```
A-X
Y:B
```

**解析：** 第一个调用只指定 `b`，`a` 与 `sep` 使用默认值；第二个调用通过命名参数重新指定 `a` 与 `sep`，`b` 使用默认值。

---

# 第四部分：面向对象/类型系统

### 35. `data class User(val name: String, val age: Int)` 会自动生成以下哪些函数？
A. `equals()` / `hashCode()`  
B. `toString()`  
C. `copy()`  
D. 以上全部

**答案：D**

**解析：** 数据类自动生成 `equals`、`hashCode`、`toString`、`copy` 以及 `componentN` 解构函数。

### 36. 以下类声明中主构造函数正确的是？
A. `class Person(name: String) { }`  
B. `class Person constructor(name: String) { }`  
C. `class Person(val name: String) { }`  
D. 以上全部

**答案：D**

**解析：** Kotlin 主构造函数可省略 `constructor` 关键字，也可在参数前加 `val/var` 使其成为属性。

### 37. Kotlin 中顶层类或成员的默认可见性是？
A. `private`  
B. `protected`  
C. `internal`  
D. `public`

**答案：D**

**解析：** Kotlin 默认可见性为 `public`，与 Java 的 `package-private` 不同。

### 38. `sealed class` 的主要作用是？
A. 防止类被继承  
B. 限制子类必须定义在密封类内部  
C. 表示一组受限的类型层级，便于编译器检查 when 分支穷尽性  
D. 自动生成数据类方法

**答案：C**

**解析：** 密封类用于表示受限继承结构；配合 `when` 时编译器可验证所有子类均已处理。

### 39. 写出基于 `data class User(val name: String, val age: Int)` 创建 age 为 30 的副本：`val older = user.______`。

**答案：** `copy(age = 30)`

**解析：** 数据类的 `copy` 允许只修改部分属性，其余属性保持原值，方便创建不可变对象的变体。

### 40. 实现接口时，使用关键字 ______ 代替 `extends`/`implements`。

**答案：** `:`

**解析：** Kotlin 统一使用冒号 `:` 表示继承类或实现接口，多个接口用逗号分隔。

### 41. Kotlin 中所有类默认都是 `final` 的，需要显式使用 `open` 才能被继承。

**答案：** ✅正确

**解析：** 默认 `final` 是 Kotlin 设计选择，防止意外继承；子类化需在类、方法和属性上加 `open`。

### 42. 密封类的直接子类必须位于与密封类相同的包和模块中。

**答案：** ✅正确

**解析：** 自 Kotlin 1.5 起，密封类的子类可在同一包和模块内定义，保证编译器能掌握完整的类型集合。

### 43. 简述主构造函数、次构造函数与 `init` 块的执行顺序。

**参考答案：**
- 首先执行主构造函数参数初始化。
- 然后按类体中 `init` 块的出现顺序执行。
- 最后执行次构造函数体；次构造函数必须委托给主构造函数（显式或隐式）。

### 44. 简述 Kotlin 中抽象类与接口的区别。

**参考答案：**
- 抽象类：可保存状态（属性），只能单继承，适合“is-a”关系。
- 接口：不能保存状态（直到 Kotlin 1.8 可含有 backing field 的属性有限制），可多实现，适合定义能力契约。

### 45. 定义一个密封类 `Shape` 及子类 `Circle`、`Rectangle`，并编写函数 `area` 使用 `when` 计算面积。

**答案：**
```kotlin
sealed class Shape
data class Circle(val radius: Double) : Shape()
data class Rectangle(val width: Double, val height: Double) : Shape()

fun area(shape: Shape): Double = when (shape) {
    is Circle -> Math.PI * shape.radius * shape.radius
    is Rectangle -> shape.width * shape.height
}
```

**解析：** 密封类子类受限，`when` 作为表达式无需 `else` 即可保证穷尽性；使用智能 casts 访问子类属性。

### 46. 阅读代码，写出输出。
```kotlin
open class Animal(open val name: String) {
    init { println("Animal: $name") }
}
class Dog(name: String) : Animal(name) {
    override val name: String = "Dog:$name"
    init { println("Dog: ${super.name}") }
}
fun main() {
    Dog("Buddy")
}
```

**答案：**
```
Animal: null
Dog: null
```

**解析：** 在基类 `init` 中访问的 `name` 是子类中被覆盖的属性，但此时子类构造函数尚未执行，属性未初始化，故为 `null`（`String` 非空但运行时显示 null）。这展示了在 init/构造函数中调用 open 成员的危险。

---

# 第五部分：高级特性

### 47. 以下代码中哪一行会在编译期报错？
```kotlin
val s: String? = "kotlin"
val a = s.length
val b = s?.length
val c = s!!.length
```
A. `val a = s.length`  
B. `val b = s?.length`  
C. `val c = s!!.length`  
D. 都不会

**答案：A**

**解析：** `s` 为可空 `String?`，直接访问 `s.length` 需要安全调用 `?.` 或断言 `!!`，否则编译器报错。

### 48. 关于 `launch` 与 `async` 的说法正确的是？
A. 两者都返回 `Job`  
B. `async` 返回 `Deferred<T>`，可用 `await()` 获取结果  
C. `launch` 必须调用 `await()`  
D. `async` 不能用于 `runBlocking`

**答案：B**

**解析：** `launch` 返回 `Job`，用于 fire-and-forget；`async` 返回 `Deferred<T>`，通常与 `await()` 配合获取协程结果。

### 49. 当 `when` 的参数是 `sealed class` 实例且覆盖了所有子类时，`when` 表达式 ______。
A. 仍必须写 `else`  
B. 不需要写 `else`  
C. 会生成运行时异常  
D. 编译器忽略未覆盖的子类

**答案：B**

**解析：** 密封类子类集合在编译期已知，若 `when` 处理所有子类，编译器认为穷尽，无需 `else`。

### 50. 在 Kotlin 集合中，`List<out E>` 的 `out` 表示？
A. 该列表可写入类型为 `E` 的元素  
B. 该列表是只读的，且可安全用于协变位置  
C. 该列表可存放 `E` 的父类型  
D. 与 Java 的 `? super E` 等价

**答案：B**

**解析：** `out` 表示协变，只读集合中可安全返回 `E`，不能写入，对应 Java 的 `? extends E`。

### 51. `inline` 函数的主要优势是？
A. 自动把函数放入接口  
B. 在调用点展开函数体，减少高阶函数 lambda 的对象分配开销  
C. 强制所有参数不可变  
D. 允许函数被重写

**答案：B**

**解析：** `inline` 在编译期将函数体及 lambda 参数内联到调用处，常用于高阶函数以减少运行时对象创建。

### 52. Flow 是冷流，只有在调用 ______ 等终端操作符时才会开始收集。
A. `map`  
B. `filter`  
C. `collect`  
D. `emit`

**答案：C**

**解析：** `map`、`filter` 是中间操作；`emit` 在构建器内发送数据；`collect` 等终端操作触发实际数据流。

### 53. 补全代码：若 `name` 为 `null`，则使用 `"unknown"`。
```kotlin
val display = name ______ "unknown"
```

**答案：** `?:`

**解析：** Elvis 运算符 `?:` 在左侧表达式为 `null` 时返回右侧表达式，常用于提供默认值。

### 54. 在 Kotlin 中可以使用 `lateinit var count: Int` 延迟初始化基本类型 Int。

**答案：** ❌错误

**解析：** `lateinit` 只能用于非空的引用类型，不能用于基本类型（如 `Int`）或可空类型。

### 55. 简述 `crossinline` 与 `noinline` 在高阶 `inline` 函数中的区别。

**参考答案：**
- `noinline`：保持该 lambda 为普通对象，不随 `inline` 展开，可赋值给变量或多次调用。
- `crossinline`：仍会被内联，但禁止在 lambda 中使用非局部 `return`，防止返回语义混乱。

### 56. 简述 `by lazy` 与 `lateinit` 的适用场景。

**参考答案：**
- `by lazy`：用于 `val`，第一次访问时按 lambda 初始化，线程安全（默认 SYNCHRONIZED），适合计算成本高或依赖运行时的只读属性。
- `lateinit`：用于 `var`，先声明后初始化，适合依赖注入、测试 setup 等必须在对象创建后赋值的场景。

### 57. 为 `Int` 编写扩展函数 `isEven()` 与 `isOdd()`，并演示调用。

**答案：**
```kotlin
fun Int.isEven(): Boolean = this % 2 == 0
fun Int.isOdd(): Boolean = !this.isEven()

fun main() {
    println(4.isEven()) // true
    println(5.isOdd())  // true
}
```

**解析：** 扩展函数为现有类型添加方法而不修改其源码；`this` 指接收者对象。

### 58. 编写泛型函数 `maxOf`，返回两个可比较对象中的较大值。

**答案：**
```kotlin
fun <T : Comparable<T>> maxOf(a: T, b: T): T =
    if (a > b) a else b
```

**解析：** 类型参数约束 `T : Comparable<T>` 保证可以使用 `>` 运算符；泛型函数在调用时才确定具体类型。

### 59. 使用协程并发计算两个延迟结果并求和。

**答案：**
```kotlin
import kotlinx.coroutines.*

suspend fun sumDeferred(): Int = coroutineScope {
    val a = async { computeA() }
    val b = async { computeB() }
    a.await() + b.await()
}

suspend fun computeA(): Int { delay(100); return 10 }
suspend fun computeB(): Int { delay(100); return 20 }
```

**解析：** `async` 启动两个并发协程，`await()` 挂起直至结果返回；`coroutineScope` 等待所有子协程完成。

### 60. 阅读协程代码，写出输出。
```kotlin
import kotlinx.coroutines.*
fun main() = runBlocking {
    launch {
        delay(100)
        print("A")
    }
    print("B")
    delay(200)
    print("C")
}
```

**答案：** `BAC`

**解析：** `launch` 在后台启动协程；主协程立即打印 `B`；100ms 后子协程打印 `A`；再延迟到 200ms 后打印 `C`。

### 61. 阅读 Flow 代码，写出输出。
```kotlin
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    flow {
        emit(1); emit(2); emit(3)
    }
    .filter { it > 1 }
    .map { it * 10 }
    .collect { print("$it ") }
}
```

**答案：** `20 30 `

**解析：** Flow 先过滤掉 1，再将 2、3 映射为 20、30；`collect` 逐个消费并打印。

### 62. 阅读代码，是否存在编译错误？若有，如何修正？
```kotlin
sealed class Result
object Success : Result()
data class Error(val msg: String) : Result()

fun handle(r: Result): String = when (r) {
    is Success -> "OK"
}
```

**答案：** 存在编译错误；`when` 未处理 `Error` 子类，编译器提示必须添加 `else` 或补充分支。

**解析：** 密封类虽然分支有限，但仍需覆盖所有已知子类；修正方案是添加 `is Error -> "Error: ${r.msg}"`。

---

# 第六部分：标准库与工程实践

### 63. 以下代码中 `p` 的类型与值分别是？
```kotlin
val p = StringBuilder().apply {
    append("K")
    append("otlin")
}
```
A. `Unit`  
B. `String`  
C. `StringBuilder`，内容为 `"Kotlin"`  
D. 编译错误

**答案：C**

**解析：** `apply` 返回接收者本身，并在 lambda 中通过 `this` 配置对象，因此 `p` 是配置后的 `StringBuilder`。

### 64. `let` 与 `run` 的主要区别是？
A. `let` 返回接收者，`run` 返回 lambda 结果  
B. `let` 在 lambda 中使用 `it`，`run` 使用 `this`  
C. `run` 只能用于可空对象  
D. 两者完全相同

**答案：B**

**解析：** `let` 将接收者作为参数 `it` 传入并返回 lambda 结果；`run` 在接收者作用域内执行，`this` 指向接收者，返回 lambda 结果。

### 65. 在 Android Jetpack 中，`ViewModel` 的主要作用是？
A. 替代 `Activity` 的 UI 渲染  
B. 管理 UI 相关数据并在配置变更（如旋转屏幕）后存活  
C. 处理数据库迁移  
D. 自动管理 Fragment 回退栈

**答案：B**

**解析：** `ViewModel` 用于存储和管理与 UI 相关的数据，生命周期长于 Activity/Fragment，配置变更后保持数据。

### 66. 补全代码，使发生异常时返回 0。
```kotlin
val result = runCatching { 10 / 0 }.______ { 0 }
```

**答案：** `getOrDefault`

**解析：** `runCatching` 将代码块结果封装为 `Result`；`getOrDefault` 在失败时返回默认值，成功时返回原值。

### 67. Kotlin 标准库的 `use` 扩展会在 lambda 执行完毕后自动关闭 `Closeable` 资源，即使在 lambda 中发生异常。

**答案：** ✅正确

**解析：** `use` 等价于 try-with-resources，确保 `Closeable` 在 lambda 结束时调用 `close()`，并优先抛出原始异常。

### 68. 简述 `let`、`run`、`with`、`apply`、`also` 的使用差异。

**参考答案：**
- `let`：对可空对象执行操作，lambda 参数为 `it`，返回 lambda 结果。
- `run`：对象配置并返回 lambda 结果，lambda 内 `this`。
- `with`：非扩展形式，对对象执行 lambda，返回 lambda 结果。
- `apply`：返回接收者本身，lambda 内 `this`，用于对象初始化链。
- `also`：返回接收者本身，lambda 参数为 `it`，用于附加副作用。

### 69. 简述 `ViewModel` 与 `LiveData` 在 MVVM 中的协作关系。

**参考答案：**
- `ViewModel` 持有业务逻辑与 UI 数据，生命周期独立于视图。
- `LiveData` 是可观察数据持有者，能感知生命周期，仅在活跃状态下通知观察者，避免内存泄漏。
- ViewModel 暴露 LiveData/StateFlow，View 订阅并更新 UI。

### 70. 编写一段代码，测量某段代码的执行时间并打印。

**答案：**
```kotlin
import kotlin.system.measureTimeMillis

fun main() {
    val time = measureTimeMillis {
        repeat(1_000_000) { it * it }
    }
    println("耗时 ${time}ms")
}
```

**解析：** `measureTimeMillis` 接收 lambda 并返回其执行耗时（毫秒），常用于简单性能测试。

### 71. 阅读代码，写出输出。
```kotlin
fun main() {
    val sb = StringBuilder("A")
    val r = sb.apply { append("B") }.let { it.append("C"); it.toString() }
    println(r)
}
```

**答案：** `ABC`

**解析：** `apply` 在 `sb` 上追加 `B` 并返回 `sb`；`let` 接收 `sb` 作为 `it`，追加 `C` 后返回字符串 `ABC`。

### 72. 阅读代码，写出输出。
```kotlin
fun main() {
    val r = runCatching { "100".toInt() }
        .map { it * 2 }
        .getOrThrow()
    println(r)
}
```

**答案：** `200`

**解析：** `"100".toInt()` 成功得到 100，`map` 将其乘 2，`getOrThrow` 返回成功值 200。

---

# 第七部分：智力与逻辑

### 73. 有三个箱子，分别标签为 “苹果”、“橙子”、“混合”，但所有标签都贴错了。你只能从一个箱子里拿出一个水果查看，如何确定每个箱子的真实内容？

**参考答案：**
- 从标签为 “混合” 的箱子中取出一个水果。由于标签全错，该箱实际只装一种水果。
- 若取出的是苹果，则该箱为 “苹果”；标签为 “橙子” 的箱子不能是橙子，也不能是苹果（已确定），故为 “混合”；标签为 “苹果” 的箱子则为 “橙子”。
- 若取出的是橙子，推理对称。

### 74. 数列 1、1、2、3、5、8、? 中，下一个数字是多少？请说明规律。

**参考答案：**
- 下一个数字是 13。
- 从第三项起，每一项都是前两项之和，即斐波那契数列。

### 75. 已知 `(A && B)` 为假，`(A || B)` 为真，能确定 A 与 B 的真值关系是什么？

**参考答案：**
- A 与 B 中有且仅有一个为真。
- `A && B` 为假说明不同时为真；`A || B` 为真说明至少一个为真；二者结合即“恰好一真”。

### 76. 有 8 个外观相同的小球，其中 1 个偏重。使用天平最少需要称几次一定能找出重球？请给出策略。

**参考答案：**
- 最少需要 2 次。
- 第一次将 8 个球分为 3、3、2，称两组 3 个：若平衡，重球在剩余 2 个中，第二次称即可；若不平衡，重球在较重一侧 3 个中，第二次任取 2 个称，平衡则剩余为重，否则可直接看出。

### 77. 一个房间里有三盏灯，门外有三个开关，每个开关对应一盏灯。你只能进入房间一次，如何确定每个开关控制哪盏灯？

**参考答案：**
- 打开第一个开关并等待足够长时间后关闭；立即打开第二个开关，然后进入房间。
- 亮着的灯由第二个开关控制；灭的但灯泡发热的灯由第一个开关控制；灭的且冰凉的灯由第三个开关控制。

### 78. 用 Kotlin 集合操作思维：从 1 到 100 中，先过滤掉所有偶数，再映射为平方，最后取前 5 个，结果列表是什么？

**参考答案：**
- 结果是 `[1, 9, 25, 49, 81]`。
- 1 到 100 的奇数为 1、3、5、7、9…，前 5 个奇数的平方依次是 1、9、25、49、81。

### 79. 2024 年是闰年，那么 2024 年 2 月的最后一天是星期几？（已知 2024 年 1 月 1 日是星期一）

**参考答案：**
- 2024 年 2 月 29 日是星期四。
- 1 月 1 日到 2 月 29 日共 31 + 29 = 60 天；60 mod 7 = 4；星期一往后推 4 天是星期四。

### 80. 有四个人（A、B、C、D）过桥，分别需要 1、2、5、10 分钟。只有一只手电筒，桥每次最多承受两人，且必须手持电筒。最快多久能让所有人过桥？

**参考答案：**
- 最快需要 17 分钟。
- 方案：A 与 B 过桥（2 分钟），A 带电筒返回（1 分钟），C 与 D 过桥（10 分钟），B 带电筒返回（2 分钟），A 与 B 过桥（2 分钟）。总耗时 2+1+10+2+2 = 17 分钟。

---

# 第八部分：实战演练

### 81. （综合应用题）使用密封类 `Result` 与 `Flow` 实现一个用户列表 Repository，要求包含 Loading、Success、Error 三种状态。

**答案：**
```kotlin
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

sealed class Result<out T> {
    object Loading : Result<Nothing>()
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
}

data class User(val id: Int, val name: String)

class UserRepository {
    fun fetchUsers(): Flow<Result<List<User>>> = flow {
        emit(Result.Loading)
        try {
            val users = listOf(User(1, "Alice"), User(2, "Bob"))
            emit(Result.Success(users))
        } catch (e: Exception) {
            emit(Result.Error(e))
        }
    }
}
```

**解析：** 密封类将状态限制为固定子类，`Flow` 按顺序发射状态；UI 层收集后可据此显示加载、内容或错误界面。

### 82. （综合应用题）用协程实现一个带超时与重试的简单网络请求封装。

**答案：**
```kotlin
import kotlinx.coroutines.*

suspend fun <T> fetchWithRetry(
    times: Int = 3,
    timeoutMs: Long = 5_000,
    block: suspend () -> T
): T = withTimeout(timeoutMs) {
    var last: Throwable? = null
    repeat(times) {
        try {
            return@withTimeout block()
        } catch (e: Throwable) {
            last = e
        }
    }
    throw last ?: IllegalStateException("All retries failed")
}
```

**解析：** `withTimeout` 设置单次调用总超时；`repeat` 实现重试；成功即返回，全部失败抛出最后一次异常。

### 83. （综合应用题）编写一个配置解析器，将形如 `name=Kotlin;version=2.0;debug=true` 的字符串安全解析为 data class，缺失字段使用默认值。

**答案：**
```kotlin
data class Config(
    val name: String = "Unknown",
    val version: String = "1.0",
    val debug: Boolean = false
)

fun parseConfig(raw: String): Config {
    val map = raw.split(";").mapNotNull {
        val parts = it.split("=", limit = 2)
        if (parts.size == 2) parts[0] to parts[1] else null
    }.toMap()
    return Config(
        name = map["name"] ?: "Unknown",
        version = map["version"] ?: "1.0",
        debug = map["debug"]?.toBooleanStrictOrNull() ?: false
    )
}
```

**解析：** 先按 `;` 拆分成键值对，缺失键使用 Elvis 提供默认值；`toBooleanStrictOrNull` 避免异常值导致崩溃。

### 84. （综合应用题）实现一个简易的 ViewModel 风格状态持有者，使用 `StateFlow` 暴露计数器状态，并提供增减方法。

**答案：**
```kotlin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class CounterViewModel {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()

    fun increment() { _count.value += 1 }
    fun decrement() { _count.value -= 1 }
}
```

**解析：** `MutableStateFlow` 仅在内部修改，对外暴露只读 `StateFlow`；`asStateFlow` 防止外部直接修改状态。

### 85. （综合应用题）使用 Kotlin 标准库实现一个线程安全的泛型内存缓存，支持 `get`/`put` 与基于 `computeIfAbsent` 的加载。

**答案：**
```kotlin
class MemoryCache<K, V> {
    private val map = mutableMapOf<K, V>()

    @Synchronized
    fun put(key: K, value: V) { map[key] = value }

    @Synchronized
    fun get(key: K): V? = map[key]

    @Synchronized
    fun getOrLoad(key: K, loader: (K) -> V): V {
        return map.getOrPut(key) { loader(key) }
    }
}
```

**解析：** `getOrPut` 在键不存在时执行 lambda 加载并缓存；`@Synchronized` 保证多线程安全，生产环境可用 `ConcurrentHashMap`。

### 86. （代码调试题）以下代码存在什么问题？如何修正？
```kotlin
fun main() {
    GlobalScope.launch {
        delay(1000)
        println("done")
    }
}
```

**答案：** 问题：`GlobalScope` 生命周期与整个应用相同，可能导致内存泄漏，且主线程可能立刻退出导致协程未执行。

**修正方案：**
```kotlin
fun main() = runBlocking {
    launch {
        delay(1000)
        println("done")
    }
}
```

**解析：** 使用结构化并发作用域（如 `runBlocking`、`lifecycleScope`、`viewModelScope`）管理协程生命周期，避免泄漏并确保完成。

### 87. （代码调试题）以下代码意图向只读 List 添加元素，存在什么错误？请修正。
```kotlin
fun main() {
    val list: List<String> = mutableListOf("a")
    list.add("b")
}
```

**答案：** 错误：变量声明为 `List<String>`，虽然实际对象是 `MutableList`，但静态类型不可变，调用 `add` 编译失败。

**修正方案：**
```kotlin
fun main() {
    val list = mutableListOf("a")
    list.add("b")
}
```

**解析：** Kotlin 集合分为只读接口与可变接口；需要修改时应声明为 `MutableList` 或使用 `mutableListOf`。

### 88. （代码调试题）以下协程代码在 Android 主线程调用会导致 ANR，请指出问题并修正。
```kotlin
suspend fun loadData(): String = withContext(Dispatchers.Main) {
    networkRequest() // 同步阻塞网络请求
}
```

**答案：** 问题：在 `Dispatchers.Main` 中执行阻塞网络请求会卡住主线程，导致 ANR。

**修正方案：**
```kotlin
suspend fun loadData(): String = withContext(Dispatchers.IO) {
    networkRequest()
}
```

**解析：** 阻塞 IO 应切换到 `Dispatchers.IO`；主线程只用于轻量 UI 更新，耗时操作必须放到后台调度器。

### 89. （系统设计题）设计一个 Android 离线优先的笔记应用架构，说明各层职责与选用的 Jetpack 组件。

**参考答案：**
- **UI 层**：Activity/Fragment/Compose 负责展示；通过 `ViewModel` 暴露 `StateFlow`/`LiveData`，观察者更新界面。
- **领域/数据层**：`Repository` 封装本地 Room 数据库与远程 Retrofit 数据源；优先返回本地缓存，后台同步云端。
- **数据源**：Room 作为本地 SSOT（Single Source of Truth），配合 `Flow` 实现数据自动刷新；WorkManager 处理定时同步与冲突解决。
- **依赖注入**：使用 Hilt/Koin 管理 `ViewModel`、`Repository`、数据库实例生命周期。
- **离线策略**：网络可用时拉取并写库；无网络时直接读库；通过 `ConnectivityManager` 或 WorkManager 约束触发同步。

### 90. （系统设计题）设计一个基于 Kotlin Flow 与 Repository 模式的图片列表功能，要求支持分页加载、下拉刷新与错误重试。

**参考答案：**
- **Repository**：暴露 `Pager<Int, ImageItem>`（使用 Paging 3 库），`Pager` 内部通过 `PagingSource` 按页请求网络或本地数据。
- **ViewModel**：将 `Pager.flow` 转换为 `Flow<PagingData<ImageItem>>`，并提供 `refresh()`、`retry()` 公开方法。
- **UI 层**：使用 `LazyColumn`/`RecyclerView` 配合 `PagingDataAdapter`；监听 `LoadState` 显示加载、空态与错误界面。
- **错误重试**：在 `PagingSource.load()` 失败时返回 `LoadResult.Error`，UI 调用 `adapter.retry()`；ViewModel 中维护 `trigger` StateFlow，刷新时更新 `trigger` 重新构建 Flow。
- **下拉刷新**：触发 ViewModel 的 `refresh()`，内部调用 `PagingDataAdapter.refresh()` 或重建 Pager Flow。

---

## 📊 参考答案汇总

| 题号 | 答案 | 题号 | 答案 | 题号 | 答案 |
|:---:|:---|:---:|:---|:---:|:---|
| 1 | B | 2 | B | 3 | B |
| 4 | C | 5 | `Long` | 6 | `"""..."""` |
| 7 | `10 downTo 1 step 2` | 8 | ❌错误 | 9 | ❌错误 |
| 10 | `val` 只读；`var` 可变；`const val` 编译期常量 | 11 | 表达式、多条件范围类型判断、穷尽检查 | 12 | `fallback` |
| 13 | C | 14 | B | 15 | C |
| 16 | `filter { it % 2 == 0 }` | 17 | `getOrElse` | 18 | ❌错误 |
| 19 | `words.groupingBy { it }.eachCount()` | 20 | `words.groupBy { it.length }` | 21 | `[9, 16]` |
| 22 | `{1=A, 2=B}` | 23 | B | 24 | D |
| 25 | D | 26 | B | 27 | `x * x` |
| 28 | `listOf(1,2,3).fold(0) { acc, i -> acc + i }` | 29 | ✅正确 | 30 | `noinline` 不内联；`crossinline` 内联但禁止非局部 return |
| 31 | `::max` 直接引用函数，lambda 更灵活 | 32 | `retry(times, block)` 高阶函数 | 33 | `tailrec fun factorial(n, acc=1)` |
| 34 | `A-X` / `Y:B` | 35 | D | 36 | D |
| 37 | D | 38 | C | 39 | `copy(age = 30)` |
| 40 | `:` | 41 | ✅正确 | 42 | ✅正确 |
| 43 | 主构造 → init → 次构造 | 44 | 抽象类可保存状态、单继承；接口可多实现、定义契约 | 45 | sealed Shape + when area |
| 46 | `Animal: null` / `Dog: null` | 47 | A | 48 | B |
| 49 | B | 50 | B | 51 | B |
| 52 | C | 53 | `?:` | 54 | ❌错误 |
| 55 | `crossinline` 禁止非局部 return；`noinline` 不内联 | 56 | `by lazy` 用于 `val` 延迟初始化；`lateinit` 用于 `var` 先声明后赋值 | 57 | `fun Int.isEven()/isOdd()` 扩展函数 |
| 58 | `fun <T : Comparable<T>> maxOf(a, b)` | 59 | `async` 并发 + `await` 求和 | 60 | `BAC` |
| 61 | `20 30 ` | 62 | 编译错误；补充 `is Error` 分支 | 63 | C |
| 64 | B | 65 | B | 66 | `getOrDefault` |
| 67 | ✅正确 | 68 | `let/run/with/apply/also` 作用域差异 | 69 | ViewModel 持有数据，LiveData 生命周期感知通知 UI |
| 70 | `measureTimeMillis { ... }` | 71 | `ABC` | 72 | `200` |
| 73 | 从“混合”箱取一个水果，依标签全错推导其余两箱 | 74 | `13`（斐波那契） | 75 | A、B 恰好一个为真 |
| 76 | 2 次；3/3/2 分组策略 | 77 | 开关开一会关，第二个开，进屋看亮/热/凉 | 78 | `[1, 9, 25, 49, 81]` |
| 79 | 星期四 | 80 | 17 分钟 | 81 | sealed Result + Flow Repository |
| 82 | `withTimeout` + `repeat` 重试封装 | 83 | 按 `;`/`=` 解析，缺失使用默认值 | 84 | `MutableStateFlow` + `asStateFlow` CounterViewModel |
| 85 | `@Synchronized` + `getOrPut` 缓存 | 86 | 避免 `GlobalScope`，使用 `runBlocking`/`viewModelScope` | 87 | 声明为 `MutableList` 或 `mutableListOf` |
| 88 | 使用 `Dispatchers.IO` 执行网络请求 | 89 | MVVM + Room + Repository + WorkManager + Hilt/Koin | 90 | Paging 3 + Flow + Repository + LoadState 错误重试 |

## 🔐 最终签名

**DNA:** #龍芯⚡️丙午·甲申·壬寅·坤卦-LEARNING-KOTLIN-EXAM-v1.0-UID9622
**GPG:** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**确认码:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**创建者:** 诸葛鑫（UID9622）
**三色审计:** 🟢 通过


