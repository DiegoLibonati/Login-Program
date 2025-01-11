# Login Program

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Execute: `python -m venv venv`
4. Execute in Windows: `venv\Scripts\activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. You must execute the command: `docker-compose up --force-recreate` in the terminal
8. Use `python -m src.app` to execute program

NOTE: You have to be standing in the folder containing the: `docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

## Description

I made a python program using tkinter as user interface. Basically I made a login system in which if you don't have an account you can register. It will ask you for a username and password, use mongo db to store the information in a database and werkzeug for password encryption. It is very useful to access a program that is protected by this login, if you have an account you will be able to access the program, otherwise you will not be able to.

## Technologies used

1. Python

## Libraries used

#### Requirements.txt

```
pymongo==4.10.1
Werkzeug==3.1.3
python-dotenv==1.0.1
```

#### Requirements.test.txt

```
pytest
pytest-env
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Login-Program`](https://www.diegolibonati.com.ar/#/project/Login-Program)

## Video

https://user-images.githubusercontent.com/99032604/199149396-0e2f1703-c84e-4278-ac90-e806f0aba018.mp4

## Testing

1. Join to the correct path of the clone
2. Execute in Windows: `venv\Scripts\activate`
3. Execute: `pytest --log-cli-level=INFO`