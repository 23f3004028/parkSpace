<template>
  <div>
    <BaseNavbar />

    <div style="display: flex; align-items: center; justify-content: center; height: 90vh;">
      <div style="width: fit-content; margin: auto; font-family: 'Montserrat', sans-serif; border: 2px solid #000; border-radius: 15px; padding: 30px; box-shadow: 2px 2px 5px #aaa;">
        
        <h2 style="text-align: center; color: #0300ac; font-weight: bold;">Login</h2><br>
        
        <form @submit.prevent="handleLogin">
          <table style="font-size: 1.2rem;">
            <tr>
              <td><label for="user_email">Email ID :</label></td>
              <td><input v-model="email" type="email" id="user_email" required style="width: 100%; border-radius: 10px; padding: 5px;"></td>
            </tr>
            <tr>
              <td><label for="user_password">Password :</label></td>
              <td><input v-model="password" type="password" id="user_password" required style="width: 100%; border-radius: 10px; padding: 5px;"></td>
            </tr>
          </table>

          <p v-if="errorMessage" style="color: red; text-align: center;">{{ errorMessage }}</p>

          <div style="text-align: center; margin-top: 20px;">
            <button type="submit" style="padding: 8px 20px; background-color: #87CEFA; border: none; border-radius: 8px; font-size: 1rem;">Login</button>
            <div style="margin-top: 10px;">
              <router-link to="/register" style="color: orange; text-decoration: none;">Register here!</router-link>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import BaseNavbar from './BaseNavbar.vue'

export default {
  components: { BaseNavbar },
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const formData = new FormData();
        formData.append('user_email', this.email);
        formData.append('user_password', this.password);

        const response = await this.$axios.post('/login', formData);
        
        if (response.status === 200) {
          const role = response.data.role;
          localStorage.setItem('user_role', role);
          if (response.data.role === 'admin') {
            this.$router.push('/admin/home');
          } else {
            this.$router.push('/user/home');
          }
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Login Failed";
      }
    }
  }
}
</script>
