import json

# Load metrics
with open('/Users/franciscomateus/Documents/DashboardUMB/processed_metrics.json') as f:
    data = json.load(f)

# Let's create the comprehensive HTML dashboard
html_template = '''<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-900 text-slate-100">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Ejecutivo UMB - Auditoría RPA Blue Prism (CASE)</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Font Awesome CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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
            umb: {
              red: '#B91C1C',
              darkRed: '#7F1D1D',
              gold: '#F59E0B',
              navy: '#0F172A',
              card: '#1E293B',
              border: '#334155'
            }
          }
        }
      }
    }
  </script>
  <style>
    /* Custom scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #475569;
    }
    .badge-glow {
      box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
    }
    .badge-glow-amber {
      box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .badge-glow-blue {
      box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
    }
  </style>
</head>
<body class="min-h-screen bg-slate-950 font-sans antialiased text-slate-200">

  <!-- HEADER SUPREMO EJECUTIVO -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-red-600 via-rose-700 to-red-900 flex items-center justify-center shadow-lg shadow-red-950/50 border border-red-500/30">
            <i class="fa-solid fa-graduation-cap text-2xl text-white"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold tracking-wider uppercase px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800/60">
                Auditoría Forense RPA
              </span>
              <span class="text-xs font-semibold px-2 py-0.5 rounded bg-amber-950/70 text-amber-300 border border-amber-800/40">
                SS&C Blue Prism 7.2
              </span>
            </div>
            <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
              Universidad Manuela Beltrán <span class="text-slate-500 font-light text-base">| Trámites CASE</span>
            </h1>
            <p class="text-xs text-slate-400">
              Contraste Ejecutivo: <strong class="text-slate-200">Status Report NBI</strong> vs. <strong class="text-rose-400">Realidad Técnica y Operativa</strong> (Telemetría de 414 envíos y 226 tickets)
            </p>
          </div>
        </div>

        <!-- Acciones rápidas & Estado del Sistema -->
        <div class="flex flex-wrap items-center gap-2">
          <div class="flex items-center gap-2 bg-slate-800/90 border border-slate-700/80 px-3 py-1.5 rounded-lg text-xs">
            <span class="relative flex h-2.5 w-2.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
            </span>
            <span class="font-medium text-slate-300">Diagnóstico: <strong class="text-rose-400 font-bold">Riesgo Operativo Crítico</strong></span>
          </div>

          <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition flex items-center gap-1.5">
            <i class="fa-solid fa-print"></i> Imprimir / PDF
          </button>
          
          <button onclick="exportDataCSV()" class="px-3 py-1.5 rounded-lg bg-red-700 hover:bg-red-600 text-white text-xs font-semibold shadow-md shadow-red-950 transition flex items-center gap-1.5">
            <i class="fa-solid fa-download"></i> Exportar Auditoría (.CSV)
          </button>
        </div>

      </div>

      <!-- Pestañas de Navegación -->
      <nav class="flex space-x-1 sm:space-x-2 border-t border-slate-800/80 mt-4 pt-3 overflow-x-auto text-xs sm:text-sm font-medium">
        <button onclick="switchTab('tab-resumen')" id="btn-tab-resumen" class="nav-tab active-tab px-3 py-1.5 rounded-lg bg-red-900/40 text-red-300 border border-red-700/50 flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-chart-pie"></i> Resumen Ejecutivo & KPIs
        </button>
        <button onclick="switchTab('tab-espejo')" id="btn-tab-espejo" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-scale-unbalanced text-amber-400"></i> Relato Oficial vs. Realidad
        </button>
        <button onclick="switchTab('tab-telemetria')" id="btn-tab-telemetria" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-chart-line text-blue-400"></i> Telemetría & Gráficos
        </button>
        <button onclick="switchTab('tab-codigo')" id="btn-tab-codigo" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-code text-purple-400"></i> Auditoría Código Blue Prism
        </button>
        <button onclick="switchTab('tab-tickets')" id="btn-tab-tickets" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-list-check text-emerald-400"></i> Explorador de Tickets (226)
        </button>
        <button onclick="switchTab('tab-roadmap')" id="btn-tab-roadmap" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-route text-sky-400"></i> Plan de Remediación
        </button>
      </nav>
    </div>
  </header>

  <!-- CONTENEDOR PRINCIPAL -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- ALERTA EJECUTIVA PRINCIPAL (CALLOUT) -->
    <div class="mb-8 rounded-2xl bg-gradient-to-r from-red-950/60 via-slate-900 to-slate-900 border border-red-800/40 p-5 shadow-2xl relative overflow-hidden">
      <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-red-600/10 rounded-full blur-2xl pointer-events-none"></div>
      <div class="flex items-start gap-4">
        <div class="p-3 rounded-xl bg-red-900/60 text-red-300 border border-red-700/50 mt-1">
          <i class="fa-solid fa-triangle-exclamation text-2xl"></i>
        </div>
        <div class="flex-1">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h2 class="text-lg font-bold text-white">Alerta de Gobierno TI: Discrepancia Crítica entre Reporte y Operación Real</h2>
            <span class="text-xs bg-red-900 text-red-200 font-bold px-2.5 py-0.5 rounded-full border border-red-700">Severidad: Alta</span>
          </div>
          <p class="text-sm text-slate-300 mt-1 leading-relaxed">
            Mientras el reporte de estatus emitido por NBI presenta una solución en producción automática para 3 trámites desde septiembre, la auditoría forense del código <span class="font-mono text-red-400 text-xs">.bpprocess</span> y el análisis de los 414 envíos revelan que:
            <strong class="text-white">el 45.4% de los correos enviados son duplicados redundantes generados por un bucle infinito</strong> (el robot no cierra ni actualiza tickets al toparse con excepciones),
            <strong class="text-white">"Certificado de Admisión" no existe como proceso Blue Prism</strong> (es una plantilla Word local reutilizada), 
            <strong class="text-white">Certificado de Horarios generó certificados de admisión por error</strong> al copiar código de Estudios, y
            <strong class="text-white">claves privadas y tokens de HubSpot se encuentran expuestos en texto plano</strong>.
          </p>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 1: RESUMEN EJECUTIVO Y KPIS (TAB 1) -->
    <section id="tab-resumen" class="tab-content space-y-8">
      
      <!-- GRID DE KPIS COMPARATIVOS -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- KPI 1: Envíos Totales vs Tickets Reales -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition relative">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Volumen de Envíos</span>
            <i class="fa-solid fa-envelope-open-text text-slate-500"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-white">414</span>
            <span class="text-xs text-rose-400 font-semibold">(226 tickets únicos)</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Inflación por bucle:</span>
            <span class="font-bold text-rose-400">+83.2% sobrecupo</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">188 correos fueron reenvíos redundantes al mismo estudiante.</p>
        </div>

        <!-- KPI 2: Tasa de Reprocesamiento / Loop -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition relative">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Tasa de Reproceso</span>
            <i class="fa-solid fa-arrows-spin text-amber-500"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-amber-400">31.9%</span>
            <span class="text-xs text-slate-400">(72 tickets afectados)</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Máximo reenvío a 1 ticket:</span>
            <span class="font-bold text-rose-400 font-mono">15 envíos (2 casos)</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Estudiantes recibieron hasta 15 respuestas idénticas cada 2 horas.</p>
        </div>

        <!-- KPI 3: Procesos Reales vs Prometidos -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition relative">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Procesos en Blue Prism</span>
            <i class="fa-solid fa-robot text-purple-400"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-purple-300">2 <span class="text-lg font-normal text-slate-500">de 3 reportados</span></span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Admisión independiente:</span>
            <span class="font-bold text-rose-400">INEXISTENTE (Macro Word)</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Verificación Académica cancelada por falta de VPN site-to-site.</p>
        </div>

        <!-- KPI 4: Desbalance de Demanda -->
        <div class="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition relative">
          <div class="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Concentración Trámite</span>
            <i class="fa-solid fa-chart-column text-sky-400"></i>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-extrabold text-sky-300">97.3%</span>
            <span class="text-xs text-slate-400">Estudios (220 tickets)</span>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
            <span class="text-slate-400">Certificados de Horarios:</span>
            <span class="font-bold text-amber-400">Solo 6 tickets (2.7%)</span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">El proceso de Horarios no tiene tracción ni validación aprobada.</p>
        </div>

      </div>

      <!-- DOS COLUMNAS: ANÁLISIS DE EFICIENCIA Y HALLAZGOS ESTRUCTURALES -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Columna Izquierda: Gráfico Donut de Eficiencia -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-pie-chart text-red-500"></i> Eficiencia Real de Envíos
              </h3>
              <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">414 Envíos</span>
            </div>
            <p class="text-xs text-slate-400 mb-4">
              Relación entre respuestas únicas a solicitudes versus re-ejecuciones redundantes enviadas por el loop de excepción.
            </p>
            <div class="relative h-56 flex items-center justify-center">
              <canvas id="chartEficiencia"></canvas>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-slate-800 grid grid-cols-2 gap-3 text-xs">
            <div class="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50">
              <span class="text-slate-400 block">Envíos Útiles</span>
              <strong class="text-base text-emerald-400 font-mono">226 (54.6%)</strong>
              <span class="text-[10px] text-slate-500 block mt-0.5">1 respuesta por ticket</span>
            </div>
            <div class="p-3 rounded-xl bg-red-950/40 border border-red-800/50">
              <span class="text-red-300 block">Duplicados / Spam</span>
              <strong class="text-base text-rose-400 font-mono">188 (45.4%)</strong>
              <span class="text-[10px] text-red-400/80 block mt-0.5">Reenvíos cíclicos</span>
            </div>
          </div>
        </div>

        <!-- Columna Central/Derecha: Los 4 Hallazgos de Impacto Inmediato -->
        <div class="lg:col-span-2 bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-shield-virus text-amber-500"></i> Síntesis Ejecutiva de Riesgos y Deuda Técnica
            </h3>
            <span class="text-xs px-2.5 py-1 rounded-full bg-red-950 text-red-400 font-bold border border-red-800">
              4 Riesgos Críticos
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <!-- Riesgo 1 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-red-900/40 hover:border-red-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-red-900/80 text-red-300 flex items-center justify-center text-xs font-bold">1</span>
                <h4 class="text-sm font-bold text-red-300">Bucle Infinito de Notificación</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                Cuando una solicitud tiene cédula vacía o no tiene notas en AulaNet, el proceso envía correo pero <strong class="text-white">omite actualizar la propiedad <span class="font-mono text-amber-300">hs_pipeline_stage</span></strong> en HubSpot. El robot la vuelve a tomar en la siguiente pasada cada 2 horas indefinidamente.
              </p>
              <div class="mt-2 text-[11px] text-rose-400 font-medium">
                Impacto: Estudiantes acosados con hasta 15 correos (Ej. Victor Castillo y Joaquín Tabares).
              </div>
            </div>

            <!-- Riesgo 2 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-red-900/40 hover:border-red-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-red-900/80 text-red-300 flex items-center justify-center text-xs font-bold">2</span>
                <h4 class="text-sm font-bold text-red-300">Credenciales Hardcodeadas en XML</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                Tokens Bearer de HubSpot (<span class="font-mono text-amber-300">pat-na1-5609b...</span>) y contraseña SMTP de Gmail (<span class="font-mono text-amber-300">ranqloif********</span>) viajan incrustadas en texto claro dentro de los archivos <span class="font-mono text-xs">.bpprocess</span>, violando políticas de seguridad y NIST.
              </p>
              <div class="mt-2 text-[11px] text-rose-400 font-medium">
                Impacto: Riesgo de suplantación y exfiltración de base de datos de estudiantes.
              </div>
            </div>

            <!-- Riesgo 3 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-amber-900/40 hover:border-amber-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-amber-900/80 text-amber-300 flex items-center justify-center text-xs font-bold">3</span>
                <h4 class="text-sm font-bold text-amber-300">Clonación Errónea en Horarios</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                El Proceso 02 (Horarios) fue copiado del Proceso 01. Si el estudiante no está matriculado, <strong class="text-white">el robot le genera un Certificado de Admisión de Pregrado Bogotá</strong> en lugar de indicar que no puede emitirse el horario. Además guarda en carpetas de "Certificados de Estudio".
              </p>
              <div class="mt-2 text-[11px] text-amber-400 font-medium">
                Impacto: Entrega de documentos oficiales incorrectos a los estudiantes.
              </div>
            </div>

            <!-- Riesgo 4 -->
            <div class="p-4 rounded-xl bg-slate-950/60 border border-amber-900/40 hover:border-amber-700/60 transition">
              <div class="flex items-center gap-2 mb-2">
                <span class="w-6 h-6 rounded-md bg-amber-900/80 text-amber-300 flex items-center justify-center text-xs font-bold">4</span>
                <h4 class="text-sm font-bold text-amber-300">Dependencia Total de GCP de NBI</h4>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">
                La universidad no tiene servidores propios de Blue Prism. La operación corre en un servidor cloud privado de NBI con rutas absolutas a disco (<span class="font-mono text-xs text-amber-300">C:\\UMB\\...</span>). No hay contingencia, disaster recovery ni gobierno institucional.
              </p>
              <div class="mt-2 text-[11px] text-amber-400 font-medium">
                Impacto: Servicio sujeto a la disponibilidad del proveedor; migración pendiente.
              </div>
            </div>

          </div>

          <!-- Barra resumen inferior -->
          <div class="mt-4 p-3 rounded-xl bg-slate-800/60 border border-slate-700 flex flex-wrap items-center justify-between text-xs gap-2">
            <span class="text-slate-400">
              <i class="fa-solid fa-clock-rotate-left text-slate-400"></i> Frecuencia reportada: <strong>Cada 2h (6:00 a 18:00 Lun-Sáb)</strong>
            </span>
            <span class="text-slate-400">
              Envíos en producción (Sep 2026): <strong class="text-white font-mono">288 envíos (149 tickets)</strong>
            </span>
            <span class="text-rose-400 font-bold">
              48.3% de envíos de septiembre fueron duplicados
            </span>
          </div>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 2: RELATO OFICIAL VS REALIDAD OPERATIVA (TAB 2) -->
    <section id="tab-espejo" class="tab-content hidden space-y-6">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-scale-unbalanced text-amber-400"></i> Matriz de Auditoría: Lo Reportado vs. La Evidencia Empírica
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Comparativa punto a punto entre las afirmaciones del correo enviado a la nueva Dirección de Tecnología y los hallazgos técnicos del código y la telemetría.
        </p>
      </div>

      <!-- MATRIZ DE 6 PUNTOS -->
      <div class="space-y-4">

        <!-- Punto 1 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-lg">
          <div class="grid grid-cols-1 md:grid-cols-12 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <!-- Lo que dice el correo -->
            <div class="md:col-span-5 p-5 bg-slate-900/50">
              <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
                <i class="fa-solid fa-envelope"></i> Afirmación en Correo de Estatus
              </div>
              <blockquote class="text-sm font-medium text-slate-200 italic border-l-2 border-amber-500 pl-3">
                "Desde septiembre de 2026, los tres procesos (Certificado de Estudios, Certificado de Admisión y Certificado de Horarios) se encuentran desarrollados y en ejecución en producción..."
              </blockquote>
              <div class="mt-3 text-xs text-slate-400">
                Se presenta al cliente un alcance completado de 3 procesos independientes en operación productiva.
              </div>
            </div>
            <!-- La realidad técnica -->
            <div class="md:col-span-7 p-5 bg-slate-950/80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-microchip"></i> Evidencia en Código y Datos (.bpprocess)
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">Discrepancia Severa</span>
              </div>
              <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-xmark text-rose-500 mt-0.5"></i>
                  <span><strong>Solo existen 2 archivos de proceso Blue Prism:</strong> <code class="text-amber-300">01 - Certificados de Estudios</code> y <code class="text-amber-300">02 - Certificado de Horarios</code>.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-xmark text-rose-500 mt-0.5"></i>
                  <span><strong>"Certificado de Admisión" NO es un proceso independiente ni un trámite de HubSpot:</strong> Es simplemente una bifurcación condicional de 4 pasos de Word (MS Word VBO) dentro de Estudios cuando el estudiante tiene estado distinto a "Matriculado".</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-xmark text-rose-500 mt-0.5"></i>
                  <span>En los 226 tickets procesados, <strong>no existe un solo ticket con trámite "Certificado de Admisión"</strong>. Todo se carga bajo "Certificado de Estudio" o "Certificado de Horarios".</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Punto 2 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-lg">
          <div class="grid grid-cols-1 md:grid-cols-12 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <div class="md:col-span-5 p-5 bg-slate-900/50">
              <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
                <i class="fa-solid fa-envelope"></i> Afirmación en Correo de Estatus
              </div>
              <blockquote class="text-sm font-medium text-slate-200 italic border-l-2 border-amber-500 pl-3">
                "El robot valida cada solicitud recibida: si está correctamente diligenciada, genera el certificado correspondiente y lo envía directamente; si presenta algún error, responde al solicitante indicando el inconveniente y solicitando que la cree nuevamente."
              </blockquote>
              <div class="mt-3 text-xs text-slate-400">
                Se transmite la noción de un manejo controlado y limpio de excepciones con respuesta única.
              </div>
            </div>
            <div class="md:col-span-7 p-5 bg-slate-950/80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-microchip"></i> Evidencia en Código y Datos (.bpprocess)
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">Falla de Arquitectura</span>
              </div>
              <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-triangle-exclamation text-rose-400 mt-0.5"></i>
                  <span><strong>El robot NO actualiza la etapa del ticket en HubSpot al fallar:</strong> En la ruta de error (cédula vacía o sin registros en AulaNet), se envía correo SMTP pero la ejecución va a <code class="text-amber-300">Anchor5 &rarr; Anchor6 &rarr; Anchor7 &rarr; Loop End Ticket</code>, saltándose por completo la llamada PATCH de cierre.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-triangle-exclamation text-rose-400 mt-0.5"></i>
                  <span>Al permanecer el ticket en etapa 1 o 2, <strong>el robot lo vuelve a buscar y procesar cada 2 horas</strong>. Esto generó que <strong>72 tickets (31.9%) cayeran en bucle</strong>, llegando a enviar hasta 15 correos al mismo solicitante a lo largo de 4 días.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-triangle-exclamation text-rose-400 mt-0.5"></i>
                  <span>En septiembre (producción), <strong>139 de los 288 correos enviados (48.3%) fueron reintentos cíclicos</strong> provocados por este defecto.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Punto 3 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-lg">
          <div class="grid grid-cols-1 md:grid-cols-12 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <div class="md:col-span-5 p-5 bg-slate-900/50">
              <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
                <i class="fa-solid fa-envelope"></i> Afirmación en Correo de Estatus
              </div>
              <blockquote class="text-sm font-medium text-slate-200 italic border-l-2 border-amber-500 pl-3">
                "...se decidió reemplazar el proceso de Verificación Académica por los procesos de Certificado de Admisión y Certificado de Horarios, con el fin de dar cumplimiento al alcance definido..."
              </blockquote>
              <div class="mt-3 text-xs text-slate-400">
                Se argumenta cumplimiento contractual sustituyendo el trámite crítico de Verificación Académica.
              </div>
            </div>
            <div class="md:col-span-7 p-5 bg-slate-950/80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-microchip"></i> Evidencia en Código y Datos (.bpprocess)
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">Desbalance & Defecto</span>
              </div>
              <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-triangle-exclamation text-amber-400 mt-0.5"></i>
                  <span><strong>Falta total de volumen en Horarios:</strong> De 226 tickets, solo 6 fueron de Horarios (2.7%). Verificación Académica era un trámite de alto volumen empresarial que quedó 100% huérfano.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-bug text-rose-400 mt-0.5"></i>
                  <span><strong>Bug de copia en Proceso 02:</strong> Si el solicitante de Horarios no está matriculado, el robot genera un <em>Certificado de Admisión</em> mediante la plantilla de Word de Estudios, y lo guarda en <code class="text-amber-300">C:\\UMB\\Certificados de Estudio\\certificado_estudio_&lt;id&gt;.pdf</code>.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-triangle-exclamation text-amber-400 mt-0.5"></i>
                  <span>El correo de error reutilizado en Horarios afirma textualmente: <em>"no es posible generar el certificado de estudios solicitado"</em>, confundiendo al usuario final.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Punto 4 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-lg">
          <div class="grid grid-cols-1 md:grid-cols-12 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <div class="md:col-span-5 p-5 bg-slate-900/50">
              <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
                <i class="fa-solid fa-envelope"></i> Afirmación en Correo de Estatus
              </div>
              <blockquote class="text-sm font-medium text-slate-200 italic border-l-2 border-amber-500 pl-3">
                "Actualmente la infraestructura sobre la cual operan estos procesos ha sido asumida y provista por NBI, sin costo alguno para la Universidad Manuela Beltrán."
              </blockquote>
              <div class="mt-3 text-xs text-slate-400">
                Se destaca como valor agregado y concesión comercial el despliegue del servidor en Google Cloud.
              </div>
            </div>
            <div class="md:col-span-7 p-5 bg-slate-950/80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-microchip"></i> Evidencia en Código y Datos (.bpprocess)
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">Riesgo de Gobierno TI</span>
              </div>
              <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-circle-exclamation text-amber-400 mt-0.5"></i>
                  <span><strong>Falta de portabilidad y fragilidad local:</strong> Los procesos tienen acoplamiento rígido a la máquina virtual de NBI (<code class="text-amber-300">C:\\UMB\\Templates\\PLANTILLA ADMITIDO WORD.docx</code>). En cualquier otro servidor sin esa estructura exacta, el robot falla de inmediato.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-circle-exclamation text-amber-400 mt-0.5"></i>
                  <span><strong>Bloqueo de VPN por infraestructura externa:</strong> El motivo real por el cual no se pudo conectar con Campus para Verificación Académica fue que el servidor estaba en GCP de NBI sin una VPN site-to-site autorizada por UMB.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-circle-exclamation text-amber-400 mt-0.5"></i>
                  <span>Si NBI apaga la VM o caducan los créditos de GCP, el servicio del CASE se paraliza sin que UMB tenga acceso ni respaldo directo.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Punto 5 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-lg">
          <div class="grid grid-cols-1 md:grid-cols-12 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <div class="md:col-span-5 p-5 bg-slate-900/50">
              <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
                <i class="fa-solid fa-envelope"></i> Afirmación en Correo de Estatus
              </div>
              <blockquote class="text-sm font-medium text-slate-200 italic border-l-2 border-amber-500 pl-3">
                "Adjunto encontrarán el reporte detallado... (414 envíos, 226 tickets únicos, incluyendo el análisis de re procesamiento)."
              </blockquote>
              <div class="mt-3 text-xs text-slate-400">
                Se adjunta la cifra como muestra de alto volumen procesado en la fase.
              </div>
            </div>
            <div class="md:col-span-7 p-5 bg-slate-950/80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-microchip"></i> Evidencia en Código y Datos (.bpprocess)
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">Métricas Confusas</span>
              </div>
              <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-circle-exclamation text-rose-400 mt-0.5"></i>
                  <span><strong>126 de los 414 envíos corresponden a Julio (pruebas con francisco.mateus@narnajabi.com):</strong> No son estudiantes reales de la UMB.</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-circle-exclamation text-rose-400 mt-0.5"></i>
                  <span>En la fase real con estudiantes (septiembre), se atendieron <strong>149 tickets únicos</strong>, pero se emitieron <strong>288 correos</strong>. El 48.3% del tráfico de producción fue desperdicio generado por fallas en el software.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Punto 6 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-lg">
          <div class="grid grid-cols-1 md:grid-cols-12 divide-y md:divide-y-0 md:divide-x divide-slate-800">
            <div class="md:col-span-5 p-5 bg-slate-900/50">
              <div class="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
                <i class="fa-solid fa-envelope"></i> Afirmación en Correo de Estatus
              </div>
              <blockquote class="text-sm font-medium text-slate-200 italic border-l-2 border-amber-500 pl-3">
                "Próximos pasos: Nuevas cotizaciones, reunión para nuevos procesos fuera de alcance, y links de pago mediante Blue Prism WorkHQ..."
              </blockquote>
              <div class="mt-3 text-xs text-slate-400">
                Se impulsa la venta y cotización de nuevos alcances y módulos avanzados de Blue Prism.
              </div>
            </div>
            <div class="md:col-span-7 p-5 bg-slate-950/80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-sky-400 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-microchip"></i> Evidencia en Código y Datos (.bpprocess)
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800">Recomendación Técnica</span>
              </div>
              <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-hand text-sky-400 mt-0.5"></i>
                  <span><strong>Premaduro para expandir:</strong> La base actual no utiliza las buenas prácticas recomendadas por Blue Prism (falta de Work Queues con locking, sin Credential Vault, consultas REST monolíticas con límite de 100 tickets sin paginación).</span>
                </li>
                <li class="flex items-start gap-2">
                  <i class="fa-solid fa-hand text-sky-400 mt-0.5"></i>
                  <span>Antes de cotizar trámites adicionales o licenciar WorkHQ, la universidad debe <strong class="text-white">estabilizar la arquitectura actual</strong>, corregir los bucles de spam, migrar la infraestructura y sanear la deuda técnica.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 3: TELEMETRÍA Y GRÁFICOS (TAB 3) -->
    <section id="tab-telemetria" class="tab-content hidden space-y-8">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-chart-line text-blue-400"></i> Telemetría Operativa y Análisis Estadístico
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Distribución temporal, concentración de ejecuciones horarias, comportamiento del bucle y picos de producción.
        </p>
      </div>

      <!-- FILA 1: TIMELINE DIARIO Y DISTRIBUCIÓN POR TRÁMITE -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Timeline de envíos por día (2 cols) -->
        <div class="lg:col-span-2 bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-chart-area text-blue-500"></i> Evolución Cronológica de Envíos Diarios
              </h3>
              <p class="text-xs text-slate-400">Desglose de los 414 correos en Fase de Pruebas (Julio) vs. Fase "Producción" (Septiembre)</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="inline-flex items-center gap-1 text-slate-400">
                <span class="w-2.5 h-2.5 rounded-full bg-slate-500"></span> Julio (126)
              </span>
              <span class="inline-flex items-center gap-1 text-red-400">
                <span class="w-2.5 h-2.5 rounded-full bg-red-500"></span> Septiembre (288)
              </span>
            </div>
          </div>
          <div class="h-64 sm:h-72">
            <canvas id="chartTimeline"></canvas>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between text-xs text-slate-400">
            <span>Pico Máximo en Producción: <strong class="text-rose-400 font-mono">16 de Septiembre (49 envíos)</strong></span>
            <span>Segundo Pico: <strong class="text-amber-400 font-mono">17 de Septiembre (39 envíos)</strong></span>
            <span>Fin de Registro: <strong class="text-slate-300 font-mono">25 de Septiembre</strong></span>
          </div>
        </div>

        <!-- Distribución de Trámites Reales (1 col) -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2 mb-2">
              <i class="fa-solid fa-layer-group text-purple-400"></i> Demanda por Trámite Real
            </h3>
            <p class="text-xs text-slate-400 mb-4">
              Participación de solicitudes únicas recibidas en la bandeja de entrada.
            </p>
            <div class="h-52 flex items-center justify-center">
              <canvas id="chartTramites"></canvas>
            </div>
          </div>
          
          <div class="mt-4 pt-3 border-t border-slate-800 space-y-2 text-xs">
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-800/50">
              <span class="text-slate-300 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-red-500"></span> Certificado de Estudios:
              </span>
              <strong class="font-mono text-white">220 tickets (97.3%)</strong>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-800/50">
              <span class="text-slate-300 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-amber-500"></span> Certificado de Horarios:
              </span>
              <strong class="font-mono text-amber-400">6 tickets (2.7%)</strong>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-800/50">
              <span class="text-slate-400 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-slate-600"></span> Verificación Académica:
              </span>
              <strong class="font-mono text-slate-500">0 (Bloqueado)</strong>
            </div>
          </div>
        </div>

      </div>

      <!-- FILA 2: DISTRIBUCIÓN HORARIA Y ANATOMÍA DEL REPROCESO -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Gráfico Horario de Ejecución -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-clock text-amber-400"></i> Frecuencia de Ejecución Horaria (UTC vs COL)
              </h3>
              <p class="text-xs text-slate-400">Muestra las pasadas cada 2 horas del robot y ejecuciones fuera de ventana</p>
            </div>
          </div>
          <div class="h-64">
            <canvas id="chartHoras"></canvas>
          </div>
          <div class="mt-3 text-xs text-slate-400 bg-slate-800/40 p-3 rounded-xl border border-slate-800">
            <i class="fa-solid fa-circle-info text-amber-400 mr-1"></i> <strong>Nota:</strong> Los horarios corresponden a UTC. Las horas pico en Colombia (UTC-5) son 08:00 (13:00 UTC con 72 envíos), 10:00 (15:00 UTC con 55 envíos), 12:00 (17:00 UTC con 53 envíos) y 14:00 (19:00 UTC con 46 envíos). Se observan ejecuciones residuales a las 00:00 - 04:00 UTC.
          </div>
        </div>

        <!-- Histograma de Reprocesamiento -->
        <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-repeat text-rose-400"></i> Severidad de Reenvíos por Ticket
              </h3>
              <p class="text-xs text-slate-400">Cantidad de tickets agrupados según el número de respuestas recibidas</p>
            </div>
          </div>
          <div class="h-64">
            <canvas id="chartReprocesos"></canvas>
          </div>
          <div class="mt-3 text-xs text-slate-400 bg-slate-800/40 p-3 rounded-xl border border-slate-800">
            <i class="fa-solid fa-triangle-exclamation text-rose-400 mr-1"></i> <strong>Hallazgo crítico:</strong> 72 tickets sufrieron reenvío múltiple. 15 tickets recibieron 5 o más respuestas, alcanzando un pico absurdo de 15 respuestas para dos estudiantes particulares.
          </div>
        </div>

      </div>

      <!-- TOP 15 TICKETS CON MÁS REPROCESAMIENTO -->
      <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 shadow-xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-bomb text-red-500"></i> Top 15 Tickets Más Afectados por el Bucle Infinito
            </h3>
            <p class="text-xs text-slate-400">Casos donde el estudiante recibió múltiples correos de error repetidos por falta de cambio de estado</p>
          </div>
          <span class="text-xs font-mono px-3 py-1 rounded-full bg-red-950 text-red-300 font-bold border border-red-800">
            Bucle cada 2 horas confirmado
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider bg-slate-950/50">
                <th class="p-3">Ticket ID</th>
                <th class="p-3">Estudiante</th>
                <th class="p-3">Trámite</th>
                <th class="p-3 text-center">Envíos Recibidos</th>
                <th class="p-3">Primer Envío</th>
                <th class="p-3">Último Envío</th>
                <th class="p-3">Duración del Bucle</th>
                <th class="p-3 text-center">Acción</th>
              </tr>
            </thead>
            <tbody id="topTicketsBody" class="divide-y divide-slate-800/60 font-mono">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- SECCIÓN 4: AUDITORÍA DE CÓDIGO BLUE PRISM (TAB 4) -->
    <section id="tab-codigo" class="tab-content hidden space-y-6">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-code text-purple-400"></i> Auditoría Forense de Código Blue Prism (.bpprocess)
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Inspección directa de los archivos XML exportados de Blue Prism: vulnerabilidades de seguridad, anti-patrones y fallos de lógica.
        </p>
      </div>

      <!-- ACORDEÓN / TARJETAS DETALLADAS DE AUDITORÍA -->
      <div class="space-y-4">

        <!-- Defecto 1: Seguridad -->
        <div class="bg-slate-900/90 rounded-2xl border border-red-900/40 p-5 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-red-950 text-red-300 text-xs font-bold border border-red-800">CRÍTICO - SEGURIDAD</span>
              <h3 class="text-base font-bold text-white">1. Credenciales y Tokens Privados Hardcodeados en Texto Plano</h3>
            </div>
            <span class="text-xs font-mono text-slate-500">Stage: Headers HUB & Configure3</span>
          </div>
          <p class="text-xs text-slate-300 mb-3">
            El archivo exportado de Blue Prism contiene credenciales sensibles quemadas en las propiedades iniciales de las colecciones y bloques de acción, en lugar de utilizar el <em>Blue Prism Credential Manager</em> o un almacén de claves (CyberArk/Azure Key Vault).
          </p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="text-[11px] text-amber-400 font-semibold mb-1 flex items-center gap-1">
                <i class="fa-solid fa-key"></i> Token Privado HubSpot (Expuesto en Headers HUB)
              </div>
              <code class="text-red-400 break-all text-[11px]">
                Bearer pat-na1-5609b158-****-****-****-[REDACTED]
              </code>
            </div>
            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="text-[11px] text-amber-400 font-semibold mb-1 flex items-center gap-1">
                <i class="fa-solid fa-lock-open"></i> Contraseña de Aplicación Gmail (Configure3)
              </div>
              <div class="text-slate-400 text-[11px]">Usuario: <span class="text-slate-200">francisco.mateus@narnajabi.com</span></div>
              <div class="text-slate-400 text-[11px]">Password: <span class="text-red-400">ranqloif********</span></div>
            </div>
          </div>
          <div class="mt-3 text-xs bg-red-950/30 p-2.5 rounded-lg border border-red-900/50 text-red-300 flex items-center gap-2">
            <i class="fa-solid fa-shield-halved"></i>
            <span><strong>Acción Inmediata Requerida:</strong> Revocar inmediatamente el token privado de HubSpot en el portal de desarrolladores de HubSpot, invalidar la clave de aplicación de Gmail y crear las credenciales seguras en el Credential Manager de Blue Prism.</span>
          </div>
        </div>

        <!-- Defecto 2: Bucle Infinito -->
        <div class="bg-slate-900/90 rounded-2xl border border-red-900/40 p-5 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-red-950 text-red-300 text-xs font-bold border border-red-800">CRÍTICO - OPERATIVO</span>
              <h3 class="text-base font-bold text-white">2. Bucle Infinito por Omisión de Cambio de Etapa en Errores</h3>
            </div>
            <span class="text-xs font-mono text-slate-500">Stage: Email - POP3/SMTP::Send Message</span>
          </div>
          <p class="text-xs text-slate-300 mb-3">
            En el proceso de atención, si la validación <span class="font-mono text-amber-300">Nit vacio?</span> o la decisión <span class="font-mono text-amber-300">Result Empty</span> detectan que no hay datos académicos del estudiante en AulaNet, el flujo salta a enviar el correo de error. Sin embargo, la salida del envío de correo conduce directamente a <span class="font-mono text-amber-300">Anchor5 &rarr; Anchor6 &rarr; Anchor7 &rarr; Loop End Ticket</span>.
          </p>
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 overflow-x-auto">
            <div class="text-slate-500 mb-1">// Secuencia observada en el XML (Líneas 440-608):</div>
            <span class="text-blue-400">&lt;stage name="Email - POP3/SMTP::Send Message"&gt;</span><br>
            &nbsp;&nbsp;<span class="text-purple-400">&lt;onsuccess&gt;</span>126128f0-b12b-427d-bef4-7b0bd7cf53e1<span class="text-purple-400">&lt;/onsuccess&gt;</span> <span class="text-slate-500">// Anchor5</span><br>
            <span class="text-blue-400">&lt;/stage&gt;</span><br>
            <span class="text-rose-400">// ¡FALTA LLAMADA A PATCH /crm/v3/objects/tickets/:id! El ticket sigue con hs_pipeline_stage = 1 o 2.</span>
          </div>
          <div class="mt-3 text-xs bg-slate-800/50 p-2.5 rounded-lg border border-slate-700 text-slate-300 flex items-center gap-2">
            <i class="fa-solid fa-wrench text-amber-400"></i>
            <span><strong>Solución:</strong> Interpolar una etapa de "Update Ticket Error" que cambie <code class="text-amber-300">hs_pipeline_stage</code> a una etapa de Excepción (ej. etapa 5) y marque una propiedad de control para que no vuelva a ser consultado por la búsqueda inicial.</span>
          </div>
        </div>

        <!-- Defecto 3: Bug en Horarios -->
        <div class="bg-slate-900/90 rounded-2xl border border-amber-900/40 p-5 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 text-xs font-bold border border-amber-800">ALTO - INTEGRIDAD DE NEGOCIO</span>
              <h3 class="text-base font-bold text-white">3. Clonación Errónea: Certificado de Admisión Generado en Horarios</h3>
            </div>
            <span class="text-xs font-mono text-slate-500">Proceso 02 - Líneas 1234-1444</span>
          </div>
          <p class="text-xs text-slate-300 mb-3">
            En el Proceso 02 (Certificado de Horarios), si el estudiante no tiene estado "Matriculado", la decisión <span class="font-mono text-amber-300">Matriculado?</span> enruta a la acción de Microsoft Word VBO que abre <span class="font-mono text-amber-300">C:\\UMB\\Templates\\PLANTILLA ADMITIDO WORD.docx</span>, generando un Certificado de Admisión y guardándolo en la carpeta de Certificados de Estudio.
          </p>
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-amber-300">
            &lt;input name="File Name" expr="&quot;C:\UMB\Certificados de Estudio\certificado_estudio_&quot;&amp;[Properties.documento_de_identificacion_nit]&amp;&quot;.pdf&quot;" /&gt;
          </div>
          <div class="mt-3 text-xs bg-slate-800/50 p-2.5 rounded-lg border border-slate-700 text-slate-300 flex items-center gap-2">
            <i class="fa-solid fa-circle-exclamation text-amber-400"></i>
            <span><strong>Consecuencia:</strong> Un estudiante no matriculado que solicita su horario recibe una carta de admisión a la universidad sin haberla solicitado.</span>
          </div>
        </div>

        <!-- Defecto 4: Límite de 100 sin paginación -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-xs font-bold border border-slate-700">MEDIO - ESCALABILIDAD</span>
              <h3 class="text-base font-bold text-white">4. Límite Fijo de 100 Tickets sin Paginación en API de HubSpot</h3>
            </div>
            <span class="text-xs font-mono text-slate-500">Stage: HTTP Request Phase 1 (Línea 42)</span>
          </div>
          <p class="text-xs text-slate-300 mb-2">
            El payload JSON enviado al endpoint <span class="font-mono text-xs text-slate-400">/crm/objects/2026-03/tickets/search</span> tiene fijado <span class="font-mono text-amber-300">"limit": 100</span> sin manejar cursores ni paginación (<span class="font-mono text-xs">after</span>).
          </p>
          <p class="text-xs text-slate-400">
            Si durante una temporada de matrículas se acumulan más de 100 tickets en etapa 1 o 2, los tickets posteriores al número 100 quedan permanentemente en cola y nunca son atendidos por el robot.
          </p>
        </div>

        <!-- Defecto 5: Cédula de prueba quemada -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-xs font-bold border border-slate-700">MEDIO - CALIDAD DE CÓDIGO</span>
              <h3 class="text-base font-bold text-white">5. Cédula de Prueba Hardcodeada en Cálculo de Adjuntos de Error</h3>
            </div>
            <span class="text-xs font-mono text-slate-500">Stage: Attachment (Línea 448)</span>
          </div>
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-slate-300">
            &lt;calculation expression="&quot;C:\UMB\Certificados de Estudio\certificado_estudio_1066599028.pdf&quot;" stage="Attachments.Path" /&gt;
          </div>
          <p class="text-xs text-slate-400 mt-2">
            La cédula <span class="font-mono text-amber-300">1066599028</span> quedó quemada en el cálculo del adjunto para el flujo de error. Si ese archivo PDF de prueba no existe físicamente en el disco de la máquina, el robot puede fallar arrojando excepción de archivo no encontrado.
          </p>
        </div>

        <!-- Defecto 6: Selección de período Count Tabla - 1 -->
        <div class="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-xs font-bold border border-slate-700">MEDIO - CALIDAD DE DATOS</span>
              <h3 class="text-base font-bold text-white">6. Selección Ciega de Período Académico (Count Tabla - 1)</h3>
            </div>
            <span class="text-xs font-mono text-slate-500">Stage: Copy Rows (Línea 1224)</span>
          </div>
          <p class="text-xs text-slate-300 mb-2">
            El robot cuenta las filas de la tabla de asignaturas y extrae la última fila (<span class="font-mono text-amber-300">[Count Tabla] - 1</span>) asumiendo ciegamente que la última fila siempre corresponde al período académico vigente. Si el ordenamiento de AulaNet cambia o un estudiante tiene homologaciones o registros históricos al final, el certificado se emite con un período o estado incorrecto.
          </p>
        </div>

      </div>

    </section>

    <!-- SECCIÓN 5: EXPLORADOR DE TICKETS (TAB 5) -->
    <section id="tab-tickets" class="tab-content hidden space-y-6">
      
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
            <i class="fa-solid fa-list-check text-emerald-400"></i> Auditoría Individual de Tickets (226 Casos Únicos)
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Explore los tickets procesados, identifique los casos con reintentos y consulte la trazabilidad horaria exacta de envíos.
          </p>
        </div>

        <!-- Buscador -->
        <div class="relative w-full sm:w-72">
          <input type="text" id="ticketSearch" onkeyup="filterTickets()" placeholder="Buscar por nombre o ticket ID..." 
                 class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 pl-10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-red-500 transition">
          <i class="fa-solid fa-search absolute left-3.5 top-3 text-slate-500 text-xs"></i>
        </div>
      </div>

      <!-- Filtros rápidos -->
      <div class="flex flex-wrap items-center gap-2 text-xs font-medium">
        <button onclick="setFilter('all')" id="filter-all" class="filter-btn active-filter px-3 py-1.5 rounded-lg bg-red-900/40 text-red-300 border border-red-700/60">
          Todos (226)
        </button>
        <button onclick="setFilter('reprocessed')" id="filter-reprocessed" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Reprocesados / Loop (72)
        </button>
        <button onclick="setFilter('critical')" id="filter-critical" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Críticos (&ge;5 envíos: 15)
        </button>
        <button onclick="setFilter('single')" id="filter-single" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Un solo envío (154)
        </button>
        <button onclick="setFilter('horarios')" id="filter-horarios" class="filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">
          Horarios (6)
        </button>
      </div>

      <!-- Tabla de Tickets -->
      <div class="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
        <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="sticky top-0 z-10 bg-slate-950 text-slate-400 font-semibold uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th class="p-3">Ticket ID</th>
                <th class="p-3">Estudiante</th>
                <th class="p-3">Trámite</th>
                <th class="p-3 text-center"># Envíos</th>
                <th class="p-3">Primer Envío (UTC)</th>
                <th class="p-3">Último Envío (UTC)</th>
                <th class="p-3 text-center">Estado Loop</th>
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

    <!-- SECCIÓN 6: HOJA DE RUTA Y PLAN DE REMEDIACIÓN (TAB 6) -->
    <section id="tab-roadmap" class="tab-content hidden space-y-8">
      
      <div class="border-b border-slate-800 pb-4">
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <i class="fa-solid fa-route text-sky-400"></i> Plan de Remediación y Transición Institucional
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Hoja de ruta estructurada para estabilizar la operación actual, blindar la seguridad, migrar a servidores de la UMB y desbloquear nuevos trámites.
        </p>
      </div>

      <!-- TIMELINE DE FASES DE REMEDIACIÓN -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        <!-- Fase 1 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-red-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-red-900 text-red-300 font-bold flex items-center justify-center text-sm mb-3">
            F1
          </div>
          <span class="text-xs font-bold text-red-400 uppercase tracking-wider">Días 1 - 5</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Parche Crítico Inmediato (Hotfix)</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-red-400 mt-0.5"></i>
              <span><strong>Detener bucle infinito:</strong> Agregar PATCH en HubSpot para cambiar etapa a excepción al fallar validación.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-red-400 mt-0.5"></i>
              <span><strong>Rotación de credenciales:</strong> Revocar token de HubSpot expuesto y password de Gmail. Mover a Credential Manager.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-red-400 mt-0.5"></i>
              <span><strong>Desactivar macro Word en Horarios:</strong> Evitar emisión de cartas de admisión no procedentes.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Responsable: <strong>NBI / RPA Dev</strong>
          </div>
        </div>

        <!-- Fase 2 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-amber-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-amber-900 text-amber-300 font-bold flex items-center justify-center text-sm mb-3">
            F2
          </div>
          <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">Semanas 2 - 3</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Estabilización y Portabilidad</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-amber-400 mt-0.5"></i>
              <span><strong>Paginación en HubSpot:</strong> Implementar cursor para procesar más de 100 tickets por lote sin pérdida.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-amber-400 mt-0.5"></i>
              <span><strong>Desacople de rutas:</strong> Reemplazar <code class="text-amber-300">C:\\UMB\\...</code> por variables de entorno y recursos compartidos.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-amber-400 mt-0.5"></i>
              <span><strong>Mapeo dinámico de programas:</strong> Dejar de quemar <code class="text-amber-300">pregrado_presencial_bogota</code>.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Responsable: <strong>NBI + QA Conjunto</strong>
          </div>
        </div>

        <!-- Fase 3 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-blue-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-blue-900 text-blue-300 font-bold flex items-center justify-center text-sm mb-3">
            F3
          </div>
          <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">Semanas 3 - 6</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Migración a Infraestructura UMB</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-blue-400 mt-0.5"></i>
              <span><strong>Despliegue On-Premise/Cloud UMB:</strong> Instalar Blue Prism Application Server y Runtime Resources propios.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-blue-400 mt-0.5"></i>
              <span><strong>VPN Site-to-Site con Campus:</strong> Conectar el entorno con el ERP Campus para <strong>desbloquear Verificación Académica</strong>.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-blue-400 mt-0.5"></i>
              <span><strong>Centralización de correo:</strong> Eliminar el SMTP de pruebas de Gmail y canalizar todo por Conversations API de HubSpot.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Responsable: <strong>Dirección de TI UMB</strong>
          </div>
        </div>

        <!-- Fase 4 -->
        <div class="bg-slate-900/90 rounded-2xl p-5 border border-purple-800/40 relative">
          <div class="w-8 h-8 rounded-lg bg-purple-900 text-purple-300 font-bold flex items-center justify-center text-sm mb-3">
            F4
          </div>
          <span class="text-xs font-bold text-purple-400 uppercase tracking-wider">Mes 2 en Adelante</span>
          <h3 class="text-sm font-bold text-white mt-1 mb-2">Madurez y Nuevos Trámites</h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-purple-400 mt-0.5"></i>
              <span><strong>Migración a Work Queues:</strong> Reestructurar el proceso hacia la arquitectura Blue Prism de colas con reintentos y candados.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-purple-400 mt-0.5"></i>
              <span><strong>Evaluación de WorkHQ:</strong> Análisis de viabilidad técnica y retorno de inversión para pasarela de pagos.</span>
            </li>
            <li class="flex items-start gap-1.5">
              <i class="fa-solid fa-check text-purple-400 mt-0.5"></i>
              <span><strong>Nuevos trámites CASE:</strong> Levantamiento formal con la coordinación, sujetos a aprobación y cotización independiente.</span>
            </li>
          </ul>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Responsable: <strong>Comité de Gobierno UMB - NBI</strong>
          </div>
        </div>

      </div>

      <!-- MATRIZ DE DECISIÓN PARA LA REUNIÓN CON TI UMB -->
      <div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800">
        <h3 class="text-base font-bold text-white flex items-center gap-2 mb-3">
          <i class="fa-solid fa-handshake text-emerald-400"></i> Recomendaciones para la Mesa de Trabajo con la Nueva Dirección de Tecnología
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h4 class="font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-1 text-slate-500"></i> Postura sobre Nuevos Trámites
            </h4>
            <p class="leading-relaxed">
              No iniciar el desarrollo de nuevos trámites ni contratar módulos como Blue Prism WorkHQ hasta que la infraestructura propia de la universidad esté operativa y los 2 procesos vigentes se encuentren completamente estabilizados y libres de bucles.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h4 class="font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-2 text-slate-500"></i> Prioridad en Verificación Académica
            </h4>
            <p class="leading-relaxed">
              Exigir a NBI el diseño técnico para la reactivación de Verificación Académica una vez la infraestructura esté en la UMB, ya que este trámite sustituido era uno de los pilares del caso de negocio original del CASE.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h4 class="font-bold text-white mb-2 flex items-center gap-2">
              <i class="fa-solid fa-3 text-slate-500"></i> Acuerdo de Niveles de Servicio (SLA)
            </h4>
            <p class="leading-relaxed">
              Establecer métricas claras de monitoreo: tasa máxima admisible de reprocesos (&lt; 2%), tiempo de resolución por ticket (&lt; 15 min), y auditoría trimestral de seguridad en el Credential Manager de Blue Prism.
            </p>
          </div>
        </div>
      </div>

    </section>

  </main>

  <!-- MODAL DE TRAZABILIDAD DE TICKET INDIVIDUAL -->
  <div id="ticketModal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] flex flex-col">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
        <div>
          <span class="text-xs font-mono text-slate-400">Trazabilidad Cronológica de Envíos</span>
          <h3 id="modalStudent" class="text-lg font-bold text-white flex items-center gap-2"></h3>
          <span id="modalTicketId" class="text-xs font-mono text-amber-400"></span>
        </div>
        <button onclick="closeModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="overflow-y-auto flex-1 pr-2 space-y-3" id="modalEventsList">
        <!-- Events rendered via JS -->
      </div>

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
      <span>Dashboard de Auditoría RPA - Universidad Manuela Beltrán &copy; 2026</span>
      <span>Generado con base en <strong>BPA Process 01, 02</strong>, PDD Versión 2 y Reporte Forense de 414 Envíos</span>
    </div>
  </footer>

  <!-- SCRIPT DE DATOS Y LÓGICA -->
  <script>
    // Embedded Data from Python Parser
    const rawData = ''' + json.dumps(data) + ''';

    // Current filter state
    let currentFilter = 'all';

    // Tab Navigation
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-tab').forEach(el => {
        el.classList.remove('bg-red-900/40', 'text-red-300', 'border-red-700/50', 'active-tab');
        el.classList.add('text-slate-400', 'border-transparent');
      });

      document.getElementById(tabId).classList.remove('hidden');
      const btn = document.getElementById('btn-' + tabId);
      if (btn) {
        btn.classList.add('bg-red-900/40', 'text-red-300', 'border-red-700/50', 'active-tab');
        btn.classList.remove('text-slate-400', 'border-transparent');
      }
    }

    // Initialize Charts on Load
    window.addEventListener('DOMContentLoaded', () => {
      initCharts();
      renderTopTickets();
      renderTicketsTable();
    });

    function initCharts() {
      // 1. Chart Eficiencia (Donut)
      const ctxEficiencia = document.getElementById('chartEficiencia').getContext('2d');
      new Chart(ctxEficiencia, {
        type: 'doughnut',
        data: {
          labels: ['Envíos Útiles (1 por ticket)', 'Envíos Duplicados / Loop'],
          datasets: [{
            data: [226, 188],
            backgroundColor: ['#10B981', '#EF4444'],
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
      const dates = rawData.date_distribution.map(d => d[0].substring(5)); // MM-DD
      const counts = rawData.date_distribution.map(d => d[1]);
      
      const barColors = rawData.date_distribution.map(d => d[0].startsWith('2026-07') ? 'rgba(100, 116, 139, 0.7)' : 'rgba(239, 68, 68, 0.85)');

      new Chart(ctxTimeline, {
        type: 'bar',
        data: {
          labels: dates,
          datasets: [{
            label: 'Correos Enviados',
            data: counts,
            backgroundColor: barColors,
            borderRadius: 6,
            borderSkipped: false
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
                label: (item) => 'Envíos: ' + item.raw + (item.label.startsWith('07') ? ' (Pruebas NBI)' : ' (Producción UMB)')
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            },
            y: {
              grid: { color: '#1e293b' },
              ticks: { color: '#64748b', font: { size: 10 } },
              beginAtZero: true
            }
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
            backgroundColor: ['#EF4444', '#F59E0B'],
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
            label: 'Envíos por Hora (UTC)',
            data: hourCounts,
            borderColor: '#F59E0B',
            backgroundColor: 'rgba(245, 158, 11, 0.15)',
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#F59E0B',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            },
            y: {
              grid: { color: '#1e293b' },
              ticks: { color: '#64748b', font: { size: 10 } },
              beginAtZero: true
            }
          }
        }
      });

      // 5. Chart Reprocesos (Histogram)
      const ctxRepro = document.getElementById('chartReprocesos').getContext('2d');
      const reprocessLabels = rawData.reprocess_distribution.map(r => r[0] + (r[0] === 1 ? ' envío' : ' envíos'));
      const reprocessCounts = rawData.reprocess_distribution.map(r => r[1]);

      new Chart(ctxRepro, {
        type: 'bar',
        data: {
          labels: reprocessLabels,
          datasets: [{
            label: 'Cantidad de Tickets',
            data: reprocessCounts,
            backgroundColor: [
              '#10B981', // 1 send (healthy)
              '#3B82F6', '#6366F1', '#8B5CF6', '#EC4899', '#F43F5E', '#EF4444', '#DC2626', '#991B1B'
            ],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            },
            y: {
              grid: { color: '#1e293b' },
              ticks: { color: '#64748b', font: { size: 10 } },
              beginAtZero: true
            }
          }
        }
      });
    }

    // Render Top Tickets Table
    function renderTopTickets() {
      const tbody = document.getElementById('topTicketsBody');
      tbody.innerHTML = '';

      rawData.top_reprocessed.forEach(t => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition border-b border-slate-800/40';
        
        // Duration calc
        const d1 = new Date(t.first_send);
        const d2 = new Date(t.last_send);
        const diffHours = Math.round((d2 - d1) / (1000 * 60 * 60));
        const durText = diffHours > 24 ? Math.round(diffHours / 24) + ' días (' + diffHours + ' hrs)' : diffHours + ' hrs';

        tr.innerHTML = `
          <td class="p-3 text-amber-400 font-semibold">${t.ticket}</td>
          <td class="p-3 font-sans font-medium text-white">${t.student}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[11px]">${t.type}</span></td>
          <td class="p-3 text-center">
            <span class="px-2.5 py-1 rounded-full ${t.sends >= 6 ? 'bg-red-950 text-red-300 border border-red-700 font-bold badge-glow' : 'bg-amber-950 text-amber-300 border border-amber-700 font-bold'} text-xs">
              ${t.sends} envíos
            </span>
          </td>
          <td class="p-3 text-slate-400 text-[11px]">${t.first_send.substring(0, 16)}</td>
          <td class="p-3 text-slate-400 text-[11px]">${t.last_send.substring(0, 16)}</td>
          <td class="p-3 text-rose-400 text-[11px] font-sans font-semibold">${durText}</td>
          <td class="p-3 text-center">
            <button onclick="openTicketModal('${t.ticket}')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-sans transition">
              <i class="fa-solid fa-timeline"></i> Trazabilidad
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Render Full Tickets Explorer
    function renderTicketsTable() {
      const tbody = document.getElementById('ticketsTableBody');
      const query = document.getElementById('ticketSearch').value.toLowerCase();
      tbody.innerHTML = '';

      let filtered = rawData.tickets.filter(t => {
        // Text search
        const matchSearch = t.ticket.toLowerCase().includes(query) || t.student.toLowerCase().includes(query);
        if (!matchSearch) return false;

        // Chip filter
        if (currentFilter === 'reprocessed') return t.sends > 1;
        if (currentFilter === 'critical') return t.sends >= 5;
        if (currentFilter === 'single') return t.sends === 1;
        if (currentFilter === 'horarios') return t.type === 'Horarios';
        return true;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="p-8 text-center text-slate-500 font-sans">No se encontraron tickets con ese criterio de búsqueda.</td></tr>';
        return;
      }

      filtered.forEach(t => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/30 transition border-b border-slate-800/40 text-[11px]';
        
        const isLoop = t.sends > 1;
        const statusBadge = isLoop 
          ? `<span class="px-2 py-0.5 rounded-full bg-red-950 text-red-300 border border-red-800 text-[10px] font-bold">REPROCESADO</span>`
          : `<span class="px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 text-[10px] font-bold">NORMAL (1)</span>`;

        tr.innerHTML = `
          <td class="p-3 text-amber-400 font-semibold">${t.ticket}</td>
          <td class="p-3 font-sans font-medium text-slate-200">${t.student}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">${t.type}</span></td>
          <td class="p-3 text-center font-bold ${t.sends > 1 ? 'text-rose-400' : 'text-slate-400'}">${t.sends}</td>
          <td class="p-3 text-slate-400">${t.first_send.substring(0, 16)}</td>
          <td class="p-3 text-slate-400">${t.last_send.substring(0, 16)}</td>
          <td class="p-3 text-center">${statusBadge}</td>
          <td class="p-3 text-center">
            <button onclick="openTicketModal('${t.ticket}')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-sans hover:text-white transition">
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
        btn.classList.remove('bg-red-900/40', 'text-red-300', 'border-red-700/60');
        btn.classList.add('bg-slate-900', 'text-slate-400', 'border-slate-800');
      });
      document.getElementById('filter-' + type).classList.remove('bg-slate-900', 'text-slate-400', 'border-slate-800');
      document.getElementById('filter-' + type).classList.add('bg-red-900/40', 'text-red-300', 'border-red-700/60');
      renderTicketsTable();
    }

    function filterTickets() {
      renderTicketsTable();
    }

    // Modal logic
    function openTicketModal(ticketId) {
      const ticket = rawData.tickets.find(t => t.ticket === ticketId);
      if (!ticket) return;

      const events = rawData.events.filter(e => e.ticket === ticketId);

      document.getElementById('modalStudent').innerText = ticket.student;
      document.getElementById('modalTicketId').innerText = `Ticket #${ticket.ticket} (${ticket.type})`;
      document.getElementById('modalSummary').innerText = `Total de respuestas emitidas: ${events.length} envíos`;

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
          intervalText = 'Primer envío';
        }

        item.innerHTML = `
          <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center font-bold text-[11px]">${idx + 1}</span>
            <div>
              <span class="text-white font-medium">${ev.timestamp} UTC</span>
              <span class="text-[10px] text-slate-500 block">Asunto: Respuesta Solicitud de Trámite - Certificado</span>
            </div>
          </div>
          <span class="text-amber-400 text-xs font-semibold">${intervalText}</span>
        `;
        list.appendChild(item);
      });

      document.getElementById('ticketModal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('ticketModal').classList.add('hidden');
    }

    // Export CSV
    function exportDataCSV() {
      let csv = 'Ticket,Estudiante,Tipo de Certificado,# de Envios,Primer Envio (UTC),Ultimo Envio (UTC),Reprocesado\\n';
      rawData.tickets.forEach(t => {
        csv += `"${t.ticket}","${t.student}","${t.type}",${t.sends},"${t.first_send}","${t.last_send}","${t.reprocessed}"\\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Auditoria_Tickets_RPA_UMB.csv';
      a.click();
    }
  </script>
</body>
</html>
'''

# Write to DashboardUMB/index.html
with open('/Users/franciscomateus/Documents/DashboardUMB/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated /Users/franciscomateus/Documents/DashboardUMB/index.html successfully!")
