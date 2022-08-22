from caios.test import TestCase, main, project_name
import os
from service import Jira


class TestJiraLocal(TestCase):
    def test_jira_local(self):
        """ Local system test """
        srv = Jira(f'{os.environ["CAIOS_USER_STORAGE"]}/{project_name}/data')
        # resp = srv._greetings(name="John")
        resp = srv.get_tickets()
        print(resp)


if __name__ == "__main__":
    main()
