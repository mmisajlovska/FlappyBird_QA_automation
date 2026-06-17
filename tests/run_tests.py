import unittest
import HtmlTestRunner
import os
import sys

# Add the project root to the python path so imports work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

if __name__ == '__main__':
    # Discover tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir=os.path.join(project_root, 'tests'), pattern='test_*.py')
    
    # Reports directory
    report_dir = os.path.join(project_root, 'reports')
    os.makedirs(report_dir, exist_ok=True)
    
    print("Running QA Automation Test Suite...")
    print("Logs will be saved to tests/test_run.log")
    print(f"HTML Report will be generated in {report_dir}")
    
    # Run tests with HTMLTestRunner
    runner = HtmlTestRunner.HTMLTestRunner(
        output=report_dir,
        report_title='Flappy Bird QA Automation Report',
        report_name='Test_Run_Results',
        combine_reports=True,
        add_timestamp=True
    )
    
    runner.run(test_suite)
