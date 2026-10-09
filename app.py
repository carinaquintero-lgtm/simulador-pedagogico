import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CASOS = {
    1: {
        "titulo": "Caso 1: El atajo en la planificación docente",
        "descripcion": "Un/a docente le pide a una IA que le diseñe una secuencia didáctica completa sobre desigualdad social para nivel superior y decide subirla al aula virtual tal cual fue generada, sin modificar nada.",
        "consigna": "Analizá la situación desde los conceptos de 'enseñar es decidir' (Castañeda) y la mediación pedagógica. ¿Qué riesgos observás en delegar toda la planificación en la IA sin intervención crítica? Escribí tu análisis y propuesta de mejora.",
        "eje_relacionado": "Eje 3 y 4: Rediseño y decisiones pedagógicas."
    },
    2: {
        "titulo": "Caso 2: La sospecha en la entrega domiciliaria",
        "descripcion": "Al corregir un ensayo domiciliario sobre teorías sociológicas, un/a profesor/a detecta que tres estudiantes presentaron textos impecables, formales pero vacíos de apropiación personal, claramente redactados por IA.",
        "consigna": "El/la docente está tentado/a en prohibir el uso de herramientas digitales y exigir trabajos presenciales escritos a mano. Desde los aportes de Mariana Maggio ('hackeo a la evaluación') y la evaluación situada, ¿cómo rediseñarías esta tarea para hacer visible el proceso?",
        "eje_relacionado": "Eje 4: Evaluación situada y evidencias de aprendizaje."
    },
    3: {
        "titulo": "Caso 3: El peligro de la verosimilitud en los materiales",
        "descripcion": "Un/a profesor/a utiliza una IA generativa para crear un cuadro comparativo y explicaciones breves sobre conceptos teóricos complejos. Al leerlos rápido, parecen correctos, pero contienen una 'alucinación' sutil y bibliografía inventada.",
        "consigna": "Analizá el límite técnico de la IA ('verosimilitud no es validez' según la UNESCO). ¿Qué pasos de auditoría y contraste debiera haber realizado el/la docente antes de validar ese contenido para sus estudiantes?",
        "eje_relacionado": "Eje 2: Límites de la IA, alucinaciones y sesgos."
    },
    4: {
        "titulo": "Caso 4: De la prohibición a la integración crítica",
        "descripcion": "Una institución educativa mantiene una postura de prohibición absoluta de la IA bajo el argumento de que 'promueve la deshonestidad académica'. Sin embargo, los estudiantes la usan masivamente a escondidas, generando dinámicas de simulación y fraude administrativo.",
        "consigna": "Argumentá por qué esta postura responde al 'prohibicionismo' (Lion y Kap) y proponé una estrategia institucional para transicionar hacia una regulación formativa donde se enseñe a usar la IA críticamente.",
        "eje_relacionado": "Eje 1 y 3: Narrativas frente a la tecnología y posicionamientos institucionales."
    }
}

@app.route('/')
def index():
    return render_template('simulador.html', casos=CASOS)

@app.route('/evaluar', methods=['POST'])
def evaluar():
    data = request.json
    caso_id = int(data.get('caso_id'))
    respuesta_usuario = data.get('respuesta')
    
    caso_actual = CASOS.get(caso_id)
    
    system_prompt = f"""
    Sos un/a tutor/a pedagógico/a experto/a en tecnología educativa, formado/a en los marcos teóricos de Linda Castañeda, Gloria Edelstein, Miriam Kap, Sara Lion y Mariana Maggio.
    Estás evaluando la respuesta de un/a estudiante/docente en un simulador sobre un caso del trayecto 'Enseñar y evaluar en tiempos de IA generativa'.
    
    Contexto del caso actual: {caso_actual['titulo']}
    Descripción: {caso_actual['descripcion']}
    Consigna respondida: {caso_actual['consigna']}
    
    Tu retroalimentación debe ser:
    1. Formativa, constructiva y situada.
    2. Rescatar los aciertos del análisis del usuario/a vinculándolos explícitamente con los autores del marco teórico (mencionando a Castañeda, Edelstein, Kap, Maggio o UNESCO según corresponda).
    3. Señalar con respeto qué dimensiones pedagógicas o matices faltó profundizar.
    4. Mantener un tono cercano, profesional y estimulante (como Cari o Silvina guiando un taller de posgrado).
    """
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": respuesta_usuario}
            ],
            temperature=0.7
        )
        feedback = completion.choices.message.content
        return jsonify({"feedback": feedback})
    except Exception as e:
        return jsonify({"feedback": f"Error al generar la retroalimentación: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
