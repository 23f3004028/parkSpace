<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/user/home">Parking App</router-link>
      <div class="d-flex" style="gap: 15px;">
        <router-link to="/user/home" class="btn btn-outline-light">Home</router-link>
        <router-link to="/user/summary" class="btn btn-outline-light">Summary</router-link>
        <router-link to="/user/edit_profile" class="btn btn-outline-light">Profile</router-link>
        <button @click="logout" class="btn btn-danger">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    async logout() {
      try {
        await this.$axios.get('/api/user/logout');
      } catch (error) {
        console.error("Logout API error:", error);
      } finally {
        localStorage.removeItem('user_role');
        this.$router.push('/login');

      }
    }
  }
}
</script>
