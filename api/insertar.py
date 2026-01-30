from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import pyodbc

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Datos de tu servidor remoto
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=35.170.142.239;"
            "DATABASE=INM_TELEMETRIA;"
            "UID=USRCUBOS1;"
            "PWD=C0nsult4$%"
        )
        
        try:
            # Extraer temperatura e ID de la URL enviada por la ESP32
            query = parse_qs(urlparse(self.path).query)
            temp = query.get('temperatura', [0])[0]
            id_disp = query.get('id', ['Termocupla_1'])[0]

            # Conexión e inserción en SQL Server
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dbo.measurements_receipt (fecha_hora, dispositivo_id, valor) VALUES (GETDATE(), ?, ?)", (id_disp, temp))
            conn.commit()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("EXITO_SQL".encode())
            conn.close()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
