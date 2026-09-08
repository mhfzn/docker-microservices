# Gunakan OS Alpine Linux yang sangat ringan
FROM python:3.9-alpine

# Buat folder /app di dalam container
WORKDIR /app

# Menginstal library Redis untuk Python
RUN pip install redis prometheus-client

# Salin file app.py dari laptop Anda ke dalam container
COPY app.py .

# Beri tahu Docker bahwa aplikasi ini butuh port 8080
EXPOSE 8080

# Perintah yang dijalankan saat container dihidupkan
CMD ["python", "app.py"]
