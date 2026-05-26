import unittest
import csv
import os

# importing functions from main file
import student_manager as sm

# using a different file for testing so real data is not affected
sm.filename = "test_data.csv"

class TestAddStudent(unittest.TestCase):

    def setUp(self):
        # delete test file before each test
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def tearDown(self):
        # cleanup after test
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_file_is_created(self):
        sm.create_file()
        self.assertTrue(os.path.exists("test_data.csv"))

    def test_empty_at_start(self):
        sm.create_file()
        result = sm.read_students()
        self.assertEqual(result, [])

    def test_id_starts_from_S001(self):
        result = sm.make_id([])
        self.assertEqual(result, "S001")

    def test_id_increments(self):
        fake_students = [{"ID": "S003"}]
        result = sm.make_id(fake_students)
        self.assertEqual(result, "S004")

    def test_save_and_read(self):
        # saving one student and reading back
        students = [{"ID": "S001", "Name": "Rahul", "Age": "20", "Marks": "85.0", "Subject": "Maths"}]
        sm.save_students(students)
        result = sm.read_students()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Name"], "Rahul")

class TestDeleteStudent(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
        # add one student before delete test
        sm.save_students([
            {"ID": "S001", "Name": "Priya", "Age": "21", "Marks": "90.0", "Subject": "Physics"}
        ])

    def tearDown(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_student_count_after_delete(self):
        students = sm.read_students()
        students.remove(students[0])
        sm.save_students(students)
        result = sm.read_students()
        # should be empty now
        self.assertEqual(len(result), 0)

class TestSearch(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
        sm.save_students([
            {"ID": "S001", "Name": "Amit", "Age": "20", "Marks": "75.0", "Subject": "Chemistry"},
            {"ID": "S002", "Name": "Sunita", "Age": "22", "Marks": "88.0", "Subject": "Biology"},
        ])

    def tearDown(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_search_by_name(self):
        students = sm.read_students()
        # manually doing search logic
        result = [s for s in students if "amit" in s["Name"].lower()]
        self.assertEqual(len(result), 1)

    def test_search_not_found(self):
        students = sm.read_students()
        result = [s for s in students if "xyz" in s["Name"].lower()]
        self.assertEqual(len(result), 0)

# run tests
if __name__ == "__main__":
    unittest.main(verbosity=2)
