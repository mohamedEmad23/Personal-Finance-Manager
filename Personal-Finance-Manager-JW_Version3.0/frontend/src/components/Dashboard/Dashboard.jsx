import React, { useEffect, useState } from 'react';
import Navbar from '../Navbar/Navbar';
import Sidebar from '../Sidebar/Sidebar';
import './Dashboard.css';
import { useLocation } from 'react-router-dom';
import api from '../../api';
import BudgetFormModal from '../FormModal/BudgetFormModal';
import IncomeFormModal from '../FormModal/IncomeFormModal'; // Assuming you'll create a similar modal for income
import ExpenseFormModal from '../FormModal/ExpenseFormModal'
import { toast } from 'react-toastify';

const Dashboard = () => {
  const [activePage, setActivePage] = useState(''); // Tracks the active sidebar button
  const location = useLocation();
  const { userId } = location.state || {}; // Extract userId from location state
  const [budgets, setBudgets] = useState([]);
  const [incomes, setIncomes] = useState([]); // State for incomes
  const [expenses, setExpenses] = useState([]);
  const [menuVisible, setMenuVisible] = useState({});
  const [isModalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null); // Can handle both budget and income updates

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
        deleteEndpoint = 'budgets/budgets/';
        break;
      case 'income':
        deleteEndpoint = 'income/incomes/';
        break;
      case 'expense':
        deleteEndpoint = 'expenses/expenses/';
        break;
      default:
        console.error('Invalid type:', type);
        return; // Exit early if the type is not valid
    }
    api
        .delete(`${deleteEndpoint}${id}`)
        .then(() => {
        if (type === 'budget') {
            setBudgets(budgets.filter((budget) => budget.id !== id));
        } else if (type === 'income') {
            setIncomes(incomes.filter((income) => income.id !== id));
        } else if (type === 'expense') {
            setExpenses(expenses.filter((expenses) => expenses.id !==id));
        }
        })
        .catch((error) => {
        console.error(`Error deleting ${type}:`, error);
        });
    };

    const handleCreateItem = (formData, type) => {
        let createEndpoint;
        let newItem;
      
        switch (type) {
          case 'budget':
            createEndpoint = 'budgets/budgets/';
            newItem = {
              category: formData.category,
              amount: Number(formData.amount),
              start_date: formData.start_date || new Date().toISOString(),
              end_date: formData.end_date || new Date().toISOString(),
            };

            // Check if the category already exists in budgets
            const categoryExists = budgets.some((budget) => budget.category === formData.category);
            if (categoryExists) {
              toast.error(`A budget for the category "${formData.category}" already exists.`);
              return; // Exit early to prevent API call
            }
            break;
      
          case 'income':
            createEndpoint = 'income/incomes/';
            newItem = {
              amount: Number(formData.amount),
              description: formData.description,
              frequency: formData.frequency,
              source: formData.source,
            };
            break;
      
          case 'expense':
            createEndpoint = 'expenses/expenses/';
            newItem = {
              amount: Number(formData.amount),
              category: formData.category,
              description: formData.description,
              date: formData.date || new Date().toISOString(),
            };
      

            break;
      
          default:
            toast.error('Invalid type selected.');
            return;
        }
      
        if (userId) {
          api
            .post(createEndpoint, newItem, {
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
      
                  // Update the current_usage of the budget for the expense's category
                  const updatedBudgets = budgets.map((budget) =>
                    budget.category === formData.category
                      ? { ...budget, current_usage: budget.current_usage + Number(formData.amount) }
                      : budget
                  );
                  setBudgets(updatedBudgets);
                  break;
      
                default:
                  break;
              }
              setModalOpen(false);
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
            updateEndpoint = `budgets/budgets/${itemId}/`;
            break;
          case 'income':
            updateEndpoint = `income/incomes/${itemId}/`;
            break;
        case 'expense':
            updateEndpoint = `expenses/expenses/${itemId}/`;
            break;
          default:
            console.error('Invalid type:', type);
            return; // Exit early if the type is invalid
        }
      
        api
          .put(updateEndpoint, updatedData)
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
              default:
                break;
            }
            setEditingItem(itemId);
            setModalOpen(false);
          })
          .catch((error) => {
            console.error(`Error updating ${type}:`, error);
          });
      };
      
  const renderContent = () => {
    switch (activePage) {
      case 'budget':
        return (
          <div className="budget-content">
            <div className="budget-header">
              <h1>Budgets</h1>
              <div className="budget-buttons">
                <button className="filter-button">Filter</button>
                <button className="create-button" onClick={() => setModalOpen(true)}>
                  Create
                </button>
              </div>
            </div>
            <div className="budget-cards">
              {budgets.length === 0 ? (
                <p>No budgets available.</p>
              ) : (
                budgets.map((budget) => (
                  <div key={budget.id} className="budget-card">
                    <button className="menu-button" onClick={() => toggleMenu(budget.id)}>
                      &#x22EE;
                    </button>
                    <div className={`dropdown-menu ${menuVisible[budget.id] ? 'show' : ''}`}>
                      <button onClick={() => deleteItem(budget.id, 'budget')}>Delete</button>
                      <button onClick={() => {setEditingItem(budget); setModalOpen(true);}}>Update</button>
                    </div>
                    <h3>{budget.category}</h3>
                    <p>
                      <strong>Amount:</strong> ${budget.amount}
                    </p>
                    <p>
                      <strong>Current Usage:</strong> ${budget.current_usage}
                    </p>
                    <p>
                      <strong>Start Date:</strong> {new Date(budget.start_date).toLocaleDateString()}
                    </p>
                    <p>
                      <strong>End Date:</strong> {new Date(budget.end_date).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
            {isModalOpen && (
              <BudgetFormModal
                initialData={editingItem ? {
                amount: editingItem.amount,
                description: editingItem.description, // Add description if relevant
                end_date: editingItem.end_date
              } : {}}
              onSubmit={(formData) => {
                if (editingItem) {
                  handleUpdateItem(editingItem.id, formData, 'budget');
                } else {
                  handleCreateItem(formData, 'budget');
                }
              }}
              onClose={() => {
                setModalOpen(false);
                setEditingItem(null);
              }}
              isEditMode={!!editingItem} // Pass a flag for edit mode
            />            
            )}
          </div>
        );
      case 'income':
        return (
          <div className="budget-content">
            <div className="budget-header">
              <h1>Income</h1>
              <div className="budget-buttons">
                <button className="filter-button">Filter</button>
                <button className="create-button" onClick={() => setModalOpen(true)}>
                  Create
                </button>
              </div>
            </div>
            <div className="budget-cards">
              {incomes.length === 0 ? (
                <p>No incomes available.</p>
              ) : (
                incomes.map((income) => (
                  <div key={income.id} className="budget-card">
                    <button className="menu-button" onClick={() => toggleMenu(income.id)}>
                      &#x22EE;
                    </button>
                    <div className={`dropdown-menu ${menuVisible[income.id] ? 'show' : ''}`}>
                      <button onClick={() => deleteItem(income.id, 'income')}>Delete</button>
                      <button onClick={() => {setEditingItem(income); setModalOpen(true);}}>Update</button>
                    </div>
                    <h2>{income.source}</h2>
                    <p>
                      <strong>Amount:</strong> ${income.amount}
                    </p>
                    <p>
                      <strong>Description:</strong> {income.description}
                    </p>
                    <p>
                      <strong>Frequency:</strong> {income.frequency}
                    </p>
                    <p>
                      <strong>Date:</strong> {new Date(income.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
            {isModalOpen && (
              <IncomeFormModal
                initialData={editingItem ? {
                amount: editingItem.amount,
                description: editingItem.description, // Add description
                frequency: editingItem.frequency, // Add frequency
                source: editingItem.source // Add source
              } : {}}
              onSubmit={(formData) => {
                if (editingItem) {
                  handleUpdateItem(editingItem.id, formData, 'income');
                } else {
                  handleCreateItem(formData, 'income');
                }
              }}
              onClose={() => {
                setModalOpen(false);
                setEditingItem(null);
              }}
              isEditMode={!!editingItem} // Pass a flag for edit mode
            />            
            )}
          </div>
        );
        case 'expenses':
        return (
          <div className="budget-content">
            <div className="budget-header">
              <h1>Expenses</h1>
              <div className="budget-buttons">
                <button className="filter-button">Filter</button>
                <button className="create-button" onClick={() => setModalOpen(true)}>
                  Add
                </button>
              </div>
            </div>
            <div className="budget-cards">
              {expenses.length === 0 ? (
                <p>No expenses recorded.</p>
              ) : (
                expenses.map((expense) => (
                  <div key={expense.id} className="budget-card">
                    <button className="menu-button" onClick={() => toggleMenu(expense.id)}>
                      &#x22EE;
                    </button>
                    <div className={`dropdown-menu ${menuVisible[expense.id] ? 'show' : ''}`}>
                      <button onClick={() => deleteItem(expense.id, 'expense')}>Delete</button>
                      <button onClick={() => {setEditingItem(expense); setModalOpen(true);}}>Update</button>
                    </div>
                    <h2>{expense.category}</h2>
                    <p>
                      <strong>Amount:</strong> ${expense.amount}
                    </p>
                    <p>
                      <strong>Description:</strong> {expense.description}
                    </p>
                    <p>
                      <strong>Date recorded:</strong> {new Date(expense.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
            {isModalOpen && (
              <ExpenseFormModal
                initialData={editingItem ? {
                amount: editingItem.amount,
                description: editingItem.description, // Add description
                category: editingItem.category // Add source
              } : {}}
              onSubmit={(formData) => {
                if (editingItem) {
                  handleUpdateItem(editingItem.id, formData, 'expense');
                } else {
                  handleCreateItem(formData, 'expense');
                }
              }}
              onClose={() => {
                setModalOpen(false);
                setEditingItem(null);
              }}
              isEditMode={!!editingItem} // Pass a flag for edit mode
            />            
            )}
          </div>
        );
      case 'reports':
        return <h3>Reports Page</h3>;
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
