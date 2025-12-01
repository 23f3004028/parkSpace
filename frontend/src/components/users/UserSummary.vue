<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      <div class="text-center mb-4">
        <h2>Welcome, {{ user.name }}</h2>
        <p class="text-muted">Your Parking Summary</p>
      </div>

      <div class="row text-center mb-5">
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
              <h5 class="text-warning">Active Bookings</h5>
              <h3>{{ stats.active }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm border-success">
            <div class="card-body">
              <h5 class="text-success">Total Spent</h5>
              <h3>₹{{ (stats.spent ?? 0).toFixed(2) }}</h3>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-secondary text-white">
              <h4 class="mb-0">Recent Bookings (Last 10)</h4>
            </div>
            <div class="card-body p-0">
              <div v-if="recent_bookings.length > 0">
                <table class="table table-striped table-hover mb-0">
                  <thead>
                    <tr>
                      <th>Booking ID</th>
                      <th>Parking Lot</th>
                      <th>Spot Number</th>
                      <th>Status</th>
                      <th>Price (₹)</th>
                      <th>Booked At</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="booking in recent_bookings" :key="booking.id">
                      <td>{{ booking.id }}</td> 
                      <td>Lot #{{ booking.lot_id }}</td> 
                      <td>{{ booking.spot_number }}</td>
                      <td>
                        <span :class="{'badge bg-success': booking.booking_status === 'closed', 'badge bg-warning text-dark': booking.booking_status === 'open'}">
                          {{ booking.booking_status }}
                        </span>
                      </td>
                      
                      <td>
                        <span v-if="booking.price != null">₹{{ booking.price.toFixed(2) }}</span>
                        <span v-else>-</span>
                      </td>
                      
                      <td>{{formatDate(booking.timestamp_booked) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p v-else class="p-3 text-center text-muted">No recent bookings found.</p>
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
  data() { 
    return { 
      user: {}, 
      stats: { total: 0, active: 0, spent: 0 }, 
    recent_bookings: [] 
    } 
  },
  async created() {
    try {
      const res = await this.$axios.get('/api/user/summary');
      this.user = res.data.user;
      this.stats = res.data.stats;
      

      this.recent_bookings = res.data.recent_bookings || []; 

    } catch (error) {
      console.error("Error fetching user summary:", error);
    }
  },
  methods: {
    formatDate(ts) {
      if (!ts) return '';
      return new Date(ts * 1000).toLocaleString();
    }
  }
}
</script>
