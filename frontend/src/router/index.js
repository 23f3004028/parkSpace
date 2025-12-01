import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../components/base/LandingPage.vue'
import Login from '../components/base/Login.vue'
import Register from '../components/base/Register.vue'
import AdminHome from '../components/admin/AdminHome.vue'
import AdminUsers from '../components/admin/AdminUsers.vue'
import AdminSummary from '../components/admin/AdminSummary.vue'
import AdminSearch from '../components/admin/AdminSearch.vue'
import AdminProfile from '../components/admin/AdminProfile.vue'
import UserHome from '../components/users/UserHome.vue'
import UserSummary from '../components/users/UserSummary.vue'
import UserProfile from '../components/users/UserProfile.vue'

const routes = [
  { path: '/', component: LandingPage }, 
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin/home', component: AdminHome , meta: { requiresAuth: true, role: 'admin' }},
  { path: '/admin/users', component: AdminUsers , meta: { requiresAuth: true, role: 'admin' }},
  { path: '/admin/summary', component: AdminSummary, meta: { requiresAuth: true, role: 'admin'  }},
  { path: '/admin/search', component: AdminSearch, meta: { requiresAuth: true, role: 'admin'  }},
  { path: '/admin/profile', component: AdminProfile , meta: { requiresAuth: true, role: 'admin' }},
  { path: '/user/home', component: UserHome , meta: { requiresAuth: true, role: 'user' }},
 { path: '/user/summary', component: UserSummary, meta: { requiresAuth: true, role: 'user' } },
 { path: '/user/edit_profile', component: UserProfile, meta: { requiresAuth: true, role: 'user' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('user_role');

  if (to.meta.requiresAuth) {
    
    if (!role) {
      return next('/login');
    }

    if (to.meta.role && to.meta.role !== role) {
      if (role === 'admin') return next('/admin/home');
      return next('/user/home');
    }
  }

  next();
});

export default router
