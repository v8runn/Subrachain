**Subrachain**

- A blockchain-based cryptocurrency.

**Activate the virtual environment**

```
source blockchain-env/Scripts/activate
```

**Install all packages**


**Run the tests**
Activate virtual environment.
```
python -m pytest backend/tests
```

***Run the application and API**
Activate the virtual environment.

```
python -m backend.app
```

**Run a peer instance**
Activate the virtual environment.
```
export PEER=True && python -m backend.app
```

**Run frontend**
```
npm start
```

**Provide dummy data for frontend**
Activate the virtual environment
```
export SEED_DATA=True && python -m backend.app
```