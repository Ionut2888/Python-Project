import unittest
from main import *

class Test(unittest.TestCase):
    log_entries, errors = count_logs("testfile.txt")

    # Log Identification Test
    def test_count_logs(self):
        # Error
        actual = "Warning: Skipped line 17 as it does not match the expected format."
        self.assertEqual(self.errors, actual)
        
        # Logs
        actual = [('INFO', 'SYSTEM', '01:46:48', 'has started running...', None),
                  ('INFO', 'SYSTEM', '01:46:48', 'has ran successfully in 16ms', 16),
                  ('ERROR', 'BackendApp', '04:22:33', 'has failed after 25ms. Retrying...', 25),
                  ('INFO', 'BackendApp', '13:08:50', 'has started running...', None),
                  ('INFO', 'BackendApp', '13:08:50', 'has ran successfully in 20ms', 20),
                  ('DEBUG', 'BackendApp', '16:11:12', 'is still running, please wait...', None),
                  ('INFO', 'API', '17:23:35', 'has started running...', None),
                  ('INFO', 'API', '17:23:35', 'has ran successfully in 14ms', 14),
                  ('DEBUG', 'SYSTEM', '02:49:49', 'is still running, please wait...', None),
                  ('INFO', 'FrontendApp', '02:51:24', 'has started running...', None),
                  ('INFO', 'FrontendApp', '02:51:24', 'has ran successfully in 15ms', 15),
                  ('ERROR', 'API', '12:32:31', 'has failed after 28ms. Retrying...', 28),
                  ('DEBUG', 'API', '05:29:28', 'is still running, please wait...', None),
                  ('DEBUG', 'FrontendApp', '13:48:30', 'is still running, please wait...', None),
                  ('INFO', 'BackendApp', '12:26:42', 'has started running...', None),
                  ('INFO', 'BackendApp', '12:26:42', 'has ran successfully in 18ms', 18)]
        self.assertEqual(self.log_entries, actual)

    # Req 1 Test
    def test_count_and_print_logs(self):
        actual = "Log Counts:\n"
        actual += "ERROR BackendApp: 1 logs\nERROR API: 1 logs\n"
        actual += "DEBUG BackendApp: 1 logs\nDEBUG SYSTEM: 1 logs\n"
        actual += "DEBUG API: 1 logs\nDEBUG FrontendApp: 1 logs\n"
        actual += "INFO SYSTEM: 1 logs\nINFO BackendApp: 2 logs\n"
        actual += "INFO API: 1 logs\nINFO FrontendApp: 1 logs\n"
        self.assertEqual(count_and_print_logs(self.log_entries), actual)
        self.assertEqual(count_and_print_logs([]), "Log Counts:\n")
    # Req 2 Test
    def test_average_successful_run_time(self):
        actual = "\nAverage Successful Run Time:\n"
        actual += "BackendApp: 19.00 ms\nAPI: 14.00 ms\nFrontendApp: 15.00 ms"
        self.assertEqual(average_successful_run_time(self.log_entries), actual)
        self.assertEqual(average_successful_run_time([]), "No relevant INFO logs found.")

    # Req 3 Test
    def test_count_failure(self):
        # Test File
        actual = "\nFailure Counts:"
        actual += "\nBackendApp: 1 failures\nAPI: 1 failures"
        self.assertEqual(count_failures(self.log_entries), actual)
        
        # Empty File / No ERROR Logs
        self.assertEqual(count_failures([]), "\nFailure Counts:")

    # Req 4 Test
    def test_most_failed_app(self):
        # Test File Equality
        actual = "\nApp with the most failed runs:"
        actual += "\nBackendApp: 1 failures"
        self.assertEqual(most_failed_app(self.log_entries), actual)
        
        # Test File Non-Equality
        mod_logs = self.log_entries[:]
        actual = "\nApp with the most failed runs:"
        actual += "\nAPI: 2 failures"
        mod_logs.append(("ERROR", "API", "00:00:00", "has failed after 25ms. Retrying...", 25))
        self.assertEqual(most_failed_app(mod_logs), actual)
        
        # Empty File / No ERROR Logs
        actual = "\nNo ERROR logs found."
        self.assertEqual(most_failed_app([]), actual)

    # Req 5 Test
    def test_most_successful_app(self):
        # Test File
        actual = "\nApp with the most successful runs:"
        actual += "\nBackendApp: 2 successful runs"
        self.assertEqual(most_successful_app(self.log_entries), actual)

        # Empty File / No Succes Logs
        actual = "\nNo successful INFO logs found."
        self.assertEqual(most_successful_app([]), actual)

    # Req 6 Test
    def test_most_failed_third_of_day(self):
        # Test File Equality
        actual = "\nThird of the day with the most failed runs:"
        actual += "\n00:00:00-07:59:59: 1 failures"
        log_entries2, errors2 = count_logs("testfile.txt")
        self.assertEqual(log_entries2, self.log_entries)
        self.assertEqual(most_failed_third_of_day(self.log_entries), actual)

        # Test File Non-Equality
        mod_logs = self.log_entries[:]
        mod_logs.append(("ERROR", "API", "00:00:00", "has failed after 25ms. Retrying...", 25))
        actual = actual = "\nThird of the day with the most failed runs:"
        actual += "\n00:00:00-07:59:59: 2 failures"
        self.assertEqual(most_failed_third_of_day(mod_logs), actual)

        # Empty File / No Fails
        actual = "\nNo fails today!"
        self.assertEqual(most_failed_third_of_day([]), actual)

    # Req 7 Test
    def test_longest_shortest_successful_run_times(self):
        # Test File
        actual = "\nLongest Run: BackendApp 13:08:50 20ms"
        actual += "\nShortest Run: API 17:23:35 14ms"
        self.assertEqual(longest_shortest_successful_run_times(self.log_entries), actual)

        # Empty File / No Succes Logs
        actual = "\nNo successful runs found."
        self.assertEqual(longest_shortest_successful_run_times([]), actual)

    # Req 8 Test
    def test_most_active_hour_by_app_and_log_type(self):
        # Test File
        actual = "\nMost Active Hour by App and Log Type:"
        actual += "\nHour=17:00:00-17:59:00, App=API, Log Type=INFO, Count=2"
        actual += "\nHour=12:00:00-12:59:00, App=API, Log Type=ERROR, Count=1"
        actual += "\nHour=05:00:00-05:59:00, App=API, Log Type=DEBUG, Count=1"
        actual += "\nHour=13:00:00-13:59:00, App=BackendApp, Log Type=INFO, Count=2"
        actual += "\nHour=04:00:00-04:59:00, App=BackendApp, Log Type=ERROR, Count=1"
        actual += "\nHour=16:00:00-16:59:00, App=BackendApp, Log Type=DEBUG, Count=1"
        actual += "\nHour=02:00:00-02:59:00, App=FrontendApp, Log Type=INFO, Count=2"
        actual += "\nNo logs, App=FrontendApp, Log Type=ERROR"
        actual += "\nHour=13:00:00-13:59:00, App=FrontendApp, Log Type=DEBUG, Count=1"
        actual += "\nHour=01:00:00-01:59:00, App=SYSTEM, Log Type=INFO, Count=2"
        actual += "\nNo logs, App=SYSTEM, Log Type=ERROR"
        actual += "\nHour=02:00:00-02:59:00, App=SYSTEM, Log Type=DEBUG, Count=1"
        self.assertEqual(most_active_hour_by_app_and_log_type(self.log_entries), actual)

        # Empty File
        actual = "\nNo logs."
        self.assertEqual(most_active_hour_by_app_and_log_type([]), actual)

    # Req 9 Test
    def test_calculate_failure_rate(self):
        # Test File
        actual = "\nFailure Rate Percentage by App Type:"
        actual += "\nApp=API, Failure Rate=25.00%"
        actual += "\nApp=BackendApp, Failure Rate=16.67%"
        actual += "\nApp=FrontendApp, Failure Rate=0.00%"
        actual += "\nApp=SYSTEM, Failure Rate=0.00%"
        self.assertEqual(calculate_failure_rate(self.log_entries), actual)

        # Empty File
        actual = "\nNo logs."
        self.assertEqual(calculate_failure_rate([]), actual)


if __name__ == '__main__':
    unittest.main()