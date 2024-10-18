# 🐾 Lost Pet Tracker

A simple web application for tracking lost pets. Users can submit details of their lost pets, including images, descriptions, and last seen locations. The app stores this data in a database using Flask-SQLAlchemy.

## Features
- **Report Lost Pets:** Users can report a lost pet by filling out a form with important details such as breed, color, size, distinguishing features, and more.
- **Image Upload:** Multiple images of the lost pet can be uploaded.
- **Database Storage:** Information is saved in an SQLite database, allowing future retrieval or updates.
- **Responsive Design:** The form and layout are built to be mobile-friendly.

## Tech Stack
- **Flask:** Python web framework used for the backend.
- **Flask-SQLAlchemy:** ORM for managing database interactions.
- **HTML/CSS:** Frontend form and page design.
- **SQLite:** Database used for storing lost pet details.
- **Bootstrap:** Used for responsive design (optional, you can add it to enhance the UI).

## Project Structure

```
Lost Pet Tracker/
│
├── app.py                 # Main Flask application
├── static/
│   ├── uploads/
│   │   └── pet_images/    # Folder to store uploaded pet images
│   └── css/
│       └── styles.css     # Optional CSS file for styling
├── templates/
│   └── report_lost_pet.html # HTML form for reporting lost pets
├── lost_pets.db           # SQLite database file
├── README.md              # Project documentation (this file)
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### 1. Clone the Repository

First, clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/darsh32774/PAW-TRACKERS.git
cd lost-pet-tracker
```

### 2. Install Dependencies

You need to install the required dependencies from the `requirements.txt` file. If you don't have the file yet, you can create it by adding the necessary libraries.

```bash
pip install -r requirements.txt
```

Here’s a sample `requirements.txt`:

```
Flask==2.3.2
Flask-SQLAlchemy==3.0.4
Werkzeug==2.3.7
```

### 3. Create the Uploads Folder

Make sure the folder for storing pet images exists:

```bash
mkdir -p static/uploads/pet_images
```

### 4. Initialize the Database

Initialize the SQLite database by running the Flask app, which will create the necessary tables based on the SQLAlchemy model.

```bash
python app.py
```

This will create a `lost_pets.db` file.

### 5. Run the Application

After setting up everything, run the Flask application:

```bash
python app.py
```

You can now access the app by navigating to `http://127.0.0.1:5000` in your web browser.

### 6. Submitting a Lost Pet Report

- Navigate to the `/submit_lost_pet` URL.
- Fill in the form fields with the pet's details.
- Upload one or more images of the lost pet.
- Submit the form.

The data will be stored in the SQLite database (`lost_pets.db`), and the images will be stored in the `static/uploads/pet_images` folder.

### 7. View Submitted Reports

Currently, this app does not have a frontend to display the lost pet reports. However, you can query the `lost_pets.db` database directly to view the submitted reports. You can enhance the app by adding a route to list or search through lost pets.

## How to Contribute

Feel free to submit pull requests or report issues to improve this project. Here are some areas that need enhancement:
- A page to list and search lost pets.
- Adding more pet tracking features (e.g., a "found" section).
- Enhance the design with Bootstrap or other CSS frameworks.

## License

This project is licensed under the MIT License. Feel free to use and modify it.
