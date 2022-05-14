import httpClient from './http-client';

const LOGIN_END_POINT = '/login';
const ACCOUNTS_END_POINT = '/accounts';

const loginUser = (data) => httpClient.post(LOGIN_END_POINT, data);
const fetchAccounts = () => httpClient.get(ACCOUNTS_END_POINT);

export {
  loginUser,
  fetchAccounts
}
