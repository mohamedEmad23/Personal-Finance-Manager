import React, { useState, useEffect } from 'react';
import './FormModal.css';

const categories = ['food', 'transport', 'utilities', 'entertainment', 'shopping', 'health', 'other'];

const ExpenseFormModal = ({ initialData = {}, onSubmit, onClose, isEditMode = false }) => {
  const [formData, setFormData] = useState({
    amount: initialData.amount || '',
    category: initialData.category || '',
    description: initialData.description || '',
    date: initialData.date || '',
  });

  useEffect(() => {
    setFormData({
      amount: initialData.amount || '',
      category: initialData.category || '',
      description: initialData.description || '',
      date: initialData.date || '',
    });
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="income-modal">
      <div className="modal-content">
        <h2>{isEditMode ? 'Edit Expense' : 'Create Expense'}</h2>
        <form onSubmit={handleSubmit}>
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
            Category:
            <select name="category" value={formData.category} onChange={handleChange} required>
              <option value="" disabled>Select a category</option>
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
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
            Date:
            <input
              type="date"
              name="date"
              value={formData.date || new Date().toISOString().split('T')[0]}
              onChange={handleChange}
              required
            />
          </label>
          <div className="form-buttons">
            <button className='submit-button' type="submit">{isEditMode ? 'Update' : 'Create'}</button>
            <button type="button" className="cancel-button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ExpenseFormModal;
