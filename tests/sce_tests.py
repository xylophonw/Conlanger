import unittest

from test_basic_changes import TestBasicChanges
from test_categories import TestCategories
from test_flags import TestFlags
from test_exceptions import TestExceptions


all_tests = unittest.TestSuite()
all_tests.addTest(unittest.makeSuite(TestBasicChanges))
all_tests.addTest(unittest.makeSuite(TestCategories))
all_tests.addTest(unittest.makeSuite(TestFlags))
all_tests.addTest(unittest.makeSuite(TestExceptions))

unittest.TextTestRunner(verbosity=2).run(all_tests)
