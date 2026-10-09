from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Casos pedagógicos y devoluciones precalculadas basadas en criterios de retroalimentación formativa
CASOS = {
    1: {
        "titulo": "Caso 01: El peligro de delegar toda la planificación en la IA sin mediación docente",
        "descripcion": "Un docente utiliza ChatGPT para que le planifique toda la secuencia didáctica de un trimestre sin revisar los contextos institucionales ni los saberes previos del grupo.",
        "consigna": "Analizá la situación desde los conceptos de 'enseñar es decidir' (Castañeda) y la mediación pedagógica. ¿Qué riesgos observás en delegar toda la planificación en la IA sin intervención crítica? Escribí tu análisis y propuesta de mejora.",
        "retro_base": "Excelente análisis sobre la mediación pedagógica. Al delegar sin revisión, se pierde la autoría docente y el anclaje institucional. La intervención crítica es fundamental para adecuar la propuesta al grupo real de estudiantes."
    },
    2: {
        "titulo": "Caso 02: Uso de IA generativa para la redacción de consignas de evaluación",
        "descripcion": "Se diseñan consignas automáticas extremadamente complejas y abstractas mediante IA, generando barreras cognitivas no deseadas para los estudiantes de educación de jóvenes y adultos.",
        "consigna": "Evaluá la consigna generada bajo los principios del Diseño Universal para el Aprendizaje (DUA 3.0). ¿Cómo rediseñarías la propuesta para garantizar accesibilidad y claridad en la evaluación formativa?",
        "retro_base": "Muy buena mirada desde el DUA 3.0. Considerar las múltiples formas de representación y expresión evita que la consigna sea una barrera en lugar de un instrumento de evaluación formativa auténtica."
    },
    3: {
        "titulo": "Caso 03: Criterios de evaluación y transparencia frente a producciones con IA",
        "descripcion": "Ante la sospecha de plagio o uso automatizado de IA en los trabajos prácticos, un docente decide prohibir totalmente el uso de herramientas digitales en lugar de redefinir la tarea.",
        "consigna": "Proponé una alternativa pedagógica basada en la coevaluación y en el registro del proceso de construcción del conocimiento, en lugar de la prohibición punitiva.",
        "retro_base": "Enfoque muy pertinente. La prohibición suele ser ineficaz; en su lugar, explicitar los criterios de uso ético, documentar el proceso de trabajo y fomentar la metacognición transforma la IA en un recurso de aprendizaje."
    }
}

@app.route('/')
def index():
    return render_template('simulador.html', casos=CASOS)

@app.route('/evaluar', methods=['POST'])
def evaluar():
    data = request.get_json()
    caso_id = data.get('caso_id')
    respuesta = data.get('respuesta', '').strip()
    
    caso = CASOS.get(caso_id)
    if not caso:
        return jsonify({"feedback": "Caso no encontrado."}), 404
    
    # Análisis inteligente simulado según la longitud y pertinencia de la respuesta
    if len(respuesta) < 30:
        feedback = (
            f"Tu respuesta es muy breve. Para enriquecer la intervención en este caso "
            f"sobre '{caso['titulo']}', te sugerimos profundizar en la fundamentación teórica "
            f"y vincularla de manera más directa con los conceptos trabajados en el trayecto."
        )
    else:
        feedback = (
            f"¡Muy buen aporte, Carina! Tu intervención aborda con solidez el núcleo problemático.\n\n"
            f"🔍 **Retroalimentación pedagógica:** {caso['retro_base']}\n\n"
            f"💡 **Sugerencia para la práctica:** Continuá promoviendo espacios de reflexión crítica donde la tecnología se subordine siempre a los propósitos político-pedagógicos de la enseñanza."
        )
        
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)
