import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Line, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const SpendingChart = ({ data }) => {
  return (
    <div className="charts-container">
      <div className="chart">
        <h3>Monthly Spending</h3>
        <Line data={data.monthly_spending} />
      </div>
      <div className="chart">
        <h3>Category Distribution</h3>
        <Pie data={data.category_distribution} />
      </div>
    </div>
  );
};

export default SpendingChart;