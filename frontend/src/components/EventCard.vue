<template>
  <div class="evento-card" @click="goToEvent">
    <div class="card-content">
      <h3>{{ event.name }}</h3>
      <p>{{ $t(i18nKeys.events.date) }}: {{ event.date?.substring(0, 10) }}</p>
      <p>{{ $t(i18nKeys.events.time) }}: {{ event.time }}</p>
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
  border-radius: 8px;
  padding: 1em;
  margin: 1em 0;
  cursor: pointer;
  transition:
    box-shadow 0.2s,
    background 0.2s,
    color 0.2s;
  background: var(--color-background-soft);
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.evento-card:hover {
  box-shadow: 0 2px 8px #0001;
  background: var(--color-background-mute);
  color: var(--color-text);
}
.card-content {
  flex: 1;
}
.excluir-btn {
  background: none;
  border: none;
  color: #d32f2f;
  font-size: 1.3em;
  cursor: pointer;
  margin-left: 1em;
  transition: color 0.2s;
}
.excluir-btn:hover {
  color: #b71c1c;
}
</style>
