from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)

    return data

@app.get("/")
def hello():
    return{'message': "Patients Management System"}

@app.get("/about")
def about():
    return{"message":"FastAPI server for Patient Management System"}


@app.get("/view")
def view():
    data = load_data()
    return data