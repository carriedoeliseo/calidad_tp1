from tp_limpieza import data0
import pandas as pd
from inline_sql import sql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

consulta = """
                SELECT d.Incidente , d.FATAL AS Fatal, COUNT(*) AS cantidad_incidentes 
                FROM data0 AS d 
                GROUP BY d.Incidente,d.FATAL 
            """
cantidad_incidentes_tipo_faltal = sql^consulta

cantidad_incidentes_tipo = cantidad_incidentes_tipo_faltal.groupby('Incidente')['cantidad_incidentes'].sum()

 

cantidad_incidentes_tipo = cantidad_incidentes_tipo.sort_values()[::-1]
colores = sns.color_palette("mako", cantidad_incidentes_tipo.shape[0])
fig, ax = plt.subplots()
ax.bar(x= cantidad_incidentes_tipo.index ,width = 0.7, height=cantidad_incidentes_tipo,color = colores)
ax.set_xlabel('Tipos de ataque')
ax.set_ylabel('Cantidad de ataques')
ax.set_title('cantidad de ataques de cada tipo', size=10)
ax.set_yticks([100,1000,3000,2000,4000,5000])
ax.set_xticklabels(ax.set_xticklabels(cantidad_incidentes_tipo.index, rotation=45))
plt.show()








# Asumimos que cantidad_incidentes_tipo_fatal es tu DataFrame

# Filtrar y agrupar los datos, asegurando que estén ordenados
fatal_incidents = cantidad_incidentes_tipo_faltal[cantidad_incidentes_tipo_faltal['Fatal'] == 'VERDADERO'].sort_values(by=['Incidente'])
total_incidents = cantidad_incidentes_tipo_faltal.groupby('Incidente')['cantidad_incidentes'].sum().sort_index().reset_index()

# Combinar DataFrame de incidentes fatales con los totales
df_combinado = pd.merge(fatal_incidents, total_incidents, on='Incidente', suffixes=('_fatal', '_total'))
df_combinado['Porcentaje'] = (df_combinado['cantidad_incidentes_fatal'] / df_combinado['cantidad_incidentes_total']) * 100
df_combinado['Porcentaje_str'] = df_combinado['Porcentaje'].round(2).astype(str) + '%'

# Ordenar por total de incidentes
df_combinado = df_combinado.sort_values(by='cantidad_incidentes_total', ascending=False)

# Crear gráfico de barras
fig, ax = plt.subplots(figsize=(6, 8))
ax.bar(df_combinado['Incidente'], df_combinado['cantidad_incidentes_total'], width=0.7, label='Total', alpha=0.7, color='#FFB6C1')
barfatal = ax.bar(df_combinado['Incidente'], df_combinado['cantidad_incidentes_fatal'], width=0.7, alpha=0.7, label='Fatal', color='#C8A2D6')
ax.bar_label(barfatal, df_combinado['Porcentaje_str'], size=9)

# Etiquetas y configuración del gráfico
ax.set_xticklabels(df_combinado['Incidente'], rotation=45)
ax.set_xlabel('Tipo de caso')
ax.set_ylabel('Cantidad de casos')
ax.legend(loc='upper right')
ax.grid()

# Mostrar gráfico
plt.tight_layout()
plt.show()

#%%

consulta = """
                SELECT d.Incidente ,d.Pais,d.Color, COUNT(*) AS cantidad_incidentes 
                FROM data0 AS d 
                GROUP BY d.Incidente, d.Pais , d.Color
                HAVING d.Pais = 'United States of America' or d.Pais = 'Australia' or d.Pais = 'South Africa'
                ORDER BY cantidad_incidentes DESC, d.Pais , Incidente 
            """
cantidad_incidentes_tipo_faltal_pais = sql^consulta


us = cantidad_incidentes_tipo_faltal_pais[cantidad_incidentes_tipo_faltal_pais['Pais'] == 'United States of America']
au = cantidad_incidentes_tipo_faltal_pais[cantidad_incidentes_tipo_faltal_pais['Pais'] == 'Australia']
sf = cantidad_incidentes_tipo_faltal_pais[cantidad_incidentes_tipo_faltal_pais['Pais'] == 'South Africa']




