<template>
  <div class="player-statistics">
    <h3>{{ player.name }} - Statistics</h3>
    
    <div class="stats-grid">
      <!-- Elo Rating -->
      <div class="stat-box">
        <div class="stat-label">Current Elo</div>
        <div class="stat-value elo">{{ formatElo(player.elo_rating) }}</div>
        <div class="stat-description">
          <span :class="{ gained: eloChange > 0, lost: eloChange < 0 }">
            {{ eloChange > 0 ? "+" : "" }}{{ eloChange }}
          </span>
          from starting rating
        </div>
      </div>
      
      <!-- Win/Loss Record -->
      <div class="stat-box">
        <div class="stat-label">Record</div>
        <div class="stat-value record">{{ player.score }}-{{ calculateLosses() }}</div>
        <div class="stat-description">Wins-Losses</div>
      </div>
      
      <!-- Win Rate -->
      <div class="stat-box">
        <div class="stat-label">Win Rate</div>
        <div class="stat-value">{{ formatWinRate() }}</div>
        <div class="stat-description">{{ calculateMatches() }} total matches</div>
      </div>
      
      <!-- Ranking -->
      <div class="stat-box">
        <div class="stat-label">Current Rank</div>
        <div class="stat-value rank">#{{ player.ranking || "—" }}</div>
        <div class="stat-description">Among tournament players</div>
      </div>
    </div>
    
    <!-- Elo Progress Bar -->
    <div class="elo-progress">
      <div class="progress-label">
        <span>Elo Progress</span>
        <span class="starting-elo">Starting: 1600</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: getProgressWidth() }"></div>
      </div>
      <div class="progress-stats">
        <span class="min">1600</span>
        <span class="current">{{ formatElo(player.elo_rating) }}</span>
        <span class="max" v-if="getMaxElo() > 1600">{{ getMaxElo() }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  player: {
    type: Object,
    required: true,
    default: () => ({
      name: "",
      elo_rating: 1600,
      score: 0,
      ranking: null,
      losses: 0
    })
  }
});

const formatElo = (elo) => {
  if (!elo) return "1600";
  return Math.round(elo).toString();
};

const calculateLosses = () => {
  return props.player.losses || Math.max(0, calculateMatches() - (props.player.score || 0));
};

const calculateMatches = () => {
  return (props.player.score || 0) + calculateLosses();
};

const calculateWinRate = () => {
  const total = calculateMatches();
  if (total === 0) return 0;
  return ((props.player.score || 0) / total) * 100;
};

const formatWinRate = () => {
  return calculateWinRate().toFixed(1) + "%";
};

const eloChange = computed(() => {
  const current = props.player.elo_rating || 1600;
  return Math.round(current - 1600);
});

const getMaxElo = () => {
  const current = props.player.elo_rating || 1600;
  return Math.max(1600, Math.round(current) + 100);
};

const getProgressWidth = () => {
  const current = props.player.elo_rating || 1600;
  const max = getMaxElo();
  const min = 1600;
  
  if (max === min) return "0%";
  
  const progress = ((current - min) / (max - min)) * 100;
  return Math.min(100, Math.max(0, progress)) + "%";
};
</script>

<style scoped>
.player-statistics {
  background: var(--color-background-soft);
  border-radius: 8px;
  padding: 1.5em;
  box-shadow: 0 2px 8px #0002;
}

.player-statistics h3 {
  margin-top: 0;
  margin-bottom: 1.5em;
  color: var(--color-text);
  font-size: 1.3em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1.5em;
  margin-bottom: 2em;
}

.stat-box {
  text-align: center;
  padding: 1em;
  background: var(--color-background);
  border-radius: 6px;
  border-left: 4px solid #667eea;
  transition: transform 0.2s;
}

.stat-box:hover {
  transform: translateY(-2px);
}

.stat-label {
  display: block;
  font-size: 0.85em;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.stat-value {
  display: block;
  font-size: 1.8em;
  font-weight: 700;
  margin-bottom: 0.5em;
  color: var(--color-text);
}

.stat-value.elo {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-value.record {
  color: #2e7d32;
}

.stat-value.rank {
  color: #6a1b9a;
}

.stat-description {
  font-size: 0.8em;
  color: var(--color-text-secondary);
}

.stat-description .gained {
  color: #2e7d32;
  font-weight: 600;
}

.stat-description .lost {
  color: #c62828;
  font-weight: 600;
}

.elo-progress {
  margin-top: 2em;
  padding-top: 2em;
  border-top: 1px solid var(--color-border);
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1em;
  font-weight: 600;
}

.starting-elo {
  font-size: 0.85em;
  color: var(--color-text-secondary);
  font-weight: 400;
}

.progress-bar {
  height: 8px;
  background: var(--color-background);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5em;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.8em;
  color: var(--color-text-secondary);
}

.min {
  font-weight: 600;
}

.current {
  font-weight: 700;
  color: var(--color-text);
}

.max {
  font-weight: 600;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1em;
  }

  .stat-box {
    padding: 0.75em;
  }

  .stat-value {
    font-size: 1.4em;
  }
}
</style>
