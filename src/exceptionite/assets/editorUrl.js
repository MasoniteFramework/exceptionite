export default function editorUrl(editorName, file, lineNumber) {
    const editor = editorName
    const editors = {
        sublime: 'subl://open?url=file://%path&line=%line',
        textmate: 'txmt://open?url=file://%path&line=%line',
        emacs: 'emacs://open?url=file://%path&line=%line',
        macvim: 'mvim://open/?url=file://%path&line=%line',
        pycharm: 'pycharm://open?file=%path&line=%line',
        idea: 'idea://open?file=%path&line=%line',
        vscode: 'vscode://file/%path:%line',
        'vscode-insiders': 'vscode-insiders://file/%path:%line',
        'vscode-remote': 'vscode://vscode-remote/%path:%line',
        'vscode-insiders-remote': 'vscode-insiders://vscode-remote/%path:%line',
        vscodium: 'vscodium://file/%path:%line',
        atom: 'atom://core/open/file?filename=%path&line=%line',
    };

    if (!Object.keys(editors).includes(editor)) {
        console.error(
            `'${editor}' is not supported. Support editors are: ${Object.keys(editors).join(', ')}`,
        );

        return null;
    }

    return editors[editor]
        .replace('%path', encodeURIComponent(file))
        .replace('%line', encodeURIComponent(lineNumber));
}