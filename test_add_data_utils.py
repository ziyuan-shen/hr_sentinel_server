import pytest


@pytest.mark.parametrize("db, id, email, age, expected", [
    ({}, 100, "john.smith@duke.edu", 40, True)
])
def test_add_patient_to_db(db, id, email, age, expected):
    from add_data_utils import add_patient_to_db
    answer = add_patient_to_db(db, id, email, age)
    assert answer == expected


@pytest.mark.parametrize("db, id, hr, timestamp, expected", [
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, 100, 140, '2020-04-11 19:42:57.960440',
     "tachycardic"),
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": [('2020-04-11 19:42:57.960440', 140)]}},
     100, 80, '2020-04-11 23:30:56.055539', "not tachycardic")
])
def test_add_hr_to_db(db, id, hr, timestamp, expected):
    from add_data_utils import add_hr_to_db
    answer = add_hr_to_db(db, id, hr, timestamp)
    assert answer == expected
