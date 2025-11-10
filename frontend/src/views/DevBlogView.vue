<template>
  <div class="dev-blog-container">
    <h1>Dev Blog</h1>
    <section>
      <h2>Updates</h2>
      <ul>
        <li>
          Standardization of all backend and frontend file names to English and
          improved code clarity.
        </li>
        <li>
          Added global feedback system for success/error messages in the
          frontend.
        </li>
        <li>Implemented breadcrumb navigation on all pages.</li>
        <li>All URLs refactored to clear and English names.</li>
        <li>
          Housekeeping: removed dead code, organized imports, and added comments
          throughout backend and frontend.
        </li>
        <li>
          Implemented soft delete for events (mark as inactive instead of
          removing from the database).
        </li>
        <li>
          Improved folder structure in frontend and backend for easier
          maintenance.
        </li>
      </ul>
    </section>
    <section>
      <h2>Project Particularities</h2>
      <ul>
        <li>
          Backend uses FastAPI with SQLAlchemy ORM and SQLite for rapid
          prototyping.
        </li>
        <li>
          Frontend built with Vue 3 and Vite for agile development and hot
          reload.
        </li>
        <li>
          All API endpoints follow RESTful conventions and use English names.
        </li>
        <li>Soft delete is used for events, preserving data history.</li>
        <li>
          Feedback system is global and can be triggered from any component via
          events.
        </li>
        <li>
          Breadcrumbs are generated dynamically based on the current route and
          now display the event name when viewing an event or its subpages.
        </li>
        <li>
          All code is commented and organized to facilitate onboarding of new
          developers. Recent updates include improved comments for new features
          and code sections.
        </li>
      </ul>
    </section>
    <section>
      <h2>How to Contribute</h2>
      <ul>
        <li>
          Follow the English naming convention for all new files and endpoints.
        </li>
        <li>Document new features or changes on this Dev Blog page.</li>
        <li>
          Keep the code clean, commented, and remove dead code whenever
          possible.
        </li>
        <li>Test all changes locally before pushing to the main branch.</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
// This page is for developers to track project progress and important notes.
</script>

<style scoped>
.dev-blog-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #0001;
}
h1 {
  margin-bottom: 1.5rem;
}
h2 {
  margin-top: 2rem;
  color: #42b983;
}
ul {
  margin: 0 0 1.5rem 1.5rem;
  padding: 0;
}
li {
  margin-bottom: 0.5rem;
}
</style>
