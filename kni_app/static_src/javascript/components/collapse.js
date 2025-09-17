class CollapseToggle {
    static selector() {
        return '[data-hs-collapse]';
    }

    constructor(node) {
        this.toggle = node;
        this.targetSelector = this.toggle.getAttribute('data-hs-collapse');
        this.target = document.querySelector(this.targetSelector);
        this.isTransitioning = false;

        if (!this.target) {
            return;
        }

        this.closeOnLinkClick = this.closeOnLinkClick.bind(this);
        this.handleToggle = this.handleToggle.bind(this);
        this.updateForViewport = this.updateForViewport.bind(this);

        this.target.classList.add('hidden');
        this.target.style.height = '0px';
        this.toggle.setAttribute('aria-expanded', this.toggle.classList.contains('hs-collapse-open') ? 'true' : 'false');

        this.toggle.addEventListener('click', this.handleToggle);
        this.target.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', this.closeOnLinkClick);
        });

        this.breakpoint = window.matchMedia('(min-width: 768px)');
        if (this.breakpoint.addEventListener) {
            this.breakpoint.addEventListener('change', this.updateForViewport);
        } else if (this.breakpoint.addListener) {
            this.breakpoint.addListener(this.updateForViewport);
        }

        this.updateForViewport(this.breakpoint);
    }

    handleToggle(event) {
        event.preventDefault();

        if (this.isTransitioning) {
            return;
        }

        if (this.toggle.classList.contains('hs-collapse-open')) {
            this.close();
        } else {
            this.open();
        }
    }

    closeOnLinkClick() {
        if (window.matchMedia('(max-width: 767px)').matches && this.toggle.classList.contains('hs-collapse-open')) {
            this.close();
        }
    }

    open() {
        this.isTransitioning = true;
        this.toggle.classList.add('hs-collapse-open');
        this.toggle.setAttribute('data-hs-collapse-open', 'true');
        this.toggle.setAttribute('aria-expanded', 'true');
        this.target.classList.remove('hidden');
        this.target.style.height = '0px';

        requestAnimationFrame(() => {
            this.target.style.height = this.target.scrollHeight + 'px';
            this.target.classList.add('open');
        });

        this.target.addEventListener('transitionend', () => {
            this.isTransitioning = false;
            this.target.style.height = '';
        }, { once: true });
    }

    close() {
        this.isTransitioning = true;
        this.toggle.classList.remove('hs-collapse-open');
        this.toggle.removeAttribute('data-hs-collapse-open');
        this.toggle.setAttribute('aria-expanded', 'false');

        this.target.style.height = this.target.scrollHeight + 'px';
        requestAnimationFrame(() => {
            this.target.style.height = '0px';
        });

        this.target.addEventListener('transitionend', () => {
            this.isTransitioning = false;
            this.target.classList.remove('open');
            this.target.classList.add('hidden');
            this.target.style.height = '';
        }, { once: true });
    }

    updateForViewport(event) {
        const matches = typeof event.matches === 'boolean' ? event.matches : event;

        if (matches) {
            this.toggle.classList.add('hs-collapse-open');
            this.toggle.setAttribute('data-hs-collapse-open', 'true');
            this.toggle.setAttribute('aria-expanded', 'true');
            this.target.classList.remove('hidden');
            this.target.style.height = '';
        } else {
            this.toggle.classList.remove('hs-collapse-open');
            this.toggle.removeAttribute('data-hs-collapse-open');
            this.toggle.setAttribute('aria-expanded', 'false');
            this.target.classList.add('hidden');
            this.target.style.height = '0px';
        }
    }
}

export default CollapseToggle;
