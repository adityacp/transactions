<template>
<q-page class="row justify-center items-center">
  <div class="q-pa-md login-form" style="max-width: 400px">
    <q-form
      @submit.prevent="submit"
      class="q-gutter-md"
    >
      <q-input
        filled
        v-model="user.username"
        label="Username *"
        hint="Username"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Please type your username']"
      />

      <q-input
        filled
        type="password"
        v-model="user.password"
        label="Password *"
        hint="Password"
        lazy-rules
        :rules="[
          val => val !== null && val !== '' || 'Please type your password'
        ]"
      />
      <div>
        <q-btn 
          :loading="submitting"
          label="Submit"
          type="submit"
          color="primary">
          <template v-slot:loading>
            <q-spinner />
          </template>
        </q-btn>
      </div>
    </q-form>
  </div>
</q-page>
</template>

<script>

import { mapActions, mapGetters } from "vuex";

export default {
  name: 'Login',
  data() {
    return {
      submitting: false,
      user: {
        username: "",
        password: ""
      },
      error: {}
    }
  },
  computed: {
    ...mapGetters('User', ['getUser'])
  },
  methods: {
    ...mapActions('User', ['login']),
    async submit() {
      if ( Object.keys(this.getUser).length === 0 ) {
        this.submitting = true;
        await this.login(this.user);
        this.submitting = false;
        this.$router.push("dashboard")
      }
    }
  }
}
</script>

<style scoped>
</style>
