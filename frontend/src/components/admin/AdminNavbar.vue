<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-danger">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/admin/home" style="font-size: 1.5rem; font-weight: bold;">
        Admin Panel
      </router-link>
      
      <div class="collapse navbar-collapse">
        <div class="navbar-nav ms-auto" style="gap: 10px;">
          <router-link to="/admin/home" class="btn btn-outline-light">Home</router-link>
          <router-link to="/admin/users" class="btn btn-outline-light">Users</router-link>
          <router-link to="/admin/search" class="btn btn-outline-light">Search</router-link>
          <router-link to="/admin/summary" class="btn btn-outline-light">Summary</router-link>
          <router-link to="/admin/profile" class="btn btn-outline-light">Profile</router-link>
          <button @click="logout" class="btn btn-warning">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    async logout() {
      await this.$axios.get('/api/admin/logout');
      localStorage.removeItem('user_role');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.navbar { padding: 15px; }
</style>
