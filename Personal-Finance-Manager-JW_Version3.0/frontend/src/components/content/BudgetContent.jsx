import React from 'react';
import BudgetFormModal from '../FormModal/BudgetFormModal';

const BudgetContent = ({ 
  budgets, 
  menuVisible, 
  toggleMenu, 
  deleteItem, 
  setEditingItem, 
  setModalOpen, 
  editingItem, 
  handleUpdateItem, 
  handleCreateItem,
  isModalOpen  // Add this prop
}) => {
  return (
    <div className="budget-content">
      <div className="budget-header">
        <h1>Budgets</h1>
        <div className="budget-buttons">
          <button 
            className="filter-button" 
            onClick={() => console.log('Filter button clicked')}
          >
            Filter
          </button>
          <button 
            className="create-button" 
            onClick={() => {
              setEditingItem(null);
              setModalOpen(true);
            }}
          >
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
              <div className="card-header">
                <button 
                  className="menu-button" 
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleMenu(budget.id);
                  }}
                >
                  &#x22EE;
                </button>
                <div className={`dropdown-menu ${menuVisible[budget.id] ? 'show' : ''}`}>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteItem(budget.id, 'budget');
                    }}
                  >
                    Delete
                  </button>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditingItem(budget);
                      setModalOpen(true);
                    }}
                  >
                    Update
                  </button>
                </div>
              </div>
              <h3>{budget.category}</h3>
              <p><strong>Amount:</strong> ${budget.amount}</p>
              <p><strong>Current Usage:</strong> ${budget.current_usage}</p>
              <p><strong>Start Date:</strong> {new Date(budget.start_date).toLocaleDateString()}</p>
              <p><strong>End Date:</strong> {new Date(budget.end_date).toLocaleDateString()}</p>
            </div>
          ))
        )}
      </div>
      {isModalOpen && (
        <BudgetFormModal
          initialData={editingItem ? {
            category: editingItem.category,
            amount: editingItem.amount,
            start_date: editingItem.start_date,
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
          isEditMode={!!editingItem}
        />
      )}
    </div>
  );
};

export default BudgetContent;