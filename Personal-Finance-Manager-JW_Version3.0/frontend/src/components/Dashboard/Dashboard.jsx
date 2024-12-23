import React, { useEffect, useState } from 'react';
import Navbar from '../Navbar/Navbar';
import Sidebar from '../Sidebar/Sidebar';
import './Dashboard.css';
import { useLocation } from 'react-router-dom';
import api from '../../api';
import BudgetContent from '../content/BudgetContent';
import IncomeContent from '../content/IncomeContent';
import ExpenseContent from '../content/ExpenseContent';
import ReportContent from '../content/ReportContent';
import { toast } from 'react-toastify';

const Dashboard = () => {
  const [activePage, setActivePage] = useState('');
  const location = useLocation();
  const { userId } = location.state || {};
  const [budgets, setBudgets] = useState([]);
  const [incomes, setIncomes] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [reports, setReports] = useState([]);
  const [menuVisible, setMenuVisible] = useState({});
  const [isModalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);

  useEffect(() => {
    if (userId) {
      // Fetch budgets for the user
      api
        .get(`budgets/budgets/`, { params: { user_id: userId } })
        .then((response) => {
          if (response.data) {
            setBudgets(response.data); // Store the fetched budgets
          } else {
            console.error('No budgets found');
          }
        })
        .catch((error) => {
          console.error('Error fetching budgets:', error);
        });

      // Fetch incomes for the user
      api
        .get('income/income/incomes', { params: { user_id: userId } })
        .then((response) => {
          if (response.data) {
            setIncomes(response.data); // Store the fetched incomes
          } else {
            console.error('No incomes found');
          }
        })
        .catch((error) => {
          console.error('Error fetching incomes:', error);
        });

        api
            .get('expenses/expenses', { params: { user_id: userId } })
            .then((response) => {
            if (response.data) {
                setExpenses(response.data); // Store the fetched incomes
            } else {
                console.error('No expenses found');
            }
            })
            .catch((error) => {
            console.error('Error fetching expenses:', error);
        });
         // New Code Snippet !!!!!!!!!!!!
         api.get('reports/user/' + userId)
        .then(response => setReports(response.data || []))
        .catch(error => console.error('Error fetching reports:', error));
    }
  }, [userId]);

  const toggleMenu = (id) => {
    setMenuVisible((prevState) => ({
      ...prevState,
      [id]: !prevState[id],
    }));
  };

  const deleteItem = (id, type) => {
    let deleteEndpoint;
    switch (type) {
      case 'budget':
        deleteEndpoint = `/budgets/budgets/${id}/`;
        break;
      case 'income':
        deleteEndpoint = `/income/incomes/${id}/`;
        break;
      case 'expense':
        deleteEndpoint = `/expenses/expenses/${id}/`;
        break;
      case 'report':
        deleteEndpoint = `/reports/${id}/`;
        break;
      default:
        console.error('Invalid type:', type);
        return;
    }
    api.delete(deleteEndpoint)
      .then(() => {
        if (type === 'budget') {
          setBudgets(budgets.filter((budget) => budget.id !== id));
        } else if (type === 'income') {
          setIncomes(incomes.filter((income) => income.id !== id));
        } else if (type === 'expense') {
          setExpenses(expenses.filter((expense) => expense.id !== id));
        } else if (type === 'report') {
          setReports(reports.filter((report) => report.id !== id));
        }
      })
      .catch((error) => {
        console.error(`Error deleting ${type}:`, error);
        toast.error(`Error deleting ${type}: ${error.message}`);
      });
  };

  const handleCreateItem = (formData, type) => {
    let createEndpoint;
    let newItem;

    switch (type) {
      case 'budget':
        createEndpoint = '/budgets/budgets/';
        newItem = {
          category: formData.category,
          amount: Number(formData.amount),
          start_date: formData.start_date || new Date().toISOString().split('T')[0],
          end_date: formData.end_date || new Date().toISOString().split('T')[0],
        };
        const categoryExists = budgets.some((budget) => budget.category === formData.category);
        if (categoryExists) {
          toast.error(`A budget for the category "${formData.category}" already exists.`);
          return;
        }
        break;
      case 'income':
        createEndpoint = '/income/incomes/';
        newItem = {
          amount: Number(formData.amount),
          description: formData.description,
          frequency: formData.frequency,
          source: formData.source,
        };
        break;
      case 'expense':
        createEndpoint = '/expenses/expenses/';
        newItem = {
          amount: Number(formData.amount),
          category: formData.category,
          description: formData.description,
          date: formData.date || new Date().toISOString().split('T')[0],
        };
        break;
      case 'report':
        createEndpoint = '/reports/';
        newItem = {
          report_type: formData.report_type,
          format: formData.format,
          start_date: formData.start_date,
          end_date: formData.end_date,
          title: formData.title,
          description: formData.description,
          file_path: formData.file_path,
        };
        break;
      default:
        toast.error('Invalid type selected.');
        return;
    }

    if (userId) {
      api.post(createEndpoint, newItem, {
        params: { user_id: userId },
      })
      .then((response) => {
        switch (type) {
          case 'budget':
            setBudgets([...budgets, response.data]);
            toast.success('Budget created successfully!');
            break;
          case 'income':
            setIncomes([...incomes, response.data]);
            toast.success('Income created successfully!');
            break;
          case 'expense':
            setExpenses([...expenses, response.data]);
            toast.success('Expense created successfully!');
            const updatedBudgets = budgets.map((budget) =>
              budget.category === formData.category
                ? { ...budget, current_usage: budget.current_usage + Number(formData.amount) }
                : budget
            );
            setBudgets(updatedBudgets);
            break;
          case 'report':
            setReports([...reports, response.data]);
            toast.success('Report created successfully!');
            break;
          default:
            break;
        }
        setModalOpen(false);
        setEditingItem(null);
      })
      .catch((error) => {
        toast.error(`Error creating ${type}: ${error.message}`);
      });
    } else {
      toast.error('User ID is missing. Cannot create item.');
    }
  };

  const handleUpdateItem = (itemId, updatedData, type) => {
    let updateEndpoint;
    switch (type) {
      case 'budget':
        updateEndpoint = `/budgets/budgets/${itemId}/`;
        break;
      case 'income':
        updateEndpoint = `/income/incomes/${itemId}/`;
        break;
      case 'expense':
        updateEndpoint = `/expenses/expenses/${itemId}/`;
        break;
      case 'report':
        updateEndpoint = `/reports/${itemId}/`;
        break;
      default:
        console.error('Invalid type:', type);
        return;
    }

    api.put(updateEndpoint, updatedData)
      .then((response) => {
        switch (type) {
          case 'budget':
            setBudgets((prevBudgets) =>
              prevBudgets.map((budget) =>
                budget.id === itemId ? { ...budget, ...response.data } : budget
              )
            );
            break;
          case 'income':
            setIncomes((prevIncomes) =>
              prevIncomes.map((income) =>
                income.id === itemId ? { ...income, ...response.data } : income
              )
            );
            break;
          case 'expense':
            setExpenses((prevExpenses) =>
              prevExpenses.map((expense) =>
                expense.id === itemId ? { ...expense, ...response.data } : expense
              )
            );
            break;
          case 'report':
            setReports(prevReports =>
              prevReports.map(report => report.id === itemId ? { ...report, ...response.data } : report));
            break;
          default:
            break;
        }
        setEditingItem(null);
        setModalOpen(false);
      })
      .catch((error) => {
        console.error(`Error updating ${type}:`, error);
        toast.error(`Error updating ${type}: ${error.message}`);
      });
  };

  const renderContent = () => {
    switch (activePage) {
      case 'budget':
        return <BudgetContent
          budgets={budgets}
          menuVisible={menuVisible}
          toggleMenu={toggleMenu}
          deleteItem={deleteItem}
          setEditingItem={setEditingItem}
          setModalOpen={setModalOpen}
          editingItem={editingItem}
          handleUpdateItem={handleUpdateItem}
          handleCreateItem={handleCreateItem}
          isModalOpen={isModalOpen}
        />;
      case 'income':
        return <IncomeContent
          incomes={incomes}
          menuVisible={menuVisible}
          toggleMenu={toggleMenu}
          deleteItem={deleteItem}
          setEditingItem={setEditingItem}
          setModalOpen={setModalOpen}
          editingItem={editingItem}
          handleUpdateItem={handleUpdateItem}
          handleCreateItem={handleCreateItem}
          isModalOpen={isModalOpen}
        />;
      case 'expenses':
        return <ExpenseContent
          expenses={expenses}
          menuVisible={menuVisible}
          toggleMenu={toggleMenu}
          deleteItem={deleteItem}
          setEditingItem={setEditingItem}
          setModalOpen={setModalOpen}
          editingItem={editingItem}
          handleUpdateItem={handleUpdateItem}
          handleCreateItem={handleCreateItem}
          isModalOpen={isModalOpen}
        />;
      case 'reports':
        return <ReportContent
          reports={reports}
          menuVisible={menuVisible}
          toggleMenu={toggleMenu}
          deleteItem={deleteItem}
          setEditingItem={setEditingItem}
          setModalOpen={setModalOpen}
          editingItem={editingItem}
          handleUpdateItem={handleUpdateItem}
          handleCreateItem={handleCreateItem}
          isModalOpen={isModalOpen}
          userId={userId}
        />;
      default:
        return <h3>Please select an option from the sidebar</h3>;
    }
  };

  return (
    <div className="dashboard">
      <Navbar />
      <div className="dashboard-content">
        <Sidebar onPageChange={setActivePage} />
        <div className="content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
