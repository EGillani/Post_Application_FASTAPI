
## Requirements

Python 3.6+
Postgres/PgAdmin (For Database)
Docker for Desktop (Optional)

FastAPI stands on the shoulders of giants:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> for the web parts.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> for the data parts.

## Installation

Create a virtual environment.
<div class="termy">

```console
$ py -3 -m venv your_env_name 

```
</div>

Invoke the virtual environment. 
<div class="termy">

```console
$ your_env_name\Scripts\activate.bat

```
</div>

Download all packages found in the requirements.txt file 
<div class="termy">

```console
$ pip install -r requirements.txt

```
</div>

### Run it

Run the server with:

<div class="termy">

```console
$ uvicorn app.main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
</div>

<details markdown="1">
<summary>About the command <code>uvicorn main:app --reload</code>...</summary>

The command `uvicorn app.main:app` refers to:

* `main`: the file `main.py` (the Python "module") inside the directory `app`.
* `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
* `--reload`: make the server restart after code changes. Only do this for development.

</details>

### Check it

Open your browser at <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

You will see the JSON response as:

```JSON
{"message": "Welcome to my post application"}
```

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

### Alternative API docs

And now, go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):