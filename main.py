from fastapi import FastAPI, HTTPException, Path, Query
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

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Field to sort by', example='name'), 
                  order: str = Query(..., description='Sort order', example='asc')):
    valid_fields = ['age', 'bmi', 'weight', 'height']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid sort field. Must be one of: {", ".join(valid_fields)}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Must be either "asc" or "desc"')
    
    data = load_data()
    sort_order = True if order == 'asc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data
