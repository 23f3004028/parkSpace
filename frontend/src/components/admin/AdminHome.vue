<template>
  <div>
    <AdminNavbar />
    
    <div class="container mt-4">
      <div class="header">Parking Lots</div>

      <div v-if="loading" class="text-center mt-5">Loading Dashboard...</div>

      <div v-else v-for="lot in lots" :key="lot.id" class="lot-box" style="margin-top: 40px; text-align: center;">
        
        <h2 style="font-size: 1.5rem; font-family: 'Montserrat', sans-serif">{{ lot.prime_location }}</h2>

        <div class="lot-actions">
          <label :for="'edit-' + lot.id" class="edit" style="cursor: pointer;">Edit</label> | 
          <label :for="'delete-' + lot.id" class="delete" style="cursor: pointer;">Delete</label>

          <input type="checkbox" :id="'edit-' + lot.id" class="modal-toggle" hidden>
          <div class="modal">
            <div class="modal-content">
              <label :for="'edit-' + lot.id" class="close-btn">X</label>
              <h3 class="modal-heading">Update Parking Lot</h3>
              <div class="form-wrapper">
                <form @submit.prevent="updateLot(lot)">
                  <div class="form-row"><label>Location</label><input v-model="lot.prime_location" required></div>
                  <div class="form-row"><label>Address</label><input v-model="lot.address" required></div>
                  <div class="form-row"><label>Pincode</label><input v-model="lot.pincode" required></div>
                  <div class="form-row"><label>Price</label><input type="number" v-model="lot.price" required></div>
                  <div class="form-row"><label>Total Spots</label><input type="number" v-model="lot.max_no_of_spots" required></div>
                  <div class="form-actions">
                    <button type="submit" class="btn-wide">Update</button>
                    <label :for="'edit-' + lot.id" class="btn-wide cancel-btn">Cancel</label>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <input type="checkbox" :id="'delete-' + lot.id" class="modal-toggle" hidden>
          <div class="modal">
            <div class="modal-content">
              <label :for="'delete-' + lot.id" class="close-btn">X</label>
              <h3 class="modal-heading">Delete Parking Lot</h3>
              <div class="form-wrapper">
                <form @submit.prevent="deleteLot(lot.id)">
                   <p>Are you sure you want to delete {{ lot.prime_location }}?</p>
                   <div class="form-actions">
                    <button type="submit" class="btn-wide">Delete</button>
                    <label :for="'delete-' + lot.id" class="btn-wide cancel-btn">Cancel</label>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>

        <div class="occupancy">
          <span style="color: red;">Occupied: {{ lot.max_no_of_spots - lot.no_of_available }}</span> | 
          <span style="color: green;">Available: {{ lot.no_of_available }}</span>
        </div>
        <hr>

        <div class="spot-grid">
          <div v-for="spot in getSpotsForLot(lot.id)" :key="spot.id" class="lot lot-actions">
             <label :for="'spot-' + spot.id" :class="['spot', spot.status === 'A' ? 'available' : 'occupied']">
                {{ spot.status }}
             </label>

             <input type="checkbox" :id="'spot-' + spot.id" class="modal-toggle" hidden>
             <div class="modal">
               <div class="modal-content">
                 <label :for="'spot-' + spot.id" class="close-btn">X</label>
                 <h3 class="modal-heading">Spot Details</h3>
                 <div class="form-wrapper">
                    <form @submit.prevent="deleteSpot(spot.id, lot.id)">
                       <div class="form-row"><label>Spot #</label><input :value="spot.spot_number" readonly></div>
                       <div v-if="spot.status === 'O'">
                           <div class="form-row"><label>User</label><input :value="spot.email" readonly></div>
                           <div class="form-row"><label>Vehicle</label><input :value="spot.vn" readonly></div>
                           <div class="form-row"><label>Time</label><input :value="formatDate(spot.tb)" readonly></div>
                       </div>
                       <div class="form-actions">
                           <button type="submit" class="btn-wide">Delete Spot</button>
                           <label :for="'spot-' + spot.id" class="btn-wide cancel-btn">Close</label>
                       </div>
                    </form>
                 </div>
               </div>
             </div>
          </div>
        </div>

      </div>

      <div style="margin-top: 40px; text-align: center;">
        <label for="create-modal" class="btn btn-primary-add" style="font-size:1.5rem; padding:12px 24px;">+ Add Lot</label>
      </div>

      <input type="checkbox" id="create-modal" class="modal-toggle" hidden>
      <div class="modal">
        <div class="modal-content">
          <label for="create-modal" class="close-btn">X</label>
          <h3 class="modal-heading">Create New Lot</h3>
          <div class="form-wrapper">
             <form @submit.prevent="createLot">
                <div class="form-row"><label>Location</label><input v-model="newLot.prime_location" required></div>
                <div class="form-row"><label>Address</label><input v-model="newLot.address" required></div>
                <div class="form-row"><label>Pincode</label><input v-model="newLot.pincode" required></div>
                <div class="form-row"><label>Price</label><input type="number" v-model="newLot.price" required></div>
                <div class="form-row"><label>Spots</label><input type="number" v-model="newLot.max_no_of_spots" required></div>
                <div class="form-actions">
                   <button type="submit" class="btn-wide">Create</button>
                   <label for="create-modal" class="btn-wide cancel-btn">Cancel</label>
                </div>
             </form>
          </div>
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
      lots: [],
      spots: [], 
      newLot: { prime_location: '', address: '', pincode: '', price: '', max_no_of_spots: '' }
    }
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await this.$axios.get('/api/admin/home');
        this.lots = res.data.lots;
        this.spots = res.data.spots;
        this.loading = false;
      } catch (e) {
        if(e.response && e.response.status === 403) 
        alert("Access Denied: Please Login as Admin");
        this.$router.push('/login');
      }
    },
    getSpotsForLot(lotId) {
        return this.spots.filter(s => s.lot_id === lotId);
    },
    async createLot() {
        try {
            const formData = new FormData();
            Object.keys(this.newLot).forEach(key => formData.append(key, this.newLot[key]));
            await this.$axios.post('/api/admin/lot/create', formData);
            alert("Lot Created");
            this.newLot = { prime_location: '', address: '', pincode: '', price: '', max_no_of_spots: '' };
            const modalCheckbox = document.getElementById('create-modal');
            if(modalCheckbox) modalCheckbox.checked = false;
            this.fetchData();
        } catch (e) { alert(e.response?.data?.message || "Failed"); }
    },
    async updateLot(lot) {
        try {
            await this.$axios.post('/api/admin/lot/update', lot);
            alert("Updated");
            const modalCheckbox = document.getElementById('edit-' + lot.id);
            if(modalCheckbox) modalCheckbox.checked = false;
            this.fetchData();
        } catch (e) { alert(e.response?.data?.message || "Failed"); }
    },
    async deleteLot(id) {
        if(!confirm("Delete this lot?")) return;
        try {
            await this.$axios.post('/api/admin/lot/delete', { lot_id: id });
            this.fetchData();
        } catch (e) { alert(e.response?.data?.message || "Failed"); }
    },
    async deleteSpot(spotId, lotId) {
        if(!confirm("Delete this spot?")) return;
        try {
            await this.$axios.post('/api/admin/spot/delete', { spot_id: spotId, lot_id: lotId });
            this.fetchData();
        } catch (e) { alert("Failed"); }
    },
    formatDate(ts) {
        if (!ts) return '-';
        return new Date(ts * 1000).toLocaleString();
    }
  }
}
</script>
