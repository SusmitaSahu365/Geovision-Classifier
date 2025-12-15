# GeoVision Classifier

GeoVision Classifier is a web based satellite image classification system developed using machine learning techniques. The application classifies satellite images into predefined land cover categories such as land, clouds, water bodies, and forests. The system integrates a Convolutional Neural Network with a Flask based backend and a MySQL database for user management and prediction history storage.

This project was developed as a Mini Project for the Bachelor of Engineering in Computer Engineering under the University of Mumbai.

---

## Project Overview

Satellite imagery is widely used in environmental monitoring, urban planning, disaster management, and resource analysis. Manual interpretation of satellite images is time consuming and prone to human error, especially when handling large volumes of data. GeoVision Classifier addresses this challenge by providing an automated and scalable solution for satellite image classification using deep learning techniques.

The system allows authenticated users to upload satellite images, receive real time classification results, and maintain a history of past predictions. Each prediction is securely stored in the database and linked to the corresponding user.

---

## Objectives

- To develop an automated system for classifying satellite images into predefined land cover categories  
- To implement Convolutional Neural Networks for accurate image classification  
- To provide a user friendly web interface for image upload and result visualization  
- To store user details and prediction history using a relational database  
- To enable scalability and future model enhancement  

---

## Classification Categories

- Land  
- Clouds  
- Water Bodies  
- Forests  

---

## Dataset

The Convolutional Neural Network model used in this project is trained using a publicly available dataset from Kaggle.

Satellite Image Classification Dataset  
https://www.kaggle.com/datasets/mahmoudreda55/satellite-image-classification/data

The dataset contains labeled satellite images representing different land cover classes. Although the dataset is relatively old, it provides a strong foundation for training the classification model. The system can be retrained with newer datasets in future versions to improve accuracy and generalization.

---

## Model Performance

The Convolutional Neural Network was trained and validated on the satellite image dataset using multiple training epochs. The model demonstrated consistent learning behavior with improving accuracy across epochs.

- Final training accuracy: approximately 86 percent  
- Final validation accuracy: approximately 89 percent  

The validation accuracy indicates effective feature learning and good generalization performance for satellite image classification tasks.

---

## Technology Stack

Frontend  
HTML  
CSS  
Bootstrap  
JavaScript  

Backend  
Python  
Flask  

Machine Learning  
TensorFlow  
Keras  
Convolutional Neural Networks  

Database  
MySQL  

---

## Database Design

The system uses a MySQL relational database to manage user authentication and prediction history. The database consists of two primary tables: users and predictions.

### Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    predicted_class VARCHAR(100) NOT NULL,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```
##License

This project is developed strictly for academic purposes. Dataset credits belong to the respective authors on Kaggle.
