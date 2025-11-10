import js from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import prettier from "@vue/eslint-config-prettier";
import globals from "globals";

export default [
  {
    ignores: ["node_modules", "dist"],
  },
  js.configs.recommended,
  ...pluginVue.configs["flat/recommended"],
  prettier,
  {
    files: ["**/*.{js,mjs,cjs,jsx,vue}"],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      "vue/multi-word-component-names": "off",
      "vue/require-default-prop": "off",
      "no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
    },
  },
];
