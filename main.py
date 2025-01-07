from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

# Función para descargar el video
def descargar_video_youtube(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.%(ext)s',  # Se descarga como video.mp4
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Ruta principal con el formulario
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Descargar Videos de YouTube</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <h1 class="text-center mb-4">Descargar Videos de YouTube</h1>
                            <form action="/download" method="post">
                                <div class="mb-3">
                                    <label for="url" class="form-label">Ingresa la URL del video:</label>
                                    <input type="url" id="url" name="url" class="form-control" placeholder="https://www.youtube.com/watch?v=..." required>
                                </div>
                                <div class="text-center">
                                    <button type="submit" class="btn btn-primary w-100">Descargar</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

# Ruta para procesar la descarga
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "Error: No se proporcionó una URL", 400

    try:
        # Descargar el video
        descargar_video_youtube(url)

        # Servir el archivo al usuario
        return send_file("video.mp4", as_attachment=True)

    except Exception as e:
        return f"Error al descargar el video: {e}", 500

    finally:
        # Limpiar el archivo descargado después de enviarlo
        if os.path.exists("video.mp4"):
            try:
                os.remove("video.mp4")
            except PermissionError:
                pass  # Ignorar si aún está siendo usado por send_file

if __name__ == "__main__":
    app.run(debug=True)
