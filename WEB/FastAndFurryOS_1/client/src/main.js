import { createApp } from 'vue'
import App from './App.vue'

import { createWebHashHistory, createRouter } from 'vue-router'

import MainPage from './views/MainPage.vue'
import AboutPage from './views/AboutPage.vue'
import CarsPage from './views/CarsPage.vue'
import LoginPage from './views/LoginPage.vue'
import NotFoundComponent from './views/NotFoundComponent.vue'

const routes = [
  { path: '/', component: MainPage },
  { path: '/about', component: AboutPage },
  { path: '/cars', component: CarsPage },
  { path: '/dev_testing/furry_login', component: LoginPage },
  { path: '/:pathMatch(.*)', component: NotFoundComponent }
]

const router = createRouter({
  history: createWebHashHistory(), 
  routes,
})


createApp(App)
  .use(router)
  .mount('#app')