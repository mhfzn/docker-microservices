import redis
from http.server import HTTPServer, BaseHTTPRequestHandler
from prometheus_client import start_http_server, Counter

# Membuat sensor penghitung (counter) untuk metrik Prometheus
REQUEST_COUNT = Counter('app_requests_total', 'Total permintaan ke aplikasi web Python')

cache = redis.Redis(host='redis-server', port=6379)

class HaloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Menaikkan angka sensor setiap kali ada orang yang mengakses web
        REQUEST_COUNT.inc()
        
        try:
            hits = cache.incr('hits')
            pesan = f'🚀 Halo dari K3s CI/CD Pipeline! Anda pengunjung ke-{hits}.\n'
        except redis.exceptions.ConnectionError:
            pesan = "Halo! (Gagal terhubung ke Redis)"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(pesan.encode('utf-8'))

if __name__ == '__main__':
    # Membuka port 8000 khusus agar bisa disedot oleh Prometheus
    start_http_server(8000)
    
    server = HTTPServer(('0.0.0.0', 8080), HaloHandler)
    print("Server web di port 8080. Metrik Prometheus di port 8000...")
    server.serve_forever()

