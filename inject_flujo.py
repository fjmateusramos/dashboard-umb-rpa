import re
import json

# Read current template
with open('/Users/franciscomateus/Documents/DashboardUMB/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 1. Add nav button
old_nav = '''<button onclick="switchTab('tab-telemetria')" id="btn-tab-telemetria" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-chart-line text-blue-400"></i> Telemetría & Gráficos
        </button>'''

new_nav = '''<button onclick="switchTab('tab-telemetria')" id="btn-tab-telemetria" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-chart-line text-blue-400"></i> Telemetría & Gráficos
        </button>
        <button onclick="switchTab('tab-flujo')" id="btn-tab-flujo" class="nav-tab px-3 py-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-transparent transition flex items-center gap-2 whitespace-nowrap">
          <i class="fa-solid fa-diagram-project text-teal-400"></i> Diagrama de Flujo Interactivo
        </button>'''

if old_nav in template:
    template = template.replace(old_nav, new_nav)
    print("Nav button added successfully!")
else:
    print("Warning: old_nav not found exactly, check nav markup")

# 2. Add Tab Content
# We will inject tab-flujo right before tab-codigo
flujo_tab_html = '''
    <!-- SECCIÓN: DIAGRAMA DE FLUJO INTERACTIVO (TAB FLUJO) -->
    <section id="tab-flujo" class="tab-content hidden space-y-6">
      
      <!-- Encabezado de la Sección -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-2.5 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/60 uppercase">
              Blue Prism Flow Engine
            </span>
            <span class="text-xs text-slate-400">Basado en PDD Versión 2 y Procesos 01 / 02</span>
          </div>
          <h2 class="text-xl font-extrabold text-white mt-1 flex items-center gap-2">
            <i class="fa-solid fa-diagram-project text-teal-400"></i> Diagrama de Flujo Interactivo: Procesos en Producción
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Explore el recorrido visual paso a paso, simule escenarios en tiempo real (éxito, admisiones y bucle de error) e inspeccione cada etapa técnica.
          </p>
        </div>

        <!-- Selector de Proceso -->
        <div class="flex items-center bg-slate-900 p-1.5 rounded-xl border border-slate-800">
          <button onclick="selectProcessFlow('p1')" id="btn-flow-p1" class="flow-proc-btn px-3 py-1.5 rounded-lg bg-teal-950 text-teal-300 border border-teal-700/60 font-semibold text-xs transition flex items-center gap-1.5">
            <i class="fa-solid fa-file-lines text-teal-400"></i> Proceso 01: Estudios & Admisión
          </button>
          <button onclick="selectProcessFlow('p2')" id="btn-flow-p2" class="flow-proc-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium text-xs transition flex items-center gap-1.5 ml-1">
            <i class="fa-solid fa-calendar-days text-amber-400"></i> Proceso 02: Horarios
          </button>
        </div>
      </div>

      <!-- Barra de Simulación Interactiva -->
      <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800 flex flex-wrap items-center justify-between gap-3 shadow-lg">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5 mr-1">
            <i class="fa-solid fa-play text-emerald-400"></i> Simulador:
          </span>
          <button onclick="runSimulation('success')" id="btn-sim-success" class="sim-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-emerald-950 hover:text-emerald-300 text-slate-200 border border-slate-700 hover:border-emerald-700 text-xs font-semibold transition flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. Caso Éxito (Matriculado)
          </button>
          <button onclick="runSimulation('admission')" id="btn-sim-admission" class="sim-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-purple-950 hover:text-purple-300 text-slate-200 border border-slate-700 hover:border-purple-700 text-xs font-semibold transition flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-purple-400"></span> 2. No Matriculado (Admisión Word)
          </button>
          <button onclick="runSimulation('loop')" id="btn-sim-loop" class="sim-btn px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-rose-950 hover:text-rose-300 text-slate-200 border border-slate-700 hover:border-rose-700 text-xs font-semibold transition flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span> 3. Excepción (Bucle Infinito 2h)
          </button>
          <button onclick="resetSimulation()" class="px-3 py-1.5 rounded-lg bg-slate-800/60 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 text-xs font-medium transition flex items-center gap-1">
            <i class="fa-solid fa-rotate-left"></i> Reiniciar
          </button>
        </div>

        <!-- Estado de Simulación -->
        <div id="simStatusBadge" class="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-mono flex items-center gap-1.5">
          <i class="fa-solid fa-circle-info text-slate-400"></i> Modo exploración: Haga clic en cualquier etapa
        </div>
      </div>

      <!-- ÁREA PRINCIPAL: DIAGRAMA (IZQUIERDA) + INSPECTOR (DERECHA) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- LIENZO DEL DIAGRAMA DE FLUJO (8 COLS) -->
        <div class="lg:col-span-7 xl:col-span-8 bg-slate-900/90 rounded-2xl p-5 border border-slate-800 overflow-hidden relative shadow-xl">
          
          <!-- Banner dinámico del proceso activo -->
          <div class="mb-4 pb-3 border-b border-slate-800 flex items-center justify-between">
            <div id="flowProcessBanner" class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-teal-400"></span>
              <strong class="text-sm text-white">Proceso 01 - Certificados de Estudios / Admisión</strong>
              <span class="text-[11px] text-slate-400 font-mono">(tramite = 'Certificado de Estudio')</span>
            </div>
            <div class="flex items-center gap-3 text-[11px] text-slate-400 font-mono">
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-cyan-500"></span> HubSpot</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-emerald-500"></span> AulaNet</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-purple-500"></span> Word VBO</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-rose-500"></span> Error / Loop</span>
            </div>
          </div>

          <!-- CONTENEDOR DE NODOS VERTICALES ESTRUCTURADOS -->
          <div id="flowCanvas" class="space-y-4 relative py-2">
            
            <!-- NODO 1: INICIO & SCHEDULER -->
            <div class="flex flex-col items-center">
              <div id="node-start" onclick="inspectStep('start')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-slate-700 hover:border-teal-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-teal-900/50 text-teal-300 border border-teal-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-clock"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-teal-300 transition">1. Inicio & Programación Operativa</h4>
                      <p class="text-[11px] text-slate-400">Scheduler ejecuta cada 2h (8:00 a 18:00 Lun-Sáb)</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">08, 10, 12, 14, 16, 18</span>
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
                        <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">2. Búsqueda de Tickets en HubSpot</h4>
                        <span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 border border-amber-800/50">Límite 100</span>
                      </div>
                      <p id="searchStepFilterText" class="text-[11px] text-slate-400 font-mono">Filtro: tramite = "Certificado de Estudio" & stage IN (1, 2)</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">REST API</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 3: DECISIÓN ENCARGADO DEL INSUMO -->
            <div class="flex flex-col items-center">
              <div id="node-encargado" onclick="inspectStep('encargado')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-amber-800/40 hover:border-amber-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-amber-950 text-amber-300 border border-amber-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-code-branch"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-amber-300 transition">3. ¿encargado_del_insumo_del_tramite vacío?</h4>
                      <p class="text-[11px] text-slate-400">Si tiene encargado asignado, se omite el ticket (manual)</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-amber-400">Decisión</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 4: AULANET LOGIN & ATTACH -->
            <div class="flex flex-col items-center">
              <div id="node-aulanet-login" onclick="inspectStep('aulanet-login')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-emerald-800/40 hover:border-emerald-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-arrow-right-to-bracket"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">4. Attach Chrome & Login AulaNet</h4>
                      <p class="text-[11px] text-slate-400">Apertura de sesión del robot en la interfaz web de AulaNet</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">UI Chrome</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 5: BIFURCACIÓN DE VALIDACIÓN Y BUCLE DE ERROR -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
              
              <!-- RAMA NORMAL: CONSULTA ESTUDIANTE -->
              <div class="flex flex-col items-center">
                <div id="node-consulta" onclick="inspectStep('consulta')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-emerald-800/50 hover:border-emerald-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold text-emerald-400 uppercase">Cédula válida (SÍ)</span>
                    <span class="text-[10px] font-mono text-slate-400">Consulta Estudiante</span>
                  </div>
                  <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">5. Consulta Académica en AulaNet</h4>
                  <p class="text-[11px] text-slate-400 mt-0.5">Extrae historial de notas en colección <code class="text-amber-300">Tabla</code></p>
                </div>
                <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
              </div>

              <!-- RAMA DE ERROR / TRAMPA DEL BUCLE INFINITO -->
              <div class="flex flex-col items-center">
                <div id="node-error-loop" onclick="inspectStep('error-loop')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-red-950/40 border border-red-700/60 hover:border-red-400 transition shadow-md relative group">
                  <div class="absolute -top-2.5 right-3 px-2 py-0.2 bg-red-700 text-white font-bold text-[9px] rounded-full uppercase tracking-wider animate-pulse">
                    Falla de Arquitectura
                  </div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-bold text-rose-400 uppercase">Cédula Vacía o Sin Notas</span>
                    <i class="fa-solid fa-repeat text-rose-400 text-xs"></i>
                  </div>
                  <h4 class="text-xs font-bold text-red-300 group-hover:text-white transition">Ruta de Excepción: Bucle Infinito</h4>
                  <p class="text-[11px] text-slate-300 mt-0.5 leading-tight">
                    Envía correo de error pero <strong>NO actualiza etapa en HubSpot</strong>. Salta a fin de loop y <strong>se re-ejecuta cada 2h</strong>.
                  </p>
                </div>
                <!-- Flecha de retorno curva al inicio -->
                <div class="text-[10px] font-mono text-rose-400 mt-1 flex items-center gap-1">
                  <i class="fa-solid fa-arrow-turn-up fa-rotate-270"></i> Vuelve a cola HubSpot (+2h)
                </div>
              </div>

            </div>

            <!-- NODO 6: EVALUACIÓN DE MATRÍCULA (BIFURCACIÓN ESTUDIOS VS ADMISIÓN) -->
            <div class="flex flex-col items-center pt-2">
              <div id="node-matricula" onclick="inspectStep('matricula')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-amber-700/60 hover:border-amber-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-amber-900/40 text-amber-300 border border-amber-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-user-check"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-amber-300 transition">6. ¿Tabla.Estado = "Matriculado"?</h4>
                      <p class="text-[11px] text-slate-400">Evalúa registro <code class="text-amber-300">[Count Tabla] - 1</code></p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">Decisión</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 7: BIFURCACIÓN DE GENERACIÓN DE CERTIFICADO -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
              
              <!-- RAMA SÍ: AULANET CERTIFICADO -->
              <div class="flex flex-col items-center">
                <div id="node-gen-aulanet" onclick="inspectStep('gen-aulanet')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-emerald-800/60 hover:border-emerald-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-bold text-emerald-400 uppercase">Estado = "Matriculado"</span>
                    <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">AulaNet UI</span>
                  </div>
                  <h4 id="genAulanetTitle" class="text-xs font-bold text-white group-hover:text-emerald-300 transition">7A. Generar Certificado de Estudios</h4>
                  <p class="text-[11px] text-slate-400 mt-0.5">Invoca acción en AulaNet con Cédula y Período, descarga PDF en disco local.</p>
                </div>
                <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
              </div>

              <!-- RAMA NO: PLANTILLA WORD ADMISIÓN -->
              <div class="flex flex-col items-center">
                <div id="node-gen-word" onclick="inspectStep('gen-word')" class="flow-node cursor-pointer w-full p-3.5 rounded-xl bg-slate-950 border border-purple-800/60 hover:border-purple-400 transition shadow-md group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-bold text-purple-400 uppercase">Estado &ne; "Matriculado"</span>
                    <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-purple-950 text-purple-300 border border-purple-800">MS Word VBO</span>
                  </div>
                  <h4 id="genWordTitle" class="text-xs font-bold text-white group-hover:text-purple-300 transition">7B. Generar Certificado de Admisión</h4>
                  <p id="genWordSubtitle" class="text-[11px] text-slate-400 mt-0.5">Abre plantilla Word, reemplaza marcadores, guarda DOCX y exporta PDF.</p>
                </div>
                <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
              </div>

            </div>

            <!-- NODO 8: ACTUALIZACIÓN DE TICKET HUBSPOT -->
            <div class="flex flex-col items-center">
              <div id="node-update-ticket" onclick="inspectStep('update-ticket')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-cyan-800/50 hover:border-cyan-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-pen-to-square"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">8. Actualizar Ticket en HubSpot (PATCH)</h4>
                      <p class="text-[11px] text-slate-400 font-mono">hs_pipeline_stage = "4" & cierre = "Procesado por Blue Prism"</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">PATCH</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 9: CARGA PRIVADA DE ARCHIVO A HUBSPOT FILES -->
            <div class="flex flex-col items-center">
              <div id="node-upload-file" onclick="inspectStep('upload-file')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-cyan-800/50 hover:border-cyan-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-cloud-arrow-up"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-cyan-300 transition">9. Subida Multipart a HubSpot Files</h4>
                      <p class="text-[11px] text-slate-400 font-mono">Carga PDF en carpeta /BluePrism (acceso PRIVATE) &rarr; Obtiene fileId</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">fileId</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 10: RESPUESTA AL ESTUDIANTE VÍA CONVERSATIONS API -->
            <div class="flex flex-col items-center">
              <div id="node-conversations" onclick="inspectStep('conversations')" class="flow-node cursor-pointer w-full max-w-md p-3.5 rounded-xl bg-slate-950 border border-emerald-700/60 hover:border-emerald-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700/50 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-paper-plane"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-emerald-300 transition">10. Envío de Respuesta al Estudiante</h4>
                      <p class="text-[11px] text-slate-400">HubSpot Conversations API: Adjunta PDF usando <code class="text-amber-300">fileId</code> y envía HTML</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">Salida Exitosa</span>
                </div>
              </div>
              <div class="h-5 w-0.5 bg-slate-700 connector-line"></div>
            </div>

            <!-- NODO 11: NOTIFICACIÓN INTERNA SMTP & CIERRE -->
            <div class="flex flex-col items-center">
              <div id="node-smtp" onclick="inspectStep('smtp')" class="flow-node cursor-pointer w-full max-w-md p-3 rounded-xl bg-slate-950 border border-slate-700 hover:border-slate-400 transition shadow-md group">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-slate-800 text-slate-300 border border-slate-700 flex items-center justify-center text-xs font-bold">
                      <i class="fa-solid fa-inbox"></i>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white group-hover:text-slate-200 transition">11. Notificación Interna SMTP a CASE</h4>
                      <p class="text-[11px] text-slate-400 font-mono">Envío a cesar.plata@umb.edu.co & coord.case@umb.edu.co</p>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">Gmail SMTP</span>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- PANEL LATERAL: INSPECTOR TÉCNICO DE ETAPAS (4 COLS) -->
        <div class="lg:col-span-5 xl:col-span-4 space-y-4 sticky top-24">
          
          <div class="bg-slate-900/95 rounded-2xl p-5 border border-slate-800 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-teal-400"></span>
                <h3 class="text-sm font-bold text-white">Inspector de Etapa</h3>
              </div>
              <span id="inspectStageCategory" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                Selección manual
              </span>
            </div>

            <div id="stageInspectorContent" class="space-y-3">
              <!-- Content rendered dynamically via JS -->
              <div>
                <h4 id="inspectStageName" class="text-base font-extrabold text-teal-300">Haga clic en una etapa del diagrama</h4>
                <p id="inspectStageDesc" class="text-xs text-slate-400 mt-1">
                  Seleccione cualquier bloque del flujo o ejecute una de las simulaciones superiores para ver los detalles técnicos, objetos de Blue Prism, datos de entrada y hallazgos forenses asociados.
                </p>
              </div>

              <div id="inspectDetailsBox" class="hidden space-y-2.5 pt-2 border-t border-slate-800/80 text-xs">
                <div>
                  <span class="text-slate-400 block text-[11px] font-semibold uppercase">Objeto / VBO Blue Prism:</span>
                  <code id="inspectVBO" class="text-amber-300 font-mono text-[11px] bg-slate-950 px-2 py-0.5 rounded block mt-0.5 border border-slate-800"></code>
                </div>

                <div>
                  <span class="text-slate-400 block text-[11px] font-semibold uppercase">Acción o Expresión:</span>
                  <p id="inspectAction" class="text-slate-200 text-xs mt-0.5"></p>
                </div>

                <div>
                  <span class="text-slate-400 block text-[11px] font-semibold uppercase">Propiedades / Variables Clave:</span>
                  <div id="inspectVariables" class="font-mono text-[11px] text-cyan-300 space-y-0.5 mt-0.5"></div>
                </div>

                <div id="inspectAuditAlert" class="p-3 rounded-xl bg-red-950/40 border border-red-800/60 text-xs text-red-200 space-y-1 mt-2">
                  <div class="flex items-center gap-1.5 font-bold text-rose-300">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>Hallazgo de Auditoría:</span>
                  </div>
                  <p id="inspectAuditText" class="text-[11px] text-slate-300 leading-relaxed"></p>
                </div>
              </div>
            </div>

          </div>

          <!-- Tarjeta de Referencia Rápida -->
          <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800 text-xs space-y-2 text-slate-400">
            <h4 class="font-bold text-white flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-400"></i> ¿Por qué se produce el bucle de 15 envíos?
            </h4>
            <p class="leading-relaxed text-[11px]">
              Al fallar la validación de documento o no encontrar notas, el robot ejecuta la acción de envío SMTP pero <strong class="text-white">omite invocar el PATCH en HubSpot</strong>. Como el ticket sigue en <code class="text-amber-300">hs_pipeline_stage = 1 o 2</code>, la búsqueda inicial lo vuelve a recuperar exactamente 2 horas después en la siguiente pasada programada.
            </p>
          </div>

        </div>

      </div>

    </section>
'''

if '<!-- SECCIÓN 4: AUDITORÍA DE CÓDIGO BLUE PRISM (TAB 4) -->' in template:
    template = template.replace('<!-- SECCIÓN 4: AUDITORÍA DE CÓDIGO BLUE PRISM (TAB 4) -->', flujo_tab_html + '\n    <!-- SECCIÓN 4: AUDITORÍA DE CÓDIGO BLUE PRISM (TAB 4) -->')
    print("Flujo tab HTML injected successfully!")
else:
    print("Warning: tab-codigo comment not found")

# 3. Add Flowchart Logic to JavaScript section
flujo_js = '''
    // ==========================================
    // DIAGRAMA DE FLUJO INTERACTIVO & SIMULADOR
    // ==========================================
    let currentProcessFlow = 'p1'; // 'p1' or 'p2'
    let activeSimulationTimer = null;

    const stageCatalog = {
      'start': {
        name: 'Inicio & Programación Operativa',
        category: 'Scheduler / Orquestación',
        vbo: 'Blue Prism Scheduler Service',
        action: 'Disparo recurrente cada 2 horas (08:00, 10:00, 12:00, 14:00, 16:00, 18:00)',
        vars: ['Ventana operativa: 8:00 a.m. a 6:00 p.m.', 'Días: Lunes a Sábado', 'Servidor: GCP VM (NBI)'],
        audit: 'La programación operativa se ejecuta en la máquina cloud provista por NBI. En caso de corte o falta de pago de la VM, las ejecuciones se detienen sin respaldo en la UMB.'
      },
      'search': {
        name: 'Búsqueda de Tickets en HubSpot',
        category: 'Integración CRM / Carga de Cola',
        vbo: 'Utility - HTTP::HTTP Request',
        action: 'POST https://api.hubapi.com/crm/objects/2026-03/tickets/search',
        vars: ['filterGroups: tramite EQ [Trámite]', 'hs_pipeline_stage EQ "1" y "2" (combinados)', 'limit: 100 (sin paginación)'],
        audit: 'CRÍTICO: Límite fijo de 100 tickets por búsqueda sin paginación (offset after). Si hay >100 tickets en cola, los excedentes quedan desatendidos indefinidamente.'
      },
      'encargado': {
        name: '¿encargado_del_insumo_del_tramite vacío?',
        category: 'Regla de Decisión',
        vbo: 'Decision Stage',
        action: 'Evalúa si la propiedad encargado_del_insumo_del_tramite = ""',
        vars: ['True: Continúa a proceso automático', 'False: Omitir ticket y continuar (gestión manual)'],
        audit: 'Control funcional para evitar que el robot procese tickets que ya están siendo atendidos manualmente por funcionarios del CASE.'
      },
      'aulanet-login': {
        name: 'Attach Chrome & Login AulaNet',
        category: 'Automatización UI Web',
        vbo: 'Crome - AulaNET::Attach / Login',
        action: 'Adjuntar instancia activa de Google Chrome y ejecutar Login en AulaNet',
        vars: ['Navegador: Google Chrome', 'Target: Portal AulaNet UMB'],
        audit: 'Depende de selectores UI web. Si AulaNet cambia su interfaz o muestra un modal inesperado, el robot requiere bloques Recover/Resume para no colapsar.'
      },
      'consulta': {
        name: 'Consulta Estudiante en AulaNet',
        category: 'Consulta Académica',
        vbo: 'Crome - AulaNET::Consulta Estudiante',
        action: 'Busca al estudiante por cédula y recupera la tabla histórica de materias',
        vars: ['Input: Properties.documento_de_identificacion_nit', 'Output: Tabla (Asignatura, Estado, Periodo)', 'Output: Result (Texto resultado)'],
        audit: 'Si el resultado queda vacío (estudiante no existe o sin registros), el proceso toma la ruta de error.'
      },
      'error-loop': {
        name: 'Ruta de Excepción: Bucle Infinito (2h)',
        category: 'Falla Crítica de Arquitectura',
        vbo: 'Email - POP3/SMTP::Send Message',
        action: 'Envía correo de error a CASE pero NO actualiza etapa en HubSpot',
        vars: ['Destinatario: cesar.plata@umb.edu.co, coord.case@umb.edu.co', 'Cédula de error quemada: C:\\\\UMB\\\\...\\\\certificado_estudio_1066599028.pdf', 'HubSpot PATCH: ¡OMITIDO!'],
        audit: 'CAUSA RAÍZ DEL SPAM: El ticket permanece en etapa 1 o 2 en HubSpot. El robot lo vuelve a buscar a las 2 horas y envía otro correo de error. Generó hasta 15 correos repetidos por estudiante.'
      },
      'matricula': {
        name: '¿Tabla.Estado = "Matriculado"?',
        category: 'Regla de Decisión Académica',
        vbo: 'Decision Stage (Tabla.Estado = "Matriculado")',
        action: 'Copia fila [Count Tabla] - 1 y evalúa el campo Estado',
        vars: ['True: Generar Certificado AulaNet', 'False: Rama de Admisión Word'],
        audit: 'Selecciona ciegamente la última fila de la colección sin validar si ese registro corresponde realmente al período académico vigente.'
      },
      'gen-aulanet': {
        name: 'Generar Certificado en AulaNet',
        category: 'Generación Oficial de Documento',
        vbo: 'Crome - AulaNET::Generar Certificado',
        action: 'Descarga el PDF generado oficialmente desde el sistema académico',
        vars: ['Cédula: [Properties.documento_de_identificacion_nit]', 'Período: [Tabla.Periodo]', 'Ruta local: C:\\\\UMB\\\\Certificados de Estudio\\\\certificado_estudio_<nit>.pdf'],
        audit: 'En Horarios (Proceso 02), guarda el archivo con el nombre "certificado_estudio_<nit>.pdf" en la carpeta de Certificados de Estudio por copia de código.'
      },
      'gen-word': {
        name: 'Generar Certificado de Admisión (Word)',
        category: 'Generación Local vía MS Word',
        vbo: 'MS Word VBO::Open / Find Text / Type Text / ExportPDF',
        action: 'Abre plantilla Word, busca marcadores (NOMBRE, IDENTIFICACION, PROGRAMA) y exporta PDF',
        vars: ['Plantilla: C:\\\\UMB\\\\Templates\\\\PLANTILLA ADMITIDO WORD.docx', 'Programa quemado: pregrado_presencial_bogota'],
        audit: 'BUG DE HORARIOS: Si en el Proceso 02 el alumno no está matriculado, ¡este paso le genera una carta de admisión a Pregrado Bogotá por error!'
      },
      'update-ticket': {
        name: 'Actualizar Ticket en HubSpot (PATCH)',
        category: 'Actualización CRM',
        vbo: 'Utility - HTTP::HTTP Request (PATCH)',
        action: 'Marca el ticket como cerrado y asigna etapa 4',
        vars: ['hs_pipeline_stage: "4"', 'respuesta_o_correo_de_cierre: "Procesado por Blue Prism"', 'hubspot_owner_id: "25085377"'],
        audit: 'Esta llamada solo se ejecuta en la ruta exitosa. Nunca se llama en la ruta de excepción, lo que causa el bucle.'
      },
      'upload-file': {
        name: 'Subida Multipart a HubSpot Files',
        category: 'Almacenamiento Cloud CRM',
        vbo: 'Utility - HTTP::HTTP Request Multipart',
        action: 'Sube el archivo PDF a la carpeta privada /BluePrism de HubSpot',
        vars: ['Endpoint: https://api.hubapi.com/files/v3/files', 'Carpeta: /BluePrism', 'Access: PRIVATE', 'Output: fileId'],
        audit: 'El token Bearer privado de HubSpot se pasa como Header. En el proceso original, dicho token estaba expuesto en texto plano.'
      },
      'conversations': {
        name: 'Envío de Respuesta vía Conversations API',
        category: 'Atención al Estudiante',
        vbo: 'Utility - HTTP::HTTP Request (POST)',
        action: 'Publica mensaje en el hilo del ticket con el PDF adjunto usando fileId',
        vars: ['Thread ID: [Thread.results.id]', 'Recipient: [Ticket Details.properties.correo]', 'Attachment: [UploadFile.id]'],
        audit: 'Canal oficial de respuesta al estudiante integrado con la bandeja omnicanal de HubSpot.'
      },
      'smtp': {
        name: 'Notificación Interna SMTP a CASE',
        category: 'Notificación de Auditoría',
        vbo: 'Email - POP3/SMTP::Send Message',
        action: 'Envía copia de respaldo con el PDF adjunto a los coordinadores de CASE',
        vars: ['From: pruebas_umb@narnajabi.com', 'To: cesar.plata@umb.edu.co, director.case@umb.edu.co, coord.case@umb.edu.co'],
        audit: 'Utiliza credenciales SMTP de Gmail en texto plano. Se recomienda migrar a envío autenticado corporativo o centralizar en HubSpot.'
      }
    };

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
        aulanetTitle.innerText = '7A. Generar Certificado de Estudios';
        wordTitle.innerText = '7B. Generar Certificado de Admisión';
        wordSubtitle.innerText = 'Abre plantilla Word, reemplaza marcadores, guarda DOCX y exporta PDF.';
        inspectStep('search');
      } else {
        btnP2.className = 'flow-proc-btn px-3 py-1.5 rounded-lg bg-amber-950 text-amber-300 border border-amber-700/60 font-semibold text-xs transition flex items-center gap-1.5 ml-1';
        btnP1.className = 'flow-proc-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium text-xs transition flex items-center gap-1.5';
        banner.innerHTML = `<span class="w-3 h-3 rounded-full bg-amber-400"></span><strong class="text-sm text-white">Proceso 02 - Certificado de Horarios</strong> <span class="text-[11px] text-slate-400 font-mono">(tramite = 'Certificado de Horarios')</span>`;
        searchFilter.innerText = 'Filtro: tramite = "Certificado de Horarios" & stage IN (1, 2)';
        aulanetTitle.innerText = '7A. Generar Certificado de Horarios';
        wordTitle.innerText = '7B. Rama Admisión Word (¡BUG DE CLONACIÓN!)';
        wordSubtitle.innerText = '¡Alerta! Si no está matriculado, genera por error Certificado de Admisión Bogotá.';
        inspectStep('gen-word');
      }
    }

    function inspectStep(stepId) {
      const data = stageCatalog[stepId];
      if (!data) return;

      // Update inspector UI
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

      // Visual highlight of active node
      document.querySelectorAll('.flow-node').forEach(node => {
        node.classList.remove('ring-2', 'ring-teal-400', 'ring-amber-400', 'ring-rose-500', 'bg-slate-900');
      });
      const activeNode = document.getElementById('node-' + stepId);
      if (activeNode) {
        activeNode.classList.add('ring-2', stepId === 'error-loop' ? 'ring-rose-500' : 'ring-teal-400', 'bg-slate-900');
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
        badge.innerHTML = `<span class="relative flex h-2 w-2 mr-1"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span></span> Simulando: Caso No Matriculado (Admisión Word)...`;
        badge.className = 'text-xs px-3 py-1 rounded-full bg-purple-950 text-purple-300 border border-purple-700 font-mono flex items-center';
        steps = ['start', 'search', 'encargado', 'aulanet-login', 'consulta', 'matricula', 'gen-word', 'update-ticket', 'upload-file', 'conversations', 'smtp'];
      } else if (scenario === 'loop') {
        badge.innerHTML = `<span class="relative flex h-2 w-2 mr-1"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span></span> Simulando: Fallo de Cédula &rarr; Bucle Infinito cada 2h...`;
        badge.className = 'text-xs px-3 py-1 rounded-full bg-red-950 text-red-300 border border-red-700 font-mono flex items-center';
        steps = ['start', 'search', 'encargado', 'aulanet-login', 'error-loop', 'search', 'error-loop'];
      }

      let currentStepIdx = 0;
      activeSimulationTimer = setInterval(() => {
        if (currentStepIdx >= steps.length) {
          clearInterval(activeSimulationTimer);
          if (scenario === 'loop') {
            badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-rose-400 mr-1"></i> Bucle confirmado: Sin PATCH en HubSpot, el ticket se vuelve a procesar a las 2h`;
          } else {
            badge.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400 mr-1"></i> Simulación finalizada exitosamente`;
          }
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
        node.classList.remove('ring-2', 'ring-teal-400', 'ring-amber-400', 'ring-rose-500', 'bg-slate-900');
      });
      document.getElementById('simStatusBadge').innerHTML = `<i class="fa-solid fa-circle-info text-slate-400 mr-1"></i> Modo exploración: Haga clic en cualquier etapa`;
      document.getElementById('simStatusBadge').className = 'text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700 font-mono flex items-center';
    }
'''

# Add to the script section before the closing </script>
if '// Embedded Data from Python Parser' in template:
    template = template.replace('// Embedded Data from Python Parser', flujo_js + '\n    // Embedded Data from Python Parser')
    print("Flujo JS added successfully!")
else:
    print("Warning: JS marker not found")

# Write updated template
with open('/Users/franciscomateus/Documents/DashboardUMB/template.html', 'w', encoding='utf-8') as f:
    f.write(template)

print("Updated template.html successfully!")
