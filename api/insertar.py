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

            # Conexión usando pymssql
            conn = pymssql.connect(**config)
            cursor = conn.cursor()
            
            # Inserción en tu tabla real
            query_sql = "INSERT INTO dbo.measurements_receipt (fecha_hora, dispositivo_id, valor) VALUES (GETDATE(), %s, %s)"
            cursor.execute(query_sql, (id_disp, temp))
            
            conn.commit()
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("EXITO_SQL".encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
