<template>
  <div>
    <UserNavbar />
    <div class="container mt-5 p-4 border border-primary rounded shadow-lg" style="max-width: 600px;">
      <h2 class="text-center">Edit Profile</h2>
      <form @submit.prevent="update">
        <div class="mb-3"><label>Name</label><input v-model="form.name" class="form-control" required></div>
        <div class="mb-3"><label>Email</label><input v-model="form.email" class="form-control" disabled></div>
        <div class="mb-3"><label>Address</label><textarea v-model="form.address" class="form-control"></textarea></div>
        <div class="mb-3"><label>Pincode</label><input v-model="form.pincode" class="form-control"></div>
        <button class="btn btn-primary w-100">Save Changes</button>
      </form>
    </div>
  </div>
</template>

<script>
import UserNavbar from './UserNavbar.vue'

export default {
  components: { UserNavbar },
  data() { return { form: {} } },
  async created() {
    const res = await this.$axios.get('/api/user/profile');
    this.form = res.data;
  },
  methods: {
    async update() {
      await this.$axios.post('/api/user/profile', this.form);
      alert("Profile Updated");
    }
  }
}
</script>
