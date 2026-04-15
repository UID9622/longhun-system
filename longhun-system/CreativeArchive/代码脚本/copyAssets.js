const fs = require("fs")
const path = require("path")
const os = require("os");
const { spawn } = require("child_process");
/**
 * @type {import('esbuild').Plugin}
 */

function copyAssets() {
	// tree sitter

	const sourceDir = path.join(__dirname, "node_modules", "web-tree-sitter")
	const targetDir = path.join(__dirname, "out")

	// Copy tree-sitter.wasm
	fs.copyFileSync(path.join(sourceDir, "tree-sitter.wasm"), path.join(targetDir, "tree-sitter.wasm"))

	// Copy codicon from node_modules
  const sourceCodiconDir = path.join(__dirname, "node_modules", "@vscode", "codicons", "dist")
	// 暂时屏蔽cline const sourceKatexDir = path.join(__dirname, "cline", "webview-ui", "node_modules", "katex", "dist")
	fs.copyFileSync(path.join(sourceCodiconDir, "codicon.css"), path.join(targetDir, "codicon.css"))
	fs.copyFileSync(path.join(sourceCodiconDir, "codicon.ttf"), path.join(targetDir, "codicon.ttf"))
	// 暂时屏蔽cline fs.copyFileSync(path.join(sourceKatexDir, "katex.min.css"), path.join(targetDir, "katex.min.css"))
}
function downloadRigGrep() {
	const platform = os.platform(); // win32 / linux / darwin

	let cmd;
	let args;

	if (platform === "win32") {
		cmd = "cmd.exe";
		args = [
			"/c",
			path.join(__dirname, "script", "windows", "ripgrep.bat")
		];
	} else {
		cmd = "sh";
		args = [
			path.join(__dirname, "script", "linux", "ripgrep.sh")
		];
	}

	const child = spawn(cmd, args, { stdio: "inherit" });
}
async function main() {
	copyAssets();
	downloadRigGrep();
}

main().catch((e) => {
	console.error(e)
	process.exit(1)
})
