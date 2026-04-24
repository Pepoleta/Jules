# Guía de Pruebas - Gemini Automator 🧪

Esta guía detalla cómo realizar pruebas automáticas y manuales para la aplicación Gemini Automator.

## 1. Pruebas Unitarias Automáticas

Se han implementado pruebas unitarias que utilizan **Mocks**. Esto significa que prueban la lógica del código sin necesidad de abrir un navegador real o tener las dependencias instaladas.

### Cómo ejecutar las pruebas:
Ejecuta el script principal de pruebas desde la raíz del proyecto:

```bash
python run_tests.py
```

### Qué cubren estas pruebas:
- **`test_gemini_bot.py`**: Verifica que el bot intente navegar a la URL correcta, que escriba los prompts, que maneje la subida de archivos y que cierre el navegador correctamente.
- **`test_app.py`**: Verifica la lógica de Streamlit, incluyendo la inicialización del bot en el `session_state`, el manejo de formularios y la subida temporal de archivos.

---

## 2. Pruebas de Integración (Manuales)

Para probar la aplicación en un entorno real, sigue estos pasos:

### Requisitos previos:
1. Tener Google Chrome instalado.
2. Tener las dependencias instaladas: `pip install -r requirements.txt`.

### Pasos para probar:
1. **Inicio de Sesión**: La primera vez que corras la app, es posible que debas loguearte en Google en la ventana de Chrome que se abre. El perfil se guarda en la carpeta `chrome_profile`.
2. **Ejecución**: 
   ```bash
   streamlit run app.py
   ```
3. **Flujo de Usuario**:
   - Ingresa un texto en el área de prompt.
   - Sube un archivo pequeño (imagen o PDF).
   - Haz clic en "Send to Gemini".
   - Verifica que en la ventana de Chrome el bot realice las acciones y que la respuesta aparezca en la interfaz de Streamlit.

---

## 3. Estructura de Pruebas

```text
Jules/
├── tests/
│   ├── test_gemini_bot.py  # Pruebas del Bot (Selenium/UC)
│   └── test_app.py         # Pruebas de la UI (Streamlit)
├── run_tests.py            # Ejecutor de pruebas y reporte
└── TESTING.md              # Esta guía
```
