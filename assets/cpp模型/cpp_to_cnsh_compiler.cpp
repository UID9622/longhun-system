// ═══════════════════════════════════════════════════════════
// C++ → CNSH 反向编译器 v1.0
// 功能：将C++代码翻译为CNSH语法（只转语法，不探测逻辑）
// 创建者：龍芯北辰·UID9622（诸葛鑫）
// 协作：Claude (Anthropic)
// DNA追溯：#龍芯⚡️20260303-反向编译器-v1.0
// 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// 
// 授权说明：
//   ✅ UID9622（诸葛鑫）- 创建者，完全授权
//   ✅ 华为技术团队 - 授权使用（合作目的）
//   ✅ UID9622明确授权的个人/组织
//   ❌ 未经授权的商业使用
//   ❌ 探测商业秘密用途
// 
// 基本原则：
//   - 只转换语法，不分析商业逻辑
//   - 不记录、不上传、不分析源代码内容
//   - 尊重知识产权，只做语法映射
// ═══════════════════════════════════════════════════════════

#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <regex>
#include <fstream>
#include <sstream>

using namespace std;

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// C++ → CNSH 映射表（反向映射）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

map<string, string> cpp_to_cnsh = {
    // 基本关键词（从C++到CNSH）
    {"auto", "定义"},
    {"void", ""},
    {"return", "返回"},
    {"if", "如果"},
    {"else", "否则"},
    {"while", "当"},
    {"for", "循环"},
    {"true", "真"},
    {"false", "假"},
    {"&&", "并且"},
    {"||", "或者"},
    {"!", "不是"},
    {"==", "等于"},
    {"!=", "不等于"},
    {">", "大于"},
    {"<", "小于"},
    {">=", "大于等于"},
    {"<=", "小于等于"},
    
    // 数据类型
    {"int", "整数"},
    {"double", "小数"},
    {"float", "小数"},
    {"string", "文本"},
    {"bool", "布尔"},
    {"vector", "列表"},
    
    // 输入输出
    {"cout", "打印"},
    {"cin", "输入"},
    {"endl", ""},
    
    // 数学函数
    {"pow", "平方"},
    {"sqrt", "平方根"},
    {"abs", "绝对值"},
    {"max", "最大值"},
    {"min", "最小值"},
    
    // 容器操作
    {".size()", "长度"},
    {".push_back", "添加"},
    {".erase", "删除"},
    {".find", "查找"},
    
    // 其他
    {"continue", "继续"},
    {"break", "跳出"}
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 辅助函数
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

string trim(const string& str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    if (first == string::npos) return "";
    size_t last = str.find_last_not_of(" \t\n\r");
    return str.substr(first, (last - first + 1));
}

string replaceAll(string str, const string& from, const string& to) {
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
    return str;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// C++ → CNSH 反向编译器核心类
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CPPtoCNSHCompiler {
private:
    vector<string> cnsh_output;
    
    // 翻译单行C++代码为CNSH
    string translateLine(const string& line) {
        string result = line;
        
        // 跳过注释（保持原样）
        if (trim(result).substr(0, 2) == "//") {
            return result;
        }
        
        // 处理函数定义
        // void functionName() { → 定义 functionName 为 函数() {
        regex func_pattern(R"(^\s*(void|int|double|string)\s+(\w+)\s*\([^)]*\)\s*\{?)");
        smatch matches;
        if (regex_search(result, matches, func_pattern)) {
            string func_name = matches[2];
            result = "定义 " + func_name + " 为 函数() {";
            return result;
        }
        
        // 处理变量定义
        // int x = 10; → 定义 x 为 整数 = 10
        regex var_pattern(R"(^\s*(int|double|float|string|bool)\s+(\w+)\s*=\s*([^;]+);)");
        if (regex_search(result, matches, var_pattern)) {
            string type = matches[1];
            string var_name = matches[2];
            string value = matches[3];
            
            string cnsh_type;
            if (type == "int") cnsh_type = "整数";
            else if (type == "double" || type == "float") cnsh_type = "小数";
            else if (type == "string") cnsh_type = "文本";
            else if (type == "bool") cnsh_type = "布尔";
            
            result = "定义 " + var_name + " 为 " + cnsh_type + " = " + trim(value);
            return result;
        }
        
        // 处理cout输出
        // cout << "text" << endl; → 打印("text")
        if (result.find("cout") != string::npos) {
            // 简单处理：提取引号中的内容或变量
            regex cout_pattern(R"(cout\s*<<\s*(.+?)\s*(?:<<\s*endl)?;?)");
            if (regex_search(result, matches, cout_pattern)) {
                string content = matches[1];
                content = replaceAll(content, "<<", "");
                content = trim(content);
                result = "打印(" + content + ")";
                return result;
            }
        }
        
        // 处理if语句
        // if (condition) { → 如果 condition 那么 {
        if (result.find("if") != string::npos && result.find("(") != string::npos) {
            regex if_pattern(R"(if\s*\(([^)]+)\)\s*\{?)");
            if (regex_search(result, matches, if_pattern)) {
                string condition = matches[1];
                result = "如果 " + trim(condition) + " 那么 {";
                return result;
            }
        }
        
        // 处理else
        if (trim(result) == "} else {" || trim(result) == "else {") {
            return "} 否则 {";
        }
        
        // 处理while循环
        // while (condition) { → 当 condition {
        if (result.find("while") != string::npos) {
            regex while_pattern(R"(while\s*\(([^)]+)\)\s*\{?)");
            if (regex_search(result, matches, while_pattern)) {
                string condition = matches[1];
                result = "当 " + trim(condition) + " {";
                return result;
            }
        }
        
        // 处理return语句
        // return value; → 返回 value
        if (result.find("return") != string::npos) {
            regex return_pattern(R"(return\s+([^;]+);?)");
            if (regex_search(result, matches, return_pattern)) {
                string value = matches[1];
                result = "返回 " + trim(value);
                return result;
            }
        }
        
        // 逐个替换关键词（对于没有被特殊处理的）
        for (const auto& pair : cpp_to_cnsh) {
            if (!pair.second.empty()) {
                result = replaceAll(result, pair.first, pair.second);
            }
        }
        
        // 移除多余的分号
        if (result.back() == ';') {
            result.pop_back();
        }
        
        return result;
    }
    
public:
    CPPtoCNSHCompiler() {
        // 添加文件头
        cnsh_output.push_back("// ═══════════════════════════════════════════════");
        cnsh_output.push_back("// C++编译生成的CNSH代码");
        cnsh_output.push_back("// DNA追溯：#龍芯⚡️20260303-反向编译输出-v1.0");
        cnsh_output.push_back("// 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z");
        cnsh_output.push_back("// ═══════════════════════════════════════════════");
        cnsh_output.push_back("");
    }
    
    // 编译C++代码
    void compile(const vector<string>& cpp_lines) {
        for (const string& line : cpp_lines) {
            string trimmed = trim(line);
            
            // 跳过空行
            if (trimmed.empty()) {
                cnsh_output.push_back("");
                continue;
            }
            
            // 跳过#include等预处理指令
            if (trimmed[0] == '#') {
                continue;
            }
            
            // 跳过using namespace
            if (trimmed.find("using namespace") != string::npos) {
                continue;
            }
            
            // 翻译并添加到输出
            string translated = translateLine(line);
            cnsh_output.push_back(translated);
        }
    }
    
    // 获取CNSH代码
    string getCNSHCode() {
        string result;
        for (const string& line : cnsh_output) {
            result += line + "\n";
        }
        return result;
    }
    
    // 保存到文件
    void saveToFile(const string& filename) {
        ofstream outfile(filename);
        outfile << getCNSHCode();
        outfile.close();
        cout << "✅ CNSH代码已保存到: " << filename << endl;
    }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 主程序
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

int main(int argc, char* argv[]) {
    cout << "╔═══════════════════════════════════════════╗" << endl;
    cout << "║                                           ║" << endl;
    cout << "║     🐉 C++ → CNSH 反向编译器 v1.0 🐉    ║" << endl;
    cout << "║                                           ║" << endl;
    cout << "║  C++ → CNSH 语法翻译                     ║" << endl;
    cout << "║                                           ║" << endl;
    cout << "╚═══════════════════════════════════════════╝" << endl;
    cout << endl;
    cout << "DNA追溯：#龍芯⚡️20260303-反向编译器-v1.0" << endl;
    cout << "确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z" << endl;
    cout << endl;
    cout << "授权用户：UID9622、华为技术团队、明确授权者" << endl;
    cout << "基本原则：只转语法，不探测商业逻辑" << endl;
    cout << endl;
    
    // 检查参数
    if (argc < 2) {
        cout << "用法: " << argv[0] << " <C++源文件>" << endl;
        return 1;
    }
    
    // 读取C++源文件
    string input_file = argv[1];
    ifstream infile(input_file);
    
    if (!infile.is_open()) {
        cout << "❌ 无法打开文件: " << input_file << endl;
        return 1;
    }
    
    vector<string> cpp_lines;
    string line;
    while (getline(infile, line)) {
        cpp_lines.push_back(line);
    }
    infile.close();
    
    cout << "✅ 已读取C++源文件: " << input_file << endl;
    cout << "📄 共 " << cpp_lines.size() << " 行代码" << endl;
    cout << endl;
    
    // 编译
    cout << "🔄 开始反向编译..." << endl;
    CPPtoCNSHCompiler compiler;
    compiler.compile(cpp_lines);
    
    // 生成输出文件名
    string output_file = input_file;
    size_t pos = output_file.find(".cpp");
    if (pos != string::npos) {
        output_file = output_file.substr(0, pos) + ".cnsh";
    } else {
        output_file += ".cnsh";
    }
    
    // 保存CNSH代码
    compiler.saveToFile(output_file);
    
    cout << endl;
    cout << "✅ 反向编译完成！" << endl;
    cout << "📝 CNSH代码: " << output_file << endl;
    cout << endl;
    cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << endl;
    cout << "⚠️  重要提醒：" << endl;
    cout << "   - 此工具仅用于语法转换" << endl;
    cout << "   - 不记录、不分析代码逻辑" << endl;
    cout << "   - 尊重知识产权" << endl;
    cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << endl;
    cout << endl;
    
    return 0;
}
