from app.unittests.test_model import ModelsUnittest
from app.unittests.test_views import ViewsUnittest
from app.functionaltests.test_cases import NoteFunctionalTest
import unittest


def load_tests(test_case):
    return unittest.defaultTestLoader.loadTestsFromTestCase(test_case)


if __name__ == '__main__':
    result = unittest.TestResult()

    suite = unittest.TestSuite()
    suite.addTests(load_tests(ModelsUnittest))
    suite.addTests(load_tests(ViewsUnittest))
    suite.addTests(load_tests(NoteFunctionalTest))

    unittest.TextTestRunner().run(suite)