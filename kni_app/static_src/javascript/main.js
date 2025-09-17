import ThemeToggle from "./components/theme-toggle";
import HeaderSearchPanel from "./components/header-search-panel";
import SkipLink from './components/skip-link';
import CollapseToggle from './components/collapse';

import '../sass/main.scss';


function initComponent(ComponentClass) {
    const items = document.querySelectorAll(ComponentClass.selector());
    items.forEach((item) => new ComponentClass(item));
}

document.addEventListener('DOMContentLoaded', () => {
    initComponent(ThemeToggle);
    initComponent(SkipLink);
    initComponent(HeaderSearchPanel);
    initComponent(CollapseToggle);
});
