# Project scrapi

## Start
...
## <span style='color:red'>Installing</span>

### <span style='color:yellow'>Instal Deps</span>
```bash
# install pipenv
pip install pipenv

# activate virtual env
pipenv shell

# install deps
pipenv sync --dev
```

### Additional

```bash
# regenerate Pipfile.lock file
pipenv lock

# pipenv lock & pipenv sync
pipenv update
```
\
## Usage code quality tools
The pre-commit hook will be automatically run

You can use the code quality checkers on GitHub CI

\
## <span style='color:red'>Run application</span>
```bash
# copy the default environment file to create your own configuration file
cp .env.default .env,

# extract dates for source and save to json
python src/product_parser/run.py

# run django server
python src/manage.py runserver
```
### Endpoints

```bash
# return all information about all products
get: http://localhost:8000/all_products/ 

# return information about exact product
get: http://localhost:8000/products/{product_name} 

# return information about exact field exact product
get: http://localhost:8000/products/{product_name}/{product_field}  

```
