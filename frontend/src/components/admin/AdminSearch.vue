<template>
  <div>
    <AdminNavbar />
    <div class="container mt-4">
      <h2 class="mb-4">Admin Search</h2>
      
      <form @submit.prevent="performSearch">
        <div class="row g-3 align-items-center mb-3">
          <div class="col-md-3">
            <label class="form-label">Search By</label>
            <select class="form-select" v-model="field" required>
              <option value="email">User Email</option>
              <option value="prime_location">Parking Lot Location</option>
              <option value="spot_number">Spot Number</option>
              <option value="vehicle_number">Vehicle Number</option>
            </select>
          </div>
          <div class="col-md-6">
            <label class="form-label">Value</label>
            <input type="text" class="form-control" v-model="value" placeholder="Enter value to search" required>
          </div>
          <div class="col-md-3 d-flex align-items-end">
            <button type="submit" class="btn btn-primary w-100">Search</button>
          </div>
        </div>
      </form>

      <div v-if="results.length > 0">
        <h4 class="mt-4">Search Results</h4>
        <table class="table table-bordered table-hover table-striped mt-3">
          <thead class="table-dark">
            <tr>
              <th v-for="(val, key) in results[0]" :key="key" class="text-center">{{ key }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in results" :key="index" :class="getRowClass(row)">
              <td v-for="(val, key) in row" :key="key" class="text-center">
                {{ val || '-' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="searched" class="alert alert-warning mt-3">No results found.</div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  components: { AdminNavbar },
  data() {
    return {
      field: 'email',
      value: '',
      results: [],
      searched: false
    }
  },
  methods: {
    async performSearch() {
      try {
        const res = await this.$axios.post('/api/admin/search', {
          field: this.field,
          value: this.value
        });
        this.results = res.data.results;
        this.searched = true;
      } catch (e) {
        alert("Search Failed");
      }
    },
    getRowClass(row) {
      const status = row['Spot Status'];
      if (status === 'Available' || status === 'Parked Out') return 'table-success';
      if (status === 'Occupied') return 'table-danger';
      return '';
    }
  }
}
</script>
