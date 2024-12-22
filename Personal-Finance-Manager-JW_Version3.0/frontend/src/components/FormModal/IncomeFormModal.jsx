import React, { useState, useEffect } from 'react';
import './FormModal.css';

const frequencies = ['once', 'daily', 'weekly', 'monthly', 'yearly'];

const IncomeFormModal = ({ initialData = {}, onSubmit, onClose, isEditMode = false }) => {
  const [formData, setFormData] = useState({
    amount: initialData.amount || '',
    description: initialData.description || '',
    frequency: initialData.frequency || '',
    source: initialData.source || ''
  });

  useEffect(() => {
    setFormData({
      amount: initialData.amount || '',
      description: initialData.description || '',
      frequency: initialData.frequency || '',
      source: initialData.source || ''
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
            Source:
            <input
              type="text"
              name="source"
              value={formData.source}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Frequency:
            <select name="frequency" value={formData.frequency} onChange={handleChange} required>
              <option value="" disabled>Select frequency</option>
              {frequencies.map((freq) => (
                <option key={freq} value={freq}>{freq}</option>
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
            />
          </label>
          <div className="form-buttons">
            <button className="submit-button" type="submit">
              {isEditMode ? 'Update' : 'Create'}
            </button>
            <button type="button" className="cancel-button" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default IncomeFormModal;