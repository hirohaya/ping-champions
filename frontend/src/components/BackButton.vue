<template>
  <div class="back-button-container">
    <button @click="goBack" class="back-button" :title="$t('navigation.goBack')">
      ← {{ $t('navigation.back') }}
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { i18nKeys } from '@/i18n.keys';

const router = useRouter();

const goBack = () => {
  if (window.history.length > 1) {
    router.back();
  } else {
    router.push('/');
  }
};
</script>

<style scoped>
.back-button-container {
  margin-bottom: 1.5em;
  padding-bottom: 1em;
  border-bottom: 1px solid var(--color-border, #e0e0e0);
}

.back-button {
  background: var(--color-primary, #42b983);
  color: white;
  border: none;
  padding: 0.6em 1.2em;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95em;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.back-button:hover {
  background: var(--color-primary-hover, #3a9970);
  transform: translateX(-2px);
}

.back-button:active {
  transform: translateX(-1px);
  opacity: 0.9;
}

@media (max-width: 768px) {
  .back-button-container {
    margin-bottom: 1em;
    padding-bottom: 0.8em;
  }

  .back-button {
    padding: 0.5em 1em;
    font-size: 0.9em;
  }
}
</style>
