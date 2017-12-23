# StudentskaPrehrana
Python scraper for studentska-prehrana.si website.

## Installation
To install this package first clone it from this repository and then install it by running python setup script.
```
git clone https://github.com/drobilc/studentskaprehrana.git
python setup.py install
```

## Usage
Example program that prints names of all restaurants where you have eaten in the last 30 days, your most visited restaurant and total prices of your meals.
```python
from studentskaprehrana import StudentskaPrehrana
from datetime import datetime, timedelta

# First create an object to fetch data from website
studentska_prehrana = StudentskaPrehrana("email", "password")

# Create two datetime objects to fetch transactions
end_date = datetime.now()
start_date = end_date - datetime.timedelta(days=30)

# Fetch transactions
transactions = studentska_prehrana.getTransactions(start_date, end_date)

# Print restaurant name for each transaction
for transaction in transactions:
	print(transaction['restaurant'])

# Get most visited restaurant
print(studentska_prehrana.getMostVisited(start_date, end_date))

# Get total prices of your meals in the last 30 days
print(studentska_prehrana.getSums(start_date, end_date))
```