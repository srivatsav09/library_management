# Copyright (c) 2023, Srivatsav V and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator

class Article(WebsiteGenerator):
	def validate(self):
		self.copies_left = self.total_copies_available - self.copies_issued
