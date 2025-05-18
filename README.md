# 🚗 Travel Route Recommendation System

A smart travel route suggestion system that recommends personalized travel destinations and optimal routes using **Machine Learning** and **Search Algorithms**. It combines **A\*** algorithm for path optimization and **Clustering** for personalized travel experiences based on user preferences and place characteristics.

---

## 📌 Objective

To help users discover suitable travel destinations and plan efficient routes based on:
- Place popularity and ratings
- Road and weather conditions
- User preferences and age group
- Travel difficulty and category

---

## 🧠 Algorithms Used

### 🔹 A\* (A-Star) Algorithm
Used to find the most efficient travel route from one place to another by considering factors like distance, road conditions, and complexity.

### 🔹 Clustering
Groups similar places or user patterns to recommend destinations based on interest categories (e.g., historical, spiritual, entertainment).

---

## 🛠️ Tech Stack

| Layer       | Technology |
|-------------|------------|
| **Frontend**| HTML, CSS, JavaScript |
| **Backend** | Python (Flask) |
| **Database**| MySQL |
| **ML Tools**| Pandas, Scikit-learn, SQLAlchemy, A\*, KMeans |
| **API**     | Flask RESTful APIs |

---

## 🧩 Dataset Structure

The system uses three main datasets:

1. **Places Dataset**
   - `Place_Id`, `Place_Name`, `Age`, `Category`, `Description`, `Weather_Condition`, `Road_Condition`, `Latitude`, `Longitude`

2. **Ratings Dataset**
   - `User_Id`, `Place_Id`, `Rating`

3. **Distances Dataset**
   - `Source`, `Destination`, `Distance_km`

---

## 🔄 Project Workflow

1. **Collect Data**: Import and clean data from CSV files
2. **Store Data**: Save into MySQL using SQLAlchemy
3. **Build Algorithms**: Apply A\* for route and clustering for recommendations
4. **Develop Backend**: Flask APIs to handle logic and communication
5. **Frontend**: UI built to collect user input and display recommendations
6. **Integrate**: Connect backend logic to frontend
7. **Test**: Validate accuracy and performance of route and recommendation engine

---


