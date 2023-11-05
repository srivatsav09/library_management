# Copyright (c) 2023, Srivatsav V and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from datetime import timedelta,datetime

#fee=0

class LibraryTransaction(Document):
    def validate(self):
        if self.type == "Return":
            startdate = self.validate_return()
            sett = frappe.get_doc("LibrarySettings")
            feecheck = frappe.db.get_all("LibMembership",filters={
                "librarymember":self.librarymember,
                "docstatus":DocStatus.submitted(),
                "from_date":("<=",self.return_date),
                "to_date":(">=",self.return_date)
                },
                fields=['name','type'],
            )
            if feecheck[-1].type == "Gold":
                finaldate = startdate + timedelta(days=sett.loan_gold)
            elif feecheck[-1].type == "Silver":
                finaldate = startdate + timedelta(days=sett.loan_silver)
            elif feecheck[-1].type == "Bronze":
                finaldate = startdate + timedelta(days=sett.loan_bronze)
            else:
                finaldate = startdate + timedelta(days=sett.loan_normal)
            #librarytransaction = self.return_date
            calc = datetime.strptime(self.return_date,'%Y-%m-%d').date()
            if finaldate < calc:
                fee = int((calc - finaldate).days) * 15
            else:
                fee=0 
            self.fine_amount = fee
        else:
            pass

            # finaldate = startdate + timedelta(days=sett.loan_period)
            # #librarytransaction = frappe.get_doc("LibraryTransaction",self.name)
            # p=self.return_date
            # calcdate = datetime.strptime(self.return_date,'%Y-%m-%d').date()
            # if finaldate < calcdate:
            #     fee = int((calcdate - finaldate).days) * 15
            # else:
            #     fee=0
            # self.fine_amount = fee
            # t=self.fine_amount
        
        
    def before_cancel(self):
        if self.type == "Issue":
            article = frappe.get_doc("Article", self.article)
            article.copies_issued -=1
            m=article.copies_issued
            article.copies_left +=1
            q=article.copies_left
            article.save()
        elif self.type == "Return":
            article = frappe.get_doc("Article", self.article)
            article.copies_issued +=1
            m=article.copies_issued
            article.copies_left -=1
            q=article.copies_left
            article.save()

    # def on_save(self):
    #     datee = self.validate_return()
    #     sett = frappe.get_doc("LibrarySettings",self.name)
    #     finaldate = datee + timedelta(days=sett.loan_period)
    #     librarytransaction = frappe.get_doc("LibraryTransaction",self.name)
    #     if finaldate < librarytransaction.return_date:
    #         fee = int((librarytransaction.return_date - finaldate).days) * 15
    #     else:
    #         fee=0
    #     #member= frappe.get_doc("LibraryMember",self.librarymember)
    #     #member.fee_owed += fee
    #     librarytransaction.fine_amount = fee
    #     t=librarytransaction.fine_amount
    #     librarytransaction.save()
    #     #member.save()



    def before_submit(self):
        if self.type == "Issue":
            ship = self.validate_issue()
            self.validate_maximum_limit(ship)
            # set the article status to be Issued
            article = frappe.get_doc("Article", self.article)            
            article.copies_issued +=1
            article.copies_left -=1
            if article.copies_issued > article.total_copies_available:
                frappe.throw("max copies issued. Please wait for return!")
            if article.copies_left < 0 :
                frappe.throw("no copies left!!")
            article.save()
            

        elif self.type == "Return":
            self.validate_paid()
            startdate=self.validate_return()
            feecheck = frappe.db.get_all("LibMembership",filters={
                "librarymember":self.librarymember,
                "docstatus":DocStatus.submitted(),
                "from_date":("<=",self.return_date),
                "to_date":(">=",self.return_date)
                },
                fields=['name','type'],
            )
            article = frappe.get_doc("Article", self.article)
            article.copies_issued -=1
            m=article.copies_issued
            article.copies_left +=1
            q=article.copies_left
            article.save()
            member= frappe.get_doc("LibraryMember",self.librarymember)
            #feecheck = frappe.get_doc("LibMembership",self.libmembership)
            if article.copies_issued > article.total_copies_available:
                frappe.throw("max copies issued. Please wait for return!")
            if article.copies_left < 0 :
                frappe.throw("no copies left!!")
            sett = frappe.get_doc("LibrarySettings")
            if feecheck[-1].type == "Gold":
                finaldate = startdate + timedelta(days=sett.loan_gold)
            elif feecheck[-1].type == "Silver":
                finaldate = startdate + timedelta(days=sett.loan_silver)
            elif feecheck[-1].type == "Bronze":
                finaldate = startdate + timedelta(days=sett.loan_bronze)
            else:
                finaldate = startdate + timedelta(days=sett.loan_normal)
            librarytransaction = frappe.get_doc("LibraryTransaction",self.name)
            if finaldate < librarytransaction.return_date:
                fee = int((librarytransaction.return_date - finaldate).days) * 15
            else:
                fee=0 
            #self.fine_amount = fee           
            member.fee_owed += fee
            # librarytransaction.fine_amount = fee
            # t=librarytransaction.fine_amount
            # librarytransaction.save()
            member.save()
 
    def validate_issue(self):
        ship = self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be issued if it is already issued
        # if article.status == "Issued":
        #     frappe.throw("Article is already issued by another member")
        return ship

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not issued first
        #librarytransaction = frappe.get_doc("LibraryTransaction",self.name)
        #t=frappe.db.get_all("article")
        x = frappe.db.get_list("LibraryTransaction",filters={'article':self.article,'type':"Issue"},fields=["full_name","issue_date"])
        n=self.full_name
        flag=0
        for p in x[::-1]:
            if p['full_name'] == n:
                startdate = p['issue_date']
                flag=1
                pass
        if flag==0:
            frappe.throw("member hasnt bought the book to return it")
        return startdate
                                    
    def validate_maximum_limit(self,ship):
        if ship[-1].type=="Gold":
            max_articles = frappe.db.get_single_value("LibrarySettings", "article_gold")
        elif ship[-1].type=="Silver":
            max_articles = frappe.db.get_single_value("LibrarySettings", "article_silver")
        elif ship[-1].type=="Bronze":
            max_articles = frappe.db.get_single_value("LibrarySettings", "article_bronze")
        else:
            max_articles = frappe.db.get_single_value("LibrarySettings", "article_normal")
        
        count = frappe.db.count(
            "LibraryTransaction",
            {"librarymember": self.librarymember, "type": "Issue", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "LibMembership",
            {
                "librarymember": self.librarymember,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<=", self.issue_date),
                "to_date": ("=>", self.issue_date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
        else:
            ship = frappe.db.get_all("LibMembership",filters={
                "librarymember":self.librarymember,
                "docstatus":DocStatus.submitted(),
                "from_date":("<=",self.issue_date),
                "to_date":(">=",self.issue_date)
                },
                fields=['name','type'],
            )
        return ship

    def validate_paid(self):
        lib = frappe.get_doc("LibraryTransaction",self.name)
        if lib.paid == 0:
            frappe.throw("Please settle the bill before submitting the transaction and tick the paid box")
