<template>
  <div class="evento-card" @click="goToEvent">
    <div class="card-content">
      <h3>{{ event.name }}</h3>
      <p>{{ $t(i18nKeys.events.date) }}: {{ event.date?.substring(0, 10) }}</p>
      <p>{{ $t(i18nKeys.events.time) }}: {{ event.time }}</p>
      <p style="margin-top: 0.5em; font-size: 0.9em;">
        <strong>{{ $t(i18nKeys.events.status) }}:</strong>
        <span :style="{ color: event.active ? '#42b983' : '#999' }">
          {{ event.active ? $t(i18nKeys.events.active) : $t(i18nKeys.events.inactive) }}
        </span>
      </p>
    </div>
    <button
      class="excluir-btn"
      @click.stop="emitDeleteEvent"
      :title="$t(i18nKeys.events.deleteEvent)"
    >
      🗑️
    </button>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { i18nKeys } from "@/i18n.keys";

// Receives the event object as a prop
const props = defineProps({ event: Object });
const emit = defineEmits(["delete-event"]);
const router = useRouter();

// Navigates to the event detail page when the card is clicked
const goToEvent = () => {
  router.push(`/events/${props.event.id}`);
};

// Emits the delete-event event to the parent component when the delete button is clicked
const emitDeleteEvent = () => {
  emit("delete-event", props.event.id);
};
</script>
<style scoped>
.evento-card {
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 0.75em 1em;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, color 0.2s;
  background: var(--color-background-soft);
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 60px;
}

.evento-card:hover {
  box-shadow: 0 2px 8px #0001;
  background: var(--color-background-mute);
}

.card-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 150px 100px 120px;
  gap: 1.5em;
  align-items: center;
  width: 100%;
}

.card-content h3 {
  margin: 0;
  font-size: 0.95em;
  font-weight: 500;
  color: var(--color-heading);
}

.card-content p {
  margin: 0;
  font-size: 0.85em;
  color: var(--color-text);
}

.card-content p strong {
  font-weight: 600;
}

.excluir-btn {
  background: none;
  border: none;
  color: #d32f2f;
  font-size: 1.2em;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0.5em;
  flex-shrink: 0;
  margin-left: 1em;
}

.excluir-btn:hover {
  color: #b71c1c;
}

@media (max-width: 1024px) {
  .card-content {
    grid-template-columns: 1fr 120px 100px;
    gap: 1em;
  }
}

@media (max-width: 768px) {
  .card-content {
    grid-template-columns: 1fr 100px;
    gap: 0.8em;
  }

  .card-content p {
    display: none;
  }

  .card-content p:first-of-type {
    display: block;
  }
}
</style>
