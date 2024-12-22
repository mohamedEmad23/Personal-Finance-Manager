import React, { useState, useEffect } from 'react';
import './FormModal.css';

const categories = ['food', 'transport', 'utilities', 'entertainment', 'shopping', 'health', 'other'];

const BudgetFormModal = ({ initialData = {}, onSubmit, onClose, isEditMode = false }) => {
  const [formData, setFormData] = useState({
    category: initialData.category || '',
    amount: initialData.amount || '',
    start_date: initialData.start_date || '',
    end_date: initialData.end_date || '',
  });

  useEffect(() => {
    setFormData({
      category: initialData.category || '',
      amount: initialData.amount || '',
      start_date: initialData.start_date || '',
      end_date: initialData.end_date || '',
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
        <h2>{isEditMode ? 'Edit Budget' : 'Create Budget'}</h2>
        <form onSubmit={handleSubmit}>
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
            Start Date:
            <input
              type="date"
              name="start_date"
              value={formData.start_date || new Date().toISOString().split('T')[0]}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            End Date:
            <input
              type="date"
              name="end_date"
              value={formData.end_date}
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

export default BudgetFormModal;
