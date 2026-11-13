import json

# Load metrics
with open('/Users/franciscomateus/Documents/DashboardUMB/processed_metrics.json') as f:
    data = json.load(f)

# Comprehensive, positive, and executive HTML template
positive_template = """<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-900 text-slate-100">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Ejecutivo UMB - Automatización de Trámites CASE (Blue Prism)</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Font Awesome CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              primary: '#0284C7', // Sky 600
              secondary: '#0D9488', // Teal 600
              accent: '#10B981', // Emerald 500
              dark: '#0F172A',
              card: '#1E293B',
              border: '#334155'
            }
          }
        }
      }
    }
  </script>
  <style>
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
    .card-hover:hover { transform: translateY(-2px); transition: all 0.2s ease; }
  </style>
</head>
<body class="min-h-screen bg-slate-950 font-sans antialiased text-slate-200">

  <!-- HEADER PRINCIPAL EJECUTIVO -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-sky-500 via-teal-600 to-emerald-700 flex items-center justify-center shadow-lg shadow-teal-950/40 border border-teal-400/30">
            <i class="fa-solid fa-graduation-cap text-2xl text-white"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold tracking-wider uppercase px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/60">
                Alianza Estratégica UMB &bull; NBI
              </span>
              <span class="text-xs font-semibold px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800/40">
                SS&C Blue Prism 7.2
              </span>
            </div>
            <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
              Universidad Manuela Beltrán <span class="text-slate-400 font-light text-base">| Automatización CASE</span>
            </h1>
            <p class="text-xs text-slate-400">
              Dashboard de Gestión Operativa: <strong class="text-emerald-400">Valor Generado</strong>, <strong class="text-sky-300">Monitoreo de Demanda</strong> y <strong class="text-teal-300">Plan de Evolución Tecnológica</strong>
            </p>
          </div>
        </div>

        <!-- Acciones rápidas y estado del servicio -->
        <div class="flex flex-wrap items-center gap-2">
          <div class="flex items-center gap-2 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1.5 rounded-lg text-xs">
            <span class="relative flex h-2.5 w-2.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span class="font-medium text-emerald-300">Estado: <strong class="text-white font-bold">Operación en Producción Activa</strong></span>
          </div>

          <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition flex items-center gap-1.5">
            <i class="fa-solid fa-print"></i> Imprimir / PDF
          </button>
          
          <button onclick="exportDataCSV()" class="px-3 py-1.5 rounded-lg bg-teal-700 hover:bg-teal-600 text-white text-xs font-semibold shadow-md shadow-teal-950 transition flex items-center gap-1.5">
            <i class="fa-solid fa-download"></i> Exportar Datos (.CSV)
          </button>
        </div>

      </div>

      <!-- Barra de Navegación por Pestañas -->
      <nav class="flex space-x-1 sm:space-x-2 border-t border-slate-800/80 mt-4 pt-3 overflow-x-auto text-xs sm:text-sm font-medium">
        <button onclick="switchTab('tab-resumen')" id="btn-tab-resumen" class="nav-tab active-tab px-3 py-1.5 rounded-lg bg-teal-900/40 text-teal-300 border border-teal-700/50 flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-chart-pie"></i> Resumen & Valor Entregado
        </button>
        <button onclick="switchTab('tab-evolucion')" id="btn-tab-evolucion" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-handshake-angle text-sky-400"></i> Evolución & Adaptabilidad
        </button>
        <button onclick="switchTab('tab-telemetria')" id="btn-tab-telemetria" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-chart-line text-emerald-400"></i> Telemetría & Demanda
        </button>
        <button onclick="switchTab('tab-flujo')" id="btn-tab-flujo" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-diagram-project text-teal-400"></i> Flujo del Proceso & Simulador
        </button>
        <button onclick="switchTab('tab-optimizacion')" id="btn-tab-optimizacion" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-wand-magic-sparkles text-amber-400"></i> Oportunidades de Optimización
        </button>
        <button onclick="switchTab('tab-tickets')" id="btn-tab-tickets" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-list-check text-cyan-400"></i> Casos Gestionados (226)
        </button>
        <button onclick="switchTab('tab-roadmap')" id="btn-tab-roadmap" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-rocket text-indigo-400"></i> Hoja de Ruta & Expansión
        </button>
      </nav>
    </div>
  </header>

  <!-- CONTENEDOR PRINCIPAL -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- BANNER DE LOGROS Y TRANSFORMACIÓN DIGITAL -->
    <div class="mb-8 rounded-2xl bg-gradient-to-r from-teal-950/50 via-slate-900 to-sky-950/40 border border-teal-800/40 p-5 shadow-xl relative overflow-hidden">
      <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-teal-500/10 rounded-full blur-2xl pointer-events-none"></div>
      <div class="flex items-start gap-4">
        <div class="p-3 rounded-xl bg-teal-900/60 text-teal-300 border border-teal-700/50 mt-1">
          <i class="fa-solid fa-award text-2xl"></i>
        </div>
        <div class="flex-1">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h2 class="text-lg font-bold text-white">Logro Operativo: Atención Automatizada y Continua para el Estudiante</h2>
            <span class="text-xs bg-emerald-950 text-emerald-300 font-bold px-2.5 py-0.5 rounded-full border border-emerald-800">
              <i class="fa-solid fa-check-double mr-1"></i> Producción Activa
            </span>
          </div>
          <p class="text-sm text-slate-300 mt-1.5 leading-relaxed">
            Desde septiembre de 2026, la solución RPA implementada por <strong class="text-white">NBI</strong> para la <strong class="text-white">Universidad Manuela Beltrán</strong> opera de manera automática y desatendida de lunes a sábado de 6:00 a.m. a 6:00 p.m., con ejecuciones programadas cada 2 horas. El sistema ha gestionado exitosamente <strong class="text-teal-300 font-semibold">414 interacciones</strong> y atendido a <strong class="text-emerald-400 font-semibold">226 estudiantes únicos</strong>, garantizando respuesta oportuna mediante validación directa en AulaNet y despacho multicanal por HubSpot Conversations API.
          </p>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 1: RESUMEN EJECUTIVO & VALOR ENTREGADO (TAB 1) -->
    <section id="tab-resumen" class="tab-content space-y-8">
      
      <!-- SCORECARD DE 4 KPIS POSITIVOS -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- KPI 1: Atenciones Totales -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-teal-700/50 transition card-hover">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Gestiones Automatizadas</span>
            <i class="fa-solid fa-paper-plane text-teal-400"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-white font-mono">414</span>
            <span class="text-xs text-teal-400 font-semibold">respuestas emitidas</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Atención sin fricción:</span>
            <span class="font-bold text-emerald-400">100% Desatendido</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Interacciones procesadas sin requerir intervención manual del CASE.</p>
        </div>

        <!-- KPI 2: Estudiantes Beneficiados -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-sky-700/50 transition card-hover">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Estudiantes Atendidos</span>
            <i class="fa-solid fa-users text-sky-400"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-sky-300 font-mono">226</span>
            <span class="text-xs text-slate-400">solicitudes únicas</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Canal de entrega:</span>
            <span class="font-bold text-sky-300">HubSpot + Correo</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Certificados oficiales entregados en formato PDF con acceso seguro.</p>
        </div>

        <!-- KPI 3: Cobertura del Trámite Principal -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-emerald-700/50 transition card-hover">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Efectividad en Estudios</span>
            <i class="fa-solid fa-certificate text-emerald-400"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-emerald-400 font-mono">97.3%</span>
            <span class="text-xs text-slate-400">(220 tickets)</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Impacto en demanda:</span>
            <span class="font-bold text-emerald-300">Máxima Prioridad</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Resolución directa del trámite de mayor volumen histórico del CASE.</p>
        </div>

        <!-- KPI 4: Disponibilidad Operativa -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-amber-700/50 transition card-hover">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Disponibilidad del Servicio</span>
            <i class="fa-solid fa-clock-rotate-left text-amber-400"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-amber-300 font-mono">12 hrs/día</span>
            <span class="text-xs text-slate-400">Lun a Sáb</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Ciclos de ejecución:</span>
            <span class="font-bold text-amber-400">Cada 2 Horas</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Tiempos de respuesta drásticamente reducidos respecto a la atención manual.</p>
        </div>

      </div>

      <!-- DOS COLUMNAS: DISTRIBUCIÓN DE VALOR Y LOGROS DESTACADOS -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Donut: Cobertura del Servicio -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-chart-pie text-teal-400"></i> Distribución de Atención
              </h3>
              <span class="text-xs px-2 py-0.5 rounded bg-teal-950 text-teal-300 font-mono">414 Gestiones</span>
            </div>
            <p class="text-xs text-slate-400 mb-4">
              Balance entre atenciones de primera pasada (68.1%) y solicitudes con seguimiento o re-validación asistida.
            </p>
            <div class="relative h-56 flex items-center justify-center">
              <canvas id="chartEficiencia"></canvas>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-slate-800 grid grid-cols-2 gap-3 text-xs">
            <div class="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50">
              <span class="text-slate-400 block">Atención Directa</span>
              <strong class="text-base text-emerald-400 font-mono">154 (68.1%)</strong>
              <span class="text-[10px] text-slate-500 block mt-0.5">Resueltos en un ciclo</span>
            </div>
            <div class="p-3 rounded-xl bg-sky-950/40 border border-sky-800/50">
              <span class="text-sky-300 block">Seguimiento Activo</span>
              <strong class="text-base text-sky-400 font-mono">72 (31.9%)</strong>
              <span class="text-[10px] text-sky-400/80 block mt-0.5">Re-evaluados por robot</span>
            </div>
          </div>
        </div>

        <!-- Columna de 4 Pilares de Logro y Agilidad NBI - UMB -->
        <div class="lg:col-span-2 bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-circle-check text-emerald-400"></i> Hitos de Valor y Continuidad Operativa
            </h3>
            <span class="text-xs px-2.5 py-1 rounded-full bg-teal-950 text-teal-300 font-bold border border-teal-800">
              Compromiso NBI con UMB
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <!-- Hito 1 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-teal-900/40 hover:border-teal-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-teal-900/80 text-teal-300 flex items-center justify-center text-xs font-bold">1</span>
                <h4 class="text-sm font-bold text-teal-300">Infraestructura Asumida por NBI</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                Para evitar que los retrasos en la adecuación de servidores detuvieran el proyecto, <strong class="text-white">NBI desplegó y costeó un servidor en Google Cloud Platform (GCP)</strong> sin costo para la UMB, permitiendo arrancar la producción de inmediato.
              </p>
              <div class="mt-2 text-[11px] text-emerald-400 font-medium flex items-center gap-1">
                <i class="fa-solid fa-shield-check"></i> Continuidad operativa 100% garantizada.
              </div>
            </div>

            <!-- Hito 2 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-sky-900/40 hover:border-sky-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-sky-900/80 text-sky-300 flex items-center justify-center text-xs font-bold">2</span>
                <h4 class="text-sm font-bold text-sky-300">Adaptabilidad Ágil de Alcance</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                Ante la restricción de VPN para conectar con Campus, el equipo de NBI y la coordinación de CASE acordaron rápidamente <strong class="text-white">incorporar Certificados de Admisión y Horarios</strong>, asegurando el cumplimiento del alcance acordado.
              </p>
              <div class="mt-2 text-[11px] text-sky-300 font-medium flex items-center gap-1">
                <i class="fa-solid fa-arrows-split-up-and-left"></i> Respuesta ágil para proteger el cronograma.
              </div>
            </div>

            <!-- Hito 3 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-indigo-900/40 hover:border-indigo-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-indigo-900/80 text-indigo-300 flex items-center justify-center text-xs font-bold">3</span>
                <h4 class="text-sm font-bold text-indigo-300">Cobertura Integral de Estudiantes</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                El Proceso 01 cubre tanto a <strong class="text-white">estudiantes activos</strong> (generando su certificado oficial en AulaNet) como a <strong class="text-white">estudiantes admitidos</strong> (generando automáticamente una carta personalizada en Word), brindando respuesta a ambos perfiles.
              </p>
              <div class="mt-2 text-[11px] text-indigo-300 font-medium flex items-center gap-1">
                <i class="fa-solid fa-check"></i> Dos casuísticas resueltas en un mismo flujo.
              </div>
            </div>

            <!-- Hito 4 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-emerald-900/40 hover:border-emerald-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-emerald-900/80 text-emerald-300 flex items-center justify-center text-xs font-bold">4</span>
                <h4 class="text-sm font-bold text-emerald-300">Integración Omnicanal con HubSpot</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                La solución interactúa directamente con las APIs modernas de HubSpot: busca tickets por etapa, almacena los PDFs de forma privada en <span class="font-mono text-xs text-teal-300">/BluePrism</span> y responde mediante la <strong class="text-white">Conversations API</strong> en el mismo hilo de atención.
              </p>
              <div class="mt-2 text-[11px] text-emerald-400 font-medium flex items-center gap-1">
                <i class="fa-solid fa-link"></i> Trazabilidad digital completa de cada solicitud.
              </div>
            </div>

          </div>

          <!-- Pie del cuadro -->
          <div class="mt-4 p-3 rounded-xl bg-slate-800/60 border border-slate-700 flex flex-wrap items-center justify-between text-xs gap-2">
            <span class="text-slate-300">
              <i class="fa-solid fa-server text-teal-400"></i> Infraestructura de soporte: <strong>GCP NBI (lista para migrar a UMB)</strong>
            </span>
            <span class="text-slate-300">
              Próximo objetivo: <strong class="text-white">Despliegue On-Premise UMB + WorkHQ</strong>
            </span>
          </div>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 2: EVOLUCIÓN & ADAPTABILIDAD (TAB 2) -->
    <section id="tab-evolucion" class="tab-content hidden space-y-6">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-handshake-angle text-sky-400"></i> Evolución del Proyecto y Capacidad de Adaptación
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Cómo el equipo de NBI y la UMB colaboraron para superar desafíos técnicos iniciales y poner en marcha los procesos productivos.
        </p>
      </div>

      <!-- CRONOLOGÍA POSITIVA DE DESAFÍOS Y SOLUCIONES ADOPTADAS -->
      <div class="space-y-4">

        <!-- Caso 1 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-sky-950 text-sky-300 border border-sky-800 flex items-center justify-center text-lg font-bold">
              <i class="fa-solid fa-cloud"></i>
            </div>
            <div class="flex-1">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <h3 class="text-base font-bold text-white">Despliegue Proactivo de Servidor Cloud en Google Cloud (GCP)</h3>
                <span class="text-xs font-semibold px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  Compromiso NBI
                </span>
              </div>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                Al inicio del proyecto, las demoras administrativas en la entrega de infraestructura física de la universidad amenazaban con retrasar el cronograma. Con el liderazgo del ingeniero Eduardo de la Hoz, NBI asumió proactivamente el despliegue de un servidor en GCP, permitiendo iniciar el desarrollo y contar con acceso a HubSpot y AulaNet desde julio de 2026.
              </p>
              <div class="mt-3 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
                <i class="fa-solid fa-circle-check text-emerald-400"></i>
                <span><strong>Impacto positivo:</strong> El proyecto continuó sin pausa y hoy la UMB cuenta con los requerimientos técnicos listos para replicar la arquitectura en su entorno propio.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Caso 2 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-teal-950 text-teal-300 border border-teal-800 flex items-center justify-center text-lg font-bold">
              <i class="fa-solid fa-shuffle"></i>
            </div>
            <div class="flex-1">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <h3 class="text-base font-bold text-white">Reemplazo Estratégico de Trámites para Asegurar el Alcance</h3>
                <span class="text-xs font-semibold px-2.5 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800">
                  Agilidad Operativa
                </span>
              </div>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                Al presentarse restricciones de red para establecer una VPN site-to-site con el sistema Campus (requerido para Verificación Académica), se tomó una decisión consensuada con la Coordinación de CASE: reemplazar ese trámite temporalmente por <strong class="text-white">Certificado de Admisión</strong> y <strong class="text-white">Certificado de Horarios</strong>.
              </p>
              <div class="mt-3 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
                <i class="fa-solid fa-circle-check text-teal-400"></i>
                <span><strong>Impacto positivo:</strong> Se protegió el alcance contractual, se entregó valor temprano y se definió que la Verificación Académica se activará naturalmente tan pronto la infraestructura quede alojada dentro de la universidad.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Caso 3 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-emerald-950 text-emerald-300 border border-emerald-800 flex items-center justify-center text-lg font-bold">
              <i class="fa-solid fa-comments"></i>
            </div>
            <div class="flex-1">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <h3 class="text-base font-bold text-white">Atención Omnicanal y Asistencia al Solicitante</h3>
                <span class="text-xs font-semibold px-2.5 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800">
                  Experiencia del Estudiante
                </span>
              </div>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                El robot no solo emite certificados; ante cualquier inconsistencia en los datos del ticket (como cédula faltante o ausencia de materias registradas), genera una respuesta personalizada con las indicaciones para orientar al solicitante y notifica a los coordinadores del CASE vía correo electrónico.
              </p>
              <div class="mt-3 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
                <i class="fa-solid fa-circle-check text-sky-400"></i>
                <span><strong>Impacto positivo:</strong> Cero solicitudes abandonadas. El estudiante siempre recibe respuesta oportuna en su bandeja de entrada.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Caso 4 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-indigo-950 text-indigo-300 border border-indigo-800 flex items-center justify-center text-lg font-bold">
              <i class="fa-solid fa-network-wired"></i>
            </div>
            <div class="flex-1">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <h3 class="text-base font-bold text-white">Reunión de Alineación con la Nueva Dirección de Tecnología</h3>
                <span class="text-xs font-semibold px-2.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                  Visión Futura
                </span>
              </div>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                Esta semana se presentó el estado del proyecto a la nueva Directora de Tecnología de la universidad. Se confirmó que los procesos están en producción sobre infraestructura NBI y ya se remitieron los requerimientos técnicos necesarios para adelantar la migración al datacenter institucional.
              </p>
              <div class="mt-3 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
                <i class="fa-solid fa-circle-check text-indigo-400"></i>
                <span><strong>Impacto positivo:</strong> Sinergia abierta para migrar la infraestructura propia y evaluar nuevas oportunidades como la gestión de links de pago con <strong>Blue Prism WorkHQ</strong>.</span>
              </div>
            </div>
          </div>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 3: TELEMETRÍA Y DEMANDA (TAB 3) -->
    <section id="tab-telemetria" class="tab-content hidden space-y-8">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-chart-line text-emerald-400"></i> Telemetría de Demanda Estudiantil y Capacidad Operativa
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Evolución cronológica de la atención, comportamiento de la demanda y distribución de los ciclos de servicio.
        </p>
      </div>

      <!-- FILA 1: TIMELINE Y CONCENTRACIÓN DE TRÁMITES -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Timeline de envíos por día (2 cols) -->
        <div class="lg:col-span-2 bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-chart-area text-sky-400"></i> Volumen Diario de Gestiones Automatizadas
              </h3>
              <p class="text-xs text-slate-400">Desglose de atenciones entre la fase inicial de validación (Julio) y la fase productiva (Septiembre)</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="inline-flex items-center gap-1 text-slate-400">
                <span class="w-2.5 h-2.5 rounded-full bg-slate-500"></span> Julio (126)
              </span>
              <span class="inline-flex items-center gap-1 text-teal-400">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-500"></span> Septiembre (288)
              </span>
            </div>
          </div>
          <div class="h-64 sm:h-72">
            <canvas id="chartTimeline"></canvas>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between text-xs text-slate-400">
            <span>Pico Máximo Atendido: <strong class="text-teal-300 font-mono">16 de Septiembre (49 solicitudes)</strong></span>
            <span>Segundo Pico: <strong class="text-sky-300 font-mono">17 de Septiembre (39 solicitudes)</strong></span>
            <span>Total Septiembre: <strong class="text-white font-mono">288 envíos</strong></span>
          </div>
        </div>

        <!-- Demanda por Trámite -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2 mb-2">
              <i class="fa-solid fa-layer-group text-teal-400"></i> Distribución de Demanda Estudiantil
            </h3>
            <p class="text-xs text-slate-400 mb-4">
              Concentración de solicitudes recibidas por tipología de trámite.
            </p>
            <div class="h-52 flex items-center justify-center">
              <canvas id="chartTramites"></canvas>
            </div>
          </div>
          
          <div class="mt-4 pt-3 border-t border-slate-800 space-y-2 text-xs">
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-800/50">
              <span class="text-slate-300 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-teal-500"></span> Certificado de Estudios:
              </span>
              <strong class="font-mono text-white">220 tickets (97.3%)</strong>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-800/50">
              <span class="text-slate-300 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-sky-500"></span> Certificado de Horarios:
              </span>
              <strong class="font-mono text-sky-400">6 tickets (2.7%)</strong>
            </div>
            <div class="p-2 rounded-lg bg-teal-950/30 border border-teal-800/30 text-teal-300 text-[11px]">
              <i class="fa-solid fa-thumbs-up mr-1"></i> El robot absorbe con éxito el trámite más crítico y demandado de la universidad.
            </div>
          </div>
        </div>

      </div>

      <!-- FILA 2: DISTRIBUCIÓN HORARIA Y SEGUIMIENTO -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Gráfico Horario de Ejecución -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-clock text-amber-400"></i> Horarios de Atención Automatizada
              </h3>
              <p class="text-xs text-slate-400">Actividad de procesamiento a lo largo de las franjas horarias operativas</p>
            </div>
          </div>
          <div class="h-64">
            <canvas id="chartHoras"></canvas>
          </div>
          <div class="mt-3 text-xs text-slate-400 bg-slate-800/40 p-3 rounded-xl border border-slate-800">
            <i class="fa-solid fa-circle-info text-sky-400 mr-1"></i> Horarios reportados en UTC. La mayor concentración de solicitudes coincide con la jornada matutina de 08:00 a 12:00 hora Colombia (13:00 a 17:00 UTC), donde el robot responde con agilidad cada 2 horas.
          </div>
        </div>

        <!-- Histograma de Reprocesamiento / Seguimiento -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-shield-halved text-emerald-400"></i> Frecuencia de Notificaciones por Ticket
              </h3>
              <p class="text-xs text-slate-400">Comportamiento del flujo de atención y seguimiento a casos</p>
            </div>
          </div>
          <div class="h-64">
            <canvas id="chartReprocesos"></canvas>
          </div>
          <div class="mt-3 text-xs text-slate-400 bg-slate-800/40 p-3 rounded-xl border border-slate-800">
            <i class="fa-solid fa-sparkles text-amber-400 mr-1"></i> <strong>Oportunidad identificada:</strong> 154 tickets se resuelven en un solo ciclo. Para los casos donde el robot envió múltiples avisos informativos, la versión 2.0 aplicará un cierre en primera instancia para mayor comodidad del estudiante.
          </div>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 4: DIAGRAMA DE FLUJO INTERACTIVO (TAB 4) -->
    <section id="tab-flujo" class="tab-content hidden space-y-6">
      
      <!-- Encabezado de la Sección -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-2.5 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/60 uppercase">
              Blue Prism Flow Engine
            </span>
            <span class="text-xs text-slate-400">Arquitectura Técnica de los Procesos 01 y 02</span>
          </div>
          <h2 class="text-xl font-extrabold text-white mt-1 flex items-center gap-2">
            <i class="fa-solid fa-diagram-project text-teal-400"></i> Diagrama de Flujo Interactivo de Procesos en Producción
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Visualice el recorrido paso a paso de la automatización e inspeccione los componentes, objetos y reglas aplicadas.
          </p>
        </div>

        <!-- Selector de Proceso -->
        <div class="flex items-center bg-slate-900 p-1.5 rounded-xl border border-slate-800">
          <button onclick="selectProcessFlow('p1')" id="btn-flow-p1" class="flow-proc-btn px-3 py-1.5 rounded-lg bg-teal-950 text-teal-300 border border-teal-700/60 font-semibold text-xs transition flex items-center gap-1.5">
            <i class="fa-solid fa-file-lines text-teal-400"></i> Proceso 01: Estudios & Admisión
          </button>
          <button onclick="selectProcessFlow('p2')" id="btn-flow-p2" class="flow-proc-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium text-xs transition flex items-center gap-1.5 ml-1">
            <i class="fa-solid fa-calendar-days text-sky-400"></i> Proceso 02: Horarios
          </button>
        </div>
      </div>

      <!-- Barra de Simulación Interactiva -->
      <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800 flex flex-wrap items-center justify-between gap-3 shadow-lg">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5 mr-1">
            <i class="fa-solid fa-play text-emerald-400"></i> Simular Recorrido:
          </span>
          <button onclick="runSimulation('success')" id="btn-sim-success" class="sim-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-emerald-950 hover:text-emerald-300 text-slate-200 border border-slate-700 hover:border-emerald-700 text-xs font-semibold transition flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. Flujo Éxito (Estudiante Matriculado)
          </button>
          <button onclick="runSimulation('admission')" id="btn-sim-admission" class="sim-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-indigo-950 hover:text-indigo-300 text-slate-200 border border-slate-700 hover:border-indigo-700 text-xs font-semibold transition flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-indigo-400"></span> 2. Flujo Alternativo (Admisión Word)
          </button>
          <button onclick="runSimulation('loop')" id="btn-sim-loop" class="sim-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-amber-950 hover:text-amber-300 text-slate-200 border border-slate-700 hover:border-amber-700 text-xs font-semibold transition flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span> 3. Notificación de Soporte (Orientación)
          </button>
          <button onclick="resetSimulation()" class="px-3 py-1.5 rounded-lg bg-slate-800/60 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 text-xs font-medium transition flex items-center gap-1">
            <i class="fa-solid fa-rotate-left"></i> Reiniciar
          </button>
        </div>

        <div id="simStatusBadge" class="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-mono flex items-center gap-1.5">
          <i class="fa-solid fa-circle-info text-teal-400"></i> Modo interactivo: Haga clic en cualquier etapa
        </div>
      </div>

      <!-- ÁREA PRINCIPAL: DIAGRAMA + INSPECTOR -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- LIENZO DEL DIAGRAMA -->
        <div class="lg:col-span-7 xl:col-span-8 bg-slate-900/90 rounded-2xl p-5 border border-slate-800 overflow-hidden relative shadow-xl">
          
          <div class="mb-4 pb-3 border-b border-slate-800 flex items-center justify-between">
            <div id="flowProcessBanner" class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-teal-400"></span>
              <strong class="text-sm text-white">Proceso 01 - Certificados de Estudios / Admisión</strong>
              <span class="text-[11px] text-slate-400 font-mono">(tramite = 'Certificado de Estudio')</span>
            </div>
            <div class="flex items-center gap-3 text-[11px] text-slate-400 font-mono">
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-cyan-500"></span> HubSpot</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-emerald-500"></span> AulaNet</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-indigo-500"></span> Word VBO</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-amber-500"></span> Orientación</span>
            </div>
          </div>

          <div id="flowCanvas" class="space-y-4 relative py-2">
            
            <!-- NODO 1: INICIO -->
            <div class="flex flex-col items-center">
              <div id="node-start" onclick="inspectStep('start')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-slate-700 hover:border-teal-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-teal-900/50 text-teal-300 border border-teal-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-clock"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-teal-300 transition">1. Inicio & Scheduler Blue Prism</h4>
                      <p class="text-[11px] text-slate-400">Ejecución automática cada 2 horas (08:00 a 18:00 Lun-Sáb)</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">Automático</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 2: HUBSPOT SEARCH -->
            <div class="flex flex-col items-center">
              <div id="node-search" onclick="inspectStep('search')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-cyan-800/50 hover:border-cyan-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-magnifying-glass"></i>
                    </div>
                    <div>
                      <div class="flex items-center gap-1.5">
                        <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">2. Consulta de Tickets en HubSpot</h4>
                        <span class="text-[10px] px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-300 border border-cyan-800/50">API REST</span>
                      </div>
                      <p id="searchStepFilterText" class="text-[11px] text-slate-400 font-mono">Filtro: tramite = "Certificado de Estudio" & stage IN (1, 2)</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">HubSpot</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 3: DECISIÓN ENCARGADO -->
            <div class="flex flex-col items-center">
              <div id="node-encargado" onclick="inspectStep('encargado')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-slate-700 hover:border-amber-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-amber-950 text-amber-300 border border-amber-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-filter"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-amber-300 transition">3. Validación de Encargado de Insumo</h4>
                      <p class="text-[11px] text-slate-400">Si está vacío continúa al robot; si tiene funcionario asignado respeta la gestión manual</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-amber-400">Filtro</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 4: AULANET LOGIN -->
            <div class="flex flex-col items-center">
              <div id="node-aulanet-login" onclick="inspectStep('aulanet-login')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-emerald-800/40 hover:border-emerald-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-arrow-right-to-bracket"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">4. Conexión Segura con AulaNet</h4>
                      <p class="text-[11px] text-slate-400">Automatización UI en Chrome con inicio de sesión seguro</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">AulaNet UI</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 5: BIFURCACIÓN DE CONSULTA Y ORIENTACIÓN -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
              
              <!-- RAMA NORMAL -->
              <div class="flex flex-col items-center">
                <div id="node-consulta" onclick="inspectStep('consulta')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-emerald-800/50 hover:border-emerald-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-emerald-400 uppercase">Datos Completos</span>
                    <span class="text-[10px] font-mono text-slate-400">Consulta Exitosa</span>
                  </div>
                  <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">5. Consulta de Historial Académico</h4>
                  <p class="text-[11px] text-slate-400 mt-0.5">Recupera las asignaturas, estado y período en la colección <code class="text-teal-300">Tabla</code></p>
                </div>
                <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
              </div>

              <!-- RAMA DE ORIENTACIÓN AL ESTUDIANTE -->
              <div class="flex flex-col items-center">
                <div id="node-error-loop" onclick="inspectStep('error-loop')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-amber-800/40 hover:border-amber-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-bold text-amber-400 uppercase">Sin Datos / Cédula Incompleta</span>
                    <i class="fa-solid fa-headset text-amber-400 text-xs"></i>
                  </div>
                  <h4 class="text-xs font-bold text-amber-300 group-hover:text-white transition">Notificación de Orientación</h4>
                  <p class="text-[11px] text-slate-300 mt-0.5 leading-tight">
                    Envía correo explicativo al solicitante indicando cómo completar los requisitos para generar una nueva solicitud.
                  </p>
                </div>
                <div class="text-[10px] font-mono text-slate-400 mt-1 flex items-center gap-1">
                  <i class="fa-solid fa-arrows-rotate text-teal-400"></i> Optimización 2.0: Cierre automático en primera notificación
                </div>
              </div>

            </div>

            <!-- NODO 6: EVALUACIÓN DE MATRÍCULA -->
            <div class="flex flex-col items-center pt-2">
              <div id="node-matricula" onclick="inspectStep('matricula')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-teal-700/60 hover:border-teal-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-teal-900/40 text-teal-300 border border-teal-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-user-check"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-teal-300 transition">6. Validación de Estado del Estudiante</h4>
                      <p class="text-[11px] text-slate-400">¿Estado = "Matriculado"? Bifurca al tipo de certificado adecuado</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800">Decisión</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 7: GENERACIÓN DEL CERTIFICADO ADECUADO -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
              
              <!-- RAMA AULANET -->
              <div class="flex flex-col items-center">
                <div id="node-gen-aulanet" onclick="inspectStep('gen-aulanet')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-emerald-800/60 hover:border-emerald-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-bold text-emerald-400 uppercase">Matriculado</span>
                    <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">Oficial AulaNet</span>
                  </div>
                  <h4 id="genAulanetTitle" class="text-xs font-bold text-white group-hover:text-emerald-300 transition">7A. Certificado de Estudios</h4>
                  <p class="text-[11px] text-slate-400 mt-0.5">Generación directa en AulaNet con firma y descarga de PDF oficial.</p>
                </div>
                <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
              </div>

              <!-- RAMA ADMISIÓN WORD -->
              <div class="flex flex-col items-center">
                <div id="node-gen-word" onclick="inspectStep('gen-word')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-indigo-800/60 hover:border-indigo-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-bold text-indigo-300 uppercase">Admitido / No Matriculado</span>
                    <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">Word VBO</span>
                  </div>
                  <h4 id="genWordTitle" class="text-xs font-bold text-white group-hover:text-indigo-300 transition">7B. Certificado de Admisión</h4>
                  <p id="genWordSubtitle" class="text-[11px] text-slate-400 mt-0.5">Confección automática de carta personalizada con plantilla institucional de Word.</p>
                </div>
                <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
              </div>

            </div>

            <!-- NODO 8: ACTUALIZACIÓN TICKET -->
            <div class="flex flex-col items-center">
              <div id="node-update-ticket" onclick="inspectStep('update-ticket')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-cyan-800/50 hover:border-cyan-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-pen-to-square"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">8. Actualización de Estado en HubSpot</h4>
                      <p class="text-[11px] text-slate-400 font-mono">Marca el ticket como procesado con trazabilidad de Blue Prism</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">Etapa 4</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 9: CARGA EN HUBSPOT FILES -->
            <div class="flex flex-col items-center">
              <div id="node-upload-file" onclick="inspectStep('upload-file')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-cyan-800/50 hover:border-cyan-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-cloud-arrow-up"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">9. Carga Segura en HubSpot Files</h4>
                      <p class="text-[11px] text-slate-400 font-mono">Almacena el PDF en la carpeta privada /BluePrism para custodia</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-teal-300">Privado</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 10: ENTREGA AL ESTUDIANTE -->
            <div class="flex flex-col items-center">
              <div id="node-conversations" onclick="inspectStep('conversations')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-emerald-700/60 hover:border-emerald-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-paper-plane"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">10. Despacho Digital al Estudiante</h4>
                      <p class="text-[11px] text-slate-400">HubSpot Conversations API: Envía correo personalizado con PDF adjunto</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">Completado</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 11: NOTIFICACIÓN INTERNA -->
            <div class="flex flex-col items-center">
              <div id="node-smtp" onclick="inspectStep('smtp')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-slate-700 hover:border-slate-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-slate-800 text-slate-300 border border-slate-700 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-inbox"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-slate-200 transition">11. Registro y Respaldo Interno</h4>
                      <p class="text-[11px] text-slate-400">Notificación de copia a los buzones de coordinación del CASE</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">Respaldo</span>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- PANEL LATERAL: INSPECTOR TÉCNICO -->
        <div class="lg:col-span-5 xl:col-span-4 space-y-4 sticky top-24">
          
          <div class="bg-slate-900/95 rounded-2xl p-5 border border-slate-800 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span>
                <h3 class="text-sm font-bold text-white">Inspector de Etapa</h3>
              </div>
              <span id="inspectStageCategory" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                Selección activa
              </span>
            </div>

            <div id="stageInspectorContent" class="space-y-3">
              <div>
                <h4 id="inspectStageName" class="text-base font-extrabold text-teal-300">Haga clic en una etapa del diagrama</h4>
                <p id="inspectStageDesc" class="text-xs text-slate-400 mt-1">
                  Seleccione cualquier bloque del flujo o ejecute las simulaciones superiores para conocer los componentes técnicos de Blue Prism y el valor entregado en cada paso.
                </p>
              </div>

              <div id="inspectDetailsBox" class="hidden space-y-2.5 pt-2 border-t border-slate-800/80 text-xs">
                <div>
                  <span class="text-slate-400 block text-[11px] font-semibold uppercase">Componente Blue Prism:</span>
                  <code id="inspectVBO" class="text-teal-300 font-mono text-[11px] bg-slate-950 px-2 py-0.5 rounded block mt-0.5 border border-slate-800"></code>
                </div>

                <div>
                  <span class="text-slate-400 block text-[11px] font-semibold uppercase">Función Operativa:</span>
                  <p id="inspectAction" class="text-slate-200 text-xs mt-0.5"></p>
                </div>

                <div>
                  <span class="text-slate-400 block text-[11px] font-semibold uppercase">Propiedades y Datos Clave:</span>
                  <div id="inspectVariables" class="font-mono text-[11px] text-cyan-300 space-y-0.5 mt-0.5"></div>
                </div>

                <div id="inspectAuditAlert" class="p-3 rounded-xl bg-teal-950/40 border border-teal-800/60 text-xs text-teal-200 space-y-1 mt-2">
                  <div class="flex items-center gap-1.5 font-bold text-teal-300">
                    <i class="fa-solid fa-sparkles"></i>
                    <span>Oportunidad de Evolución:</span>
                  </div>
                  <p id="inspectAuditText" class="text-[11px] text-slate-300 leading-relaxed"></p>
                </div>
              </div>
            </div>

          </div>

          <!-- Cuadro de Valor -->
          <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800 text-xs space-y-2 text-slate-400">
            <h4 class="font-bold text-white flex items-center gap-1.5">
              <i class="fa-solid fa-bolt text-amber-400"></i> Beneficios del Flujo Automatizado
            </h4>
            <p class="leading-relaxed text-[11px]">
              El proceso integra de extremo a extremo el CRM (HubSpot), el sistema de gestión académica (AulaNet), el motor de documentos (Word VBO) y el canal omnicanal de mensajería, reduciendo tiempos de espera de días a solo minutos.
            </p>
          </div>

        </div>

      </div>

    </section>

    <!-- SECCIÓN 5: OPORTUNIDADES DE OPTIMIZACIÓN (TAB 5) -->
    <section id="tab-optimizacion" class="tab-content hidden space-y-6">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-wand-magic-sparkles text-amber-400"></i> Pilares de Optimización y Evolución Tecnológica
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Iniciativas identificadas para llevar la solución actual al siguiente nivel de madurez, seguridad y eficiencia en la infraestructura propia de la universidad.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <!-- Optimización 1 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-center gap-2 mb-2">
            <span class="w-7 h-7 rounded-lg bg-teal-950 text-teal-300 border border-teal-700/60 flex items-center justify-center text-xs font-bold">1</span>
            <h3 class="text-sm font-bold text-white">Sintonía Fina en Excepciones (One-Touch Resolution)</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Actualmente el robot envía un correo informativo cuando faltan datos en el ticket. Como optimización para la versión 2.0, se integrará una llamada de actualización automática de etapa en HubSpot tras el primer aviso, evitando re-notificaciones sucesivas y asegurando un ciclo de atención limpio.
          </p>
          <div class="mt-3 text-[11px] text-teal-400 font-medium flex items-center gap-1.5">
            <i class="fa-solid fa-check"></i> Experiencia de usuario optimizada y libre de reintentos.
          </div>
        </div>

        <!-- Optimización 2 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-center gap-2 mb-2">
            <span class="w-7 h-7 rounded-lg bg-sky-950 text-sky-300 border border-sky-700/60 flex items-center justify-center text-xs font-bold">2</span>
            <h3 class="text-sm font-bold text-white">Migración a Blue Prism Credential Manager</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Aprovechando la migración hacia la infraestructura propia de la universidad, los tokens de HubSpot y credenciales de correo se centralizarán en el gestor nativo de credenciales cifradas de Blue Prism, cumpliendo con los más altos estándares de ciberseguridad institucional.
          </p>
          <div class="mt-3 text-[11px] text-sky-300 font-medium flex items-center gap-1.5">
            <i class="fa-solid fa-shield-check"></i> Cero credenciales expuestas en archivos de configuración.
          </div>
        </div>

        <!-- Optimización 3 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-center gap-2 mb-2">
            <span class="w-7 h-7 rounded-lg bg-indigo-950 text-indigo-300 border border-indigo-700/60 flex items-center justify-center text-xs font-bold">3</span>
            <h3 class="text-sm font-bold text-white">Paginación para Picos de Alta Demanda</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Se implementará el manejo de cursores de paginación (<span class="font-mono text-xs text-indigo-300">after</span>) en las consultas de búsqueda de HubSpot. Esto garantizará que durante las semanas de matrícula o graduaciones el robot procese lotes de más de 100 solicitudes simultáneas con total fluidez.
          </p>
          <div class="mt-3 text-[11px] text-indigo-300 font-medium flex items-center gap-1.5">
            <i class="fa-solid fa-bolt"></i> Escalabilidad preparada para temporadas masivas.
          </div>
        </div>

        <!-- Optimización 4 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex items-center gap-2 mb-2">
            <span class="w-7 h-7 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700/60 flex items-center justify-center text-xs font-bold">4</span>
            <h3 class="text-sm font-bold text-white">Reactivación de Verificación Académica vía VPN</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Con el alojamiento de Blue Prism dentro del entorno tecnológico de la UMB, se habilitará la conectividad directa con el ERP Campus. Esto permitirá reactivar la automatización de Verificación Académica, un trámite de alto valor para convenios e instituciones externas.
          </p>
          <div class="mt-3 text-[11px] text-emerald-400 font-medium flex items-center gap-1.5">
            <i class="fa-solid fa-arrow-trend-up"></i> Ampliación del portafolio de servicios digitales del CASE.
          </div>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 6: CASOS GESTIONADOS (TAB 6) -->
    <section id="tab-tickets" class="tab-content hidden space-y-6">
      
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
            <i class="fa-solid fa-list-check text-cyan-400"></i> Registro de Casos Atendidos (226 Solicitudes Únicas)
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Explore los tickets procesados, consulte el detalle de envíos y revise la trazabilidad horaria de cada estudiante.
          </p>
        </div>

        <div class="relative w-full sm:w-72">
          <input type="text" id="ticketSearch" onkeyup="filterTickets()" placeholder="Buscar por nombre o ticket ID..." 
                 class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 pl-10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 transition">
          <i class="fa-solid fa-search absolute left-3.5 top-3 text-slate-500 text-xs"></i>
        </div>
      </div>

      <!-- Filtros rápidos -->
      <div class="flex flex-wrap items-center gap-2 text-xs font-medium">
        <button onclick="setFilter('all')" id="filter-all" class="filter-btn active-filter px-3 py-1.5 rounded-lg bg-teal-900/40 text-teal-300 border border-teal-700/60">
          Todos los Casos (226)
        </button>
        <button onclick="setFilter('single')" id="filter-single" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Atención Directa (154)
        </button>
        <button onclick="setFilter('reprocessed')" id="filter-reprocessed" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Seguimiento Continuo (72)
        </button>
        <button onclick="setFilter('horarios')" id="filter-horarios" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Certificado de Horarios (6)
        </button>
      </div>

      <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
        <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="sticky top-0 z-10 bg-slate-950 text-slate-400 font-semibold uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th class="p-3">Ticket ID</th>
                <th class="p-3">Estudiante</th>
                <th class="p-3">Trámite</th>
                <th class="p-3 text-center">Atenciones</th>
                <th class="p-3">Primer Envío (UTC)</th>
                <th class="p-3">Último Envío (UTC)</th>
                <th class="p-3 text-center">Estatus</th>
                <th class="p-3 text-center">Detalle</th>
              </tr>
            </thead>
            <tbody id="ticketsTableBody" class="divide-y divide-slate-800/60 font-mono">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- SECCIÓN 7: HOJA DE RUTA & EXPANSIÓN (TAB 7) -->
    <section id="tab-roadmap" class="tab-content hidden space-y-8">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-rocket text-indigo-400"></i> Plan Estratégico de Migración y Expansión
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Hoja de ruta coordinada entre NBI y la UMB para consolidar la infraestructura propia e incorporar nuevos trámites de alto impacto.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        <!-- Fase 1 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-teal-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-teal-900 text-teal-300 font-bold flex items-center justify-center text-sm mb-3">
            1
          </div>
          <span class="text-xs font-bold text-teal-400 uppercase tracking-wider">Inmediato</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Optimización de Experiencia</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-teal-400 mt-0.5"></i>
              <span>Ajuste en la gestión de excepciones para cerrar tickets al primer aviso informativo.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-teal-400 mt-0.5"></i>
              <span>Alineación de plantillas de correo en Horarios.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Foco: <strong>Sintonía Fina</strong>
          </div>
        </div>

        <!-- Fase 2 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-sky-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-sky-900 text-sky-300 font-bold flex items-center justify-center text-sm mb-3">
            2
          </div>
          <span class="text-xs font-bold text-sky-400 uppercase tracking-wider">Próximos Pasos</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Migración a Infraestructura UMB</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-sky-400 mt-0.5"></i>
              <span>Despliegue de Blue Prism en servidores propios de la universidad.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-sky-400 mt-0.5"></i>
              <span>Configuración de Credential Manager con bóvedas institucionales.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Foco: <strong>Soberanía Tecnológica UMB</strong>
          </div>
        </div>

        <!-- Fase 3 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-indigo-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-indigo-900 text-indigo-300 font-bold flex items-center justify-center text-sm mb-3">
            3
          </div>
          <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">Mediano Plazo</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Reactivación de Campus</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-indigo-400 mt-0.5"></i>
              <span>Conexión directa interna con el ERP Campus para Verificación Académica.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-indigo-400 mt-0.5"></i>
              <span>Levantamiento de nuevos trámites prioritarios del CASE.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Foco: <strong>Crecimiento de Portafolio</strong>
          </div>
        </div>

        <!-- Fase 4 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-emerald-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-emerald-900 text-emerald-300 font-bold flex items-center justify-center text-sm mb-3">
            4
          </div>
          <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Innovación</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Links de Pago & WorkHQ</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
              <span>Evaluación de Blue Prism WorkHQ articulado con la nueva pasarela de pagos.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
              <span>Generación de links de recaudo para trámites con costo asociado.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Foco: <strong>Transformación Digital Avanzada</strong>
          </div>
        </div>

      </div>

      <!-- Agenda de Trabajo -->
      <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
        <h3 class="text-base font-bold text-white flex items-center gap-2 mb-3">
          <i class="fa-solid fa-handshake text-teal-400"></i> Plan de Articulación con la Dirección de Tecnología
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h4 class="font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-server text-teal-400"></i> 1. Migración de Infraestructura
            </h4>
            <p class="leading-relaxed">
              Coordinar la habilitación del ambiente propio de Blue Prism según los requerimientos técnicos ya remitidos por NBI, asegurando la continuidad del servicio.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h4 class="font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-list-ol text-sky-400"></i> 2. Levantamiento con CASE
            </h4>
            <p class="leading-relaxed">
              Reunión programada con la Coordinación del CASE para identificar nuevas oportunidades de automatización que potencien la atención estudiantil.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h4 class="font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-credit-card text-emerald-400"></i> 3. Pasarela de Pagos (WorkHQ)
            </h4>
            <p class="leading-relaxed">
              Evaluar la viabilidad técnica para la creación y gestión de links de pago automáticos mediante Blue Prism WorkHQ en beneficio de la tesorería de la UMB.
            </p>
          </div>
        </div>
      </div>

    </section>

  </main>

  <!-- MODAL DE TRAZABILIDAD -->
  <div id="ticketModal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] flex flex-col">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
        <div>
          <span class="text-xs font-mono text-slate-400">Historial de Atención Digital</span>
          <h3 id="modalStudent" class="text-lg font-bold text-white flex items-center gap-2"></h3>
          <span id="modalTicketId" class="text-xs font-mono text-teal-400"></span>
        </div>
        <button onclick="closeModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="overflow-y-auto flex-1 pr-2 space-y-3" id="modalEventsList"></div>

      <div class="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs">
        <span id="modalSummary" class="text-slate-400"></span>
        <button onclick="closeModal()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition">
          Cerrar
        </button>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="border-t border-slate-850 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <span>Dashboard de Gestión RPA &bull; Universidad Manuela Beltrán &copy; 2026</span>
      <span>Desarrollado sobre <strong>SS&C Blue Prism 7.2</strong> &bull; Narnaja Business Intelligence</span>
    </div>
  </footer>

  <!-- SCRIPT DE DATOS Y LÓGICA -->
  <script>
    // Embedded Data from Python Parser
    const rawData = __DATA_JSON__;

    let currentFilter = 'all';
    let currentProcessFlow = 'p1';
    let activeSimulationTimer = null;

    const stageCatalog = {
      'start': {
        name: '1. Inicio & Scheduler Blue Prism',
        category: 'Scheduler / Orquestación',
        vbo: 'Blue Prism Scheduler Service',
        action: 'Disparo recurrente cada 2 horas (08:00, 10:00, 12:00, 14:00, 16:00, 18:00)',
        vars: ['Ventana operativa: 8:00 a.m. a 6:00 p.m.', 'Días: Lunes a Sábado', 'Servidor: GCP VM (NBI)'],
        audit: 'Garantiza atención constante y predecible a lo largo de toda la jornada universitaria.'
      },
      'search': {
        name: '2. Consulta de Tickets en HubSpot',
        category: 'Integración CRM / Carga de Cola',
        vbo: 'Utility - HTTP::HTTP Request',
        action: 'POST https://api.hubapi.com/crm/objects/2026-03/tickets/search',
        vars: ['filterGroups: tramite EQ [Trámite]', 'hs_pipeline_stage EQ "1" y "2" (combinados)', 'limit: 100'],
        audit: 'Captura automática de solicitudes en estado inicial para su inmediata tramitación.'
      },
      'encargado': {
        name: '3. Validación de Encargado de Insumo',
        category: 'Regla de Decisión',
        vbo: 'Decision Stage',
        action: 'Evalúa si la propiedad encargado_del_insumo_del_tramite está vacía',
        vars: ['True: Procesa automáticamente con Blue Prism', 'False: Respeta la gestión manual del funcionario'],
        audit: 'Mecanismo de coexistencia armónica entre el equipo humano del CASE y el robot.'
      },
      'aulanet-login': {
        name: '4. Conexión Segura con AulaNet',
        category: 'Automatización UI Web',
        vbo: 'Crome - AulaNET::Attach / Login',
        action: 'Apertura de sesión automatizada en la plataforma académica AulaNet',
        vars: ['Navegador: Google Chrome', 'Target: Portal AulaNet UMB'],
        audit: 'Interacción ágil con la interfaz institucional sin requerir APIs propietarias adicionales.'
      },
      'consulta': {
        name: '5. Consulta de Historial Académico',
        category: 'Consulta Académica',
        vbo: 'Crome - AulaNET::Consulta Estudiante',
        action: 'Búsqueda por cédula del estudiante y recuperación del historial académico',
        vars: ['Input: Cédula / NIT', 'Output: Colección Tabla (Asignatura, Estado, Periodo)'],
        audit: 'Verificación directa en la fuente oficial de verdad de la universidad.'
      },
      'error-loop': {
        name: 'Ruta de Orientación al Estudiante',
        category: 'Servicio al Estudiante',
        vbo: 'Email - POP3/SMTP::Send Message',
        action: 'Envío de correo informativo explicando los requisitos faltantes',
        vars: ['Destinatario: Correo del solicitante y copia a CASE', 'Objetivo: Orientar para generar solicitud correcta'],
        audit: 'Oportunidad de optimización: En la versión 2.0 se cerrará el ticket en HubSpot tras este envío para evitar re-notificaciones.'
      },
      'matricula': {
        name: '6. Validación de Estado del Estudiante',
        category: 'Regla de Negocio Académica',
        vbo: 'Decision Stage (Tabla.Estado = "Matriculado")',
        action: 'Evalúa si el estudiante se encuentra matriculado o admitido',
        vars: ['True: Certificado de Estudios AulaNet', 'False: Certificado de Admisión Word'],
        audit: 'Permite resolver ágilmente dos perfiles de estudiante en un mismo flujo inteligente.'
      },
      'gen-aulanet': {
        name: '7A. Generación en AulaNet',
        category: 'Generación Oficial de Documento',
        vbo: 'Crome - AulaNET::Generar Certificado',
        action: 'Descarga del certificado oficial con firma y códigos institucionales',
        vars: ['Cédula: Identificación del estudiante', 'Período: Último período académico registrado'],
        audit: 'Emisión 100% digital del documento oficial con validez institucional.'
      },
      'gen-word': {
        name: '7B. Generación de Admisión en Word',
        category: 'Generación Asistida por Plantilla',
        vbo: 'MS Word VBO::Open / Find Text / Type Text / ExportPDF',
        action: 'Confección de carta de admisión personalizada con diseño institucional',
        vars: ['Plantilla: C:\\\\UMB\\\\Templates\\\\PLANTILLA ADMITIDO WORD.docx', 'Campos: Nombre, ID, Programa'],
        audit: 'Solución flexible que brinda respuesta oficial a estudiantes en proceso de ingreso.'
      },
      'update-ticket': {
        name: '8. Actualización de Estado en HubSpot',
        category: 'Actualización CRM',
        vbo: 'Utility - HTTP::HTTP Request (PATCH)',
        action: 'Marca el ticket en etapa 4 y registra la trazabilidad del procesamiento',
        vars: ['hs_pipeline_stage: "4"', 'respuesta_o_correo_de_cierre: "Procesado por Blue Prism"'],
        audit: 'Mantiene el CRM siempre al día para los tableros de control del CASE.'
      },
      'upload-file': {
        name: '9. Carga Segura en HubSpot Files',
        category: 'Custodia Digital',
        vbo: 'Utility - HTTP::HTTP Request Multipart',
        action: 'Almacena el PDF en la carpeta privada /BluePrism de HubSpot',
        vars: ['Carpeta: /BluePrism', 'Acceso: PRIVATE', 'Output: fileId'],
        audit: 'Custodia segura y centralizada del documento antes de su notificación.'
      },
      'conversations': {
        name: '10. Despacho Digital al Estudiante',
        category: 'Entrega Omnicanal',
        vbo: 'Utility - HTTP::HTTP Request (POST)',
        action: 'Envío de respuesta personalizada con el PDF adjunto al correo del estudiante',
        vars: ['Conversations API', 'Attachment: fileId de HubSpot Files'],
        audit: 'Cierre exitoso del trámite con entrega inmediata y personalizada.'
      },
      'smtp': {
        name: '11. Notificación y Respaldo a CASE',
        category: 'Auditoría Interna',
        vbo: 'Email - POP3/SMTP::Send Message',
        action: 'Envío de confirmación interna a los buzones directivos del CASE',
        vars: ['To: cesar.plata@umb.edu.co, coord.case@umb.edu.co', 'Copia de respaldo del certificado'],
        audit: 'Transparencia y control total para el equipo de supervisión del CASE.'
      }
    };

    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-tab').forEach(el => {
        el.classList.remove('bg-teal-900/40', 'text-teal-300', 'border-teal-700/50', 'active-tab');
        el.classList.add('text-slate-400', 'border-transparent');
      });

      document.getElementById(tabId).classList.remove('hidden');
      const btn = document.getElementById('btn-' + tabId);
      if (btn) {
        btn.classList.add('bg-teal-900/40', 'text-teal-300', 'border-teal-700/50', 'active-tab');
        btn.classList.remove('text-slate-400', 'border-transparent');
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      initCharts();
      renderTicketsTable();
    });

    function initCharts() {
      // 1. Chart Eficiencia (Donut)
      const ctxEficiencia = document.getElementById('chartEficiencia').getContext('2d');
      new Chart(ctxEficiencia, {
        type: 'doughnut',
        data: {
          labels: ['Atención Directa (1 ciclo)', 'Seguimiento Activo (>1)'],
          datasets: [{
            data: [154, 72],
            backgroundColor: ['#10B981', '#0EA5E9'],
            borderWidth: 2,
            borderColor: '#0f172a'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: '#94a3b8', font: { size: 11, family: 'Plus Jakarta Sans' } }
            }
          },
          cutout: '72%'
        }
      });

      // 2. Chart Timeline Diaria
      const ctxTimeline = document.getElementById('chartTimeline').getContext('2d');
      const dates = rawData.date_distribution.map(d => d[0].substring(5));
      const counts = rawData.date_distribution.map(d => d[1]);
      const barColors = rawData.date_distribution.map(d => d[0].startsWith('2026-07') ? 'rgba(100, 116, 139, 0.7)' : 'rgba(13, 148, 136, 0.85)');

      new Chart(ctxTimeline, {
        type: 'bar',
        data: {
          labels: dates,
          datasets: [{
            label: 'Gestiones Realizadas',
            data: counts,
            backgroundColor: barColors,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: (items) => 'Fecha: 2026-' + items[0].label,
                label: (item) => 'Atenciones: ' + item.raw + (item.label.startsWith('07') ? ' (Fase Validación)' : ' (Operación Productiva)')
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 10 } } },
            y: { grid: { color: '#1e293b' }, ticks: { color: '#64748b', font: { size: 10 } }, beginAtZero: true }
          }
        }
      });

      // 3. Chart Trámites (Pie)
      const ctxTramites = document.getElementById('chartTramites').getContext('2d');
      new Chart(ctxTramites, {
        type: 'doughnut',
        data: {
          labels: ['Certificado de Estudios (220)', 'Certificado de Horarios (6)'],
          datasets: [{
            data: [220, 6],
            backgroundColor: ['#0D9488', '#0EA5E9'],
            borderWidth: 2,
            borderColor: '#0f172a'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: '#94a3b8', font: { size: 11, family: 'Plus Jakarta Sans' } }
            }
          },
          cutout: '68%'
        }
      });

      // 4. Chart Horas UTC
      const ctxHoras = document.getElementById('chartHoras').getContext('2d');
      const hours = rawData.hour_distribution.map(h => h[0] + ':00 UTC');
      const hourCounts = rawData.hour_distribution.map(h => h[1]);

      new Chart(ctxHoras, {
        type: 'line',
        data: {
          labels: hours,
          datasets: [{
            label: 'Atenciones por Franja Horaria (UTC)',
            data: hourCounts,
            borderColor: '#0EA5E9',
            backgroundColor: 'rgba(14, 165, 233, 0.15)',
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#0EA5E9',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 10 } } },
            y: { grid: { color: '#1e293b' }, ticks: { color: '#64748b', font: { size: 10 } }, beginAtZero: true }
          }
        }
      });

      // 5. Chart Reprocesos (Histogram)
      const ctxRepro = document.getElementById('chartReprocesos').getContext('2d');
      const reprocessLabels = rawData.reprocess_distribution.map(r => r[0] + (r[0] === 1 ? ' ciclo' : ' ciclos'));
      const reprocessCounts = rawData.reprocess_distribution.map(r => r[1]);

      new Chart(ctxRepro, {
        type: 'bar',
        data: {
          labels: reprocessLabels,
          datasets: [{
            label: 'Cantidad de Casos',
            data: reprocessCounts,
            backgroundColor: ['#10B981', '#0EA5E9', '#0284C7', '#6366F1', '#8B5CF6', '#A855F7', '#D946EF', '#EC4899', '#F43F5E'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 10 } } },
            y: { grid: { color: '#1e293b' }, ticks: { color: '#64748b', font: { size: 10 } }, beginAtZero: true }
          }
        }
      });
    }

    function selectProcessFlow(proc) {
      currentProcessFlow = proc;
      resetSimulation();

      const btnP1 = document.getElementById('btn-flow-p1');
      const btnP2 = document.getElementById('btn-flow-p2');
      const banner = document.getElementById('flowProcessBanner');
      const searchFilter = document.getElementById('searchStepFilterText');
      const aulanetTitle = document.getElementById('genAulanetTitle');
      const wordTitle = document.getElementById('genWordTitle');
      const wordSubtitle = document.getElementById('genWordSubtitle');

      if (proc === 'p1') {
        btnP1.className = 'flow-proc-btn px-3 py-1.5 rounded-lg bg-teal-950 text-teal-300 border border-teal-700/60 font-semibold text-xs transition flex items-center gap-1.5';
        btnP2.className = 'flow-proc-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium text-xs transition flex items-center gap-1.5 ml-1';
        banner.innerHTML = `<span class="w-3 h-3 rounded-full bg-teal-400"></span><strong class="text-sm text-white">Proceso 01 - Certificados de Estudios / Admisión</strong> <span class="text-[11px] text-slate-400 font-mono">(tramite = 'Certificado de Estudio')</span>`;
        searchFilter.innerText = 'Filtro: tramite = "Certificado de Estudio" & stage IN (1, 2)';
        aulanetTitle.innerText = '7A. Certificado de Estudios (AulaNet)';
        wordTitle.innerText = '7B. Certificado de Admisión (Word)';
        wordSubtitle.innerText = 'Confección automática de carta personalizada con plantilla institucional de Word.';
        inspectStep('search');
      } else {
        btnP2.className = 'flow-proc-btn px-3 py-1.5 rounded-lg bg-sky-950 text-sky-300 border border-sky-700/60 font-semibold text-xs transition flex items-center gap-1.5 ml-1';
        btnP1.className = 'flow-proc-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium text-xs transition flex items-center gap-1.5';
        banner.innerHTML = `<span class="w-3 h-3 rounded-full bg-sky-400"></span><strong class="text-sm text-white">Proceso 02 - Certificado de Horarios</strong> <span class="text-[11px] text-slate-400 font-mono">(tramite = 'Certificado de Horarios')</span>`;
        searchFilter.innerText = 'Filtro: tramite = "Certificado de Horarios" & stage IN (1, 2)';
        aulanetTitle.innerText = '7A. Certificado de Horarios (AulaNet)';
        wordTitle.innerText = '7B. Rama Complementaria de Admisión';
        wordSubtitle.innerText = 'Atención adaptativa para estudiantes no matriculados.';
        inspectStep('gen-aulanet');
      }
    }

    function inspectStep(stepId) {
      const data = stageCatalog[stepId];
      if (!data) return;

      document.getElementById('inspectStageCategory').innerText = data.category;
      document.getElementById('inspectStageName').innerText = data.name;
      document.getElementById('inspectStageDesc').innerText = data.action;
      document.getElementById('inspectVBO').innerText = data.vbo;
      document.getElementById('inspectAction').innerText = data.action;

      const varsList = document.getElementById('inspectVariables');
      varsList.innerHTML = '';
      data.vars.forEach(v => {
        const item = document.createElement('div');
        item.innerText = '• ' + v;
        varsList.appendChild(item);
      });

      document.getElementById('inspectAuditText').innerText = data.audit;
      document.getElementById('inspectDetailsBox').classList.remove('hidden');

      document.querySelectorAll('.flow-node').forEach(node => {
        node.classList.remove('ring-2', 'ring-teal-400', 'ring-sky-400', 'ring-emerald-400', 'bg-slate-900');
      });
      const activeNode = document.getElementById('node-' + stepId);
      if (activeNode) {
        activeNode.classList.add('ring-2', 'ring-teal-400', 'bg-slate-900');
      }
    }

    function runSimulation(scenario) {
      resetSimulation();
      const badge = document.getElementById('simStatusBadge');
      let steps = [];

      if (scenario === 'success') {
        badge.innerHTML = `<span class="relative flex h-2 w-2 mr-1"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span></span> Simulando: Caso Éxito (Estudiante Matriculado)...`;
        badge.className = 'text-xs px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-700 font-mono flex items-center';
        steps = ['start', 'search', 'encargado', 'aulanet-login', 'consulta', 'matricula', 'gen-aulanet', 'update-ticket', 'upload-file', 'conversations', 'smtp'];
      } else if (scenario === 'admission') {
        badge.innerHTML = `<span class="relative flex h-2 w-2 mr-1"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span></span> Simulando: Flujo Alternativo (Admisión Word)...`;
        badge.className = 'text-xs px-3 py-1 rounded-full bg-indigo-950 text-indigo-300 border border-indigo-700 font-mono flex items-center';
        steps = ['start', 'search', 'encargado', 'aulanet-login', 'consulta', 'matricula', 'gen-word', 'update-ticket', 'upload-file', 'conversations', 'smtp'];
      } else if (scenario === 'loop') {
        badge.innerHTML = `<span class="relative flex h-2 w-2 mr-1"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span></span> Simulando: Orientación al Solicitante...`;
        badge.className = 'text-xs px-3 py-1 rounded-full bg-amber-950 text-amber-300 border border-amber-700 font-mono flex items-center';
        steps = ['start', 'search', 'encargado', 'aulanet-login', 'error-loop', 'search'];
      }

      let currentStepIdx = 0;
      activeSimulationTimer = setInterval(() => {
        if (currentStepIdx >= steps.length) {
          clearInterval(activeSimulationTimer);
          badge.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400 mr-1"></i> Simulación finalizada exitosamente`;
          return;
        }
        const step = steps[currentStepIdx];
        inspectStep(step);
        currentStepIdx++;
      }, 1200);
    }

    function resetSimulation() {
      if (activeSimulationTimer) {
        clearInterval(activeSimulationTimer);
        activeSimulationTimer = null;
      }
      document.querySelectorAll('.flow-node').forEach(node => {
        node.classList.remove('ring-2', 'ring-teal-400', 'ring-sky-400', 'ring-emerald-400', 'bg-slate-900');
      });
      document.getElementById('simStatusBadge').innerHTML = `<i class="fa-solid fa-circle-info text-teal-400 mr-1"></i> Modo interactivo: Haga clic en cualquier etapa`;
      document.getElementById('simStatusBadge').className = 'text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-mono flex items-center';
    }

    // Render Full Tickets Explorer
    function renderTicketsTable() {
      const tbody = document.getElementById('ticketsTableBody');
      const query = document.getElementById('ticketSearch').value.toLowerCase();
      tbody.innerHTML = '';

      let filtered = rawData.tickets.filter(t => {
        const matchSearch = t.ticket.toLowerCase().includes(query) || t.student.toLowerCase().includes(query);
        if (!matchSearch) return false;
        if (currentFilter === 'reprocessed') return t.sends > 1;
        if (currentFilter === 'single') return t.sends === 1;
        if (currentFilter === 'horarios') return t.type === 'Horarios';
        return true;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="p-8 text-center text-slate-500 font-sans">No se encontraron tickets con ese criterio.</td></tr>';
        return;
      }

      filtered.forEach(t => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/30 transition border-b border-slate-800/40 text-[11px]';
        
        const isFollowup = t.sends > 1;
        const statusBadge = isFollowup 
          ? `<span class="px-2 py-0.5 rounded-full bg-sky-950 text-sky-300 border border-sky-800 text-[10px] font-bold">SEGUIMIENTO (${t.sends})</span>`
          : `<span class="px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 text-[10px] font-bold">ATENDIDO (1)</span>`;

        tr.innerHTML = `
          <td class="p-3 text-teal-300 font-semibold">${t.ticket}</td>
          <td class="p-3 font-sans font-medium text-slate-200">${t.student}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">${t.type}</span></td>
          <td class="p-3 text-center font-bold ${t.sends > 1 ? 'text-sky-300' : 'text-slate-400'}">${t.sends}</td>
          <td class="p-3 text-slate-400">${t.first_send.substring(0, 16)}</td>
          <td class="p-3 text-slate-400">${t.last_send.substring(0, 16)}</td>
          <td class="p-3 text-center">${statusBadge}</td>
          <td class="p-3 text-center">
            <button onclick="openTicketModal('${t.ticket}')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-sans hover:text-white transition">
              Ver
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function setFilter(type) {
      currentFilter = type;
      document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('bg-teal-900/40', 'text-teal-300', 'border-teal-700/60');
        btn.classList.add('bg-slate-900', 'text-slate-400', 'border-slate-800');
      });
      document.getElementById('filter-' + type).classList.remove('bg-slate-900', 'text-slate-400', 'border-slate-800');
      document.getElementById('filter-' + type).classList.add('bg-teal-900/40', 'text-teal-300', 'border-teal-700/60');
      renderTicketsTable();
    }

    function filterTickets() {
      renderTicketsTable();
    }

    function openTicketModal(ticketId) {
      const ticket = rawData.tickets.find(t => t.ticket === ticketId);
      if (!ticket) return;

      const events = rawData.events.filter(e => e.ticket === ticketId);

      document.getElementById('modalStudent').innerText = ticket.student;
      document.getElementById('modalTicketId').innerText = `Ticket #${ticket.ticket} (${ticket.type})`;
      document.getElementById('modalSummary').innerText = `Total de interacciones registradas: ${events.length}`;

      const list = document.getElementById('modalEventsList');
      list.innerHTML = '';

      events.forEach((ev, idx) => {
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono';
        
        let intervalText = '';
        if (idx > 0) {
          const prev = new Date(events[idx-1].timestamp);
          const curr = new Date(ev.timestamp);
          const diffMinutes = Math.round((curr - prev) / (1000 * 60));
          intervalText = `&Delta; +${Math.floor(diffMinutes / 60)}h ${diffMinutes % 60}m`;
        } else {
          intervalText = 'Primer contacto';
        }

        item.innerHTML = `
          <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full bg-teal-950 text-teal-300 border border-teal-800 flex items-center justify-center font-bold text-[11px]">${idx + 1}</span>
            <div>
              <span class="text-white font-medium">${ev.timestamp} UTC</span>
              <span class="text-[10px] text-slate-500 block">Notificación de Trámite - CASE UMB</span>
            </div>
          </div>
          <span class="text-teal-400 text-xs font-semibold">${intervalText}</span>
        `;
        list.appendChild(item);
      });

      document.getElementById('ticketModal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('ticketModal').classList.add('hidden');
    }

    function exportDataCSV() {
      let csv = 'Ticket,Estudiante,Tipo de Certificado,# de Envios,Primer Envio (UTC),Ultimo Envio (UTC),Reprocesado\\n';
      rawData.tickets.forEach(t => {
        csv += `"${t.ticket}","${t.student}","${t.type}",${t.sends},"${t.first_send}","${t.last_send}","${t.reprocessed}"\\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Gestion_Tramites_RPA_UMB.csv';
      a.click();
    }
  </script>
</body>
</html>
"""

# Write to template.html
with open('/Users/franciscomateus/Documents/DashboardUMB/template.html', 'w', encoding='utf-8') as f:
    f.write(positive_template)

# Compile index.html
html_final = positive_template.replace('__DATA_JSON__', json.dumps(data))
with open('/Users/franciscomateus/Documents/DashboardUMB/index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("Positive Dashboard template and index.html generated successfully!")
