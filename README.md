# API_webserver_project


# Table of Contents
- [Installation Guide](#R14)

1. [R1: Identification of the problem you are trying to solve by building this particular app.](#R1)
2. [R2: Why is it a problem that needs solving?](#R2)
3. [R3: Why have you chosen this database system. What are the drawbacks compared to others?](#R3)
4. [R4: Identify and discuss the key functionalities and benefits of an ORM](#R4)
5. [R5: Document all endpoints for your API](#R5)
6. [R6: An ERD for your app](#R6)
7. [R7: Detail any third party services that your app will use](#R7)
8. [R8: Describe your projects models in terms of the relationships they have with each other](#R8)
9. [R9: Discuss the database relations to be implemented in your application](#R9)
10. [R10: Describe the way tasks are allocated and tracked in your project](#R10)
11. [Email Feature](#R11)
12. [Logging Configuration](#R12)
13. [Bibliography](#R13)



<a id="R14"></a>
## Installation Guide

1. Ensure you've downloaded a version of linux (I've used Ubuntu). If you're on Mac you only need navigate to your terminal. Next check you've installed Python, Postgres.
Check the versions like this: 
```
python --version

psql --version
```
If prompted to install them, do so. Python should have a version of at least 3.10, and postgres 16.0

2. Clone the rpository to your local machine using "git clone **LINK OR SSH KEY HERE**", then navigate to the file of the repository and use the command:
```
python3 -m venv .venv
```
Next use the command:
```
code .
```
This should install VSCode, an IDE (integrated development environment) that lets you view and alter the code.
Once VS code opens, use this command to activate the virtual environment:
```
source venv/bin/activate
```
A small blue dot should appear next to your command line.

3. Next install the requirements using this command:
```
pip install -r requirements
```
4. Next navigate to postgres using the command line command:
```
sudo -u postgres psql
```
If prompted to make a password, do so. Once inside postgres, use this command:

```
CREATE DATABASE partnerships;
```
Next create a user for the database with this command:
```
CREATE USER partnerships_dev WITH PASSWORD 'your_password_here';
```
Remember this password, you will need it to replace the YOURDATABASEPASSWORDHERE inside the DB_URI string inside the .flaskenv file.

Still inside postgres, run this command to grant the user superuser access to the database:
```
ALTER USER your_username WITH SUPERUSER;
```
Okay, now you're ready to change the files inside VScode.

5. Change the file called server_log_sample.txt to the name server_log.txt. 
Next change the config.ini.sample file to config.ini. If you want to be able to send emails, you must create a gmail account and get a third-part app key. Pass them into the respective paramaters in config.ini.
**Please note that you must also create a user in cli_bp with the email address you wish to have the internship update sent to if you wish to test this feature.**
Next change the .flaskenv.sample to be named .flaskenv. The JWT SECRET KEY is arbitrary and can be made into whatever you like, however the CONNECTION STRING must follow this sytax: DB_URI=postgresql+psycopg2://partnerships_dev:YOURDATABASEPASSWORDHERE@127.0.0.1:5432/partnerships

6. Next run the commands:
```
flask db create
```
AND:
```
flask db seed
```
This will create the tables and seed them with data.

7. Now, we simply need to run the server. This is done using the following command:
```
flask run
```

Now that you know this, I'll have to kill you.

KIDDING 

Happy API'ing!


<a id="R1"></a>
## R1: Identification of the problem you are trying to solve by building this particular app.

The problem that needs solving with this API is that the Parnerships team likely has no way to properly track student progression (and if they do... well... enjoy another solution!) throughout the internship process. This means that not only are students and staff often left guessing as to a company's intentions along each step of the way, but so are companies left in the dark when it comes to staff and student decisions.

By creating an API that allows all student, staff, and companies to view every step of the process and update their status the moment decisions are made, communication is not only swift but also extremely clear. This creates less room for interpretation and misunderstanding, thereby shortening the expendature of time for all parties involved.

<a id="R2"></a>
## R2: Why is it a problem that needs solving?

A company's efficiency can be measured by the time a team/team member spends on any given project/task. Software's job is to increase the efficiency of teams and their members, whatever the software or task may be. Zoom increases efficiency by creating a single point of communication for all members of a team. Microsoft Word allows users to create presentable documents using a variety of editing tools compiled into the one editor.

What do these have in common? They all unite people or features that are spread across different platforms to come together and become more efficient. Why not have all team members message each other via text? Why not edit a single document across multiple different editors to achieve the final product? Because it's less efficient.

Therefore the problem that needs solving is the efficiency of the organisation. Tools provide the solution to becoming more efficient, and this is simply another one of those tools.
<a id="R3"></a>
## R3: Why have you chosen this database system. What are the drawbacks compared to others?

Familiarity does play a part in my selection, but so does compatibility, online documentation, and flexibility.

#### Compatibility

- PostgreSQL is used widely within the tech industry, and is largely known for its compatibility with other softwares and libraries. It also has many GUI tools built for it such as pgAdmin, DBeaver, DataGrip, and OmniDB. GUI tools can reduce the time spent interacting with the database.

#### Documentation

-Online there can be found large volumes of documentation about PostgreSQL, much of it via the [PostgreSQL website itself](https://www.postgresql.org/docs/). Aside from official documentation, there are millions of posts online to help speed up troubleshooting.

#### Flexibility

- PostgreSQL has been developed to run on the following operating systems: Linux, Windows, FreeBSD, OpenBSD, NetBSD, DragonFlyBSD, macOS, AIX, Solaris, and illumos. This covers the vast majority of all OS, which allows co-working developers around the world to download PostgreSQL as their DBMS.

#### Drawbacks

- Compared to many other DBMS (Database Management Systems), PostgreSQL isn't the quickest. It's priority of compatibility over efficiency means it runs slower than DBMS such as Cassandra or MongoDB. Also, customer support is only available commercially, and even then it has a price as the support is actually a professional service provider.
Lastly, not all open source applications support PostgreSQL. They may run a DBMS such as MySQL or NoSQL instead.
<a id="R4"></a>
## R4: Identify and discuss the key functionalities and benefits of an ORM

### Functionality

- An ORM (Object Relational Mapper) provides a way for OOP (Object Oriented Programming) to interact with a database. Specifically using CRUD operations, which stands for Create, Read, Update, Delete. It removes the gap between OOP and SQL (Structured Query Language), in its place creating a mapping that allows a developer to query the database through the ORM instead of manually writing SQL queries.
There are many ORMs (at the very least one for most any programming language). One such example is SQLAlchemy, which is an ORM for the Python programming language. With SQLAlchemy, one can query a DBMS (such as PostgreSQL!) using a command as such:

```
stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
```

This command has an SQL equivalent, which is:

```
SELECT * FROM user WHERE name IN ('spongebob', 'sandy');
```

While the first statement might appear more complex (and indeed, it is), this is actually a benefit of an ORM. Compared to the second statement, the first is more expressive and explicit, with much more space for specification.

### Benefits

- As previously seen, one large benefit of ORMs is that they allow us to write SQL queries in a language of our choice. This means that instead of having to switch between SQL and Python, one can simply write Python instead and not have to split their attention. This can appear unweildy, but once the syntax is learned it can be much faster than switching languages constantly. This can greatly reduce the time developers spend interacting directly with the database, therefore speeding up productivity.

- Speaking of productivity: the queries that are translated and written by the ORM from your programming language to SQL are likely to be more effective than if you wrote them yourself. Any error will likely be discovered on the command line long before the ORM translates your code into a query, meaning that it's much harder to devise incorrect queries.

- ORMs such as SQLAlchemy help protect against SQL injections by parameterizing, escaping, and quoting the data before querying the database with it. Therefore if there is any malicious SQL it becomes harmless. This process is known as data sanatisation.


<a id="R5"></a>
## R5: Document all endpoints for your API

Endpoints have been organised by Entities (Users, Companies, Internships)

#### Users

- GET /users/register
Create New User

*Allows is_admin users to register a new account, whether admin (staff) or not (student). This function must check whether a user is a User and also is_admin.*

FIELDS: 
{
    "email": "samples@example.com", **required**
    "password": "samplepassword", **required**
    "name": "samplename" **required**
}

![Register User](/imgs/register_user_route.png)

- POST /users/login
User Login

*A route for users to login to their accounts from. Will check JWT (JSON Web Token) for authentication, and unless you're is_admin, the user will be granted read-only permissions.*

FIELDS: 
{
    "email": "samples@example.com", **required**
    "password": "samplepassword" **required**
}

![Login User](/imgs/login_user_route.png)

- GET /users/
View All Users

*Retrieves a list of all users. This route will only be accessible for the admin (both user and companies) to view, since students don't need access to view their peers or their internship status. Nested beneath the users should be a list/dict with their current internships.*

FIELDS: NONE

![Get User](/imgs/get_all_users_route.png)

- GET /users/user_id
View One User

*Once again this route will only be accessible for the admin (both user and companies) to view for the same reasons. This will return the student along with their nested internships.*

FIELDS: NONE

![Get One User](/imgs/get_one_user_route.png)

- PUT /users/user_id
Update User Information

*This route allows user information to be updated. It's only accessible by admins.*

FIELDS:
{
    "email": "samples@example.com", **optional**
    "password": "samplepassword" **optional**
}

![Update User](/imgs/update_a_user_route.png)

- PUT /users/update-password/user_id
Update User Password 

*Changes the old password (current password) to a new password. Anyone may update a password, as it requires prior knowledge of the password, which only the individual should have.*

FIELDS:
{
 "old_password": "sample_old_password",
  "password": "sample_new_password"
}

![Update User Password](/imgs/update_user_password_route.png)

- DELETE /users/user_id
Delete One User

*Simply, this route deletes a user from the database, and therefore all listings. The user must have admin permissions.*

FIELDS: NONE

![Delete User](/imgs/delete_user_route.png)

#### Companies

- GET /companies/register
Create New Company

*Allows accounts to be created for companies. Only is_admin users and companies can use. This prevents regular users from creating a company account.*

FIELDS: 
{
    "email": "samples@example.com", **required**
    "password": "samplepassword", **required**
    "name": "samplename", **required**
    "ph_number": "0411222333" **required**
}

![Register Company](/imgs/register_company_route.png)

- POST /companies/login
Company Login

*A route for companies to login to their accounts. Authenticates via JWT. Companies will only be able to alter the status of internships and view students.*

FIELDS: 
{
    "email": "samples@example.com", **required**
    "password": "samplepassword" **required**
}

![Login Company](/imgs/company_login_route.png)

- GET /companies/
View All Companies

*Allows user to view a list of companies. Companies can view the list of other companies too.*

FIELDS: NONE

![Get All Companies](/imgs/get_all_companies_route.png)

- GET /companies/company_id
View One Company

*Allows user to view one company. Will likely be is_admin and company, as students nor companies need to view a single company for any reason.*

FIELDS: NONE

![Get One Company](/imgs/get_one_company_route.png)

- PUT /companies/company_id
Update Company Information

*Allows user (is_admin) to update company information. Companies can update their own information too. General users cannot, obviously, update company information.*

FIELDS: 
{
    "email": "samples@example.com", **optional**
    "name": "samplename", **optional**
    "ph_number": "0411222333" **optional**
}

![Update Company](/imgs/update_company_route.png)

- PUT /companies/update-password/company_id
Update Company Password 

*Changes the old password (current password) to a new password. Anyone may update a password, as it requires prior knowledge of the password, which only the individual should have.*

FIELDS:
{
 "old_password": "sample_old_password",
  "password": "sample_new_password"
}

![Update Company Password](/imgs/update_company_password_route.png)

- DELETE /companies/company_id
Delete One Company

*Deletes a single company from the database. Only accessible by an is_admin user and companies.*

FIELDS: NONE

![Delete Company](/imgs/delete_company_route.png)

#### Internships

- POST /internships/create
Create Internship

*Create an internship and attach it to a user. Only is_admin users and companies will be allowed to create internships.*

VALID_STATUSES = ("Company Interested", "Student Interview Pending" , "Student Declined Interview", "Company Offered Position", "Student Accepted Offer", "Student Declined Offer", "Student Offered Employment", "Student Completed Internship")
VALID_POSITIONS = ("Front-end", "Back-end", "Full-stack")

FIELDS:
{
  "status": "Company Interested", **required**
  "position_type": "Back-end", **required**
  "user_id": user_id, **required**
  "company_id": company_id **required**
}

![Create Internship](/imgs/create_internship_route.png)

- GET /internships/internship_id
View One Internship

*View a single internship, which will show its attached user along with details about its status. Only available to companies or is_admin users.*

FIELDS: NONE

![Get One Internship](/imgs/get_one_internship_route.png)

- GET /internships/
View All Internships

*Gets a list of every internship. Nested after the internships are the users they're attached to. Only accessible by companies or is_admin users.*

FIELDS: NONE

![Get All Internships](/imgs/get_all_internships_route.png)

- PUT /internships/internship_id
Update Internship Status

*Updates the internship status. Only available to companies or is_admin users, and is an essential feature of the API.*

STATUSES: Refer to Create Internship Route
POSITIONS: Refer to Create Internship Route

FIELDS:
{
  "position_type": "Back-end", **optional**
  "status": "Company Interested" **optional**
}

![Update Internship](/imgs/update_internship_route.png)

- DELETE /internships/internship_id
Delete One Internship

Allows deletion of a single internship. For when the internship is over or offer has been rejected by either party.

FIELDS: NONE

![Delete Internship](/imgs/delete_internship_route.png)

<a id="R6"></a>
## R6: An ERD for your app

![An image of my API ERD](/imgs/API_ERD.png)

In this ERD of my Partnerships API, you can see three entities and the attributes they are tracking. Crows foot notation dictates the cardinality of the relationships. As you can see, Users can have 0 or many Internships, but Internships can only have one User. This relationship is mimicked in that Companies can have 0 or many Internships, but Internships can only be assigned to one Company.

Here are the entities and their attributes in written form:

PK = Primary Key
FK = Foreign Key

Users((PK)user_id, name, email, password, is_admin)

Companies((PK)company_id, name, email, ph_number, password, is_admin)

Internships((PK)company_id, status, date_created, position_type, (FK)user_id, (FK)company_id)
<a id="R7"></a>
## R7: Detail any third party services that your app will use

- **Bcrypt**

Flask-Bcrypt is an extension of Bcrypt that gives us hashing capabilities to further protect sensitive information in our API. This information could be anything from passwords to access keys.

Hashing is the process of running a piece of information (usually a password or key) through a hashing algorithm. This algorithm turns the information into a string of characters and numbers completely different from the original string. We will use this to store passwords in our database, which will in turn stop anyone (even admins!) from reading them.

- **SQLAlchemy**

As previously mentioned, SQLAlchemy is an ORM, but it's also a Python SQL tolkit. It's designed to help us access the database by creating Models (pre-made classes) that allow us to create tables in our chosen DBMS (PostgreSQL). Within these Models, we can specify columns to be made as well as relationships to other tables within our database. 

Note: We will also be using the module Flask-SQLAlchemy, which is an extension that allows more specific support for Flask within the original extension. 

- **Psycopg2**

Psycopg2 acts like an adapter to connect our database with our application. By specifying our connection string in the .flaskenv file, we're able to establish a connection between PostgreSQL and psycopg2 (our app).

This also gives us a better way to interact with our database via Python instead of SQL, however much of this isn't used in this application due to the overlap between Pyscopg2 and SQLAlchemy's way of interacting with the database.

- **Marshmallow**

Marshmallow-SQLAlchemy is a (de)serialization library that allows us to recieve and output data into the required form. This can mean serialization, which is converting SQLAlchemy models into JSON. It can also mean deserialization, which is converting incoming JSON data back into Marshmallow Schemas. 

Marshmallow Schemas allow us to specify the fields we wish to be (de)serialized. These should correspond with our SQLAlchemy Model columns. They also allow us to specify nested fields we wish to display, allowing us to display more than one Model when serializing data.

- **Flask-JWT-Extended**

Flask-JWT-Extended allows us to create JWT (JSON Web Token) access tokens for individual session usage, limit access by requiring a token from a user (e.g user must be signed in), or retrieve the JWT identity within a protected route.

By confirming a JWT token exists within the authorization header, we add an extra layer of security to our API which dictates that only specified users can view/update/delete certain endpoints.

- **Python-dotenv**

This lets us reference .env files and set them as global variables. It reads the file as key-value pairs and sets the key to the variable name and the value to the key's content. More specifically, we use this to reference a .gitignored file called .flaskenv that contains our JWT Key and our Connection String so that we don't push sensitive information to our GitHub, but rather store it locally.

- **PostgreSQL**

PostgreSQL is an open source database management system for relational databases with a huge amount of compatability with various Frameworks and operating systems.

<a id="R8"></a>
## R8: Describe your projects models in terms of the relationships they have with each other

There are three Models in this project: Users, Companies, and Internships. 

**Users**

The Users Model will relate to the Internships Model with a foreign key of user_id, as the Internships Model will need to have a User associated with it for identification purposes. This will back populate the user using the Internships Model.

Relationships: Internships = One-To-Many. Companies = None.

Nested Models: Internship attibute id, status.

Users((PK)user_id, name, email, password, is_admin)

![User Model](/imgs/user_model.png)

**Companies**

The Companies Model will relate to the Internships Model alonside the user_id with its own foreign key of company_id, as an Internship obviously has to be related to a company. This will back populate the company using the the Internships Model.

Relationships: Internships = One-To-Many. Users = None.

Nested Models: Internships attibute id, position_type, status. 

Companies((PK)company_id, name, email, ph_number, password, is_admin)

![Company Model](/imgs/company_model.png)

**Internships**

Unlike either the Users or Companies Models, the Internships Model relates back to each Entity in the ERD. This is because it contains both the user_id and the company_id foreign keys, as there can be no Internship without a user (student) and a company.

Relationships: Companies = Many-To-One. Users = Many-To-One.

Nested Models: Users attibute name. Companies attribute name. 

Internships((PK)company_id, status, date_created, position_type, (FK)user_id, (FK)company_id)

![Internship Model](/imgs/user_model.png)

<a id="R9"></a>
## R9: Discuss the database relations to be implemented in your application

To begin with I will create a database called "Partnerships" using PostgreSQL. From there I will create the tables Users, Companies, and Internships. These tables all consist of a primary key which will be used for identification. (E.G Users primary key is user_id, even when referenced in another table).

Since it's a relational database, we need a way to *relate* tables to one another. This is done by the use of foregin keys within the tables themselves whenever a connection is established between two tables. For instance, the Internships table has two foreign keys: user_id and company_id. The definition of these keys establishes the relationship within the database. However it's to be noted that not every table relates to every other table. Users doesn't relate to Companies, and vice versa. Their only connection is through the Internships table.

Although tables are created at the API (Flask) level, they exist on a database level. Luckily, SQLAlchemy gives us a way to create the connections that are accessible and mutable via Flask.

<a id="R10"></a>
## R10: Describe the way tasks are allocated and tracked in your project

Tasks are allocated via GitHub Projects, which acts like a progress board (think Trello) for developers to take tickets from the board in various states of urgency. Tickets are assigned a level of importance, and from there developers can move tickets accross the columns (TODO, In Progress, Done). For larger projects, a more developed system would be beneficial. Something like Trello would allow states to be tracked easier, and has more features overall.

Allocation isn't something I have to worry about as this is a solo project, however tickets on the board can be allocated to users on the project by clicking the ticket and manually allocating them. This brings up the developer's profile picture next to the ticket, allowing for easy identification.

![1st Progress Snapshot](/imgs/task_tracking_1.png)


![2nd Progress Snapshot](/imgs/task_tracking_2.png)


![3rd Progress Snapshot](/imgs/task_tracking_3.png)


![4th Progress Snapshot](/imgs/task_tracking_4.png)

<a id="R11"></a>
## Email Feature

When the status of an internship is changed, an email is sent to the user whom matches the id of the internship. This feature could be expanded upon in multiple aspects, such as implementing email notifications for changes in details or for user and company account creation/deletion. This section will describe the email feature in detail.

Firstly, the standard Python [smtplib](https://docs.python.org/3/library/smtplib.html) library doesn't appear to support the user of environ to retrieve variables from .flaskenv, so instead we're using [configparser](https://docs.python.org/3/library/configparser.html) instead, which retains the same functionality and is even more explicit, allowing us to read and write configuration files. So intead of reading from .flaskenv, we're reading from config.ini.

Next we've created a function that takes an email address and a name as parameters. The email address is used to send the email to, while the name is used to address the user by their name in the body of the email.

Here is a picture of said function:

![Email Function](/imgs/email_function.png)

Next is setting the variables within the function (this is where we use configparser). After that we use MIME (Multipurpose Internet Mail Extensions) classes to create an object for the email to read. This gives us a simple format with which to pass subjects, senders, and receivers into. The body of the email is next, and here is where we've interpolated the name parameter so as to display the users name when the email is sent.

Below the message body is us attaching the message into another class for formatting purposes, and below that is the connection to the Gmail server using port 587. This does the dirty work of securing the connection, logging into the email account, and sending the email for us.

Lastly we print the successful outcome to a file named email_log.json for data logging purposes.

NOTE: I have tried to user configparser to retrieve the JWT_SECRET_KEY and the SQLALCHEMY_DATABASE_URI, however it appears they only work when retrieved via environ.

![Sent Email](/imgs/sent_email.jpg)

<a id="R12"></a>
## Logging Configuration

Using the [logging module](https://docs.python.org/3/library/logging.html), we're able to control the output of our terminal logging information and redirect it to wherever we want. As seen in the commented basicConfig() function below, we manually set the output using StreamHandler and Filehandler to print to the console and a file called "server_log.txt" respectively.

![Logging Function](/imgs/logging_function.png)

<a id="R13"></a>
## Bibliography

Bayer, M 2023, SQLAlchemy Documentation — SQLAlchemy 2.0 Documentation, docs.sqlalchemy.org, viewed 1 December 2023, <https://docs.sqlalchemy.org/en/20/>.

ConfigParser – Work with configuration files - Python Module of the Week n.d., pymotw.com, viewed 9 December 2023, <https://pymotw.com/2/ConfigParser/>.

Countryman, M 2011, Flask-Bcrypt — Flask-Bcrypt 1.0.1 documentation, flask-bcrypt.readthedocs.io, viewed 4 December 2023, <https://flask-bcrypt.readthedocs.io/en/1.0.1/>.

HTTP response status codes n.d., MDN Web Docs, viewed 11 December 2023, <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#Client_error_responses>.

Liang, M 2021, Understanding Object-Relational Mapping: Pros, Cons, and Types, AltexSoft, viewed 2 December 2023, <https://www.altexsoft.com/blog/object-relational-mapping/>.

logging — Logging facility for Python — Python 3.10.0 documentation 2023, docs.python.org, viewed 12 December 2023, <https://docs.python.org/3/library/logging.html>.

Loria, S 2023, marshmallow-sqlalchemy — marshmallow-sqlalchemy 0.29.0 documentation, marshmallow-sqlalchemy.readthedocs.io, viewed 1 December 2023, <https://marshmallow-sqlalchemy.readthedocs.io/en/latest/>.

PostgreSQL: Documentation 2023, www.postgresql.org, viewed 2 December 2023, <https://www.postgresql.org/docs/>.

Priya, B 2022, Logging in Python: A Developer’s Guide, Product Blog • Sentry, viewed 11 December 2023, <https://blog.sentry.io/logging-in-python-a-developers-guide/>.

Python - Sending Email using SMTP - Tutorialspoint 2020, Tutorialspoint.com, viewed 8 December 2023, <https://www.tutorialspoint.com/python/python_sending_email.htm>.

Shrivastava, M 2020, How to send emails using python, Medium, viewed 8 December 2023, <https://medium.com/@manavshrivastava/how-to-send-emails-using-python-c89b802e0b05>.

smtplib — SMTP protocol client — Python 3.8.1 documentation 2020, Python.org, viewed 9 December 2023, <https://docs.python.org/3/library/smtplib.html>.

Welcome to Flask — Flask Documentation (3.0.x) 2010, flask.palletsprojects.com, viewed 1 December 2023, <https://flask.palletsprojects.com/en/3.0.x/>.
