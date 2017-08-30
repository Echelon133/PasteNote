from app.unittests.models_test import ModelsUnittest
import unittest


class NotesAppSuite(unittest.TestSuite):
    pass


if __name__ == '__main__':
    result = unittest.TestResult()

    suite = NotesAppSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ModelsUnittest))

    unittest.TextTestRunner().run(suite)