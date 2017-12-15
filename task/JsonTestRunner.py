import unittest
import time


class JsonTestResult(unittest.TestResult):
    def __init__(self):
        super(JsonTestResult, self).__init__()
        self.successes = []

    def addSuccess(self, test):
        super(JsonTestResult, self).addSuccess(test)
        self.successes.append(test)

    def toObject(self):
        failures = [{fail[0]._testMethodName: fail[1]} for fail in self.failures]
        errors = [{err[0]._testMethodName: err[1]} for err in self.errors]
        skips = [{skip[0]._testMethodName: skip[1]} for skip in self.skipped]
        expectedFailures = [{fail[0]._testMethodName: fail[1]} for fail in self.expectedFailures]
        unexpectedSuccesses = [{suc._testMethodName: 'U'} for suc in self.unexpectedSuccesses]
        successes = [{suc._testMethodName: 'OK'} for suc in self.successes]
        return {
            'failures': failures,
            'errors': errors,
            'skips': skips,
            'expectedFailures': expectedFailures,
            'unexpectedSuccesses': unexpectedSuccesses,
            'successes': successes
        }


class JsonTestRunner(object):
    def __init__(self, failfast=False, buffer=False, tb_locals=False):
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.output = {}

    def run(self, test):
        result = JsonTestResult()
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        run = result.testsRun

        self.output['total_run'] = run
        self.output['total_time'] = timeTaken

        expectedFails = unexpectedSuccesses = successes = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped,
                                result.successes))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped, successes = results

        failed, errored = len(result.failures), len(result.errors)

        self.output['failed'] = failed
        self.output['errored'] = errored
        self.output['skipped'] = skipped
        self.output['expectedFails'] = expectedFails
        self.output['unexpectedSuccesses'] = unexpectedSuccesses
        self.output['successes'] = successes

        if not result.wasSuccessful():
            self.output['status'] = 'FAILED'
        else:
            self.output['status'] = 'OK'

        self.output['result'] = result.toObject()

        return self.output
