# Optimizely Web App

This is a simplified version of something similar to one of our products.  
There are 3 reported bugs that we would like to to fix and if you have enough time, add 1 new endpoint.

There are 3 tables
```
create table account (
    id integer primary key autoincrement,
    admin_email_address text,
    account_name text
);
create table project (
    id integer primary key autoincrement,
    description text,
    account_id integer,
    archived text
);
create table switch (
    id integer primary key autoincrement,
    project_id integer,
    switch_type text,
    description text,
    archived text
);
```

Bug 1:  For the project list endpoint, the url that points to the detail list url was not included.  Please add it to the JSON response as `"url": "/project/<id>"` so the front end can render it correctly.

Bug 2:  The `/project/<id>` endpoint lists the switches that are included in a specific project, the system returns an empty response if the project_id is not found.  It should return a `404` so our frontend can display the appropriate error message.

Bug 3:  The switch list endpoint should also automatically filter out archived switches from the response.

Feature 1:  Add a new endpoint `/projectsummary/<id>` that has the same output as the project list endpoint but add a new key of `summarycount` and the content is a dictionary with the count of project switches by `switch_type`.

e.g.

```
"123": {
    "account_id": 456,
    "description": "some project",
    "id": 123,
    "url": "/project/123",
    "summarycount": {
        "flag": 10,
        "flagexp": 4,
        "exp": 1
    }
},
