<template>
  <div>
    <AdminNavbar />
    <div class="container mt-4">
      <div class="header">Registered Users</div>
      
      <table class="table table-bordered table-striped mt-3">
        <thead class="table-dark">
           <tr><th>#</th><th>Email</th><th>Name</th><th>Address</th></tr>
        </thead>
        <tbody>
           <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.address || '-' }}</td>
           </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  components: { AdminNavbar },
  data() { return { users: [] } },
  async created() {
      const res = await this.$axios.get('/api/admin/users');
      this.users = res.data;
  }
}
</script>
