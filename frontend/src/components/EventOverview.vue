<template>
  <div class="event-overview">
    <!-- Loading state -->
    <div v-if="loading" class="loading">{{ $t('common.loading') }}</div>

    <!-- Error state -->
    <div v-else-if="error" class="error">
      {{ $t('messages.errorLoadingData') }}: {{ error }}
    </div>

    <!-- Event overview display -->
    <div v-else-if="event" class="overview-container">
      <div class="overview-header">
        <h2>{{ event.name }}</h2>
        <span class="event-status" :class="{ active: event.active }">
          {{ event.active ? $t('events.active') : $t('events.inactive') }}
        </span>
      </div>

      <div class="overview-grid">
        <!-- Event details card -->
        <div class="overview-card details-card">
          <h3>{{ $t('events.eventDetails') }}</h3>
          <div class="details-list">
            <div class="detail-item">
              <span class="label">{{ $t('events.date') }}:</span>
              <span class="value">{{ formatDate(event.date) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">{{ $t('events.time') }}:</span>
              <span class="value">{{ event.time }}</span>
            </div>
          </div>
        </div>

        <!-- Statistics card -->
        <div class="overview-card stats-card">
          <h3>{{ $t('events.statistics') }}</h3>
          <div class="stats-list">
            <div class="stat-item">
              <span class="label">{{ $t('navigation.players') }}</span>
              <span class="stat-value">{{ stats.players }}</span>
            </div>
            <div class="stat-item">
              <span class="label">{{ $t('navigation.matches') }}</span>
              <span class="stat-value">{{ stats.matches }}</span>
            </div>
          </div>
        </div>

        <!-- Quick actions card -->
        <div class="overview-card actions-card">
          <h3>{{ $t('common.actions') }}</h3>
          <div class="actions-list">
            <router-link
              :to="`/events/${event.id}/players`"
              class="action-btn players-btn"
            >
              {{ $t('navigation.players') }}
            </router-link>
            <router-link
              :to="`/events/${event.id}/matches`"
              class="action-btn matches-btn"
            >
              {{ $t('navigation.matches') }}
            </router-link>
            <router-link
              :to="`/ranking?event=${event.id}`"
              class="action-btn ranking-btn"
            >
              {{ $t('navigation.ranking') }}
            </router-link>
          </div>
        </div>
      </div>

      <!-- Top players preview -->
      <div class="overview-preview">
        <h3>{{ $t('events.topPlayers') }}</h3>
        <div v-if="topPlayers.length > 0" class="players-preview-list">
          <div
            v-for="(player, index) in topPlayers"
            :key="player.id"
            class="player-preview"
          >
            <span class="position">{{ index + 1 }}</span>
            <span class="name">{{ player.name }}</span>
            <span class="elo">{{ player.current_elo || player.initial_elo }}</span>
          </div>
        </div>
        <div v-else class="no-data">
          {{ $t('messages.noDataToDisplay') }}
        </div>
      </div>
    </div>

    <!-- No event found -->
    <div v-else class="no-data">
      {{ $t('events.noEvents') }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import eventsService from '../services/events';
import playersService from '../services/players';
import partidasService from '../services/partidas';

const { t } = useI18n();
const route = useRoute();

const event = ref(null);
const loading = ref(true);
const error = ref(null);
const stats = ref({ players: 0, matches: 0 });
const topPlayers = ref([]);

const formatDate = (dateString) => {
  if (!dateString) return '';
  const [year, month, day] = dateString.split('-');
  return `${day}/${month}/${year}`;
};

const loadEventDetails = async () => {
  try {
    loading.value = true;
    error.value = null;

    const eventId = route.params.id;

    // Load event details
    const eventRes = await eventsService.get(eventId);
    event.value = eventRes.data;

    // Load players for this event
    const playersRes = await playersService.list(eventId);
    const players = playersRes.data;
    stats.value.players = players.length;
    topPlayers.value = players
      .slice()
      .sort((a, b) => (b.current_elo || b.initial_elo) - (a.current_elo || a.initial_elo))
      .slice(0, 5);

    // Load matches for this event
    const matchesRes = await partidasService.listarPorEvento(eventId);
    stats.value.matches = matchesRes.data.length;
  } catch (err) {
    error.value = err.message || 'Failed to load event details';
    console.error('Error loading event:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(loadEventDetails);
</script>

<style scoped>
.event-overview {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.loading,
.error,
.no-data {
  padding: 2rem;
  text-align: center;
  color: var(--color-text);
  background: var(--color-background-soft);
  border-radius: 0.8rem;
  margin-bottom: 1.5rem;
}

.error {
  background: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

.overview-container {
  width: 100%;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-border);
}

.overview-header h2 {
  margin: 0;
  color: var(--color-heading);
  font-size: 1.8rem;
}

.event-status {
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: bold;
  background: #fee;
  color: #c33;
}

.event-status.active {
  background: #efe;
  color: #3c3;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.overview-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.overview-card h3 {
  margin: 0 0 1rem 0;
  color: var(--color-heading);
  font-size: 1.1rem;
  border-bottom: 2px solid var(--color-border);
  padding-bottom: 0.5rem;
}

.details-list,
.stats-list,
.actions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item,
.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.detail-item .label,
.stat-item .label {
  font-weight: 500;
  color: var(--color-text);
}

.detail-item .value {
  font-weight: bold;
  color: var(--color-heading);
}

.stat-value {
  display: inline-block;
  min-width: 2rem;
  text-align: right;
  font-size: 1.3rem;
  font-weight: bold;
  color: #42b983;
}

.actions-list {
  gap: 0.5rem;
}

.action-btn {
  display: block;
  padding: 0.75rem 1.2rem;
  text-align: center;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  color: white;
}

.action-btn.players-btn {
  background: #42b983;
}

.action-btn.players-btn:hover {
  background: #359268;
  transform: translateY(-2px);
}

.action-btn.matches-btn {
  background: #4a90e2;
}

.action-btn.matches-btn:hover {
  background: #2e5c8a;
  transform: translateY(-2px);
}

.action-btn.ranking-btn {
  background: #f5a623;
}

.action-btn.ranking-btn:hover {
  background: #d67e1d;
  transform: translateY(-2px);
}

.overview-preview {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-top: 2rem;
}

.overview-preview h3 {
  margin: 0 0 1rem 0;
  color: var(--color-heading);
  font-size: 1.1rem;
}

.players-preview-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.player-preview {
  display: grid;
  grid-template-columns: 2rem 1fr 4rem;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--color-background);
  border-radius: 0.5rem;
  border-left: 4px solid #42b983;
}

.player-preview .position {
  font-weight: bold;
  font-size: 1rem;
  color: #42b983;
  text-align: center;
}

.player-preview .name {
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.player-preview .elo {
  text-align: right;
  font-weight: bold;
  color: var(--color-heading);
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }

  .overview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .player-preview {
    grid-template-columns: 2rem 1fr;
    gap: 0.75rem;
  }

  .player-preview .elo {
    grid-column: 2;
    text-align: left;
  }
}
</style>
