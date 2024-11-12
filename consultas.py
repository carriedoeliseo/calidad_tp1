from tp_limpieza import data0
import pandas as pd
from inline_sql import sql


consulta = """
                SELECT d.Incidente , d.FATAL AS Fatal, COUNT(*) AS cantidad_incidentes 
                FROM data0 AS d 
                GROUP BY d.Incidente,d.FATAL 
            """
cantidad_incidentes_tipo = sql^consulta

