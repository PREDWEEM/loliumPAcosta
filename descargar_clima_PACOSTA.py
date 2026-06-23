
import pandas as pd
import requests

# Coordenadas de pablo acosta, provincia de Buenos Aires
lat = -37.132
lon = -59.789

# Rango de fechas de tu archivo original
start_date = "2026-01-01"
end_date = "2026-06-20"

# URL de la API de Open-Meteo para datos históricos diarios
url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FSao_Paulo"

print("Obteniendo datos meteorológicos para Azul...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    daily = data['daily']
    
    # Construcción del DataFrame con las columnas idénticas a tu archivo
    df_PACOSTA = pd.DataFrame({
        'Fecha': daily['time'],
        'TMAX': daily['temperature_2m_max'],
        'TMIN': daily['temperature_2m_min'],
        'Prec': daily['precipitation_sum']
    })
    
    # Rellenar posibles datos nulos (si la API tiene algún bache reciente) con 0 para lluvia o interpolando temperaturas
    df_PACOSTA['Prec'] = df_PACOSTA['Prec'].fillna(0)
    df_PACOSTA['TMAX'] = df_PACOSTA['TMAX'].interpolate()
    df_PACOSTA['TMIN'] = df_PACOSTA['TMIN'].interpolate()
    
    # Exportar el archivo final
    nombre_archivo = 'meteo_daily_PACOSTA_real.csv'
    df_PACOSTA.to_csv(nombre_archivo, index=False)
    
    print(f"¡Archivo '{nombre_archivo}' generado con éxito!")
    print(df_PACOSTA.head())
else:
    print(f"Error al consultar la API. Código de estado: {response.status_code}")
