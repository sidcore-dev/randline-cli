import unittest

from randline_cli.core import reservoir_sample


class TestReservoirSample(unittest.TestCase):
    def test_zero_returns_empty(self) -> None:
        self.assertEqual(reservoir_sample(["a", "b", "c"], 0), [])

    def test_n_greater_than_input_returns_all_in_order(self) -> None:
        lines = ["a", "b", "c"]
        self.assertEqual(reservoir_sample(lines, 10), lines)

    def test_n_equal_to_input_returns_all_in_order(self) -> None:
        lines = ["a", "b", "c"]
        self.assertEqual(reservoir_sample(lines, 3), lines)

    def test_negative_n_raises(self) -> None:
        with self.assertRaises(ValueError):
            reservoir_sample(["a"], -1)

    def test_result_size_matches_n(self) -> None:
        lines = [str(i) for i in range(1000)]
        result = reservoir_sample(lines, 17, seed=7)
        self.assertEqual(len(result), 17)

    def test_result_is_subset_without_duplicates(self) -> None:
        lines = [str(i) for i in range(500)]
        result = reservoir_sample(lines, 50, seed=3)
        self.assertEqual(len(set(result)), 50)
        self.assertTrue(set(result).issubset(set(lines)))

    def test_seed_is_reproducible(self) -> None:
        lines = [str(i) for i in range(200)]
        first = reservoir_sample(lines, 10, seed=99)
        second = reservoir_sample(lines, 10, seed=99)
        self.assertEqual(first, second)

    def test_different_seeds_can_differ(self) -> None:
        lines = [str(i) for i in range(200)]
        first = reservoir_sample(lines, 10, seed=1)
        second = reservoir_sample(lines, 10, seed=2)
        self.assertNotEqual(first, second)

    def test_works_on_single_pass_iterator(self) -> None:
        # A generator can only be consumed once — this verifies the
        # function never re-reads the input.
        def gen():
            for i in range(100):
                yield str(i)

        result = reservoir_sample(gen(), 5, seed=5)
        self.assertEqual(len(result), 5)

    def test_empty_input_returns_empty(self) -> None:
        self.assertEqual(reservoir_sample([], 5), [])


if __name__ == "__main__":
    unittest.main()
