<template>
  <div class="matches-view">
    <h2>{{ $t(i18nKeys.matches.title) }}</h2>

    <div v-if="loading" class="loading">{{ $t(i18nKeys.common.loading) }}</div>

    <div v-else class="match-controls">
      <!-- STEP 1: Create Match -->
      <div class="create-match">
        <h3>{{ $t(i18nKeys.matches.step1) }}</h3>
        <div class="form-group">
          <label>{{ $t(i18nKeys.matches.player1) }}:</label>
          <select v-model="newMatch.player1_id" class="select-input">
            <option value="">{{ $t(i18nKeys.matches.selectPlayers) }}</option>
            <option v-for="player in players" :key="player.id" :value="player.id">
              {{ player.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>{{ $t(i18nKeys.matches.player2) }}:</label>
          <select v-model="newMatch.player2_id" class="select-input">
            <option value="">{{ $t(i18nKeys.matches.selectPlayers) }}</option>
            <option v-for="player in players" :key="player.id" :value="player.id">
              {{ player.name }}
            </option>
          </select>
        </div>

        <button @click="createMatch" class="btn-primary">{{ $t(i18nKeys.matches.createMatch) }}</button>
      </div>

      <!-- STEP 2: Add Scores -->
      <div class="add-scores" v-if="editingMatchId">
        <h3>{{ $t(i18nKeys.matches.step2) }}</h3>
        <div class="match-info">
          <strong>{{ getPlayerName(editingMatchData?.player1_id) }}</strong> vs 
          <strong>{{ getPlayerName(editingMatchData?.player2_id) }}</strong>
        </div>

        <div class="form-group">
          <label>{{ getPlayerName(editingMatchData?.player1_id) }} {{ $t(i18nKeys.matches.player1Games) }}:</label>
          <input v-model.number="editingMatchData.player1_games" type="number" min="0" class="input-field">
        </div>

        <div class="form-group">
          <label>{{ getPlayerName(editingMatchData?.player2_id) }} {{ $t(i18nKeys.matches.player2Games) }}:</label>
          <input v-model.number="editingMatchData.player2_games" type="number" min="0" class="input-field">
        </div>

        <div class="form-group">
          <label>{{ $t(i18nKeys.matches.winner) }}:</label>
          <select v-model.number="editingMatchData.winner_id" class="select-input">
            <option value="">{{ $t(i18nKeys.matches.selectPlayers) }}</option>
            <option :value="editingMatchData.player1_id">
              {{ getPlayerName(editingMatchData?.player1_id) }}
            </option>
            <option :value="editingMatchData.player2_id">
              {{ getPlayerName(editingMatchData?.player2_id) }}
            </option>
          </select>
        </div>

        <div class="buttons">
          <button @click="finishMatch" class="btn-success">{{ $t(i18nKeys.matches.finishMatch) }}</button>
          <button @click="cancelEdit" class="btn-secondary">{{ $t(i18nKeys.common.cancel) }}</button>
        </div>
      </div>

      <!-- Match Results List -->
      <div v-if="matches.length === 0 && !editingMatchId" class="empty-state">
        <p>{{ $t(i18nKeys.matches.noMatches) }}</p>
      </div>

      <div v-else-if="!editingMatchId" class="matches-list">
        <h3>{{ $t(i18nKeys.matches.matchDetails) }}</h3>
        <div v-for="match in matches" :key="match.id" class="match-item">
          <div class="match-header">
            <span class="player-name">{{ getPlayerName(match.player1_id) }}</span>
            <span class="vs">vs</span>
            <span class="player-name">{{ getPlayerName(match.player2_id) }}</span>
          </div>

          <div class="match-scores">
            <div class="game-count">
              <span class="games">{{ match.player1_games }}</span>
              <span class="dash">-</span>
              <span class="games">{{ match.player2_games }}</span>
            </div>
            <div v-if="match.games_score" class="detailed-score">
              {{ match.games_score }}
            </div>
          </div>

          <div class="match-result">
            <span v-if="match.winner_id" class="winner">
              {{ $t(i18nKeys.matches.winner) }}: <strong>{{ getPlayerName(match.winner_id) }}</strong>
            </span>
            <span v-else class="pending">{{ $t(i18nKeys.messages.loadingData) }}</span>
          </div>

          <div class="match-actions">
            <button @click="editMatch(match)" class="btn-edit">{{ $t(i18nKeys.common.edit) }}</button>
            <button @click="deleteMatch(match.id)" class="btn-delete">{{ $t(i18nKeys.common.delete) }}</button>
            <button @click="openScoresModal(match)" class="btn-scores">{{ $t(i18nKeys.matches.detailedScores) }}</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Detailed Scores -->
    <div v-if="showScoresModal && getEditingMatch()" class="modal-overlay" @click="closeScoresModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ $t(i18nKeys.matches.gamesScore) }}</h3>
          <button class="close-btn" @click="closeScoresModal">✕</button>
        </div>

        <div class="modal-body">
          <div class="match-title">
            <strong>{{ getPlayerName(getEditingMatch().player1_id) }}</strong> vs 
            <strong>{{ getPlayerName(getEditingMatch().player2_id) }}</strong>
          </div>

          <div class="form-group">
            <label>{{ $t(i18nKeys.matches.gamesScore) }} (e.g., "11-9,10-12,11-8"):</label>
            <p class="help-text">{{ $t(i18nKeys.matches.gamesScoreHelp) }}</p>
            <textarea 
              v-model="getEditingMatch().games_score" 
              :placeholder="$t(i18nKeys.matches.gamesScoreHelp)"
              class="textarea-input"
              rows="3"
            ></textarea>
          </div>

          <div class="modal-actions">
            <button @click="saveDetailedScores" class="btn-success">{{ $t(i18nKeys.common.save) }}</button>
            <button @click="closeScoresModal" class="btn-secondary">{{ $t(i18nKeys.common.cancel) }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import { i18nKeys } from "@/i18n.keys";
import jogosService from "../services/jogos";
import playersService from "../services/players";

const route = useRoute();
const { t } = useI18n();
const eventId = route.params.id;
const matches = ref([]);
const players = ref([]);
const loading = ref(true);
const editingMatchId = ref(null);
const editingMatchData = ref({});
const showScoresModal = ref(false);
const editingScoresMatchId = ref(null);

const newMatch = ref({
  player1_id: "",
  player2_id: "",
  player1_games: 0,
  player2_games: 0,
  games_score: "",
  winner_id: "",
});

const getPlayerName = (playerId) => {
  const numId = typeof playerId === 'string' ? parseInt(playerId) : playerId;
  const player = players.value.find((p) => p.id === numId);
  return player ? player.name : "Unknown";
};

const createMatch = async () => {
  if (!newMatch.value.player1_id || !newMatch.value.player2_id) {
    alert(t(i18nKeys.matches.selectPlayers));
    return;
  }

  if (newMatch.value.player1_id === newMatch.value.player2_id) {
    alert(t(i18nKeys.validation.differentPlayers));
    return;
  }

  try {
    const res = await jogosService.create({
      event_id: parseInt(eventId),
      player1_id: parseInt(newMatch.value.player1_id),
      player2_id: parseInt(newMatch.value.player2_id),
      player1_games: 0,
      player2_games: 0,
    });
    
    // Open edit form for the new match
    editingMatchId.value = res.data.id;
    editingMatchData.value = { ...res.data };
    newMatch.value = { 
      player1_id: "", 
      player2_id: "", 
      player1_games: 0,
      player2_games: 0,
      games_score: "",
      winner_id: "" 
    };
  } catch (err) {
    console.error("Failed to create match:", err);
    alert(t(i18nKeys.messages.errorSavingData));
  }
};

const editMatch = (match) => {
  editingMatchId.value = match.id;
  editingMatchData.value = { ...match };
};

const cancelEdit = () => {
  editingMatchId.value = null;
  editingMatchData.value = {};
};

const finishMatch = async () => {
  if (!editingMatchData.value.winner_id) {
    alert(t(i18nKeys.validation.selectWinner));
    return;
  }

  try {
    const updateData = {
      player1_games: parseInt(editingMatchData.value.player1_games),
      player2_games: parseInt(editingMatchData.value.player2_games),
      games_score: editingMatchData.value.games_score || null,
      winner_id: parseInt(editingMatchData.value.winner_id),
      finished: true,
    };

    const res = await jogosService.update(editingMatchId.value, updateData);
    
    // Update the match in the list
    const index = matches.value.findIndex(m => m.id === editingMatchId.value);
    if (index >= 0) {
      matches.value[index] = res.data;
    } else {
      matches.value.push(res.data);
    }
    
    editingMatchId.value = null;
    editingMatchData.value = {};
    alert(t(i18nKeys.matches.matchUpdatedSuccess));
  } catch (err) {
    console.error("Failed to finish match:", err);
    alert(t(i18nKeys.messages.errorSavingData));
  }
};

const deleteMatch = async (matchId) => {
  if (!confirm(t(i18nKeys.messages.confirmDelete))) return;
  try {
    await jogosService.delete(matchId);
    matches.value = matches.value.filter((m) => m.id !== matchId);
  } catch (err) {
    console.error("Failed to delete match:", err);
    alert(t(i18nKeys.messages.errorDeletingData));
  }
};

const openScoresModal = (match) => {
  editingScoresMatchId.value = match.id;
  showScoresModal.value = true;
};

const closeScoresModal = () => {
  showScoresModal.value = false;
  editingScoresMatchId.value = null;
};

const getEditingMatch = () => {
  return matches.value.find(m => m.id === editingScoresMatchId.value);
};

const saveDetailedScores = async () => {
  const match = getEditingMatch();
  if (!match) return;

  try {
    const updateData = {
      games_score: match.games_score || null,
    };

    const res = await jogosService.update(match.id, updateData);
    
    // Update the match in the list
    const index = matches.value.findIndex(m => m.id === match.id);
    if (index >= 0) {
      matches.value[index] = res.data;
    }
    
    closeScoresModal();
    alert(t(i18nKeys.common.success));
  } catch (err) {
    console.error("Failed to save scores:", err);
    alert(t(i18nKeys.messages.errorSavingData));
  }
};

const fetchData = async () => {
  loading.value = true;
  try {
    const [matchRes, playerRes] = await Promise.all([
      jogosService.getEventMatches(eventId),
      playersService.list(eventId),
    ]);
    matches.value = matchRes.data || [];
    players.value = playerRes.data || [];
  } catch (err) {
    console.error("Failed to load matches:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>

<style scoped>
.matches-view {
  max-width: 900px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 2em;
  color: #666;
}

.match-controls {
  display: flex;
  flex-direction: column;
  gap: 2em;
}

.create-match,
.add-scores {
  background: var(--color-background-soft);
  padding: 1.5em;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0002;
}

.create-match h3,
.add-scores h3 {
  margin-top: 0;
  margin-bottom: 1.5em;
  color: var(--color-text);
}

.form-group {
  margin-bottom: 1.2em;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5em;
  color: var(--color-text);
}

.select-input,
.input-field {
  padding: 0.7em;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 1em;
  background: white;
  cursor: pointer;
  font-family: inherit;
}

.input-field {
  cursor: text;
}

.select-input:hover,
.input-field:hover {
  border-color: #667eea;
}

.select-input:focus,
.input-field:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.match-info {
  background: var(--color-background);
  padding: 1em;
  border-radius: 4px;
  margin-bottom: 1em;
  font-weight: 500;
  text-align: center;
  border-left: 4px solid #667eea;
}

.buttons {
  display: flex;
  gap: 1em;
  margin-top: 1.5em;
}

.btn-primary,
.btn-success,
.btn-secondary,
.btn-edit,
.btn-delete {
  padding: 0.8em 1.5em;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary,
.btn-success {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover,
.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
}

.btn-secondary:hover {
  background: #d0d0d0;
}

.btn-edit {
  background: #4caf50;
  color: white;
  padding: 0.5em 1em;
  font-size: 0.9em;
}

.btn-edit:hover {
  background: #45a049;
}

.btn-delete {
  background: #ff6b6b;
  color: white;
  padding: 0.5em 1em;
  font-size: 0.9em;
}

.btn-delete:hover {
  background: #ff5252;
}

.btn-scores {
  background: #2196f3;
  color: white;
  padding: 0.5em 1em;
  font-size: 0.9em;
}

.btn-scores:hover {
  background: #1976d2;
}

.empty-state {
  text-align: center;
  padding: 2em;
  color: #666;
}

.matches-list {
  background: var(--color-background-soft);
  padding: 1.5em;
  border-radius: 8px;
}

.matches-list h3 {
  margin-top: 0;
  margin-bottom: 1.5em;
}

.match-item {
  background: var(--color-background);
  padding: 1.2em;
  margin-bottom: 1.2em;
  border-radius: 6px;
  border-left: 4px solid #667eea;
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.match-item:hover {
  box-shadow: 0 2px 8px #0002;
}

.match-header {
  display: flex;
  align-items: center;
  gap: 1em;
  font-weight: 600;
  font-size: 1.05em;
}

.player-name {
  color: #667eea;
}

.vs {
  color: #999;
  font-size: 0.9em;
}

.match-scores {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
  background: linear-gradient(135deg, #f5f5f5 0%, #efefef 100%);
  padding: 1em;
  border-radius: 4px;
}

.game-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  font-size: 1.3em;
  font-weight: 700;
}

.games {
  min-width: 30px;
  text-align: center;
}

.dash {
  color: #999;
}

.detailed-score {
  text-align: center;
  color: #666;
  font-size: 0.9em;
  font-family: monospace;
}

.match-result {
  text-align: center;
  font-weight: 500;
}

.winner {
  color: #2e7d32;
}

.pending {
  color: #ff9800;
  font-style: italic;
}

.match-actions {
  display: flex;
  gap: 0.5em;
  justify-content: flex-end;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5em;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  color: var(--color-text);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5em;
}

.match-title {
  text-align: center;
  font-weight: 600;
  margin-bottom: 1.5em;
  color: var(--color-text);
}

.help-text {
  font-size: 0.9em;
  color: #999;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.textarea-input {
  width: 100%;
  padding: 0.8em;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-family: monospace;
  font-size: 1em;
  resize: vertical;
}

.textarea-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1em;
  margin-top: 1.5em;
}

@media (max-width: 768px) {
  .match-item {
    gap: 0.8em;
  }

  .match-header {
    flex-direction: column;
    text-align: center;
  }

  .buttons {
    flex-direction: column;
  }

  .buttons button {
    width: 100%;
  }
}
</style>
