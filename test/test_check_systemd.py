import unittest
import os
import subprocess

BIN = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin'))
os.environ['PATH'] = BIN + ':' + os.environ['PATH']


class TestCheckSystemd(unittest.TestCase):

    def test_failure(self):
        process = subprocess.run(
            ['./check_systemd.py'],
            encoding='utf-8',
            stdout=subprocess.PIPE
        )
        self.assertEqual(process.returncode, 2)
        self.assertEqual(
            process.stdout,
            'SYSTEMD CRITICAL - test.service: failed\n'
        )

    def test_exclusive_group(self):
        process = subprocess.run(
            ['./check_systemd.py', '-s', 'test1.service', '-e',
             'test2.service'],
            encoding='utf-8',
            stderr=subprocess.PIPE
        )
        self.assertEqual(process.returncode, 2)
        self.assertIn(
            'error: argument -e/--exclude: not allowed with argument '
            '-s/--service',
            process.stderr,
        )

    def test_option_exclude_known_service(self):
        process = subprocess.run(
            ['./check_systemd.py', '-e', 'test.service'],
            encoding='utf-8',
            stdout=subprocess.PIPE
        )
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stdout, 'SYSTEMD OK - all\n')

    def test_option_exclude_unknown_service(self):
        process = subprocess.run(
            ['./check_systemd.py', '-e', 'testX.service'],
            encoding='utf-8',
            stdout=subprocess.PIPE
        )
        self.assertEqual(process.returncode, 2)
        self.assertEqual(
            process.stdout,
            'SYSTEMD CRITICAL - test.service: failed\n'
        )


if __name__ == '__main__':
    unittest.main()