import { 
  fetchStatistics,
  fetchTransactions,
  fetchTransactionsWithFilter,
  addTransaction
} from "@/service/account.service"

const accountStore = {
  state() {
    return {
      accountData: {},
      transactionsData: []
    }
  },
  mutations: {
    SET_DATA(state, data) {
      state.accountData = data;
    },
    SET_TRANSACTIONS_DATA(state, data) {
      state.transactionsData = data;
    },
  },
  actions: {
    async getStatistics({ commit }) {
      try {
        const response = await fetchStatistics();
        commit('SET_DATA', response.data);
      } catch (error) {
        console.log(error);
      }
    },
    async getTransactions({ commit }) {
      try {
        const response = await fetchTransactions();
        commit('SET_TRANSACTIONS_DATA', response.data.transactions);
      } catch (error) {
        console.log(error);
      }
    },
    async getTransactionsWithFilter({ commit }, data) {
      try {
        const response = await fetchTransactionsWithFilter(data);
        commit('SET_TRANSACTIONS_DATA', response.data.transactions);
      } catch (error) {
        console.log(error);
      }
    },
    async addNewTransaction({ commit }, data) {
      try {
        const response = await addTransaction(data);
        commit('SET_TRANSACTIONS_DATA', response.data.transactions);
      } catch (error) {
        console.log(error);
      }
    },
  },
  getters: {
    getAccountData: state => state.accountData,
    getTransactionsData: state => state.transactionsData,
  },
  namespaced: true
};

export default accountStore;
