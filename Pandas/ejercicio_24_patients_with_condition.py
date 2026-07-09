"""Patients with a Condition

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| patient_id   | int     |
| patient_name | varchar |
| conditions   | varchar |
+--------------+---------+
patient_id is the primary key (column with unique values) for this table.
'conditions' contains 0 or more code separated by spaces. 
This table contains information of the patients in the hospital.
 

Write a solution to find the patient_id, patient_name, and conditions of the patients who have Type I Diabetes. Type I Diabetes always starts with DIAB1 prefix.

Return the result table in any order.

"""

import pandas as pd

def find_patients(patients: pd.DataFrame) -> pd.DataFrame:

    regex_diabetes = r'(^|\s)DIAB1'
    resultado = patients[patients['conditions'].str.contains(regex_diabetes, na=False)]
    return resultado

# --- 1. Crear datos de prueba ---
data_patients = {
    'patient_id': [1, 2, 3, 4, 5],
    'patient_name': ['Daniel', 'Alice', 'Bob', 'George', 'Alain'],
    'conditions': [
        'YFEVER DIAB100',  # Válido (Segunda palabra empieza con DIAB1)
        'SNORE',           # Inválido
        'DIAB100 MYOP',    # Válido (Primera palabra empieza con DIAB1)
        'ACEDIAB100',      # Inválido (DIAB1 no es prefijo, está en medio)
        'DIAB201'          # Inválido (Es Diabetes Tipo II)
    ]
}
df_patients = pd.DataFrame(data_patients)

# --- 2. Ejecutar la función ---
resultado = find_patients(df_patients)

# --- 3. Mostrar el resultado ---
print("--- RESULTADO DE PACIENTES CON DIABETES TIPO I ---")
print(resultado)

