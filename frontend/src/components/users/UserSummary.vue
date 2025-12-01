<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      <div class="text-center mb-4">
        <h2>Welcome, {{ user.name }}</h2>
        <p class="text-muted">Your Parking Summary</p>
      </div>

      <div class="row text-center mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm border-primary">
            <div class="card-body">
              <h5 class="text-primary">Total Bookings</h5>
              <h3>{{ stats.total }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-warning">
            <div class="card-body">
              <h5 class="text-warning">Active</h5>
              <h3>{{ stats.active }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-success">
            <div class="card-body">
              <h5 class="text-success">Spent</h5>
              <h3>₹{{ stats.spent }}</h3>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import UserNavbar from './UserNavbar.vue'

export default {
  components: { UserNavbar },
  data() { return { user: {}, stats: {} } },
  async created() {
    const res = await this.$axios.get('/api/user/summary');
    this.user = res.data.user;
    this.stats = res.data.stats;
  }
}
</script>
