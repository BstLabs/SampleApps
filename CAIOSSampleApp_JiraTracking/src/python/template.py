def ticket_json(title, desc, account_id, labels, priority):
  if account_id == None:
    return {
    "fields": {
        "project": {
    		"id": "10000"
    	},
    	"summary": title,
        "issuetype": {
                "name": "Bug"
        },
        "assignee": None,
        "priority":{
           "name": priority.capitalize()
        },
        "labels": labels,
        "description": {
          "type": "doc",
          "version": 1,
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "text": desc,
                  "type": "text"
                }
              ]
            }
          ]
      }
    }
  }
  else:
    return {
    "fields": {
        "project": {
    		"id": "10000"
    	},
    	"summary": title,
        "issuetype": {
                "name": "Bug"
        },
        "assignee": {
          "accountId": account_id
        },
        "priority":{
           "name": priority.capitalize()
        },
        "labels": labels,
        "description": {
          "type": "doc",
          "version": 1,
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "text": desc,
                  "type": "text"
                }
              ]
            }
          ]
      }
    }
  }