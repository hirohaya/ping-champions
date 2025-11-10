<template>
  <div>
    <h1>Ping Champions: pinging the ponging</h1>
    <Breadcrumbs />
    <!-- Feedback Snackbar/Alert -->
    <div v-if="feedback.message" :class="['feedback', feedback.type]">
      {{ feedback.message }}
    </div>
    <router-view @feedback="showFeedback" />
  </div>
</template>

<script>
// Main App component: handles global feedback and renders breadcrumbs and router views
import Breadcrumbs from "./components/Breadcrumbs.vue";

export default {
  name: "App",
  components: { Breadcrumbs },
  data() {
    return {
      // feedback: stores the current feedback message and type
      feedback: {
        message: "",
        type: "success", // 'success' | 'error'
      },
      feedbackTimeout: null, // timeout id for auto-hiding feedback
    };
  },
  methods: {
    // showFeedback: displays a feedback message for a set duration
    showFeedback({ message, type = "success", duration = 3000 }) {
      this.feedback.message = message;
      this.feedback.type = type;
      if (this.feedbackTimeout) clearTimeout(this.feedbackTimeout);
      this.feedbackTimeout = setTimeout(() => {
        this.feedback.message = "";
      }, duration);
    },
  },
};
</script>

<style scoped>
/* h1 style mantido */
h1 {
  margin-bottom: 1rem;
}
/* Feedback styles */
.feedback {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  min-width: 200px;
  max-width: 90vw;
  padding: 16px 32px;
  border-radius: 8px;
  color: #fff;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  text-align: center;
  transition: opacity 0.3s;
}
.feedback.success {
  background: #4caf50;
}
.feedback.error {
  background: #f44336;
}
</style>
