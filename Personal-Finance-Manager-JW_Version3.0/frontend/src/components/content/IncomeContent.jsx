import React from 'react';
import IncomeFormModal from '../FormModal/IncomeFormModal';

const IncomeContent = ({ incomes, menuVisible, toggleMenu, deleteItem, setEditingItem, setModalOpen, editingItem, handleUpdateItem, handleCreateItem }) => {
  return (
    <div className="budget-content">
      <div className="budget-header">
        <h1>Income</h1>
        <div className="budget-buttons">
          <button className="filter-button" onClick={() => console.log('Filter button clicked')}>Filter</button>
          <button className="create-button" onClick={() => { setEditingItem(null); setModalOpen(true); }}>
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
                <button onClick={() => { setEditingItem(income); setModalOpen(true); }}>Update</button>
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
      {editingItem !== null && (
        <IncomeFormModal
          initialData={editingItem ? {
            amount: editingItem.amount,
            description: editingItem.description,
            frequency: editingItem.frequency,
            source: editingItem.source
          } : {}}
          onSubmit={(formData) => {
            if (editingItem) {
              handleUpdateItem(editingItem.id, formData, 'income');
            } else {
              handleCreateItem(formData, 'income');
            }
          }}
          onClose={() => { setModalOpen(false); setEditingItem(null); }}
          isEditMode={!!editingItem}
        />
      )}
    </div>
  );
};

export default IncomeContent;
