import requests

# Define the API endpoint
url = "http://localhost:8000/api/v1/reports/plot_income_expense/"

# Define the request payload
params = {
    "user_id": 22,
    "start_date": "2023-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59"
}

# Send the POST request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Save the plot image
    with open('income_expense_plot.png', 'wb') as file:
        file.write(response.content)
    print("Plot saved as income_expense_plot.png")
else:
    print(f"Failed to generate plot: {response.status_code}")
    print(response.json())