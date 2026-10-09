import os
import re
import unicodedata

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MIN_PALABRAS = 30
MAX_CARACTERES = 6000

# Contenidos tomados del programa y de los desarrollos de los Ejes 1 a 4 del taller
# "Enseñar y evaluar en tiempos de IA generativa: criterios y decisiones en las intervenciones docentes".
CASOS = {
    1: {
        "eje": "Eje 1",
        "nombre": "Narrativas y posicionamientos",
        "titulo": "Eje 1 · Narrativas y posicionamientos: «la IA es una herramienta más» y «hay que incorporarla ya»",
        "descripcion": (
            "En una reunión de cátedra de nivel superior, un colega afirma que «la IA es una herramienta más: "
            "todo depende del uso que haga cada docente». Otra colega propone incorporarla en todas las materias "
            "desde el próximo cuatrimestre «porque los estudiantes ya la usan y es inevitable». "
            "Un tercero sostiene que, en cambio, la IA destruye la escritura y el pensamiento propio."
        ),
        "consigna": (
            "Identificá qué narrativas sobre la IA aparecen en la escena (promesa, amenaza, herramienta neutral, "
            "inevitabilidad) y qué supuestos sobre cómo se aprende y qué significa enseñar hay detrás de cada una. "
            "Luego formulá un posicionamiento situado para tu propia materia: para qué, cuándo y con qué cuidados "
            "usarías (o no) IA."
        ),
        "criterios": [
            {
                "titulo": "Reconoce las narrativas en juego",
                "patrones": [r"promesa", r"amenaza", r"neutral", r"inevitab"],
                "minimo": 2,
                "pista": "¿Qué narrativas (promesa, amenaza, herramienta neutral, inevitabilidad) reconocés en cada intervención?",
            },
            {
                "titulo": "Explicita los supuestos sobre enseñar y aprender",
                "patrones": [r"supuesto", r"como se aprende", r"que significa ensenar", r"concepcion de (la )?(ensenanza|aprendizaje)", r"papel del docente|rol del docente"],
                "minimo": 1,
                "pista": "¿Qué idea de aprendizaje, de enseñanza y de rol docente está detrás de cada frase?",
            },
            {
                "titulo": "Pone en cuestión la neutralidad de la tecnología",
                "patrones": [r"no (es|son) neutr", r"sociotecnic", r"sesgo", r"condiciona|impone|favorece|obstaculiza", r"lenguaje|interlocutor|interaccion"],
                "minimo": 1,
                "pista": "Si «todo depende del uso», ¿qué queda sin mirar sobre lo que la herramienta hace posible, dificulta o condiciona?",
            },
            {
                "titulo": "Distingue presencia social de necesidad pedagógica",
                "patrones": [r"necesidad pedagogica", r"decidir no (usar|utilizar|incorporar)|no usar|no utilizar|prescindir|sin (usar )?(ia|inteligencia)", r"inevitab.{0,60}(pedagog|decision)|(pedagog|decision).{0,60}inevitab", r"preservar|otras formas de trabajo"],
                "minimo": 1,
                "pista": "Que los estudiantes ya la usen, ¿alcanza para que sea pedagógicamente necesaria? ¿Decidir no usarla también puede ser una decisión pedagógica?",
            },
            {
                "titulo": "Formula un posicionamiento situado y fundamentado",
                "patrones": [r"decision(es)? fundamentada", r"ensenar es decidir|castaneda", r"para que", r"cuando", r"cuidado", r"condicion", r"situad", r"contexto|materia|catedra"],
                "minimo": 3,
                "pista": "Tu posición, ¿responde para qué, cuándo, con qué cuidados y bajo qué condiciones de tu materia?",
            },
        ],
        "lectura": (
            "**Claves del Eje 1.** Las cuatro narrativas no son solo opiniones sobre una tecnología: cada una esconde supuestos sobre cómo se aprende, "
            "qué significa enseñar, cuál es el papel del docente y qué lugar ocupa la tecnología.\n\n"
            "• «Todo depende del uso» devuelve la responsabilidad a quienes toman decisiones, pero silencia que toda herramienta ofrece ciertas posibilidades, "
            "impone condiciones y porta sesgos comerciales y algorítmicos. Además, la IA generativa trabaja con lenguaje y reorganiza la interacción "
            "(un «interlocutor artificial»), por lo que pensarla solo como herramienta resulta insuficiente.\n\n"
            "• «Es inevitable» confunde la presencia social de una tecnología con su necesidad pedagógica. La inevitabilidad tecnológica no debería "
            "convertirse en inevitabilidad pedagógica, y decidir no utilizar IA también es una decisión pedagógica.\n\n"
            "• Con Castañeda (2026): enseñar es decidir. La pregunta de diseño deja de ser «se puede o no se puede» y pasa a ser "
            "«¿qué estamos haciendo inevitable cuando diseñamos?». El objetivo es pasar de la opinión a la decisión fundamentada."
        ),
        "preguntas": [
            "¿En qué situaciones de tu materia tiene sentido incorporar IA y en cuáles resulta más valioso preservar otras formas de trabajo?",
            "¿Qué tipo de «educación muerta» (Castañeda) te preocupa evitar: tareas hechas con IA que se entregan y califican sin diálogo intelectual?",
        ],
        "lecturas": ["Castañeda, L. (2026). Enseñar es decidir. Transmedia XXI.", "Desarrollo del Eje 1 del taller."],
    },
    2: {
        "eje": "Eje 2",
        "nombre": "Funcionamiento y límites",
        "titulo": "Eje 2 · Funcionamiento y límites: «se lee bien, así que lo uso tal cual»",
        "descripcion": (
            "Un docente le pide a una IA generativa un resumen de una teoría para su clase, con cinco referencias bibliográficas. "
            "La respuesta suena muy convincente. Al revisarla, dos referencias no existen, el resumen simplifica un debate complejo "
            "y menciona como vigente una normativa que cambió. El docente decide usarlo igual «porque se lee bien»."
        ),
        "consigna": (
            "Analizá qué límites de la IA generativa se ponen en juego en esta situación. Proponé criterios de revisión para decidir "
            "qué se acepta, qué se ajusta y qué se descarta de una producción de IA, y explicá qué no convendría delegar y por qué."
        ),
        "criterios": [
            {
                "titulo": "Distingue verosimilitud de validez",
                "patrones": [r"verosimil|plausib|suena (bien|convincente)|se lee bien", r"valid|verdad|correct"],
                "minimo": 2,
                "pista": "Que algo suene convincente, ¿equivale a que sea válido? ¿Qué pregunta conviene hacer en lugar de «qué respondió la IA»?",
            },
            {
                "titulo": "Nombra límites concretos de la IA generativa",
                "patrones": [r"invenc|alucin|inexistent|inventa", r"simplific|sesgo", r"desactualiz|fecha de corte|vigente", r"opacidad|caja negra"],
                "minimo": 2,
                "pista": "¿Qué límites aparecen en la escena: invenciones, simplificaciones y sesgos, desactualización, opacidad?",
            },
            {
                "titulo": "Propone criterios de revisión (aceptar, ajustar, descartar)",
                "patrones": [r"verific|contrast|fuente", r"acept", r"ajust", r"descart"],
                "minimo": 3,
                "pista": "¿Qué verificarías, con qué fuentes y bajo qué criterios decidirías aceptar, ajustar o descartar?",
            },
            {
                "titulo": "Distingue qué delegar y qué conservar bajo criterio docente",
                "patrones": [r"delegar", r"criterio", r"agencia|juicio|autonomia", r"residuo cognitivo|operacion(es)? intelectual|proceso cognitivo|trabajo intelectual"],
                "minimo": 2,
                "pista": "¿Qué trabajo intelectual necesitás preservar para que la actividad siga siendo formativa? ¿Qué se puede delegar sin perder el criterio?",
            },
            {
                "titulo": "Considera responsabilidad, cuidado de datos y desigualdades",
                "patrones": [r"responsab", r"dato|privacidad|propiedad intelectual", r"desigualdad|acceso|brecha", r"acuerdo(s)? institucional|institucion"],
                "minimo": 1,
                "pista": "¿Qué responsabilidad docente, qué cuidado de datos y qué desigualdades de acceso o de alfabetización habría que considerar?",
            },
        ],
        "lectura": (
            "**Claves del Eje 2.** Siguiendo la guía de la UNESCO (2023), los sistemas generativos producen respuestas plausibles pero no necesariamente correctas. "
            "Cuatro riesgos estructurales: invenciones («alucinaciones»), simplificaciones y sesgos, desactualización (fecha de corte) y opacidad («caja negra»).\n\n"
            "• Verosimilitud no equivale a validez: la pregunta ya no es solo «¿qué respondió la IA?» sino «¿cómo sabemos que lo que respondió es válido?». "
            "Hoy resulta imprescindible enseñar a evaluar y auditar la información, no solo a buscarla.\n\n"
            "• Agencia humana: no delegar aquello que necesitamos aprender. Kap recupera la noción de «residuo cognitivo» (Salomon y Perkins): "
            "cuando una tecnología realiza parte de la tarea, ¿qué saberes, capacidades y criterios permanecen?\n\n"
            "• Delegar la ejecución repetible, no el criterio con el que se decide. Y las decisiones sobre usos habilitados, restringidos, "
            "privacidad y autoría exceden la práctica individual: requieren acuerdos institucionales."
        ),
        "preguntas": [
            "¿Qué tendría que hacer un estudiante con una respuesta de IA para que esa interacción sea una experiencia de aprendizaje?",
            "¿Qué voces y qué supuestos culturales pueden estar presentes (o ausentes) en lo que la IA produce?",
        ],
        "lecturas": [
            "UNESCO (Miao y Holmes) (2023). Guía para el uso de IA generativa en educación e investigación.",
            "Edelstein, G. (2022). El análisis en clave didáctica.",
            "Kap, M. (2024). Didáctica indisciplinada.",
        ],
    },
    3: {
        "eje": "Eje 3",
        "nombre": "Análisis de práctica y rediseño",
        "titulo": "Eje 3 · Análisis de la práctica y rediseño con IA: la consigna «leé y elaborá una síntesis»",
        "descripcion": (
            "Una consigna habitual de una cátedra de nivel superior dice: «Leé el texto y elaborá una síntesis de dos páginas». "
            "Varios estudiantes la resuelven pegando el texto en una IA y entregando el resultado con pocos cambios. "
            "El equipo docente duda entre prohibir el uso de IA o aceptarlo sin más."
        ),
        "consigna": (
            "Analizá la propuesta como un momento de tu práctica: qué aprendizaje buscaba promover y qué evidencia daba el producto. "
            "Luego rediseñala decidiendo qué lugar ocupa la IA (resolver, apoyar, interactuar y revisar, problematizar) y qué operaciones "
            "intelectuales querés preservar como experiencia propia del estudiante."
        ),
        "criterios": [
            {
                "titulo": "Analiza aprendizaje buscado y evidencia que da el producto",
                "patrones": [r"aprendizaje", r"evidencia", r"proposito|objetivo", r"operacion|proceso cognitivo"],
                "minimo": 2,
                "pista": "¿Qué querías que aprendiera el estudiante al sintetizar? ¿Qué evidencia de eso da, hoy, el producto entregado?",
            },
            {
                "titulo": "Sale del binomio «prohibir / aceptar sin más»",
                "patrones": [r"solucionismo|prohibicionismo|determinismo", r"ni (solucionar|prohibir|adaptar)", r"oportunidad.{0,20}amenaza", r"analizar.{0,20}decidir"],
                "minimo": 1,
                "pista": "Más allá de prohibir o adaptarse, ¿qué otra posición es posible? (Lion y Kap, 2024).",
            },
            {
                "titulo": "Primero lo pedagógico, después la tecnología",
                "patrones": [r"problema pedagogic", r"primero.{0,50}(propuesta|aprendizaje|pedagog|problema)", r"herramienta.{0,40}(despues|luego)|(despues|luego).{0,40}(tecnolog|herramienta|ia)", r"que necesito cambiar"],
                "minimo": 1,
                "pista": "¿Qué necesitás cambiar de tu propuesta para favorecer el aprendizaje y cómo podría ayudarte la IA (y no al revés)?",
            },
            {
                "titulo": "Define el nivel de interacción con la IA",
                "patrones": [r"resolver", r"apoyar|apoyo", r"interactuar|revisar|contrast|compar", r"problematizar|objeto de analisis"],
                "minimo": 2,
                "pista": "¿La IA va a resolver, apoyar, ser contrastada y revisada o ser objeto de análisis? ¿Podés justificar ese lugar?",
            },
            {
                "titulo": "Preserva la actividad intelectual y rediseña la evidencia",
                "patrones": [r"preserv|conserv|no (delegar|sustituy)|sin delegar", r"propia (sintesis|interpretacion|version)|primero.{0,30}propi", r"comparar|contrast", r"justific|fundament", r"identific.{0,30}(error|omision)|omision"],
                "minimo": 2,
                "pista": "¿Qué hace el estudiante antes, durante y después de consultar a la IA? ¿Qué evidencia nueva obtenés?",
            },
        ],
        "lectura": (
            "**Claves del Eje 3.** Lion y Kap (2024) advierten tres posiciones recurrentes ante una tecnología nueva: solucionismo tecnológico, "
            "prohibicionismo y determinismo tecnológico. Frente a ellas: «ni solucionar, ni prohibir, ni adaptarnos pasivamente: analizar, decidir y diseñar pedagógicamente».\n\n"
            "• Rediseñar no es sumar una herramienta: primero aparece el problema pedagógico, después la decisión didáctica y recién entonces se analiza "
            "qué puede aportar la IA. La pregunta pasa de «¿qué puedo hacer con IA?» a «¿qué necesito cambiar de mi propuesta y cómo puede ayudarme la IA?».\n\n"
            "• Cuatro niveles de interacción (no jerárquicos): resolver, apoyar, interactuar y revisar, problematizar. Lo importante es poder justificar "
            "qué lugar ocupa la IA y qué actividad intelectual se promueve.\n\n"
            "• Ejemplo del eje: el estudiante elabora primero su interpretación, pide a la IA una síntesis alternativa, las compara, identifica omisiones, "
            "verifica afirmaciones, vuelve al texto y construye una síntesis propia. La diferencia no está en la herramienta, sino en la actividad cognitiva que demanda.\n\n"
            "• La matriz de análisis (propósito, actividad, consigna, rol docente, rol del estudiante, IA, evidencias, fundamentación) ayuda a decidir "
            "qué conservar y qué transformar."
        ),
        "preguntas": [
            "¿Qué cambió en la propuesta y por qué considerás que ese cambio genera mejores oportunidades de aprendizaje?",
            "¿Qué evidencias te mostrarán, después de implementar el rediseño, lo que tus estudiantes están aprendiendo?",
        ],
        "lecturas": [
            "Lion, C. y Kap, M. (2024). Las inteligencias artificiales generativas desde un prisma multidimensional.",
            "Anijovich, R. y Cappelletti, G. (2017). La evaluación como oportunidad. Cap. 3.",
            "Anijovich, R. y Cappelletti, G. (2023). Planificar la enseñanza: Tramas y alternativas.",
        ],
    },
    4: {
        "eje": "Eje 4",
        "nombre": "IA formativa y evaluación situada",
        "titulo": "Eje 4 · IA como dispositivo formativo y evaluación situada: evidenciar el proceso sin vigilar",
        "descripcion": (
            "Para «asegurarse» de que sus estudiantes no hacen trampa con IA, una docente exige: el informe final, todos los borradores, "
            "el historial completo de conversaciones con la IA, capturas de pantalla, un diario de aprendizaje y, además, una defensa oral. "
            "Los estudiantes con menos acceso a las herramientas o con menos experiencia se sienten bajo sospecha."
        ),
        "consigna": (
            "Analizá la propuesta desde la evaluación situada. ¿Qué evidencias necesitás realmente para reconocer el aprendizaje que querés promover? "
            "Rediseñá la evaluación para que el proceso sea visible sin convertirla en vigilancia, y decidí qué lugar puede tener la IA en la retroalimentación."
        ),
        "criterios": [
            {
                "titulo": "Diferencia vigilancia de evaluación formativa",
                "patrones": [r"vigilancia|control|sospecha", r"formativ", r"transparencia"],
                "minimo": 2,
                "pista": "¿Qué parte de lo que se pide funciona como control y qué parte permite al estudiante reconstruir y comunicar su aprendizaje?",
            },
            {
                "titulo": "Define qué evidenciar (producto, proceso, desempeño, argumentación con fuentes)",
                "patrones": [r"producto", r"proceso", r"desempeno", r"argumentacion|fuentes", r"acumul|seleccion|no (se trata de )?(sumar|multiplicar)"],
                "minimo": 3,
                "pista": "¿Qué necesitás observar para reconocer el aprendizaje? ¿Todo lo que se pide es necesario o se está acumulando evidencia?",
            },
            {
                "titulo": "Elige instrumentos con sentido (rúbrica, portafolio, diario, defensa)",
                "patrones": [r"rubrica", r"portafolio", r"diario|bitacora", r"defensa|argumentacion oral|exposicion|conversacion"],
                "minimo": 1,
                "pista": "¿Qué instrumento haría visible el proceso con menos carga y con criterios conocidos desde el inicio?",
            },
            {
                "titulo": "Analiza la retroalimentación mediada por IA con criterios",
                "patrones": [r"retroalimentacion|devolucion", r"pertinen|oportun", r"valid", r"especific|generic", r"alucin|error|conceptualmente", r"orientacion|pistas|preguntas"],
                "minimo": 2,
                "pista": "Si la IA ofrece devoluciones, ¿con qué criterios las valorarías (oportunidad, pertinencia, comprensibilidad, validez, especificidad, orientación hacia la acción)?",
            },
            {
                "titulo": "Considera autoría, transparencia y justicia curricular",
                "patrones": [r"autoria", r"acceso|desigualdad|justicia", r"alfabetiz|ensenar a usar|ensenad", r"transparen"],
                "minimo": 2,
                "pista": "¿Cómo entendés la autoría cuando hay IA? ¿Qué condiciones de acceso y de alfabetización hay que prever para no exigir un saber que no se enseñó?",
            },
        ],
        "lectura": (
            "**Claves del Eje 4.** La IA hace insuficiente la relación «lo que el estudiante entrega = lo que aprendió». Las evidencias pueden ser: "
            "producto, proceso (decisiones, fuentes consultadas, revisiones), desempeño (qué puede explicar o resolver frente a situaciones nuevas) "
            "y argumentación con fuentes. No se trata de sumar requisitos para comprobar que «el estudiante realmente hizo el trabajo», sino de diseñar "
            "situaciones en las que el aprendizaje pueda hacerse visible.\n\n"
            "• Acumular producto final, borradores, historial de prompts, capturas, diario y defensa puede transformar la evaluación en un dispositivo de "
            "vigilancia más que de formación. La pregunta es: ¿qué evidencia necesito para reconocer lo que quiero que el estudiante aprenda?\n\n"
            "• Autoría: puede entenderse como la capacidad de apropiarse de la producción y dar cuenta de las decisiones tomadas (para qué usó IA, qué recuperó, "
            "qué descartó, cómo verificó). La transparencia no es vigilancia: es una oportunidad formativa.\n\n"
            "• Retroalimentación con IA: criterios para analizarla (oportunidad, pertinencia, comprensibilidad, validez, especificidad, orientación hacia la acción). "
            "Recibir más devoluciones no es recibir mejores devoluciones.\n\n"
            "• Justicia curricular y epistémica: prever acceso, alfabetización y apoyos, evitando convertir en requisito implícito un saber que no fue enseñado. "
            "Con Maggio (2026): la IA «hackea» tareas que eran fáciles de resolver; es una oportunidad para interrogar esas propuestas."
        ),
        "preguntas": [
            "¿Qué evidencia mínima de proceso pedirías, y cómo les enseñarías a producirla?",
            "¿Qué parte de la retroalimentación podría apoyar la IA sin perder autoridad docente, y cuál no conviene delegar?",
        ],
        "lecturas": [
            "Anijovich, R. y Cappelletti, G. (2023). Evidencias de aprendizaje y evaluación formativa.",
            "Anijovich, R. y González, C. (2017). El portafolio como dispositivo para seleccionar y reflexionar sobre evidencias de aprendizaje.",
            "Castañeda, L. (2024). Inteligencia artificial, evaluación y accountability educativa.",
            "Maggio, M. (2026). La IA generativa como hackeo a la evaluación: hacia una didáctica en vivo.",
        ],
    },
}

CAMPOS_PUBLICOS = ("eje", "nombre", "titulo", "descripcion", "consigna")


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def criterio_cubierto(criterio, texto):
    coincidencias = sum(1 for patron in criterio["patrones"] if re.search(patron, texto))
    return coincidencias >= criterio["minimo"]


@app.route("/")
def index():
    publicos = {
        str(caso_id): {campo: caso[campo] for campo in CAMPOS_PUBLICOS}
        for caso_id, caso in CASOS.items()
    }
    return render_template("simulador.html", casos=publicos)


@app.route("/evaluar", methods=["POST"])
def evaluar():
    data = request.get_json(silent=True) or {}
    try:
        caso = CASOS.get(int(data.get("caso_id")))
    except (TypeError, ValueError):
        caso = None
    if not caso:
        return jsonify({"error": "Eje no encontrado."}), 404

    respuesta = str(data.get("respuesta", "")).strip()[:MAX_CARACTERES]
    texto = normalizar(respuesta)

    if len(respuesta.split()) < MIN_PALABRAS:
        return jsonify({
            "estado": "breve",
            "resumen": (
                f"Tu respuesta todavía es breve (menos de {MIN_PALABRAS} palabras). "
                "Desarrollá tu análisis; estas preguntas pueden ayudarte a empezar."
            ),
            "pendientes": [{"titulo": c["titulo"], "pista": c["pista"]} for c in caso["criterios"]],
            "cubiertos": [],
        })

    cubiertos = [c["titulo"] for c in caso["criterios"] if criterio_cubierto(c, texto)]
    pendientes = [
        {"titulo": c["titulo"], "pista": c["pista"]}
        for c in caso["criterios"]
        if not criterio_cubierto(c, texto)
    ]

    total = len(caso["criterios"])
    if not pendientes:
        resumen = "Tu análisis recupera todos los ejes de lectura del caso. Contrastalo con la lectura del eje y seguí profundizando con las preguntas."
    elif len(cubiertos) >= total - 2:
        resumen = "Tu análisis recupera buena parte de los ejes de lectura del caso. Te quedan algunos por considerar."
    else:
        resumen = "Tu análisis recupera algunos ejes de lectura del caso. Revisá los que aparecen pendientes y volvé a escribir."

    return jsonify({
        "estado": "ok",
        "resumen": resumen,
        "cubiertos": cubiertos,
        "pendientes": pendientes,
        "lectura": caso["lectura"],
        "preguntas": caso["preguntas"],
        "lecturas": caso["lecturas"],
        "aviso": (
            "Esta devolución es automática: detecta conceptos clave del eje en tu texto, pero no valora la calidad de tu argumentación. "
            "Compartí tu análisis en el foro o en el encuentro sincrónico para ponerlo en diálogo con otros/as colegas."
        ),
    })


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
