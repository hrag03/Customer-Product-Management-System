# Product and Customer Management System

This repository contains a Flask-based web application for managing products, customers, and users. It provides endpoints for authentication, customer management, product management, and more.

## Features

- **Authentication**: Users can register, login, and access their accounts securely using JSON Web Tokens (JWT).
- **User Management**: Admins can manage user accounts, including creating, editing, and deleting users.
- **Customer Management**: Users can manage customer information, such as adding, editing, and removing customer records.
- **Product Management**: Users can register new products, view all products, and manage products assigned to customers.
- **Role-Based Access Control**: The system supports role-based access control, allowing admins to restrict access to certain functionalities based on user roles.


## API Endpoints

### Authentication

- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Log in and receive an authentication token.
- `GET /auth/user`: Retrieve user information based on the authentication token.
- `GET /auth/users`: Retrieve a list of users (admin-only).
- `POST /auth/edit`: Edit user information (admin-only).
- `POST /auth/delete`: Delete a user (admin-only).
- `GET /auth/roles`: Retrieve a list of user roles.

### Customer Management

- `GET /customer/all`: Retrieve a list of all customers.
- `POST /customer/register`: Register a new customer record.
- `POST /customer/edit`: Edit customer information.
- `POST /customer/remove`: Remove a customer record.

### Product Management

- `GET /product/all`: Retrieve a list of all products.
- `POST /product/register`: Register a new product.
- `POST /product/registerCustomerProduct`: Register a new product assigned to a customer.
- `POST /product/edit`: Edit product information.
- `POST /product/remove`: Remove a product.
- `POST /product/search`: Search for a product assigned to a specific customer.
- `GET /product/type`: Retrieve a list of product types.

## Role-Based Access Control

The system supports the following user roles:

- `admin`: Admin users have access to all functionalities.
- `test`: Test users have restricted access to certain functionalities.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.
