import React, { useState, useEffect } from 'react';
import './FormModal.css';

const IncomeFormModal = ({ initialData, onSubmit, onClose, isEditMode }) => {
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
        frequency: initialData.frequency || 'once',
        source: initialData.source || '',
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
        <h2>{isEditMode ? 'Edit Income' : 'Create Income'}</h2>
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
            Frequency:
            <select
              name="frequency"
              value={formData.frequency}
              onChange={handleChange}
              required
            >
              <option value="once">Once</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
          </label>
          <label>
            Source:
            <input
              type="text"
              name="source"
              value={formData.source}
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

export default IncomeFormModal;
