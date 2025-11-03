<template>
  <div>
    <h2>Events</h2>
    <!-- Form to create a new event -->
  <form class="event-create-form" @submit.prevent="createEvent">
  <input v-model="name" placeholder="Event name" required style="margin-right: 0.5em;" />
  <input v-model="date" type="date" required style="margin-right: 0.5em;" />
  <input v-model="time" type="time" required style="margin-right: 0.5em;" />
       <button type="submit">Create Event</button>
    </form>
    <!-- Feedback message -->
    <div v-if="message" :style="{color: error ? 'red' : 'green', margin: '1em 0'}">{{ message }}</div>
    <!-- List of events -->
    <div style="display: flex; flex-wrap: wrap; gap: 1em;">
      <EventCard v-for="event in events" :key="event.id" :event="event" @delete-event="deleteEvent" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import eventsService from '../services/events'
import EventCard from '../components/EventCard.vue'

// Reactive state for events and form fields
const events = ref([])
const name = ref('')
const date = ref('')
const time = ref('')
const message = ref('')
const error = ref(false)

// Fetch all active events
const listEvents = async () => {
  const res = await eventsService.list()
  events.value = res.data
}

// Create a new event
const createEvent = async () => {
  message.value = ''
  error.value = false
  try {
    await eventsService.create(name.value, date.value, time.value)
    message.value = 'Event created successfully!'
    error.value = false
    name.value = ''
    date.value = ''
    time.value = ''
    listEvents()
  } catch (e) {
    message.value = 'Error creating event.'
    error.value = true
  }
}

// Remove an event (soft delete)
const deleteEvent = async (id) => {
  message.value = ''
  error.value = false
  try {
    await eventsService.delete(id)
    message.value = 'Event removed successfully!'
    error.value = false
    listEvents()
  } catch (e) {
    message.value = 'Error removing event.'
    error.value = true
  }
}

// Load events on component mount
onMounted(listEvents)
</script>

<style scoped>
.event-create-form {
  display: flex;
  flex-direction: column;
  gap: 2em;
  margin-bottom: 3em;
  margin-right: 3em;
}

.event-create-form input {
  flex: 1 1 180px;
  min-width: 0;
  padding: 0.6em 1em;
  border-radius: 6px;
  margin-right: 3em;
  border: 1px solid #bdbdbd;
  font-size: 1em;
}

.event-create-form button[type="submit"] {
  padding: 0.6em 1.5em;
  border-radius: 6px;
  background: #42b983;
  color: #fff;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}

.event-create-form button[type="submit"]:hover {
  background: #36976b;
}
</style>


