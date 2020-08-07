from verify_data_utils import is_tachycardic
from datetime import datetime


def generate_patient_status(db, id):
    if len(db[id]["heart_rate"]) == 0:
        return "No heart rate data available"
    else:
        hr = db[id]["heart_rate"][-1][1]
        timestamp = db[id]["heart_rate"][-1][0]
        status = is_tachycardic(db[id]["age"], hr)
        return {"heart_rate": hr, "status": status, "timestamp": timestamp}


def generate_hr_list(db, id):
    hr_list = []
    for hr_tupple in db[id]["heart_rate"]:
        hr_list.append(hr_tupple[1])
    return hr_list


def generate_hr_average(db, id):
    hr_list = generate_hr_list(db, id)
    if len(hr_list) == 0:
        return "No heart rate data available"
    hr_avg = sum(hr_list) / len(hr_list)
    return round(hr_avg)


def generate_interval_average(db, id, timestamp):
    hr_list = []
    for hr_tupple in db[id]["heart_rate"]:
        if datetime.strptime(hr_tupple[0], '%Y-%m-%d %H:%M:%S.%f') >= \
                datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f'):
            hr_list.append(hr_tupple[1])
    if len(hr_list) == 0:
        return "No heart rate data since {}".format(timestamp)
    hr_avg = sum(hr_list) / len(hr_list)
    return round(hr_avg)
