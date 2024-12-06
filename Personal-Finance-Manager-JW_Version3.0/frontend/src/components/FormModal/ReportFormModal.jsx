import React, { useState } from 'react';
import Modal from 'react-modal';
import './FormModal.css';

const ReportFormModal = ({ initialData, onSubmit, onClose, isEditMode }) => {
  const [formData, setFormData] = useState({
    report_type: initialData.report_type || '',
    format: initialData.format || '',
    start_date: initialData.start_date || '',
    end_date: initialData.end_date || '',
    title: initialData.title || '',
    description: initialData.description || '',
    file_path: initialData.file_path || ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Modal isOpen={true} onRequestClose={onClose} contentLabel="Report Form Modal">
      <h2>{isEditMode ? 'Edit Report' : 'Create Report'}</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Report Type:
          <select name="report_type" value={formData.report_type} onChange={handleChange} required>
            <option value="">Select Report Type</option>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
            <option value="budget">Budget</option>
            <option value="summary">Summary</option>
          </select>
        </label>
        <label>
          Format:
          <select name="format" value={formData.format} onChange={handleChange} required>
            <option value="">Select Format</option>
            <option value="pdf">PDF</option>
            <option value="csv">CSV</option>
            <option value="excel">Excel</option>
          </select>
        </label>
        <label>
          Start Date:
          <input type="date" name="start_date" value={formData.start_date} onChange={handleChange} required />
        </label>
        <label>
          End Date:
          <input type="date" name="end_date" value={formData.end_date} onChange={handleChange} required />
        </label>
        <label>
          Title:
          <input type="text" name="title" value={formData.title} onChange={handleChange} required />
        </label>
        <label>
          Description:
          <textarea name="description" value={formData.description} onChange={handleChange} />
        </label>
        <label>
          File Path (optional):
          <input type="text" name="file_path" value={formData.file_path} onChange={handleChange} />
        </label>
        <button type="submit">{isEditMode ? 'Update' : 'Create'}</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </Modal>
  );
};

export default ReportFormModal;