# 📋 Ejemplos de Casos de Uso

## Caso 1: Prospección Mineral en Zonas Alpinas

### Descripción
Exploración de depósitos minerales en zonas de montaña. Se necesita alta precisión en ciertos puntos pero con limitaciones de tiempo y acceso.

### Parámetros

**Configuración General:**
- Tiempo disponible: 45 días
- Horas trabajo/día: 6 (por difícil acceso)
- Presupuesto: €80,000
- Costo equipo/día: €800 (incluye escalada, desplazamientos)
- Mediciones 24h mín: 8
- Mediciones extendidas mín: 5

**Círculo 1: "Cresta Principal"**
- Perímetro: 2000 metros
- Puntos multinivel mín: 5
- Separaciones: 25m, 50m, 100m

**Círculo 2: "Colateral Sur"**
- Perímetro: 1200 metros
- Puntos multinivel mín: 3
- Separaciones: 30m, 60m, 120m

**Tiempos:**
- Punto estándar: 1.5h (difícil acceso)
- Punto multinivel: 3h (necesita equipo especial)
- Medición 24h: 24h
- Medición extendida: 48h

**Análisis de Lab:**
- Mineralógico: €200/muestra, mín 10
- Geoquímico: €150/muestra, mín 8
- ICP-MS: €300/muestra, mín 5
- Datación: €500/muestra, mín 2

**Pesos de Calidad:**
- Puntos estándar: 0.4
- Puntos multinivel: 0.8 (CRÍTICO en montaña)
- Med 24h: 0.9
- Med ext: 0.9
- Laboratorio: 0.8

### Resultado Esperado
El modelo probablemente elegirá separaciones más amplias (50-100m) para controlar costos, compensando con mayor número de mediciones especiales de alta calidad.

---

## Caso 2: Monitoreo Ambiental de Cuenca Hidrográfica

### Descripción
Monitoreo de calidad del agua en una cuenca. Se priorizan mediciones de larga duración para capturar variabilidad temporal.

### Parámetros

**Configuración General:**
- Tiempo disponible: 90 días (estación completa)
- Horas trabajo/día: 8
- Presupuesto: €120,000
- Costo equipo/día: €600 (2 vehículos, equipos)
- Mediciones 24h mín: 20
- Mediciones extendidas mín: 10

**Círculo 1: "Cabecera"**
- Perímetro: 5000 metros
- Puntos multinivel mín: 4
- Separaciones: 100m, 200m, 500m

**Círculo 2: "Tramo Medio"**
- Perímetro: 8000 metros
- Puntos multinivel mín: 6
- Separaciones: 150m, 300m, 600m

**Círculo 3: "Desembocadura"**
- Perímetro: 3000 metros
- Puntos multinivel mín: 3
- Separaciones: 100m, 200m, 400m

**Tiempos:**
- Punto estándar: 0.5h (fácil acceso, agua)
- Punto multinivel: 1.5h
- Medición 24h: 24h
- Medición extendida: 72h (para agua, más completa)

**Análisis de Lab:**
- Físico-químico: €80/muestra, mín 15
- Microbiología: €120/muestra, mín 10
- Ecotoxicología: €200/muestra, mín 5
- Isótopos: €400/muestra, mín 3

**Pesos de Calidad:**
- Puntos estándar: 0.3 (menos importante)
- Puntos multinivel: 0.5
- Med 24h: 0.9 (CRÍTICO para variabilidad)
- Med ext: 0.95 (MUY CRÍTICO)
- Laboratorio: 0.7

### Resultado Esperado
El modelo elegirá separaciones más amplias (200-600m) para cubrir más área con menos puntos, priorizando mediciones de larga duración.

---

## Caso 3: Estudios Paleoclimáticos en Testigos de Hielo

### Descripción
Muestreo de testigos de hielo en glaciar. Máxima precisión en lugares específicos con presupuesto limitado.

### Parámetros

**Configuración General:**
- Tiempo disponible: 20 días (ventana de muestreo corta)
- Horas trabajo/día: 4 (altura, acclimatación)
- Presupuesto: €150,000 (muy costoso)
- Costo equipo/día: €2000 (logística de montaña)
- Mediciones 24h mín: 15
- Mediciones extendidas mín: 8

**Círculo 1: "Zona Alta"**
- Perímetro: 800 metros
- Puntos multinivel mín: 8 (MUY IMPORTANTE)
- Separaciones: 10m, 25m, 50m (MUY DENSO)

**Tiempos:**
- Punto estándar: 2h (muy especializado)
- Punto multinivel: 4h (testigos profundos)
- Medición 24h: 24h
- Medición extendida: 120h (análisis continuo)

**Análisis de Lab:**
- Isotopos de O: €500/muestra, mín 20
- Isotopos de H: €500/muestra, mín 20
- Cromatografía Iónica: €300/muestra, mín 15
- Radiocarbono: €800/muestra, mín 5
- Apatita/Magnetita: €1000/muestra, mín 2

**Pesos de Calidad:**
- Puntos estándar: 0.2
- Puntos multinivel: 0.95 (ABSOLUTAMENTE CRÍTICO)
- Med 24h: 0.95
- Med ext: 0.99 (MÁX PRIORIDAD)
- Laboratorio: 0.9

### Resultado Esperado
El modelo usará separaciones muy cerradas (10-25m) con muchos puntos multinivel. Gasto máximo en laboratorio para análisis de alta precisión. Pocos equipos por espacio limitado.

---

## Caso 4: Prospección de Agua Subterránea en Semiaridez

### Descripción
Búsqueda de acuíferos en región desértica. Balance entre cobertura y profundidad de muestreo.

### Parámetros

**Configuración General:**
- Tiempo disponible: 60 días
- Horas trabajo/día: 10 (clima favorable)
- Presupuesto: €45,000 (moderado)
- Costo equipo/día: €400
- Mediciones 24h mín: 3
- Mediciones extendidas mín: 2

**Círculo 1: "Llanura Norte"**
- Perímetro: 12000 metros (zona grande)
- Puntos multinivel mín: 2
- Separaciones: 500m, 1000m, 2000m (AMPLIAS)

**Círculo 2: "Depresión Central"**
- Perímetro: 8000 metros
- Puntos multinivel mín: 3
- Separaciones: 400m, 800m, 1600m

**Tiempos:**
- Punto estándar: 0.5h (perforación simple)
- Punto multinivel: 2h (múltiples niveles)
- Medición 24h: 24h
- Medición extendida: 48h

**Análisis de Lab:**
- Análisis básico: €50/muestra, mín 20
- Hidrogeoquímico: €150/muestra, mín 15
- Isótopos ambientales: €300/muestra, mín 8
- Traza/Pesticidas: €200/muestra, mín 5

**Pesos de Calidad:**
- Puntos estándar: 0.7 (COBERTURA IMPORTANTE)
- Puntos multinivel: 0.5
- Med 24h: 0.4
- Med ext: 0.4
- Laboratorio: 0.6

### Resultado Esperado
El modelo maximizará puntos estándar con separaciones amplias (1000-2000m) para cubrir gran área, minimizando puntos multinivel y mediciones especiales para controlar presupuesto.

---

## Cómo Usar Estos Ejemplos

### Opción 1: Copiar y Modificar
1. Abre la app con los parámetros de uno de estos casos
2. Ve cambiando valores según tu situación específica
3. Observa cómo cambian los resultados

### Opción 2: Comparar Escenarios
1. Resuelve el caso como está
2. Luego cambia UN parámetro (ej: aumenta presupuesto 20%)
3. Resuelve de nuevo y compara resultados
4. Entenderás qué parámetros son críticos

### Opción 3: Personalizar
Toma el caso más parecido a tu situación y personaliza:
- Los nombres de los círculos
- Los perímetros reales
- Los tipos de análisis que necesitas
- Los pesos según tu prioridad científica

---

## Tips de Interpretación

### ¿Qué significa que el modelo elige separación 100m en lugar de 25m?

**Significa:** Con 100m entre puntos hay menos puntos pero se gasta menos tiempo/presupuesto. El modelo lo eligió porque:
- Tu presupuesto/tiempo es limitado
- Los pesos científicos favorecen otras actividades
- Es el mejor balance entre cobertura y recursos

**Qué hacer:** Si necesitas más densidad:
- Aumenta presupuesto
- Aumenta peso de puntos estándar
- Reduce mínimos de otras cosas
- Vuelve a resolver

### ¿Qué significa calidad científica 3.5/5?

**Significa:** Tu estrategia alcanza un nivel de calidad MODERADO-BUENO. No es máximo porque:
- Hay restricciones de tiempo/presupuesto
- Hay conflictos entre objetivos
- Algo tuvo que sacrificarse

**Para mejorar:** Aumenta presupuesto, tiempo, o reduce exigencias mínimas.

### ¿Por qué no usa todos los análisis de laboratorio?

**Es normal.** El modelo:
- Respeta mínimos (obligatorio)
- Elige más solo si cabe en presupuesto y ayuda a calidad
- Si ve que otros componentes contribuyen más a calidad con menor costo, los prioriza

---

## Validación de Resultados

Después de resolver, pregúntate:

1. **¿Son realistas los números?**
   - ¿El presupuesto gastado tiene sentido?
   - ¿Las horas totales caben en los días disponibles?
   
2. **¿Tiene sentido la estrategia?**
   - ¿Los puntos multinivel están donde más los necesitas?
   - ¿Las mediciones especiales están bien asignadas?

3. **¿Puedo mejorar algo?**
   - ¿Hay presupuesto sin usar? → Aumenta calidad
   - ¿Horas sobrantes? → Añade más muestreo
   - ¿No alcanza? → Ajusta presupuesto/tiempo

---

## ¡Buena Suerte! 🔬

Si tienes preguntas sobre cómo configurar TU caso específico, 
recuerda que puedes iterar: resolver → analizar → cambiar parámetros → resolver de nuevo
