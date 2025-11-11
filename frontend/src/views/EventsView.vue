<template>
  <div>
    <h2>{{ $t(i18nKeys.events.title) }}</h2>
    <!-- Form to create a new event -->
    <form class="event-create-form" @submit.prevent="createEvent">
      <div class="form-row">
        <input
          v-model="name"
          :placeholder="$t(i18nKeys.events.eventName)"
          required
        />
        <input v-model="date" type="date" required />
        <input v-model="time" type="time" required />
        <button type="submit">{{ $t(i18nKeys.common.create) }}</button>
      </div>
    </form>
    <!-- Feedback message -->
    <div
      v-if="message"
      :style="{ color: error ? 'red' : 'green', margin: '1em 0' }"
    >
      {{ message }}
    </div>
    <!-- List of events -->
    <div style="display: flex; flex-wrap: wrap; gap: 1em">
      <EventCard
        v-for="event in events"
        :key="event.id"
        :event="event"
        @delete-event="deleteEvent"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { i18nKeys } from "@/i18n.keys";
import eventsService from "../services/events";
import EventCard from "../components/EventCard.vue";

const { t } = useI18n();

// Reactive state for events and form fields
const events = ref([]);
const name = ref("");
const date = ref("");
const time = ref("");
const message = ref("");
const error = ref(false);

// Fetch all active events
const listEvents = async () => {
  const res = await eventsService.list();
  events.value = res.data;
};

// Create a new event
const createEvent = async () => {
  message.value = "";
  error.value = false;
  try {
    await eventsService.create(name.value, date.value, time.value);
    message.value = t(i18nKeys.events.eventCreatedSuccess);
    error.value = false;
    name.value = "";
    date.value = "";
    time.value = "";
    listEvents();
    // eslint-disable-next-line no-unused-vars
  } catch (_) {
    message.value = t(i18nKeys.messages.errorSavingData);
    error.value = true;
  }
};

// Remove an event (soft delete)
const deleteEvent = async (id) => {
  message.value = "";
  error.value = false;
  try {
    await eventsService.delete(id);
    message.value = t(i18nKeys.events.eventDeletedSuccess);
    error.value = false;
    listEvents();
    // eslint-disable-next-line no-unused-vars
  } catch (_) {
    message.value = t(i18nKeys.messages.errorDeletingData);
    error.value = true;
  }
};

// Load events on component mount
onMounted(listEvents);
</script>

<style scoped>
.event-create-form {
  display: flex;
  flex-direction: row;
  gap: 0.5em;
  margin-bottom: 3em;
  align-items: flex-start;
  flex-wrap: wrap;
}

.form-row {
  display: flex;
  gap: 0.5em;
  width: 100%;
  flex-wrap: wrap;
}

.event-create-form input {
  padding: 0.6em 1em;
  border-radius: 6px;
  border: 1px solid #bdbdbd;
  font-size: 1em;
  flex: 1 1 150px;
  min-width: 120px;
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
  flex: 0 0 auto;
}

.event-create-form button[type="submit"]:hover {
  background: #36976b;
}
</style>
