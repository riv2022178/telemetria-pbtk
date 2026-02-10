from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import pymssql

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Datos de tu servidor
        config = {
            'server': '35.170.142.239',
            'user': 'USRCUBOS1',
            'password': 'C0nsult4$%',
            'database': 'INM_TELEMETRIA'
        }
        
        try:
            query = parse_qs(urlparse(self.path).query)
            temp = query.get('temperatura', [0])[0]
            id_disp = query.get('id', ['Termocupla_1'])[0]
            # NUEVO: Capturar el valor de humedad enviado como 'valor_1'
            humedad = query.get('valor_1', [None])[0] 

            # Conexión usando pymssql
            conn = pymssql.connect(**config)
            cursor = conn.cursor()
            
            # MODIFICADO: Ahora insertamos también en la columna valor_1
            query_sql = "INSERT INTO dbo.measurements_receipt (fecha_hora, dispositivo_id, valor, valor_1) VALUES (GETDATE(), %s, %s, %s)"
            cursor.execute(query_sql, (id_disp, temp, humedad))
            
            conn.commit()
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("EXITO_SQL_CON_HUMEDAD".encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
