from app.unittests.test_model import ModelsUnittest
from app.unittests.test_views import ViewsUnittest
import unittest


class NotesAppSuite(unittest.TestSuite):
    pass


if __name__ == '__main__':
    result = unittest.TestResult()

    suite = NotesAppSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelsUnittest))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ViewsUnittest))

    unittest.TextTestRunner().run(suite)