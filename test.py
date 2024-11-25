import pandas as pd

# File path
file_path = './billing/transactions.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Ensure that 'Amount' is treated as a numeric column (convert to float)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

# Drop rows where the Merchant is 'Transfer out'
df = df[df['Merchant'] != 'Transfer out']

# Replace 'Shao Xiang Ju' with 'Shui Zhu Rou'
df['Merchant'] = df['Merchant'].replace('Shao Xiang Ju', 'Shui Zhu Rou')

# Filter rows where the Amount is negative (expenses)
expenses_df = df[df['Amount'] < 0]

# Filter rows where the Amount is positive (income)
income_df = df[df['Amount'] > 0]

# Group by Merchant and sum the Amounts (expenses)
merchant_expenses = expenses_df.groupby('Merchant')['Amount'].sum().reset_index()

# Group by Merchant and sum the Amounts (income)
merchant_income = income_df.groupby('Merchant')['Amount'].sum().reset_index()

# Sort the data by the summed Amount (expenses), in ascending order
sorted_expenses = merchant_expenses.sort_values(by='Amount', ascending=True)

# Sort the data by the summed Amount (income), in descending order
sorted_income = merchant_income.sort_values(by='Amount', ascending=False)

# Create a new 'ID' column (unique identifier for each merchant for both income and expenses)
sorted_expenses['ID'] = range(1, len(sorted_expenses) + 1)
sorted_income['ID'] = range(1, len(sorted_income) + 1)

# Calculate Total Expense and Total Income
total_expense = expenses_df['Amount'].sum()
total_income = income_df['Amount'].sum()

# Display the results with the new ID column and totals
print("Expenses:")
print(sorted_expenses[['ID', 'Merchant', 'Amount']])
print(f"Total Expense: {total_expense:.2f}\n")

print("Income:")
print(sorted_income[['ID', 'Merchant', 'Amount']])
print(f"Total Income: {total_income:.2f}")

regexPattern = {
    "Shopping": ["Loblaw", "H-Mart", "7 Eleven Store", "Dollarama", "Shoppers Drug Mart"],
    "cafe": ["The Oats Kafe", "Tim Hortons"],
    "Restaurant": ["Shui Zhu Rou", "Le Lert", "Nando's", "Dahu Hotpot", "Seoulgamjatang", "Mr Fish", "Happy Lamb Hot Pot", "Bingz Crispy Burger", "Jimmy The Greek", "Jollibee", "Mcdonald's"],
    "Transit": ["Presto Fare", "Uber* Pending", "Uber Canada/Ubertrip", "Uber* Trip"],
    "Health": ["Shining Stars Health C"],
    "Entertainme": ["Cineplex"],
    "Electronic": ["Walmart.ca", "Amazon.ca", "Amazon.com", "Apple.com", "hsjs"],
    "Subscription": ["Tst-Globol", "Apple.com/Bill"],
    "Other": ["Momentum Plus", "Cu"],
}