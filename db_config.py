# db_config.py

from sqlalchemy import create_engine

# Connect to your MySQL DB
engine = create_engine("mysql+pymysql://root:SiKu17%4026R@localhost:3306/TravelRecommendationDB2")

