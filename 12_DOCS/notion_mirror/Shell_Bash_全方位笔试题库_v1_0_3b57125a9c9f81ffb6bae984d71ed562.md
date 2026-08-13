# 🐉 Shell/Bash 全方位笔试题库 v1.0

> Notion URL: https://app.notion.com/p/Shell-Bash-v1-0-3b57125a9c9f81ffb6bae984d71ed562
> Created: 2026-08-07T15:41:00.000Z
> Last edited: 2026-08-07T15:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 🐉 Shell/Bash 全方位笔试题库 v1.0

> DNA: #龍芯⚡️丙午·甲申·壬寅·坤卦-LEARNING-SHELL-EXAM-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 三色: 🟢 通过
> 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 📋 试卷结构

| 部分 | 题型 | 题量 | 分值 |
|:---:|:---|:---:|:---:||
| 第一部分：Shell/Bash基础语法 | 选择题、填空题、判断题、简答题 | 14 | 18 |
| 第二部分：数据结构与容器 | 选择题、填空题、判断题、程序分析题 | 8 | 12 |
| 第三部分：函数/方法/模块 | 选择题、填空题、简答题、编程题 | 10 | 20 |
| 第四部分：面向对象/类型系统 | 选择题、判断题、简答题、编程题 | 6 | 10 |
| 第五部分：高级特性 | 编程题、程序分析题、综合应用题、代码调试题 | 10 | 30 |
| 第六部分：标准库与工程实践 | 选择题、填空题、判断题、系统设计题 | 10 | 26 |
| 第七部分：智力与逻辑 | 智力与逻辑题 | 5 | 15 |
| 第八部分：实战演练 | 编程题、综合应用题、代码调试题、系统设计题 | 7 | 23 |
| **合计** | — | **70** | **150** |

---

## 📊 详细题型分布

| 题型 | 题量 | 每题分值 | 小计 |
|:---:|:---:|:---:|:---:||
| 选择题 | 14 | 1 | 14 |
| 填空题 | 10 | 1 | 10 |
| 判断题 | 10 | 1 | 10 |
| 简答题 | 5 | 3 | 15 |
| 编程题 | 8 | 3 | 24 |
| 程序分析题 | 5 | 3 | 15 |
| 智力与逻辑题 | 5 | 3 | 15 |
| 综合应用题 | 5 | 3 | 15 |
| 代码调试题 | 4 | 3 | 12 |
| 系统设计题 | 4 | 5 | 20 |
| **合计** | **70** | — | **150** |

---

## 🎯 知识点分布与难度标注

| 知识点 | 难度 | 分值 |
|:---:|:---:|:---:||
| 基础语法 | ⭐ | 18 |
| 数据类型与容器 | ⭐⭐ | 12 |
| 函数与模块 | ⭐⭐⭐ | 20 |
| 面向对象/类型系统 | ⭐⭐⭐⭐ | 10 |
| 高级特性 | ⭐⭐⭐⭐ | 30 |
| 标准库与工程实践 | ⭐⭐⭐⭐ | 26 |
| 逻辑思维 | ⭐⭐⭐⭐⭐ | 15 |
| 实战演练 | ⭐⭐⭐⭐ | 23 |

---

# 第一部分：Shell/Bash基础语法

## 一、选择题（每题1分，共4分）

### 1. 以下哪个命令可以正确输出当前用户的家目录？

A. `echo HOME`
B. `echo $home`
C. `echo $HOME`
D. `echo ${ HOME }`

**答案：C**

**解析：** 在 Bash 中，变量引用使用 `$VAR` 或 `${VAR}`，且变量名区分大小写。`$HOME` 是系统预定义变量。`echo HOME` 会输出字符串“HOME”，`$home` 未定义时为空。

### 2. `echo $?` 的输出表示什么含义？

A. 上一条命令的进程 ID
B. 上一条命令的退出状态码
C. 当前脚本名
D. 命令行参数个数

**答案：B**

**解析：** `$?` 保存最近一个前台命令的退出状态码，`0` 通常表示成功，非 `0` 表示失败或不同错误。

### 3. 仅将命令的标准错误（stderr）重定向到文件 `err.log`，应使用哪个写法？

A. `cmd > err.log`
B. `cmd 2> err.log`
C. `cmd &> err.log`
D. `cmd >> err.log`

**答案：B**

**解析：** 文件描述符 `2` 代表 stderr，`2>` 只重定向 stderr。`&>` 会把 stdout 与 stderr 同时重定向，`>` 只重定向 stdout。

### 4. 管道符 `cmd1 | cmd2` 的作用是？

A. 先执行 cmd1，成功后执行 cmd2
B. 将 cmd1 的标准输出作为 cmd2 的标准输入
C. 将 cmd1 与 cmd2 的 stderr 合并
D. 在后台并行执行两个命令

**答案：B**

**解析：** 管道是进程间通信机制，把左侧命令的标准输出连接到右侧命令的标准输入。

## 二、填空题（每题1分，共4分）

### 5. 在函数内部声明局部变量应使用关键字 `______`。

**答案：local**

**解析：** `local` 使变量只在当前函数作用域有效，函数返回后不会污染调用环境的同名变量。

### 6. 标准输出（stdout）对应的文件描述符是 `______`。

**答案：1**

**解析：** Shell 中 `0` 为 stdin，`1` 为 stdout，`2` 为 stderr。

### 7. 在条件表达式 `[[ $str =~ ^[0-9]+$ ]]` 中，` =~ ` 表示进行 `______` 匹配。

**答案：正则表达式（regex）**

**解析：** `[[ ... =~ regex ]]` 是 Bash 扩展条件测试，支持扩展正则表达式匹配字符串。

### 8. 旧式的命令替换语法使用反引号，现代 Bash 推荐的语法是 `______`。

**答案：$(命令)**

**解析：** `$(command)` 支持嵌套，可读性更好；旧式反引号 `` `command` `` 在嵌套和转义时容易出错。

## 三、判断题（每题1分，共4分）

### 9. Shell 中退出状态码 `0` 表示命令执行成功。

**答案：正确**

**解析：** 按照 Unix 惯例，退出状态码 `0` 表示成功，非零表示失败或不同异常。

### 10. Shebang `#!/bin/bash` 必须位于脚本文件的第一行，且前面不能有空格。

**答案：正确**

**解析：** 操作系统内核通过读取文件最开始的两个字节 `#!` 来识别解释器，因此 shebang 必须从文件开头开始。

### 11. 重定向 `echo "foo" >> file` 会覆盖 file 原有内容。

**答案：错误**

**解析：** `>>` 是追加模式，不会覆盖原有内容；`>` 才会覆盖。

### 12. 单引号字符串会原样保留，双引号字符串允许变量和命令替换展开。

**答案：正确**

**解析：** 单引号禁止一切扩展，双引号允许 `$var`、`$(cmd)`、反引号等扩展，但保留字面空格。

## 四、简答题（每题3分，共6分）

### 13. 请说明 `$*` 与 `$@` 的区别，尤其是在被双引号包围时。

**答案：当不加引号时两者行为类似；加引号后，`"$*"` 展开为单个字符串（以 IFS 分隔），`"$@"` 展开为保留每个参数的独立单词，常用于遍历所有参数。**

**解析：** `$*` 将所有位置参数合并为一个词，`$@` 保持每个参数的独立。循环中推荐 `for arg in "$@"; do ... done`。

### 14. 解释 `source script.sh`（或 `. script.sh`）与直接执行 `./script.sh` 的区别。

**答案：`source` / `.` 在当前 Shell 进程中执行脚本，脚本中定义的环境变量和函数会影响当前会话；`./script.sh` 会启动子进程执行，变量不会带回到父进程，且文件需要可执行权限。**

**解析：** Source 用于加载配置、函数库；直接执行用于独立运行程序逻辑。

---

# 第二部分：数据结构与容器

## 一、选择题（每题1分，共2分）

### 15. 下面哪些写法可以创建 Bash 索引数组？

A. `declare -A arr`
B. `arr=(a b c)`
C. `declare -a arr`
D. B 和 C

**答案：D**

**解析：** `declare -a` 显式声明索引数组；`arr=(...)` 直接赋值也会创建索引数组。`declare -A` 创建关联数组。

### 16. 遍历关联数组 `declare -A map` 的所有键，应使用？

A. `${map[@]}`
B. `${!map[@]}`
C. `${#map[@]}`
D. `${map[*]}`

**答案：B**

**解析：** `${!map[@]}` 返回数组的所有索引（键）。`${map[@]}` 返回值，`${#map[@]}` 返回元素个数。

## 二、填空题（每题1分，共2分）

### 17. 访问数组 `arr` 第一个元素的语法是 `______`。

**答案：${arr[0]}**

**解析：** Bash 数组使用零基索引，`${arr[0]}` 取第一个元素，`${arr[@]}` 取全部。

### 18. 获取数组 `arr` 元素个数的语法是 `______`。

**答案：${#arr[@]}**

**解析：** `${#arr[@]}` 返回数组长度；对字符串变量 `${#var}` 返回字符串长度。

## 三、判断题（每题1分，共2分）

### 19. Bash 关联数组使用整数索引。

**答案：错误**

**解析：** 关联数组使用字符串作为键，通过 `declare -A` 声明；索引数组才使用整数索引。

### 20. `declare -A arr` 会创建一个关联数组。

**答案：正确**

**解析：** `-A` 选项用于声明 associative array（关联数组），Bash 4.0 及以上支持。

## 四、程序分析题（每题3分，共6分）

### 21. 分析以下脚本输出：
```bash
arr=(foo bar baz)
echo ${#arr[@]}
echo ${arr[-1]}
```

**答案：输出为：
```
3
baz
```**

**解析：** `${#arr[@]}` 返回数组长度 3；Bash 支持负索引，`${arr[-1]}` 取最后一个元素。

### 22. 分析以下脚本输出：
```bash
x="1 2 3"
set -- $x
echo $#
echo "$@"
```

**答案：输出为：
```
3
1 2 3
```**

**解析：** `set --` 重新设置位置参数；`$#` 为参数个数 3，`"$@"` 展开为 `1 2 3`。

---

# 第三部分：函数/方法/模块

## 一、选择题（每题1分，共3分）

### 23. Shell 函数要把计算得到的字符串结果返回给调用者，最常用的方式是？

A. `return 0`
B. `echo "$result"`
C. `exit 0`
D. `export result`

**答案：B**

**解析：** `return` 只能返回 0-255 的整数退出状态；通过 `echo` 输出到 stdout，调用者用 `$(func)` 捕获是返回字符串结果的标准做法。

### 24. 在函数中使用 `local var=1` 的作用是？

A. 把变量导出到子进程
B. 声明全局变量
C. 将变量作用域限制在函数内
D. 没有任何作用

**答案：C**

**解析：** `local` 声明的变量只在函数执行期间可见，不会覆盖外部同名变量。

### 25. 如何将函数 `myfunc` 的输出赋值给变量 `out`？

A. `out=myfunc`
B. `out=$(myfunc)`
C. `out={myfunc}`
D. `out=myfunc()`

**答案：B**

**解析：** 命令替换 `$(...)` 捕获函数的标准输出并赋给变量。

## 二、填空题（每题1分，共2分）

### 26. 除了 `function foo() { ... }`，函数定义还可以省略 `function`，写成 `______ { ... }`。

**答案：foo()**

**解析：** Shell 函数支持 `name() { commands; }` 和 `function name() { commands; }` 两种语法。

### 27. 在脚本中获取脚本自身所在目录时，常用 `$(cd "$(dirname "$0")" && pwd)`，其中 `______` 用于切换工作目录。

**答案：cd**

**解析：** `cd "$(dirname "$0")"` 进入脚本所在目录，`pwd` 返回绝对路径，从而避免相对路径问题。

## 三、简答题（每题3分，共6分）

### 28. 解释 `set -euo pipefail` 这三项选项各自的作用。

**答案：`-e`：命令返回非零时立即退出脚本；`-u`：使用未定义变量时报错；`-o pipefail`：管道中任一命令失败，整条管道的退出状态为失败（而不仅是最后一个命令）。**

**解析：** 三者合称“严格模式”，可显著减少脚本中隐藏的错误；常与 `set -x` 调试模式区分使用。

### 29. 如何 source 另一个脚本并向其传递参数？

**答案：使用 `source ./script.sh arg1 arg2` 或 `. ./script.sh arg1 arg2`。被 source 的脚本中 `$1`、`$2` 等位置参数会接收到这些参数，但会覆盖当前脚本的位置参数，必要时先保存 `$@`。**

**解析：** source 执行的脚本共享当前 Shell 环境，因此位置参数也被传递并可能覆盖。

## 四、编程题（每题3分，共9分）

### 30. 编写函数 `sum()`，接受任意多个整数参数并输出它们的和。

**答案：```bash
sum() {
  local total=0
  for n in "$@"; do
    total=$((total + n))
  done
  echo "$total"
}
```**

**解析：** 使用 `"$@"` 遍历所有参数，`local` 保证 `total` 不污染外部变量。`$((...))` 进行整数运算。

### 31. 编写一行命令，列出当前目录下所有 `.sh` 文件并按文件名排序。

**答案：```bash
find . -maxdepth 1 -type f -name "*.sh" | sort
```**

**解析：** `find` 按模式查找，`| sort` 排序。为避免文件名含空格的问题，更健壮的做法是使用 `find ... -print0 | sort -z`。

### 32. 编写函数 `is_even`，当第一个参数为偶数时返回退出码 `0`，否则返回 `1`。

**答案：```bash
is_even() {
  (( "$1" % 2 == 0 ))
}
```**

**解析：** `(( ... ))` 是算术计算环境，条件为真时退出码为 `0`，为假时退出码为 `1`，正好对应函数的返回要求。

---

# 第四部分：面向对象/类型系统

## 一、选择题（每题1分，共2分）

### 33. `declare -i x` 会把变量 `x` 声明为什么类型？

A. 整数
B. 只读
C. 关联数组
D. 导出变量

**答案：A**

**解析：** `-i` 选项声明整数变量，赋值时会尝试进行算术求值。

### 34. `declare -r var=5` 使变量 `var` 具有什么属性？

A. 局部
B. 只读
C. 引用
D. 数组

**答案：B**

**解析：** `-r` 声明只读变量，赋值后不能被修改或取消。

## 二、判断题（每题1分，共2分）

### 35. Bash 原生支持像 Python 一样的类与对象。

**答案：错误**

**解析：** Bash 没有内置的类、对象、继承机制；可以通过关联数组和函数模拟，但不是语言原生支持。

### 36. `declare -n ref=$1` 会创建一个 name reference（ nameref ）。

**答案：正确**

**解析：** Bash 4.3+ 支持 `declare -n` 创建对另一个变量名的引用，常用于按名称传递数组。

## 三、简答题（每题3分，共3分）

### 37. 什么是 Bash 的 nameref？请给出一个典型使用场景。

**答案：nameref 是通过 `declare -n ref=var` 创建的变量引用，对 `ref` 的读写实际上是对 `var` 的读写。典型场景：函数需要按名称修改调用者指定的变量或数组，例如 `f() { local -n out=$1; out=value; }`。**

**解析：** nameref 让函数可以间接操作外部变量，避免全局污染。

## 四、编程题（每题3分，共3分）

### 38. 使用 nameref 编写函数 `max`，将两个整数中的较大值写入调用者指定的变量名。

**答案：```bash
max() {
  local -n out=$1
  local a=$2 b=$3
  if (( a > b )); then
    out=$a
  else
    out=$b
  fi
}

# 用法
result=0
max result 10 25
echo "$result"   # 25
```**

**解析：** `local -n out=$1` 把 `out` 绑定到调用者变量名；通过赋值 `out` 即可修改外部变量。

---

# 第五部分：高级特性

## 一、编程题（每题3分，共6分）

### 42. 使用 `xargs` 编写一行命令，删除 `files.txt` 中列出的所有文件（每行一个路径）。

**答案：```bash
xargs -a files.txt -d "\n" rm -f
```**

**解析：** `-a files.txt` 从文件读取输入，`-d "\n"` 指定换行分隔，避免文件名含空格被错误拆分。

### 43. 使用 `mapfile`（或 `readarray`）把文件 `data.txt` 的每行读入数组 `lines`。

**答案：```bash
mapfile -t lines < data.txt
```**

**解析：** `mapfile -t` 读取标准输入到数组并去掉每行末尾的换行符；`readarray` 是同义词。

## 二、程序分析题（每题3分，共9分）

### 39. 分析以下脚本是否会在 `false` 处退出，并说明最终输出：
```bash
set -e
false || true
echo ok
```

**答案：不会退出，最终输出 `ok`。**

**解析：** `set -e` 在遇到命令失败时会退出，但如果失败命令位于 `||` 的左侧，则被认为是“已处理”的错误，不会触发退出。

### 40. 分析以下循环的输出：
```bash
for i in {1..5..2}; do
  echo "$i"
done
```

**答案：输出：
```
1
3
5
```**

**解析：** {start..end..step} 是 Bash 的花括号序列扩展，`{1..5..2}` 生成 1、3、5。

### 41. 启用 `shopt -s extglob` 后，以下代码会输出什么？
```bash
shopt -s extglob
[[ "file.txt" == ?(*.txt|*.md) ]] && echo yes
```

**答案：输出 `yes`。**

**解析：** `extglob` 开启扩展通配，`?(*.txt|*.md)` 匹配空或 `.txt` / `.md` 结尾的字符串；`file.txt` 匹配成功。

## 三、综合应用题（每题3分，共9分）

### 44. 给定一个日志文件 `access.log`，每行格式为 `IP METHOD STATUS PATH`，请写出一条管道命令统计每种 HTTP 状态码（第三列）出现的次数，并按出现次数降序排列。

**答案：```bash
awk "{print \$3}" access.log | sort | uniq -c | sort -rn
```**

**解析：** `awk` 提取第三列，`sort | uniq -c` 统计频次，`sort -rn` 按数字降序。

### 45. 请写出一条命令，找出 `/var/log` 下最大的 5 个普通文件，并输出它们的大小（字节）与完整路径。

**答案：```bash
find /var/log -type f -printf "%s %p\n" | sort -rn | head -n 5
```**

**解析：** `find -printf` 自定义输出格式，`sort -rn` 按大小降序，`head` 取前 5。若系统不支持 `-printf`，可用 `du -ah | sort -rh | head -5`。

### 46. 请写出一条 crontab 表达式，让备份脚本 `/home/user/backup.sh` 每周日凌晨 02:30 执行。

**答案：```
30 2 * * 0 /home/user/backup.sh
```**

**解析：** crontab 格式为 `分 时 日 月 周`。`0` 表示周日；也可使用 `7`。命令使用绝对路径更安全。

## 四、代码调试题（每题3分，共6分）

### 47. 以下判断语句在 `var` 为空时会报错，请修正。
```bash
if [ $var = "ok" ]; then
  echo yes
fi
```

**答案：```bash
if [[ "$var" == "ok" ]]; then
  echo yes
fi
```**

**解析：** 原语句中 `$var` 为空会导致 `[ = "ok" ]` 语法错误。使用 `[[` 是 Bash 扩展测试，无需对变量加引号也能安全处理空值；或者保持 `[` 并为 `"$var"` 加双引号。

### 48. 以下循环在文件名包含空格时会出错，请改写为健壮的版本。
```bash
for f in $(ls *.log); do
  rm "$f"
done
```

**答案：```bash
for f in *.log; do
  rm -- "$f"
done
```**

**解析：** `$(ls *.log)` 会按空格分词，导致含空格文件名被拆成多个参数。直接使用 glob `*.log` 并在引用 `"$f"` 后处理，可正确处理任意合法文件名。`--` 防止文件名以 `-` 开头被解析为选项。

---

# 第六部分：标准库与工程实践

## 一、选择题（每题1分，共3分）

### 49. 以下哪个命令/服务用于周期性调度任务？

A. `at`
B. `cron`
C. `batch`
D. `nohup`

**答案：B**

**解析：** `cron` 用于按周期执行命令；`at` 一次性执行；`batch` 按系统负载执行；`nohup` 忽略挂断信号。

### 50. `curl -s URL` 中的 `-s` 选项含义是？

A. 只显示响应头
B. 静默模式，不显示进度和错误信息
C. 跟随重定向
D. 使用 POST 方法

**答案：B**

**解析：** `-s`/`--silent` 静默模式；跟随重定向用 `-L`，POST 用 `-X POST`。

### 51. 测试文件是否可执行应使用哪个条件运算符？

A. `-e`
B. `-f`
C. `-x`
D. `-d`

**答案：C**

**解析：** `-x` 测试文件存在且可执行；`-e` 存在；`-f` 普通文件；`-d` 目录。

## 二、填空题（每题1分，共2分）

### 52. 要让命令在用户退出终端后继续运行，可在命令前加上 `______`。

**答案：nohup**

**解析：** `nohup` 使进程忽略 SIGHUP 信号，通常与 `&` 后台运行配合使用，如 `nohup ./job.sh &`。

### 53. 命令 `trap "echo caught" INT` 用于捕获 `______` 信号。

**答案：SIGINT（中断信号）**

**解析：** `INT` 是 `SIGINT` 的简写，通常由 Ctrl+C 产生；`trap` 用于指定信号处理动作。

## 三、判断题（每题1分，共2分）

### 54. `set -x` 会在执行每条命令前将其打印到 stderr。

**答案：正确**

**解析：** `-x` 是 xtrace 模式，便于调试脚本。

### 55. `crontab -e` 编辑的是系统级 crontab 文件。

**答案：错误**

**解析：** `crontab -e` 编辑当前用户的 crontab；系统级 cron 通常需要 root 权限修改 `/etc/crontab` 或 `/etc/cron.d/`。

## 四、系统设计题（每题5分，共15分）

### 56. 设计一个 Shell 健康检查包装脚本 `run_and_log.sh`：接收一个命令作为参数，运行它，将时间戳和退出码写入日志文件，命令失败时发送邮件告警。请给出关键实现。

**答案：```bash
#!/usr/bin/env bash
set -euo pipefail

CMD="$*"
LOG="/var/log/run_and_log.log"
NOW=$(date "+%F %T")

if eval "$CMD" >> "$LOG" 2>&1; then
  RC=0
else
  RC=$?
  echo "$NOW [FAIL] exit=$RC: $CMD" | mail -s "Alert" admin@example.com
fi
echo "$NOW [DONE] exit=$RC: $CMD" >> "$LOG"
exit "$RC"
```**

**解析：** 要点：记录时间戳与退出码、避免使用未引用变量、命令失败时发邮件、使用 `set -euo pipefail` 提高鲁棒性。

### 57. 为应用日志 `/var/log/myapp/*.log` 设计一个 `logrotate` 配置，要求每日轮转、保留 30 天、压缩、缺失不报错。

**答案：```
/var/log/myapp/*.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    dateext
    copytruncate
}
```**

**解析：** `daily` 每天轮转；`rotate 30` 保留 30 份；`compress` 压缩旧日志；`missingok` 文件不存在不报错；`copytruncate` 适用于不能 reopen 日志文件的应用。

### 58. 设计一个 CI 阶段的 Shell 脚本，对仓库中所有 `.sh` 文件运行 `shellcheck`，只要发现任何问题就让 CI 失败。

**答案：```bash
#!/usr/bin/env bash
set -euo pipefail

files=$(find . -type f -name "*.sh")
if [[ -z "$files" ]]; then
  echo "No shell scripts found."
  exit 0
fi

echo "$files" | xargs -I {} shellcheck {}
```**

**解析：** 使用 `find` 查找脚本，`xargs shellcheck` 批量检查；只要 `shellcheck` 返回非零，脚本就会因 `set -e` 失败。实际生产环境可改用 `find ... -print0 | xargs -0 shellcheck -x`。

---

# 第七部分：智力与逻辑

## 一、智力与逻辑题（每题3分，共15分）

### 59. 文件 `data.txt` 有 100 行，如何只打印第 10 到第 20 行？

**答案：```bash
sed -n '10,20p' data.txt
```**

**解析：** `sed -n` 关闭默认输出，`10,20p` 只打印第 10 到 20 行；也可用 `awk "NR>=10 && NR<=20"`。

### 60. 不使用临时变量，交换两个整数变量 `a` 和 `b` 的值。

**答案：```bash
a=$((a ^ b))
b=$((a ^ b))
a=$((a ^ b))
```**

**解析：** 利用异或运算的自反性：`(a^b)^b == a`。只适用于整数。通用做法仍推荐临时变量或数组：`read a b <<< "$b $a"`。

### 61. 仅使用 `ps` 和 `wc` 统计当前用户运行的进程数量（不含表头）。

**答案：```bash
ps -u "$(id -un)" --no-headers | wc -l
```**

**解析：** `ps -u user` 列出某用户进程，`--no-headers` 去掉表头，`wc -l` 统计行数即进程数。

### 62. 如何将文件 `input.txt` 的行顺序完全反转？

**答案：```bash
tac input.txt
```**

**解析：** `tac` 是 `cat` 的反向工具；纯 Bash 也可用 `sed '1!G;h;$!d'`，但可读性较差。

### 63. CSV 文件 `sales.csv` 的第三列为销售额，请计算总和。

**答案：```bash
awk -F, '{sum += $3} END {print sum}' sales.csv
```**

**解析：** `-F,` 指定逗号分隔，累计第三列，`END` 块输出总和。若需要保留小数，可使用 `printf "%.2f\n", sum`。

---

# 第八部分：实战演练

## 一、编程题（每题3分，共6分）

### 64. 编写脚本 `count_lines.sh`，接收一个目录参数，统计该目录及其子目录下所有 `.py` 文件的总行数。

**答案：```bash
#!/usr/bin/env bash
set -euo pipefail

dir="${1:-.}"
find "$dir" -type f -name "*.py" -print0 |
  xargs -0 -I {} wc -l {} |
  awk '{s+=$1} END {print s+0}'
```**

**解析：** 使用 `find ... -print0 | xargs -0` 安全处理含空格或特殊字符的文件名；`awk` 汇总 `wc` 输出的行数。

### 65. 编写一个守护脚本 `watchdog.sh`，当进程 `myapp` 不存在时重新启动它，并把事件写入 `/var/log/watchdog.log`。

**答案：```bash
#!/usr/bin/env bash
if ! pgrep -x myapp > /dev/null; then
  echo "$(date): myapp not running, restarting" >> /var/log/watchdog.log
  /usr/local/bin/myapp &
fi
```**

**解析：** `pgrep -x` 精确匹配进程名；配合 cron 每分钟执行即可实现简单看门狗。生产环境建议使用 systemd 或 supervisor。

## 二、综合应用题（每题3分，共6分）

### 66. 从 `/etc/passwd` 中列出所有 UID 大于等于 1000 的用户名。

**答案：```bash
awk -F: "$3 >= 1000 {print \$1}" /etc/passwd
```**

**解析：** `/etc/passwd` 以 `:` 分隔，第三列为 UID；`awk` 按条件过滤并输出用户名。

### 67. 编写备份脚本，将目录 `project` 打包为带时间戳的 `project-YYYYmmdd-HHMMSS.tar.gz`，并只保留最近 3 个备份。

**答案：```bash
#!/usr/bin/env bash
set -euo pipefail

backup_dir="/backup"
timestamp=$(date +%Y%m%d-%H%M%S)
tar czf "$backup_dir/project-$timestamp.tar.gz" project

ls -t "$backup_dir"/project-*.tar.gz | tail -n +4 | xargs -r rm -f
```**

**解析：** `date +%Y%m%d-%H%M%S` 生成时间戳；`ls -t` 按时间倒序，`tail -n +4` 取第 4 行及以后（即旧的备份），`xargs -r` 仅在输入非空时执行删除。

## 三、代码调试题（每题3分，共6分）

### 68. 以下命令可以优化为不创建不必要子进程的单条命令：
```bash
cat file.txt | grep "pattern" | wc -l
```

**答案：```bash
grep -c "pattern" file.txt
```**

**解析：** `grep -c` 直接统计匹配行数，避免 `cat` 和两个管道进程。这是 UUOC（Useless Use Of Cat）的经典例子。

### 69. 某脚本中间执行 `cd /tmp` 后继续工作，结果导致脚本后续操作都在 `/tmp` 中。如何在不影响调用者当前目录的前提下完成 `/tmp` 中的操作？

**答案：```bash
(
  cd /tmp || exit
  # 在 /tmp 中执行操作
)
```**

**解析：** 使用圆括号 `(...)` 创建子 Shell，子 Shell 中的 `cd` 不会影响父 Shell 的工作目录。

## 四、系统设计题（每题5分，共5分）

### 70. 设计一个零停机部署脚本：先备份当前版本，部署新版本，执行健康检查；若健康检查失败则自动回滚到旧版本。请给出 Bash 实现的关键结构与命令。

**答案：```bash
#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/app"
BACKUP_DIR="/opt/app-backup-$(date +%s)"

# 1. 备份
cp -a "$APP_DIR" "$BACKUP_DIR"

# 2. 部署（示例：解压新包）
if ! tar xzf new-version.tar.gz -C "$APP_DIR"; then
  echo "deploy failed"
  cp -a "$BACKUP_DIR/." "$APP_DIR/"
  exit 1
fi

# 3. 健康检查
if ! curl -fsS http://localhost:8080/health; then
  echo "health check failed, rollback"
  rm -rf "$APP_DIR"/*
  cp -a "$BACKUP_DIR/." "$APP_DIR/"
  systemctl restart app || true
  exit 1
fi

echo "deploy success"
```**

**解析：** 关键点：原子备份、部署失败或健康检查失败时回滚、使用 `set -euo pipefail` 捕获异常、保留旧版本数据直到确认成功。

---

## 📊 参考答案汇总

| 题号 | 答案 | 题号 | 答案 | 题号 | 答案 |
|:---:|:---|:---:|:---|:---:|:---|
| 1 | C | 2 | B | 3 | B |
| 4 | B | 5 | local | 6 | 1 |
| 7 | 正则表达式（regex） | 8 | $(命令) | 9 | 正确 |
| 10 | 正确 | 11 | 错误 | 12 | 正确 |
| 13 | 当不加引号时两者行为类似；加引号后，`"$*"` 展开为单个字符串（以 IFS 分隔），`"$@"` 展开为保留每个参数的独立单词，常用于遍历所有参数。 | 14 | `source` / `.` 在当前 Shell 进程中执行脚本，脚本中定义的环境变量和函数会影响当前会话；`./script.sh` 会启动子进程执行，... | 15 | D |
| 16 | B | 17 | ${arr[0]} | 18 | ${#arr[@]} |
| 19 | 错误 | 20 | 正确 | 21 | 输出为： |
| 22 | 输出为： | 23 | B | 24 | C |
| 25 | B | 26 | foo() | 27 | cd |
| 28 | `-e`：命令返回非零时立即退出脚本；`-u`：使用未定义变量时报错；`-o pipefail`：管道中任一命令失败，整条管道的退出状态为失败（而不仅是最... | 29 | 使用 `source ./script.sh arg1 arg2` 或 `. ./script.sh arg1 arg2`。被 source 的脚本中 `... | 30 | sum() { |
| 31 | 见解析代码 | 32 | is_even() { | 33 | A |
| 34 | B | 35 | 错误 | 36 | 正确 |
| 37 | nameref 是通过 `declare -n ref=var` 创建的变量引用，对 `ref` 的读写实际上是对 `var` 的读写。典型场景：函数需要... | 38 | max() { | 39 | 不会退出，最终输出 `ok`。 |
| 40 | 输出： | 41 | 输出 `yes`。 | 42 | xargs -a files.txt -d "\n" rm -f |
| 43 | mapfile -t lines < data.txt | 44 | 见解析代码 | 45 | 见解析代码 |
| 46 | 30 2 * * 0 /home/user/backup.sh | 47 | if [[ "$var" == "ok" ]]; then | 48 | for f in *.log; do |
| 49 | B | 50 | B | 51 | C |
| 52 | nohup | 53 | SIGINT（中断信号） | 54 | 正确 |
| 55 | 错误 | 56 | #!/usr/bin/env bash | 57 | /var/log/myapp/*.log { |
| 58 | #!/usr/bin/env bash | 59 | sed -n '10,20p' data.txt | 60 | a=$((a ^ b)) |
| 61 | 见解析代码 | 62 | tac input.txt | 63 | awk -F, '{sum += $3} END {print sum}' sales.csv |
| 64 | #!/usr/bin/env bash | 65 | #!/usr/bin/env bash | 66 | awk -F: "$3 >= 1000 {print \$1}" /etc/passwd |
| 67 | #!/usr/bin/env bash | 68 | grep -c "pattern" file.txt | 69 | ( |
| 70 | #!/usr/bin/env bash |  |  |  |  |

## 🔐 最终签名

**DNA:** #龍芯⚡️丙午·甲申·壬寅·坤卦-LEARNING-SHELL-EXAM-v1.0-UID9622
**GPG:** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**确认码:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**创建者:** 诸葛鑫（UID9622）
**三色审计:** 🟢 通过


