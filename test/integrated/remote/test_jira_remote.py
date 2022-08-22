from caios.test import TestCase, main, test_service
import warnings


class TestJiraRemote(TestCase):
    def test_jira_remote(self):
        """ Remote test """
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        
        
if __name__ == "__main__":
    main()
