# StudentskaPrehrana
Python scraper for studentska-prehrana.si website.

## Installation
To install this package first clone it from this repository and then install it by running python setup script.
```
git clone https://github.com/drobilc/studentskaprehrana.git
cd studentskaprehrana
python setup.py install
```

You can also install it using `pip`.
```
pip install studentskaprehrana
```

## Usage
To use this package you first have to install it and then import it into your python script. This is usually done using `import studentskaprehrana`.

### Creating StudentskaPrehrana object
Once module is imported you have to create `StudentskaPrehrana` object which holds your user data and allows you to scrape transactions from [studentska prehrana website](https://www.studentska-prehrana.si/).

```python
studentska_prehrana = StudentskaPrehrana(email, password)
```

If the email or password is incorrect, the module will raise an Exception. Otherwise you can start fetching data.

### Getting transactions
Once you are logged in, you can get list of transactions by calling `getTransactions` function. It accepts two `datetime` objects (`date_from` and `date_to`).
The function returns list of all transactions between those 2 dates (but at most 200 results).

For example - if we want to fetch data for the last 30 days we can call our function like this.
```python
date_to = datetime.now()
date_from = date_to - datetime.timedelta(days=30)
transactions = studentska_prehrana.getTransactions(date_from, date_to)
```

Each transaction is a dictionary and contains the following keys:
  * `restaurant` - name of the restaurant
  * `time` - a datetime object containing date and time of transaction
  * `rating` - meal rating between 0 and 5
  * `price` - meal price with subvention
  * `full_price` - full meal price (without subvention)

### Getting most visited restaurant
To get the most visited restaurant you can call `getMostVisited` function. You must supply 2 parameters - two datetime objects (`date_from`, and `date_to`).
It returns dictionary which contains two keys:
  * `restaurant` - name of the most visited restaurant
  * `count` - number of visits

### Getting total prices
To get the total price of your meals (with and without subventions) you can call `getSums` function. It accepts two `datetime` objects (`date_from` and `date_to`).
The function returns dictionary with 3 keys:
  * `full` - the full price of your meals for date range supplied
  * `subsidy` - the full price of your subventions
  * `surcharge` - full price you had to pay

## Example
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