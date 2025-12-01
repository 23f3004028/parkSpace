<template>
  <div>
    <AdminNavbar />
    <div class="container mt-4">
      <h2 class="text-center mb-4">Admin Summary Dashboard</h2>

      <div v-if="loading" class="text-center">Loading Stats...</div>

      <div v-else>
        <div class="row text-center mb-4">
          <div class="col-md-3 mb-3" v-for="(val, key) in displayStats" :key="key">
            <div class="card shadow-sm bg-light border-success">
              <div class="card-body">
                <h5 class="card-title text-success">{{ key }}</h5>
                <h3>{{ val }}</h3>
              </div>
            </div>
          </div>
        </div>

        <h4 class="mt-5">Lot-wise Occupancy</h4>
        <table class="table table-bordered table-striped text-center">
          <thead class="table-success text-center">
            <tr><th>ID</th><th>Location</th><th>Total</th><th>Available</th><th>Occupied</th><th>Price</th></tr>
          </thead>
          <tbody>
            <tr v-for="lot in lotData" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td>{{ lot.prime_location }}</td>
              <td>{{ lot.max_no_of_spots }}</td>
              <td>{{ lot.no_of_available }}</td>
              <td>{{ lot.max_no_of_spots - lot.no_of_available }}</td>
              <td>₹{{ lot.price }}</td>
            </tr>
          </tbody>
        </table>

        <h4 class="mt-5">Recent Bookings</h4>
        <div class="table-responsive">
          <table class="table table-hover table-bordered text-center">
            <thead class="table-primary text-center">
              <tr><th>User</th><th>Vehicle</th><th>Spot</th><th>Lot ID</th><th>Booked At</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr v-for="b in recentBookings" :key="b.spot_number + b.timestamp_booked">
                <td>{{ b.name }}</td>
                <td>{{ b.vehicle_number }}</td>
                <td>{{ b.spot_number }}</td>
                <td>{{ b.lot_id }}</td>
                <td>{{ formatDate(b.timestamp_booked) }}</td>
                <td>
                  <span :class="['badge', b.booking_status === 'open' ? 'bg-success' : 'bg-danger']">
                    {{ b.booking_status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  components: { AdminNavbar },
  data() {
    return {
      loading: true,
      stats: {},
      lotData: [],
      recentBookings: []
    }
  },
  computed: {
    displayStats() {
      if (!this.stats.total_users) return {};
      return {
        "Users": this.stats.total_users,
        "Admins": this.stats.total_admins,
        "Lots": this.stats.total_lots,
        "Spots": this.stats.total_spots,
        "Available": this.stats.available_spots,
        "Bookings": this.stats.booked_spots,
        "Active": this.stats.active_bookings
      }
    }
  },
  async created() {
    try {
      const res = await this.$axios.get('/api/admin/summary');
      this.stats = res.data.stats;
      this.lotData = res.data.lot_data;
      this.recentBookings = res.data.recent_bookings;
      this.loading = false;
    } catch (e) {
      console.error(e);
    }
  },
  methods: {
    formatDate(ts) { return new Date(ts * 1000).toLocaleString(); }
  }
}
</script>
