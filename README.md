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


## Tech Stack 

### Components: 

#### Frontend Components

**HTML:** HTML is the standard language for creating web pages. It provides the structure of a webpage using elements such as headings, paragraphs, links, images, and forms.

**CSS:** CSS is used to style and design web pages. It controls a website's layout, colors, fonts, and responsiveness, making it visually appealing and adaptable to different screen sizes.

**JavaScript:** JavaScript is a programming language that adds interactivity to web pages. It allows for dynamic content updates, form validation, animations, and communication with backend services using APIs.

#### Backend and Database Components

**FastAPI:** FastAPI is a modern, high-performance web framework for building APIs with Python. It is known for its speed, automatic data validation, and easy integration with asynchronous programming.

**MongoDB:** MongoDB is a NoSQL database that stores data in flexible, JSON-like documents. It is designed for scalability and performance, making it ideal for applications that handle large volumes of unstructured data.

#### Cloud and Deployment Components

**Google Cloud Platform:** GCP is a cloud computing service that offers infrastructure, machine learning, and storage solutions. It provides virtual machines, databases, and networking services for deploying and managing applications.

**Docker:** Docker is a platform for developing, shipping, and running applications 
inside lightweight, portable containers. It ensures consistency across different environments and simplifies application deployment.

**Kubernetes:** Kubernetes is an open-source system for automating the deployment, scaling, and management of containerized applications. It helps in orchestrating multiple Docker containers efficiently.

**Ingress:** Ingress is a Kubernetes resource that manages external access to services within a cluster. It allows the routing of HTTP and HTTPS traffic to backend services based on defined rules, improving security and scalability.


## Total Cost of all Materials

| Item/Component           | Unit Cost                   | Quantity     | Total Cost | Notes                                                                 |
|--------------------------|-----------------------------|--------------|------------|-----------------------------------------------------------------------|
| **Google Cloud Hosting** | $25/month – after trial ends| 1 account     | $0         | Pay-as-you-go account after your free trial or when you exceed the free tier usage. |
| **MongoDB Atlas**        | Free                        | 1 account     | $0         | Free tier option selected.                                            |
| **Docker, Ingress**      | Free                        | N/A          | $0         | Open-source tool.                                                     |
| **Kubernetes**           | Free (basic tier)           | N/A          | $0         | Managed via Google Kubernetes Engine.                                 |
| **FastAPI**              | Free                        | N/A          | $0         | Open-source Python framework.                                         |
| **VSCode IDE**           | Free                        | N/A          | $0         | Visual Studio Builder Community version.                              |
| **HTML/CSS/JS libraries**| Free                        | N/A          | $0         | Open-source, Bootstrap.                                               |

**Total Cost: $0**


## Performance 

The table below presents the performance metrics of the LMS website based on network activity recorded using the IP address of the deployed web application. We have considered three types of metrics to measure the performance of the website application: First, the Largest Contentful Paint (LCP) measures how fast the largest visible content (like an image or hero text) is rendered, the Cumulative Layout Shift (CLS) measures whether content shifts around while loading, and the Interaction to Next Paint (INP) measures how quickly the page reacts to user input (e.g., clicking, typing).  The goal for each of these metrics is to achieve less than 2.5 seconds for LCP, zero shifts of the elements on each page for CLS, and less than 200 milliseconds for INP.

Table 9.1: Local Metrics of the Deployed Website Application

| API Endpoint                        | LCP (s) | CLS (shift) | INP (ms) |
|------------------------------------|---------|--------------|----------|
| `/auth/login`                      | 0.32    | 0.0          | 56.0     |
| `/auth/register`                   | 0.17    | 0.0          | 56.0     |
| `/auth/manager`                    | 0.10    | 0.0          | 40.0     |
| `/search/home`                     | 0.48    | 0.21         | 40.0     |
| `/search/search_result_page`      | 0.30    | 0.0          | 112.0    |
| `/search/book_info`               | 1.04    | 0.14         | 112.0    |
| `/mylib/dashboard`                | 0.29    | 0.0          | 32.0     |
| `/mylib/access`                   | 0.38    | 0.0          | 32.0     |
| `/catalog/admin_dashboard`        | 0.04    | 0.0          | 16.0     |
| `/catalog/view-inventory (eBook)` | 0.18    | 0.72         | 80.0     |
| `/catalog/view-inventory (Audio)` | 0.18    | 0.72         | 88.0     |
| `/catalog/edit_inventory`         | 0.30    | 0.0          | 16.0     |
| `/catalog/add-item`               | 0.36    | 0.0          | 48.0     |
| `/userManage/main`                | 0.41    | 0.69         | 0.7      |
| `/userManage/edit-user`           | 0.29    | 0.02         | 40.0     |
| `/userManage/delete-user`         | 0.28    | 0.0          | 16.0     |
| `/notif/main`                     | 0.21    | 0.0          | 32.0     |


Next, the performance of the FastAPI endpoints (in seconds) is measured using a timer function in the backend module. To test the performance of these endpoints, a timer is added in the middleware definition to measure how long each request takes to process and complete. The following code snippet showcases this test procedure used for all microservices.

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request took {process_time:.3f}s")
    return
```

Table 9.2: Performance of FastAPI Endpoints

| Endpoint                                | Method | Time (s)  |
|-----------------------------------------|--------|-----------|
| `/search/home`                          | GET    | 0.170     |
| `/search/popular`                       | GET    | 0.065     |
| `/search/newest`                        | GET    | 0.219     |
| `/search/serve-book-cover`             | GET    | 0.123     |
| `/search/searchQuery`                  | GET    | 0.231     |
| `/search/search_result_page`           | GET    | 0.026     |
| `/search/filter_books`                 | GET    | 0.128     |
| `/search/book_info`                    | GET    | 0.010     |
| `/search/retrieve-reviews`             | GET    | 0.036     |
| `/search/write-review`                 | POST   | 0.058     |
| `/search/place_hold`                   | POST   | 0.024     |
| `/auth/login`                           | GET    | 0.019     |
| `/auth/home`                            | GET    | 6.343     |
| `/auth/forgot-password`                 | GET    | 0.032     |
| `/auth/forgot-password`                 | POST   | 0.096     |
| `/auth/verification-code`               | GET    | 0.008     |
| `/auth/verification-code`               | POST   | 0.032     |
| `/auth/reset-password`                  | GET    | 0.008     |
| `/auth/reset-password`                  | POST   | 0.024     |
| `/auth/aboutus`                         | GET    | 0.008     |
| `/auth/register`                        | GET    | 0.032     |
| `/auth/register`                        | POST   | 0.040     |
| `/auth/manager`                         | GET    | 0.024     |
| `/auth/manager`                         | POST   | 0.032     |
| `/catalog/admin_dashboard`              | GET    | 0.049     |
| `/catalog/view-inventory`               | GET    | 0.060     |
| `/catalog/edit-inventory`               | GET    | 0.004     |
| `/catalog/add-item`                     | GET    | 0.003     |
| `/catalog/add-item`                     | POST   | 0.918     |
| `/catalog/modify-item`                  | GET    | 0.056     |
| `/catalog/modify-item`                  | POST   | 0.191     |
| `/catalog/remove-item`                  | GET    | 0.006     |
| `/catalog/remove-item`                  | POST   | 0.086     |
| `/catalog/userManage`                   | GET    | 0.048     |
| `/catalog/manage-holds`                 | GET    | 0.024     |
| `/catalog/notifications`                | GET    | 0.024     |
| `/reservations/holds-admin`             | GET    | 0.018     |
| `/reservations/admin_dashboard`         | GET    | 0.003     |
| `/reservations/list-holds`              | GET    | 0.067     |
| `/reservations/book-title`              | GET    | 0.034     |
| `/reservations/update-status`           | GET    | 0.032     |
| `/reservations/extend-hold`             | POST   | 0.033     |
| `/reservations/delete-hold`             | POST   | 0.035     |
| `/mylib/dashboard`                      | GET    | 0.023     |
| `/mylib/pending-holds`                  | POST   | 0.002     |
| `/mylib/completed-holds`                | POST   | 0.001     |
| `/mylib/wishlist`                       | POST   | 0.001     |
| `/mylib/wishlist-remove`                | POST   | 0.048     |
| `/mylib/wishlist-clear`                 | POST   | 0.048     |
| `/userManage/add-user`                  | GET    | 0.039     |
| `/userManage/edit-user`                 | GET    | 0.038     |
| `/userManage/delete-user`               | GET    | 0.044     |
| `/userManage/customer-info`             | GET    | 0.001     |
| `/userManage/all-users`                 | GET    | 0.010     |
| `/userManage/dashboard`                 | GET    | 0.003     |
| `/userManage/catalog`                   | GET    | 0.001     |
| `/notif/main`                           | GET    | 0.018     |
| `/notif/return-soon`                    | GET    | 0.480     |
| `/notif/returns-today`                  | GET    | 0.348     |
| `/notif/available-now`                  | GET    | 0.440     |


## Conclusions

Throughout the development of this capstone project, LMS, a fully working application, was built using a Python-based microservices architecture. All the core features were completed across the microservices, including user authentication, borrowing books, making reservations, managing a wishlist, personalized dashboards, and email notifications. In total, seven microservices were created, all connected to a refined MongoDB database and fully deployed on Google Cloud. The app was thoroughly tested, and solid error handling was added to make sure users have a smooth and reliable experience. The final project is live and available online for everyone to try out.

### Discrepancies and Unfinished Components

While the system achieved a high level of functionality, aligning with the initial objectives, a few areas remain incomplete and outside the scope of the project. The LMS currently does not implement the processing and handling of payments for purchases or rentals of digital material, including ebooks and audiobooks, which was originally proposed. Furthermore, while efficient user authentication, session management, and security features were developed, more advanced features such as multi-factor authentication, error logging, and OAuth were not included in this version. Despite these gaps, the core objectives of creating a scalable, efficient, and user-friendly web application were accomplished. 

### Difficulties Encountered

During the development of the software application, several technical challenges were encountered, especially during the deployment phase. One major issue involved routing between microservices within the Kubernetes cluster. Early in development, the project used a single IP address, so routing wasn’t a concern. However, deploying each microservice with a unique IP would have made internal communication complex and difficult to manage. To solve this, we implemented an Ingress controller that routed requests internally based on URL prefixes, while exposing a single public IP address to users. Another challenge was designing and implementing custom queuing algorithms for book reservations, which required careful handling to maintain data integrity and ensure users received accurate reservation status updates.

### Future Work

The future of this project will focus on expanding the system’s features to include payment processing, an AI-based recommendation system tailored to user behavior, faster load times for images and digital content, and additional microservices for purchasing and renting digital materials. Since the project is built using a microservices architecture, it is highly scalable and flexible, making it easy to add new features. The MongoDB database also supports this growth, allowing the system to handle more users and data as it continues to evolve. 



