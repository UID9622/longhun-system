# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
CNSH v2.1 语法分析器 (Parser)
DNA: #龍芯⚡️2026-06-29-CNSH-PARSER-v2.1
"""
from typing import List, Optional

from .tokens import Token
from .ast_nodes import (
    Program, ModuleDecl, FunctionDecl, Parameter, VarDecl, StructDecl,
    UseStmt, IfStmt, ElifBranch, WhileStmt, ForStmt, ReturnStmt,
    BreakStmt, ContinueStmt, ExpressionStmt, BinaryExpr, UnaryExpr,
    LiteralExpr, IdentifierExpr, CallExpr, MemberExpr, IndexExpr,
    ListExpr, MapExpr, MapPair, ASTNode,
    # 新增节点
    Decorator, ClassDecl, MethodDecl, YieldStmt, YieldFromStmt,
    ExceptClause, TryStmt, RaiseStmt, PassStmt, WithItem, WithStmt,
    AsyncWithStmt, AsyncForStmt, AwaitExpr, GeneratorExpr,
    EnumMember, EnumDecl, DataClassField, DataClassDecl, ImportStmt,
    # Bra-Ket 节点
    PersonaBasisDecl, SystemDecl,
    # CNSH v2.0-v2.3 新增节点
    SwitchStmt, CaseClause, DNARegisterStmt, DNAVerifyStmt, DNASignStmt,
    AbortStmt, CreateRollbackStmt, RollbackStmt, VerifyRollbackStmt,
    HookStmt, TriColorAuditStmt, TestStmt, AssertStmt, ExpectStmt,
    RouteToStmt, QuantumEntangleStmt, CollapseStmt,
    ColdStartStmt, HotStartStmt, ExitProgramStmt, ExportStmt, AuditStmt,
)
from .errors import CNSHParseError


class Parser:
    """递归下降语法分析器"""

    # 可作为类型注解的 token 类型（含中文类型名关键字）
    _TYPE_ANNOTATION_TOKENS = {
        "STRING_TYPE", "INTEGER_TYPE", "FLOAT_TYPE", "BOOLEAN_TYPE",
        "LIST_TYPE", "ARRAY_TYPE", "MAP_TYPE", "VECTOR_TYPE", "BINARY_TYPE",
        "CLASS", "OBJECT", "INSTANCE", "IDENTIFIER",
    }

    def __init__(self, tokens: List[Token]):
        # 预先过滤注释，但保留 DNA 注释可能不需要解析
        self.tokens = [t for t in tokens if t.type not in ("COMMENT", "DNA_COMMENT")]
        self.pos = 0

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def _advance(self) -> Token:
        tok = self._peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def _match(self, *types: str) -> bool:
        return self._peek().type in types

    def _check(self, type_: str) -> bool:
        return self._peek().type == type_

    def _expect(self, type_: str, message: Optional[str] = None) -> Token:
        if not self._check(type_):
            tok = self._peek()
            msg = message or f"期望 {type_}，但得到 {tok.type}({tok.value!r})"
            raise CNSHParseError(msg, tok.line, tok.column, tok.file)
        return self._advance()

    def _skip_newlines(self):
        while self._check("NEWLINE"):
            self._advance()

    def _statement_end(self):
        """语句结束：允许分号或换行"""
        if self._check("SEMICOLON"):
            self._advance()
        elif self._check("NEWLINE"):
            self._advance()
        elif self._check("RBRACE") or self._check("EOF"):
            return
        else:
            tok = self._peek()
            raise CNSHParseError(
                f"期望语句结束符（; 或换行），但得到 {tok.type}",
                tok.line, tok.column, tok.file,
            )

    def parse(self) -> Program:
        statements: List[ASTNode] = []
        while not self._check("EOF"):
            self._skip_newlines()
            if self._check("EOF"):
                break
            statements.append(self._statement())
        return Program(statements=statements)

    def _statement(self) -> ASTNode:
        self._skip_newlines()
        tok = self._peek()
        # 装饰器可修饰类/方法/函数（支持 @ 与无 @ 中文装饰器）
        decorator_starts = {
            "AT", "UNIQUE", "DATACLASS", "PROPERTY",
            "CLASSMETHOD", "STATICMETHOD", "ABSTRACTMETHOD",
        }
        if tok.type in decorator_starts:
            decorators = self._decorators()
            return self._decorated_decl(decorators)
        if tok.type == "MODULE":
            return self._module_decl()
        if tok.type == "PERSONA_BASIS":
            return self._persona_basis_decl()
        if tok.type == "SYSTEM":
            return self._system_decl()
        if tok.type in ("FUNCTION", "DEF"):
            return self._function_decl()
        if tok.type == "CLASS":
            return self._class_decl()
        if tok.type == "STRUCT":
            return self._struct_decl()
        if tok.type == "VAR":
            return self._var_decl(is_const=False)
        if tok.type == "CONST":
            return self._var_decl(is_const=True)
        if tok.type == "IMPORT" or tok.type == "FROM":
            return self._import_stmt()
        if tok.type == "IF":
            return self._if_stmt()
        if tok.type == "WHILE":
            return self._while_stmt()
        if tok.type == "FOR":
            return self._for_stmt()
        if tok.type == "ASYNC":
            return self._async_stmt()
        if tok.type == "WITH":
            return self._with_stmt()
        if tok.type == "TRY":
            return self._try_stmt()
        if tok.type == "RETURN":
            return self._return_stmt()
        if tok.type == "YIELD" or tok.type == "YIELD_FROM":
            return self._yield_stmt()
        if tok.type == "RAISE":
            return self._raise_stmt()
        if tok.type == "PASS":
            return self._pass_stmt()
        if tok.type == "BREAK":
            return self._break_stmt()
        if tok.type == "CONTINUE":
            return self._continue_stmt()
        # ── CNSH v2.0-v2.3 新增语句 ──
        if tok.type == "SWITCH":
            return self._switch_stmt()
        if tok.type == "HOOK":
            return self._hook_stmt(hook_type="")
        if tok.type == "BEFORE_HOOK":
            return self._hook_stmt(hook_type="before")
        if tok.type == "AFTER_HOOK":
            return self._hook_stmt(hook_type="after")
        if tok.type == "TRI_COLOR_AUDIT":
            return self._tri_color_audit_stmt()
        if tok.type == "DNA_REGISTER":
            return self._dna_register_stmt()
        if tok.type == "DNA_VERIFY":
            return self._dna_verify_stmt()
        if tok.type == "DNA_SIGN":
            return self._dna_sign_stmt()
        if tok.type == "ABORT":
            return self._abort_stmt()
        if tok.type == "CREATE_ROLLBACK":
            return self._create_rollback_stmt()
        if tok.type == "ROLLBACK":
            return self._rollback_stmt()
        if tok.type == "VERIFY_ROLLBACK":
            return self._verify_rollback_stmt()
        if tok.type == "TEST":
            return self._test_stmt()
        if tok.type == "ASSERT":
            return self._assert_stmt()
        if tok.type == "EXPECT":
            return self._expect_stmt()
        if tok.type == "ROUTE_TO":
            return self._route_to_stmt()
        if tok.type == "QUANTUM_ENTANGLE":
            return self._quantum_entangle_stmt()
        if tok.type == "COLLAPSE":
            return self._collapse_stmt()
        if tok.type == "COLD_START":
            return self._cold_start_stmt()
        if tok.type == "HOT_START":
            return self._hot_start_stmt()
        if tok.type == "EXIT_PROGRAM":
            return self._exit_program_stmt()
        if tok.type == "EXPORT":
            return self._export_stmt()
        if tok.type in ("AUDITING", "AUDITED"):
            return self._audit_stmt()
        if tok.type == "GLOBAL":
            return self._global_decl()
        return self._expression_stmt()

    def _module_decl(self) -> ModuleDecl:
        start = self._advance()  # MODULE
        name = self._expect_identifier_like("模块声明需要名称")
        weight = self._optional_weight()
        self._expect("LBRACE", "模块体需要 '{'")
        body = self._block_body()
        return ModuleDecl(name=name, weight=weight, body=body, line=start.line, column=start.column)

    def _persona_basis_decl(self) -> PersonaBasisDecl:
        start = self._advance()  # PERSONA_BASIS
        name = self._expect_identifier_like("人格基态需要名称")
        self._expect("LBRACE", "人格基态体需要 '{'")
        fields = self._key_value_body()
        return PersonaBasisDecl(name=name, fields=fields, line=start.line, column=start.column)

    def _system_decl(self) -> SystemDecl:
        start = self._advance()  # SYSTEM
        name = self._expect_identifier_like("系统需要名称")
        self._expect("LBRACE", "系统体需要 '{'")
        fields = self._key_value_body()
        return SystemDecl(name=name, fields=fields, line=start.line, column=start.column)

    def _key_value_body(self) -> List[MapPair]:
        """解析 { 键: 值, ... } 形式的人格基态/系统体。"""
        pairs: List[MapPair] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            key_tok = self._expect("IDENTIFIER", "键需要名称")
            self._expect("COLON", "键值对需要 ':'")
            value = self._expression()
            pairs.append(MapPair(key=IdentifierExpr(name=key_tok.value), value=value))
            if self._check("COMMA"):
                self._advance()
            self._skip_newlines()
        self._expect("RBRACE", "体需要 '}'")
        return pairs

    def _function_decl(self, decorators: Optional[List[Decorator]] = None) -> ASTNode:
        start = self._advance()  # FUNCTION or DEF
        name = self._expect_identifier_like("函数声明需要名称")
        self._expect("LPAREN", "函数参数需要 '('")
        params = self._parameter_list()
        self._expect("RPAREN", "函数参数需要 ')'")
        return_type_ann: Optional[str] = None
        if self._check("ARROW"):
            self._advance()
            return_type_ann = self._parse_type_annotation("函数返回类型")
        weight = self._optional_weight()
        self._expect("LBRACE", "函数体需要 '{'")
        body = self._block_body()
        if decorators:
            return MethodDecl(
                name=name,
                params=params,
                return_type_annotation=return_type_ann,
                decorators=decorators,
                body=body,
                is_async=False,
                line=start.line,
                column=start.column,
            )
        return FunctionDecl(
            name=name,
            params=params,
            return_type_annotation=return_type_ann,
            weight=weight,
            body=body,
            line=start.line,
            column=start.column,
        )

    def _struct_decl(self) -> StructDecl:
        start = self._advance()  # STRUCT
        name = self._expect_identifier_like("结构体需要名称")
        self._expect("LBRACE", "结构体体需要 '{'")
        fields: List[Parameter] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            field_name = self._expect("IDENTIFIER", "结构体字段需要名称").value
            type_ann: Optional[str] = None
            if self._check("COLON"):
                self._advance()
                type_ann = self._parse_type_annotation("结构体字段类型")
            fields.append(Parameter(name=field_name, type_annotation=type_ann))
            if self._check("COMMA"):
                self._advance()
            self._skip_newlines()
        self._expect("RBRACE", "结构体体需要 '}'")
        return StructDecl(name=name, fields=fields, line=start.line, column=start.column)

    def _var_decl(self, is_const: bool) -> VarDecl:
        start = self._advance()  # VAR or CONST
        name = self._expect_identifier_like("变量声明需要名称")
        type_ann: Optional[str] = None
        if self._check("COLON"):
            self._advance()
            type_ann = self._parse_type_annotation("变量类型")
        init: Optional[ASTNode] = None
        if self._check("ASSIGN"):
            self._advance()
            init = self._expression()
        self._statement_end()
        return VarDecl(name=name, initializer=init, is_const=is_const, type_annotation=type_ann, line=start.line, column=start.column)

    def _use_stmt(self) -> UseStmt:
        start = self._advance()  # USE
        path: List[str] = [self._expect("IDENTIFIER", "使用语句需要模块名").value]
        while self._check("DOT"):
            self._advance()
            path.append(self._expect("IDENTIFIER", "模块路径需要名称").value)
        self._statement_end()
        return UseStmt(module_path=path, line=start.line, column=start.column)

    def _if_stmt(self) -> IfStmt:
        start = self._advance()  # IF
        condition = self._expression()
        self._expect("LBRACE", "如果分支需要 '{'")
        then_body = self._block_body()
        elif_branches: List[ElifBranch] = []
        while self._check("ELIF"):
            self._advance()
            elif_cond = self._expression()
            self._expect("LBRACE", "否则如果分支需要 '{'")
            elif_body = self._block_body()
            elif_branches.append(ElifBranch(condition=elif_cond, body=elif_body))
        else_body: List[ASTNode] = []
        if self._check("ELSE"):
            self._advance()
            self._expect("LBRACE", "否则分支需要 '{'")
            else_body = self._block_body()
        return IfStmt(condition=condition, then_body=then_body, elif_branches=elif_branches, else_body=else_body, line=start.line, column=start.column)

    def _while_stmt(self) -> WhileStmt:
        start = self._advance()  # WHILE
        condition = self._expression()
        self._expect("LBRACE", "当循环需要 '{'")
        body = self._block_body()
        return WhileStmt(condition=condition, body=body, line=start.line, column=start.column)

    def _for_stmt(self) -> ForStmt:
        start = self._advance()  # FOR
        # 语法：对于 变量 在 表达式 { ... }
        var_name = self._expect_identifier_like("对于循环需要循环变量")
        if self._peek().value not in ("在", "in"):
            tok = self._peek()
            raise CNSHParseError("对于循环需要 '在' 或 'in'", tok.line, tok.column, tok.file)
        self._advance()
        iterable = self._expression()
        self._expect("LBRACE", "对于循环需要 '{'")
        body = self._block_body()
        return ForStmt(var_name=var_name, iterable=iterable, body=body, line=start.line, column=start.column)

    def _return_stmt(self) -> ReturnStmt:
        start = self._advance()  # RETURN
        value: Optional[ASTNode] = None
        if not (self._check("SEMICOLON") or self._check("NEWLINE") or self._check("RBRACE") or self._check("EOF")):
            value = self._expression()
        self._statement_end()
        return ReturnStmt(value=value, line=start.line, column=start.column)

    def _break_stmt(self) -> BreakStmt:
        start = self._advance()
        self._statement_end()
        return BreakStmt(line=start.line, column=start.column)

    def _continue_stmt(self) -> ContinueStmt:
        start = self._advance()
        self._statement_end()
        return ContinueStmt(line=start.line, column=start.column)

    def _expression_stmt(self) -> ExpressionStmt:
        expr = self._expression()
        self._statement_end()
        return ExpressionStmt(expression=expr, line=expr.line, column=expr.column)

    def _block_body(self) -> List[ASTNode]:
        body: List[ASTNode] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            body.append(self._statement())
        self._expect("RBRACE", "代码块需要 '}'")
        return body

    def _parameter_list(self) -> List[Parameter]:
        params: List[Parameter] = []
        self._skip_newlines()
        if self._check("RPAREN"):
            return params
        while True:
            self._skip_newlines()
            name = self._expect_identifier_like("参数需要名称")
            type_ann: Optional[str] = None
            if self._check("COLON"):
                self._advance()
                type_ann = self._parse_type_annotation("参数类型")
            params.append(Parameter(name=name, type_annotation=type_ann))
            self._skip_newlines()
            if self._check("COMMA"):
                self._advance()
            else:
                break
        self._skip_newlines()
        return params

    def _optional_weight(self) -> Optional[int]:
        if self._check("WEIGHT"):
            self._advance()
            if self._check("NUMBER"):
                return int(self._advance().value)
            raise CNSHParseError("权重符号后需要数字", self._peek().line, self._peek().column)
        return None

    def _parse_type_annotation(self, message: str = "需要类型") -> str:
        """解析类型注解，支持中文类型关键字与普通标识符。"""
        tok = self._peek()
        if tok.type in self._TYPE_ANNOTATION_TOKENS:
            return self._advance().value
        raise CNSHParseError(
            f"{message}，但得到 {tok.type}({tok.value!r})",
            tok.line, tok.column, tok.file,
        )

    def _expect_identifier_like(self, message: str) -> str:
        """解析类标识符的名称（允许关键字作为自定义名称，如 类、全局 等）。"""
        tok = self._peek()
        if tok.type == "IDENTIFIER" or tok.value.isidentifier():
            return self._advance().value
        raise CNSHParseError(f"{message}，但得到 {tok.type}({tok.value!r})", tok.line, tok.column, tok.file)

    # ---------- 类 / 装饰器 / 异步 / 上下文管理器 / 异常 / 导入 ----------

    def _method_decl(self, decorators: Optional[List[Decorator]] = None) -> MethodDecl:
        start = self._advance()  # FUNCTION or DEF
        name = self._expect_identifier_like("方法需要名称")
        self._expect("LPAREN", "方法参数需要 '('")
        params = self._parameter_list()
        self._expect("RPAREN", "方法参数需要 ')'")
        return_type_ann: Optional[str] = None
        if self._check("ARROW"):
            self._advance()
            return_type_ann = self._parse_type_annotation("方法返回类型")
        self._expect("LBRACE", "方法体需要 '{'")
        body = self._block_body()
        return MethodDecl(
            name=name,
            params=params,
            return_type_annotation=return_type_ann,
            decorators=decorators or [],
            body=body,
            is_async=False,
            line=start.line,
            column=start.column,
        )

    def _decorators(self) -> List[Decorator]:
        decorators: List[Decorator] = []
        decorator_starts = {
            "AT", "UNIQUE", "DATACLASS", "PROPERTY",
            "CLASSMETHOD", "STATICMETHOD", "ABSTRACTMETHOD",
        }
        while self._peek().type in decorator_starts:
            decorators.append(self._decorator())
        return decorators

    def _decorator(self) -> Decorator:
        start = self._peek()
        if self._check("AT"):
            self._advance()
        name: str
        if self._check("IDENTIFIER"):
            name = self._advance().value
            while self._check("DOT"):
                self._advance()
                name = f"{name}.{self._expect('IDENTIFIER', '装饰器路径需要名称').value}"
        elif self._check("DATACLASS"):
            name = self._advance().value
        elif self._check("UNIQUE"):
            name = self._advance().value
        elif self._check("PROPERTY"):
            name = self._advance().value
        elif self._check("CLASSMETHOD"):
            name = self._advance().value
        elif self._check("STATICMETHOD"):
            name = self._advance().value
        elif self._check("ABSTRACTMETHOD"):
            name = self._advance().value
        else:
            raise CNSHParseError("装饰器需要名称", start.line, start.column)
        args: List[ASTNode] = []
        if self._check("LPAREN"):
            self._advance()
            args = self._argument_list()
            self._expect("RPAREN", "装饰器参数需要 ')'")
        return Decorator(name=name, args=args, line=start.line, column=start.column)

    def _decorated_decl(self, decorators: List[Decorator]) -> ASTNode:
        self._skip_newlines()
        if self._peek().type in ("FUNCTION", "DEF"):
            return self._function_decl(decorators)
        if self._peek().type == "CLASS":
            return self._class_decl(decorators)
        if self._peek().type == "ASYNC":
            return self._async_stmt(decorators)
        raise CNSHParseError("装饰器只能修饰函数、方法或类", self._peek().line, self._peek().column)

    def _class_decl(self, decorators: Optional[List[Decorator]] = None) -> ASTNode:
        start = self._advance()  # CLASS
        name = self._expect_identifier_like("类声明需要名称")
        base: Optional[str] = None
        if self._check("LPAREN"):
            self._advance()
            if self._peek().type in ("IDENTIFIER", "ENUM") or self._peek().value.isidentifier():
                base = self._advance().value
            else:
                tok = self._peek()
                raise CNSHParseError(f"类基类需要名称，但得到 {tok.type}({tok.value!r})", tok.line, tok.column, tok.file)
            self._expect("RPAREN", "类基类需要 ')'")
        self._expect("LBRACE", "类体需要 '{'")
        decorators = decorators or []
        is_enum = base == "枚举类" or any(d.name == "枚举类" for d in decorators)
        is_dataclass = any(d.name == "数据类" for d in decorators)
        if is_enum:
            members = self._enum_body()
            self._expect("RBRACE", "枚举类体需要 '}'")
            unique = any(d.name == "枚举唯一" for d in decorators)
            return EnumDecl(
                name=name,
                base=base or "枚举类",
                unique=unique,
                members=members,
                line=start.line,
                column=start.column,
            )
        if is_dataclass:
            fields, body = self._dataclass_body()
            self._expect("RBRACE", "数据类体需要 '}'")
            return DataClassDecl(
                name=name,
                decorators=decorators,
                fields=fields,
                body=body,
                line=start.line,
                column=start.column,
            )
        body = self._class_body()
        self._expect("RBRACE", "类体需要 '}'")
        return ClassDecl(
            name=name,
            base=base,
            decorators=decorators,
            body=body,
            line=start.line,
            column=start.column,
        )

    def _class_body(self) -> List[ASTNode]:
        body: List[ASTNode] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            body.append(self._class_body_item())
        return body

    def _class_body_item(self) -> ASTNode:
        decorator_starts = {
            "AT", "UNIQUE", "DATACLASS", "PROPERTY",
            "CLASSMETHOD", "STATICMETHOD", "ABSTRACTMETHOD",
        }
        if self._peek().type in decorator_starts:
            decorators = self._decorators()
            self._skip_newlines()
            if self._peek().type in ("FUNCTION", "DEF", "ASYNC"):
                if self._peek().type == "ASYNC":
                    return self._async_stmt(decorators)
                return self._method_decl(decorators)
            raise CNSHParseError("装饰器后需要方法定义", self._peek().line, self._peek().column)
        if self._peek().type == "ASYNC":
            return self._async_stmt()
        if self._peek().type in ("FUNCTION", "DEF"):
            return self._method_decl()
        if self._peek().type == "IDENTIFIER" and self._peek(1).type == "COLON":
            return self._field_decl()
        return self._statement()

    def _field_decl(self) -> DataClassField:
        start = self._advance()  # IDENTIFIER
        name = start.value
        if not name.isidentifier():
            raise CNSHParseError(f"字段需要名称，但得到 {start.type}({start.value!r})", start.line, start.column, start.file)
        self._expect("COLON", "字段声明需要 ':'")
        type_ann = self._parse_type_annotation("字段需要类型")
        default: Optional[ASTNode] = None
        if self._check("ASSIGN"):
            self._advance()
            default = self._expression()
        return DataClassField(
            name=name,
            type_annotation=type_ann,
            default=default,
            line=start.line,
            column=start.column,
        )

    def _enum_body(self) -> List[EnumMember]:
        members: List[EnumMember] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            stmt = self._statement()
            if (
                isinstance(stmt, ExpressionStmt)
                and isinstance(stmt.expression, BinaryExpr)
                and stmt.expression.op == "="
                and isinstance(stmt.expression.left, IdentifierExpr)
            ):
                members.append(
                    EnumMember(
                        name=stmt.expression.left.name,
                        value=stmt.expression.right,
                        line=stmt.line,
                        column=stmt.column,
                    )
                )
            else:
                raise CNSHParseError("枚举成员必须是 名称 = 值", stmt.line, stmt.column)
        return members

    def _dataclass_body(self):
        fields: List[DataClassField] = []
        body: List[ASTNode] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            if self._peek().type == "IDENTIFIER" and self._peek(1).type == "COLON":
                fields.append(self._field_decl())
            else:
                body.append(self._class_body_item())
        return fields, body

    def _with_stmt(self) -> WithStmt:
        start = self._advance()  # WITH
        items = self._with_items()
        self._expect("LBRACE", "使用语句需要 '{'")
        body = self._block_body()
        return WithStmt(items=items, body=body, line=start.line, column=start.column)

    def _async_with_stmt(self) -> AsyncWithStmt:
        start = self._advance()  # WITH
        items = self._with_items()
        self._expect("LBRACE", "异步使用语句需要 '{'")
        body = self._block_body()
        return AsyncWithStmt(items=items, body=body, line=start.line, column=start.column)

    def _with_items(self) -> List[WithItem]:
        items: List[WithItem] = []
        while True:
            context_expr = self._expression()
            var_name: Optional[str] = None
            if self._check("AS"):
                self._advance()
                var_name = self._expect("IDENTIFIER", "作为需要变量名").value
            items.append(WithItem(context_expr=context_expr, var_name=var_name))
            self._skip_newlines()
            if self._check("COMMA"):
                self._advance()
            else:
                break
        return items

    def _async_stmt(self, decorators: Optional[List[Decorator]] = None) -> ASTNode:
        self._advance()  # ASYNC
        self._skip_newlines()
        if self._peek().type in ("FUNCTION", "DEF"):
            return self._async_function_decl(decorators)
        if self._peek().type == "WITH":
            return self._async_with_stmt()
        if self._peek().type == "FOR":
            return self._async_for_stmt()
        raise CNSHParseError("异步语句只能是函数、使用或对于", self._peek().line, self._peek().column)

    def _async_function_decl(self, decorators: Optional[List[Decorator]] = None) -> MethodDecl:
        start = self._advance()  # FUNCTION or DEF
        name = self._expect_identifier_like("异步函数需要名称")
        self._expect("LPAREN", "异步函数参数需要 '('")
        params = self._parameter_list()
        self._expect("RPAREN", "异步函数参数需要 ')'")
        return_type_ann: Optional[str] = None
        if self._check("ARROW"):
            self._advance()
            return_type_ann = self._parse_type_annotation("异步函数返回类型")
        self._expect("LBRACE", "异步函数体需要 '{'")
        body = self._block_body()
        return MethodDecl(
            name=name,
            params=params,
            return_type_annotation=return_type_ann,
            decorators=decorators or [],
            body=body,
            is_async=True,
            line=start.line,
            column=start.column,
        )

    def _async_for_stmt(self) -> AsyncForStmt:
        start = self._advance()  # FOR
        var_name = self._expect_identifier_like("异步对于循环需要循环变量")
        if self._peek().value not in ("在", "in"):
            raise CNSHParseError("异步对于循环需要 '在' 或 'in'", self._peek().line, self._peek().column)
        self._advance()
        iterable = self._expression()
        self._expect("LBRACE", "异步对于循环需要 '{'")
        body = self._block_body()
        return AsyncForStmt(
            var_name=var_name,
            iterable=iterable,
            body=body,
            line=start.line,
            column=start.column,
        )

    def _try_stmt(self) -> TryStmt:
        start = self._advance()  # TRY
        self._expect("LBRACE", "尝试块需要 '{'")
        body = self._block_body()
        except_clauses: List[ExceptClause] = []
        while self._check("EXCEPT"):
            self._advance()
            exc_type: Optional[str] = None
            alias: Optional[str] = None
            if not self._check("AS") and not self._check("LBRACE"):
                exc_type = self._expect("IDENTIFIER", "捕获类型需要异常名").value
            if self._check("AS"):
                self._advance()
                alias = self._expect("IDENTIFIER", "作为需要变量名").value
            self._expect("LBRACE", "捕获块需要 '{'")
            clause_body = self._block_body()
            except_clauses.append(
                ExceptClause(
                    exc_type=exc_type,
                    alias=alias,
                    body=clause_body,
                )
            )
        finally_body: List[ASTNode] = []
        if self._check("FINALLY"):
            self._advance()
            self._expect("LBRACE", "最终块需要 '{'")
            finally_body = self._block_body()
        return TryStmt(
            body=body,
            except_clauses=except_clauses,
            finally_body=finally_body,
            line=start.line,
            column=start.column,
        )

    def _yield_stmt(self) -> ASTNode:
        start = self._advance()
        value: Optional[ASTNode] = None
        if not (self._check("SEMICOLON") or self._check("NEWLINE") or self._check("RBRACE") or self._check("EOF")):
            value = self._expression()
        self._statement_end()
        if start.type == "YIELD_FROM":
            return YieldFromStmt(value=value, line=start.line, column=start.column)
        return YieldStmt(value=value, line=start.line, column=start.column)

    def _raise_stmt(self) -> RaiseStmt:
        start = self._advance()
        value: Optional[ASTNode] = None
        if not (self._check("SEMICOLON") or self._check("NEWLINE") or self._check("RBRACE") or self._check("EOF")):
            value = self._expression()
        self._statement_end()
        return RaiseStmt(value=value, line=start.line, column=start.column)

    def _pass_stmt(self) -> PassStmt:
        start = self._advance()
        self._statement_end()
        return PassStmt(line=start.line, column=start.column)

    def _import_stmt(self) -> ImportStmt:
        start = self._advance()  # IMPORT or FROM
        if start.type == "IMPORT":
            module = self._parse_dotted_name()
            alias: Optional[str] = None
            if self._check("AS"):
                self._advance()
                alias = self._expect_identifier_like("作为需要别名")
            self._statement_end()
            return ImportStmt(module=module, alias=alias, line=start.line, column=start.column)
        # FROM ... IMPORT ...
        module = self._parse_dotted_name()
        self._expect("IMPORT", "从导入语句需要 导入")
        names: List[str] = [self._expect_identifier_like("导入名称")]
        while self._check("COMMA"):
            self._advance()
            names.append(self._expect_identifier_like("导入名称"))
        self._statement_end()
        return ImportStmt(module=module, names=names, is_from=True, line=start.line, column=start.column)

    def _parse_dotted_name(self) -> str:
        name = self._expect_identifier_like("需要模块名")
        while self._check("DOT"):
            self._advance()
            name = f"{name}.{self._expect_identifier_like('模块路径需要名称')}"
        return name

    # ---------- 表达式（优先级 climbing） ----------

    def _expression(self) -> ASTNode:
        return self._assignment()

    def _assignment(self) -> ASTNode:
        left = self._or_expr()
        assign_types = {"ASSIGN", "PLUS_ASSIGN", "MINUS_ASSIGN", "STAR_ASSIGN", "SLASH_ASSIGN", "PERCENT_ASSIGN"}
        if self._peek().type in assign_types:
            op = self._advance().value
            right = self._assignment()
            return BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _or_expr(self) -> ASTNode:
        left = self._and_expr()
        while self._check("OR"):
            op = self._advance().value
            right = self._and_expr()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _and_expr(self) -> ASTNode:
        left = self._equality()
        while self._check("AND"):
            op = self._advance().value
            right = self._equality()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _equality(self) -> ASTNode:
        left = self._comparison()
        while self._check("EQ") or self._check("NE"):
            op = self._advance().value
            right = self._comparison()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _comparison(self) -> ASTNode:
        left = self._additive()
        while self._check("LT") or self._check("GT") or self._check("LE") or self._check("GE"):
            op = self._advance().value
            right = self._additive()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _additive(self) -> ASTNode:
        left = self._multiplicative()
        while self._check("PLUS") or self._check("MINUS"):
            op = self._advance().value
            right = self._multiplicative()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _multiplicative(self) -> ASTNode:
        left = self._unary()
        while self._check("STAR") or self._check("SLASH") or self._check("PERCENT") or self._check("POWER") or self._check("FLOOR_DIV"):
            op = self._advance().value
            right = self._unary()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line, column=left.column)
        return left

    def _unary(self) -> ASTNode:
        if self._check("NOT") or self._check("PLUS") or self._check("MINUS"):
            op = self._advance().value
            operand = self._unary()
            return UnaryExpr(op=op, operand=operand, line=operand.line, column=operand.column)
        if self._check("AWAIT"):
            start = self._advance()
            operand = self._unary()
            return AwaitExpr(value=operand, line=start.line, column=start.column)
        return self._postfix()

    def _postfix(self) -> ASTNode:
        node = self._primary()
        while True:
            if self._check("LPAREN"):
                self._advance()
                args = self._argument_list()
                self._expect("RPAREN", "函数调用需要 ')'")
                node = CallExpr(callee=node, args=args, line=node.line, column=node.column)
            elif self._check("DOT"):
                self._advance()
                member_tok = self._peek()
                if member_tok.type != "IDENTIFIER" and not member_tok.value.isidentifier():
                    raise CNSHParseError(
                        f"成员访问需要名称，但得到 {member_tok.type}({member_tok.value!r})",
                        member_tok.line, member_tok.column, member_tok.file,
                    )
                member = self._advance().value
                node = MemberExpr(object=node, member=member, line=node.line, column=node.column)
            elif self._check("LBRACKET"):
                self._advance()
                idx = self._expression()
                self._expect("RBRACKET", "索引需要 ']'")
                node = IndexExpr(object=node, index=idx, line=node.line, column=node.column)
            else:
                break
        return node

    def _argument_list(self) -> List[ASTNode]:
        args: List[ASTNode] = []
        self._skip_newlines()
        if self._check("RPAREN"):
            return args
        while True:
            self._skip_newlines()
            # 关键字参数：名称 = 值
            if self._peek().type in ("IDENTIFIER", "DEFAULT_FACTORY") and self._peek(1).type == "ASSIGN":
                name = self._advance().value
                self._advance()  # =
                value = self._expression()
                args.append(BinaryExpr(op="=", left=IdentifierExpr(name=name), right=value))
            else:
                args.append(self._expression())
            self._skip_newlines()
            if self._check("COMMA"):
                self._advance()
            else:
                break
        self._skip_newlines()
        return args

    def _primary(self) -> ASTNode:
        tok = self._peek()
        if tok.type == "NUMBER":
            self._advance()
            value = float(tok.value) if "." in tok.value else int(tok.value)
            return LiteralExpr(value=value, line=tok.line, column=tok.column)
        if tok.type == "STRING":
            self._advance()
            return LiteralExpr(value=tok.value, line=tok.line, column=tok.column)
        if tok.type == "TRUE":
            self._advance()
            return LiteralExpr(value=True, line=tok.line, column=tok.column)
        if tok.type == "FALSE":
            self._advance()
            return LiteralExpr(value=False, line=tok.line, column=tok.column)
        if tok.type == "NULL":
            self._advance()
            return LiteralExpr(value=None, line=tok.line, column=tok.column)
        if tok.type == "IDENTIFIER" or tok.value.isidentifier():
            self._advance()
            return IdentifierExpr(name=tok.value, line=tok.line, column=tok.column)
        if tok.type == "LPAREN":
            self._advance()
            expr = self._expression()
            # 生成器表达式：(expr 对于 var 在 iterable 如果 condition)
            if self._check("FOR"):
                self._advance()
                var_name = self._expect("IDENTIFIER", "生成器表达式需要循环变量").value
                if self._peek().value not in ("在", "in"):
                    raise CNSHParseError("生成器表达式需要 '在' 或 'in'", self._peek().line, self._peek().column)
                self._advance()
                iterable = self._expression()
                condition: Optional[ASTNode] = None
                if self._check("IF"):
                    self._advance()
                    condition = self._expression()
                self._expect("RPAREN", "生成器表达式需要 ')'")
                return GeneratorExpr(
                    element=expr,
                    var_name=var_name,
                    iterable=iterable,
                    condition=condition,
                    line=tok.line,
                    column=tok.column,
                )
            self._expect("RPAREN", "括号表达式需要 ')'")
            return expr
        if tok.type == "LBRACKET":
            return self._list_literal()
        if tok.type == "LBRACE":
            return self._map_literal()
        raise CNSHParseError(f"无法解析的表达式起始: {tok.type}({tok.value!r})", tok.line, tok.column, tok.file)

    def _list_literal(self) -> ListExpr:
        start = self._advance()  # [
        elements: List[ASTNode] = []
        self._skip_newlines()
        if not self._check("RBRACKET"):
            while True:
                self._skip_newlines()
                elements.append(self._expression())
                self._skip_newlines()
                if self._check("COMMA"):
                    self._advance()
                else:
                    break
        self._skip_newlines()
        self._expect("RBRACKET", "列表需要 ']'")
        return ListExpr(elements=elements, line=start.line, column=start.column)

    def _map_literal(self) -> MapExpr:
        start = self._advance()  # {
        pairs: List[MapPair] = []
        self._skip_newlines()
        if not self._check("RBRACE"):
            while True:
                self._skip_newlines()
                key = self._expression()
                self._skip_newlines()
                self._expect("COLON", "映射键值对需要 ':'")
                self._skip_newlines()
                value = self._expression()
                pairs.append(MapPair(key=key, value=value))
                self._skip_newlines()
                if self._check("COMMA"):
                    self._advance()
                else:
                    break
        self._skip_newlines()
        self._expect("RBRACE", "映射需要 '}'")
        return MapExpr(pairs=pairs, line=start.line, column=start.column)

    # ═══════════════════════════════════════════════════════════════
    # CNSH v2.0-v2.3 新增语句解析方法
    # ═══════════════════════════════════════════════════════════════

    def _switch_stmt(self) -> SwitchStmt:
        """切换 表达式 { 情况 值: ... 默认: ... }"""
        start = self._advance()  # SWITCH
        value = self._expression()
        self._expect("LBRACE", "切换语句需要 '{'")
        cases: List[CaseClause] = []
        default_body: List[ASTNode] = []
        while not self._check("RBRACE") and not self._check("EOF"):
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            if self._check("CASE"):
                self._advance()
                case_val = self._expression()
                self._expect("COLON", "情况需要 ':'")
                case_body: List[ASTNode] = []
                while not self._check("CASE") and not self._check("DEFAULT") and not self._check("RBRACE"):
                    self._skip_newlines()
                    if self._check("CASE") or self._check("DEFAULT") or self._check("RBRACE"):
                        break
                    case_body.append(self._statement())
                cases.append(CaseClause(value=case_val, body=case_body))
            elif self._check("DEFAULT"):
                self._advance()
                self._expect("COLON", "默认需要 ':'")
                while not self._check("RBRACE") and not self._check("EOF"):
                    self._skip_newlines()
                    if self._check("RBRACE"):
                        break
                    default_body.append(self._statement())
            else:
                raise CNSHParseError("切换体需要 情况 或 默认", self._peek().line, self._peek().column)
        self._expect("RBRACE", "切换体需要 '}'")
        return SwitchStmt(value=value, cases=cases, default_body=default_body, line=start.line, column=start.column)

    def _hook_stmt(self, hook_type: str = "") -> HookStmt:
        """钩子/前置钩子/后置钩子 名称(参数) { ... }"""
        start = self._advance()  # HOOK / BEFORE_HOOK / AFTER_HOOK
        name = self._expect("IDENTIFIER", "钩子需要名称").value
        params: List[Parameter] = []
        if self._check("LPAREN"):
            self._advance()
            params = self._parameter_list()
            self._expect("RPAREN", "钩子参数需要 ')'")
        self._expect("LBRACE", "钩子体需要 '{'")
        body = self._block_body()
        return HookStmt(name=name, params=params, body=body, hook_type=hook_type, line=start.line, column=start.column)

    def _tri_color_audit_stmt(self) -> TriColorAuditStmt:
        """三色审计(操作映射)"""
        start = self._advance()  # TRI_COLOR_AUDIT
        operation: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                operation = self._expression()
            self._expect("RPAREN", "三色审计参数需要 ')'")
        self._statement_end()
        return TriColorAuditStmt(operation=operation, line=start.line, column=start.column)

    def _dna_register_stmt(self) -> DNARegisterStmt:
        """DNA登记(信息)"""
        start = self._advance()  # DNA_REGISTER
        info: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                info = self._expression()
            self._expect("RPAREN", "DNA登记参数需要 ')'")
        self._statement_end()
        return DNARegisterStmt(info=info, line=start.line, column=start.column)

    def _dna_verify_stmt(self) -> DNAVerifyStmt:
        """DNA验证(码)"""
        start = self._advance()  # DNA_VERIFY
        dna_code: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                dna_code = self._expression()
            self._expect("RPAREN", "DNA验证参数需要 ')'")
        self._statement_end()
        return DNAVerifyStmt(dna_code=dna_code, line=start.line, column=start.column)

    def _dna_sign_stmt(self) -> DNASignStmt:
        """DNA签章(信息)"""
        start = self._advance()  # DNA_SIGN
        info: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                info = self._expression()
            self._expect("RPAREN", "DNA签章参数需要 ')'")
        self._statement_end()
        return DNASignStmt(info=info, line=start.line, column=start.column)

    def _abort_stmt(self) -> AbortStmt:
        """熔断(原因)"""
        start = self._advance()  # ABORT
        reason: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                reason = self._expression()
            self._expect("RPAREN", "熔断参数需要 ')'")
        self._statement_end()
        return AbortStmt(reason=reason, line=start.line, column=start.column)

    def _create_rollback_stmt(self) -> CreateRollbackStmt:
        """生成回滚点(标记)"""
        start = self._advance()  # CREATE_ROLLBACK
        label: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                label = self._expression()
            self._expect("RPAREN", "生成回滚点参数需要 ')'")
        self._statement_end()
        return CreateRollbackStmt(label=label, line=start.line, column=start.column)

    def _rollback_stmt(self) -> RollbackStmt:
        """回滚(快照ID)"""
        start = self._advance()  # ROLLBACK
        snapshot_id: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                snapshot_id = self._expression()
            self._expect("RPAREN", "回滚参数需要 ')'")
        self._statement_end()
        return RollbackStmt(snapshot_id=snapshot_id, line=start.line, column=start.column)

    def _verify_rollback_stmt(self) -> VerifyRollbackStmt:
        """验证回滚(快照ID)"""
        start = self._advance()  # VERIFY_ROLLBACK
        snapshot_id: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                snapshot_id = self._expression()
            self._expect("RPAREN", "验证回滚参数需要 ')'")
        self._statement_end()
        return VerifyRollbackStmt(snapshot_id=snapshot_id, line=start.line, column=start.column)

    def _test_stmt(self) -> TestStmt:
        """测试 "名称" { ... }"""
        start = self._advance()  # TEST
        name = self._expect("STRING", "测试需要名称字符串").value
        self._expect("LBRACE", "测试体需要 '{'")
        body = self._block_body()
        return TestStmt(name=name, body=body, line=start.line, column=start.column)

    def _assert_stmt(self) -> AssertStmt:
        """断言 表达式 == 期望值"""
        start = self._advance()  # ASSERT
        actual = self._expression()
        expected: Optional[ASTNode] = None
        if self._check("EQ"):
            self._advance()
            expected = self._expression()
        self._statement_end()
        return AssertStmt(actual=actual, expected=expected, line=start.line, column=start.column)

    def _expect_stmt(self) -> ExpectStmt:
        """期望 表达式 == 值"""
        start = self._advance()  # EXPECT
        actual = self._expression()
        expected: Optional[ASTNode] = None
        if self._check("EQ"):
            self._advance()
            expected = self._expression()
        self._statement_end()
        return ExpectStmt(actual=actual, expected=expected, line=start.line, column=start.column)

    def _route_to_stmt(self) -> RouteToStmt:
        """路由到 人格名"""
        start = self._advance()  # ROUTE_TO
        persona = self._expect("IDENTIFIER", "路由到需要人格名").value
        self._statement_end()
        return RouteToStmt(persona=persona, line=start.line, column=start.column)

    def _quantum_entangle_stmt(self) -> QuantumEntangleStmt:
        """量子纠缠(父, 子)"""
        start = self._advance()  # QUANTUM_ENTANGLE
        self._expect("LPAREN", "量子纠缠需要 '('")
        parent: Optional[ASTNode] = None
        child: Optional[ASTNode] = None
        if not self._check("RPAREN"):
            parent = self._expression()
            if self._check("COMMA"):
                self._advance()
                child = self._expression()
        self._expect("RPAREN", "量子纠缠需要 ')'")
        self._statement_end()
        return QuantumEntangleStmt(parent=parent, child=child, line=start.line, column=start.column)

    def _collapse_stmt(self) -> CollapseStmt:
        """坍缩到(状态)"""
        start = self._advance()  # COLLAPSE
        state: Optional[ASTNode] = None
        if self._check("LPAREN"):
            self._advance()
            if not self._check("RPAREN"):
                state = self._expression()
            self._expect("RPAREN", "坍缩到需要 ')'")
        self._statement_end()
        return CollapseStmt(state=state, line=start.line, column=start.column)

    def _cold_start_stmt(self) -> ColdStartStmt:
        """冷启动"""
        start = self._advance()
        self._statement_end()
        return ColdStartStmt(line=start.line, column=start.column)

    def _hot_start_stmt(self) -> HotStartStmt:
        """热启动"""
        start = self._advance()
        self._statement_end()
        return HotStartStmt(line=start.line, column=start.column)

    def _exit_program_stmt(self) -> ExitProgramStmt:
        """终止执行(退出码)"""
        start = self._advance()  # EXIT_PROGRAM
        code: Optional[ASTNode] = None
        if not (self._check("SEMICOLON") or self._check("NEWLINE") or self._check("RBRACE") or self._check("EOF")):
            code = self._expression()
        self._statement_end()
        return ExitProgramStmt(code=code, line=start.line, column=start.column)

    def _export_stmt(self) -> ExportStmt:
        """导出 名称"""
        start = self._advance()  # EXPORT
        name = self._expect("IDENTIFIER", "导出需要名称").value
        self._statement_end()
        return ExportStmt(name=name, line=start.line, column=start.column)

    def _audit_stmt(self) -> AuditStmt:
        """已审计 / 审计中"""
        start = self._advance()  # AUDITING or AUDITED
        self._statement_end()
        return AuditStmt(status=start.type, line=start.line, column=start.column)

    def _global_decl(self) -> VarDecl:
        """全局 变量名 = 初始值"""
        start = self._advance()  # GLOBAL
        name = self._expect_identifier_like("全局变量需要名称")
        type_ann: Optional[str] = None
        if self._check("COLON"):
            self._advance()
            type_ann = self._parse_type_annotation("全局变量类型")
        init: Optional[ASTNode] = None
        if self._check("ASSIGN"):
            self._advance()
            init = self._expression()
        self._statement_end()
        return VarDecl(name=name, initializer=init, is_const=False, type_annotation=type_ann, line=start.line, column=start.column)
