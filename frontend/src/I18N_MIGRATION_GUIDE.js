/**
 * i18n Refactoring Guide - Sprint 1
 * 
 * This guide helps you migrate from hardcoded strings and
 * simple string keys to type-safe i18n.keys usage.
 */

/**
 * BEFORE (Hardcoded strings):
 * 
 * <h2>{{ $t('events.title') }}</h2>
 * <button>{{ $t('common.create') }}</button>
 * 
 * AFTER (Type-safe):
 * 
 * <script setup>
 *   import { i18nKeys } from '@/i18n.keys'
 * </script>
 * 
 * <h2>{{ $t(i18nKeys.events.title) }}</h2>
 * <button>{{ $t(i18nKeys.common.create) }}</button>
 * 
 * Benefits:
 * ✅ IDE autocomplete: i18nKeys.events.* shows all keys
 * ✅ Type checking: Wrong keys caught at build time
 * ✅ Refactoring safe: Rename translation keys with confidence
 * ✅ Bundle: Tree-shaking removes unused strings
 */

/**
 * STEP-BY-STEP MIGRATION
 */

// Step 1: Import i18nKeys in your component
// import { i18nKeys } from '@/i18n.keys'

// Step 2: Use i18nKeys instead of string literals
// BEFORE: $t('events.title')
// AFTER:  $t(i18nKeys.events.title)

// Step 3: For dynamic keys, create helper if needed
// import { i18nKeys } from '@/i18n.keys'
// const getMessage = (key: string) => $t(key)

/**
 * QUICK REPLACEMENTS FOR COMMON PATTERNS
 */

// Pattern 1: Simple element translation
// BEFORE:
// <h1>{{ $t('events.title') }}</h1>
// AFTER:
// <h1>{{ $t(i18nKeys.events.title) }}</h1>

// Pattern 2: Button with dynamic class
// BEFORE:
// <button :title="$t('common.save')">{{ $t('common.save') }}</button>
// AFTER:
// <button :title="$t(i18nKeys.common.save)">{{ $t(i18nKeys.common.save) }}</button>

// Pattern 3: Message display
// BEFORE:
// message.value = 'Event created successfully!'
// AFTER:
// message.value = $t(i18nKeys.events.eventCreatedSuccess)

// Pattern 4: Placeholder translations
// BEFORE:
// <input :placeholder="$t('events.eventName')" />
// AFTER:
// <input :placeholder="$t(i18nKeys.events.eventName)" />

/**
 * MIGRATION CHECKLIST
 */

const migrationChecklist = {
  'LanguageSwitcher.vue': {
    status: 'compat', // Already works with string keys
    notes: 'Uses settings.language - no changes needed'
  },
  'EventsView.vue': {
    status: 'todo',
    hardcoded: [
      '"Event created successfully!"',
      '"Error creating event."',
      '"Event removed successfully!"',
      '"Error removing event."'
    ],
    plan: 'Add import + replace message assignments'
  },
  'EventCard.vue': {
    status: 'todo',
    hardcoded: [],
    plan: 'Check for any hardcoded text'
  },
  'MatchesView.vue': {
    status: 'todo',
    plan: 'Full refactor to use i18nKeys'
  },
  'PlayersView.vue': {
    status: 'todo',
    plan: 'Full refactor to use i18nKeys'
  },
  'RankingView.vue': {
    status: 'todo',
    plan: 'Full refactor to use i18nKeys'
  }
}

/**
 * VALIDATION AFTER MIGRATION
 */

// 1. No console errors about missing translations
// 2. All UI text appears correctly in both languages
// 3. Changing language switches all text correctly
// 4. No hardcoded English/Portuguese text visible
// 5. Build succeeds with no type errors

/**
 * TESTING STRATEGY
 */

// Test each component:
// 1. Navigate to component page
// 2. Switch to English (en-US)
// 3. Verify all text English
// 4. Switch to Portuguese (pt-BR)
// 5. Verify all text Portuguese
// 6. Refresh page
// 7. Verify language persists

/**
 * ESTIMATED TIMELINE
 */

// ⏱️  2-3 hours total
// - 15 min: Setup (understanding current structure)
// - 30 min: LanguageSwitcher.vue (already done)
// - 45 min: EventsView.vue + EventCard.vue
// - 45 min: MatchesView.vue + PlayersView.vue
// - 30 min: RankingView.vue + testing

/**
 * NEXT STEPS AFTER MIGRATION
 */

// 1. ✅ Create i18n.keys.ts (DONE)
// 2. 🔄 Refactor main components (IN PROGRESS)
// 3. ✅ Add tests for i18n usage
// 4. 🚀 Measure bundle size improvement (expect ~10-15% reduction)
// 5. 📝 Document best practices

export default migrationChecklist
