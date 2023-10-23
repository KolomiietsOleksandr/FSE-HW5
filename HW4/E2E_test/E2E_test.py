import unittest
import json
from flask import Flask
from HW1_3_codes.user import CustomUser
from HW1_3_codes.translator import CustomTranslator
from HW1_3_codes.online_count import UserStatsController
from HW1_3_codes.UserStatsUserController import UserStatsHistoryController
from HW1_3_codes.user_online_predictor import UserOnlinePredictorWithPrediction
from HW1_3_codes.users_online_predictor import UserOnlinePredictor
from HW4.user_average_time_tracker import UserAverageTimeTracker
from HW4.UserOnlineTimeCalculator import UserTotalTimeOnlineTracker
from HW4.user_forget_data import UserForgetDataHandler

app = Flask(__name__)

class TestE2E(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_initialize_users(self):
        custom_users = [
            {"username": "User1", "registration_date": "2023-10-08T10:00:00.000", "is_online": True, "online_time": None},
            {"username": "User2", "registration_date": "2023-10-08T11:00:00.000", "is_online": False, "online_time": None},
            {"username": "User3", "registration_date": "2023-10-08T12:00:00.000", "is_online": True, "online_time": None},
        ]

        data = {
            "custom_users": custom_users
        }

        response = self.app.post('/initialize_users', json=data)
        self.assertEqual(response.status_code, 200)

    def test_calculate_users_online_count(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        date1 = datetime(2023, 10, 8, 10, 30, 0)

        data = {
            "custom_users": custom_users,
            "date": date1.strftime('%Y-%m-%d %H:%M:%S')
        }

        response = self.app.post('/calculate_users_online_count', json=data)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['online_count'], 1)

    def test_get_user_history(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = self.app.post('/initialize_users', json=data)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/get_user_history?username=User1&date=2023-10-08-10:30')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('history' in result)

    def test_predict_user_online(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = self.app.post('/initialize_users', json=data)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/predict_user_online?username=User1&date=2023-10-08-11:00&threshold=0.5')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('prediction' in result)

    def test_calculate_average_users_online(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = self.app.post('/initialize_users', json=data)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/calculate_average_users_online')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('average_online' in result)

    def test_calculate_daily_average(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = this.app.post('/initialize_users', json=data)
        this.assertEqual(response.status_code, 200)

        response = this.app.get('/calculate_daily_average?user_id=User1')
        result = json.loads(response.data)
        this.assertEqual(response.status_code, 200)
        this.assertTrue('daily_average' in result)

    def test_calculate_weekly_average(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = this.app.post('/initialize_users', json=data)
        this.assertEqual(response.status_code, 200)

        response = this.app.get('/calculate_weekly_average?user_id=User1')
        result = json.loads(response.data)
        this.assertEqual(response.status_code, 200)
        this.assertTrue('weekly_average' in result)

    def test_get_total_time_online(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = this.app.post('/initialize_users', json=data)
        this.assertEqual(response.status_code, 200)

        response = this.app.get('/get_total_time_online?user_id=User1')
        result = json.loads(response.data)
        this.assertEqual(response.status_code, 200)
        this.assertTrue('total_time_online' in result)

    def test_forget_user_data(self):
        custom_users = [
            CustomUser("User1", "2023-10-08T10:00:00.000", True, None),
            CustomUser("User2", "2023-10-08T11:00:00.000", False, None),
            CustomUser("User3", "2023-10-08T12:00:00.000", True, None),
        ]

        data = {
            "custom_users": custom_users
        }

        response = this.app.post('/initialize_users', json=data)
        this.assertEqual(response.status_code, 200)

        response = this.app.get('/forget_user_data?user_id=User1')
        result = json.loads(response.data)
        this.assertEqual(response.status_code, 200)
        this.assertTrue('deleted_user' in result)

if __name__ == '__main__':
    unittest.main()
