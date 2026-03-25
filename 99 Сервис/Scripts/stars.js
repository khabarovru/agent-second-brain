module.exports = async (params) => {
    console.log("Starting asterisk toggle script...");

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

    // Проверяем, есть ли уже звёздочки в начале и в конце текста
    let newText;
    if (/^\*\*.*\*\*$/.test(selectedText)) {
        newText = selectedText.slice(2, -2);  // Удаляем двойные звёздочки
        console.log("Удалены двойные звёздочки:", newText);
    } else if (/^\*.*\*$/.test(selectedText)) {
        newText = `**${selectedText.slice(1, -1)}**`;  // Заменяем на двойные
        console.log("Заменены звёздочки на двойные:", newText);
    } else {
        newText = `*${selectedText}*`;  // Добавляем одну звёздочку
        console.log("Добавлены звёздочки:", newText);
    }

    // Вставляем новый текст
    editor.replaceSelection(newText);

    // Фиксируем точное выделение вручную
    const newSelectionEnd = {
        line: selectionStart.line,
        ch: selectionStart.ch + newText.length
    };
    editor.setSelection(selectionStart, newSelectionEnd);

    console.log("Выделение восстановлено:", selectionStart, newSelectionEnd);
};
