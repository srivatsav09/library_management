# Copyright (c) 2023, Srivatsav V and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from dateutil.relativedelta import relativedelta
from datetime import timedelta,datetime


class LibMembership(Document):
    # check before submitting this document
    def validate(self):
        cost = self.validate_type()
        self.cost = cost
    def before_submit(self):
        self.validate_paid()
        exists = frappe.db.exists(
            "LibMembership",
            {
                "librarymember": self.librarymember,
                "docstatus": DocStatus.submitted(),
                # check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")
        # loan_period = frappe.db.get_single_value("LibrarySettings", "loan_period")
        # self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
    
    def validate_type(self):
        mem = self.type
        settings = frappe.get_doc("LibrarySettings")
        if mem=="Gold":
            self.to_date = datetime.strptime(self.from_date,'%Y-%m-%d').date() + relativedelta(months=settings.gold)
            cost=settings.gold_price
        elif mem=="Silver":
            self.to_date = datetime.strptime(self.from_date,'%Y-%m-%d').date() + relativedelta(months=settings.silver)
            cost=settings.silver_price
        elif mem=="Bronze":
            self.to_date = datetime.strptime(self.from_date,'%Y-%m-%d').date() + relativedelta(months=settings.bronze)
            cost = settings.bronze_price
        else:
            self.to_date = datetime.strptime(self.from_date,'%Y-%m-%d').date() + relativedelta(months=settings.normal)
            cost = settings.normal_price
        return cost
    
    def validate_paid(self):
        if self.paid==0:
            frappe.throw("Please pay for the membership and check the box")
