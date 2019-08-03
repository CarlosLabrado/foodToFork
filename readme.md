# Food2Fork Assignment

#### Communicates to the food2fork.com API and returns recipes.


### Dependencies
Needs python 3.6
* [requests](https://2.python-requests.org/en/master/) python Requests
* [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) handles the unversioned YAML file with the credentials

Also needs a `credentials.yaml` file in the root of the directory with your API key, formatted like this:
```yaml
api_key: '<YOUR API KEY>'
```

### Build with
```docker
pip3 install \
requests \ 
PyYAML \
```

### How to use

Pass space separated, coma separated or dot separated ingredients with --i example:
```bash
python3 main.py --i 'onion tomato'
```
Optionally you can pass your API Key as an argument with --c

## Food2Fork API
https://www.food2fork.com/about/api
