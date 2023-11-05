// Copyright (c) 2023, Srivatsav V and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Transaction"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.month_start(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.month_end(),
		},
		{
			fieldname: "article",
			label: __("Article"),
			fieldtype: "Link",
			options: "Article",
		},
		{
			fieldname: "librarymember",
			label: __("LibraryMember"),
			fieldtype: "Link",
			options: "LibraryMember",
		},
		{
			fieldname: "type",
			label: __("Type"),
			fieldtype: "Select",
			options: ["Return", "Issue"],
		},
		{
			fieldname: "fine_amount",
			label: __("Fee"),
			fieldtype: "Check",
		},
		{
			fieldname: "min_fee",
			label: __("MIN Fee"),
			fieldtype: "Int"
		}

	],
	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);
		if (
			(column.fieldname === "issue_date" && data.issue_date) ||
			(column.fieldname === "return_date" && data.return_date)
		) {
			value = `<span style='color:red!important'>${value}</span>`;
		}
		return value;
	},
};

var dt_filter = frappe.query_report.get_filter("min_fee");
if (frappe.user.has_role("fine_amount")) {
	dt_filter.toggle_display(false);
}
dt_filter.refresh();


