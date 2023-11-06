## Library Management

# frappe-bench

We have utilised the latest frappe documentation for this

installation steps for frappe :

1-sudo apt-get update -y && sudo apt-get upgrade -y
<br>
6- sudo apt-get install git
<br>
7- sudo apt-get install python3-dev python3.10-dev python3-setuptools python3-pip python3-distutils
<br>
8- sudo apt-get install python3.10-venv
<br>
9- sudo apt-get install software-properties-common
<br>
10- sudo apt install mariadb-server mariadb-client
<br>
11- sudo apt-get install redis-server
<br>
12- sudo apt-get install xvfb libfontconfig wkhtmltopdf
<br>
13- sudo apt-get install libmysqlclient-dev
<br>
14- sudo mysql_secure_installation
<br>

Enter current password for root: (Enter your SSH root user password)
-Switch to unix_socket authentication [Y/n]: Y
-Change the root password? [Y/n]: Y
It will ask you to set new MySQL root password at this step. This can be different from the SSH root user password.

-Remove anonymous users? [Y/n] Y
-Disallow root login remotely? [Y/n]: N
This is set as N because we might want to access the database from a remote server for using business analytics software like Metabase / PowerBI / Tableau, etc.

-Remove test database and access to it? [Y/n]: Y
-Reload privilege tables now? [Y/n]: Y
<br>
15- sudo nano /etc/mysql/my.cnf

Add the below code block at the bottom of the file:
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
<br>
16- sudo service mysql restart
<br>
17- sudo apt install curl
<br>
18- curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
<br>
19- source ~/.profile
<br>
20- nvm install 16.15.0
<br>
21- sudo apt-get install npm
<br>
22- sudo npm install -g yarn
<br>
23- sudo pip3 install frappe-bench
<br>
24- bench init --frappe-branch version-14 frappe-bench
<br>
25- cd frappe-bench
<br>

27- bench new-site site1.local

here we are creating a new site called site1.This will connect to the local host and will show us the website in chrome
<br>
28- bench get-app payments
<br>
29- bench get-app --branch version-14 erpnext
<br>
30- bench get-app hrms
<br>
31- bench --site site1.local install-app erpnext
<br>
32- bench --site site1.local install-app hrms
<br>
for frappe, there are already inbuilt apps like frappe and erp next
<br>
we have added hrms, payments and another app called library managment system
<br>
Doctypes :
<br>
doctypes are similar to how modules work in python.for one app we can create many doctypes and link these modules 
together

the doctypes i have created in the library management system are 
articles , library settings , library membership , library transaction , and library member
<br>
articles - doctype that contains the list of books and its related fields
lib settings - this is singular doctype which means there can be only one set of fields and can be given values
membership - doctype where u can register a member for a certain type of membership
transaction - doctype where the member either issues a book or returns it
member - doctype that stores the name of the member and their related fields

<br>
this system is designed for a librarian to use so that they can easily manage the books,members,transactions 
and any fees is owed to the library
<br>
bench commands used :
<br>
bench start - will start the bench which connects to mariadb and redis

bench restart - will restart the bench

bench mariadb - will activate mysql in mariadb 

bench stop - will stop the bench from running

bench init frappe-bench - installs the frappe-bench in ur directory

bench new site site1.local - creates a new site in ur sites folder

bench get app payments - creates an app called payments in app folder

bench --site site1.local install-app payments - installs the app in ur site folder .. this will connect ur apps to the site

bench update - will update the bench

bench drop-site site1.local  - will delete the site 

bench reinstall site site1.local  - will reinstall the site

bench site site1.local list-apps  - will list the apps installed by you


Document api used :

frappe.get_doc("doctype",name) - returns a document object of the record identified by doctype and name

Database api used :

frappe.db.get_list(doctype, filters, or_filters, fields, order_by, group_by, start, page_length)
- returns a list of records from a doctype table


For more information visit the <a href = "https://frappeframework.com/docs/user/en/introduction">Documentation</a>

