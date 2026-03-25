function collapseBacklinks() {
    console.log("Collapsing backlinks...");
    
    // Попробуем разные возможные селекторы
    const selectors = [
        '.embedded-backlinks',
        '.backlink-pane',
        '[data-type="backlink"]',
        '.view-content .tree-item'
    ];
    
    selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        console.log(`Found ${elements.length} elements for selector: ${selector}`);
        
        elements.forEach(element => {
            // Попробуем найти элементы для сворачивания
            const children = element.querySelectorAll('.tree-item-children, .search-result-container');
            children.forEach(child => {
                child.style.display = 'none';
            });
            
            // Добавим класс is-collapsed если возможно
            element.classList.add('is-collapsed');
        });
    });
}

// Запускаем при разных событиях
if (typeof app !== 'undefined' && app.workspace) {
    app.workspace.on('layout-ready', () => {
        setTimeout(collapseBacklinks, 1000);
    });
    app.workspace.on('active-leaf-change', () => {
        setTimeout(collapseBacklinks, 500);
    });
    app.workspace.on('file-open', () => {
        setTimeout(collapseBacklinks, 300);
    });
}

// Также запускаем при загрузке
setTimeout(collapseBacklinks, 2000);