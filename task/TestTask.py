import types
import unittest
import io


class TestTask:
    def __init__(self, teststr, testid):
        self.module = types.ModuleType('test')
        exec(teststr, self.module.__dict__)

        self.test_suite = unittest.TestLoader().loadTestsFromModule(self.module)

        self.testid = testid

        self.test_result = io.StringIO()

    def run(self):
        unittest.TextTestRunner(verbosity=2, stream=self.test_result).run(self.test_suite)
        return self.test_result
