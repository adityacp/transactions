import httpClient from './http-client';

const STATISTICS_END_POINT = '/get_statistics';
const GET_TRANSACTIONS_END_POINT = '/get_transactions';
const ADD_TRANSACTIONS_END_POINT = '/add_transaction';

const fetchStatistics = () => httpClient.get(STATISTICS_END_POINT);
const fetchTransactions = () => httpClient.get(GET_TRANSACTIONS_END_POINT);
const fetchTransactionsWithFilter = (data) => httpClient.post(GET_TRANSACTIONS_END_POINT, data)
const addTransaction = (data) => httpClient.post(ADD_TRANSACTIONS_END_POINT, data)

export {
  fetchStatistics,
  fetchTransactions,
  fetchTransactionsWithFilter,
  addTransaction,
}
