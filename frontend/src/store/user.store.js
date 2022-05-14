import { loginUser, fetchAccounts } from "@/service/user.service"

const userStore = {
  state() {
    return {
      user: {},
      accounts: []
    }
  },
  mutations: {
    SET_USER(state, data) {
      state.user = data;
    },
    SET_ACCOUNTS(state, data) {
      state.accounts = data
    }
  },
  actions: {
    async login({ commit }, data) {
      try {
        const response = await loginUser(data);
        sessionStorage.setItem("token", response.data.token)
        sessionStorage.setItem("user_id", response.data.account.id)
        commit('SET_USER', response.data);
      } catch (error) {
        console.log(error);
      }
    },
    async getAllAccounts({ commit }) {
      try {
        const response = await fetchAccounts();
        commit('SET_ACCOUNTS', response.data);
      } catch (error) {
        console.log(error);
      }
    }
  },
  getters: {
    getUser: state => state.user,
    getAccounts: state => state.accounts
  },
  namespaced: true
};

export default userStore;
