# SGSI - Sistema de Gestión de Seguridad de la Información

Repositorio del Proyecto de Título de **Priscila Bahamondez** (INACAP).

## 📌 Contexto del proyecto

**SGSI** corresponde a un sistema orientado a apoyar la gestión de la seguridad de la información dentro de una organización, tomando como referencia buenas prácticas y lineamientos de control de seguridad.

El objetivo principal del proyecto es centralizar y facilitar procesos como:

- Registro y administración de activos de información.
- Identificación y seguimiento de riesgos de seguridad.
- Gestión de controles y cumplimiento.
- Trazabilidad de acciones y estados asociados al sistema.

Este proyecto fue desarrollado como parte del proceso de titulación, con foco en una solución funcional, escalable y mantenible.

---

## ✅ Requisitos previos

Antes de ejecutar los comandos para levantar el sistema, asegúrate de contar con lo siguiente instalado en tu entorno:

### 1) Git
Para clonar y gestionar el repositorio.

- Verificar instalación:
```bash
git --version
```

### 2) Node.js y npm
El proyecto utiliza ecosistema JavaScript/TypeScript para instalación de dependencias y ejecución.

- Versión recomendada de Node.js: **18.x o superior**
- npm se instala junto con Node.js
- Verificar instalación:
```bash
node -v
npm -v
```

### 3) Base de datos (si aplica al entorno del proyecto)
Si el sistema utiliza persistencia (por ejemplo PostgreSQL/MySQL), debes tener:

- Motor de base de datos instalado y en ejecución.
- Credenciales de acceso (usuario, contraseña, host, puerto, nombre de base de datos).
- Variables de entorno correctamente configuradas.

> Si tu proyecto usa otro motor o servicios externos, ajusta esta sección según corresponda.

### 4) Archivo de variables de entorno
Debes crear un archivo `.env` en la raíz del proyecto (o usar `.env.example` si existe).

Ejemplo referencial:
```env
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_USER=usuario
DB_PASSWORD=tu_password
DB_NAME=sgsi
JWT_SECRET=tu_clave_secreta
```

---

## 🚀 Levantar el sistema

> Ejecuta estos comandos desde la raíz del proyecto.

### 1) Clonar repositorio
```bash
git clone https://github.com/pbahamondez-inacap/proyectotitulo-inacap-Pbahamondez.git
cd proyectotitulo-inacap-Pbahamondez
```

### 2) Instalar dependencias
```bash
npm install
```

### 3) Configurar variables de entorno
- Crear `.env` con los valores de tu entorno.
- Validar conexión a base de datos (si corresponde).

### 4) Ejecutar migraciones (si aplica)
```bash
npm run migrate
```

### 5) Levantar en desarrollo
```bash
npm run dev
```

### 6) Levantar en modo producción (opcional)
```bash
npm run build
npm start
```

---

## 🧪 Comandos útiles

```bash
npm run dev        # Ejecuta en modo desarrollo
npm run build      # Compila el proyecto
npm start          # Ejecuta versión compilada
npm test           # Ejecuta pruebas (si están definidas)
npm run lint       # Revisión estática de código (si aplica)
```

---

## 📁 Estructura general del proyecto

```text
.
├── src/              # Código fuente principal
├── public/           # Recursos estáticos (si aplica)
├── README.md
├── package.json
└── .env              # Variables de entorno (no versionar)
```

---

## 👩‍💻 Autoría

**Priscila Bahamondez**  
Proyecto de Título - INACAP

---

## 📄 Licencia

Este proyecto se distribuye para fines académicos.  
Puedes agregar aquí una licencia formal si corresponde (MIT, Apache 2.0, etc.).
