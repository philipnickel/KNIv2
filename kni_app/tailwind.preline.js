const plugin = require('tailwindcss/plugin');

module.exports = plugin(function({ addVariant, e }) {
    addVariant('hs-collapse-open', ({ modifySelectors, separator }) => {
        modifySelectors(({ className }) => {
            return `.hs-collapse-open .${e(`hs-collapse-open${separator}${className}`)}`;
        });
    });
});
