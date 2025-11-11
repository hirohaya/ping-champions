<template>
  <div class="language-switcher">
    <select
      v-model="currentLocale"
      @change="changeLocale"
      class="locale-select"
      :title="$t('settings.language')"
    >
      <option
        v-for="locale in availableLocales"
        :key="locale.code"
        :value="locale.code"
      >
        {{ locale.name }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLocale, getAvailableLocales } from '@/i18n'

const { locale, t } = useI18n()
const currentLocale = ref(locale.value)
const availableLocales = getAvailableLocales()
const isChanging = ref(false)

const changeLocale = () => {
  // Prevent multiple changes while processing
  if (isChanging.value) return
  
  isChanging.value = true
  const newLocale = currentLocale.value
  
  // Save the new locale
  setLocale(newLocale)
  
  // Show loading message and reload after a brief delay
  setTimeout(() => {
    // Alert user about language change
    alert(t('messages.languageChanged') || `Language changed to ${availableLocales.find(l => l.code === newLocale)?.name}`)
    
    // Reload the page to ensure all text updates
    window.location.reload()
  }, 300)
}

// Watch for external changes
watch(() => locale.value, (newLocale) => {
  currentLocale.value = newLocale
})
</script>

<style scoped>
.language-switcher {
  display: flex;
  align-items: center;
  gap: 8px;
}

.locale-select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.locale-select:hover {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.locale-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}
</style>
