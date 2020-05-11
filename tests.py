import unittest
import programm


class tests(unittest.TestCase):

    def test_calculate_period(self):
        self.assertEqual(programm.calculate_period(1000, 20, None, 500), 3)

    def test_calculate_period_not_enough_payment_size(self):
        self.assertEqual(programm.calculate_period(1000, 20, 50, 10), 50)

    def test_calculate_period_whith_zero_period(self):
        self.assertEqual(programm.calculate_period(1000, 20, None, 10), None)

    def test_get_month_graph_first(self):
        self.assertEqual(programm.get_month_graph(1000, 20, None, 500)[0], [0, 1, 2])

    def test_get_month_graph_second(self):
        self.assertEqual(programm.get_month_graph(1000, 20, None, 500)[1], [17.0, 11.0, 6.0])

    def test_get_month_graph_third(self):
        self.assertEqual(programm.get_month_graph(1000, 20, None, 500)[2], [328.0, 334.0, 339.0])

    def test_get_overpayment_graph_first_type(self):
        self.assertEqual(type(programm.get_overpayment_graph(1000, 20)[0]), list)

    def test_get_overpayment_graph_second_type(self):
        self.assertEqual(type(programm.get_overpayment_graph(1000, 20)[1]), list)

    def test_get_overpayment_graph_first_size(self):
        self.assertEqual(len(programm.get_overpayment_graph(1000, 20)[0]), 179)

    def test_get_overpayment_graph_second_size(self):
        self.assertEqual(len(programm.get_overpayment_graph(1000, 20)[1]), 179)


if __name__ == "__main__":
    unittest.main()
