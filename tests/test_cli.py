import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from randline_cli.cli import main


class TestCli(unittest.TestCase):
    def test_picks_requested_number_of_lines_from_file(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "lines.txt"
            path.write_text("a\nb\nc\nd\ne\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(path), "-n", "3", "--seed", "1"])
            self.assertEqual(code, 0)
            lines = out.getvalue().splitlines()
            self.assertEqual(len(lines), 3)
            self.assertTrue(set(lines).issubset({"a", "b", "c", "d", "e"}))

    def test_seed_reproducible_across_runs(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "lines.txt"
            path.write_text("\n".join(str(i) for i in range(100)) + "\n")

            out1 = io.StringIO()
            with redirect_stdout(out1):
                main([str(path), "-n", "5", "--seed", "42"])

            out2 = io.StringIO()
            with redirect_stdout(out2):
                main([str(path), "-n", "5", "--seed", "42"])

            self.assertEqual(out1.getvalue(), out2.getvalue())

    def test_reads_from_stdin_by_default(self) -> None:
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO("x\ny\nz\n")):
            with redirect_stdout(out):
                code = main(["-n", "2", "--seed", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(len(out.getvalue().splitlines()), 2)

    def test_negative_number_errors(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["-n", "-1"])
        self.assertEqual(code, 2)
        self.assertIn("non-negative", err.getvalue())

    def test_missing_file_errors(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["/no/such/file.txt", "-n", "1"])
        self.assertEqual(code, 2)
        self.assertIn("error", err.getvalue())

    def test_zero_prints_nothing(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "lines.txt"
            path.write_text("a\nb\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(path), "-n", "0"])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "")

    def test_n_larger_than_file_returns_all_lines(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "lines.txt"
            path.write_text("a\nb\nc\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(path), "-n", "50"])
            self.assertEqual(code, 0)
            self.assertEqual(sorted(out.getvalue().splitlines()), ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
