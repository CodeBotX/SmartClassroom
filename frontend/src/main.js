import { createApp } from 'vue'
import App from './App.vue'


// import css
import './assets/css/app.css'

// import router
import router from './router'

// import notification lib
import Notifications from '@kyvg/vue3-notification';



const app = createApp(App)
  app.use(Notifications);
  app.use(router)
  app.mount('#app')
  


