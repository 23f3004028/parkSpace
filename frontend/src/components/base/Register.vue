<template>
  <div>
    <BaseNavbar />

    <div style="display: flex; align-items: center; justify-content: center; height: 90vh;">
      <div style="width: fit-content; margin: auto; font-family: 'Montserrat', sans-serif; border: 2px solid #000; border-radius: 15px; padding: 30px; box-shadow: 2px 2px 5px #aaa;">
        
        <h2 style="text-align: center; color: #0300ac; font-weight: bold;">User Registration</h2><br>
        
        <form @submit.prevent="handleRegister">
          <table style="font-size: 1.2rem;">
            <tr>
              <td><label>Fullname :</label></td>
              <td><input v-model="form.user_name" type="text" required style="width: 100%; border-radius: 10px; padding: 5px;"></td>
            </tr>
            <tr>
              <td><label>Email ID :</label></td>
              <td><input v-model="form.user_email" type="email" required style="width: 100%; border-radius: 10px; padding: 5px;"></td>
            </tr>
            <tr>
              <td><label>Password :</label></td>
              <td><input v-model="form.user_password" type="password" required style="width: 100%; border-radius: 10px; padding: 5px;"></td>
            </tr>
            <tr>
              <td><label>Confirm Password :</label></td>
              <td><input v-model="form.user_confirm_password" type="password" required style="width: 100%; border-radius: 10px; padding: 5px;"></td>
            </tr>
          </table>

          <p v-if="errorMessage" style="color: red; text-align: center;">{{ errorMessage }}</p>

          <div style="text-align: center; margin-top: 20px;">
            <button type="submit" style="padding: 8px 20px; background-color: #87CEFA; border: none; border-radius: 8px; font-size: 1rem;">Register</button>
            <div style="margin-top: 10px;">
              <router-link to="/login" style="color: orange; text-decoration: none;">Login here!</router-link>
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
      form: {
        user_name: '',
        user_email: '',
        user_password: '',
        user_confirm_password: ''
      },
      errorMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      if (this.form.user_password !== this.form.user_confirm_password) {
          this.errorMessage = "Passwords do not match";
          return;
      }

      try {
        const formData = new FormData();
        Object.keys(this.form).forEach(key => formData.append(key, this.form[key]));

        const response = await this.$axios.post('/register', formData);

        if (response.status === 201) {
          alert("Registration Successful!");
          this.$router.push('/login');
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Registration Failed";
      }
    }
  }
}
</script>
