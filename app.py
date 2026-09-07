import redis
from http.server import HTTPServer, BaseHTTPRequestHandler

# Menghubungkan ke container Redis
cache = redis.Redis(host='redis-server', port=6379)

class HaloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Menambah dan mengambil angka dari Redis
            hits = cache.incr('hits')
            pesan = f"Halo! Aplikasi terhubung ke Redis. Anda pengunjung ke-{hits}."
        except redis.exceptions.ConnectionError:
            pesan = "Halo! (Gagal terhubung ke Redis, container mungkin mati)"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Mengirim respon ke browser/curl
        self.wfile.write(pesan.encode('utf-8'))

server = HTTPServer(('0.0.0.0', 8080), HaloHandler)
print("Server berjalan di port 8080...")
server.serve_forever()
