
<template>
  <nav aria-label="breadcrumb" class="breadcrumbs">
    <router-link to="/">Home</router-link>
    <template v-if="$route.path.startsWith('/events')">
      <span> / </span>
      <router-link to="/events">Events</router-link>
      <template v-if="$route.name === 'event-detail'">
        <span> / </span>
        <span>{{ eventName ? eventName : `Event ${$route.params.id}` }}</span>
      </template>
      <template v-else-if="$route.name === 'event-players'">
        <span> / </span>
        <router-link :to="`/events/${$route.params.id}`">{{ eventName ? eventName : `Event ${$route.params.id}` }}</router-link>
        <span> / </span>
        <span>Players</span>
      </template>
      <template v-else-if="$route.name === 'event-matches'">
        <span> / </span>
        <router-link :to="`/events/${$route.params.id}`">{{ eventName ? eventName : `Event ${$route.params.id}` }}</router-link>
        <span> / </span>
        <span>Matches</span>
      </template>
    </template>
    <template v-else-if="$route.path.startsWith('/players')">
      <span> / </span>
      <span>Players</span>
    </template>
    <template v-else-if="$route.path.startsWith('/matches')">
      <span> / </span>
      <span>Matches</span>
    </template>
    <template v-else-if="$route.path.startsWith('/ranking')">
      <span> / </span>
      <span>Ranking</span>
    </template>
    <template v-else-if="$route.path.startsWith('/status')">
      <span> / </span>
      <span>Project Status</span>
    </template>
  </nav>
</template>

<script setup>
// Breadcrumbs component dynamically fetches and displays the event name in the breadcrumb trail
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import eventsService from '../services/events'

const route = useRoute()
const eventName = ref('')

// Fetch the event name from the backend using the event id in the route
const fetchEventName = async (id) => {
  if (!id) {
    eventName.value = ''
    return
  }
  try {
    const res = await eventsService.list()
    const event = res.data.find(e => String(e.id) === String(id))
    eventName.value = event ? event.name : ''
  } catch (e) {
    eventName.value = ''
  }
}

// Watch for changes in the route event id and update the event name accordingly
watch(() => route.params.id, (id) => {
  fetchEventName(id)
}, { immediate: true })

// Fetch event name on component mount
onMounted(() => {
  fetchEventName(route.params.id)
})
</script>

<style scoped>
.breadcrumbs {
  margin-bottom: 1em;
  font-size: 1.05em;
}
.breadcrumbs a {
  color: #42b983;
  text-decoration: none;
}
.breadcrumbs a:hover {
  text-decoration: underline;
}
.breadcrumbs span {
  color: #888;
}
</style>
