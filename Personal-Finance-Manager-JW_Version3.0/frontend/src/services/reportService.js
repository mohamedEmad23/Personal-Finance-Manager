import api from '../api';

export const plotIncomeExpense = async (userId, startDate, endDate) => {
  return api.get('/reports/plot_income_expense/', {
    params: { user_id: userId, start_date: startDate, end_date: endDate }
  });
};

export const generateTransactionsFile = async (userId, reportData, fileFormat) => {
  return api.get('/reports/generate_transactions_file/', {
    params: { user_id: userId, ...reportData, file_format: fileFormat }
  });
};

export const analyzeSpending = async (userId) => {
  return api.post(`/reports/analyze-spending/${userId}`);
};