from pydantic import BaseModel
from typing import Union
class DataModelPredict(BaseModel):

# Estas varibles permiten que la librería pydantic haga el parseo entre el Json recibido y el modelo declarado.
    serial_no: Union[float,str]
    gre_score: Union[float,str]
    toefl_score: Union[float,str]
    university_rating: Union[float,str]
    sop: Union[float,str]
    lor: Union[float,str] 
    cgpa: Union[float,str]
    research:  Union[float,str]

    
#Esta función retorna los nombres de las columnas correspondientes con el modelo exportado en joblib.
    def columns(self):
        return ["Serial No.","GRE Score","TOEFL Score","University Rating","SOP","LOR " ,"CGPA","Research"]
