# LaburArg — Backend

Portal de empleo pensado para el mercado argentino. Conecta personas que buscan trabajo con empresas y consultoras de RR.HH., con foco en un nicho específico y funciones de matching asistido por IA.

Este repositorio contiene el **backend**, construido con Django + Django REST Framework.

> Proyecto de portfolio, desarrollado como preparación para una postulación real a una posición de Analista de Desarrollo Full Stack Jr.

## Stack tecnológico

- **Backend:** Python 3, Django 6, Django REST Framework
- **Base de datos:** MySQL/MariaDB (SQLite en desarrollo local inicial)
- **Tareas en segundo plano:** Celery + Redis
- **IA:** integración con APIs de Gemini y Claude para matching CV ↔ oferta y generación de contenido
- **Frontend:** React + Vite + Bootstrap (repositorio separado)
- **Infraestructura:** Docker, Git

## Estado actual del proyecto

- [x] Modelo de datos diseñado (ver diagrama entidad-relación)
- [x] Proyecto Django inicial creado (`core`)
- [x] Apps del dominio creadas: `accounts`, `companies`, `jobs`, `cvs`, `applications`
- [x] Modelos escritos y migrados (User, Company, CompanyMember, Job, CV, Application, Favorite)
- [x] Modelos registrados en el panel de administración
- [x] Repositorio versionado con Git
- [ ] Panel de administración con vistas personalizadas (list_display, filtros, búsqueda)
- [ ] API REST (serializers y endpoints DRF)
- [ ] Autenticación (JWT)
- [ ] Integración de IA (matching CV ↔ oferta, generación de carta de presentación)
- [ ] Dockerización (Django + MySQL + Redis + Celery)
- [ ] Frontend React conectado a la API
- [ ] Deploy

## Modelo de datos

| App | Modelos |
|---|---|
| `accounts` | `User` (extiende AbstractUser) |
| `companies` | `Company`, `CompanyMember` |
| `jobs` | `Job` |
| `cvs` | `CV` |
| `applications` | `Application`, `Favorite` |

## Cómo levantar el proyecto en local (Windows / PowerShell)

```powershell
# 1. Crear y activar el entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones (crear las tablas en la base de datos)
python manage.py migrate

# 4. Crear un usuario administrador
python manage.py createsuperuser

# 5. Levantar el servidor de desarrollo
python manage.py runserver
```

El servidor queda disponible en `http://127.0.0.1:8000/`, y el panel de administración en `http://127.0.0.1:8000/admin/`.


## Estructura de carpetas

```
laburarg-backend/
├── core/               # Configuración global del proyecto Django (settings, urls raíz)
├── accounts/           # App: usuarios que buscan empleo
├── companies/          # App: empresas y consultoras
├── jobs/                # App: búsquedas laborales
├── cvs/                  # App: CVs subidos por los usuarios
├── applications/    # App: postulaciones y favoritos
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```


## Notas de arquitectura

Cada app de Django agrupa un dominio específico del negocio (patrón recomendado por la propia documentación de Django para proyectos medianos/grandes). Esto facilita que cada parte del sistema se pueda testear, mantener y eventualmente extraer de forma independiente si el proyecto creciera.

Decisiones de diseño relevantes:
- `Company` unifica empresas y consultoras con un campo booleano (`is_agency`) en vez de dos modelos separados, evitando duplicación de esquema.
- `CompanyMember` es una tabla intermedia que resuelve la relación muchos-a-muchos entre usuarios y empresas (un usuario puede administrar varias empresas, una empresa puede tener varios administradores).
- `Application.cv` usa `on_delete=PROTECT` en vez de `CASCADE`: una postulación ya enviada es un registro histórico que no debe desaparecer si se borra el CV asociado.