# API_webserver_project


## R1: Identification of the problem you are trying to solve by building this particular app.

The problem that needs solving with this API is that the Parnerships team likely has no way to properly track student progression (and if they do... well... enjoy another solution!) throughout the internship process. This means that not only are students and staff often left guessing as to a company's intentions along each step of the way, but so are companies left in the dark when it comes to staff and student decisions.

By creating an API that allows all student, staff, and companies to view every step of the process and update their status the moment decisions are made, communication is not only swift but also extremely clear. This creates less room for interpretation and misunderstanding, thereby shortening the expendature of time for all parties involved.


## R2: Why is it a problem that needs solving?

A company's efficiency can be measured by the time a team/team member spends on any given project/task. Software's job is to increase the efficiency of teams and their members, whatever the software or task may be. Zoom increases efficiency by creating a single point of communication for all members of a team. Microsoft Word allows users to create presentable documents using a variety of editing tools.

What do these have in common? They all unite people or features that are spread across different platforms to come together and become more efficient. Why not have all team members message each other via text? Why not edit a single document across multiple different editors to achieve the final product? Because it's less efficient.

Therefore the problem that needs solving is the efficiency of the organisation. Tools provide the solution to becoming more efficient, and this is simply another one of those tools.

## R3: Why have you chosen this database system. What are the drawbacks compared to others?



## R4: Identify and discuss the key functionalities and benefits of an ORM



## R5: Document all endpoints for your API

Endpoints have been organised by Entities (Users, Companies, Internships)

### Users

- GET /users/register
Create New User

*Allows is_admin users to register a new account, whether admin (staff) or not (student). This function must check whether a user is a User and also is_admin; this prevents companies from altering student information.*

TODO: FIELDS TO PASS IN THE BODY

- POST /users/login
User Login

*A route for users to login to their accounts from. Will check JWT (JSON Web Token) for authentication, and unless you're is_admin, the user will be granted read-only permissions.*

TODO: FIELDS TO PASS IN THE BODY

- GET /users/
View All Users

*Retrieves a list of all users. This route will only be accessible for the admin (both user and companies) to view, since students don't need access to view their peers or their internship status. Nested beneath the users should be a list/dict with their current internships.*

- GET /users/user_id
View One User

*Once again this route will only be accessible for the admin (both user and companies) to view for the same reasons. This will return the student along with their nested internships.*

- PUT /users/user_id
Update User Information

*This route allows user information to be updated. It's only accessible by the user admin, as companies don't need to alter user information.*

TODO: FIELDS TO PASS IN THE BODY

- DELETE /users/user_id
Delete One User

*Simply, this route deletes a user from the database, and therefore all listings. The user must have admin permissions. Companies cannot delete users.*

### Companies

- GET /companies/register
Create New Company

*Allows accounts to be created for companies, however this is only possible for is_admin users. Companies cannot create new companies, it must be requested of the staff at Coder Academy. This also prevents anyone from creating a company account.*

TODO: FIELDS TO PASS IN THE BODY

- POST /companies/login
Company Login

*A route for companies to login to their accounts. Authenticates via JWT. Companies will only be able to alter the status of internships and view students.*

- GET /companies/
View All Companies

*Allows user to view a list of companies. Companies cannot view a total list, although they will be able to see when students are in the process of getting an internship. This will encourage healthy competition as well as ensure companies act quickly when selecting students.*

- GET /companies/company_id
View One Company

*Allows user to view one company. Will likely be is_admin, as students nor companies need to view a single company for any reason.*

- PUT /companies/company_id
Update Company Information

*Allows user (is_admin) to update company information. Companies can update their own information too. General users cannot, obviously, update company information.*

TODO: FIELDS TO PASS IN THE BODY

- DELETE /companies/company_id
Delete One Company

*Deletes a single company from the database. Only accessible by an is_admin user.*

TODO: FIELDS TO PASS IN THE BODY

### Internships

- POST /internships/create
Create Internship

*Create an internship and attach it to a user. Only is_admin users will be allowed to create internships.*

TODO: FIELDS TO PASS IN THE BODY

- GET /internships/internship_id
View One Internship

*View a single internship, which will show its attached user along with details about its status. Only available to companies or is_admin users.*

- GET /internships/
View All Internships

*Gets a list of every internship. Nested after the internships are the users they're attached to. Only accessible by companies or is_admin users.*

- PUT /internships/internship_id
Update Internship Status

*Updates the internship status. Only available to companies or is_admin users, and is an essential feature of the API.*

TODO: FIELDS TO PASS IN THE BODY

- DELETE /internships/internship_id
Delete One Internship

Allows deletion of a single internship. For when the internship is over or offer has been rejected by either party.

## R6: An ERD for your app

![An image of my API ERD](/imgs/API_ERD.png)

In this ERD of my Partnerships API, you can see three entities and the attributes they are tracking. Crows foot notation dictates the cardinality of the relationships. As you can see, Users can have 0 or many Internships, but Internships can only have one User. This relationship is mimicked in that Companies can have 0 or many Internships, but Internships can only be assigned to one Company.

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
