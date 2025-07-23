# LMS_CAPSTONE_2025
## LIBRARY MANAGEMENT SERVICE (LMS)

This Library Management System focuses on enhancing managerial efficiency by automating core library operations, including tracking, cataloging, returning, and reserving library items. The system was designed to streamline resource management by providing an online platform for users to search, borrow, and return digital materials efficiently. From a development perspective, the project aimed to ensure seamless user authentication, secure data handling, robust backend functionality, and thorough exception management. The LMS enabled library staff to manage user accounts, track fines and holds, and facilitate automated communication with ease. To improve reliability and scalability, the system was implemented using a microservice architecture, with each service handling a specific library function. FastAPI and MongoDB powered the backend, enabling efficient CRUD operations, while Docker, Kubernetes, and Nginx Ingress were used to deploy the application on Google Cloud, ensuring secure and scalable access. Additionally, the LMS incorporated error-handling mechanisms, logging services, and data validation features to minimize manual errors and ensure data integrity. The project report provided an in-depth analysis of the system architecture, application development, and both functional and non-functional requirements, while also identifying key challenges, limitations, and future enhancements to refine the system further.

## Features

### Customer/Manager Authentication

This service handles customer and manager authentication and authorization. It is responsible for verifying the identities of customers and managers, ensuring they have the correct permissions and access to different parts of the system. This service will handle secure login, registration, and authentication using methods such as username/password or even more advanced techniques like JWT or JSON Web Token. 



### Catalog Management

Catalog managed the collection of digital media. It allows authorized managers to add, update, and remove catalog items. It enforced security by ensuring that only authorized managers can modify the catalog. Moreover, to streamline the process, the service was built to support a large number of catalog entries and requests with minimal latency.


### Search

The search microservice provided users with a set of filters to set and search for books. It included a dynamic keyword feature where users are able to search based on title, author, and genre. When a search was performed, the service filtered the books table in the database to display the retrieved queries. In addition, it displayed the book information and provided the option to place a hold, which was then communicated to the reservations service.


### Reservations

This service was responsible for managing the queue of hold requests and updating the status of checkouts. The reservations table in the database was updated with the user information and the book that was selected. When the book is available, the user is able to view it from the My Library service. The system was designed to handle multiple reservations and queue updates efficiently while maintaining the data in the catalog. 

### My Library

This microservice handled the account dashboard, where customers could interact with the items they had checked out and access them by reading eBooks or listening to audiobooks. Users were also able to view their position in the queue for book reservations, along with other details such as the expiration date of the hold and metadata about the book. This service also hosted a personalized wishlist and allowed users to manage it.


### Manage Users

This service provided additional functionality and flexibility for administrators to add, modify, or delete users, including the library management system's customers and managers. The logged-in administrator was able to change user metadata such as first name, last name, email, manager ID, and user type, while excluding confidential information such as passwords. This microservice also handled edge cases where the administrator was not permitted to perform these operations on their own account.


### Notifications

This microservice included the ability to send three types of email notifications to users: for recently returned and available books, books due today, and books due soon. The emailing service relied on existing reservation data and an external email provider, Brevo, to enhance the user experience by keeping customers informed about their book hold status and providing options to manage their account directly from the email.



--- Tech Stack ---


--- Installation Guide ---


--- Usage instrctions ---

