<template>
  <div class="ranking-view">
    <h2>{{ $t(i18nKeys.ranking.title) }}</h2>
    
    <div v-if="loading" class="loading">{{ $t(i18nKeys.common.loading) }}</div>
    
    <div v-else-if="players.length === 0" class="empty-state">
      <p>{{ $t(i18nKeys.ranking.noMatches) }}</p>
    </div>
    
    <div v-else class="ranking-container">
      <div class="controls">
        <label>
          <input type="checkbox" v-model="sortByElo" />
          {{ $t(i18nKeys.ranking.elo) }}
        </label>
      </div>
      
      <table class="ranking-table">
        <thead>
          <tr>
            <th class="rank">#</th>
            <th class="name">{{ $t(i18nKeys.ranking.player) }}</th>
            <th class="elo">{{ $t(i18nKeys.ranking.elo) }}</th>
            <th class="wins">{{ $t(i18nKeys.players.wins) }}</th>
            <th class="losses">{{ $t(i18nKeys.players.losses) }}</th>
            <th class="winrate">{{ $t(i18nKeys.players.winRate) }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(player, index) in sortedPlayers" :key="player.id" class="player-row">
            <td class="rank">
              <span class="rank-badge" :class="getRankClass(index)">{{ index + 1 }}</span>
            </td>
            <td class="name">{{ player.name }}</td>
            <td class="elo">
              <span class="elo-badge">{{ formatElo(player.elo_rating) }}</span>
            </td>
            <td class="wins">{{ player.score }}</td>
            <td class="losses">{{ calculateLosses(player) }}</td>
            <td class="winrate">
              <span class="winrate-badge">{{ formatWinRate(player) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { i18nKeys } from "@/i18n.keys";
import rankingService from "../services/ranking";

const route = useRoute();
const eventId = route.params.id;
const players = ref([]);
const loading = ref(true);
const sortByElo = ref(false);

const fetchRanking = async () => {
  // If no eventId, show empty state
  if (!eventId) {
    loading.value = false;
    return;
  }
  
  loading.value = true;
  try {
    const res = await rankingService.getEventRanking(eventId);
    if (res.data && res.data.entries) {
      players.value = res.data.entries;
    }
  } catch (err) {
    console.error("Failed to load ranking:", err);
  } finally {
    loading.value = false;
  }
};

const sortedPlayers = computed(() => {
  let sorted = [...players.value];
  
  if (sortByElo.value) {
    sorted.sort((a, b) => {
      const eloA = a.elo_rating || 1600;
      const eloB = b.elo_rating || 1600;
      return eloB - eloA;
    });
  } else {
    sorted.sort((a, b) => {
      const winRateA = calculateWinRate(a);
      const winRateB = calculateWinRate(b);
      if (winRateA !== winRateB) return winRateB - winRateA;
      return (b.score || 0) - (a.score || 0);
    });
  }
  
  return sorted;
});

const formatElo = (elo) => {
  if (!elo) return "1600";
  return Math.round(elo).toString();
};

const calculateLosses = (player) => {
  const totalMatches = (player.score || 0) + (player.losses || 0);
  return Math.max(0, totalMatches - (player.score || 0));
};

const calculateWinRate = (player) => {
  const wins = player.score || 0;
  const losses = calculateLosses(player);
  const total = wins + losses;
  return total === 0 ? 0 : (wins / total) * 100;
};

const formatWinRate = (player) => {
  const rate = calculateWinRate(player);
  return rate.toFixed(1) + "%";
};

const getRankClass = (index) => {
  if (index === 0) return "gold";
  if (index === 1) return "silver";
  if (index === 2) return "bronze";
  return "";
};

onMounted(fetchRanking);
</script>

<style scoped>
.ranking-view {
  max-width: 900px;
  margin: 0 auto;
}

.loading,
.empty-state {
  text-align: center;
  padding: 2em;
  color: var(--color-text-secondary, #666);
  font-size: 1.1em;
}

.controls {
  margin-bottom: 1.5em;
  display: flex;
  gap: 1em;
}

.controls label {
  display: flex;
  align-items: center;
  gap: 0.5em;
  cursor: pointer;
  font-weight: 500;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-background-soft);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px #0002;
}

.ranking-table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.ranking-table th {
  padding: 1em;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #667eea;
}

.ranking-table td {
  padding: 0.8em 1em;
  border-bottom: 1px solid var(--color-border);
}

.ranking-table tbody tr:hover {
  background: var(--color-background-mute);
}

.ranking-table tbody tr:last-child td {
  border-bottom: none;
}

.rank {
  text-align: center;
  width: 60px;
}

.rank-badge {
  display: inline-block;
  width: 32px;
  height: 32px;
  line-height: 32px;
  text-align: center;
  border-radius: 50%;
  background: #e0e0e0;
  color: #333;
  font-weight: 600;
}

.rank-badge.gold {
  background: #ffd700;
  color: #333;
}

.rank-badge.silver {
  background: #c0c0c0;
  color: #333;
}

.rank-badge.bronze {
  background: #cd7f32;
  color: white;
}

.name {
  font-weight: 500;
  min-width: 150px;
}

.elo {
  text-align: center;
  min-width: 120px;
}

.elo-badge {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.4em 0.8em;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95em;
}

.wins,
.losses {
  text-align: center;
  min-width: 70px;
}

.winrate {
  text-align: center;
  min-width: 100px;
}

.winrate-badge {
  display: inline-block;
  background: #e8f5e9;
  color: #2e7d32;
  padding: 0.4em 0.8em;
  border-radius: 6px;
  font-weight: 600;
  min-width: 50px;
}

@media (max-width: 768px) {
  .ranking-table {
    font-size: 0.9em;
  }

  .ranking-table th,
  .ranking-table td {
    padding: 0.6em 0.4em;
  }

  .name {
    min-width: 100px;
  }
}
</style>
