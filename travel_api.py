# travel_api.py

from flask import Flask, jsonify, request, render_template
import pandas as pd
from db_config import engine
from geopy.distance import geodesic

# Load datasets
places_df = pd.read_sql("SELECT * FROM Places", engine)
ratings_df = pd.read_sql("SELECT * FROM Ratings", engine)
distances_df = pd.read_sql("SELECT * FROM Distances", engine)




app = Flask(__name__)

#@app.route('/')
#def home():
    #return "✅ Travel Recommendation API is Running!"


@app.route('/')
def frontend():
    #print(places_df)
    return render_template('travel4.html')

# GET all places
@app.route('/places', methods=['GET'])
def get_places():
    query = "SELECT * FROM Places"
    result = pd.read_sql(query, engine)
    return jsonify(result.to_dict(orient='records'))

# GET a single place by ID
@app.route('/place/<int:place_id>', methods=['GET'])
def get_place(place_id):
    query = f"SELECT * FROM Places WHERE Place_Id = {place_id}"
    result = pd.read_sql(query, engine)
    if result.empty:
        return jsonify({"error": "Place not found"}), 404
    return jsonify(result.to_dict(orient='records')[0])

# POST a new or updated rating
@app.route('/ratings', methods=['POST'])
def submit_rating():
    data = request.get_json()
    query = """
    INSERT INTO Ratings (User_Id, Place_Id, Rating)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE Rating = VALUES(Rating)
    """
    try:
        with engine.begin() as conn:
            conn.execute(query, (data['User_Id'], data['Place_Id'], data['Rating']))
        return jsonify({"message": "Rating submitted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET top recommended places

@app.route('/recommend', methods=['GET'])
def recommend():
    target_place = request.args.get('place')

    if not target_place:
        return jsonify({"error": "No place specified."}), 400

    place_column = 'Place_Name'
    if place_column not in places_df.columns:
        return jsonify({"error": f"Column '{place_column}' not found in dataset."}), 500

    if target_place.strip() not in places_df[place_column].values:
        return jsonify({"error": "Place not found."}), 404

    # Get selected place's location
    target_data = places_df[places_df[place_column] == target_place.strip()].iloc[0]
    target_location = (target_data['Latitude'], target_data['Longitude'])

    # Merge with ratings
    merged = places_df.merge(ratings_df, on='Place_Id', how='left')

    # Exclude selected place
    recommendations = merged[merged[place_column] != target_place.strip()].copy()

    # Calculate distances
    recommendations['Distance_km'] = recommendations.apply(
        lambda row: geodesic(target_location, (row['Latitude'], row['Longitude'])).km,
        axis=1
    )

    # Sort by distance and rating
    recommendations = recommendations.sort_values(['Distance_km', 'Rating'], ascending=[True, False])
    top_k = recommendations.head(5)

    # Suggest transport mode
    def suggest_mode(dist):
        if dist < 1: return 'Walk'
        elif dist < 5: return 'Auto/Rickshaw'
        elif dist < 20: return 'Cab'
        else: return 'Metro/Bus'

    #top_k['Suggested_Transport'] = top_k['Distance_km'].apply(suggest_mode)
    #top_k['Relevant'] = top_k['Rating'] >= 4.0

    result = top_k[[place_column, 'Category', 'Age', 'Distance_km', 'Rating', 'Mode_of_Transport']]
    result = result.rename(columns={place_column: 'Recommended Place'})

    return jsonify(result.to_dict(orient='records'))




# GET distance between two places
@app.route('/distance', methods=['GET'])
def get_distance():
    source = request.args.get('source')
    destination = request.args.get('destination')
    query = f"""
    SELECT * FROM Distances
    WHERE Source = '{source}' AND Destination = '{destination}'
    """
    result = pd.read_sql(query, engine)
    if result.empty:
        return jsonify({"error": "Distance not found."}), 404
    return jsonify(result.to_dict(orient='records')[0])






#get all ratings 

@app.route('/ratings', methods=['GET'])
def get_all_ratings():
    ratings = pd.read_sql("SELECT * FROM Ratings", engine)
    return jsonify(ratings.to_dict(orient='records'))



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
