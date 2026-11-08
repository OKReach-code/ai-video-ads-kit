Aquí se crea una carpeta por anuncio con `tools/new_project.sh <nombre>` (o `/nuevo-anuncio <nombre>`).
Por defecto no se suben a git (vídeos y audios pesan mucho): si quieres versionar el «código» de tus anuncios, quita `proyectos/*/` del `.gitignore`
y añade reglas para excluir `*.mp4`, `*.wav`, `*.mp3`, `render/` y `edit_*/`.
