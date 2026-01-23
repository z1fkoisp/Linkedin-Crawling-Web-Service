// ESLint Configuration for LinkedIn Web Crawler Frontend
// This configuration sets up linting rules for React + Vite project

// Import core ESLint recommended rules
import js from '@eslint/js'
// Import browser globals for client-side JavaScript
import globals from 'globals'
// Import React-specific ESLint plugin
import react from 'eslint-plugin-react'
// Import React Hooks ESLint plugin for hook rules
import reactHooks from 'eslint-plugin-react-hooks'
// Import Vite's React refresh plugin for HMR validation
import reactRefresh from 'eslint-plugin-react-refresh'

// Export the ESLint configuration as an array of config objects
export default [
  // First config object: Global ignore patterns
  {
    // Ignore the build output directory to avoid linting generated files
    ignores: ['dist']
  },

  // Second config object: Main configuration for source files
  {
    // Specify which files this configuration applies to
    files: ['**/*.{js,jsx}'],

    // Language options for parsing JavaScript/JSX
    languageOptions: {
      // ECMAScript version for parsing (2020 for modern JS)
      ecmaVersion: 2020,
      // Include browser globals (window, document, etc.)
      globals: globals.browser,
      // Parser options for JSX and modern JS features
      parserOptions: {
        // Latest ECMAScript version
        ecmaVersion: 'latest',
        // Enable JSX parsing
        ecmaFeatures: { jsx: true },
        // Source type is module (ES modules)
        sourceType: 'module',
      },
    },

    // Settings for specific plugins
    settings: {
      // Specify React version for accurate linting
      react: { version: '18.3' }
    },

    // Plugins to use for this configuration
    plugins: {
      // React plugin for React-specific rules
      react,
      // React hooks plugin with alias for hook rules
      'react-hooks': reactHooks,
      // React refresh plugin for Vite HMR validation
      'react-refresh': reactRefresh,
    },

    // ESLint rules configuration
    rules: {
      // Include all recommended rules from ESLint core
      ...js.configs.recommended.rules,
      // Include all recommended rules from React plugin
      ...react.configs.recommended.rules,
      // Include JSX runtime rules from React plugin
      ...react.configs['jsx-runtime'].rules,
      // Include all recommended rules from React hooks plugin
      ...reactHooks.configs.recommended.rules,

      // Custom rule overrides:

      // Allow target="_blank" without rel="noopener" (turned off for flexibility)
      'react/jsx-no-target-blank': 'off',

      // Warn about components that should be exported for React refresh
      // Allow constant exports (like styled components)
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },
]
