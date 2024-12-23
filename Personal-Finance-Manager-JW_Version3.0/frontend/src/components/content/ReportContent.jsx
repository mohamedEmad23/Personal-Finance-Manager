import React, { useState } from 'react';
import ReportFormModal from '../FormModal/ReportFormModal';
import SpendingAnalysis from '../analysis/SpendingAnalysis';
import { analyzeSpending, plotIncomeExpense } from '../../services/reportService';
import { toast } from 'react-toastify';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

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
  isModalOpen,
  userId
}) => {
  const [analysisData, setAnalysisData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isPlotting, setIsPlotting] = useState(false);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());

  const handleAnalyzeSpending = async () => {
    try {
      setIsAnalyzing(true);
      const response = await analyzeSpending(userId);
      setAnalysisData(response.data);
      toast.success('Analysis completed successfully');
    } catch (error) {
      toast.error('Failed to analyze spending');
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handlePlotIncomeExpense = async () => {
    try {
      setIsPlotting(true);
      await plotIncomeExpense(userId, startDate.toISOString(), endDate.toISOString());
      toast.success('Plot generated successfully');
    } catch (error) {
      toast.error('Failed to generate plot');
      console.error('Plot error:', error);
    } finally {
      setIsPlotting(false);
    }
  };

  return (
    <div className="budget-content">
      <div className="budget-header">
        <h1>Reports</h1>
        <div className="budget-buttons">
          <button
            className="create-button"
            onClick={() => {
              setEditingItem(null);
              setModalOpen(true);
            }}
          >
            Create Report
          </button>
          <button
            className="analyze-button"
            onClick={handleAnalyzeSpending}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze Spending'}
          </button>
          <div className="plot-controls">
            <DatePicker
              selected={startDate}
              onChange={date => setStartDate(date)}
              selectsStart
              startDate={startDate}
              endDate={endDate}
              className="date-picker"
            />
            <DatePicker
              selected={endDate}
              onChange={date => setEndDate(date)}
              selectsEnd
              startDate={startDate}
              endDate={endDate}
              minDate={startDate}
              className="date-picker"
            />
            <button
              className="plot-button"
              onClick={handlePlotIncomeExpense}
              disabled={isPlotting}
            >
              {isPlotting ? 'Plotting...' : 'Plot Income vs Expense'}
            </button>
          </div>
        </div>
      </div>

      {analysisData && (
        <div className="analysis-section">
          <SpendingAnalysis data={analysisData} />
        </div>
      )}

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