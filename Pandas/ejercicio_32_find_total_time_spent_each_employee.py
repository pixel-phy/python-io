"""Find Total Time Spent by Each Emplyee

+-------------+------+
| Column Name | Type |
+-------------+------+
| emp_id      | int  |
| event_day   | date |
| in_time     | int  |
| out_time    | int  |
+-------------+------+
(emp_id, event_day, in_time) is the primary key (combinations of columns with unique values) of this table.
The table shows the employees' entries and exits in an office.
event_day is the day at which this event happened, in_time is the minute at which the employee entered the office, and out_time is the minute at which they left the office.
in_time and out_time are between 1 and 1440.
It is guaranteed that no two events on the same day intersect in time, and in_time < out_time.
 

Write a solution to calculate the total time in minutes spent by each employee on each day at the office. Note that within one day, an employee can enter and leave more than once. The time spent in the office for a single entry is out_time - in_time.

Return the result table in any order.

"""

import pandas as pd

def total_time(employees: pd.DataFrame) -> pd.DataFrame:
    # 1. Calculamos el tiempo gastado en cada fila individual
    employees['total_time'] = employees['out_time'] - employees['in_time']
    
    # 2. Agrupamos por día y empleado, y sumamos el tiempo total
    result = employees.groupby(['event_day', 'emp_id'])['total_time'].sum().reset_index()
    
    # 3. Renombramos la columna 'event_day' a 'day'
    result = result.rename(columns={'event_day': 'day'})
    
    return result

datos_prueba = {
    'emp_id': [1, 1, 1, 2, 2],
    'event_day': ['2020-11-28', '2020-11-28', '2020-12-03', '2020-11-28', '2020-12-09'],
    'in_time': [4, 55, 1, 3, 47],
    'out_time': [32, 200, 42, 33, 74]
}

df_empleados = pd.DataFrame(datos_prueba)

# Convertimos la columna a tipo fecha para que coincida con el enunciado
df_empleados['event_day'] = pd.to_datetime(df_empleados['event_day']).dt.date

print("--- DATOS DE ENTRADA ---")
print(df_empleados)

# Ejecutamos la función
df_resultado = total_time(df_empleados)

print("\n--- RESULTADO FINAL ---")
print(df_resultado)
