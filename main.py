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

@app.route("/testCandidate", methods=["GET"])
def test_get_candidate_list():
    return '''
    [
        {
            "election": "President",
            "candidates": [
                {
                    "candidate_id": "53279",
                    "name": "Joe Biden",
                    "party": "Democratic",
                    "photo": "https://static.votesmart.org/canphoto/53279.jpg",
                    "running_mate": {
                        "candidate_id": "120012",
                        "name": "Kamala Devi Harris"
                    }
                },
                {
                    "candidate_id": "15723",
                    "name": "Donald J. Trump",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/15723.jpg",
                    "running_mate": {
                        "candidate_id": "34024",
                        "name": "Mike Pence"
                    }
                }
            ]
        },
        {
            "election": "U.S. House",
            "candidates": [
                {
                    "candidate_id": "166760",
                    "name": "Warren Davidson",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/166760.jpg"
                },
                {
                    "candidate_id": "178848",
                    "name": "Vanessa Enoch",
                    "party": "Democratic",
                    "photo": "https://static.votesmart.org/canphoto/178848.jpg"
                },
                {
                    "candidate_id": "150575",
                    "name": "Matt Guyette",
                    "party": "Democratic",
                    "photo": "https://static.votesmart.org/canphoto/150575.jpg"
                },
                {
                    "candidate_id": "167042",
                    "name": "Edward Meer",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/167042.jpg"
                }
            ]
        },
        {
            "election": "State House",
            "candidates": [
                {
                    "candidate_id": "179097",
                    "name": "Sara Carruthers",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/179097.jpg"
                },
                {
                    "candidate_id": "189460",
                    "name": "Jennifer L. Gross",
                    "party": "Republican",
                    "photo": ""
                },
                {
                    "candidate_id": "189459",
                    "name": "Chuck Horn",
                    "party": "Democratic",
                    "photo": ""
                },
                {
                    "candidate_id": "161531",
                    "name": "Mark S. Welch",
                    "party": "Republican",
                    "photo": ""
                },
                {
                    "candidate_id": "189463",
                    "name": "Brett Guido",
                    "party": "Republican",
                    "photo": ""
                },
                {
                    "candidate_id": "189462",
                    "name": "Thomas Hall",
                    "party": "Republican",
                    "photo": ""
                },
                {
                    "candidate_id": "189461",
                    "name": "Diane Mullins",
                    "party": "Republican",
                    "photo": ""
                },
                {
                    "candidate_id": "189464",
                    "name": "Michelle E. Novak",
                    "party": "Democratic",
                    "photo": ""
                },
                {
                    "candidate_id": "120535",
                    "name": "Jeffrey L. Wellbaum",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/120535.jpg"
                }
            ]
        },
        {
            "election": "State Senate",
            "candidates": [
                {
                    "candidate_id": "167037",
                    "name": "Candice Keller",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/167037.jpg"
                },
                {
                    "candidate_id": "78001",
                    "name": "George F. Lang",
                    "party": "Republican",
                    "photo": "https://static.votesmart.org/canphoto/78001.jpg"
                },
                {
                    "candidate_id": "78002",
                    "name": "Lee Wong",
                    "party": "Republican",
                    "photo": ""
                },
                {
                    "candidate_id": "179098",
                    "name": "Kathy Wyenandt",
                    "party": "Democratic",
                    "photo": "https://static.votesmart.org/canphoto/179098.jpg"
                }
            ]
        }
    ]
    '''
    
if __name__ == "__main__":
    app.run(debug=True)