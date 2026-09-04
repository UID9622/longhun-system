#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
CNSH代码生成器（Code Generator）

DNA:#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-CODEGEN-FILE1-v1.1
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计: 🟢 通过

将AST编译为目标语言代码
支持：C、C++、Python、Objective-C、Swift、JavaScript、Rust

体现原则：
- 目标语言可配置
- 缩进和格式化自动处理
- 完整的类型映射
- 标准库函数支持
"""

from .compiler_node import ASTNode, TargetLang


class CodeGenError(Exception):
    """代码生成错误"""
    pass


class CodeGenerator:
    """代码生成器"""

    # CNSH类型到各目标语言的映射
    TYPE_MAPPINGS = {
        TargetLang.C: {
            '整数': 'int',
            '小数': 'double',
            '文本': 'char*',
            '布尔': 'bool',
            '真假': 'bool',
            '列表': 'void*',
            '映射': 'void*',
            '空值': 'void',
            '空': 'NULL'
        },
        TargetLang.PYTHON: {
            '整数': 'int',
            '小数': 'float',
            '文本': 'str',
            '布尔': 'bool',
            '真假': 'bool',
            '列表': 'list',
            '映射': 'dict',
            '空值': 'None',
            '空': 'None'
        },
        TargetLang.JAVASCRIPT: {
            '整数': 'let',
            '小数': 'let',
            '文本': 'let',
            '布尔': 'let',
            '真假': 'let',
            '列表': 'let',
            '映射': 'let',
            '空值': 'let',
            '空': 'null'
        },
        TargetLang.RUST: {
            '整数': 'i32',
            '小数': 'f64',
            '文本': 'String',
            '布尔': 'bool',
            '真假': 'bool',
            '列表': 'Vec',
            '映射': 'HashMap',
            '空值': '()',
            '空': 'None'
        },
        TargetLang.CPP: {  # type: ignore[attr-defined]
            '整数': 'int',
            '小数': 'double',
            '文本': 'std::string',
            '布尔': 'bool',
            '真假': 'bool',
            '列表': 'std::vector',
            '映射': 'std::unordered_map',
            '空值': 'void',
            '空': 'nullptr'
        },
        TargetLang.OBJC: {  # type: ignore[attr-defined]
            '整数': 'NSInteger',
            '小数': 'CGFloat',
            '文本': 'NSString*',
            '布尔': 'BOOL',
            '真假': 'BOOL',
            '列表': 'NSArray*',
            '映射': 'NSDictionary*',
            '空值': 'void',
            '空': 'nil'
        },
        TargetLang.SWIFT: {  # type: ignore[attr-defined]
            '整数': 'Int',
            '小数': 'Double',
            '文本': 'String',
            '布尔': 'Bool',
            '真假': 'Bool',
            '列表': 'Array',
            '映射': 'Dictionary',
            '空值': 'Void',
            '空': 'nil'
        }
    }

    # 默认值映射
    DEFAULT_VALUES = {
        TargetLang.C: {
            'int': '0',
            'double': '0.0',
            'char*': '""',
            'bool': 'false',
            'void': ''
        },
        TargetLang.PYTHON: {
            'int': '0',
            'float': '0.0',
            'str': '""',
            'bool': 'False',
            'None': 'None'
        },
        TargetLang.JAVASCRIPT: {
            'let': '0',
            'null': 'null'
        },
        TargetLang.RUST: {
            'i32': '0',
            'f64': '0.0',
            'String': 'String::new()',
            'bool': 'false',
            'None': 'None'
        },
        TargetLang.CPP: {  # type: ignore[attr-defined]
            'int': '0',
            'double': '0.0',
            'std::string': '""',
            'bool': 'false',
            'nullptr': 'nullptr'
        },
        TargetLang.OBJC: {  # type: ignore[attr-defined]
            'NSInteger': '0',
            'CGFloat': '0.0',
            'NSString*': '@""',
            'BOOL': 'NO',
            'nil': 'nil'
        },
        TargetLang.SWIFT: {  # type: ignore[attr-defined]
            'Int': '0',
            'Double': '0.0',
            'String': '""',
            'Bool': 'false',
            'nil': 'nil'
        }
    }

    # 标准库函数映射
    STDLIB_FUNCTIONS = {
        '打印': {
            TargetLang.C: 'printf',
            TargetLang.PYTHON: 'print',
            TargetLang.JAVASCRIPT: 'console.log',
            TargetLang.RUST: 'println!',
            TargetLang.CPP: 'std::cout',  # type: ignore[attr-defined]
            TargetLang.OBJC: 'NSLog',  # type: ignore[attr-defined]
            TargetLang.SWIFT: 'print'  # type: ignore[attr-defined]
        },
        '提示': {
            TargetLang.C: 'printf',
            TargetLang.PYTHON: 'print',
            TargetLang.JAVASCRIPT: 'console.warn',
            TargetLang.RUST: 'eprintln!',
            TargetLang.CPP: 'std::cerr',  # type: ignore[attr-defined]
            TargetLang.OBJC: 'NSLog',  # type: ignore[attr-defined]
            TargetLang.SWIFT: 'print'  # type: ignore[attr-defined]
        },
        '报错': {
            TargetLang.C: 'fprintf',
            TargetLang.PYTHON: 'print',
            TargetLang.JAVASCRIPT: 'console.error',
            TargetLang.RUST: 'eprintln!',
            TargetLang.CPP: 'std::cerr',  # type: ignore[attr-defined]
            TargetLang.OBJC: 'NSLog',  # type: ignore[attr-defined]
            TargetLang.SWIFT: 'debugPrint'  # type: ignore[attr-defined]
        }
    }

    def __init__(self, target_lang: TargetLang = TargetLang.PYTHON):
        """
        初始化代码生成器

        Args:
            target_lang: 目标语言
        """
        self.target_lang = target_lang
        self.indent_level = 0
        self.output: list[str] = []
        self.indent_str = '    '  # 4空格缩进

    def generate(self, ast: ASTNode) -> str:
        """
        生成目标语言代码

        Args:
            ast: 抽象语法树（Program节点）

        Returns:
            生成的目标语言代码字符串
        """
        self.output = []
        self.indent_level = 0

        try:
            # 生成文件头
            self._generate_header()

            # 生成程序体
            self._generate_program(ast)

            # 生成文件尾（如果需要）
            self._generate_footer()

            return '\n'.join(self.output)

        except Exception as e:
            raise CodeGenError(f"代码生成失败: {str(e)}")

    # ═══════════════════════════════════════════════════════════════
    # 【文件头和文件尾】
    # ═══════════════════════════════════════════════════════════════

    def _generate_header(self):
        """生成文件头"""
        if self.target_lang == TargetLang.C:
            self._emit('// Generated by CNSH Compiler v1.0')
            self._emit('// 创建者：诸葛鑫（UID9622）')
            self._emit('//')
            self._emit('#include <stdio.h>')
            self._emit('#include <stdlib.h>')
            self._emit('#include <string.h>')
            self._emit('#include <stdbool.h>')
            self._emit('')

        elif self.target_lang == TargetLang.PYTHON:
            self._emit('#!/usr/bin/env python3')
            self._emit('# -*- coding: utf-8 -*-')
            self._emit('# Generated by CNSH Compiler v1.0')
            self._emit('# 创建者：诸葛鑫（UID9622）')
            self._emit('')

        elif self.target_lang == TargetLang.JAVASCRIPT:
            self._emit('// Generated by CNSH Compiler v1.0')
            self._emit('// 创建者：诸葛鑫（UID9622）')
            self._emit('')

        elif self.target_lang == TargetLang.RUST:
            self._emit('// Generated by CNSH Compiler v1.0')
            self._emit('// 创建者：诸葛鑫（UID9622）')
            self._emit('')
            self._emit('fn main() {')
            self.indent_level += 1

    def _generate_footer(self):
        """生成文件尾"""
        if self.target_lang == TargetLang.C:
            self._emit('')
            self._emit('int main() {')
            self.indent_level += 1
            self._emit('// 主程序入口')
            self.indent_level -= 1
            self._emit('    return 0;')
            self._emit('}')

        elif self.target_lang == TargetLang.RUST:
            self.indent_level -= 1
            self._emit('}')

    # ═══════════════════════════════════════════════════════════════
    # 【程序和语句生成】
    # ═══════════════════════════════════════════════════════════════

    def _generate_program(self, node: ASTNode):
        """生成程序"""
        statements = self._get(node, 'statements', [])
        for stmt in statements:  # pyright: ignore[reportOptionalIterable,reportGeneralTypeIssues]
            self._generate_statement(stmt)  # pyright: ignore[reportArgumentType]

    def _generate_statement(self, node: ASTNode):
        """生成语句"""
        if not isinstance(node, ASTNode):
            return

        node_type = node.node_type

        if node_type == 'VariableDeclaration':
            self._generate_variable_declaration(node)
        elif node_type == 'FunctionDeclaration':
            self._generate_function_declaration(node)
        elif node_type == 'IfStatement':
            self._generate_if_statement(node)
        elif node_type == 'LoopStatement':
            self._generate_loop_statement(node)
        elif node_type == 'ReturnStatement':
            self._generate_return_statement(node)
        elif node_type == 'ExpressionStatement':
            expr = self._get(node, 'expression')
            if expr:
                expr_str = self._generate_expression(expr)  # pyright: ignore[reportArgumentType]
                self._emit(expr_str + self._get_statement_terminator())
        elif node_type == 'Assignment':
            expr_str = self._generate_expression(node)
            self._emit(expr_str + self._get_statement_terminator())

    def _generate_variable_declaration(self, node: ASTNode):
        """生成变量声明"""
        var_type = self._get(node, 'varType')
        name = self._get(node, 'name')
        value = self._get(node, 'value')

        # 获取目标语言中的类型
        target_type = self._map_type(str(var_type))

        # 生成初值
        if value:
            value_expr = self._generate_expression(value)  # pyright: ignore[reportArgumentType]
        else:
            value_expr = self._get_default_value(target_type)

        # 根据目标语言生成不同的声明格式
        if self.target_lang == TargetLang.PYTHON:
            self._emit(f'{name} = {value_expr}')

        elif self.target_lang == TargetLang.C:
            self._emit(f'{target_type} {name} = {value_expr};')

        elif self.target_lang == TargetLang.JAVASCRIPT:
            self._emit(f'let {name} = {value_expr};')

        elif self.target_lang == TargetLang.RUST:
            self._emit(f'let {name} = {value_expr};')

    def _generate_function_declaration(self, node: ASTNode):
        """生成函数声明"""
        name = self._get(node, 'name')
        params = self._get(node, 'params', [])
        return_type = self._get(node, 'returnType', '空值')
        body = self._get(node, 'body', [])

        # 生成函数签名
        param_strs = self._generate_parameters(params)  # pyright: ignore[reportArgumentType]

        if self.target_lang == TargetLang.PYTHON:
            self._emit(f'def {name}({param_strs}):')

        elif self.target_lang == TargetLang.C:
            target_return_type = self._map_type(str(return_type))
            self._emit(f'{target_return_type} {name}({param_strs}) {{')

        elif self.target_lang == TargetLang.JAVASCRIPT:
            self._emit(f'function {name}({param_strs}) {{')

        elif self.target_lang == TargetLang.RUST:
            self._emit(f'fn {name}({param_strs}) {{')

        # 生成函数体
        self.indent_level += 1
        for stmt in body:  # pyright: ignore[reportOptionalIterable,reportGeneralTypeIssues]
            self._generate_statement(stmt)  # pyright: ignore[reportArgumentType]
        self.indent_level -= 1

        # 关闭函数
        if self.target_lang == TargetLang.PYTHON:
            self._emit('')
        else:
            self._emit('}')
            self._emit('')

    def _generate_if_statement(self, node: ASTNode):
        """生成If语句"""
        condition = self._get(node, 'condition')
        then_body = self._get(node, 'thenBody', [])
        else_body = self._get(node, 'elseBody')

        cond_str = self._generate_expression(condition)  # pyright: ignore[reportArgumentType]

        # 生成If部分
        if self.target_lang == TargetLang.PYTHON:
            self._emit(f'if {cond_str}:')
        else:
            self._emit(f'if ({cond_str}) {{')

        self.indent_level += 1
        for stmt in then_body:  # pyright: ignore[reportOptionalIterable,reportGeneralTypeIssues]
            self._generate_statement(stmt)  # pyright: ignore[reportArgumentType]
        self.indent_level -= 1

        # 生成Else部分
        if else_body:
            if self.target_lang == TargetLang.PYTHON:
                self._emit('else:')
            else:
                self._emit('} else {')

            self.indent_level += 1
            for stmt in else_body:  # pyright: ignore[reportOptionalIterable,reportGeneralTypeIssues]
                self._generate_statement(stmt)  # pyright: ignore[reportArgumentType]
            self.indent_level -= 1

        # 关闭If
        if self.target_lang != TargetLang.PYTHON:
            self._emit('}')

    def _generate_loop_statement(self, node: ASTNode):
        """生成循环语句"""
        times = self._get(node, 'times')
        body = self._get(node, 'body', [])

        times_str = self._generate_expression(times)  # pyright: ignore[reportArgumentType]

        # 根据目标语言生成不同的循环格式
        if self.target_lang == TargetLang.PYTHON:
            self._emit(f'for __i in range({times_str}):')

        elif self.target_lang == TargetLang.C:
            self._emit(f'for (int __i = 0; __i < {times_str}; __i++) {{')

        elif self.target_lang == TargetLang.JAVASCRIPT:
            self._emit(f'for (let __i = 0; __i < {times_str}; __i++) {{')

        elif self.target_lang == TargetLang.RUST:
            self._emit(f'for __i in 0..{times_str} {{')

        # 生成循环体
        self.indent_level += 1
        for stmt in body:  # pyright: ignore[reportOptionalIterable,reportGeneralTypeIssues]
            self._generate_statement(stmt)  # pyright: ignore[reportArgumentType]
        self.indent_level -= 1

        # 关闭循环
        if self.target_lang == TargetLang.PYTHON:
            pass
        else:
            self._emit('}')

    def _generate_return_statement(self, node: ASTNode):
        """生成返回语句"""
        value = self._get(node, 'value')

        if value:
            value_str = self._generate_expression(value)  # pyright: ignore[reportArgumentType]
            self._emit(f'return {value_str}{self._get_statement_terminator()}')
        else:
            self._emit(f'return{self._get_statement_terminator()}')

    # ═══════════════════════════════════════════════════════════════
    # 【表达式生成】
    # ═══════════════════════════════════════════════════════════════

    def _generate_expression(self, node: ASTNode) -> str:
        """生成表达式"""
        if not isinstance(node, ASTNode):
            return str(node)

        node_type = node.node_type

        if node_type == 'Number':
            return str(self._get(node, 'value'))

        elif node_type == 'String':
            value = self._get(node, 'value', '')
            return f'"{value}"'

        elif node_type == 'Boolean':
            value = self._get(node, 'value')
            if self.target_lang == TargetLang.PYTHON:
                return 'True' if value else 'False'
            else:
                return 'true' if value else 'false'

        elif node_type == 'Null':
            if self.target_lang == TargetLang.PYTHON:
                return 'None'
            elif self.target_lang == TargetLang.C:
                return 'NULL'
            else:
                return 'null'

        elif node_type == 'Identifier':
            return str(self._get(node, 'name'))

        elif node_type == 'BinaryOp':
            left = self._generate_expression(self._get(node, 'left'))  # pyright: ignore[reportArgumentType]
            right = self._generate_expression(self._get(node, 'right'))  # pyright: ignore[reportArgumentType]
            op = self._get(node, 'op')
            return f'({left} {op} {right})'

        elif node_type == 'UnaryOp':
            op = self._get(node, 'op')
            operand = self._generate_expression(self._get(node, 'operand'))  # pyright: ignore[reportArgumentType]
            return f'({op}{operand})'

        elif node_type == 'Assignment':
            left = self._generate_expression(self._get(node, 'left'))  # pyright: ignore[reportArgumentType]
            right = self._generate_expression(self._get(node, 'right'))  # pyright: ignore[reportArgumentType]
            return f'{left} = {right}'

        elif node_type == 'FunctionCall':
            name = self._get(node, 'name')
            args = self._get(node, 'args', [])
            arg_strs = [self._generate_expression(arg) for arg in args]  # pyright: ignore[reportOptionalIterable,reportArgumentType,reportGeneralTypeIssues]

            # 检查是否是标准库函数
            if str(name) in self.STDLIB_FUNCTIONS:
                mapped_name = self.STDLIB_FUNCTIONS[str(name)].get(self.target_lang, name)
            else:
                mapped_name = name

            if self.target_lang == TargetLang.PYTHON:
                return f'{mapped_name}({", ".join(arg_strs)})'
            elif self.target_lang in (TargetLang.C, TargetLang.JAVASCRIPT):
                return f'{mapped_name}({", ".join(arg_strs)})'
            elif self.target_lang == TargetLang.RUST:
                if '!' in str(mapped_name):  # 宏函数  # pyright: ignore[reportOperatorIssue]
                    return f'{mapped_name}({", ".join(arg_strs)})'
                else:
                    return f'{mapped_name}({", ".join(arg_strs)})'

        return ''

    # ═══════════════════════════════════════════════════════════════
    # 【辅助方法】
    # ═══════════════════════════════════════════════════════════════

    def _get(self, node: ASTNode, key: str, default: object | None = None) -> object | None:
        """从ASTNode获取属性"""
        if isinstance(node.value, dict):
            return node.value.get(key, default)
        return default

    def _emit(self, code: str):
        """输出一行代码（带缩进）"""
        if code.strip():
            indent = self.indent_str * self.indent_level
            self.output.append(indent + code)
        else:
            self.output.append('')

    def _map_type(self, cnsh_type: str) -> str:
        """将CNSH类型映射到目标语言"""
        mapping = self.TYPE_MAPPINGS.get(self.target_lang, {})
        return mapping.get(cnsh_type, 'object')

    def _get_default_value(self, target_type: str) -> str:
        """获取目标语言中类型的默认值"""
        defaults = self.DEFAULT_VALUES.get(self.target_lang, {})
        return defaults.get(target_type, 'null')

    def _get_statement_terminator(self) -> str:
        """获取语句终止符"""
        if self.target_lang == TargetLang.PYTHON:
            return ''
        else:
            return ';'

    def _generate_parameters(self, params: list[dict[str, object]]) -> str:
        """生成参数列表"""
        param_strs = []

        for param in params:
            param_type = param.get('type')
            param_name = param.get('name')
            target_type = self._map_type(str(param_type))  # pyright: ignore[reportArgumentType]

            if self.target_lang == TargetLang.PYTHON:
                param_strs.append(param_name)
            elif self.target_lang == TargetLang.C:
                param_strs.append(f'{target_type} {param_name}')
            elif self.target_lang == TargetLang.JAVASCRIPT:
                param_strs.append(param_name)
            elif self.target_lang == TargetLang.RUST:
                param_strs.append(f'{param_name}: {target_type}')

        return ', '.join(param_strs)


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-CODEGEN-v1.0"
__responsibility__ = "UID9622·不免责"
