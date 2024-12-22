import React from 'react';
import ExpenseFormModal from '../FormModal/ExpenseFormModal';

const ExpenseContent = ({ 
  expenses, 
  menuVisible, 
  toggleMenu, 
  deleteItem, 
  setEditingItem, 
  setModalOpen, 
  editingItem, 
  handleUpdateItem, 
  handleCreateItem,
  isModalOpen
}) => {
  return (
    <div className="budget-content">
      <div className="budget-header">
        <h1>Expenses</h1>
        <div className="budget-buttons">
          <button 
            className="filter-button" 
            onClick={(e) => {
              e.stopPropagation();
              console.log('Filter button clicked');
            }}
          >
            Filter
          </button>
          <button 
            className="create-button" 
            onClick={(e) => {
              e.stopPropagation();
              setEditingItem(null);
              setModalOpen(true);
            }}
          >
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
              <div className="card-header">
                <button 
                  className="menu-button" 
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleMenu(expense.id);
                  }}
                >
                  &#x22EE;
                </button>
                <div className={`dropdown-menu ${menuVisible[expense.id] ? 'show' : ''}`}>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteItem(expense.id, 'expense');
                    }}
                  >
                    Delete
                  </button>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditingItem(expense);
                      setModalOpen(true);
                    }}
                  >
                    Update
                  </button>
                </div>
              </div>
              <h2>{expense.category}</h2>
              <p><strong>Amount:</strong> ${expense.amount}</p>
              <p><strong>Description:</strong> {expense.description}</p>
              <p><strong>Date recorded:</strong> {new Date(expense.created_at).toLocaleDateString()}</p>
            </div>
          ))
        )}
      </div>
      {isModalOpen && (
        <ExpenseFormModal
          initialData={editingItem ? {
            amount: editingItem.amount,
            description: editingItem.description,
            category: editingItem.category
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
          isEditMode={!!editingItem}
        />
      )}
    </div>
  );
};

export default ExpenseContent;