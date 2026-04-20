module.exports = async (params) => {
    function collapseBacklinks() {
        const selectors = [
            '.embedded-backlinks',
            '.backlink-pane',
            '[data-type="backlink"]',
            '.view-content .tree-item'
        ];

        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                const children = element.querySelectorAll('.tree-item-children, .search-result-container');
                children.forEach(child => {
                    child.style.display = 'none';
                });
                element.classList.add('is-collapsed');
            });
        });
    }

    if (typeof app !== 'undefined' && app.workspace) {
        app.workspace.on('layout-ready', () => setTimeout(collapseBacklinks, 1000));
        app.workspace.on('active-leaf-change', () => setTimeout(collapseBacklinks, 500));
        app.workspace.on('file-open', () => setTimeout(collapseBacklinks, 300));
    }

    setTimeout(collapseBacklinks, 2000);
};
