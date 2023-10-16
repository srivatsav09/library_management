// Copyright (c) 2023, Srivatsav V and contributors
// For license information, please see license.txt

frappe.ui.form.on('LibraryMember', {
	refresh: function (frm) {
		frm.add_custom_button('Create Membership', () => {
			frappe.new_doc('LibMembership', {
				librarymember: frm.doc.name
			})
		})
		frm.add_custom_button('Create Transaction', () => {
			frappe.new_doc('LibraryTransaction', {
				librarymember: frm.doc.name
			})
		})
	}
});

