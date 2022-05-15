<template>
  <div class="q-pa-md">
    <q-card class="my-card">
      <q-card-section>
        <q-form
          @submit.prevent="submit"
          class="q-gutter-md"
        >
          <q-select
            class="element"
            v-model="transaction.type"
            :options="types"
            label="Type"
          />
          <q-select
            class="element"
            v-model="selectedUser"
            :options="accounts"
            filled
            option-label="user"
            label="User"
          ></q-select>
          <q-input
            class="element"
            filled
            v-model="transaction.reason"
            label="Reason"
            hint="Reason"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a reason']"
          />
          <q-input
            class="element"
            filled
            type="number"
            v-model="transaction.amount"
            label="Amount"
            hint="Amount"
            :min="1"
            :max="currentBalance"
          />
          <q-btn 
            :loading="submitting"
            label="Submit"
            type="submit"
            color="primary">
            <template v-slot:loading>
              <q-spinner />
            </template>
          </q-btn>
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>

import { mapActions, mapGetters } from "vuex";

export default {
  name: 'AddTransaction',
  data() {
    return {
      transaction: {
        sender_id: 0,
        receiver_id: 0,
        reason: "",
        type: "",
        status: "unpaid",
        amount: ""
      },
      submitting: false,
      types: ["borrow", "lend"],
      accounts: [],
      currentBalance: 0,
      message: '',
      currentUser: 0,
      selectedUser: ''
    }
  },
  computed: {
    ...mapGetters({
      'getAccounts': 'User/getAccounts',
      'getAccountData': 'Account/getAccountData'
    })
  },
  mounted() {
    let accountData = this.getAccounts.accounts;
    this.currentUser = parseInt(sessionStorage.getItem("user_id"))
    for(let i=0; i< accountData.length; i++) {
      this.accounts.push({
        "id": accountData[i].id,
        "user": this.getFormattedName(accountData[i].user.first_name, accountData[i].user.last_name)
      })
    }
    this.currentBalance = this.getAccountData.account_data.balance;
    this.message = 'Please enter the amount more than 0 and less than ' + this.currentBalance; 
  },
  methods: {
    ...mapActions('Account', ['addNewTransaction']),
    getFormattedName(first_name, last_name) {
      return first_name + ' ' + last_name
    },
    setUsers() {
      if (this.transaction.type === "borrow") {
        this.transaction.sender_id = this.selectedUser.id
        this.transaction.receiver_id = this.currentUser
      } else {
        this.transaction.sender_id = this.currentUser
        this.transaction.receiver_id = this.selectedUser.id
      }
    },
    async submit() {
      this.setUsers()
      console.log(this.transaction);
      this.submitting = true;
      await this.addNewTransaction(this.transaction)
      this.submitting = false;
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">
.element
  padding: 10px
</style>
