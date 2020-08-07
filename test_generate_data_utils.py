import pytest


@pytest.mark.parametrize("db, id, expected", [
    ({100: {"email": "john.smith@duke.edu", "age": 40,
     "heart_rate": []}}, 100, "No heart rate data available"),
    ({100: {"email": "john.smith@duke.edu", "age": 40,
      "heart_rate": [('2020-04-11 19:42:57.960440', 140)]}}, 100,
     {"heart_rate": 140, "status": "tachycardic",
      "timestamp": '2020-04-11 19:42:57.960440'}),
    ({100: {"email": "john.smith@duke.edu", "age": 40,
      "heart_rate": [('2020-04-11 19:42:57.960440', 140),
                     ('2020-04-12 17:52:58.775761', 80)]}}, 100,
     {"heart_rate": 80, "status": "not tachycardic",
      "timestamp": '2020-04-12 17:52:58.775761'})
])
def test_generate_patient_status(db, id, expected):
    from generate_data_utils import generate_patient_status
    answer = generate_patient_status(db, id)
    assert answer == expected


@pytest.mark.parametrize("db, id, expected", [
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": []}}, 100, []),
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": [('2020-04-11 19:42:57.960440', 140)]}},
   100, [140]),
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": [('2020-04-11 19:42:57.960440', 140),
                   ('2020-04-12 17:52:58.775761', 80)]}},
   100, [140, 80])
])
def test_generate_hr_list(db, id, expected):
    from generate_data_utils import generate_hr_list
    answer = generate_hr_list(db, id)
    assert answer == expected


@pytest.mark.parametrize("db, id, expected", [
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": []}}, 100, "No heart rate data available"),
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": [('2020-04-11 19:42:57.960440', 140)]}},
   100, 140),
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": [('2020-04-11 19:42:57.960440', 140),
                   ('2020-04-12 17:52:58.775761', 80)]}},
   100, 110)
])
def test_generate_hr_average(db, id, expected):
    from generate_data_utils import generate_hr_average
    answer = generate_hr_average(db, id)
    assert answer == expected


@pytest.mark.parametrize("db, id, timestamp, expected", [
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": []}}, 100, '2020-04-11 19:42:57.960440',
   "No heart rate data since 2020-04-11 19:42:57.960440"),
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": [('2020-04-11 19:42:57.960440', 140)]}},
   100, '2020-04-10 19:42:57.960440', 140),
  ({100: {"email": "john.smith@duke.edu", "age": 40,
    "heart_rate": [('2020-04-11 19:42:57.960440', 140),
                   ('2020-04-12 17:52:58.775761', 80)]}},
   100, '2020-03-11 19:42:57.960440', 110)
])
def test_generate_interval_average(db, id, timestamp, expected):
    from generate_data_utils import generate_interval_average
    answer = generate_interval_average(db, id, timestamp)
    assert answer == expected
