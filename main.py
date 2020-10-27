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

if __name__ == "__main__":
    app.run(debug=True)