# Copyright (c) 2023, Srivatsav V and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import timedelta,datetime


def execute(filters=None):
	columns = get_columns()
	data,flag = get_data(filters)
	chart1 = get_chart_data(data,flag,filters)
	return columns, data ,None, chart1

def get_columns():
	return [
		{
			"label": _("LibraryMember"),
			"fieldname": "librarymember",
			"fieldtype": "Link",
			"options": "librarymember",
			"width" : 200,
		},
		{
			"fieldname": "full_name",
			"fieldtype": "Data",
			"label": _("Full_Name"),
			"width": 0,
			"hidden":0,
		},
		{
			"label": _("Article"),
			"fieldname": "article",
			"fieldtype": "Link",
			"options": "article",
			"width": 120,
		},
		{
			"label": _("Return Date"),
			"fieldname": "return_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Issue Date"),
			"fieldname": "issue_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Fine Amount"),
			"fieldname": "fine_amount",
			"fieldtype": "Int",
			"width": 80,
		},
		{
			"label": _("Membership Taken"),
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Membership Start Date"),
			"fieldname":"from_date",
			"fieldtype":"date",
			"width":150,
		},
		{
			"label": _("Membership End Date"),
			"fieldname":"to_date",
			"fieldtype":"date",
			"width":150,
		}
	]

def get_data(filters):
	query,flag = get_query(filters)
	data = query.run(as_dict=True)
	# data = update_date(data,filters)
	return data,flag

def get_chart_data(data,flag,filters):
	#chart={}
	if not data:
		return None
	startdate = filters.from_date
	startdate = datetime.strptime(startdate,"%Y-%m-%d").date()
	day = timedelta(1,0,0)
	total_transactions = {}
	x=datetime.strptime(filters.to_date,"%Y-%m-%d").date() - startdate
	while(x > day):
		total_transactions[startdate] = 0
		startdate = startdate + day
		x=datetime.strptime(filters.to_date,"%Y-%m-%d").date() - startdate
	list2 = []
	if flag==1:
		mykeys = sorted(data,key=lambda d:(d['return_date']))

		for entry in mykeys:
			if entry.return_date not in list2:
				total_transactions[entry.return_date] = 1
				list2.append(entry.return_date)
			else:
				total_transactions[entry.return_date]+=1
		labels = [_(d) for d in list(total_transactions)]
		chart = {
			"data":{
				"labels":labels,
				"points":[len(list(total_transactions))],
				"datasets":[{"name":_("Return Date"),"values":list(total_transactions.values())}]
			},
			"type":"bar",
	}
	elif flag==2:
		for entry in data:
			if entry.issue_date not in list2:
				total_transactions[entry.issue_date] = 1
				list2.append(entry.issue_date)
			else:
				total_transactions[entry.issue_date]+=1
		labels = [_(d) for d in list(total_transactions)]
		chart = {
			"data":{
				"labels":labels,
				"points":[len(list(total_transactions))],
				"datasets":[{"name":_("Issue Date"),"values":list(total_transactions.values())}]
			},
			"type":"bar",
		}
	else:
		chart={}
	return chart


def get_query(filters):
	att = frappe.qb.DocType("LibraryTransaction")
	art = frappe.qb.DocType("Article")
	mem = frappe.qb.DocType("LibraryMember")
	ship = frappe.qb.DocType("LibMembership")
	t = art.article_name
	q = att.name
	r = mem.first_name
	td = frappe.db.sql(""" select tb1.article,tb1.name from tabLibraryTransaction as tb1 left join tabArticle as tb2 on tb1.article = tb2.article_name; """)
	query = (
		frappe.qb.from_(att).inner_join(art).on(att.article == art.article_name).inner_join(mem).on(att.librarymember == mem.name).inner_join(ship).on(att.full_name == ship.full_name).select(
			att.librarymember,
			att.article,
			mem.full_name,
			att.return_date,
			att.issue_date,
			att.fine_amount,
			ship.type,
			ship.from_date,
			ship.to_date,
		).where(att.docstatus==1).groupby(att.name)
	)
	if filters.type == "Return":
		flag=1
	elif filters.type == "Issue":
		flag=2
	else:
		flag=0
	for filter in filters:
		if filter == "from_date":
			if flag==1:
				query=query.where(att.return_date >=filters[filter])
			elif flag==2:
				query=query.where(att.issue_date >=filters[filter])
			else:
				query=query.where(att.issue_date >=filters[filter] or att.return_date>=filters[filter])
		elif filter == "to_date":
			if flag==1:
				query=query.where(att.return_date <=filters[filter])
			elif flag==2:
				query=query.where(att.issue_date <=filters[filter])
			else:
				query=query.where(att.issue_date <=filters[filter] or att.return_date>=filters[filter])
		elif filter == "fine_amount":
			if filters[filter] == 1:
				query=query.where(att.paid==1)
			elif filters[filter]==0:
				query=query.where(att.paid==0)
			else:
				pass
		elif filter == "min_fee":
			if "fine_amount" in filters:
				query=query.where(att.fine_amount >= filters[filter])
			else:
				pass
		else:
			query = query.where(att[filter] == filters[filter])

	return query,flag

# def update_data(data,filters):
# 	for d in data:
# 		update_data

