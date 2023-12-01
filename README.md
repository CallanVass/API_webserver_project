# API_webserver_project


## R1: Identification of the problem you are trying to solve by building this particular app.



## R2: Why is it a problem that needs solving?



## R3: Why have you chosen this database system. What are the drawbacks compared to others?



## R4: Identify and discuss the key functionalities and benefits of an ORM



## R5: Document all endpoints for your API

Endpoints have been organised by Entities (Users, Companies, Internships)

### Users

- GET /users/register
Create New User

Allows is_admin users to register a new account, whether admin (staff) or not (student). This function must check whether a user is a User and also is_admin; this prevents companies from altering student information.

TODO: FIELDS TO PASS IN THE BODY

- POST /users/login
User Login

A route for users to login to their accounts from. Will check JWT (JSON Web Token) for authentication, and unless you're is_admin, the user will be granted read-only permissions.

TODO: FIELDS TO PASS IN THE BODY

- GET /users/
View All Users

Retrieves a list of all users. This route will only be accessible for the admin (both user and companies) to view, since students don't need access to view their peers or their internship status.

- GET /users/user_id
View One User

- PUT /users/user_id
Update User Information

- DELETE /users/user_id
Delete One User

### Companies

- GET /companies/register
Create New Company

- POST /companies/login
Company Login

- GET /companies/
View All Companies

- GET /companies/company_id
View One Company

- PUT /companies/company_id
Update Company Information

- DELETE /companies/company_id
Delete One Company

### Internships

- POST /internships/
Create Internship

- GET /internships/internship_id
View One Internship

- GET /internships/
View All Internships

- PUT /internships/internship_id
Update Internship Status

- DELETE /internships/internship_id
Delete One Internship

## R6: An ERD for your app

![An image of my API ERD](/imgs/API_ERD.png)

In this ERD of my Partnerships API, you can see three entities and the attributes they are tracking. Crows foot notation dictates the cardinality of the relationships. As you can see, Users can have 0 or many Internships, but Internships can only have one user. This relationship is mimicked in that Companies can have 0 or many Internships, but Internships can only be assigned to one company.

Here are the entities and their attributes in written form:

PK = Primary Key
FK = Foreign Key

Users((PK)user_id, name, email, password, is_admin)

Companies((PK)company_id, name, email, ph_number, password, is_admin)

Internships((PK)company_id, status, date_created, (FK)user_id, (FK)company_id)

## R7: Detail any third party services that your app will use



## R8: Describe your projects models in terms of the relationships they have with each other




## R9: Discuss the database relations to be implemented in your application




## R10: Describe the way tasks are allocated and tracked in your project

Tasks are allocated via GitHub Projects, which acts like a progress board (think Trello) for developers to take tickets from the board in various states of urgency. Tickets are assigned a level of importance, and from there developers can move tickets accross the columns (TODO, In Progress, Done). For larger projects, a more developed system would be beneficial. Something like Trello would allow states to be tracked easier.

Allocation isn't something I have to worry about as this is a solo project, however tickets on the board can be allocated to users on the project by clicking the ticket and manually allocating them. This brings up the developer's profile picture next to the ticket, allowing for easy identification.
