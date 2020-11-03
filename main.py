from app import app
from flask import render_template, request
from votesmart import votesmart as Votesmart
import json

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getCandidateList", methods=["GET"])
def get_candidate_list():
    zip = request.args.get("zip")
    zip4 = request.args.get("zip4")
    candidates = Votesmart.candidates.getByZip(zip, zip4)

    output = {}

    for candidate in candidates:

        if (candidate.electionStatus != "Running"):
            continue

        election_office = candidate.electionOffice

        # TODO: Do not include null running mate
        candidate_obj = {
            "candidate_id" : candidate.candidateId,
            "name" : candidate.ballotName,
            "party" : candidate.electionParties,
            "running_mate" :
            {
                "candidate_id" : candidate.runningMateId,
                "name" : candidate.runningMateName
            }
        }
        
        if (election_office in output.keys()):
            output[election_office].append(candidate_obj)
        else:
            output[election_office] = [candidate_obj]

    return json.dumps(output)

@app.route("/testCandidate", methods=["GET"])
def test_get_candidate_list():
    return {
        "President": [
            {
                "candidate_id": "53279",
                "name": "Joe Biden",
                "party": "Democratic",
                "running_mate": {
                    "candidate_id": "120012",
                    "name": "Kamala Devi Harris"
                }
            },
            {
                "candidate_id": "15723",
                "name": "Donald J. Trump",
                "party": "Republican",
                "running_mate": {
                    "candidate_id": "34024",
                    "name": "Mike Pence"
                }
            }
        ],
        "U.S. House": [
            {
                "candidate_id": "166760",
                "name": "Warren Davidson",
                "party": "Republican",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            },
            {
                "candidate_id": "178848",
                "name": "Vanessa Enoch",
                "party": "Democratic",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            }
        ],
        "State House": [
            {
                "candidate_id": "179097",
                "name": "Sara Carruthers",
                "party": "Republican",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            },
            {
                "candidate_id": "189460",
                "name": "Jennifer L. Gross",
                "party": "Republican",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            },
            {
                "candidate_id": "189459",
                "name": "Chuck Horn",
                "party": "Democratic",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            },
            {
                "candidate_id": "189462",
                "name": "Thomas Hall",
                "party": "Republican",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            },
            {
                "candidate_id": "189464",
                "name": "Michelle E. Novak",
                "party": "Democratic",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            }
        ],
        "State Senate": [
            {
                "candidate_id": "78001",
                "name": "George F. Lang",
                "party": "Republican",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            },
            {
                "candidate_id": "179098",
                "name": "Kathy Wyenandt",
                "party": "Democratic",
                "running_mate": {
                    "candidate_id": "",
                    "name": ""
                }
            }
        ]
    }

if __name__ == "__main__":
    app.run(debug=True)