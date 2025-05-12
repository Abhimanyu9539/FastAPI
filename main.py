from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated,Literal

class Patient(BaseModel):
    id: Annotated[str, Field(...,description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(...,description="The name of the patient")]
    city: Annotated[str, Field(...,description="The city of the patient")]
    age: Annotated[int, Field(...,ge=0,le=120,description="The age of the patient")]
    gender: Annotated[Literal["male","female","other"], Field(...,description="The gender of the patient")]
    height: Annotated[float, Field(...,ge=0,description="The height of the patient in Meters")]
    weight: Annotated[float, Field(...,ge=0,description="The weight of the patient in Kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def bmi_category(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 24.9:
            return "Normal weight"
        elif self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"


app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)

    return data

def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file, indent=4)


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


@app.post('/add_patient')
def add_patient(patient: Patient):

    #load all the patients
    data = load_data()

    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    #add the patient to the database
    data[patient.id] = patient.model_dump(exclude=["id"])
    
    #save the updated database
    save_data(data)

    return JSONResponse(content={"message": "Patient added successfully"}, status_code=201)