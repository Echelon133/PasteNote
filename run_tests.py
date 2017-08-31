from app.unittests.models_test import ModelsUnittest
from app.unittests.views_test import ViewsUnittest
import unittest


class NotesAppSuite(unittest.TestSuite):
    pass


if __name__ == '__main__':
    result = unittest.TestResult()

    suite = NotesAppSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelsUnittest))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ViewsUnittest))

    unittest.TextTestRunner().run(suite)