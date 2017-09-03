from app.unittests.test_model import ModelsUnittest
from app.unittests.test_views import ViewsUnittest
from app.functionaltests.test_cases import NoteFunctionalTest
import unittest


class NotesAppSuite(unittest.TestSuite):
    pass


if __name__ == '__main__':
    result = unittest.TestResult()

    suite = NotesAppSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelsUnittest))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ViewsUnittest))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(NoteFunctionalTest))

    unittest.TextTestRunner().run(suite)