
import pandas as pd
import numpy as np

# Read CPI data, skipping the first 8 lines to find data
df = pd.read_csv("CPI.csv", skiprows=8)

# Display the first five rows
print(df.head(5))

# Display the last two rows
print(df.tail(2))

# Display column names
print(df.columns)

# Rename the CPI column
df["CPI"] = df["STATIC_INFLATIONCALC"]

# Calculate annual inflation
df["Annual Inflation"] = np.array((df["CPI"] / df["CPI"].shift(12) - 1) * 100)

# Display the first 15 rows
print(df.head(15))

import matplotlib.pyplot as plt

# Create a graph of Canadian CPI
fig, ax = plt.subplots()

# Plot CPI over time
ax.plot(df.index, df["CPI"], label="Canadian CPI")

# Add title and axis labels
ax.set_title("Canadian CPI and Annual Inflation (1914–2026)")
ax.set_xlabel("Year")
ax.set_xticks([0, 240, 480, 720, 960, 1200, 1344])
ax.set_xticklabels(["1914", "1934", "1954", "1974",
                    "1994", "2014", "2026"])
ax.set_ylabel("CPI")
ax.plot(df.index, df["CPI"] * 0 + 100,
        "k:", label="CPI Base Level (100)")
# Create a right-hand axis for annual inflation 
ax2 = ax.twinx()

# Plot annual inflation
ax2.plot(df.index, df["Annual Inflation"],
         color="red", label="Annual Inflation (%)")

ax2.set_ylabel("Annual Inflation (%)")
# Add legends
ax.legend(loc="upper left")
ax2.legend(loc="upper right")

# Save and display the graph
plt.savefig("CPI_Graph.png")

# Canadian Inflation Calculator
print("Canadian Inflation Calculator")

amount = float(input("Enter original price: $"))

start_year = int(input("Enter starting year: "))
start_month = int(input("Enter starting month: "))

end_year = int(input("Enter ending year: "))
end_month = int(input("Enter ending month: "))

# Check inputs
if amount <= 0:
    print("Invalid price")

elif start_month < 1 or start_month > 12:
    print("Invalid starting month")

elif end_month < 1 or end_month > 12:
    print("Invalid ending month")

elif start_year > end_year or (start_year == end_year and start_month >= end_month):
    print("Invalid date order")

else:
    # Create dates
    start_date = str(start_year) + "-" + "{:02d}".format(start_month) + "-01"
    end_date = str(end_year) + "-" + "{:02d}".format(end_month) + "-01"

    # Find CPI data
    start_data = df[df["date"] == start_date]
    end_data = df[df["date"] == end_date]

    if len(start_data) == 0 or len(end_data) == 0:
        print("Date not available in CPI data")

    else:
        start_cpi = start_data["CPI"].iloc[0]
        end_cpi = end_data["CPI"].iloc[0]

        # Calculations
        adjusted_price = amount * end_cpi / start_cpi
        percentage_change = (end_cpi / start_cpi - 1) * 100

        months = (end_year - start_year) * 12 + end_month - start_month
        years = months / 12

        annual_rate = ((end_cpi / start_cpi) ** (1 / years) - 1) * 100

        # Results
        print("Original price: ${:.2f}".format(amount))
        print("Starting CPI:", start_cpi)
        print("Ending CPI:", end_cpi)
        print("Adjusted price: ${:.2f}".format(adjusted_price))
        print("Percentage change: {:.2f}%".format(percentage_change))
        print("Number of years: {:.2f}".format(years))
        print("Annual inflation rate: {:.2f}%".format(annual_rate))


plt.show()