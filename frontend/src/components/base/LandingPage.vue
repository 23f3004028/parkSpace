<template>
  <div>
    <BaseNavbar />

    <div class="container my-4">
      
       <div v-if="message" class="alert alert-info alert-dismissible fade show">
          {{ message }}
          <button type="button" class="btn-close" @click="message = ''"></button>
       </div>

       <h1 class="text-center" style="font-size: 1rem">Welcome to the Parking Lot Booking App!</h1>
       <p class="text-center">Book slots easily from your device.</p>
       
       <div class="text-center mt-4">
          <router-link to="/login" class="btn btn-primary">Go to Login</router-link>
       </div>

    </div>
  </div>
</template>

<script>
import BaseNavbar from './BaseNavbar.vue'

export default {
  components: {
    BaseNavbar
  },
  data() {
    return {
      message: '' 
    }
  }
}
</script>
