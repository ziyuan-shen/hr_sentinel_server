from flask import Flask, jsonify, request
import logging
from datetime import datetime
from verify_data_utils import verify_newp_info
from verify_data_utils import verify_hr_info
from verify_data_utils import verify_get_patient_status_input
from verify_data_utils import verify_get_interval_average_input
from add_data_utils import add_patient_to_db
from add_data_utils import add_hr_to_db
from send_email import send_email
from generate_data_utils import generate_patient_status
from generate_data_utils import generate_hr_list
from generate_data_utils import generate_hr_average
from generate_data_utils import generate_interval_average

db = {}

app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_on():
    """ Check the server status.

    :param: None
    :returns: string containing server is on
    """
    server_on = "Heart Rate Sentinel Server Server is On"
    return server_on


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    """
    Receiving the posting json
    Verify the json contains the correct keys and data
    {"patient_id": 1, # usually this would be the patient MRN
    "attending_email": "dr_user_id@yourdomain.com",
    "patient_age": 50, # in years}
    If data is bad, reject request with bad status to client
    If data is good, add patient to database
    return good status to client
    """
    in_dict = request.get_json()
    check_result = verify_newp_info(in_dict)
    if check_result is not True:
        return jsonify(check_result), 400
    add_patient_to_db(db, int(in_dict["patient_id"]),
                      in_dict["attending_email"], int(in_dict["patient_age"]))
    return jsonify("Patient added"), 200


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    """
    Receiving the posting json
    Verify the json contains the correct keys and data
    {"patient_id": 1,
    "heart_rate": 100}
    If data is bad, reject request with bad status to client
    If data is good, add heart rate and timestamp to indicated patient
    If heart rate is tachycardic, send email to attending physician
    If email is not sent successfully, reject request with email sending error
    return good status to client
    """
    in_dict = request.get_json()
    check_result = verify_hr_info(in_dict)
    if check_result is not True:
        return jsonify(check_result), 400
    id = int(in_dict["patient_id"])
    hr = int(in_dict["heart_rate"])
    timestamp = str(datetime.now())
    status = add_hr_to_db(db, id, hr, timestamp)
    result = "Heart rate added\n" + "Status: {}".format(status)
    if status == "tachycardic":
        email_status_code, email_text = send_email(db[id]["email"],
                                                   id, hr, timestamp)
        if email_status_code != 200:
            return "email sending error\n" + email_text, 400
        result += ("\n" + email_text)
    return jsonify(result), 200


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_patient_status(patient_id):
    """Return a dictionary in a JSON string containing the latest heart rate
    {
    "heart_rate": 100,
    "status":  "tachycardic" | "not tachycardic",
    "timestamp": "2018-03-09 11:00:36.372339"
    }
    """
    check_result = verify_get_patient_status_input(db, patient_id)
    if check_result is not True:
        return check_result, 400
    status = generate_patient_status(db, int(patient_id))
    return jsonify(status)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate(patient_id):
    """Return a list of all the previous heart rate measurements for the patient
    """
    check_result = verify_get_patient_status_input(db, patient_id)
    if check_result is not True:
        return check_result, 400
    result = generate_hr_list(db, int(patient_id))
    return jsonify(result)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_heart_rate_average(patient_id):
    """Return the patient's average heart rate, as an integer
    """
    check_result = verify_get_patient_status_input(db, patient_id)
    if check_result is not True:
        return check_result, 400
    result = generate_hr_average(db, int(patient_id))
    return jsonify(result)


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def get_heart_rate_interval_average():
    """
    Receiving the posting json
    Verify the json contains the correct keys and data
    {"patient_id": 1,
    "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string}
    If data is bad, reject request with bad status to client
    If data is good, return the average, as an integer,
    of all the heart rates that have been posted for
    the specified patient since the given date/time
    return good status to client
    """
    in_dict = request.get_json()
    check_result = verify_get_interval_average_input(in_dict)
    if check_result is not True:
        return jsonify(check_result), 400
    result = generate_interval_average(db, int(in_dict["patient_id"]),
                                       in_dict["heart_rate_average_since"])
    return jsonify(result)


if __name__ == '__main__':
    logging.basicConfig(filename="logging.txt", filemode="w",
                        level=logging.INFO)
    app.run(host="0.0.0.0")
