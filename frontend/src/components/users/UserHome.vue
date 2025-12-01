<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      
      <div v-if="history.length > 0">

        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="header mb-0">Recent Parking History</h4>
            <button @click="triggerExport" class="btn btn-warning btn-sm">
                Export History (CSV)
            </button>
        </div>


        <div class="table-container">
          <table class="table table-bordered table-striped text-center">
            <thead class="table-dark">
              <tr>
                <th>Location</th>
                <th>Vehicle</th>
                <th>Booked At</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in history" :key="item.id">
                <td>{{ item.pl }}</td>
                <td>{{ item.vn }}</td>
                <td>{{ formatDate(item.tb) }}</td>
                <td>
                  <div v-if="item.b_status === 'open'">
                    <button class="btn btn-primary" @click="openReleaseModal(item)">Release</button>
                  </div>
                  <div v-else>
                    <span class="badge bg-success">Parked Out</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="header">No Recent History</div>

      <hr class="my-5">

      <div class="row justify-content-center mb-4">
        <div class="col-md-6 d-flex gap-2">
          <input v-model="searchQuery" class="form-control" placeholder="Search Location or Pincode">
        </div>
      </div>

      <div class="header">Available Parking Lots</div>
      <div class="table-container">
        <table class="table table-bordered table-striped text-center">
          <thead class="table-dark">
            <tr>
              <th>Location</th>
              <th>Address</th>
              <th>Available Spots</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in filteredLots" :key="lot.id">
              <td>{{ lot.prime_location }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.no_of_available }}</td>
              <td>
                <button v-if="Number(lot.no_of_available) > 0" class="btn btn-success" @click="openBookModal(lot)">Book</button>
                <button v-else class="btn btn-secondary" disabled>Full</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="showBookModal" class="modal-overlay">
        <div class="modal-content">
          <h3>Book Spot</h3>
          <form @submit.prevent="confirmBooking">
            <div class="mb-2"><label>Location:</label> <b>{{ selectedLot.prime_location }}</b></div>
            <div class="mb-2"><label>Spot ID:</label> <input :value="selectedLot.available_spot_number" readonly class="form-control"></div>
            <div class="mb-2"><label>Vehicle No:</label> <input v-model="bookingForm.vehicle_number" required class="form-control"></div>
            <div class="d-flex gap-2 mt-3">
              <button type="submit" class="btn btn-success w-50">Reserve</button>
              <button type="button" @click="showBookModal = false" class="btn btn-secondary w-50">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <div v-if="showReleaseModal" class="modal-overlay">
        <div class="modal-content">
          <h3>Release Spot</h3>
          <div class="mb-2"><label>Location:</label> {{ releaseItem.pl }}</div>
          <div class="mb-2"><label>Booked At:</label> {{ formatDate(releaseItem.tb) }}</div>
          <div class="mb-2"><label>Rate:</label> ₹{{ releaseItem.price }}/hr</div>
          <div class="mb-2 text-danger fw-bold"><label>Est. Cost:</label> ₹{{ calculateCost(releaseItem) }}</div>
          
          <div class="d-flex gap-2 mt-3">
            <button @click="confirmRelease" class="btn btn-danger w-50">Pay & Release</button>
            <button @click="showReleaseModal = false" class="btn btn-secondary w-50">Cancel</button>
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
      lots: [],
      history: [], 
      searchQuery: '',
      
      showBookModal: false,
      selectedLot: {},
      bookingForm: { vehicle_number: '' },

      showReleaseModal: false,
      releaseItem: {}
    }
  },
  computed: {
    filteredLots() {
      if (!this.searchQuery) return this.lots;
      const q = this.searchQuery.toLowerCase();
      return this.lots.filter(l => 
        l.prime_location.toLowerCase().includes(q) || 
        l.pincode.includes(q)
      );
    }
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await this.$axios.get('/api/user/home');
        this.lots = res.data.lots;
        this.history = res.data.history;
      } catch (e) {
        if(e.response && e.response.status === 401) {
          alert("Session Expired. Please Login.");
          this.$router.push('/login');
        }
      }
    },
    formatDate(ts) {
      if (!ts) return '';
      return new Date(ts * 1000).toLocaleString();
    },
    openBookModal(lot) {
      this.selectedLot = lot;
      this.bookingForm.vehicle_number = '';
      this.showBookModal = true;
    },
    async confirmBooking() {
      try {
        await this.$axios.post('/api/user/book', {
          lot_id: this.selectedLot.id,
          spot_number: this.selectedLot.available_spot_number,
          vehicle_number: this.bookingForm.vehicle_number
        });
        alert("Booked Successfully!");
        this.showBookModal = false;
        this.fetchData();
      } catch (e) { alert("Booking Failed"); }
    },
    openReleaseModal(item) {
      this.releaseItem = item;
      this.showReleaseModal = true;
    },
    calculateCost(item) {
      if (!item.tb) return 0;
      const now = Math.floor(Date.now() / 1000);
      const hours = (now - item.tb) / 3600;
      return (hours * item.price).toFixed(2);
    },
    async confirmRelease() {
      try {

        await this.$axios.post('/api/user/release', {
          booking_id: this.releaseItem.id,
          lot_id: this.releaseItem.li,     
          spot_number: this.releaseItem.sn 
        });
        alert("Spot Released Successfully");
        this.showReleaseModal = false;
        this.fetchData();
      } catch (e) { 
        alert("Release Failed"); 
        console.error(e);
      }
    },
    async triggerExport() {
        try {
            const res = await this.$axios.get('/api/user/export');
            alert(res.data.message); // Should say "Export initiated..."
        } catch (e) {
            alert("Failed to start export job.");
        }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
  background: white; padding: 20px; border-radius: 8px; width: 90%; max-width: 400px;
}
.table-container {
  overflow-x: auto;
}
</style>
