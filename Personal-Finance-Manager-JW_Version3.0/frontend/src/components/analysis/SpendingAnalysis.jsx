import React from 'react';
import SpendingChart from './SpendingChart';
import './analysis.css';

const SpendingAnalysis = ({ data }) => {
  return (
    <div className="analysis-container">
      <div className="recommendations">
        <h3>Spending Recommendations</h3>
        {data.recommendations?.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <h4>{rec.category}</h4>
            <p>Current Budget: ${rec.current_budget}</p>
            <p>Recommended: ${rec.recommended_budget}</p>
            <p>{rec.reason}</p>
          </div>
        ))}
      </div>
      <SpendingChart data={data.visualizations} />
    </div>
  );
};

export default SpendingAnalysis;