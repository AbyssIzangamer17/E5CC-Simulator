# 🌡️ Omron E5CC Virtual Simulator Pro

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Pages](https://img.shields.io/badge/Docs-GitHub%20Pages-brightgreen.svg)](https://AbyssIzangamer17.github.io/E5CC-Simulator/)

Una recreación digital de alta fidelidad del controlador de temperatura industrial **Omron E5CC**. Este simulador no es solo una interfaz visual, sino un motor de simulación térmica en tiempo real diseñado para educación, pruebas de algoritmos y entrenamiento en automatización.

---

## 🚀 Características Premium

*   **Motor de Simulación Térmica Avanzada**: Modelo de convección no lineal donde las pérdidas de calor escalan con la temperatura, simulando un horno industrial real.
*   **Algoritmo PID de Triple Corrección**: 
    *   **Proporcional (P)**: Acción inmediata sobre el error.
    *   **Integral (I)**: Eliminación del error en estado estacionario con sistema **Anti-Windup** avanzado.
    *   **Derivativo (D)**: Freno predictivo inteligente que detecta la velocidad de subida del PV.
*   **Autotuning Dinámico (AT-2)**: Sistema de sintonización automática basado en el método del relé de ciclo límite. Se adapta en tiempo real a cambios de consigna (SV).
*   **Simulación de Perturbaciones (Disturbance)**: Inyecta perturbaciones térmicas externas para probar la resiliencia del lazo de control.
*   **Interfaz Industrial Realista**:
    *   Displays de 14 segmentos (PV blanco / SV verde).
    *   Navegación por niveles (Operación, Ajuste, Inicial).
    *   Barra de telemetría de potencia de salida (0-100%).
    *   Monitorización en tiempo real de los términos P, I y D por separado.

---

## 🛠️ Instalación y Uso

### 1. Requisitos
- Python 3.8 o superior.
- Librería `matplotlib` (para el monitor gráfico en tiempo real).

### 2. Instalación Rápida
```bash
# Clonar repositorio
git clone https://github.com/AbyssIzangamer17/E5CC-Simulator.git
cd E5CC-Simulator

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecución
```bash
python main.py
```

---

## 🎮 Guía de Funcionamiento

### Menú de Navegación (Controles Omron)
*   **Botón Círculo [O]**: 
    *   *Presión corta*: Navega entre menu de **Operación** y **Ajuste**.
    *   *Presión larga (>3s)*: Entra en **Configuración Inicial**.
*   **Botón Cuadrado [M]**: Salta entre los parámetros dentro de un nivel (ej: navegar de P a I o a D).
*   **Flechas [▲/▼]**: Modifican los valores. En el display principal, cambian el **Set Point (SV)**.

### Activación del Auto-tuning
1. Accede al nivel de **Ajuste** (Botón O corto).
2. Selecciona el parámetro `AT` con el botón M.
3. Cambia a `AT-2` con la flecha ▲.
4. El LED **AT** se encenderá y el sistema buscará los mejores valores P, I, D mediante oscilaciones controladas.

---

## 🧠 El Corazón del Controlador: PID Dinámico

A diferencia de simuladores básicos, este proyecto expone la física interna del controlador:
- **PV (Process Value)**: Temperatura medida por el sensor virtual (incluye ruido y lag térmico).
- **SV (Set Value)**: Tu objetivo de temperatura.
- **Salida (MV)**: Reflejada en la barra roja lateral y el LED OUT1.

Si aplicas una **perturbación positiva** (simulando calor externo), verás el valor **D** saltar a negativo para "frenar" la subida, mientras que **I** ajustará la base de potencia para mantener el equilibrio.

---

## 🌐 Documentación en Línea

Hemos desplegado una Landing Page con la guía completa:
👉 [https://AbyssIzangamer17.github.io/E5CC-Simulator/](https://AbyssIzangamer17.github.io/E5CC-Simulator/)

---

## 📄 Licencia
Este proyecto es de código abierto bajo la licencia **MIT**.

## 👤 Autor
**AbyssIzangamer17**
GitHub: [@AbyssIzangamer17](https://github.com/AbyssIzangamer17)
