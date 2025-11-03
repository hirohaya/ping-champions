<template>
  <div>
    <!-- Breadcrumbs are now global in App.vue -->
    <h2>Event Details</h2>
    <!-- Links to internal event pages -->
    <div style="margin: 1em 0;">
      <router-link :to="`/events/${$route.params.id}/players`">Manage players</router-link>
      |
      <router-link :to="`/events/${$route.params.id}/matches`">Manage matches</router-link>
    </div>
    <router-link to="/events">Back</router-link>
    <!-- You can add more event details and features here -->
    <router-view />
  </div>
</template>
<script setup>
// In the future, fetch event details by id
</script>
