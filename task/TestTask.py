import types
import unittest
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestTask:
    def __init__(self, teststr, testid):
        self.module = types.ModuleType('test')

        chopts = Options()
        chopts.add_argument('--headless')
        self.module.driver = webdriver.Remote('http://localhost:5915', desired_capabilities=chopts.to_capabilities())
        
        exec(teststr, self.module.__dict__)

        self.test_suite = unittest.TestLoader().loadTestsFromModule(self.module)

        self.testid = testid

        self.test_result = io.StringIO()

    def run(self):
        unittest.TextTestRunner(verbosity=2, stream=self.test_result).run(self.test_suite)
        return self.test_result
