# Food2Fork Assignment

#### Communicates to the food2fork.com API and returns recipes.


### Dependencies
Needs python 3.6
* [requests](https://2.python-requests.org/en/master/) python Requests
* [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) handles the unversioned YAML file with the credentials

### Build with
```docker
pip3 install \
requests \ 
PyYAML \
```

### Setup
Can have a `credentials.yaml` file in the root of the directory with your API key, formatted like this:
```yaml
api_key: '<YOUR API KEY>'
```
Or you can pass your API Key as an argument with --c
```bash
python3 main.py --c '<YOUR API KEY>'
```

### How to use

Just run it with `python3 main.py` and wait for the input prompt to type in the list of ingredients separated by spaces,
commas or dots.

Or pass space separated, coma separated or dot separated ingredients with --i example:
```bash
python3 main.py --i 'onion tomato'
```

## Food2Fork API
https://www.food2fork.com/about/api

## Author
* Carlos Labrado