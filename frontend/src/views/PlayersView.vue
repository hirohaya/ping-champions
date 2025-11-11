<template>
  <div class="players-view">
    <h2>{{ $t(i18nKeys.players.title) }}</h2>
    
    <!-- Button to open modal -->
    <div class="players-header">
      <button @click="openModal" class="btn-add-player">
        ➕ {{ $t(i18nKeys.players.registerPlayer) }}
      </button>
    </div>

    <!-- Modal Overlay -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ $t(i18nKeys.players.registerPlayer) }}</h3>
          <button class="modal-close" @click="closeModal">✕</button>
        </div>
        <form @submit.prevent="createPlayer" class="player-form">
          <div class="form-group">
            <label :for="'playerNameInput'">{{ $t(i18nKeys.players.playerName) }}</label>
            <input
              id="playerNameInput"
              v-model="name"
              :placeholder="$t(i18nKeys.players.playerName)"
              class="form-input"
              required
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">{{ $t(i18nKeys.common.create) }}</button>
            <button type="button" class="btn-cancel" @click="closeModal">{{ $t(i18nKeys.common.cancel) }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Players List -->
    <div class="players-list">
      <div v-if="players.length === 0" class="empty-state">
        <p>{{ $t(i18nKeys.players.noPlayers) }}</p>
      </div>
      <div v-for="player in players" v-else :key="player.id" class="player-card">
        <div class="player-info">
          <span v-if="editId !== player.id" class="player-name">{{
            player.name
          }}</span>
          <input
            v-else
            v-model="editName"
            class="edit-input"
            @keyup.enter="saveEdit(player)"
            @blur="cancelEdit"
          />
          <div class="player-stats">
            <div class="stat-item">
              <span class="stat-label">{{ $t(i18nKeys.players.eloRating) }}:</span>
              <span class="stat-value elo-rating">{{ formatElo(player.elo_rating) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">{{ $t(i18nKeys.players.wins) }}:</span>
              <span class="stat-value wins">{{ player.score }}</span>
            </div>
          </div>
        </div>
        <div class="player-actions">
          <button
            v-if="editId !== player.id"
            :title="$t(i18nKeys.common.edit)"
            class="icon-btn"
            @click="startEdit(player)"
          >
            ✏️
          </button>
          <button
            v-if="editId === player.id"
            :title="$t(i18nKeys.common.save)"
            class="icon-btn"
            @click="saveEdit(player)"
          >
            💾
          </button>
          <button
            v-if="editId === player.id"
            :title="$t(i18nKeys.common.cancel)"
            class="icon-btn"
            @click="cancelEdit"
          >
            ❌
          </button>
          <button
            :title="$t(i18nKeys.common.delete)"
            class="icon-btn delete"
            @click="deletePlayer(player)"
          >
            🗑️
          </button>
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
import playersService from "../services/players";

const route = useRoute();
const { t } = useI18n();
const eventId = route.params.id;
const players = ref([]);
const name = ref("");
const showModal = ref(false);
const editId = ref(null);
const editName = ref("");

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  name.value = "";
};

const listPlayers = async () => {
  if (!eventId) return;
  const res = await playersService.list(eventId);
  players.value = res.data;
};

const createPlayer = async () => {
  await playersService.create(name.value, eventId);
  name.value = "";
  closeModal();
  listPlayers();
};

const startEdit = (player) => {
  editId.value = player.id;
  editName.value = player.name;
};

const saveEdit = async (player) => {
  if (!editName.value.trim()) return;
  await playersService.update(player.id, editName.value);
  editId.value = null;
  editName.value = "";
  listPlayers();
};

const cancelEdit = () => {
  editId.value = null;
  editName.value = "";
};

const formatElo = (elo) => {
  if (!elo) return "1600";
  return Math.round(elo).toString();
};

const deletePlayer = async (player) => {
  if (confirm(t(i18nKeys.messages.confirmDelete))) {
    await playersService.delete(player.id);
    listPlayers();
  }
};

onMounted(listPlayers);
</script>

<style scoped>
.players-view {
  max-width: 600px;
  margin: 0 auto;
}

/* Header with add button */
.players-header {
  display: flex;
  margin-bottom: 1.5em;
  gap: 1em;
}

.btn-add-player {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8em 1.5em;
  border-radius: 6px;
  font-size: 0.95em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.btn-add-player:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-add-player:active {
  transform: translateY(0);
}

/* Modal Overlay */
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
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Modal Content */
.modal-content {
  background: var(--color-background);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 90%;
  animation: slideUp 0.3s ease;
  color: var(--color-text);
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5em;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3em;
  color: var(--color-text);
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  color: var(--color-text-secondary);
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f5f5f5;
  color: var(--color-text);
}

/* Form inside modal */
.player-form {
  padding: 1.5em;
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}

.form-group label {
  font-weight: 500;
  color: var(--color-text);
  font-size: 0.95em;
}

.form-input {
  padding: 0.8em 1em;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  font-size: 1em;
  background: var(--color-background-soft);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 1em;
  justify-content: flex-end;
  margin-top: 0.5em;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8em 1.5em;
  border-radius: 6px;
  font-size: 0.95em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-cancel {
  background: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.8em 1.5em;
  border-radius: 6px;
  font-size: 0.95em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

/* Players List */
.players-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.empty-state {
  text-align: center;
  padding: 2em;
  color: var(--color-text-secondary);
  font-size: 1em;
}

.player-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 0.8em 1em;
  box-shadow: 0 1px 4px #0001;
  transition:
    box-shadow 0.2s,
    background 0.2s,
    color 0.2s;
}

.player-card:hover {
  box-shadow: 0 2px 8px #0002;
  background: var(--color-background-mute);
  color: var(--color-text);
}

.player-info {
  flex: 1;
}

.player-name {
  font-size: 1.1em;
  font-weight: 500;
}

.player-stats {
  display: flex;
  gap: 1.5em;
  margin-top: 0.4em;
  font-size: 0.9em;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.4em;
}

.stat-label {
  color: var(--color-text-secondary, #666);
  font-weight: 500;
}

.stat-value {
  font-weight: 600;
  padding: 0.2em 0.5em;
  border-radius: 4px;
}

.elo-rating {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-width: 50px;
  text-align: center;
}

.wins {
  background: #e8f5e9;
  color: #2e7d32;
}

.edit-input {
  font-size: 1em;
  padding: 0.2em 0.5em;
  border-radius: 4px;
  border: 1px solid #bdbdbd;
}

.player-actions {
  display: flex;
  gap: 0.3em;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  transition:
    background 0.2s,
    color 0.2s;
}

.icon-btn:hover {
  background: #e3f2fd;
}

.icon-btn.delete:hover {
  background: #ffebee;
  color: #d32f2f;
}

@media (max-width: 768px) {
  .players-view {
    max-width: 100%;
    padding: 0 1em;
  }

  .modal-content {
    width: 95%;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn-submit,
  .btn-cancel {
    width: 100%;
  }
}
</style>
