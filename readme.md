
# Setup

1. Navigate to the Sublime Packages directory on your machine
```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
```

2. Clone this repository into it
```
git clone https://github.com/tonyennis145/chunks-sublime.git Chunks
```

3. Set your authentication credentials
    - Every open directory in Sublime is seen as a `project`. In order to apply project specific settings, you need to save the existing open project: 
    `Project -> Save Project As`
    - I would recommend saving the project file in the directory you would like the settings to apply to.
    - Once the `.sublime-project` file is saved, open it and add your settings
    ```
    {
        "folders":
        [
            {
                "path": "/Users/you/yourpath"
            }
        ],
        "settings":
        {
            "chunks_authentication_token": "",
            "chunks_project_id": "",
        }
    }
    ```