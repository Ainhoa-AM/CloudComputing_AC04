# Cloud computing
In order to run the project, execute the following command line instruction:

```
uvicorn app.main:app --host 0.0.0.0 --port 8080 --log-level debug
```
# Carlemany Backend

Backend desarrollado con **FastAPI**, **PostgreSQL**, **Redis** y **MinIO**, para gestión de autenticación y archivos PDF.

## 🚀 Tecnologías

- Python 3.10
- FastAPI + Uvicorn
- PostgreSQL
- Redis
- MinIO (S3 compatible)
- Aerich (migraciones)
- Docker + Docker Compose

---

## ⚙️ Requisitos

- Docker y Docker Compose instalados

---

## 🟢 Arranque del Proyecto

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd carlemany-backend

