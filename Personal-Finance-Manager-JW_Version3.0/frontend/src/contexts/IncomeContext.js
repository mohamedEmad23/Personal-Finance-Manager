import React, { createContext, useState, useEffect } from 'react';
import api from '../api';

export const IncomeContext = createContext();

export const IncomeProvider = ({ children }) => {
  const [totalIncome, setTotalIncome] = useState(0);

  useEffect(() => {
    const fetchTotalIncome = async () => {
      try {
        const response = await api.get('/incomes/total');
        setTotalIncome(response.data.total_income);
      } catch (error) {
        console.error('Error fetching total income:', error);
      }
    };

    fetchTotalIncome();
  }, []);

  return (
    <IncomeContext.Provider value={{ totalIncome, setTotalIncome }}>
      {children}
    </IncomeContext.Provider>
  );
};