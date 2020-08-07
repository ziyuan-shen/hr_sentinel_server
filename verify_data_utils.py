from datetime import datetime


def verify_newp_info(in_dict):
    """
    Verify in_dict contains the correct keys and data
    {"patient_id": 1, # usually this would be the patient MRN
    "attending_email": "dr_user_id@yourdomain.com",
    "patient_age": 50, # in years}
    """
    for key in ("patient_id", "attending_email", "patient_age"):
        if key not in in_dict.keys():
            return "Key {} not found".format(key)
        if key == "attending_email":
            if type(in_dict[key]) is not str:
                return "Key attending_email not correct type"
        else:
            try:
                integer = int(in_dict[key])
            except ValueError:
                return "Key {} is not integer".format(key)
    return True


def verify_hr_info(in_dict):
    """
    Verify the json contains the correct keys and data
    {"patient_id": 1,
    "heart_rate": 100}
    """
    for key in ("patient_id", "heart_rate"):
        if key not in in_dict.keys():
            return "Key {} not found".format(key)
        try:
            integer = int(in_dict[key])
        except ValueError:
            return "Key {} is not integer".format(key)
    return True


def is_tachycardic(age, hr):
    if age in range(1, 3):
        threshold = 151
    elif age in range(3, 5):
        threshold = 137
    elif age in (5, 8):
        threshold = 133
    elif age in (8, 12):
        threshold = 130
    elif age in (12, 16):
        threshold = 119
    else:
        threshold = 100
    if hr > threshold:
        return "tachycardic"
    else:
        return "not tachycardic"


def is_patient_in_database(db, id):
    return id in db


def verify_get_patient_status_input(db, patient_id):
    try:
        id = int(patient_id)
    except ValueError:
        return "Bad patient id in URL"
    if is_patient_in_database(db, id) is False:
        return "Patient id {} does not exist in database".format(id)
    return True


def verify_get_interval_average_input(in_dict):
    """
    Verify the json contains the correct keys and data
    {"patient_id": 1,
    "heart_rate_average_since": "2018-03-09 11:00:36.372339"}
    """
    for key in ("patient_id", "heart_rate_average_since"):
        if key not in in_dict:
            return "Key {} not found".format(key)
        if key == "patient_id":
            try:
                id = int(in_dict[key])
            except ValueError:
                return "Key patient_id is not integer"
        if key == "heart_rate_average_since":
            try:
                timestamp = datetime.strptime(in_dict[key],
                                              '%Y-%m-%d %H:%M:%S.%f')
            except:
                return "Key heart_rate_average_since not " \
                    + "in correct datetime format"
    return True
