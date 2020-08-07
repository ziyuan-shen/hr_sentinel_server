import requests

server_name = "http://vcm-7631.vm.duke.edu:5007/hrss/send_email"


def send_email(to_email, id, hr, timestamp):
    r = requests.post(
        server_name, json={
            "from_email": "patient{}@duke.edu".format(id),
            "to_email": to_email, "subject": "tachycardic detected",
            "content": "Patient id {} had heart rate {} at {}."
            .format(id, hr, timestamp)
            }
        )
    return r.status_code, r.text
