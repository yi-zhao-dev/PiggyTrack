import csv
from datetime import datetime, timedelta

# Define the input and output file names
input_file = "./billing/2024-11.txt"
output_file = "./billing/transactions.csv"

# Function to parse the text file and extract transactions
def parse_transactions(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    transactions = []
    current_date = None
    merchant = None
    payment_method = "Cash"  # Assuming all entries use cash based on the provided input
    amount = None

    for line in lines:
        line = line.strip()

        # Identify and store the date
        if line.lower() in ["today", "yesterday"] or "2024" in line:
            if line.lower() == "today":
                current_date = datetime.today().strftime("%Y-%m-%d")
            elif line.lower() == "yesterday":
                current_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                current_date = datetime.strptime(line, "%B %d, %Y").strftime("%Y-%m-%d")
        elif line:  # Process non-empty lines
            if "Purchase" in line or "INTERAC e-Transfer®" in line:
                # Skip purchase lines since they don't contain new information
                continue
            elif line.startswith("−") or line.startswith("$"):
                # Extract and clean the amount
                amount = line.replace("−", "").replace("$", "").replace("CAD", "").strip()
                
                # If the amount was negative (indicated by the "−"), make it negative
                if line.startswith("−"):
                    amount = "-" + amount
                
                # Append the transaction after collecting all data
                if current_date and merchant and amount:
                    transactions.append([current_date, merchant, payment_method, amount])
                # Reset merchant and amount for the next transaction
                merchant = None
                amount = None
            elif line.lower() == "pending":
                # Skip status lines as status is no longer needed
                continue
            else:
                # Assume it’s the merchant if it’s not the above conditions
                if not merchant:
                    merchant = line

    return transactions

# Write the transactions to a CSV file
def write_to_csv(transactions, output_file):
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(["Date", "Merchant", "Payment Method", "Amount"])
        # Write the transaction data
        writer.writerows(transactions)

# Main function to process the file
def main():
    transactions = parse_transactions(input_file)
    write_to_csv(transactions, output_file)
    print(f"Transactions have been written to {output_file}.")

# Run the script
if __name__ == "__main__":
    main()