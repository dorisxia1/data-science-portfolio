import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/risk-hotspots',
    name: 'Risk Hotspots',
    component: () => import('../views/RiskHotspotsView.vue')
  },
  {
    path: '/demographic-patterns',
    name: 'Demographic Patters',
    component: () => import('../views/DemographicView.vue')
  }
  ,
  {
    path: '/medicare-coverage',
    name: 'Medicare Coverage',
    component: () => import('../views/MedicareView.vue')
  },
  {
    path: '/environmental-risks',
    name: 'Environmental Risks',
    component: () => import('../views/EnvironmentalView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
export { router }; // Add this export to allow importing the router instance