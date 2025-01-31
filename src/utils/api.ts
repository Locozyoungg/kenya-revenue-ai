import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const fetchMpesaTransactions = async () => {
  const response = await axios.get(`${API_BASE_URL}/mpesa/transactions`);
  return response.data;
};

export const submitTaxReturn = async (data: any) => {
  const response = await axios.post(`${API_BASE_URL}/tax/submit`, data);
  return response.data;
};