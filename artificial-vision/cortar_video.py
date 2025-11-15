from moviepy.video.io.VideoFileClip import VideoFileClip

# --- Parámetros ---
archivo_entrada = "videos/skiff.mp4"  # Cambia por tu archivo original
archivo_salida = "videos/ultralytics_cortado.mp4"
inicio = 10  # Segundo de inicio
fin = 25     # Segundo de fin

# --- Proceso ---
# Cargar el video
clip = VideoFileClip(archivo_entrada)

# Cortar el fragmento deseado
clip_cortado = clip.subclipped(inicio, fin)

# Guardar el nuevo archivo en formato MP4
clip_cortado.write_videofile(archivo_salida, codec="libx264", audio_codec="aac")

print(f"✅ Video guardado como '{archivo_salida}'")
s