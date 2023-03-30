### Simple Database App

This app is Python 3 App on [App Engine](https://cloud.google.com/appengine/) in [Google Cloud Platform](https://cloud.google.com/gcp).

In order to clone this project [first build simple "hello world" in App Engine](https://cloud.google.com/appengine/docs/standard/python3/building-app)

And then you can clone this all project.

#### Notice - When not in use keep the App Engine Project [clean up](https://cloud.google.com/appengine/docs/standard/python3/building-app/cleaning-up).


### DB
Use [Google Datastore](https://cloud.google.com/datastore).

The `variable_name` is the key of each entity and there is just one attribute `value` which is the `variable_value`.

## Requests

**SET** –```http://_your-app-id_.appspot.com/set?name={variable_name}&value={variable_value}```

Set the variable `variable_name` to the value `variable_value`, neither variable names nor values will contain
spaces. 

**Output**: Print the variable name and value after the change.

**GET** – ```http://_your-app-id_.appspot.com/get?name={variable_name}```

**Output**: Print out the value of the variable `variable_name` or “None” if the variable is not set.

**UNSET** – ```http://_your-app-id_.appspot.com/unset?name={variable_name}```

Unset the variable `variable_name`, making it just like the variable was never set.

**NUMEQUALTO** – ```http://_your-app-id_.appspot.com/numequalto?value={variable_value}```

**Output**: Print to the browser the number of variables that are currently set to `variable_value`. If no variables equal that
value, print 0.

**UNDO** – ```http://_your-app-id_.appspot.com/undo```
Undo the most recent SET/UNSET command. If more than one consecutive UNDO command is issued, the
original commands should be undone in the reverse order of their execution.

**Output**:Print the name and value of the changed variable (after the undo) if successful, or print NO COMMANDS if no commands may be undone.

**REDO** – ```http://_your-app-id_.appspot.com/redo```

Redo the most recent SET/UNSET command which was undone. If more than one consecutive REDO
command is issued, the original commands should be redone in the original order of their execution. If another
command was issued after an UNDO, the REDO command should do nothing.

**Output**: Print the name and value of the changed variable (after the redo) if successful, or print NO COMMANDS if no commands may be re-done.

**END** – ```http://_your-app-id_.appspot.com/end```

Exit the program. Your program will always receive this as its last command. You need to remove all your data
from the application (clean all the Datastore entities).

**Output**: Print CLEANED when done.