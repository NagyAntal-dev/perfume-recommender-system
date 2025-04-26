<script>

  import AdminDashboard from './AdminDashboard.svelte';
</script>

<main>
  <!-- You might want a proper navbar here eventually -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Perfume Shop Admin</a>
    </div>
  </nav>

  <!-- Render the Admin Dashboard -->
  <AdminDashboard />

  <!-- <hr /> -->
  <!-- <TestDbComponent /> --> <!-- Remove or comment out old component -->
  <!-- <hr /> -->
</main>

<style>
  /* Add global styles if needed, or keep them in app.css */
  main {
    /* Example: Add some padding if the container inside AdminDashboard isn't enough */
    /* padding: 1rem; */
  }
</style>
