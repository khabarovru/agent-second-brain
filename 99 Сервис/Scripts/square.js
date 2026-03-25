module.exports = async (params) => {
    console.log("Starting word-by-word bracket toggle script...");

    // Получаем активный редактор
    const activeLeaf = params.app.workspace.activeLeaf;
    if (!activeLeaf || !activeLeaf.view || !activeLeaf.view.editor) {
        console.log("Ошибка: редактор не найден");
        return;
    }

    const editor = activeLeaf.view.editor;
    const selectedText = editor.getSelection();

    if (!selectedText) {
        console.log("Ошибка: текст не выделен");
        return;
    }

    // Запоминаем исходные координаты выделенного текста
    const selectionStart = editor.getCursor('from');
    const selectionEnd = editor.getCursor('to');

    // Разбиваем текст на слова, сохраняя пробелы
    const words = selectedText.split(/(\s+)/); // Учитываем пробелы
    console.log("Разбитый текст:", words);

    let newText = words.map(word => {
        if (word.trim()) {
            if (/^\[\[.*\]\]$/.test(word)) {
                return word.slice(2, -2);
            } else if (/^\[.*\]$/.test(word)) {
                return `[[$1]]`.replace('$1', word.slice(1, -1));
            } else {
                return `[${word}]`;
            }
        }
        return word;
    }).join('');

    // Вставляем изменённый текст обратно в редактор
    editor.replaceSelection(newText);

    // Восстанавливаем выделение
    const newSelectionEnd = {
        line: selectionStart.line,
        ch: selectionStart.ch + newText.length
    };
    editor.setSelection(selectionStart, newSelectionEnd);

    console.log("Выделение восстановлено:", selectionStart, newSelectionEnd);
};
