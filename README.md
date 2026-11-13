# Dashboard Ejecutivo de Auditoría RPA - Universidad Manuela Beltrán (CASE)

Dashboard analítico e interactivo desarrollado para auditar el estado real operativo, técnico y de gobierno de las automatizaciones de trámites del CASE (Centro de Atención y Servicio al Estudiante) sobre la plataforma **SS&C Blue Prism 7.2**, comparándolo con el reporte de estatus emitido por Narnaja Business Intelligence (NBI).

---

## 📊 Vista Previa y Despliegue en Vivo

- **URL en Vivo (GitHub Pages):** [https://fjmateusramos.github.io/dashboard-umb-rpa/](https://fjmateusramos.github.io/dashboard-umb-rpa/)
- **Incrustación en Google Sites:** En Google Sites, ve a `Insertar` > `Incorporar` > `Por URL` y pega el enlace anterior.

---

## 🎯 Hallazgos Principales de la Auditoría

1. **Inflación por Bucle Infinito (+83.2% de sobrecupo):**
   - **414 envíos totales** para solo **226 tickets únicos**.
   - En septiembre (fase productiva): 288 envíos para 149 tickets únicos. El **48.3% del tráfico en producción fueron correos duplicados redundantes**.
   - **Causa raíz:** En el flujo de excepciones (cédula vacía o estudiante sin notas en AulaNet), el robot envía un correo de error pero **omite actualizar la etapa del ticket en HubSpot (`hs_pipeline_stage`)**. Al permanecer en etapa 1 o 2, el scheduler de Blue Prism vuelve a procesar el ticket cada 2 horas.
   - Dos estudiantes particulares llegaron a recibir **15 correos idénticos repetidos** a lo largo de 4 días.

2. **Discrepancia de Alcance (3 Procesos reportados vs. 2 Reales):**
   - Solo existen dos procesos Blue Prism (`01 - Certificados de Estudios` y `02 - Certificado de Horarios`).
   - "Certificado de Admisión" no es un proceso independiente ni un trámite de HubSpot; es una macro condicional de Microsoft Word VBO embebida en Estudios.
   - En Horarios (Proceso 02), si el alumno no está matriculado, el robot genera por error un Certificado de Admisión a Pregrado Presencial Bogotá por defecto de clonación de código.

3. **Vulnerabilidades de Seguridad Críticas:**
   - Token Bearer de HubSpot (`Bearer pat-na1-5609b158-...`) expuesto en texto plano en la colección `Headers HUB`.
   - Contraseña de aplicación de Gmail expuesta en texto plano en la acción `Configure3`.

4. **Concentración Extrema de la Demanda:**
   - **97.3%** Certificado de Estudios (220 tickets).
   - **2.7%** Certificado de Horarios (6 tickets).
   - **0%** Verificación Académica (bloqueado por falta de VPN site-to-site con Campus).

---

## 🛠️ Estructura del Repositorio

- `index.html`: Dashboard ejecutivo completo autocontenido (Tailwind CSS, Chart.js, FontAwesome y datos JSON integrados).
- `template.html`: Plantilla base modular del dashboard.
- `processed_metrics.json`: Base de datos de métricas estructuradas de los 414 envíos y 226 tickets.
- `parse_full_data.py`: Script de ingesta, cálculo de deltas y análisis de telemetría.
- `generate_dashboard.py`: Compilador del dashboard final.

---

## 🚀 Uso Local

Para abrir el dashboard localmente, simplemente abre `index.html` en cualquier navegador web:

```bash
open index.html
```

---

*Auditoría generada con base en los archivos BPA Process 01, 02, el Process Definition Document (PDD Versión 2) y el registro forense de correos.*
