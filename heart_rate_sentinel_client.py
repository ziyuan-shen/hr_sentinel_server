import requests

server_name = "http://127.0.0.1:5000"


def add_patient(np):
    r = requests.post(server_name+"/api/new_patient", json=np)
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.text))
    print(r.status_code)
    print(r.json())


def add_hr(hr_dict):
    r = requests.post(server_name+"/api/heart_rate", json=hr_dict)
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.txt))
    print(r.status_code)
    print(r.json())


def get_patient_status(id):
    r = requests.get(server_name+"/api/status/{}".format(id))
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.txt))
    print(r.status_code)
    print("Patient id {} status:".format(id))
    print(r.json())


def get_heart_rate(id):
    r = requests.get(server_name+"/api/heart_rate/{}".format(id))
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.txt))
    print(r.status_code)
    print("Patient id {} all heart rates:".format(id))
    print(r.json())


def get_heart_rate_average(id):
    r = requests.get(server_name+"/api/heart_rate/average/{}".format(id))
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.txt))
    print(r.status_code)
    print("Patient id {} average heart rate:".format(id))
    print(r.json())


def get_interval_average(in_dict):
    r = requests.post(server_name+"/api/heart_rate/interval_average",
                      json=in_dict)
    if r.status_code != 200:
        print("Error: {} - {}".format(r.status_code, r.txt))
    print(r.status_code)
    print("Patient id {} average heart rate since {}:"
          .format(in_dict["patient_id"], in_dict["heart_rate_average_since"]))
    print(r.json())


if __name__ == "__main__":
    add_patient({"patient_id": "100", "attending_email":
                 "john.smith@duke.edu", "patient_age": 40})
    add_hr({"patient_id": 100, "heart_rate": "140"})
    add_hr({"patient_id": 100, "heart_rate": 80})
    get_patient_status(100)
    get_heart_rate(100)
    get_heart_rate_average(100)
    get_interval_average({"patient_id": 100,
                          "heart_rate_average_since":
                          '2018-04-12 17:52:58.775761'})
    add_hr({"patient_id": 100, "heart_rate": 90})
    get_interval_average({"patient_id": 100,
                          "heart_rate_average_since":
                          '2018-04-12 17:52:58.775761'})
    get_interval_average({"patient_id": 100,
                          "heart_rate_average_since":
                          '2020-08-12 17:52:58.775761'})
