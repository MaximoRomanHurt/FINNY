# 💰 FINNY - Student Finance App

Aplicación de finanzas personal para estudiantes construida con **Python Flask** y **JavaScript vanilla**. Registra gastos, gestiona presupuesto mensual y gamifica tus hábitos financieros con rachas, misiones y logros.

---

## ✨ Características

| Característica | Descripción |
|---|---|
| 📊 **Dashboard completo** | Resumen de gastos diarios, semanales y mensuales |
| 💾 **Base de datos SQLite** | Persistencia real — tus datos se guardan entre sesiones |
| 🎮 **Gamificación** | Sistema de XP, niveles, rachas diarias, misiones y logros |
| 💡 **Consejos inteligentes** | Tips financieros personalizados según tu comportamiento |
| 🔔 **Modo alerta** | Aviso automático cuando te acercas al límite de presupuesto |
| 🗂️ **Categorías** | Clasifica gastos por categoría y filtra estadísticas |

---

## 🗂️ Estructura del Proyecto

```
FINNY/
├── backend/
│   ├── app.py          # Servidor Flask — API REST v2
│   ├── database.py     # Capa de datos SQLite (compras, perfil, misiones…)
│   └── finny.db        # Base de datos SQLite (se crea automáticamente)
├── frontend/
│   ├── index.html      # Interfaz principal
│   └── app.js          # Lógica JavaScript del frontend
├── transversal/
│   └── constants.py    # Constantes compartidas (categorías, límites)
└── requirements.txt    # Dependencias Python
```

---

## ⚙️ Requisitos

- **Python 3.7+** — [descargar](https://www.python.org/downloads/)
- Un navegador moderno (Chrome, Firefox, Edge…)

---

## 🚀 Cómo ejecutar el proyecto

> Necesitas **dos terminales abiertas** — una para el backend y otra para el frontend.

### 1. Instalar dependencias

Desde la carpeta raíz del proyecto (`FINNY/`):

```bash
pip install -r requirements.txt
```

### 2. Iniciar el backend (Terminal 1)

```bash
python backend/app.py
```

Deberías ver en la consola:

```
=======================================================
  FINNY Finance App Backend v2.0
  Server -> http://localhost:5000
=======================================================
[DB] Database initialized at: ...\backend\finny.db
 * Running on http://0.0.0.0:5000
```

> **Deja esta terminal abierta** — el servidor debe seguir corriendo mientras usas la app.

### 3. Iniciar el servidor del frontend (Terminal 2)

Desde la carpeta raíz del proyecto (`FINNY/`):

```bash
python -m http.server 8080 
```

### 4. Abrir la aplicación en el navegador

Ve a:
```
http://localhost:8080
```

> ✅ Con ambos servidores corriendo, el frontend en el puerto `8080` se comunica con el backend en el puerto `5000`.

---

## 🎮 Cómo usar FINNY

1. **Registra un gasto** — nombre, monto y categoría en el formulario
2. **Configura tu presupuesto** mensual para activar el análisis inteligente
3. **Sigue tu racha** — registrar gastos cada día acumula días consecutivos y da XP
4. **Completa misiones** para desbloquear logros y subir de nivel
5. **Lee los consejos** del día para ganar XP extra

---

## 🔌 Endpoints de la API

El backend corre en `http://localhost:5000`. Endpoints disponibles:

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Lista de todos los endpoints |
| `GET` | `/health` | Health check del servidor |
| `GET` | `/dashboard` | Resumen completo del dashboard |
| `GET` | `/compras` | Listar todas las compras (acepta `?category=`) |
| `POST` | `/compras` | Registrar una nueva compra |
| `GET` | `/compras/<id>` | Obtener una compra por ID |
| `DELETE` | `/compras/<id>` | Eliminar una compra |
| `GET` | `/estadisticas` | Estadísticas agrupadas por categoría |
| `GET` | `/tendencia` | Tendencia de gasto (acepta `?days=7`) |
| `GET` | `/presupuesto` | Obtener presupuesto del mes actual |
| `POST` | `/presupuesto` | Guardar presupuesto mensual |
| `GET` | `/racha` | Estado de la racha diaria |
| `GET` | `/misiones` | Misiones con progreso |
| `GET` | `/logros` | Logros desbloqueados y bloqueados |
| `GET` | `/consejos` | Consejos personalizados (acepta `?limit=3`) |
| `POST` | `/consejos/leer` | Marcar un consejo como leído (+5 XP) |
| `GET` | `/perfil` | Perfil del usuario (XP, nivel, avatar) |
| `PUT` | `/perfil` | Actualizar nombre o avatar |
| `GET` | `/categorias` | Categorías disponibles |

---

## 🛠️ Solución de problemas

### ❌ "Cannot connect to server" / la página no carga datos

- Verifica que **ambos** servidores estén corriendo (backend en 5000, frontend en 8080)
- Confirma que estás accediendo a `http://localhost:8080`, no abriendo el archivo HTML directamente
- Abre `http://localhost:5000/health` en el navegador — debe devolver `{"status": "OK"}`

### ❌ Error al iniciar el backend

```
ModuleNotFoundError: No module named 'flask'
```
→ Ejecuta `pip install -r requirements.txt` nuevamente.

```
Address already in use / [WinError 10048]
```
→ El puerto 5000 está ocupado. Cierra la aplicación que lo usa o reinicia la terminal.

### ❌ CORS Error en el navegador

- Asegúrate de acceder desde `http://localhost:8080` (NO abrir `index.html` directamente como `file://…`)
- Verifica que Flask-CORS esté instalado: `pip install Flask-CORS`

### ❌ Los datos no se guardan entre sesiones

- La base de datos se almacena en `backend/finny.db`. Si borraste ese archivo, se recreará vacío al reiniciar el backend.

---

## 📄 Licencia

Proyecto educativo de código abierto. Úsalo, modifícalo y compártelo libremente.

---

*Happy tracking with FINNY! 💰*