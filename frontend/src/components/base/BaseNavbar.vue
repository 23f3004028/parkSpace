<template>
  <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #28f17c;">
    <div class="container-fluid">
      
      <a class="navbar-brand" style="color: rgb(255, 0, 0); font-size: 1.62rem; font-weight: bolder;">
        ParkSpace
      </a>
      
      <div class="collapse navbar-collapse" style="font-size: 1.5rem;">
        <ul class="navbar-nav mx-auto">
           <li class="nav-item">
             <router-link to="/" class="nav-link" style="color: #990066; font-weight: bold; font-size: 2rem;">
               ParkSpace
             </router-link>
           </li>
        </ul>
        
        <ul class="navbar-nav ms-auto" style="font-size: 1.5rem;">
           <li class="nav-item">
             <router-link to="/login" class="nav-link">Login</router-link>
           </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "BaseNavbar"
}
</script>
