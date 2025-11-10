<template>
  <div class="match-history-view">
    <h2>Match History</h2>
    
    <div v-if="loading" class="loading">Loading matches...</div>
    
    <div v-else-if="matches.length === 0" class="empty-state">
      <p>No matches played yet</p>
    </div>
    
    <div v-else class="matches-container">
      <div class="match-card" v-for="match in matches" :key="match.id">
        <div class="match-info">
          <div class="date-time">
            <span class="date">{{ formatDate(match.date) }}</span>
          </div>
        </div>
        
        <div class="match-result">
          <div class="player player-1" :class="{ winner: match.winner_id === match.player_1_id }">
            <div class="player-name">{{ getPlayerName(match.player_1_id) }}</div>
            <div class="elo-change" :class="{ gain: match.winner_id === match.player_1_id, loss: match.winner_id !== match.player_1_id }">
              {{ getEloChange(match, match.player_1_id) }}
            </div>
          </div>
          
          <div class="vs">vs</div>
          
          <div class="player player-2" :class="{ winner: match.winner_id === match.player_2_id }">
            <div class="player-name">{{ getPlayerName(match.player_2_id) }}</div>
            <div class="elo-change" :class="{ gain: match.winner_id === match.player_2_id, loss: match.winner_id !== match.player_2_id }">
              {{ getEloChange(match, match.player_2_id) }}
            </div>
          </div>
        </div>
        
        <div class="match-meta">
          <span class="status" :class="getStatusClass(match)">
            {{ getStatus(match) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import jogosService from "../services/jogos";
import playersService from "../services/players";

const route = useRoute();
const eventId = route.params.id;
const matches = ref([]);
const players = ref([]);
const loading = ref(true);

const playerMap = computed(() => {
  const map = {};
  players.value.forEach(p => {
    map[p.id] = p;
  });
  return map;
});

const fetchData = async () => {
  loading.value = true;
  try {
    const [matchRes, playerRes] = await Promise.all([
      jogosService.getEventMatches(eventId),
      playersService.getEventPlayers(eventId)
    ]);
    
    matches.value = (matchRes.data || []).reverse();
    players.value = playerRes.data || [];
  } catch (err) {
    console.error("Failed to load match history:", err);
  } finally {
    loading.value = false;
  }
};

const getPlayerName = (playerId) => {
  const player = playerMap.value[playerId];
  return player ? player.name : "Unknown";
};

const getEloChange = (match, playerId) => {
  const player = playerMap.value[playerId];
  if (!player || !player.elo_rating) return "±0";
  
  const isWinner = match.winner_id === playerId;
  const change = isWinner ? 20 : -10;
  
  return isWinner ? `+${change}` : `${change}`;
};

const getStatus = (match) => {
  const winner = playerMap.value[match.winner_id];
  return winner ? `${winner.name} won` : "Unknown";
};

const getStatusClass = (match) => {
  return "completed";
};

const formatDate = (dateStr) => {
  if (!dateStr) return "Unknown";
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  });
};

onMounted(fetchData);
</script>

<style scoped>
.match-history-view {
  max-width: 800px;
  margin: 0 auto;
}

.loading,
.empty-state {
  text-align: center;
  padding: 2em;
  color: var(--color-text-secondary, #666);
  font-size: 1.1em;
}

.matches-container {
  display: flex;
  flex-direction: column;
  gap: 1.5em;
}

.match-card {
  background: var(--color-background-soft);
  border-radius: 8px;
  padding: 1.5em;
  box-shadow: 0 2px 8px #0002;
  transition: transform 0.2s, box-shadow 0.2s;
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px #0004;
}

.match-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
  padding-bottom: 1em;
  border-bottom: 1px solid var(--color-border);
}

.date-time {
  display: flex;
  gap: 1em;
  font-size: 0.9em;
  color: var(--color-text-secondary);
}

.date {
  font-weight: 500;
}

.match-result {
  display: flex;
  align-items: center;
  gap: 2em;
  margin-bottom: 1em;
  padding: 1em 0;
}

.player {
  flex: 1;
  text-align: center;
  padding: 1em;
  border-radius: 6px;
  background: var(--color-background);
  transition: background 0.2s;
}

.player.winner {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

.player-name {
  font-weight: 600;
  font-size: 1.05em;
  margin-bottom: 0.5em;
}

.elo-change {
  font-size: 0.95em;
  font-weight: 600;
}

.elo-change.gain {
  color: #2e7d32;
}

.elo-change.loss {
  color: #c62828;
}

.vs {
  color: var(--color-text-secondary);
  font-weight: 600;
  padding: 0 1em;
}

.match-meta {
  display: flex;
  justify-content: center;
  gap: 1em;
}

.status {
  display: inline-block;
  padding: 0.4em 0.8em;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: 600;
  background: #e3f2fd;
  color: #1565c0;
}

.status.completed {
  background: #f3e5f5;
  color: #6a1b9a;
}

@media (max-width: 768px) {
  .match-result {
    gap: 1em;
    font-size: 0.9em;
  }

  .player {
    padding: 0.75em;
  }

  .vs {
    padding: 0 0.5em;
  }
}
</style>
