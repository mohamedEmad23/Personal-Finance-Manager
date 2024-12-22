import React, { useState, useEffect } from 'react';
import './FormModal.css';

const ReportFormModal = ({ initialData = {}, onSubmit, onClose, isEditMode = false }) => {
  const [formData, setFormData] = useState({
    report_type: initialData.report_type || '',
    format: initialData.format || '',
    start_date: initialData.start_date || '',
    end_date: initialData.end_date || '',
    title: initialData.title || '',
    description: initialData.description || '',
    file_path: initialData.file_path || '',
  });

  useEffect(() => {
    setFormData({
      report_type: initialData.report_type || '',
      format: initialData.format || '',
      start_date: initialData.start_date || new Date().toISOString().split('T')[0],
      end_date: initialData.end_date || '',
      title: initialData.title || '',
      description: initialData.description || '',
      file_path: initialData.file_path || '',
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
        <h2>{isEditMode ? 'Edit Report' : 'Create Report'}</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Report Type:
            <input
              type="text"
              name="report_type"
              value={formData.report_type}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Format:
            <input
              type="text"
              name="format"
              value={formData.format}
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
          <label>
            Title:
            <input
              type="text"
              name="title"
              value={formData.title}
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
            File Path:
            <input
              type="text"
              name="file_path"
              value={formData.file_path}
              onChange={handleChange}
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

export default ReportFormModal;
