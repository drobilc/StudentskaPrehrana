# StudentskaPrehrana
Python scraper for studentska-prehrana.si website.

## Usage
Example program that prints names of all restaurants where you have eaten between `2017-10-01` and today.

```python
from prehrana import StudentskaPrehrana
from datetime import datetime

# First create an object to fetch data from website
studentska_prehrana = StudentskaPrehrana("email", "password")

# Create two datetime objects to fetch transactions
start_date = datetime(2017, 10, 1)
end_date = datetime.now()

# Fetch transactions
transactions = studentska_prehrana.getTransactions(start_date, end_date)

# Print restaurant name for each transaction
for transaction in transactions:
	print(transaction['restaurant'])
```