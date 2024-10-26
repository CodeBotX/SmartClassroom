
import Vue from "vue";
import VueRouter from "vue-router";
import RouterPrefetch from "vue-router-prefetch";
import App from "./App";
// TIP: change to import router from "./router/starterRouter"; to start with a clean layout
import router from "./router/index";
import { BSpinner } from 'bootstrap-vue'

import BlackDashboard from "./plugins/blackDashboard";
import i18n from "./i18n";

import "./registerServiceWorker";

// import css
import './assets/css/styles.css'

Vue.component('b-spinner', BSpinner)
Vue.use(BlackDashboard);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);
new Vue({
  router,
  i18n,
  render: (h) => h(App),
}).$mount("#app");
