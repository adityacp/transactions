<template>
  <div class="q-pa-md">
    <q-layout view="hHh lpR fFf">
       <q-header elevated class="bg-primary text-white" height-hint="98">
        <q-toolbar>
          <q-btn flat @click="drawerLeft = !drawerLeft" round dense icon="menu" />
          <q-toolbar-title>Dashboard</q-toolbar-title>
        </q-toolbar>
      </q-header>
      <q-drawer
        v-model="drawerLeft"
        show-if-above
        bordered
        side="left"
      >
        <q-scroll-area class="fit">
          <q-list padding>
            <q-item
              :active="option === 1"
              clickable
              v-ripple
              active-class="my-menu-link"
              @click="toggleOption(1)">
              <q-item-section>
                Home
              </q-item-section>
            </q-item>

            <q-item
              :active="option === 2"
              clickable
              v-ripple
              active-class="my-menu-link"
              @click="toggleOption(2)">
              <q-item-section>
                My Transactions
              </q-item-section>
            </q-item>

            <q-item
              :active="option === 3"
              clickable
              v-ripple
              active-class="my-menu-link"
              @click="toggleOption(3)">
              <q-item-section>
                Add Transaction
              </q-item-section>
            </q-item>

            <q-item
              clickable
              v-ripple
              @click="logOut()">
              <q-item-section>
                Logout
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>
      <q-page-container>
        <div class="row" v-show="option === 1">
          <div class="col-6">
            <q-card class="my-card">
              <q-card-section>
                <p class="text-h5">
                  People owing me: {{ oweData.owe_me }}
                </p>
                <p class="text-h5">
                  People I owe: {{ oweData.owe_others }}
                </p>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6">
            <q-card class="my-card">
              <q-card-section>
                <p class="text-h5">
                  Total Debt: {{ accountData.total_debt }}
                </p>
                <p class="text-h5">
                  Total Lend: {{ accountData.total_lend }}
                </p>
                <p class="text-h5">
                  Balance: {{ accountData.balance }}
                </p>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <account-details v-if="option === 2" />
        <add-transaction v-if="option === 3" />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>

import { mapActions, mapGetters } from "vuex";
import { ref } from 'vue';
import AccountDetails from "@/components/AccountDetails.vue"
import AddTransaction from "@/components/AddTransaction.vue"

export default {
  name: 'Dashboard',
  setup () {
    return {
      drawerLeft: ref(false),
    }
  },
  components: {
    'account-details': AccountDetails,
    'add-transaction': AddTransaction
  },
  data() {
    return {
      dateWiseData: {},
      accountData: {},
      oweData: {},
      option: 1
    }
  },
  computed: {
    ...mapGetters({
      'getAccountData': 'Account/getAccountData'
    })
  },
  methods: {
    ...mapActions({
      'getStatistics': 'Account/getStatistics',
      'getAllAccounts': 'User/getAllAccounts'
    }),
    toggleOption(item) {
      this.option = item
    },
    logOut() {
      sessionStorage.removeItem("token");
      this.$router.push('login')
    }
  },
  async mounted() {
    await this.getStatistics();
    await this.getAllAccounts();
    this.dateWiseData = this.getAccountData.date_wise_data;
    this.accountData = this.getAccountData.account_data;
    this.oweData = this.getAccountData.owe_data
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">
.my-menu-link
  color: white
  background: #F2C037
.col-6
  padding: 10px
.col-12
  padding: 10px
</style>
