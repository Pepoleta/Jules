import unittest
import sys
import os

def run_all_tests():
    print("="*60)
    print("Running Gemini Automator Test Suite")
    print("="*60)
    
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("Test Summary")
    print(f"Tests Run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print("="*60)
    
    if result.wasSuccessful():
        print("SUCCESS: ALL TESTS PASSED!")
        return 0
    else:
        print("FAILURE: SOME TESTS FAILED.")
        return 1

if __name__ == "__main__":
    # Ensure current directory is in path
    sys.path.append(os.getcwd())
    sys.exit(run_all_tests())
