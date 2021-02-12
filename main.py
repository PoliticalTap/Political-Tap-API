from app import app
from flask import render_template, request
from votesmart import votesmart as Votesmart
import json
import tweepy

# Twitter 
twitter_auth = tweepy.OAuthHandler(app.config["TWITTER_KEY"], app.config["TWITTER_SECRET"])
twitter_auth.set_access_token(app.config["TWITTER_ACCESS_TOKEN"], app.config["TWITTER_ACCESS_TOKEN_SECRET"])

# Initialize Tweepy Library
Tweepy = tweepy.API(twitter_auth)

# Location Service
from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent = 'test_app')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getCandidateList", methods=["GET"])
def get_candidate_list():
    zip = request.args.get("zip")
    zip4 = request.args.get("zip4")
    candidates = Votesmart.candidates.getByZip(zip, zip4)

    elections = {}
    candidate_list = {}

    for candidate in candidates:
        parsed_candidate = candidate_list.get(candidate.candidateId)

        if (parsed_candidate):
            continue
        else:
            candidate_list[candidate.candidateId] = True

        election_office = candidate.electionOffice

        candidate_bio = Votesmart.candidatebio.getBio(candidate.candidateId)
        photo = candidate_bio.photo

        candidate_obj = {
            "candidate_id" : candidate.candidateId,
            "name" : candidate.ballotName,
            "party" : candidate.electionParties,
            "photo" : candidate_bio.photo
        }

        if candidate.runningMateId:
            running_mate = {
                "candidate_id" : candidate.runningMateId,
                "name" : candidate.runningMateName
            }

            candidate_obj["running_mate"] = running_mate

        
        if (election_office in elections.keys() and candidate.candidateId not in elections[election_office]):
            elections[election_office].append(candidate_obj)
        else:
            elections[election_office] = [candidate_obj]

    output = []
    for election in elections.keys():
        elect_item = {
            "election" : election,
            "candidates" : elections[election]
        }
        output.append(elect_item)
    
    return json.dumps(output)

@app.route("/getCandidate", methods=["GET"])
def get_candidate():
    candidate_id = request.args.get("candidate_id")
    candidate = Votesmart.candidatebio.getDetailedBio(candidate_id)

    bio = candidate["bio"]
    cand = bio["candidate"]

    if "election" in bio:
        name = bio["election"]["ballotName"]
        party = bio["election"]["parties"]
    else:
        name = "%s %s" % (bio["candidate"]["firstName"], bio["candidate"]["lastName"])
        if "office" in bio:
            party = bio["office"]["parties"]
        else:
            party = "Currently Unaffiliated"

    # Get ballot name

    candidate_obj = {
        "candidate_id" : candidate_id,
        "name" : name,
        "photo" : cand["photo"],
        "birthDate" : cand["birthDate"],
        "gender" : cand["gender"],
        "religion" : cand["religion"],
        "homeCity" : cand["homeCity"],
        "homeState" : cand["homeState"],
        "education" : cand.get("education"),
        "profession" : cand.get("profession"),
        "political" : cand.get("political"),
        "orgMembership" : cand.get("orgMembership"),
        "family" : cand.get("family"),
        "office" : bio.get("office", ""),
        "party" : party
    }

    return candidate_obj

@app.route("/getCandidateTweets", methods=["GET"])
def get_candidate_tweets():
    candidate_id = request.args.get("candidate_id")
    print(candidate_id)

    try:
        for adr in Votesmart.address.getOfficeWebAddress(candidate_id):
            address = str(adr)

            if "twitter" in address.lower():
                screen_name = address.split("/")[-1]
                screen_name = screen_name.split("?")[0]
    except:
        try:
            for adr in Votesmart.address.getCampaignWebAddress(candidate_id):
                address = str(adr)

                if "twitter" in address.lower():
                    screen_name = address.split("/")[-1]
                    screen_name = screen_name.split("?")[0]
        except:
            return {
                "error" : "Web Addresses not available for this candidate",
                "tweets" : []
            }
    
    print(screen_name)

    if screen_name == None:
        return {
            "error" : "Twitter account not available for this candidate",
            "tweets" : []
        }
    
    tweet_list = Tweepy.user_timeline(screen_name=screen_name, count=10)
    tweets = []
    
    for tweet in tweet_list:
        tweets.append(tweet._json)
    
    return {"tweets" : tweets}

@app.route("/getZipFromLocation")
def get_zip_from_location():
    latitude = request.args.get("latitude", 0)
    longitude = request.args.get("longitude", 0)

    try:
        location = geocoder.reverse((latitude, longitude))
        zip = location.raw["address"]["postcode"]
    except:
        return "Could not get zipcode"

    return zip

@app.route("/getFeedFromLocation", methods=["GET"])
def get_feed_from_location():
    zip = request.args.get("zip")
    zip4 = request.args.get("zip4")

    # Get list of candidates
    candidates = Votesmart.candidates.getByZip(zip, zip4)

    # Get twitter from candidates
    twitter_ids = []
    candidate_list = {}

    for candidate in candidates:

        candidate_id = candidate.candidateId
        parsed_candidate = candidate_list.get(candidate_id)

        # Prevent duplicate candidates from being appended
        if (parsed_candidate):
            continue
        else:
            candidate_list[candidate_id] = True

        try:
            for adr in Votesmart.address.getOfficeWebAddress(candidate_id):
                address = str(adr)

                if "twitter" in address.lower():
                    screen_name = address.split("/")[-1]
                    screen_name = screen_name.split("?")[0]

                    twitter_ids.append(screen_name)
        except:
            try:
                for adr in Votesmart.address.getCampaignWebAddress(candidate_id):
                    address = str(adr)

                    if "twitter" in address.lower():
                        screen_name = address.split("/")[-1]
                        screen_name = screen_name.split("?")[0]

                        twitter_ids.append(screen_name)
            except:
                print("No office or campaign web addresses found for: %s" % candidate_id)

    # Get timeline for each candidate
    tweets = []
    for screen_name in twitter_ids:
        tweet_list = Tweepy.user_timeline(screen_name=screen_name, count=5)
        
        for tweet in tweet_list:
            tweets.append(tweet._json)

    # Return merged timelines
    return {"tweets" : tweets}
    
if __name__ == "__main__":
    app.run(debug=True)