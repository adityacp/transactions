import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createStore } from 'vuex';
import quasarUserOptions from './quasar-user-options'

import App from './App.vue'
import userStore from './store/user.store'
import accountStore from './store/account.store'
import router from "@/router";

var app = createApp(App)
const store = createStore({
  modules: {
    "User": userStore,
    "Account": accountStore
  }
});
app.use(router)
app.use(Quasar, quasarUserOptions)
app.use(store)
app.mount('#app')
