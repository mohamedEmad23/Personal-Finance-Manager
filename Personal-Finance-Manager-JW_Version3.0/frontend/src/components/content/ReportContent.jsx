import React from 'react';
import ReportFormModal from '../FormModal/ReportFormModal';

const ReportContent = ({
  reports,
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
        <h1>Reports</h1>
        <div className="budget-buttons">
          <button
            className="create-button"
            onClick={(e) => {
              e.stopPropagation();
              setEditingItem(null);
              setModalOpen(true);
            }}
          >
            Create Report
          </button>
        </div>
      </div>
      <div className="budget-cards">
        {reports.length === 0 ? (
          <p>No reports available.</p>
        ) : (
          reports.map((report) => (
            <div key={report.id} className="budget-card">
              <div className="card-header">
                <button
                  className="menu-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleMenu(report.id);
                  }}
                >
                  &#x22EE;
                </button>
                <div className={`dropdown-menu ${menuVisible[report.id] ? 'show' : ''}`}>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteItem(report.id, 'report');
                    }}
                  >
                    Delete
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditingItem(report);
                      setModalOpen(true);
                    }}
                  >
                    Update
                  </button>
                </div>
              </div>
              <h3>{report.title}</h3>
              <p><strong>Type:</strong> {report.report_type}</p>
              <p><strong>Format:</strong> {report.format}</p>
              <p><strong>Start Date:</strong> {new Date(report.start_date).toLocaleDateString()}</p>
              <p><strong>End Date:</strong> {new Date(report.end_date).toLocaleDateString()}</p>
              <a
                href={report.file_path}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
              >
                Download Report
              </a>
            </div>
          ))
        )}
      </div>
      {isModalOpen && (
        <ReportFormModal
          initialData={editingItem ? {
            report_type: editingItem.report_type,
            format: editingItem.format,
            start_date: editingItem.start_date,
            end_date: editingItem.end_date,
            title: editingItem.title,
            description: editingItem.description,
            file_path: editingItem.file_path
          } : {}}
          onSubmit={(formData) => {
            if (editingItem) {
              handleUpdateItem(editingItem.id, formData, 'report');
            } else {
              handleCreateItem(formData, 'report');
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

export default ReportContent;
