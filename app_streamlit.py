import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import pulp

# Configuración de página
st.set_page_config(
    page_title="Optimizador de Muestreo Científico",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="main-header">🔬 Optimizador de Estrategia de Muestreo</div>', 
            unsafe_allow_html=True)
st.markdown("**Círculos de Hadas** - Modelo MILP de Programación Lineal Entera Mixta")

# ============================================================================
# FUNCIONES DEL MODELO
# ============================================================================

def crear_modelo_optimizacion(params):
    """Crea y resuelve el modelo MILP"""
    
    circulos = params['circulos']
    separaciones = params['separaciones']
    tipos_lab = params['tipos_lab']
    
    T_total = params['T_total']
    h_dia = params['h_dia']
    t_std = params['t_std']
    t_multi = params['t_multi']
    t_24h = params['t_24h']
    t_extendida = params['t_extendida']
    
    B_total = params['B_total']
    costo_diario = params['costo_diario']
    costo_lab = params['costo_lab']
    
    min_multi_por_circulo = params['min_multi_por_circulo']
    min_24h_total = params['min_24h_total']
    min_ext_total = params['min_ext_total']
    min_lab_por_tipo = params['min_lab_por_tipo']
    E_max = params['E_max']
    
    pesos = params['pesos']
    perimetros = params['perimetros']
    
    modelo = pulp.LpProblem("Optimizacion_Muestreo", pulp.LpMaximize)
    
    # Variables
    x = {(i, s): pulp.LpVariable(f"sep_{i}_{s}", cat='Binary') 
         for i in circulos for s in separaciones}
    m = {i: pulp.LpVariable(f"multinivel_{i}", lowBound=0, cat='Integer') 
         for i in circulos}
    E = pulp.LpVariable("equipos", lowBound=1, upBound=E_max, cat='Integer')
    H = pulp.LpVariable("horas_hombre", lowBound=0, cat='Integer')
    M_24h = pulp.LpVariable("mediciones_24h", lowBound=0, cat='Integer')
    M_ext = pulp.LpVariable("mediciones_extendidas", lowBound=0, cat='Integer')
    L = {k: pulp.LpVariable(f"lab_{k}", lowBound=0, cat='Integer') 
         for k in tipos_lab}
    
    # Puntos estándar calculados
    n_std = {}
    for i in circulos:
        for s in separaciones:
            n_std[(i, s)] = int(perimetros[i] / s) if s > 0 else 0
    
    # Función objetivo
    calidad = (pulp.lpSum([pesos['std'] * n_std[(i, s)] * x[(i, s)] 
                           for i in circulos for s in separaciones]) +
              pulp.lpSum([pesos['multi'] * m[i] for i in circulos]) +
              pesos['24h'] * M_24h +
              pesos['ext'] * M_ext +
              pulp.lpSum([pesos['lab'][k] * L[k] for k in tipos_lab]))
    
    modelo += calidad, "Calidad_Cientifica"
    
    # Restricciones
    for i in circulos:
        for s in separaciones:
            modelo += (H >= (n_std[(i, s)] * t_std + m[i] * t_multi + 
                           M_24h * t_24h + M_ext * t_extendida - 
                           10000 * (1 - x[(i, s)])),
                      f"esfuerzo_{i}_{s}")
    
    dias_disponibles = T_total / h_dia
    modelo += H <= E * dias_disponibles * h_dia, "capacidad_tiempo"
    
    costo_total = (E * costo_diario * dias_disponibles +
                   pulp.lpSum([L[k] * costo_lab[k] for k in tipos_lab]))
    modelo += costo_total <= B_total, "presupuesto"
    
    for i in circulos:
        modelo += pulp.lpSum([x[(i, s)] for s in separaciones]) == 1, f"selec_sep_{i}"
    
    modelo += M_24h >= min_24h_total, "min_24h"
    modelo += M_ext >= min_ext_total, "min_ext"
    
    for k in tipos_lab:
        modelo += L[k] >= min_lab_por_tipo[k], f"min_lab_{k}"
    
    for i in circulos:
        modelo += m[i] >= min_multi_por_circulo, f"min_multi_{i}"
    
    return modelo, x, m, E, H, M_24h, M_ext, L, n_std, dias_disponibles


def procesar_resultados(modelo, params, x, m, E, H, M_24h, M_ext, L, n_std, dias_disponibles):
    """Procesa los resultados del modelo"""
    
    resultados = {
        'status': pulp.LpStatus[modelo.status],
        'calidad_total': float(pulp.value(modelo.objective)),
        'recursos_utilizados': {},
        'estrategia_por_circulo': {},
        'mediciones': {},
        'laboratorio': {}
    }
    
    equipos = int(E.varValue) if E.varValue else 1
    horas_total = int(H.varValue) if H.varValue else 0
    dias_usados = horas_total / params['h_dia'] / equipos if equipos > 0 else 0
    
    costo_campo = equipos * params['costo_diario'] * dias_disponibles
    costo_lab_total = sum(L[k].varValue * params['costo_lab'][k] 
                         for k in params['tipos_lab'] if L[k].varValue)
    costo_total = costo_campo + costo_lab_total
    
    resultados['recursos_utilizados'] = {
        'equipos_trabajo': equipos,
        'horas_hombre': horas_total,
        'dias_estimados': round(dias_usados, 1),
        'costo_campo': round(costo_campo, 2),
        'costo_laboratorio': round(costo_lab_total, 2),
        'costo_total': round(costo_total, 2),
        'presupuesto_disponible': params['B_total'],
        'presupuesto_utilizado_%': round(100 * costo_total / params['B_total'], 1)
    }
    
    for i in params['circulos']:
        for s in params['separaciones']:
            if x[(i, s)].varValue == 1:
                n_puntos = n_std[(i, s)]
                m_puntos = int(m[i].varValue) if m[i].varValue else 0
                resultados['estrategia_por_circulo'][i] = {
                    'separacion_m': s,
                    'puntos_estandar': n_puntos,
                    'puntos_multinivel': m_puntos,
                    'puntos_totales': n_puntos + m_puntos
                }
    
    resultados['mediciones'] = {
        'mediciones_24h': int(M_24h.varValue) if M_24h.varValue else 0,
        'mediciones_extendidas': int(M_ext.varValue) if M_ext.varValue else 0,
    }
    resultados['mediciones']['total_mediciones'] = (
        resultados['mediciones']['mediciones_24h'] + 
        resultados['mediciones']['mediciones_extendidas']
    )
    
    for k in params['tipos_lab']:
        resultados['laboratorio'][k] = int(L[k].varValue) if L[k].varValue else 0
    resultados['laboratorio']['total'] = sum([v for k, v in resultados['laboratorio'].items()])
    
    return resultados


# ============================================================================
# INTERFAZ STREAMLIT
# ============================================================================

# Sidebar: Carga de parámetros
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Opción: Cargar ejemplo o personalizado
    modo = st.radio("Selecciona modo:", ["Usar Ejemplo", "Personalizado"], horizontal=True)
    
    if modo == "Usar Ejemplo":
        params = {
            'circulos': ['HF_001', 'HF_002', 'HF_003'],
            'perimetros': {'HF_001': 1500, 'HF_002': 2000, 'HF_003': 1800},
            'separaciones': [50, 75, 100, 150],
            'T_total': 480,
            'h_dia': 8,
            't_std': 2,
            't_multi': 4,
            't_24h': 24,
            't_extendida': 72,
            'B_total': 50000,
            'costo_diario': 200,
            'costo_lab': {
                'mineralogico': 150,
                'biogeoquimico': 200,
                'cromatografia': 250,
                'deuterio': 300,
                'helio': 350
            },
            'tipos_lab': ['mineralogico', 'biogeoquimico', 'cromatografia', 'deuterio', 'helio'],
            'min_multi_por_circulo': 3,
            'min_24h_total': 5,
            'min_ext_total': 2,
            'min_lab_por_tipo': {
                'mineralogico': 5,
                'biogeoquimico': 4,
                'cromatografia': 3,
                'deuterio': 2,
                'helio': 2
            },
            'E_max': 4,
            'pesos': {
                'std': 1.0,
                'multi': 1.5,
                '24h': 2.0,
                'ext': 2.5,
                'lab': {
                    'mineralogico': 1.2,
                    'biogeoquimico': 1.5,
                    'cromatografia': 1.8,
                    'deuterio': 2.0,
                    'helio': 2.2
                }
            }
        }
        st.success("✓ Parámetros de ejemplo cargados")
    
    else:
        st.subheader("Geometría y Tiempo")
        num_circulos = st.slider("Número de círculos", 1, 5, 3)
        perimetros_input = {}
        for i in range(num_circulos):
            perimetros_input[f'HF_{i+1:03d}'] = st.number_input(
                f"Perímetro círculo {i+1} (m)", 1000, 5000, 1500
            )
        
        separaciones_input = st.multiselect(
            "Separaciones permitidas (m)",
            [25, 50, 75, 100, 125, 150, 200],
            default=[50, 75, 100, 150]
        )
        
        T_total = st.number_input("Tiempo total disponible (horas)", 100, 1000, 480)
        h_dia = st.number_input("Horas de trabajo por día", 4, 12, 8)
        
        st.subheader("Presupuesto")
        B_total = st.number_input("Presupuesto total (USD)", 10000, 200000, 50000)
        costo_diario = st.number_input("Costo diario de campo (USD)", 50, 500, 200)
        
        # Parámetros simplificados
        params = {
            'circulos': list(perimetros_input.keys()),
            'perimetros': perimetros_input,
            'separaciones': sorted(separaciones_input),
            'T_total': T_total,
            'h_dia': h_dia,
            't_std': 2,
            't_multi': 4,
            't_24h': 24,
            't_extendida': 72,
            'B_total': B_total,
            'costo_diario': costo_diario,
            'costo_lab': {
                'mineralogico': 150,
                'biogeoquimico': 200,
                'cromatografia': 250,
                'deuterio': 300,
                'helio': 350
            },
            'tipos_lab': ['mineralogico', 'biogeoquimico', 'cromatografia', 'deuterio', 'helio'],
            'min_multi_por_circulo': 3,
            'min_24h_total': 5,
            'min_ext_total': 2,
            'min_lab_por_tipo': {k: 2 for k in ['mineralogico', 'biogeoquimico', 'cromatografia', 'deuterio', 'helio']},
            'E_max': 4,
            'pesos': {
                'std': 1.0,
                'multi': 1.5,
                '24h': 2.0,
                'ext': 2.5,
                'lab': {k: 1.0 for k in ['mineralogico', 'biogeoquimico', 'cromatografia', 'deuterio', 'helio']}
            }
        }

# Botón para resolver
col1, col2 = st.columns(2)
with col1:
    resolver = st.button("🚀 Resolver Modelo", use_container_width=True, type="primary")
with col2:
    descargar_datos = st.button("💾 Descargar Configuración", use_container_width=True)

if descargar_datos:
    st.download_button(
        label="Descargar JSON",
        data=json.dumps(params, indent=2),
        file_name=f"config_muestreo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# ============================================================================
# RESOLUCIÓN Y RESULTADOS
# ============================================================================

if resolver:
    with st.spinner("🔄 Resolviendo modelo MILP..."):
        modelo, x, m, E, H, M_24h, M_ext, L, n_std, dias_disponibles = crear_modelo_optimizacion(params)
        status = modelo.solve(pulp.PULP_CBC_CMD(msg=0))
        resultados = procesar_resultados(modelo, params, x, m, E, H, M_24h, M_ext, L, n_std, dias_disponibles)
    
    # Mostrar estado
    if resultados['status'] == 'Optimal':
        st.markdown('<div class="success-box">✅ <b>Solución Óptima Encontrada</b></div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">⚠️ <b>Estado:</b>' + resultados['status'] + '</div>', 
                   unsafe_allow_html=True)
    
    # TABS para organizar resultados
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumen", "🗺️ Estrategia", "💰 Presupuesto", "📈 Gráficos"])
    
    with tab1:
        st.subheader("Indicadores Clave")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Calidad Total", f"{resultados['calidad_total']:.1f}")
        with col2:
            st.metric("Equipos", resultados['recursos_utilizados']['equipos_trabajo'])
        with col3:
            st.metric("Horas-Hombre", resultados['recursos_utilizados']['horas_hombre'])
        with col4:
            st.metric("Días", resultados['recursos_utilizados']['dias_estimados'])
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Mediciones de Larga Duración")
            med_df = pd.DataFrame({
                'Tipo': ['24 horas', 'Extendidas', 'Total'],
                'Cantidad': [
                    resultados['mediciones']['mediciones_24h'],
                    resultados['mediciones']['mediciones_extendidas'],
                    resultados['mediciones']['total_mediciones']
                ]
            })
            st.dataframe(med_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Análisis de Laboratorio")
            lab_data = {k: v for k, v in resultados['laboratorio'].items() if k != 'total'}
            lab_df = pd.DataFrame({
                'Tipo': list(lab_data.keys()),
                'Muestras': list(lab_data.values())
            })
            st.dataframe(lab_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Estrategia de Muestreo por Círculo")
        
        estrategia_df = pd.DataFrame([
            {
                'Círculo': k,
                'Separación (m)': v['separacion_m'],
                'Puntos Estándar': v['puntos_estandar'],
                'Puntos Multinivel': v['puntos_multinivel'],
                'Total Puntos': v['puntos_totales']
            }
            for k, v in resultados['estrategia_por_circulo'].items()
        ])
        
        st.dataframe(estrategia_df, use_container_width=True, hide_index=True)
        
        # Resumen total
        total_puntos = estrategia_df['Total Puntos'].sum()
        total_std = estrategia_df['Puntos Estándar'].sum()
        total_multi = estrategia_df['Puntos Multinivel'].sum()
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Puntos", total_puntos)
        col2.metric("Estándar", total_std)
        col3.metric("Multinivel", total_multi)
    
    with tab3:
        st.subheader("Análisis de Presupuesto")
        
        recursos = resultados['recursos_utilizados']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Presupuesto Total", f"${recursos['presupuesto_disponible']:,.0f}")
            st.metric("Costo de Campo", f"${recursos['costo_campo']:,.0f}")
            st.metric("Costo de Laboratorio", f"${recursos['costo_laboratorio']:,.0f}")
        
        with col2:
            st.metric("Costo Total Utilizado", f"${recursos['costo_total']:,.0f}", 
                     f"{recursos['presupuesto_utilizado_%']:.1f}%")
            st.metric("Presupuesto Disponible", f"${recursos['presupuesto_disponible'] - recursos['costo_total']:,.0f}")
        
        # Gráfico presupuesto
        st.markdown("---")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        categorias = ['Campo', 'Laboratorio', 'Disponible']
        montos = [
            recursos['costo_campo'],
            recursos['costo_laboratorio'],
            recursos['presupuesto_disponible'] - recursos['costo_total']
        ]
        colores = ['#3498db', '#e74c3c', '#95a5a6']
        
        bars = ax.bar(categorias, montos, color=colores, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('USD', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de Presupuesto', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Puntos por círculo
            fig, ax = plt.subplots(figsize=(10, 5))
            circulos_lista = list(resultados['estrategia_por_circulo'].keys())
            puntos_std = [resultados['estrategia_por_circulo'][c]['puntos_estandar'] for c in circulos_lista]
            puntos_multi = [resultados['estrategia_por_circulo'][c]['puntos_multinivel'] for c in circulos_lista]
            
            x_pos = np.arange(len(circulos_lista))
            ax.bar(x_pos, puntos_std, label='Estándar', alpha=0.8, color='steelblue')
            ax.bar(x_pos, puntos_multi, bottom=puntos_std, label='Multinivel', alpha=0.8, color='coral')
            ax.set_xlabel('Círculo', fontweight='bold')
            ax.set_ylabel('Número de Puntos', fontweight='bold')
            ax.set_title('Puntos de Muestreo por Círculo', fontweight='bold')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(circulos_lista)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            # Laboratorio
            fig, ax = plt.subplots(figsize=(10, 5))
            tipos = [k for k in resultados['laboratorio'].keys() if k != 'total']
            cantidades = [resultados['laboratorio'][t] for t in tipos]
            
            ax.barh(tipos, cantidades, color='mediumseagreen', edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Número de Muestras', fontweight='bold')
            ax.set_title('Análisis de Laboratorio', fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, v in enumerate(cantidades):
                ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
            
            st.pyplot(fig, use_container_width=True)
        
        # Mediciones de larga duración
        col3 = st.columns(1)[0]
        fig, ax = plt.subplots(figsize=(10, 5))
        
        med_tipos = ['24 horas', 'Extendidas']
        med_vals = [resultados['mediciones']['mediciones_24h'],
                   resultados['mediciones']['mediciones_extendidas']]
        colors_med = ['#3498db', '#9b59b6']
        
        bars = ax.bar(med_tipos, med_vals, color=colors_med, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Número de Mediciones', fontweight='bold')
        ax.set_title('Mediciones de Larga Duración', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   str(int(height)), ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        st.pyplot(fig, use_container_width=True)
    
    # Descarga de resultados
    st.divider()
    st.subheader("📥 Descargar Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_str = json.dumps(resultados, indent=2)
        st.download_button(
            label="📄 JSON",
            data=json_str,
            file_name=f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        csv_str = estrategia_df.to_csv(index=False)
        st.download_button(
            label="📊 CSV (Estrategia)",
            data=csv_str,
            file_name=f"estrategia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.markdown("""
        **Instrucciones para desplegar en Streamlit Cloud:**
        1. Sube los archivos a GitHub
        2. Ve a [streamlit.io](https://streamlit.io)
        3. Deploy directo desde tu repo
        """)

else:
    st.info("👈 Configura los parámetros en el panel izquierdo y haz clic en 'Resolver Modelo'")
