import logging
from datetime import datetime
from verify_data_utils import is_tachycardic


def add_patient_to_db(db, id, email, age):
    db[id] = {"email": email, "age": age, "heart_rate": []}
    logging.info("Patient id {} is registered.".format(id))
    return True


def add_hr_to_db(db, id, hr, timestamp):
    db[id]["heart_rate"].append((timestamp, hr))
    status = is_tachycardic(db[id]["age"], hr)
    if status == "tachycardic":
        logging.info("A tachycardic heart rate {} is posted for \
                     patient id {}. The attending e-mail is {}".format
                     (hr, id, db[id]["email"]))
    return status
