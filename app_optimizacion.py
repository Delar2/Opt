"""
APLICACIÓN DE OPTIMIZACIÓN DE ESTRATEGIAS DE MUESTREO
Versión: 1.0
Basada en modelo MILP (Mixed Integer Linear Programming)
"""

import streamlit as st
import pandas as pd
import numpy as np
from pulp import *
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Optimizador de Muestreo",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 Optimizador de Estrategias de Muestreo")
st.markdown("""
Esta aplicación resuelve un modelo de **Programación Lineal Entera Mixta (MILP)** 
para maximizar la calidad científica de tu estrategia de muestreo respetando 
restricciones de presupuesto y tiempo.
""")

# ============================================================================
# SIDEBAR - INPUTS GENERALES
# ============================================================================
with st.sidebar:
    st.header("⚙️ Configuración General")
    
    # Tiempo
    st.subheader("Parámetros de Tiempo")
    tiempo_total_dias = st.number_input(
        "Tiempo total disponible (días):", 
        min_value=1, max_value=365, value=30, step=1
    )
    horas_trabajo_diarias = st.number_input(
        "Horas efectivas de trabajo por día:", 
        min_value=1.0, max_value=24.0, value=8.0, step=0.5
    )
    
    # Presupuesto
    st.subheader("Presupuesto")
    presupuesto_total = st.number_input(
        "Presupuesto total (€):", 
        min_value=0, max_value=1000000, value=50000, step=1000
    )
    costo_diario_equipo = st.number_input(
        "Costo diario equipo (salarios, comida, hospedaje, transporte) (€):", 
        min_value=0, max_value=10000, value=500, step=50
    )
    
    # Mínimos generales
    st.subheader("Mínimos Requeridos Generales")
    min_mediciones_24h = st.number_input(
        "Mediciones de 24 horas mínimas:", 
        min_value=0, max_value=100, value=5, step=1
    )
    min_mediciones_extendidas = st.number_input(
        "Mediciones extendidas mínimas:", 
        min_value=0, max_value=100, value=3, step=1
    )
    
    # Equipos
    st.subheader("Recursos Humanos")
    num_equipos_max = st.number_input(
        "Cantidad máxima de equipos disponibles:", 
        min_value=1, max_value=20, value=3, step=1
    )

# ============================================================================
# MAIN - CONFIGURAR CÍRCULOS DE HADAS
# ============================================================================
st.header("📍 Configurar Círculos de Hadas")

col1, col2 = st.columns([2, 1])
with col1:
    num_circulos = st.number_input(
        "¿Cuántos círculos de hadas deseas muestrear?", 
        min_value=1, max_value=20, value=2, step=1
    )

# Almacenar datos de círculos
circulos_data = {}

tabs = st.tabs([f"Círculo {i+1}" for i in range(num_circulos)])

for idx, tab in enumerate(tabs):
    with tab:
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_circulo = st.text_input(
                "Nombre del círculo:", 
                value=f"Círculo_{idx+1}",
                key=f"nombre_circulo_{idx}"
            )
            perimetro = st.number_input(
                "Perímetro (metros):", 
                min_value=10, max_value=10000, value=500, step=10,
                key=f"perimetro_{idx}"
            )
        
        with col2:
            min_multinivel = st.number_input(
                "Puntos multinivel mínimos:", 
                min_value=0, max_value=50, value=2, step=1,
                key=f"min_multinivel_{idx}"
            )
        
        st.subheader("Opciones de Separación Entre Puntos")
        st.write("Define las distancias (en metros) que el modelo puede elegir para este círculo:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sep1 = st.number_input(
                "Separación 1 (m):", 
                min_value=10, max_value=1000, value=25, step=5,
                key=f"sep1_{idx}"
            )
        with col2:
            sep2 = st.number_input(
                "Separación 2 (m):", 
                min_value=10, max_value=1000, value=50, step=5,
                key=f"sep2_{idx}"
            )
        with col3:
            sep3 = st.number_input(
                "Separación 3 (m):", 
                min_value=10, max_value=1000, value=100, step=5,
                key=f"sep3_{idx}"
            )
        
        circulos_data[nombre_circulo] = {
            'perimetro': perimetro,
            'min_multinivel': min_multinivel,
            'separaciones': [sep1, sep2, sep3]
        }

# ============================================================================
# CONFIGURAR TIEMPOS DE MUESTREO
# ============================================================================
st.header("⏱️ Tiempos de Muestreo")

col1, col2, col3, col4 = st.columns(4)
with col1:
    tiempo_punto_standar = st.number_input(
        "Tiempo punto estándar (horas):", 
        min_value=0.1, max_value=10.0, value=1.0, step=0.1
    )
with col2:
    tiempo_punto_multinivel = st.number_input(
        "Tiempo punto multinivel (horas):", 
        min_value=0.1, max_value=10.0, value=2.0, step=0.1
    )
with col3:
    tiempo_medicion_24h = st.number_input(
        "Tiempo medición 24h (horas):", 
        min_value=0.5, max_value=50.0, value=24.0, step=0.5
    )
with col4:
    tiempo_medicion_extendida = st.number_input(
        "Tiempo medición extendida (horas):", 
        min_value=0.5, max_value=100.0, value=48.0, step=1.0
    )

# ============================================================================
# CONFIGURAR ANÁLISIS DE LABORATORIO
# ============================================================================
st.header("🧪 Análisis de Laboratorio")

analisis_tipos = ["Mineralógico", "Biogeoquímico", "Cromatografía", "Deuterio", "Helio"]
analisis_data = {}

col1, col2, col3 = st.columns(3)

for idx, analisis in enumerate(analisis_tipos):
    with [col1, col2, col3][idx % 3]:
        st.subheader(analisis)
        costo = st.number_input(
            f"Costo por muestra (€):", 
            min_value=0, max_value=10000, value=100 * (idx + 1), step=10,
            key=f"costo_analisis_{idx}"
        )
        min_muestras = st.number_input(
            f"Muestras mínimas:", 
            min_value=0, max_value=100, value=5, step=1,
            key=f"min_muestras_{idx}"
        )
        analisis_data[analisis] = {
            'costo': costo,
            'min_muestras': min_muestras
        }

# ============================================================================
# CONFIGURAR PESOS DE CALIDAD
# ============================================================================
st.header("⭐ Pesos de Calidad Científica (0-1)")
st.write("Asigna importancia relativa a cada tipo de muestreo. Mayor valor = mayor importancia.")

col1, col2, col3, col4, col5 = st.columns(5)

pesos = {}
with col1:
    pesos['punto_standar'] = st.slider(
        "Punto estándar:", min_value=0.0, max_value=1.0, value=0.3, step=0.1
    )
with col2:
    pesos['punto_multinivel'] = st.slider(
        "Punto multinivel:", min_value=0.0, max_value=1.0, value=0.6, step=0.1
    )
with col3:
    pesos['medicion_24h'] = st.slider(
        "Medición 24h:", min_value=0.0, max_value=1.0, value=0.8, step=0.1
    )
with col4:
    pesos['medicion_extendida'] = st.slider(
        "Medición extendida:", min_value=0.0, max_value=1.0, value=0.9, step=0.1
    )
with col5:
    pesos['laboratorio'] = st.slider(
        "Análisis laboratorio:", min_value=0.0, max_value=1.0, value=0.7, step=0.1
    )

# ============================================================================
# RESOLVER MODELO
# ============================================================================
if st.button("▶️ RESOLVER OPTIMIZACIÓN", type="primary", use_container_width=True):
    st.header("📊 Resultados de la Optimización")
    
    with st.spinner("Resolviendo modelo... esto puede tomar unos segundos..."):
        try:
            # Crear el problema
            prob = LpProblem("Optimizacion_Muestreo", LpMaximize)
            
            # ========== VARIABLES DE DECISIÓN ==========
            # Variables binarias para selección de separación
            x = {}  # x[circulo][separacion]
            for circulo in circulos_data.keys():
                for sep_idx, sep in enumerate(circulos_data[circulo]['separaciones']):
                    x[circulo, sep_idx] = LpVariable(f"x_{circulo}_{sep_idx}", cat='Binary')
            
            # Variables de muestreo
            y_multinivel = {}  # Puntos multinivel por círculo
            for circulo in circulos_data.keys():
                y_multinivel[circulo] = LpVariable(f"y_multinivel_{circulo}", lowBound=0, cat='Integer')
            
            # Variables globales
            total_mediciones_24h = LpVariable("total_24h", lowBound=0, cat='Integer')
            total_mediciones_extendidas = LpVariable("total_ext", lowBound=0, cat='Integer')
            num_equipos = LpVariable("num_equipos", lowBound=1, upBound=num_equipos_max, cat='Integer')
            total_horas_hombre = LpVariable("total_horas", lowBound=0, cat='Integer')
            
            # Variables de laboratorio
            muestras_lab = {}
            for analisis in analisis_tipos:
                muestras_lab[analisis] = LpVariable(f"muestras_{analisis}", lowBound=0, cat='Integer')
            
            # ========== FUNCIÓN OBJETIVO ==========
            # Contar puntos estándar por círculo y separación elegida
            objetivo = 0
            
            for circulo in circulos_data.keys():
                perimetro = circulos_data[circulo]['perimetro']
                for sep_idx, sep in enumerate(circulos_data[circulo]['separaciones']):
                    # Puntos estándar = perímetro / separación
                    puntos_standar = perimetro / sep
                    objetivo += pesos['punto_standar'] * puntos_standar * x[circulo, sep_idx]
                
                # Puntos multinivel
                objetivo += pesos['punto_multinivel'] * y_multinivel[circulo]
            
            # Mediciones 24h y extendidas
            objetivo += pesos['medicion_24h'] * total_mediciones_24h
            objetivo += pesos['medicion_extendida'] * total_mediciones_extendidas
            
            # Análisis de laboratorio
            for analisis in analisis_tipos:
                objetivo += pesos['laboratorio'] * muestras_lab[analisis]
            
            prob += objetivo, "Calidad_Cientifica"
            
            # ========== RESTRICCIONES ==========
            
            # R1: Definición de horas totales (aproximada)
            horas_trabajo_total = (tiempo_punto_standar * sum(
                (circulos_data[c]['perimetro'] / circulos_data[c]['separaciones'][s_idx]) * x[c, s_idx]
                for c in circulos_data.keys() 
                for s_idx in range(len(circulos_data[c]['separaciones']))
            ) + tiempo_punto_multinivel * sum(y_multinivel.values()) +
            tiempo_medicion_24h * total_mediciones_24h +
            tiempo_medicion_extendida * total_mediciones_extendidas)
            
            prob += horas_trabajo_total <= total_horas_hombre, "Horas_Definicion"
            
            # R2: Capacidad operativa
            prob += total_horas_hombre <= num_equipos * horas_trabajo_diarias * tiempo_total_dias, "Capacidad_Operativa"
            
            # R3: Presupuesto
            costo_lab = sum(analisis_data[analisis]['costo'] * muestras_lab[analisis] 
                           for analisis in analisis_tipos)
            costo_equipo = costo_diario_equipo * tiempo_total_dias
            prob += costo_lab + costo_equipo <= presupuesto_total, "Presupuesto"
            
            # R4: Selección única de separación por círculo
            for circulo in circulos_data.keys():
                prob += sum(x[circulo, s_idx] for s_idx in range(len(circulos_data[circulo]['separaciones']))) == 1, f"Separacion_unica_{circulo}"
            
            # R5: Mínimos de mediciones 24h
            prob += total_mediciones_24h >= min_mediciones_24h, "Min_24h"
            
            # R6: Mínimos de mediciones extendidas
            prob += total_mediciones_extendidas >= min_mediciones_extendidas, "Min_Extendidas"
            
            # R7: Mínimos de puntos multinivel por círculo
            for circulo in circulos_data.keys():
                prob += y_multinivel[circulo] >= circulos_data[circulo]['min_multinivel'], f"Min_multinivel_{circulo}"
            
            # R8: Mínimos de laboratorio
            for analisis in analisis_tipos:
                prob += muestras_lab[analisis] >= analisis_data[analisis]['min_muestras'], f"Min_lab_{analisis}"
            
            # ========== RESOLVER ==========
            prob.solve(PULP_CBC_CMD(msg=0))
            
            # ========== MOSTRAR RESULTADOS ==========
            if LpStatus[prob.status] == 'Optimal':
                st.success("✅ Solución óptima encontrada")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Calidad Científica Total", f"{value(prob.objective):.2f}")
                with col2:
                    st.metric("Equipos a usar", int(value(num_equipos)))
                with col3:
                    st.metric("Horas totales", f"{value(total_horas_hombre):.1f}")
                with col4:
                    costo_total = costo_equipo + sum(
                        analisis_data[a]['costo'] * value(muestras_lab[a])
                        for a in analisis_tipos
                    )
                    st.metric("Costo Total (€)", f"{costo_total:.2f}")
                
                # Resultados por círculo
                st.subheader("Resultados por Círculo de Hadas")
                resultados_circulos = []
                
                for circulo in circulos_data.keys():
                    sep_elegida = None
                    for sep_idx in range(len(circulos_data[circulo]['separaciones'])):
                        if value(x[circulo, sep_idx]) == 1:
                            sep_elegida = circulos_data[circulo]['separaciones'][sep_idx]
                            break
                    
                    puntos_standar = circulos_data[circulo]['perimetro'] / sep_elegida if sep_elegida else 0
                    
                    resultados_circulos.append({
                        'Círculo': circulo,
                        'Separación (m)': sep_elegida,
                        'Puntos Estándar': int(puntos_standar),
                        'Puntos Multinivel': int(value(y_multinivel[circulo]))
                    })
                
                df_circulos = pd.DataFrame(resultados_circulos)
                st.dataframe(df_circulos, use_container_width=True)
                
                # Mediciones
                st.subheader("Mediciones Especiales")
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"📊 Mediciones 24h: {int(value(total_mediciones_24h))}")
                with col2:
                    st.info(f"📈 Mediciones Extendidas: {int(value(total_mediciones_extendidas))}")
                
                # Análisis de laboratorio
                st.subheader("Muestras de Laboratorio")
                resultados_lab = []
                for analisis in analisis_tipos:
                    resultados_lab.append({
                        'Tipo de Análisis': analisis,
                        'Muestras': int(value(muestras_lab[analisis])),
                        'Costo Unitario (€)': analisis_data[analisis]['costo']
                    })
                
                df_lab = pd.DataFrame(resultados_lab)
                df_lab['Costo Total (€)'] = df_lab['Muestras'] * df_lab['Costo Unitario (€)']
                st.dataframe(df_lab, use_container_width=True)
                
                # Gráficos
                st.subheader("Visualizaciones")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de puntos de muestreo por círculo
                    total_puntos = []
                    nombres_circulos = []
                    for circulo in circulos_data.keys():
                        sep_elegida = None
                        for sep_idx in range(len(circulos_data[circulo]['separaciones'])):
                            if value(x[circulo, sep_idx]) == 1:
                                sep_elegida = circulos_data[circulo]['separaciones'][sep_idx]
                                break
                        puntos = circulos_data[circulo]['perimetro'] / sep_elegida if sep_elegida else 0
                        total_puntos.append(puntos + value(y_multinivel[circulo]))
                        nombres_circulos.append(circulo)
                    
                    fig1 = go.Figure(data=[
                        go.Bar(y=nombres_circulos, x=total_puntos, orientation='h', marker_color='indianred')
                    ])
                    fig1.update_layout(title="Total de Puntos de Muestreo por Círculo", 
                                     xaxis_title="Cantidad de Puntos", yaxis_title="Círculo")
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Gráfico de muestras de laboratorio
                    muestras = [int(value(muestras_lab[a])) for a in analisis_tipos]
                    fig2 = go.Figure(data=[
                        go.Bar(x=analisis_tipos, y=muestras, marker_color='lightseagreen')
                    ])
                    fig2.update_layout(title="Muestras de Laboratorio por Tipo", 
                                     xaxis_title="Tipo de Análisis", yaxis_title="Cantidad de Muestras")
                    fig2.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Desglose de presupuesto
                col1, col2 = st.columns(2)
                with col1:
                    costo_lab_total = sum(
                        analisis_data[a]['costo'] * value(muestras_lab[a])
                        for a in analisis_tipos
                    )
                    presupuesto_data = {
                        'Categoría': ['Equipo de Campo', 'Análisis de Laboratorio'],
                        'Costo (€)': [costo_equipo, costo_lab_total]
                    }
                    fig3 = go.Figure(data=[
                        go.Pie(labels=presupuesto_data['Categoría'], 
                              values=presupuesto_data['Costo (€)'],
                              marker_colors=['#FF6B6B', '#4ECDC4'])
                    ])
                    fig3.update_layout(title="Desglose de Presupuesto")
                    st.plotly_chart(fig3, use_container_width=True)
                
                with col2:
                    # Distribución de calidad
                    calidad_datos = {
                        'Componente': ['Puntos Estándar', 'Puntos Multinivel', 'Med. 24h', 'Med. Extendidas', 'Laboratorio'],
                        'Contribución': [
                            pesos['punto_standar'] * sum(circulos_data[c]['perimetro'] / 
                                (circulos_data[c]['separaciones'][s_idx] if value(x[c, s_idx]) == 1 else 1)
                                for c in circulos_data.keys() for s_idx in range(len(circulos_data[c]['separaciones']))),
                            pesos['punto_multinivel'] * sum(value(y_multinivel[c]) for c in circulos_data.keys()),
                            pesos['medicion_24h'] * value(total_mediciones_24h),
                            pesos['medicion_extendida'] * value(total_mediciones_extendidas),
                            pesos['laboratorio'] * sum(value(muestras_lab[a]) for a in analisis_tipos)
                        ]
                    }
                    fig4 = go.Figure(data=[
                        go.Pie(labels=calidad_datos['Componente'], 
                              values=calidad_datos['Contribución'],
                              marker_colors=['#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#A8D8EA'])
                    ])
                    fig4.update_layout(title="Contribución a Calidad Científica")
                    st.plotly_chart(fig4, use_container_width=True)
                
                # Resumen ejecutivo
                st.subheader("📋 Resumen Ejecutivo")
                resumen = f"""
                **Configuración Óptima:**
                - Calidad Científica Alcanzada: {value(prob.objective):.2f}/5.0
                - Número de Equipos: {int(value(num_equipos))}
                - Horas Totales de Trabajo: {value(total_horas_hombre):.1f} horas
                - Días Disponibles: {tiempo_total_dias}
                - Presupuesto Utilizado: €{costo_equipo + costo_lab_total:.2f} de €{presupuesto_total}
                
                **Puntos de Muestreo:**
                - Total de Puntos Estándar: {sum(int(circulos_data[c]['perimetro'] / 
                    (circulos_data[c]['separaciones'][s_idx] if value(x[c, s_idx]) == 1 else 1))
                    for c in circulos_data.keys() for s_idx in range(len(circulos_data[c]['separaciones'])))}
                - Total de Puntos Multinivel: {sum(int(value(y_multinivel[c])) for c in circulos_data.keys())}
                
                **Mediciones Especiales:**
                - Mediciones de 24 horas: {int(value(total_mediciones_24h))}
                - Mediciones Extendidas: {int(value(total_mediciones_extendidas))}
                
                **Análisis de Laboratorio:**
                - Total de Muestras: {sum(int(value(muestras_lab[a])) for a in analisis_tipos)}
                - Costo de Laboratorio: €{costo_lab_total:.2f}
                """
                st.markdown(resumen)
                
            else:
                st.error(f"❌ No se encontró solución óptima. Estado: {LpStatus[prob.status]}")
                st.info("Intenta ajustar los parámetros (aumenta presupuesto, tiempo o reduce mínimos requeridos)")
        
        except Exception as e:
            st.error(f"❌ Error en la optimización: {str(e)}")
            st.info("Por favor verifica que todos los parámetros sean válidos")

st.markdown("---")
st.markdown("""
**Notas importantes:**
- El modelo utiliza CBC Solver (gratuito y open-source)
- Los resultados son óptimos dentro de las restricciones especificadas
- Para cambiar los parámetros, modifica los valores en la interfaz y vuelve a resolver
""")
