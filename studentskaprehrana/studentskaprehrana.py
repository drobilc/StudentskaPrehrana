import requests
from bs4 import BeautifulSoup
import datetime
import re
import locale
import csv

locale.setlocale(locale.LC_NUMERIC, "sl")
price_regex = re.compile(r"(\d+(,\d+)?)")

class StudentskaPrehrana(object):
	
	def __init__(self, email, password):
		self.email = email
		self.password = password

		self.session = requests.Session()

		url = "https://www.studentska-prehrana.si/sl/Account/LoginOrRegister"
		response = self.session.get(url)
		html = BeautifulSoup(response.text, "html.parser")
		form = html.find("form")

		verification_token_field = form.find("input", {"name": "__RequestVerificationToken"})
		self.verification_token = verification_token_field["value"]

		# Poskusimo se prijaviti
		login_url = "https://www.studentska-prehrana.si/sl/Account/Login"

		login_data = {
			"Email": self.email,
			"Password": self.password,
			"RememberMe": True,
			"__RequestVerificationToken": self.verification_token
		}
		login_response = self.session.post(login_url, data=login_data)
		if login_response.url == login_url:
			raise Exception("Invalid login data")

	def parseTransactions(self, transactions_json):
		# Keys: 'Transactions', 'NumOfTransactions', 'MostVisited', 'MostVisitedCount', 'SumSurcharge', 'SumSubsidy', 'SumFull'
		transactions_html = BeautifulSoup(transactions_json['Transactions'], "html.parser")
		transactions_elements = transactions_html.findAll("li", {"class": "equal-height-columns"})

		all_data = []
		for element in transactions_elements:
			# Get transaction date and time
			element_time = element.find("div", {"class": "cbp_tmtime"})
			time_element, date_element = element_time.findAll("span")
			time = time_element.text.strip()
			date = date_element.text.strip()
			datetime_string = "{} {}".format(date, time)
			transaction_time = datetime.datetime.strptime(datetime_string, "%d.%m.%Y %H:%M")

			# Get the restaurant name
			transaction_restaurant = element.find("h4").text.strip()

			# Get transaction rating
			rating_input = element.find("input", {"type": "radio", "checked": True})
			transaction_rating = 0
			if rating_input:
				transaction_rating = int(rating_input["value"])

			# Get transaction price
			price_element, full_price_element = element.findAll("li")
			price = price_element.text
			full_price = full_price_element.text

			transaction_price = 0
			price_match = price_regex.search(price)
			if price_match and len(price_match.groups()) > 0:
				transaction_price = locale.atof(price_match.group(0))

			transaction_full_price = 0
			full_price_match = price_regex.search(full_price)
			if full_price_match and len(full_price_match.groups()) > 0:
				transaction_full_price = locale.atof(full_price_match.group(0))

			transaction_data = {
				"time": transaction_time,
				"restaurant": transaction_restaurant,
				"price": transaction_price,
				"full_price": transaction_full_price,
				"rating": transaction_rating
			}

			all_data.append(transaction_data)
		return all_data

	def getMostVisited(self, date_from, date_to):
		transactions_url = "https://www.studentska-prehrana.si/sl/transactions/ListForPeriod"
		transactions_data = {
			"from": date_from.strftime("%Y-%m-%d"),
			"to": date_to.strftime("%Y-%m-%d")
		}
		transactions_response = self.session.post(transactions_url, data=transactions_data)
		transactions_json = transactions_response.json()
		most_visited_data = {
			"restaurant": transactions_json['MostVisited'],
			"count": transactions_json['MostVisitedCount']
		}
		return most_visited_data

	def getSums(self, date_from, date_to):
		transactions_url = "https://www.studentska-prehrana.si/sl/transactions/ListForPeriod"
		transactions_data = {
			"from": date_from.strftime("%Y-%m-%d"),
			"to": date_to.strftime("%Y-%m-%d")
		}
		transactions_response = self.session.post(transactions_url, data=transactions_data)
		transactions_json = transactions_response.json()
		sums = {
			"full": transactions_json['SumFull'],
			"subsidy": transactions_json['SumSubsidy'],
			"surcharge": transactions_json['SumSurcharge']
		}
		return sums

	def getTransactions(self, date_from, date_to):
		transactions_url = "https://www.studentska-prehrana.si/sl/transactions/ListForPeriod"
		transactions_data = {
			"from": date_from.strftime("%Y-%m-%d"),
			"to": date_to.strftime("%Y-%m-%d")
		}
		transactions_response = self.session.post(transactions_url, data=transactions_data)
		transactions_json = transactions_response.json()
		return self.parseTransactions(transactions_json)