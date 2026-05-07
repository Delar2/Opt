# 📚 Guía de Instalación y Uso - Optimizador de Muestreo

## 🚀 Instalación Rápida

### Paso 1: Instalar las librerías necesarias

Abre tu terminal/CMD y ejecuta:

```bash
pip install streamlit pandas numpy pulp plotly
```

**¿Qué instala?**
- **streamlit**: Framework para crear apps web
- **pandas**: Manejo de datos
- **numpy**: Cálculos matemáticos
- **pulp**: Resolver problemas de optimización MILP
- **plotly**: Gráficos interactivos

### Paso 2: Guardar el archivo

Guarda el archivo `app_optimizacion.py` en una carpeta de tu computadora (ejemplo: `C:\mis_proyectos\optimizacion`)

### Paso 3: Ejecutar la app

1. Abre la terminal/CMD
2. Navega a la carpeta donde guardaste el archivo:
   ```bash
   cd C:\mis_proyectos\optimizacion
   ```
   (Cambia la ruta según dónde hayas guardado el archivo)

3. Ejecuta la app:
   ```bash
   streamlit run app_optimizacion.py
   ```

4. ¡Listo! Tu navegador debería abrirse automáticamente en `http://localhost:8501`

---

## 📖 Cómo Usar la Aplicación

### Estructura General

La app tiene tres secciones principales:

#### **1️⃣ SIDEBAR (Panel Izquierdo) - Configuración General**

Aquí configuras los parámetros que aplican a toda tu estrategia:

- **Tiempo Total**: Cuántos días tienes para el muestreo
- **Horas de Trabajo**: Cuántas horas efectivas trabaja el equipo por día
- **Presupuesto Total**: Dinero disponible para toda la campaña
- **Costo Diario del Equipo**: Salarios, comida, hospedaje, transporte
- **Mínimos Requeridos**: Cantidad mínima de mediciones especiales necesarias

#### **2️⃣ ZONA CENTRAL - Configurar Círculos**

Aquí defines cada "círculo de hadas" (área de muestreo):

- **Nombre**: Identificador del círculo (ej: "Zona Alpina", "Llanura Occidental")
- **Perímetro**: Distancia alrededor del círculo en metros
- **Puntos Multinivel Mínimos**: Puntos especiales que DEBEN tener
- **Opciones de Separación**: El modelo ELIGE entre estas 3 distancias entre puntos

**Ejemplo:**
- Círculo "Zona A" con perímetro 500m
- El modelo puede elegir: separación de 25m, 50m u 100m entre puntos
- Con 25m: 500/25 = 20 puntos
- Con 50m: 500/50 = 10 puntos
- Con 100m: 500/100 = 5 puntos
- El modelo elige la que MEJOR optimiza la calidad científica

#### **3️⃣ Otras Secciones**

- **Tiempos de Muestreo**: Cuántas horas toma cada tipo de actividad
- **Análisis de Laboratorio**: Tipos de análisis, costo y mínimos necesarios
- **Pesos de Calidad**: Importancia relativa de cada actividad (0=nada importante, 1=muy importante)

---

## 🎯 Ejemplo Práctico

Imaginemos que quieres muestrear **2 círculos** en una región:

### Configuración General (SIDEBAR)
- Tiempo total: 30 días
- Horas/día: 8 horas
- Presupuesto: €50,000
- Costo diario equipo: €500
- Mediciones 24h mínimas: 5
- Mediciones extendidas mínimas: 3

### Círculo 1: "Montaña Central"
- Perímetro: 1000 metros
- Puntos multinivel mínimos: 3
- Opciones de separación: 25m, 50m, 100m

### Círculo 2: "Valle del Río"
- Perímetro: 800 metros
- Puntos multinivel mínimos: 2
- Opciones de separación: 30m, 60m, 120m

### Tiempos
- Punto estándar: 1 hora
- Punto multinivel: 2 horas
- Medición 24h: 24 horas
- Medición extendida: 48 horas

### Análisis de Laboratorio
- Mineralógico: €100/muestra, mín 5
- Biogeoquímico: €150/muestra, mín 5
- (etc...)

### Pesos de Calidad
- Puntos estándar: 0.3 (menos importante)
- Puntos multinivel: 0.6 (importante)
- Mediciones 24h: 0.8 (muy importante)
- Mediciones extendidas: 0.9 (muy importante)
- Laboratorio: 0.7 (importante)

---

## 📊 Interpretación de Resultados

Una vez resuelta la optimización, verás:

### **Métricas Principales**
- **Calidad Científica Total**: Score de 0-5 que indica cuán buena es tu estrategia
- **Equipos a usar**: Número de equipos recomendados
- **Horas totales**: Tiempo de trabajo necesario
- **Costo Total**: Dinero que gastarás

### **Tabla de Círculos**
Muestra para cada círculo:
- Separación elegida por el modelo
- Cantidad de puntos estándar
- Cantidad de puntos multinivel

**Interpretación:** Si ves "Separación: 50m", significa que el modelo eligió espaciar 50 metros entre puntos en ese círculo.

### **Mediciones Especiales**
- Mediciones de 24 horas asignadas
- Mediciones extendidas asignadas

### **Muestras de Laboratorio**
Tabla con:
- Tipo de análisis
- Cantidad de muestras
- Costo unitario
- Costo total por tipo

### **Gráficos**
1. **Puntos por Círculo**: Barras mostrando total de muestreos
2. **Muestras de Lab**: Cantidad de muestras por tipo
3. **Presupuesto**: Desglose entre equipo y laboratorio
4. **Calidad**: Contribución de cada componente a la calidad total

---

## ⚙️ Ajustes y Troubleshooting

### "No se encontró solución óptima"

**Causas comunes:**
1. **Presupuesto muy bajo**: Aumenta el presupuesto total
2. **Tiempo muy limitado**: Aumenta días o horas/día
3. **Mínimos muy altos**: Reduce los requerimientos mínimos
4. **Costos de laboratorio muy altos**: Ajusta costos unitarios

**Solución:** Intenta uno de estos cambios:
- Aumentar presupuesto en 20-30%
- Reducir mínimos requeridos en 10-20%
- Aumentar tiempo disponible

### La app se congela o tarda mucho

**Solución:** Reduce el número de círculos a 2-3 mientras aprendes a usarla.

### Error: "module not found"

Significa que no instalaste todas las librerías. Ejecuta:
```bash
pip install streamlit pandas numpy pulp plotly
```

---

## 💡 Tips y Buenas Prácticas

### 1. **Empieza Simple**
- Comienza con 2 círculos
- Después expande a más

### 2. **Entiende tus Restricciones**
- ¿Cuál es realmente tu presupuesto?
- ¿Cuántos días reales tienes?
- Sé realista con mínimos requeridos

### 3. **Pesos de Calidad**
- Asigna mayor peso a lo que es científicamente IMPORTANTE
- Menor peso a lo que es opcional
- Ejemplo: Si las mediciones 24h son críticas → asigna 0.9
- Si los puntos estándar son simplemente background → asigna 0.2

### 4. **Separaciones Realistas**
- 25m es muy denso (mucho tiempo/costo)
- 100m+ es muy disperso (puede perder detalles)
- Típicamente: 25-50m es buen balance

### 5. **Iteración**
- Resuelve una vez
- Mira los resultados
- Si no te satisfacen los puntos multinivel → aumenta su peso
- Vuelve a resolver

---

## 🔍 Entendiendo el Modelo Matemático

**Lo que hace el modelo:**

1. **Objetivo**: Maximizar esta fórmula:
   ```
   Calidad = (peso_estándar × puntos_estándar) +
             (peso_multinivel × puntos_multinivel) +
             (peso_24h × mediciones_24h) +
             (peso_ext × mediciones_ext) +
             (peso_lab × muestras_laboratorio)
   ```

2. **Restricciones**: Bajo estas limitaciones:
   - Horas totales ≤ equipos × horas/día × días
   - Gasto ≤ presupuesto
   - Cada círculo usa UNA separación
   - Se cumplen todos los mínimos

3. **Decisiones**: El modelo elige:
   - Qué separación usar en cada círculo
   - Cuántos puntos multinivel
   - Cuántos equipos necesita
   - Cuántas mediciones especiales
   - Cuántas muestras de laboratorio

**Resultado**: Una estrategia ÓPTIMA que maximiza calidad respetando restricciones.

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que instalaste todas las librerías
2. Intenta con parámetros más simples (menos círculos, menos análisis)
3. Revisa que los números tenga sentido (presupuesto > 0, tiempo > 0, etc)

¡Buena suerte con tu muestreo! 🔬
