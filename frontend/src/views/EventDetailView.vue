<template>
  <div class="event-detail-container">
    <!-- Event Overview Section -->
    <EventOverview />

    <!-- Navigation Links -->
    <div class="navigation-links" style="margin: 2rem 0; padding: 1rem; background: var(--color-background-soft); border-radius: 0.8rem;">
      <p style="margin: 0 0 1rem 0; color: var(--color-text);">{{ $t('events.manageEvent') }}</p>
      <div class="link-group">
        <router-link :to="`/events/${$route.params.id}/players`" class="nav-link">
          {{ $t('events.managePlayers') }}
        </router-link>
        <router-link :to="`/events/${$route.params.id}/matches`" class="nav-link">
          {{ $t('events.manageMatches') }}
        </router-link>
      </div>
    </div>

    <!-- Back Button -->
    <router-link to="/events" class="back-link">
      ← {{ $t('common.back') }}
    </router-link>

    <!-- Nested Routes -->
    <router-view />
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

.navigation-links {
  margin: 2rem 0;
  padding: 1rem;
  background: var(--color-background-soft);
  border-radius: 0.8rem;
  border-left: 4px solid #42b983;
}

.navigation-links p {
  margin: 0 0 1rem 0;
  color: var(--color-text);
  font-weight: 500;
}

.link-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.nav-link {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-link:hover {
  background: #359268;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.3);
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

  .link-group {
    flex-direction: column;
  }

  .nav-link {
    width: 100%;
    text-align: center;
  }
}
</style>
