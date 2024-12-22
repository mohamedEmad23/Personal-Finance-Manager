# ml_service/budget_analyzer.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from ..models.budgetModel import Budget
from ..models.expenseModel import Expense
from ..models.incomeModel import Income


class BudgetAnalyzer:
    def __init__(self, db: Session):
        self.db = db
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def fetch_user_data(self, user_id: int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Fetch and preprocess user data from database."""
        # Fetch raw data
        incomes = self.db.query(Income).filter(Income.user_id == user_id).all()
        expenses = self.db.query(Expense).filter(Expense.user_id == user_id).all()
        budgets = self.db.query(Budget).filter(Budget.user_id == user_id).all()

        # Convert to DataFrames with enhanced features
        income_df = pd.DataFrame([{
            'date': income.created_at,
            'amount': income.amount,
            'type': 'income',
        } for income in incomes])

        expense_df = pd.DataFrame([{
            'date': expense.created_at,
            'amount': expense.amount,
            'category': expense.category,
            'type': 'expense',
        } for expense in expenses])

        budget_df = pd.DataFrame([{
            'start_date': budget.start_date,
            'end_date': budget.end_date,
            'amount': budget.amount,
            'category': budget.category,
            'current_usage': budget.current_usage,
            'duration_days': (budget.end_date - budget.start_date).days
        } for budget in budgets])

        return income_df, expense_df, budget_df

    def prepare_features(self, expense_df: pd.DataFrame, budget_df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for model training."""
        # Create time-based features
        expense_df['date_ordinal'] = expense_df['date'].apply(lambda x: x.toordinal())

        # Merge with budgets
        merged_data = pd.merge(
            expense_df,
            budget_df,
            on='category',
            how='left'
        )

        # Feature engineering
        merged_data['days_until_end'] = merged_data.apply(
            lambda x: (x['end_date'] - x['date']).days if pd.notnull(x['end_date']) else 0,
            axis=1
        )
        merged_data['budget_utilization'] = merged_data['current_usage'] / merged_data['amount']

        # Prepare feature matrix
        X = merged_data[[
            'date_ordinal', 'month', 'year', 'day_of_week',
            'days_until_end', 'budget_utilization'
        ]].values

        y = merged_data['amount'].values

        return X, y

    def train_model(self, user_id: int) -> Dict:
        """Train the model and return performance metrics."""
        income_df, expense_df, budget_df = self.fetch_user_data(user_id)

        if len(expense_df) < 10:  # Minimum data requirement
            return {"error": "Insufficient data for training"}

        X, y = self.prepare_features(expense_df, budget_df)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)

        return {
            "train_score": train_score,
            "test_score": test_score,
            "feature_importance": dict(zip(
                ['date', 'month', 'year', 'day_of_week', 'days_until_end', 'budget_utilization'],
                self.model.feature_importances_
            ))
        }

    def generate_recommendations(self, user_id: int) -> List[Dict]:
        """Generate budget recommendations based on spending patterns."""
        _, expense_df, budget_df = self.fetch_user_data(user_id)

        recommendations = []

        for category in expense_df['category'].unique():
            category_expenses = expense_df[expense_df['category'] == category]
            category_budget = budget_df[budget_df['category'] == category]

            if len(category_expenses) < 5:  # Skip categories with insufficient data
                continue

            # Calculate metrics
            monthly_avg = category_expenses.groupby(
                [category_expenses['date'].dt.year, category_expenses['date'].dt.month]
            )['amount'].sum().mean()

            monthly_trend = category_expenses.sort_values('date').tail(3)['amount'].mean()

            if len(category_budget) > 0:
                current_budget = category_budget.iloc[-1]['amount']
                if monthly_trend > current_budget * 1.2:  # 20% over budget
                    recommendations.append({
                        'category': category,
                        'current_budget': current_budget,
                        'recommended_budget': monthly_trend * 1.1,  # Add 10% buffer
                        'reason': 'Recent spending trend exceeds budget',
                        'metrics': {
                            'monthly_average': monthly_avg,
                            'recent_trend': monthly_trend
                        }
                    })

        return recommendations

    def generate_visualization(self, user_id: int) -> Dict:
        """Generate visualizations for spending patterns."""
        income_df, expense_df, budget_df = self.fetch_user_data(user_id)

        # Monthly trends
        monthly_expenses = expense_df.groupby(
            [expense_df['date'].dt.year, expense_df['date'].dt.month, 'category']
        )['amount'].sum().reset_index()

        # Create visualization data
        viz_data = {
            'monthly_spending': monthly_expenses.to_dict('records'),
            'category_distribution': expense_df.groupby('category')['amount'].sum().to_dict(),
            'income_vs_expenses': {
                'monthly_income': income_df.groupby(
                    [income_df['date'].dt.year, income_df['date'].dt.month]
                )['amount'].sum().to_dict(),
                'monthly_expenses': expense_df.groupby(
                    [expense_df['date'].dt.year, expense_df['date'].dt.month]
                )['amount'].sum().to_dict()
            }
        }

        return viz_data