import os
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from werkzeug.utils import secure_filename
from pathlib import Path

upload=APIRouter(prefix='/upload')
UPLOAD_FOLDER='static/uploads/'
config={"UPLOAD_FOLDER":UPLOAD_FOLDER}
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','mp4'])


@upload.post('/upload-file')

def uploadFile(file:UploadFile):
        if not file:
            raise HTTPException(status_code=400, detail="No se encontró el archivo")
        if not  allowed_file(file.filename):
            # raise HTTPException(status_code=400, detail="el tipo de archivo no es permitido")
            return JSONResponse(content={"error":"el tipo de archivo no es permitido"},status_code=400)
        filename = secure_filename(file.filename)
        file_path = os.path.join(config['UPLOAD_FOLDER'], filename)
        with open(file_path, "wb") as buffer:
          buffer.write(file.file.read())

    # Obtener la ruta relativa al directorio actual del script
        
        return JSONResponse(content={
            "success": "Archivo enviado con éxito",
            "path": filename
        }, status_code=200)
        
@upload.get('/display/{filename}')
def display(filename):

    file_path = os.path.join(config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(file_path)


def allowed_file(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

