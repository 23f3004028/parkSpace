<template>
  <div>
    <AdminNavbar />
    <div class="container mt-5 p-4 bg-white rounded-4 shadow-lg border border-2 border-danger" style="max-width: 600px;">
      <h2 class="text-center">Edit Admin Profile</h2>
      
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input type="text" class="form-control" v-model="admin.name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Registered Email</label>
          <input type="text" class="form-control" v-model="admin.email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Address</label>
          <textarea class="form-control" v-model="admin.address" rows="3"></textarea>
        </div>
        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input type="text" class="form-control" v-model="admin.pincode">
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
    </div>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  components: { AdminNavbar },
  data() {
    return { admin: {} }
  },
  async created() {
    const res = await this.$axios.get('/api/admin/profile');
    this.admin = res.data;
  },
  methods: {
    async updateProfile() {
      await this.$axios.post('/api/admin/profile', this.admin);
      alert("Profile Updated Successfully");
    }
  }
}
</script>
