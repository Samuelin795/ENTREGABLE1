import pandas as pd
data = {
    'Nombre': ['Juan','Ana','Luis','Marta'],
    'Edad': ['15','14','16','15'],
    'Nota': ['8.5','9.0','7.5','8.0'],
}
df = pd.DataFrame(data)
print(df)