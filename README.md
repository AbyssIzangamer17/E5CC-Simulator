# 🌡️ Omron E5CC Virtual Simulator

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una recreación digital de alta fidelidad del controlador de temperatura industrial **Omron E5CC**. Este simulador permite experimentar con el control de procesos térmicos en lazo cerrado utilizando algoritmos PID avanzados y sintonía automática (Autotuning).

---

## 🚀 Características Principales

*   **Algoritmo PID de Triple Corrección**: Implementación exacta de los componentes Proporcional, Integral y Derivativo con protección Anti-Windup.
*   **Autotuning AT-2**: Sistema de sintonizado automático basado en ciclos de límite para encontrar los parámetros óptimos del sistema.
*   **Modelo Térmico Realista**: Simulación física que incluye inercia térmica, pérdidas por convección no lineal y ruido de sensor.
*   **Interfaz Industrial**: Recreación fiel del panel frontal del E5CC, incluyendo displays PV/SV, LEDs de estado y jerarquía de menús.
*   **Simulación de Perturbaciones**: Slider interactivo para simular influencias térmicas externas y observar la respuesta del controlador.

## 📸 Vista Previa

*(Inserta aquí una captura de pantalla de la aplicación ejecutándose en tu PC)*

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/AbyssIzangamer17/E5CC-Simulator.git
   cd E5CC-Simulator
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el simulador:
   ```bash
   python main.py
   ```

## 🎮 Guía de Usuario

### Navegación de Botones
| Botón | Acción | Función |
| :--- | :--- | :--- |
| **O (Nivel)** | Clic Corto | Cambia entre modo Operación y Ajuste (P, I, D, AT) |
| **O (Nivel)** | Clic Largo | Entra en Configuración Inicial (OREV) |
| **M (Modo)** | Clic | Navega entre los parámetros del nivel seleccionado |
| **▲/▼ (Flechas)** | Clic | Ajusta el valor del parámetro o el Set Point (SV) |

### Cómo usar el Autotuning (AT)
1. Presiona **O** una vez.
2. Navega con **M** hasta ver `AT`.
3. Activa `AT-2` con la flecha **▲**.
4. El LED **AT** se encenderá y el programa calculará los mejores valores para tu sistema.

## 🧪 El "Cerebro" del Sistema: PID

El simulador desglosa la telemetría del PID para fines educativos:
*   **P (Proporcional)**: Fuerza reactiva al error actual.
*   **I (Integral)**: Corrección acumulada para eliminar el error residual.
*   **D (Derivativo)**: Freno predictivo para evitar el *overshoot*.

## 🌐 GitHub Pages

Visita nuestra página de documentación y guía interactiva aquí: 
[https://AbyssIzangamer17.github.io/E5CC-Simulator/](https://AbyssIzangamer17.github.io/E5CC-Simulator/)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👤 Autor

**AbyssIzangamer17**
*   GitHub: [@AbyssIzangamer17](https://github.com/AbyssIzangamer17)
