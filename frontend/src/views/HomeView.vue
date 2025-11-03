<template>
  <div class="home-container">
    <div class="home-hero">
      <img src="/src/assets/logo.svg" alt="Logo Ping Champions" class="home-logo" />
  <h2>Welcome to Ping Champions</h2>
  <p class="home-desc">Organize events, add players, record matches, and track your table tennis club's ranking.</p>
      <div class="home-actions">
  <router-link to="/events" class="home-btn">Events</router-link>
      </div>
    </div>

    <div class="home-stats">
  <h3>System Panel</h3>
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-label">Events</span>
          <span class="stat-value">{{ stats.events }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Players</span>
          <span class="stat-value">{{ stats.players }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Matches</span>
          <span class="stat-value">{{ stats.matches }}</span>
        </div>
      </div>
    </div>

    <div class="home-tutorial">
      <h3>How to use Ping Champions</h3>
      <ol>
        <li><b>Create an event</b> by clicking "Events".</li>
        <li><b>Add players</b> by accessing the created event and registering participants.</li>
        <li><b>Record matches</b> within the event, entering results.</li>
        <li><b>Track the ranking</b> of players for each event.</li>
      </ol>
    </div>

    <div class="home-dev-blog-btn">
  <router-link to="/dev-blog" class="dev-blog-btn">Follow the Project Dev Blog</router-link>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import eventsService from '../services/events'
import playersService from '../services/players'
import jogosService from '../services/jogos'

const stats = ref({ events: 0, players: 0, matches: 0 })

const loadStats = async () => {
  try {
    const [resEvents, resPlayers, resMatches] = await Promise.all([
      eventsService.list(),
      playersService.listAll(),
      jogosService && jogosService.listarTodos ? jogosService.listarTodos() : Promise.resolve({ data: [] })
    ])
    stats.value.events = resEvents.data.length
    stats.value.players = resPlayers.data.length
    stats.value.matches = resMatches.data.length
  } catch (e) {
    // fallback: show zero
  }
}

onMounted(loadStats)
</script>

<style scoped>
.home-container {
  max-width: 700px;
  margin: 2.5rem auto 2rem auto;
  padding: 2rem 1.5rem;
  background: var(--color-background-soft);
  color: var(--color-heading);
  border: 1px solid var(--color-border);
  border-radius: 1.2em;
  box-shadow: 0 2px 12px #0001;
}
.home-dev-blog-btn {
  display: flex;
  justify-content: center;
  margin: 2.5rem 0 0 0;
}
.dev-blog-btn {
  background: #42b983;
  color: #fff;
  font-weight: bold;
  padding: 1rem 2.5rem;
  border-radius: 2rem;
  font-size: 1.1rem;
  text-decoration: none;
  box-shadow: 0 2px 8px #0001;
  transition: background 0.2s;
}
.dev-blog-btn:hover {
  background: #36976b;
}
.home-hero {
  text-align: center;
  margin-bottom: 2.5rem;
}
.home-logo {
  width: 80px;
  margin-bottom: 1rem;
}
.home-desc {
  font-size: 1.1em;
  color: var(--color-text);
  margin-bottom: 1.2em;
}
.home-actions {
  margin-bottom: 1.5em;
}
.home-btn {
  display: inline-block;
  margin: 0 0.5em;
  padding: 0.7em 1.5em;
  background: #42b983;
  color: #fff;
  border-radius: 2em;
  text-decoration: none;
  font-weight: bold;
  font-size: 1em;
  transition: background 0.2s;
}
.home-btn:hover {
  background: #35495e;
}
.home-stats {
  margin-bottom: 2.5rem;
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 1em;
  box-shadow: 0 1px 6px #0001;
  padding: 1.5em 1em 2em 1em;
}
.stats-grid {
  display: flex;
  gap: 1.5em;
  justify-content: center;
  margin-top: 1em;
}
.stat-card {
  background: var(--color-background);
  border-radius: 1em;
  box-shadow: 0 1px 6px #0001;
  padding: 1.2em 2em;
  text-align: center;
  border: 1px solid var(--color-border);
}
.stat-label {
  color: var(--color-text);
  font-size: 0.95em;
}
.stat-value {
  display: block;
  font-size: 1.7em;
  font-weight: bold;
  color: #42b983;
}
.home-tutorial {
  margin-bottom: 2.5rem;
}
.home-tutorial ol {
  margin-left: 1.2em;
  color: var(--color-text);
}
.home-news {
  margin-bottom: 1.5rem;
}
.home-news ul {
  margin-left: 1.2em;
  color: var(--color-text);
}
@media (max-width: 600px) {
  .home-container {
    padding: 1rem 0.2rem;
  }
  .stats-grid {
    flex-direction: column;
    gap: 0.7em;
  }
  .stat-card {
    padding: 1em 0.5em;
  }
}
</style>
