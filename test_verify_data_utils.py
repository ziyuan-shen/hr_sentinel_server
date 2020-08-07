import pytest


@pytest.mark.parametrize("d, expected", [
    ({"patient_id": 100, "attending_email": "john.smith@duke.edu",
     "patient_age": 40}, True),
    ({"patient_id": "101", "attending_email": "john.smith@duke.edu",
     "patient_age": 40}, True),
    ({"patient_id": 100, "attending_email": "john.smith@duke.edu",
     "patient_age": "45"}, True),
    ({"patient_id": 100, "attending_email": 10, "patient_age": 40},
     "Key attending_email not correct type"),
    ({"patient_id": "uu", "attending_email": "john.smith@duke.edu",
     "patient_age": 40}, "Key patient_id is not integer"),
    ({"patient_id": 100, "attending_email": "john.smith@duke.edu",
     "patient_age": "ij"}, "Key patient_age is not integer"),
    ({"patient_id": 100, "patient_age": 40},
     "Key attending_email not found"),
])
def test_verify_newp_info(d, expected):
    from verify_data_utils import verify_newp_info
    answer = verify_newp_info(d)
    assert answer == expected


@pytest.mark.parametrize("d, expected", [
    ({"patient_id": 100, "heart_rate": 80}, True),
    ({"patient_id": "100", "heart_rate": 80}, True),
    ({"patient_id": 100, "heart_rate": "80"}, True),
    ({"heart_rate": 80}, "Key patient_id not found"),
    ({"patient_id": 100}, "Key heart_rate not found"),
    ({"patient_id": "iu", "heart_rate": 80}, "Key patient_id is not integer"),
    ({"patient_id": 100, "heart_rate": "ase"}, "Key heart_rate is not integer")
])
def test_verify_hr_info(d, expected):
    from verify_data_utils import verify_hr_info
    answer = verify_hr_info(d)
    assert answer == expected


@pytest.mark.parametrize("age, hr, expected", [
    (1, 150, "not tachycardic"),
    (3, 140, "tachycardic"),
    (40, 100, "not tachycardic"),
    (45, 110, "tachycardic")
])
def test_is_tachycardic(age, hr, expected):
    from verify_data_utils import is_tachycardic
    answer = is_tachycardic(age, hr)
    assert answer == expected


@pytest.mark.parametrize("db, id, expected", [
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, 100, True),
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, 101, False),
])
def test_is_patient_in_db(db, id, expected):
    from verify_data_utils import is_patient_in_database
    answer = is_patient_in_database(db, id)
    assert answer == expected


@pytest.mark.parametrize("db, patient_id, expected", [
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, "100", True),
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, "abc", "Bad patient id in URL"),
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, "101", "Patient id 101 does not exist in database"),
])
def test_verify_get_patient_status_input(db, patient_id, expected):
    from verify_data_utils import verify_get_patient_status_input
    answer = verify_get_patient_status_input(db, patient_id)
    assert answer == expected


@pytest.mark.parametrize("d, expected", [
    ({"patient_id": 100}, "Key heart_rate_average_since not found"),
    ({"heart_rate_average_since": "2018-03-09 11:00:36.372339"},
     "Key patient_id not found"),
    ({"patient_id": "aa", "heart_rate_average_since":
      "2018-03-09 11:00:36.372339"},
     "Key patient_id is not integer"),
    ({"patient_id": 101, "heart_rate_average_since":
      "2018-03-09 11:00:36.372339"},
     True),
    ({"patient_id": 101, "heart_rate_average_since": "2018-03-09"},
     "Key heart_rate_average_since not in correct datetime format"),
    ({"patient_id": 101, "heart_rate_average_since": 10},
     "Key heart_rate_average_since not in correct datetime format"),
])
def test_verify_get_interval_average_input(d, expected):
    from verify_data_utils import verify_get_interval_average_input
    answer = verify_get_interval_average_input(d)
    assert answer == expected
