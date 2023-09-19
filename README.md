# ChatApp
The ChatApp API is a Flask-based web application that provides the backend infrastructure for a real-time chat application. It allows users to create accounts, join chat rooms, send messages, and interact with other users in a chat room. This repository contains the server-side code for the ChatApp, offering a scalable and maintainable solution for chat functionality.

# Features
<strong>User Management:</strong> Users can create accounts and log in securely.<br>
<strong>Chat Room Management:</strong> Create and join chat rooms to interact with other users.<br>
<strong>Real-Time Messaging:</strong> Send and receive messages in real-time within chat rooms.<br>
<strong>Authentication:</strong> Secure authentication using JSON Web Tokens (JWT).<br>
<strong>Data Storage:</strong> Utilizes SQLAlchemy to store user data, chat rooms, and messages in a relational database.<br>

# Technology Stack
<strong>Flask:</strong> Lightweight and flexible Python web framework.<br>
<strong>SQLAlchemy:</strong> Object-Relational Mapping (ORM) for database interactions.<br>
<strong>JWT:</strong> JSON Web Tokens for secure authentication.<br>
<strong>Postgresql:</strong> Database for persistent storage.<br>

# Usage
# 1. Using the ChatApp API Directly
   
Clone this repository to your local machine: git clone https://github.com/your-username/chatapp-api.git<br>
Set up the environment by creating a virtual environment (recommended) and installing the required dependencies:<br>
cd chatapp-api<br>
python -m venv venv<br>
source venv/bin/activate     # On Windows, use: venv\Scripts\activate<br>
pip install -r requirements.txt<br>
Configure your database connection in .env file<br>
Run the Flask application: python app.py.<br>
Access the API endpoints to interact with the chat functionality..<br>

# 2. Using Docker and Docker Compose
Ensure you have Docker and Docker Compose installed on your system. <br>
Clone this repository to your local machine:git clone https://github.com/your-username/chatapp-api.git.<br>
cd chatapp-api<br>
Create a .env file in the project directory with the necessary environment variables. You can use the provided .env file as a template and customize it as needed.<br>

Build and start the Docker containers using Docker Compose: docker-compose up --build<br>
Once the containers are running, the ChatApp API should be accessible at the specified port in your .env file (e.g., http://localhost:5000).<br>
Access the API endpoints to interact with the chat functionality.<br>

*This project is created as a job assesment task for wanclouds.*
