# zookeeper-values-handler

this script upsert and delete by json schema:


```commandline
python main_script.py --update --env <environment> --pathfile data/sample.json --znode /path/to/znode
```

## Usage
Arguments
The script accepts the following command-line arguments:

- --update: Triggers the update process, updating the specified ZNode with data from the provided JSON file.
- --backup: Initiates a backup of the ZNode data.
- --env: Required. Specifies the environment as a string.
- --pathfile: Required. Path to the JSON file containing the ZNode data.
- --znode: Required. Path of the root ZNode to process.

it supports, those format of json:

```
{
  "predev": {
    "name": "dan",
    "age": "22"
  },
  "test": {
    "name": "jon",
    "age": "32",
    "student": {
      "color": "red"
    }
  }
```
or 
```
{
  "person": {
    "default_Value": 43,
    "predev": 45554,
    "prod": 58
  },
  "we": {
    "default_Value": 22,
    "predev": 1,
    "prod": 74
  }
}
```