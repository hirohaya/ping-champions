
<template>
  <div class="players-view">
    <h2>Players</h2>
    <form class="player-form" @submit.prevent="createPlayer">
      <input v-model="name" placeholder="Player name" required />
      <button type="submit">Add</button>
    </form>
    <div class="players-list">
      <div v-for="player in players" :key="player.id" class="player-card">
        <div class="player-info">
          <span v-if="editId !== player.id" class="player-name">{{ player.name }}</span>
          <input v-else v-model="editName" @keyup.enter="saveEdit(player)" @blur="cancelEdit" class="edit-input" />
        </div>
        <div class="player-actions">
          <button @click="startEdit(player)" v-if="editId !== player.id" title="Edit" class="icon-btn">✏️</button>
          <button @click="saveEdit(player)" v-if="editId === player.id" title="Save" class="icon-btn">💾</button>
          <button @click="cancelEdit" v-if="editId === player.id" title="Cancel" class="icon-btn">❌</button>
          <button @click="deletePlayer(player)" title="Delete" class="icon-btn delete">🗑️</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import playersService from '../services/players'

const route = useRoute()
const eventId = route.params.id
const players = ref([])
const name = ref('')
const editId = ref(null)
const editName = ref('')

const listPlayers = async () => {
  if (!eventId) return
  const res = await playersService.list(eventId)
  players.value = res.data
}

const createPlayer = async () => {
  await playersService.create(name.value, eventId)
  name.value = ''
  listPlayers()
}

const startEdit = (player) => {
  editId.value = player.id
  editName.value = player.name
}

const saveEdit = async (player) => {
  if (!editName.value.trim()) return
  await playersService.update(player.id, editName.value)
  editId.value = null
  editName.value = ''
  listPlayers()
}

const cancelEdit = () => {
  editId.value = null
  editName.value = ''
}

const deletePlayer = async (player) => {
  if (confirm('Are you sure you want to delete this player?')) {
    await playersService.delete(player.id)
    listPlayers()
  }
}

onMounted(listPlayers)
</script>

<style scoped>
.players-view {
  max-width: 600px;
  margin: 0 auto;
}
.player-form {
  display: flex;
  gap: 0.5em;
  margin-bottom: 1.5em;
}
.players-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
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
  transition: box-shadow 0.2s, background 0.2s, color 0.2s;
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
  transition: background 0.2s, color 0.2s;
}
.icon-btn:hover {
  background: #e3f2fd;
}
.icon-btn.delete:hover {
  background: #ffebee;
  color: #d32f2f;
}
</style>
