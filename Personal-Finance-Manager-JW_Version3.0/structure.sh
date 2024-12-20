#!/bin/bash

# Create the project directory structure
mkdir -p personal-finance-manager-backend/app/{api,core,models,schemas,services,utils}
mkdir -p personal-finance-manager-backend/tests

# Create the necessary files
touch personal-finance-manager-backend/app/{__init__.py,main.py}
touch personal-finance-manager-backend/app/api/{__init__.py,auth.py,users.py,income.py,expenses.py,budgets.py,reports.py}
touch personal-finance-manager-backend/app/core/{__init__.py,config.py,security.py,recommendations.py}
touch personal-finance-manager-backend/app/models/{__init__.py,user.py,income.py,expense.py,budget.py}
touch personal-finance-manager-backend/app/schemas/{__init__.py,user.py,income.py,expense.py,budget.py}
touch personal-finance-manager-backend/app/services/{__init__.py,auth_service.py,income_service.py,expense_service.py,budget_service.py,recommendation_service.py}
touch personal-finance-manager-backend/app/utils/{__init__.py,validators.py,helpers.py}
touch personal-finance-manager-backend/tests/{__init__.py,test_auth.py,test_income.py,test_expenses.py,test_budgets.py}
touch personal-finance-manager-backend/requirements.txt
touch personal-finance-manager-backend/alembic.ini
touch personal-finance-manager-backend/README.md