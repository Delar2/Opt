# 🔬 Optimizador de Estrategias de Muestreo

Una aplicación **Streamlit** que resuelve un modelo de **Programación Lineal Entera Mixta (MILP)** para diseñar estrategias óptimas de muestreo científico.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Open--Source-green)

---

## 🎯 ¿Qué Hace Esta Aplicación?

Optimiza automáticamente tu **estrategia de muestreo** balanceando:

✅ **Maximiza:** Calidad científica de tus mediciones  
⏱️ **Respeta:** Limitaciones de tiempo disponible  
💰 **Respeta:** Presupuesto disponible  
📋 **Cumple:** Requisitos técnicos y mínimos obligatorios  

### Ejemplo:
Tienes **30 días, €50k y 2 zonas para muestrear**. ¿Cómo distribuyo puntos, mediciones y análisis para máxima calidad?  
→ **La app te lo dice automáticamente** 🎯

---

## 📦 Contenido del Paquete

```
📁 Optimizador-Muestreo/
├── 📄 app_optimizacion.py          # Aplicación principal Streamlit
├── 📄 requirements.txt               # Dependencias Python
├── 📄 README.md                      # Este archivo
├── 📄 INSTALACION_Y_USO.md          # Guía detallada de instalación
├── 📄 EJEMPLOS_CASOS_USO.md         # 4 casos reales de uso
├── 🖥️ instalar_windows.bat           # Instalación automática Windows
└── 🖥️ instalar_mac_linux.sh          # Instalación automática Mac/Linux
```

---

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ **Instalar Dependencias**

#### Windows:
```bash
instalar_windows.bat
```

#### Mac/Linux:
```bash
bash instalar_mac_linux.sh
```

#### Manual (cualquier OS):
```bash
pip install -r requirements.txt
```

### 2️⃣ **Ejecutar la Aplicación**
```bash
streamlit run app_optimizacion.py
```

### 3️⃣ **¡Listo!**
Tu navegador se abrirá automáticamente en `http://localhost:8501`

---

## 📖 Guía de Uso Básica

### Estructura de la Aplicación

```
┌─────────────────────────────────────────────────────┐
│ SIDEBAR (Panel Izquierdo)                          │
│ ✓ Parámetros generales                            │
│ ✓ Tiempo total disponible                         │
│ ✓ Presupuesto                                      │
│ ✓ Mínimos requeridos                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ZONA CENTRAL                                        │
│ ✓ Configurar círculos de hadas                    │
│ ✓ Definir separaciones posibles                   │
│ ✓ Tiempos de muestreo                             │
│ ✓ Tipos de análisis de laboratorio                │
│ ✓ Pesos de calidad científica                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ RESULTADOS (Después de optimizar)                  │
│ ✓ Configuración óptima                            │
│ ✓ Tablas detalladas                               │
│ ✓ Gráficos interactivos                           │
│ ✓ Resumen ejecutivo                               │
└─────────────────────────────────────────────────────┘
```

### Pasos Principales

1. **Configure parámetros generales** (SIDEBAR)
   - Días disponibles
   - Presupuesto
   - Horas de trabajo
   - Mínimos obligatorios

2. **Defina sus círculos de hadas**
   - Nombre y perímetro
   - Opciones de separación (el modelo elige)
   - Puntos multinivel mínimos

3. **Configure tiempos y costos**
   - Tiempo por tipo de muestreo
   - Tipos de análisis y costos
   - Pesos de importancia

4. **Presione "RESOLVER OPTIMIZACIÓN"**
   - El modelo calcula la solución
   - Muestra resultados detallados
   - Genera gráficos

---

## 🧮 Modelo Matemático

**Tipo:** Programación Lineal Entera Mixta (MILP)

**Objetivo:**
```
Maximizar Calidad = Σ (peso_i × cantidad_i)
```

**Donde:**
- `peso_i` = importancia relativa de cada actividad (0-1)
- `cantidad_i` = número de muestreos, mediciones, análisis

**Restricciones:**
1. Horas totales ≤ Capacidad operativa
2. Gasto ≤ Presupuesto
3. Cada círculo usa una separación
4. Se cumplen mínimos obligatorios

**Solver:** CBC (Coin-or-branch-and-cut) - Gratuito y open-source

---

## 📊 Resultados Típicos

La aplicación genera:

### 📈 Métricas Clave
- **Calidad Científica Total** (0-5): Score de tu estrategia
- **Equipos necesarios**: Número de equipos de trabajo
- **Horas totales**: Tiempo de campo requerido
- **Costo total**: Presupuesto gastado

### 📋 Tablas Detalladas
- **Por círculo**: Separación elegida, puntos estándar, multinivel
- **Mediciones especiales**: Cantidad de 24h y extendidas
- **Laboratorio**: Muestras por tipo y costos

### 📉 Visualizaciones
1. **Barras**: Puntos de muestreo por círculo
2. **Barras**: Muestras de laboratorio por tipo
3. **Pastel**: Desglose de presupuesto
4. **Pastel**: Contribución a calidad científica

---

## 💡 Casos de Uso Reales

La aplicación es útil para:

### 🏔️ **Prospección Mineral**
Diseñar campañas en zonas de difícil acceso

### 💧 **Monitoreo Ambiental**
Optimizar redes de muestreo de agua

### 🧊 **Paleoclimatología**
Maximizar calidad con presupuesto limitado

### 🌍 **Estudios Hidrogeológicos**
Cubrir grandes áreas eficientemente

📖 **Ver 4 casos completos en:** `EJEMPLOS_CASOS_USO.md`

---

## 🔧 Requisitos Técnicos

### Hardware Mínimo
- CPU: Cualquiera (Intel i3 / AMD Ryzen 3 o superior)
- RAM: 4 GB
- Disco: 500 MB libres

### Software
- **Python**: 3.8 o superior
- **OS**: Windows, Mac, Linux

### Librerías (se instalan automáticamente)
- `streamlit` - Framework web
- `pandas` - Manipulación de datos
- `numpy` - Cálculos numéricos
- `pulp` - Optimización MILP
- `plotly` - Gráficos interactivos

---

## ⚙️ Configuración Avanzada

### Aumentar Tiempo de Cálculo
Para problemas muy grandes (>15 círculos), edita `app_optimizacion.py`:
```python
# Línea ~290
prob.solve(PULP_CBC_CMD(msg=0, timeLimit=300))  # 5 minutos máximo
```

### Cambiar Solver (Opcional)
En lugar de CBC, puedes usar CPLEX o Gurobi:
```python
prob.solve(CPLEX_CMD(msg=0))
```
(Requiere instalación adicional)

### Personalizar Colores y Estilos
Edita la sección de Streamlit config:
```python
st.set_page_config(
    page_title="Mi App",
    page_icon="🔬",
    ...
)
```

---

## 🐛 Troubleshooting

### Error: "module not found"
```bash
pip install -r requirements.txt
```

### Error: "No solver found"
CBC viene con PuLP. Si aún hay problema:
```bash
pip install coincbc
```

### "No se encontró solución óptima"
1. Aumenta presupuesto un 20%
2. Aumenta tiempo disponible
3. Reduce mínimos requeridos
4. Reduce número de círculos

### La app tarda mucho
Reduce número de círculos o separaciones a 2-3 opciones por círculo

### Presupuesto/Tiempo No Utilizado Completamente
Es normal. El modelo solo gasta lo necesario para máxima calidad dentro de restricciones.

---

## 📚 Documentación Completa

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Este archivo - visión general |
| `INSTALACION_Y_USO.md` | Guía completa de uso |
| `EJEMPLOS_CASOS_USO.md` | 4 casos reales completos |

---

## 💬 Preguntas Frecuentes

**P: ¿Es necesario ser programador?**  
R: No. La interfaz es completamente gráfica. Solo ingresa números y obten resultados.

**P: ¿Qué tan grande puede ser mi problema?**  
R: Funciona bien hasta ~20 círculos. Más allá requiere ajustes.

**P: ¿Puedo exportar resultados?**  
R: Sí, copias las tablas. Para exportación automática a Excel, abre issues.

**P: ¿Puedo modificar el código?**  
R: Sí, está disponible. Es código bien comentado para aprender.

**P: ¿Funciona en la nube?**  
R: Sí, puedes deployar en Heroku, Streamlit Cloud, etc.

---

## 🚀 Próximas Mejoras Posibles

- [ ] Exportación a Excel/PDF
- [ ] Importación de datos desde archivos
- [ ] Validación automática de parámetros
- [ ] Análisis de sensibilidad (¿qué pasa si cambio X?)
- [ ] Múltiples escenarios simultáneos
- [ ] Integración con Google Maps
- [ ] Almacenamiento de proyectos

---

## 📝 Licencia

Código abierto. Úsalo libremente en tus proyectos.

---

## 👨‍💻 Autor

Creado con ❤️ para investigadores y planificadores de muestreo.

---

## 📧 Soporte

Para problemas:
1. Revisa `INSTALACION_Y_USO.md`
2. Verifica requisitos en este README
3. Intenta con un ejemplo simple primero

---

## 🎓 Aprende Más

### Sobre Optimización MILP
- [Documentation PuLP](https://coin-or.github.io/pulp/)
- [Tutorial MILP Básico](https://en.wikipedia.org/wiki/Integer_programming)

### Sobre Streamlit
- [Documentación oficial](https://docs.streamlit.io/)
- [Tutoriales](https://streamlit.io/learn)

### Sobre Muestreo Científico
- Consulta a expertos en tu dominio
- Diseña pesos basado en literatura

---

## ¡Gracias por usar esta herramienta! 🙌

Si te resulta útil, comparte con colegas.  
Si tienes sugerencias, ¡bienvenidas!

**Happy Sampling!** 🔬📊
