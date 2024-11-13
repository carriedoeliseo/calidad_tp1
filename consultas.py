^^from tp_limpieza import data0
import pandas as pd
from inline_sql import sql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#%%

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
                SELECT d.Pais, d.Incidente ,d.Color, COUNT(*) AS cantidad_incidentes 
                FROM data0 AS d 
                GROUP BY d.Incidente, d.Pais , d.Color
                ORDER BY cantidad_incidentes DESC, d.Pais , Incidente 
            """
            
cantidad_incidentes_pais = sql^consulta

incidentes_us_sa_au = sql^ """
                            SELECT *
                            FROM cantidad_incidentes_tipo_faltal_pais
                            WHERE (Pais = 'United States of America') OR
                                  (Pais = 'Australia') OR
                                  (Pais = 'South Africa')
                           """

data = incidentes_us_sa_au.pivot(index='Pais', columns='Incidente', values='cantidad_incidentes')

# Pivoteo
cantidad_incidentes_pais = cantidad_incidentes_pais.pivot(index='Pais', columns='Incidente', values='cantidad_incidentes')
cantidad_incidentes_pais.fillna(0, inplace=True)
cantidad_incidentes_pais.reset_index(inplace=True)

# Dropeo paises nulos
cantidad_incidentes_pais.dropna(inplace=True)

# Agarro continentes y raros
cantidad_incidentes_pais_aparte = cantidad_incidentes_pais[(cantidad_incidentes_pais['Pais'] == 'AFRICA') |
                                                           (cantidad_incidentes_pais['Pais'] == 'ASIA') | 
                                                           (cantidad_incidentes_pais['Pais'] == 'INTERNATIONAL SEAS') |
                                                           (cantidad_incidentes_pais['Pais'] == 'DIVIDED TERRITORY') ]
cantidad_incidentes_pais_aparte.to_excel('./no_paises.xlsx')

# Agarro NO RAROS
cantidad_incidentes_pais.drop(cantidad_incidentes_pais_aparte.index, inplace=True)
cantidad_incidentes_pais.to_excel('./paises.xlsx')

data.reset_index(inplace=True)
data = data[['Pais', 'Unprovoked', 'Provoked', 'Questionable', 'Boat', 'Sea Disaster']]

fig, ax = plt.subplots()

colors = ['#eddab5', '#ffcc99', '#99ccff', '#cfeecc', '#ffffc5'] 
data.plot(x='Pais', 
          y=['Unprovoked', 'Provoked', 'Questionable', 'Boat', 'Sea Disaster'], 
          kind='bar',
          label=['Unprovoked', 'Provoked', 'Questionable', 'Boat', 'Sea Disaster'],
          color=colors,
          ax=ax,)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, size=8)
ax.set_ylabel('Cantidad de casos')


#%%

consulta = """ 
              SELECT Incidente , Color , SUM(cantidad_incidentes) as cantidad_incidentes
              FROM cantidad_incidentes_pais 
              Group by Incidente, Color
              """
Porcentaje_df = sql^ consulta

total_general = Porcentaje_df['cantidad_incidentes'].sum()

# Calcular el porcentaje de cada tipo
Porcentaje_df['Porcentaje'] = (Porcentaje_df['cantidad_incidentes'] / total_general) * 100


 


fig, ax = plt.subplots(figsize=(8, 8))  


ax.pie(Porcentaje_df['Porcentaje'], 
       labels=Porcentaje_df['Incidente'], 
       autopct='%1.1f%%',  
       colors=Porcentaje_df['Color'],  e
       startangle=90,  # Alineación desde arriba
       wedgeprops={'edgecolor': 'black', 'linewidth': 1}) 


for label in ax.labels:
    label.set_fontsize(14) 


for percentage in ax.texts: 
    percentage.set_fontsize(16)  


ax.set_title('Porcentaje de Incidentes de Tiburón por Tipo', fontsize=18, fontweight='bold')


plt.tight_layout() 
plt.show()


