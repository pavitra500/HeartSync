from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sqlite3
from flask import Flask, jsonify, g
from datetime import datetime
from g4f.client import Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\pavit\\Desktop\\react-chat-app\\src\\users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

client = Client()

db = SQLAlchemy(app)

# Define models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    essay0 = db.Column(db.Text)
    age = db.Column(db.Integer)
    status = db.Column(db.String)
    sex = db.Column(db.String)
    orientation = db.Column(db.String)
    location = db.Column(db.String)
    body_type = db.Column(db.String)
    height = db.Column(db.String)
    diet = db.Column(db.String)
    drinks = db.Column(db.String)
    drugs = db.Column(db.String)
    smokes = db.Column(db.String)
    education = db.Column(db.String)
    job = db.Column(db.String)
    ethnicity = db.Column(db.String)
    religion = db.Column(db.String)
    offspring = db.Column(db.String)
    pets = db.Column(db.String)
    speaks = db.Column(db.String)
    sign = db.Column(db.String)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    likedUsername = db.Column(db.String, db.ForeignKey('users.username'))
    liked = db.Column(db.Boolean)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    totalMatches = db.Column(db.Integer)


DATABASE = 'C:\\Users\\pavit\\Desktop\\react-chat-app\\src\\users.db'
DATABASE2 = 'C:\\Users\\pavit\\Desktop\\react-chat-app\\src\\conversations.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_db2():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE2)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/analyze_profile', methods=['POST'])
def analyze_profile():
    print("ANALYZE CALLED")

    try:
        # Get the data from the request
        data = request.get_json()
        username = data.get("username")
        profile_details = data.get("profileDetails")

        # Check if both username and profileDetails are present
        if not username or not profile_details:
            return jsonify({"error": "Missing username or profile details"}), 400
        

        conn = get_db()
        cursor = conn.cursor()

        query = """
        SELECT age, status, sex, orientation, body_type, height, diet, drinks, drugs, smokes, education, job, ethnicity, 
               religion, offspring, pets, speaks, sign, essay0 
        FROM users WHERE username = ?
        """
        cursor.execute(query, (username,))
        user_profile = cursor.fetchone()

        # Check if user profile exists
        if not user_profile:
            return jsonify({"error": "User profile not found"}), 404

        # Extract user details into a dictionary
        user_columns = ['age', 'status', 'sex', 'orientation', 'body_type', 'height', 'diet', 'drinks', 'drugs', 'smokes',
                        'education', 'job', 'ethnicity', 'religion', 'offspring', 'pets', 'speaks', 'sign', 'essay0']
        user_profile_dict = dict(zip(user_columns, user_profile))                

        # Construct the prompt for the AI assistant
        prompt = f"""
        You are an AI assistant helping users on a matchmaking platform. Analyze the compatibility of the following two profiles:

        **User Profile (Analyzer)**
        Name: {username}
        Age: {user_profile_dict.get("age")}
        Location: {profile_details.get("location")}  # Assuming the user's location might also be needed
        Status: {user_profile_dict.get("status")}
        Sex: {user_profile_dict.get("sex")}
        Orientation: {user_profile_dict.get("orientation")}
        Body Type: {user_profile_dict.get("body_type")}
        Height: {user_profile_dict.get("height")}
        Diet: {user_profile_dict.get("diet")}
        Drinks: {user_profile_dict.get("drinks")}
        Drugs: {user_profile_dict.get("drugs")}
        Smokes: {user_profile_dict.get("smokes")}
        Education: {user_profile_dict.get("education")}
        Job: {user_profile_dict.get("job")}
        Ethnicity: {user_profile_dict.get("ethnicity")}
        Religion: {user_profile_dict.get("religion")}
        Offspring: {user_profile_dict.get("offspring")}
        Pets: {user_profile_dict.get("pets")}
        Languages Spoken: {user_profile_dict.get("speaks")}
        Zodiac Sign: {user_profile_dict.get("sign")}
        Bio: {user_profile_dict.get("essay0")}

        **Potential Match Profile**
        Name: {profile_details.get("name")}
        Age: {profile_details.get("age")}
        Location: {profile_details.get("location")}
        Status: {profile_details.get("status")}
        Sex: {profile_details.get("sex")}
        Orientation: {profile_details.get("orientation")}
        Body Type: {profile_details.get("body_type")}
        Height: {profile_details.get("height")}
        Diet: {profile_details.get("diet")}
        Drinks: {profile_details.get("drinks")}
        Drugs: {profile_details.get("drugs")}
        Smokes: {profile_details.get("smokes")}
        Education: {profile_details.get("education")}
        Job: {profile_details.get("job")}
        Ethnicity: {profile_details.get("ethnicity")}
        Religion: {profile_details.get("religion")}
        Offspring: {profile_details.get("offspring")}
        Pets: {profile_details.get("pets")}
        Languages Spoken: {profile_details.get("speaks")}
        Zodiac Sign: {profile_details.get("sign")}
        Bio: {profile_details.get("essay0")}

        Analyze the compatibility of these profiles and explain your reasoning. Also give the output in English language only, not in any other language.
        """
        print("Prompt = ", prompt)

        print("Prompt = ", prompt)

        # Send the prompt to GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        print("GPT Output = ",response.choices[0].message.content)

        # Check the response object for the content
        if response.choices and len(response.choices) > 0:
            analysis_result = response.choices[0].message.content
        else:
            analysis_result = "No analysis could be generated. Please try again."

        # Return the analysis result
        return jsonify({"analysisResult": analysis_result}), 200

    except Exception as e:
        print("Error during profile analysis:", str(e))
        return jsonify({"error": "An error occurred during profile analysis"}), 500


@app.route('/profiles/<current_username>', methods=['GET'])
def get_profiles(current_username):
    try:
        # Read ROWIDs from the text file
        filename = current_username+"_recommendations.txt"
        with open(filename, 'r') as file:
            rowids = file.read().split()
        
        # Convert ROWIDs from strings to integers
        rowids = [int(id) for id in rowids]

        conn = get_db()
        cursor = conn.cursor()
        
        # Prepare the query to select users based on ROWIDs and exclude the current username
        query = """
        SELECT * FROM users 
        WHERE username != ? AND ROWID IN ({})
        """.format(','.join('?' for _ in rowids))  # Use '?' placeholders for ROWIDs in the query

        # Execute the query with the current_username and the ROWIDs
        cursor.execute(query, (current_username, *rowids))
        profiles = cursor.fetchall()

        columns = ['age','status','sex','orientation','body_type','diet','drinks','drugs','education','ethnicity','height','income','job','last_online','location','offspring','pets','religion','sign','smokes','speaks','essay0','essay1','essay2','essay3','essay4','essay5','essay6','essay7','essay8','essay9','username','password','name']
        
        # Convert query results to a list of dictionaries
        result = [dict(zip(columns, profile)) for profile in profiles]

        conn.close()
        
        return jsonify({'profiles': result})
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/like', methods=['POST'])
def like_user():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()

    print(data)
    
    username = data.get('username')
    likedUsername = data.get('likedUsername')

    if not username or not likedUsername:
        return jsonify({'error': 'Username and likedUsername are required'}), 400

    try:
        cursor.execute('INSERT INTO like (username, likedUsername, liked) VALUES (?, ?, ?)', (username, likedUsername, True))
        conn.commit()
        return jsonify({'message': 'Like saved successfully'}), 200
    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/dislike', methods=['POST'])
def dislike_user():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()

    print(data)

    username = data.get('username')
    likedUsername = data.get('likedUsername')

    if not username or not likedUsername:
        return jsonify({'error': 'Username and likedUsername are required'}), 400

    try:
        cursor.execute('INSERT INTO like (username, likedUsername, liked) VALUES (?, ?, ?)', (username, likedUsername, False))
        conn.commit()
        return jsonify({'message': 'Dislike saved successfully'}), 200
    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/match/<twousers>', methods=['GET'])
def check_match(twousers):

    likedUsername = twousers.split(':')[0]
    current_username = twousers.split(':')[1]

    print('likeduser = ' + likedUsername)
    print('current user = ' + current_username)


    conn = get_db()
    cursor = conn.cursor()

    # Assuming 'user84335' is the current logged-in username. This should be dynamically set.    

    try:
        # Prepare the SQL query to check for mutual likes
        query = """
        SELECT * FROM like 
        WHERE username = ? AND likedUsername = ? AND liked = True
        """
        cursor.execute(query, (likedUsername, current_username))
        mutual_like1 = cursor.fetchone()

        query = """
        SELECT * FROM like 
        WHERE username = ? AND likedUsername = ? AND liked = True
        """
        cursor.execute(query, (current_username,likedUsername))        

        mutual_like2 = cursor.fetchone()

        print("ml1 = ",mutual_like1)
        print("ml2 = ",mutual_like2)


        # Check if a mutual like exists
        if mutual_like1 and mutual_like2:

            conn_conversations = sqlite3.connect('conversations.db')
            cursor_conv = conn_conversations.cursor()
            try:
                # Insert both ways to track conversation pairs
                current_time = datetime.now().isoformat()
                match_message = "It's a Match!! Use our HeartSync Assistant to get going!"
                cursor_conv.execute('INSERT INTO conversations (User1, User2, Timestamp, Message) VALUES (?, ?, ?, ?)', (current_username, likedUsername, current_time, match_message))
                #cursor_conv.execute('INSERT INTO conversations (User1, User2) VALUES (?, ?)', (likedUsername, current_username))
                conn_conversations.commit()
            except sqlite3.Error as e:
                conn_conversations.rollback()
                print(e)
            finally:
                cursor_conv.close()

            return jsonify({'match': True}), 200
        else:
            return jsonify({'match': False}), 200

    except sqlite3.Error as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)

