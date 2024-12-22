import React, { useState, useEffect } from 'react';
import './FormModal.css';

const categories = ['food', 'transport', 'utilities', 'entertainment', 'shopping', 'health', 'other'];

const ExpenseFormModal = ({ initialData, onSubmit, onClose, isEditMode }) => {
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    frequency: 'once',
    source: '',
  });

  useEffect(() => {
    if (isEditMode && initialData) {
      setFormData({
        amount: initialData.amount || '',
        description: initialData.description || '',
        category: initialData.category || '',
        date_recorded: initialData.Date || ''
      });
    }
  }, [isEditMode, initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="income-modal">
      <div className="modal-content">
        <h2>{isEditMode ? 'Edit Expense' : 'Add Expense'}</h2>
        <form onSubmit={handleSubmit}>
          <label>
                Category:
                <select name="category" value={formData.category || ''} onChange={handleChange} required>
                  <option value="" disabled>
                    Select a category
                  </option>
                  {categories.map((category) => (
                    <option key={category} value={category}>
                      {category}
                    </option>
                  ))}
                </select>
          </label>
          <label>
            Amount:
            <input
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Description:
            <input
              type="text"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Date recorded:
            <input
              type="date"
              name="start_date"
              value={formData.start_date || new Date().toISOString().split('T')[0]}
              onChange={handleChange}
              required
            />
          </label>
          <div className="modal-actions">
            <button className='submit-button' type="submit">{isEditMode ? 'Update' : 'Create'}</button>
            <button className='cancel-button' type="button" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ExpenseFormModal;
