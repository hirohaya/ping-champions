<template>
  <div class="events-view">
    <h2>{{ $t(i18nKeys.events.title) }}</h2>
    
    <!-- Button to open modal -->
    <div class="events-header">
      <button @click="openModal" class="btn-add-event">
        ➕ {{ $t(i18nKeys.events.createEvent) }}
      </button>
    </div>

    <!-- Modal Overlay -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ $t(i18nKeys.events.createEvent) }}</h3>
          <button class="modal-close" @click="closeModal">✕</button>
        </div>
        <form @submit.prevent="createEvent" class="event-form">
          <div class="form-group">
            <input
              id="eventNameInput"
              v-model="name"
              placeholder="Nome do Evento"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <input
              id="eventDateInput"
              v-model="date"
              type="date"
              class="form-input"
              required
            />
          </div>
          <div class="form-group">
            <input
              id="eventTimeInput"
              v-model="time"
              type="time"
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

    <!-- Feedback message -->
    <div
      v-if="message"
      :style="{ color: error ? 'red' : 'green', margin: '1em 0' }"
    >
      {{ message }}
    </div>
    <!-- Filters section -->
    <div class="filters-section">
      <h3>{{ $t(i18nKeys.common.filter) }}</h3>
      <div class="filters-row">
        <input
          v-model="searchName"
          type="text"
          :placeholder="$t(i18nKeys.events.eventName)"
          class="filter-input"
        />
        <select v-model="filterStatus" class="filter-select">
          <option value="">{{ $t(i18nKeys.common.filter) }}</option>
          <option value="active">{{ $t(i18nKeys.events.active) }}</option>
          <option value="inactive">{{ $t(i18nKeys.events.inactive) }}</option>
        </select>
      </div>
    </div>
    <!-- List of events -->
    <div class="events-list-container">
      <EventCard
        v-for="event in filteredEvents"
        :key="event.id"
        :event="event"
        @delete-event="deleteEvent"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
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
const showModal = ref(false);

// Filter states
const searchName = ref("");
const filterStatus = ref("");

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  name.value = "";
  date.value = "";
  time.value = "";
};

// Fetch all events
const listEvents = async () => {
  const res = await eventsService.list();
  events.value = res.data;
};

// Computed property for filtered events
const filteredEvents = computed(() => {
  let filtered = events.value;

  // Filter by name
  if (searchName.value) {
    filtered = filtered.filter((event) =>
      event.name.toLowerCase().includes(searchName.value.toLowerCase())
    );
  }

  // Filter by status
  if (filterStatus.value === "active") {
    filtered = filtered.filter((event) => event.active);
  } else if (filterStatus.value === "inactive") {
    filtered = filtered.filter((event) => !event.active);
  }

  return filtered;
});

// Create a new event
const createEvent = async () => {
  message.value = "";
  error.value = false;
  try {
    await eventsService.create(name.value, date.value, time.value);
    message.value = t(i18nKeys.events.eventCreatedSuccess);
    error.value = false;
    closeModal();
    searchName.value = "";
    filterStatus.value = "";
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
.events-view {
  max-width: 900px;
  margin: 0 auto;
}

/* Header with add button */
.events-header {
  display: flex;
  margin-bottom: 1.5em;
  gap: 1em;
}

.btn-add-event {
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

.btn-add-event:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-add-event:active {
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
.event-form {
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

/* Filters section */
.filters-section {
  background: var(--color-background-soft);
  border-radius: 8px;
  padding: 1em;
  margin-bottom: 2em;
  border: 1px solid var(--color-border);
}

.filters-section h3 {
  margin-top: 0;
  margin-bottom: 1em;
  font-size: 1em;
}

.filters-row {
  display: flex;
  gap: 0.5em;
  flex-wrap: wrap;
}

.filter-input,
.filter-select {
  padding: 0.6em 1em;
  border-radius: 6px;
  border: 1px solid #bdbdbd;
  font-size: 1em;
  flex: 1 1 150px;
  min-width: 120px;
  background: var(--color-background);
  color: var(--color-text);
}

.filter-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.1);
}

.events-list-container {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
  width: 100%;
}

@media (max-width: 768px) {
  .events-view {
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
