from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ejes pedagógicos con devoluciones enriquecidas (conceptos, autores y aspectos técnicos de IA)
CASOS = {
    1: {
        "titulo": "Eje 01: El peligro de delegar toda la planificación en la IA sin mediación docente",
        "descripcion": "Un docente utiliza ChatGPT para que le planifique toda la secuencia didáctica de un trimestre sin revisar los contextos institucionales ni los saberes previos del grupo.",
        "consigna": "Analizá la situación desde los conceptos de 'enseñar es decidir' (Castañeda) y la mediación pedagógica. ¿Qué riesgos observás en delegar toda la planificación en la IA sin intervención crítica? Escribí tu análisis y propuesta de mejora.",
        "retro_base": (
            "🔍 **Análisis conceptual:** Como plantea Edith Litwin y la perspectiva de la mediación pedagógica, el docente no es un mero ejecutor sino un diseñador cultural. Enseñar implica decidir políticamente qué recortes de la realidad privilegiar ('enseñar es decidir', Castañeda).\n\n"
            "⚙️ **Dimensión técnica de la IA:** Las LLMs funcionan prediciendo el próximo token por probabilidades estadísticas, sin comprender el contexto institucional real. Delegar ciegamente genera respuestas genéricas y propensas a alucinaciones o sesgos.\n\n"
            "💡 **Propuesta de mejora:** Usar la IA como andamiaje inicial para borradores, aplicando luego una rigurosa curaduría y transposición didáctica situada."
        )
    },
    2: {
        "titulo": "Eje 02: Uso de IA generativa para la redacción de consignas de evaluación",
        "descripcion": "Se diseñan consignas automáticas extremadamente complejas y abstractas mediante IA, generando barreras cognitivas no deseadas para los estudiantes.",
        "consigna": "Evaluá la consigna generada bajo los principios del Diseño Universal para el Aprendizaje (DUA 3.0). ¿Cómo rediseñarías la propuesta para garantizar accesibilidad y claridad en la evaluación formativa?",
        "retro_base": (
            "🔍 **Análisis conceptual:** Desde el DUA 3.0, una consigna opaca genera barreras de acceso que obstaculizan la metacognición y vulneran el derecho a una evaluación formativa justa.\n\n"
            "⚙️ **Dimensión técnica de la IA:** Las inteligencias artificiales tienden a sofisticar el lenguaje si no se les asigna explícitamente un rol de accesibilidad o nivel de lectura adecuado en el prompt.\n\n"
            "💡 **Propuesta de mejora:** Pautar múltiples formas de representación y expresión, explicitando criterios de evaluación claros."
        )
    },
    3: {
        "titulo": "Eje 03: Criterios de evaluación y transparencia frente a producciones con IA",
        "descripcion": "Ante la sospecha de uso automatizado de IA en trabajos prácticos, un docente decide prohibir totalmente el uso de herramientas digitales en lugar de redefinir la tarea.",
        "consigna": "Proponé una alternativa pedagógica basada en la coevaluación y en el registro del proceso de construcción del conocimiento, en lugar de la prohibición punitiva.",
        "retro_base": (
            "🔍 **Análisis conceptual:** La prohibición punitiva suele ser ineficaz frente a los procesos de apropiación tecnológica actual. El foco de la evaluación formativa debe ponerse en el proceso y la metacognición.\n\n"
            "⚙️ **Dimensión técnica de la IA:** Los detectores automáticos de IA son poco fiables y dan falsos positivos. La solución es pedagógica, no técnica: rediseñar tareas exigiendo bitácoras de proceso y contraste situado.\n\n"
            "💡 **Propuesta de mejora:** Establecer contratos pedagógicos claros, incorporar coevaluación y solicitar la explicitación de la interacción con la herramienta."
        )
    }
}

@app.route('/')
def index():
    return render_template('simulador.html', casos=CASOS)

@app.route('/evaluar', methods=['POST'])
def evaluar():
    data = request.get_json()
    caso_id = data.get('caso_id')
    caso = CASOS.get(caso_id)
    respuesta = data.get('respuesta', '').strip()
    
    if not caso:
        return jsonify({"feedback": "Eje no encontrado."}), 404
    
    # Validación específica según el eje seleccionado
    if len(respuesta) < 40:
        if caso_id == 1:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 01:** Tu respuesta es muy breve. "
                "Debés integrar los conceptos de **'enseñar es decidir' (Castañeda)** y **mediación pedagógica (Edith Litwin)**. "
                "Desde lo técnico, tenés que mencionar qué ocurre con la **predicción estadística de tokens** y las **alucinaciones** de las LLMs al carecer de contexto institucional."
            )
        elif caso_id == 2:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 02:** Tu respuesta es muy breve. "
                "Debés integrar los principios del **Diseño Universal para el Aprendizaje (DUA 3.0)** y la **evaluación formativa**. "
                "Desde lo técnico, debés explicar cómo las IA sofistican el lenguaje por defecto y la importancia de estructurar los **prompts** para garantizar accesibilidad."
            )
        else:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 03:** Tu respuesta es muy breve. "
                "Debés abordar los límites de la **prohibición punitiva** y los enfoques de **coevaluación y metacognición**. "
                "Desde lo técnico, tenés que fundamentar por qué fallan los **detectores automáticos de IA** y cómo exigir **bitácoras de proceso**."
            )
    else:
        feedback = (
            f"¡Excelente producción, Carina! Tu análisis demuestra una sólida apropiación del problema.\n\n"
            f"{caso['retro_base']}"
        )
        
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)
