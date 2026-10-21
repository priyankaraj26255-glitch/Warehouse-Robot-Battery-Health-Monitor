import contextlib
import io
import unittest

import battery_monitor as bm


class TestBatteryArray(unittest.TestCase):
    def test_shape_is_six_robots(self):
        battery_array = bm.make_battery_array(bm.BATTERY_LEVELS)
        self.assertEqual(battery_array.shape, (6,))

    def test_dtype_is_integer(self):
        battery_array = bm.make_battery_array(bm.BATTERY_LEVELS)
        self.assertEqual(battery_array.dtype.kind, 'i')


class TestBatterySeries(unittest.TestCase):
    def setUp(self):
        self.series = bm.make_battery_series(bm.BATTERY_LEVELS, bm.ROBOT_IDS)

    def test_index_is_robot_ids(self):
        self.assertEqual(list(self.series.index), ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'])

    def test_values_keep_their_order(self):
        self.assertEqual(list(self.series), [85, 42, 67, 19, 90, 55])

    def test_battery_of_r4(self):
        self.assertEqual(bm.battery_of(self.series, 'R4'), 19)

    def test_unknown_robot_raises_key_error(self):
        with self.assertRaises(KeyError):
            bm.battery_of(self.series, 'R9')

    def test_low_battery_keeps_only_r2_and_r4(self):
        low = bm.low_battery(self.series)
        self.assertEqual(list(low.index), ['R2', 'R4'])
        self.assertEqual(list(low), [42, 19])

    def test_exactly_fifty_is_not_low(self):
        series = bm.make_battery_series([50, 49], ['A', 'B'])
        self.assertEqual(list(bm.low_battery(series).index), ['B'])


class TestTopUp(unittest.TestCase):
    def test_adds_five_to_every_level(self):
        battery_array = bm.make_battery_array(bm.BATTERY_LEVELS)
        self.assertEqual(list(bm.top_up(battery_array)), [90, 47, 72, 24, 95, 60])

    def test_original_array_is_unchanged(self):
        battery_array = bm.make_battery_array(bm.BATTERY_LEVELS)
        bm.top_up(battery_array)
        self.assertEqual(list(battery_array), [85, 42, 67, 19, 90, 55])


class TestMainOutput(unittest.TestCase):
    def test_main_prints_every_part(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            bm.main()
        output = buffer.getvalue()
        self.assertIn("Shape: (6,)", output)
        self.assertIn("Battery of R4: 19", output)
        self.assertIn("After top-up: [90 47 72 24 95 60]", output)


if __name__ == "__main__":
    unittest.main()