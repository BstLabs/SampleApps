from caios.abc.mutable_mapping import MutableMapping
from caios.protocol.secret import get_secret
import requests
from requests.auth import HTTPBasicAuth
from template import ticket_json
from jdict import jdict
import pandas as pd


class Jira:
    """Demonstrates automation of JIRA API"""

    def __init__(self, jira_test: str) -> None:
        """ JIRA service  """
        jira_secrets = get_secret("SecretsManager://jira_micro_app_creds_id")
        
        self._workbook = MutableMapping.get_mapping(jira_test)
        self._jira_username = jira_secrets['jira-username']
        self._jira_password = jira_secrets['jira-password']
        self._jira_project_url = jira_secrets['jira-project-url']
        
        
    def create_ticket(self, details: jdict) -> jdict:
        # fetch all jira users
        url = f"{self._jira_project_url}/rest/api/3/users"
        response = requests.get(url=url, verify=False, auth=HTTPBasicAuth(self._jira_username, self._jira_password))
        users = response.json()

        # create a mapping for assignee name and account_id, store in dictionary
        user_lookup = dict()
        for user in users:
            account_id = user['accountId']
            display_name = user['displayName'].lower()
            user_lookup[display_name] = account_id
        
        # call jira API and pass values to create ticket in jira account                
        url = f"{self._jira_project_url}/rest/api/3/issue"
        list_of_dicts = self._workbook['input'].to_dict('records')
        for item in list_of_dicts:
            title = item['Title']
            description  = item['Description']
            assignee = item['Assignee']
            priority = item['Priority']
            labels = item['Labels']
            
            # keep default values for account id, lables and priority unless updated
            account_id = None
            if assignee and assignee.lower() in user_lookup:
                account_id = user_lookup[assignee.lower()]
            
            _labels = []
            if labels and len(labels.strip()) > 0:
                _labels = labels.strip().split(",")
            
            if priority == None or priority == '':
                priority = 'Medium'
            
            
            # make request to jira API
            request_body = ticket_json(title, description, account_id, _labels, priority)
            print(request_body)
            response = requests.post(url=url, json=request_body, verify=False, auth=HTTPBasicAuth(self._jira_username, self._jira_password))

        # clear the input sheet
        self._workbook['input']=pd.DataFrame([{'Title': None, 'Description': None, 'Assignee': None, 'Priority': None, 'Labels':None}])
        return {"message": f"{len(list_of_dicts)} tickets created successfully"}

    
    def get_tickets(self):
        # default filter values
        assignee_filter = None
        priority_filter = None
        status_filter = None
        
        # get filter values from controller sheet, if provided
        controller_rows = self._workbook['controller'].to_dict('records')
        if len(controller_rows) > 0:
            filters = controller_rows[0]
            assignee_filter = filters['Assignee']
            priority_filter = filters['Priority']
            status_filter = filters['Status']
        
        # make request to jira get issues API
        url = f"{self._jira_project_url}/rest/api/3/search"
        response = requests.get(url=url, verify=False, auth=HTTPBasicAuth(self._jira_username, self._jira_password))
        data = response.json()
        
        # convert data to list of dict format
        response_list = []
        for issue in data['issues']:
            if 'fields' in issue:
                print('issue : ', issue)
                title = issue['fields']['summary']
                description = issue['fields']["description"]["content"][0]["content"][0]["text"] if issue['fields']["description"] else None
                status = issue['fields']["status"]["name"]
                labels = ', '.join(issue['fields']['labels'])
                
                
                assignee = ''
                if issue['fields']['assignee']:
                    assignee = issue['fields']['assignee']['displayName']
                
                priority = ''
                if issue['fields']['priority']:
                    priority = issue['fields']['priority']['name']
    
                
                response_list.append(dict(Title=title, Description=description, Status=status, Assignee=assignee, Priority=priority, Labels=labels))
        
        # filter data, if specified
        if assignee_filter:
            response_list = [item for item in response_list if item['Assignee'] == assignee_filter]
        
        if priority_filter:
            response_list = [item for item in response_list if item['Priority'] == priority_filter]

        if status_filter:
            response_list = [item for item in response_list if item['Status'] == status_filter]
        
        # write data to output sheet
        self._workbook['output']=pd.DataFrame(response_list)
        return jdict(response=response_list)