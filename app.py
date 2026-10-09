from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 4 Ejes pedagógicos con casos complejos, autores y dimensiones técnicas integrales
CASOS = {
    1: {
        "titulo": "Eje 01: La planificación algorítmica y el riesgo de vaciamiento político-pedagógico",
        "descripcion": "Un equipo docente utiliza ChatGPT para diseñar toda la programación anual de una materia de educación superior, delegando la selección de contenidos, objetivos y secuencias sin revisión institucional ni adecuación al perfil heterogéneo del estudiantado.",
        "consigna": "Analizá el problema articulando el concepto de 'enseñar es decidir' (Castañeda), la mediación pedagógica (Edith Litwin) y el rol del docente como diseñador cultural. Desde lo técnico, explicá por qué las LLMs (basadas en predicción estadística de tokens y sesgos de generalización) no pueden resolver el anclaje situado, y proponé una intervención basada en co-creación y curaduría crítica.",
        "retro_base": (
            "🔍 **Análisis conceptual integrado:** Como plantea Edith Litwin, la mediación pedagógica exige un posicionamiento político-epistemológico donde el docente es autor y curador del saber. Al delegar la programación, se vulnera el principio de que 'enseñar es decidir' (Castañeda), diluyendo el recorte ético-político necesario para el contexto real de los estudiantes.\n\n"
            "⚙️ **Dimensión técnica y de IA:** Los Grandes Modelos de Lenguaje operan calculando la probabilidad del siguiente token sobre corpus masivos de internet, lo que internaliza sesgos normalizadores y carece absoluta y lógicamente de intencionalidad pedagógica o noción de 'territorio'. Depender de su producción lineal genera respuestas descontextualizadas y propensas a alucinaciones normativas.\n\n"
            "💡 **Propuesta de intervención rigurosa:** Utilizar la IA exclusivamente como un co-piloto heurístico para explorar alternativas de estructuración, aplicando luego una rigurosa transposición didáctica situada, contrastando los outputs con el proyecto curricular institucional y las trayectorias reales del grupo."
        )
    },
    2: {
        "titulo": "Eje 02: Diseño de consignas complejas, accesibilidad cognitiva y DUA 3.0",
        "descripcion": "Se le solicita a una IA generativa la creación de consignas de trabajos prácticos evaluativos para una cohorte de adultos. La herramienta genera textos densos, abstractos y con alta carga de jerga técnica, generando barreras de comprensión masivas.",
        "consigna": "Evaluá la situación a la luz de los principios del Diseño Universal para el Aprendizaje (DUA 3.0) y la evaluación formativa. ¿Cómo interviene el diseño de 'prompts' (instrucciones) y el ajuste de parámetros técnicos para mitigar la opacidad sintáctica sin resignar densidad conceptual?",
        "retro_base": (
            "🔍 **Análisis conceptual integrado:** Desde el DUA 3.0, una consigna opaca o hiperformalizada levanta barreras cognitivas que atentan contra la equidad y la metacognición, transformando la evaluación en un obstáculo de comprensión lectora más que en una instancia de retroalimentación formativa.\n\n"
            "⚙️ **Dimensión técnica y de IA:** Por defecto, las IA tienden a imitar registros académicos hiper-sofisticados debido a su entrenamiento. Técnicamente, esto se soluciona parametrizando el *prompt* mediante ingeniería de instrucciones explícitas (otorgando roles de 'especialista en accesibilidad cognitiva', acotando niveles de legibilidad o pidiendo desglose en múltiples formatos de representación).\n\n"
            "💡 **Propuesta de intervención rigurosa:** Rediseñar la consigna asegurando múltiples formas de representación y expresión, explicitando rúbricas de coevaluación y utilizando la IA de manera situada para desglosar consignas complejas en trayectos accesibles."
        )
    },
    3: {
        "titulo": "Eje 03: Producciones estudiantiles, autoría y el mito de la detección automática",
        "descripcion": "Ante la sospecha generalizada de que los estudiantes utilizan IA para redactar sus ensayos, una institución exige el uso de software 'anti-plagio y detección de IA' y amenaza con sanciones punitivas automáticas a quienes presenten índices elevados.",
        "consigna": "Problematiza esta medida desde los enfoques críticos de la cultura digital y la evaluación formativa. Fundamentá por qué los detectores de IA fallan técnicamente y proponé un rediseño de la tarea centrado en la metacognición y el registro del proceso.",
        "retro_base": (
            "🔍 **Análisis conceptual integrado:** La prohibición punitiva y el disciplinamiento tecnológico contradicen los enfoques socio-técnicos de la educación. La evaluación formativa exige desplazar el foco del producto cerrado hacia la documentación del proceso de construcción del conocimiento y la apropiación crítica de las herramientas.\n\n"
            "⚙️ **Dimensión técnica y de IA:** Los supuestos 'detectores de IA' se basan en métricas estadísticas de perplejidad y monotonía del texto que carecen de rigor científico, arrojando altísimos índices de falsos positivos (especialmente afectando a estudiantes neurodivergentes o no nativos). Técnicamente es imposible trazar de forma infalible el origen sintético de un texto.\n\n"
            "💡 **Propuesta de intervención rigurosa:** Establecer contratos pedagógicos de uso transparente y ético, exigir bitácoras de proceso (registro de iteraciones con la IA), instancias de defensa oral y coevaluación colaborativa donde la herramienta sea objeto de análisis y no un motivo de censura."
        )
    },
    4: {
        "titulo": "Eje 04: Ciudadanía digital, sesgos algorítmicos y posicionamiento ético-político",
        "descripcion": "En un debate sobre el impacto social de la inteligencia artificial, un sector de docentes sostiene que la tecnología es neutral y que solo depende del uso individual, desestimando los sesgos políticos, económicos y extractivistas de las grandes corporaciones tecnológicas.",
        "consigna": "Desarrollá una argumentación crítica integrando perspectivas de la sociología de la tecnología y la ciudadanía digital. Analizá cómo operan los sesgos algorítmicos (entrenamiento con datos corporativos) y qué implica posicionarse pedagógicamente frente al tecnosoplismo.",
        "retro_base": (
            "🔍 **Análisis conceptual integrado:** La concepción de la tecnología como un instrumento neutral es una falacia tecnosoplista. Desde una perspectiva sociopolítica y de ciudadanía digital crítica, las plataformas y modelos de IA encapsulan relaciones de poder, intereses económicos y sesgos culturales coloniales que operan de forma invisible.\n\n"
            "⚙️ **Dimensión técnica y de IA:** Los sesgos algorítmicos no son 'errores' reparables sino propiedades estructurales derivadas de los conjuntos de datos masivos (*datasets*) utilizados en el entrenamiento, donde subrepresentan minorías y reproducen estereotipos hegemónicos normalizados por funciones de pérdida estadística.\n\n"
            "💡 **Propuesta de intervención rigurosa:** Promover una alfabetización crítica y situada que cuesture el determinismo tecnológico, analice las condiciones geopolíticas de producción de la IA y fomente la soberanía pedagógica y el uso emancipatorio de las tecnologías en el aula."
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
    
    # Validación detallada y específica por cada uno de los 4 ejes
    if len(respuesta) < 50:
        if caso_id == 1:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 01:** Tu respuesta es demasiado breve. "
                "Para un abordaje riguroso debés integrar los conceptos de **'enseñar es decidir' (Castañeda)**, el rol del docente como **diseñador cultural (Edith Litwin)**, y explicar técnicamente el problema de la **predicción estadística de tokens** y las **alucinaciones** de las LLMs frente al contexto institucional."
            )
        elif caso_id == 2:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 02:** Tu respuesta es demasiado breve. "
                "Es necesario que incorpores los principios del **Diseño Universal para el Aprendizaje (DUA 3.0)** y la **evaluación formativa**. "
                "Desde lo técnico, debés explicar cómo incide la **ingeniería de prompts** y el control de parámetros en la accesibilidad sintáctica."
            )
        elif caso_id == 3:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 03:** Tu respuesta es demasiado breve. "
                "Debés problematizar la **prohibición punitiva** y argumentar técnicamente por qué fallan los **detectores automáticos de IA (falsos positivos)**, proponiendo alternativas basadas en **bitácoras de proceso y metacognición**."
            )
        else:
            feedback = (
                "⚠️ **Análisis incompleto para el Eje 04:** Tu respuesta es demasiado breve. "
                "Debés rechazar la neutralidad tecnológica abordando la **sociología de la tecnología**, los **sesgos algorítmicos en los datasets de entrenamiento** y el desarrollo de una **ciudadanía digital crítica**."
            )
    else:
        feedback = (
            f"¡Excelente producción, Carina! Tu análisis demuestra una sólida apropiación teórica y técnica del problema.\n\n"
            f"{caso['retro_base']}"
        )
        
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)
