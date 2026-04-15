const vscode = acquireVsCodeApi();

function agreeDisclaimer() {
  vscode.postMessage({
    disclaimer: 'yes',
  });
}

function main() {
  document
    .getElementById('agree-disclaimer-btn')
    .addEventListener('click', agreeDisclaimer);
}

window.addEventListener('load', main);
