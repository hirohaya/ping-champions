<template>
  <div class="event-detail-container">
    <!-- Event Overview Section -->
    <EventOverview />

    <!-- Back Button -->
    <router-link to="/events" class="back-link">
      ← {{ $t('common.back') }}
    </router-link>
  </div>
</template>

<script setup>
import EventOverview from '../components/EventOverview.vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<style scoped>
.event-detail-container {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.back-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  color: var(--color-text);
  text-decoration: none;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.back-link:hover {
  background: var(--color-background-soft);
  color: var(--color-heading);
}

@media (max-width: 768px) {
  .event-detail-container {
    padding: 0.5rem;
  }
}
</style>
