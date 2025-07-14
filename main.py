from flask import Flask, request, jsonify
import unicodedata
from flask_cors import CORS
from rapidfuzz import fuzz
import os
import random

print('')

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*", "methods": ["POST"]}})

responses = {
    "quiénes somos": {
        "respuesta": "Somos Chanco3D, una empresa innovadora y especializada en la creación de piezas personalizadas con resina. Nos dedicamos a diseñar y fabricar modelos tridimensionales de alta calidad, adaptados a las necesidades de nuestros clientes. Utilizamos tecnología avanzada de impresión 3D en resina para ofrecer detalles precisos y acabados excepcionales, ideales para una variedad de aplicaciones, desde figuras decorativas y prototipos hasta productos personalizados para ocasiones especiales.",
        "palabras_clave": [
            "empresa", "quienes somos", "que hacemos", "informacion", "nosotros", "identidad",
            "quienes son", "acerca de la empresa", "que hacen", "que son", "dame mas informacion",
            "sobre la empresa", "presentacion", "historia de la empresa", "acerca de nosotros",
            "qué es chanco3d", "informacion de la empresa", "empresa chanco3d"
        ]
    },
    "tiempo estimado de la entrega": {
        "respuesta": "El tiempo estimado de entrega depende del proyecto, pero suele oscilar entre 3 y 7 días hábiles después de finalizar la impresión. Para proyectos más complejos o personalizados, el tiempo puede extenderse hasta 10 días hábiles.",
        "palabras_clave": [
            "como en cuanto estara", "cuando estara", "cuando llegara", "cuanto tiempo tomara",
            "cuanto tiempo tardara", "cuanto tardara", "cuanto tomara de tiempo", "en cuanto llega",
            "tiempo estimado", "cuando llega", "cuanto demora", "cuando llega el envio",
            "cual es el plazo", "cuando entregan", "cuando tarda en llegar", "cuanto tarda en llegar",
            "cual es el tiempo estimado", "cuando me llegara", "aproximadamente en cuanto",
            "aproximadamente cuando", "cuando entrega", "cuando me llega mi pedido",
            "cuando me llega mi entrega", "cuando se hacen entregas", "cuando entregas",
            "plazo de entrega", "tiempo de envio", "tiempo de entrega estimado"
        ]
    },
    "qué materiales trabajamos en la empresa": {
        "respuesta": "En nuestra empresa, nos especializamos principalmente en el uso de resina fotopolimérica a base de agua, un material innovador y de alta calidad que nos permite obtener resultados excepcionales en cada proyecto.",
        "palabras_clave": [
            "con que materiales", "con que trabajan", "material que se ocupa", "fotopolimero",
            "de que esta hecho", "con que material", "de que esta hecha", "con que se hace",
            "material con el cual se hace", "material de elaboracion", "material de fabricacion",
            "materiales usados", "materiales que utilizan", "material para imprimir", "tipo de material",
            "material para piezas", "resina que usan", "material resina", "de que son las piezas"
        ]
    },
    "por qué elegirnos a nosotros": {
        "respuesta": "Ofrecemos un trato cercano, productos personalizados, materiales de calidad y una ética de trabajo responsable porque creemos que la satisfacción del cliente es nuestra máxima prioridad. Nos esforzamos por conocer y entender las necesidades de cada persona para brindar soluciones únicas que se adapten a sus expectativas. Además, seleccionamos solo materiales de la más alta calidad para garantizar que nuestros productos sean duraderos y eficaces. Todo esto lo hacemos con un enfoque ético, actuando con responsabilidad y transparencia en cada paso, lo que nos permite construir relaciones de confianza y brindar un servicio que realmente marque la diferencia.",
        "palabras_clave": [
            "porque elegirnos", "por qué elegir", "beneficios de trabajar con ustedes",
            "beneficios de contactarnos", "comparación", "porque los elegimos", "porque con ustedes",
            "porque debemos elegirlos", "beneficio de elegirlos", "beneficio de trabajar con ustedes",
            "beneficio de contactarlos", "ventajas de elegirlos", "razones para elegirlos",
            "por que comprar con ustedes", "que ventajas ofrecen", "por que elegir chanco3d"
        ]
    },
    "ventajas del uso de resina": {
        "respuesta": (
    "La resina ofrece múltiples ventajas:\n"
    "1) Alta precisión en detalles finos,\n"
    "2) Superficies lisas que requieren poco post-procesado,\n"
    "3) Gran variedad de propiedades mecánicas,\n"
    "4) Resistencia al agua y a la intemperie,\n"
    "y 5) Ideal para piezas con geometrías complejas."
),
        "palabras_clave": [
            "calidad ofrece", "que resolucion", "que tanta resolucion", "que resistencia tienen",
            "resistencia de la resina", "definicion", "ventajas de la resina", "beneficios del uso de resina",
            "beneficios resina", "por qué resina", "resina vs otros", "porque es mejor la resina",
            "porque debo imprimir en resina", "porque la resina es mejor", "la resina es mejor",
            "la resina es superior", "beneficios de usar resina", "mejoras de la resina",
            "ventajas resina fotopolimerica", "por que usar resina", "resina detalles"
        ]
    },
    "en donde se hacen entregas": {
        "respuesta": "Actualmente realizamos entregas exclusivamente en León, Guanajuato. Estamos trabajando para expandir nuestro servicio a todo México. Para envíos especiales fuera de esta zona, contáctanos para evaluar posibilidades.",
        "palabras_clave": [
            "en que lugares", "donde entregas", "donde se entrega", "ubicación de entrega", "cobertura",
            "donde hacen envios", "zona", "donde entregan", "donde se envio", "a que ciudades se entrega",
            "a que estado se entrega", "donde puedo comprar", "en que zona puedo comprar",
            "donde venden", "donde realizan entregas", "lugar de entrega", "zonas de reparto",
            "zona de cobertura", "ciudades de entrega"
        ]
    },
    "tengo un problema con mi producto": {
        "respuesta": "¡Lamentamos los inconvenientes! Por favor contáctanos a <a href='mailto:Chanco3D@gmail.com'>Chanco3D@gmail.com</a> con: 1) Tu número de pedido, 2) Descripción del problema, y 3) Fotos si aplica. Nuestro equipo te responderá en menos de 24 horas hábiles con una solución.",
        "palabras_clave": [
            "tengo un problema", "queja", "reclamo", "dañado", "problemon", "problemas con producto",
            "tengo unos problemas", "hay un problema", "tengo una duda", "producto defectuoso", "problema con pedido",
            "producto mal", "fallo producto", "producto no funciona", "producto roto", "producto dañado"
        ]
    },
    "qué tipo de figuras imprimen en 3d": {
        "respuesta": "En Chanco3D, nos especializamos en la impresión de figuras personalizadas y model kits. Utilizando tecnología avanzada de impresión 3D en resina, transformamos tus ideas y diseños en piezas únicas con detalles excepcionales. Ya sea que busques una figura personalizada que capture un personaje o momento especial, o un model kit que puedas ensamblar y pintar, estamos aquí para hacer realidad tu visión.",
        "palabras_clave": [
            "que figuras imprimen", "que modelos imprimen", "productos manejan", "piezas hacen", "que imprimen",
            "que venden", "que ofrecen", "que productos ofrecen", "que servicio ofrecen", "en que se especializan",
            "que puedo comprar", "que piezas venden", "que es lo que ofrecen", "que es lo que venden",
            "que servicios ofrecen", "servicio ofrecen", "modelos 3d", "tipos de figuras", "figuras 3d",
            "modelos personalizados", "model kits", "figuras personalizadas"
        ]
    },
    "puedo enviar mi propio modelo 3d para que lo impriman": {
        "respuesta": "¡Sí! Aceptamos archivos en formatos .STL u .OBJ Recomendamos: 1) Que el modelo esté optimizado para impresión.",
        "palabras_clave": [
            "propio modelo", "enviar modelo", "archivo", "STL", "OBJ", "diseño propio", "custom",
            "diseño custom", "quiero un diseño propio", "quiero un producto personalizado",
            "quiero algo personalizado", "quiero algo unico", "necesito un custom", "quiero algo propio",
            "pueden hacer custom", "pueden personalizar", "archivo 3d propio", "enviar archivo 3d"
        ]
    },
    "venden kits de pintura y pinceles": {
        "respuesta": "Sí, en Chanco3D ofrecemos kits de pintura y pinceles especialmente diseñados para que puedas personalizar tus figuras impresas en 3D. Cada kit incluye una selección de colores vibrantes y pinceles de alta calidad, perfectos para trabajos de detalle y acabados precisos.",
        "palabras_clave": [
            "kits", "pintura", "pinceles", "materiales pintura", "venden kits", "venden model kits",
            "venden pinturas", "kit de pintura", "kit para pintar", "pinturas para figuras",
            "material para pintar", "pinceles para figuras"
        ]
    },
    "Que pasa si mi modelo tiene errores": {
        "respuesta": "Si tu modelo presenta errores o no es imprimible, nuestro equipo especializado realizará una revisión detallada y te notificaremos sobre los ajustes necesarios. Estamos aquí para ayudarte en todo el proceso: podemos asesorarte para corregir el modelo y asegurarnos de que sea perfectamente funcional para la impresión. Si prefieres, también podemos diseñar un modelo alternativo que cumpla con tus expectativas y requisitos.",
        "palabras_clave": [
            "errores", "no es imprimible", "no esta bien mi modelo", "mi modelo tiene un problema",
            "mi modelo tiene un error", "tengo un error con mi modelo", "tengo un problema con mi custom",
            "problemas con modelo", "modelo defectuoso", "modelo mal", "modelo con fallas"
        ]
    },
    "Tamaño maximo de impresion": {
        "respuesta": "El modelo impreso puede alcanzar un tamaño máximo de 12.7 x 8 x 16 cm, lo que garantiza un equilibrio entre detalle, estabilidad y compatibilidad con el proceso de impresión.",
        "palabras_clave": [
            "de que tamaño", "tamaño maximo", "que tan grande", "se podra imprimir por el tamaño",
            "y si es muy grande", "se podra imprimir", "y si no cabe", "limites de tamaño",
            "medidas maximas", "dimensiones maximas", "tamaño permitido"
        ]
    },
    "cómo puedo hacer un pedido": {
        "respuesta": "Para hacer un pedido, solo necesitas contactarnos por mensaje directo o a través de nuestro correo. Cuéntanos qué figura deseas, si tienes un modelo o necesitas uno personalizado, y nosotros te guiaremos paso a paso. También estamos trabajando en una tienda en línea para que puedas hacerlo todo desde la web.",
        "palabras_clave": [
            "hacer pedido", "cómo encargar", "quiero comprar", "quiero pedir", "realizar pedido",
            "como comprar", "quiero ordenar", "como puedo pedir", "puedo hacer un pedido", "quiero una figura",
            "pasos para pedir", "como hago un pedido", "como encargo", "hacer un encargo"
        ]
    },
    "puedo pedir una figura pintada": {
        "respuesta": "Sí, ofrecemos la opción de figuras pintadas bajo pedido especial. Puedes elegir entre pintura completa o detalles personalizados. También puedes optar por recibir tu figura sin pintar junto a un kit de pintura para personalizarla tú mismo.",
        "palabras_clave": [
            "figura pintada", "pintan las figuras", "coloreadas", "entregan pintadas", "quiero pintada",
            "venden ya pintadas", "pueden pintarla", "pueden pintarlo", "colorean", "quiero que venga pintada",
            "figuras con pintura", "figura con color", "figura coloreada"
        ]
    },
    "cómo cuidar mi figura impresa": {
        "respuesta": "Para conservar tu figura impresa en buen estado, evita la exposición directa al sol y al calor extremo. Límpiala con un paño seco y guárdala en un lugar fresco. Si está pintada, evita productos de limpieza con químicos.",
        "palabras_clave": [
            "cuidar figura", "conservar figura", "cómo limpiar", "mantenimiento", "me dura mucho",
            "como se cuida", "limpiar resina", "como lo cuido", "cuidados", "tips de cuidado",
            "consejos para cuidar", "limpieza figura", "mantener figura"
        ]
    },
    "aceptan pagos con tarjeta o transferencia": {
        "respuesta": "Aceptamos pagos por transferencia bancaria, depósito y pagos con tarjeta vía plataformas como Mercado Pago. Escríbenos para darte los datos exactos según el método que prefieras.",
        "palabras_clave": [
            "aceptan tarjeta", "como pagar", "metodos de pago", "formas de pago", "se puede pagar con tarjeta",
            "aceptan transferencia", "aceptan mercado pago", "puedo pagar en línea", "formas de pago aceptadas",
            "pago con tarjeta", "pago por transferencia"
        ]
    },
    "puedo pedir una figura de un videojuego o anime": {
        "respuesta": "¡Claro! Podemos imprimir figuras basadas en videojuegos, anime o personajes personalizados. Solo asegúrate de que el diseño que nos compartas no infrinja derechos si es para uso comercial.",
        "palabras_clave": [
            "anime", "videojuego", "quiero un personaje", "figura de juego", "figura anime",
            "quiero una figura de", "pueden hacerme un personaje", "de un juego", "figuras de anime",
            "figuras de videojuego", "personajes de juegos", "personajes anime"
        ]
    },
    "pueden hacer prototipos o piezas funcionales": {
        "respuesta": "Sí, realizamos prototipos personalizados y piezas funcionales en resina con gran precisión. Ideal para pruebas, diseño de productos o ingeniería. Cuéntanos qué necesitas y lo evaluamos juntos.",
        "palabras_clave": [
            "pueden funcionar", "funcionales", "prototipo", "pieza funcional", "pieza para trabajo",
            "pieza tecnica", "pieza de ingenieria", "pieza mecanica", "pieza util", "pieza para producto",
            "prototipos personalizados", "piezas técnicas"
        ]
    },
    "tienen tienda física o solo en línea": {
        "respuesta": "Por el momento trabajamos bajo pedido y atendemos en línea. No contamos con una tienda fisica, pero puedes contactarnos para entregas locales en León, Guanajuato.",
        "palabras_clave": [
            "tienda fisica", "donde estan", "tienen local", "puedo visitar", "donde puedo ir",
            "venden en local", "solo online", "solo en linea", "tienda online", "venta en linea"
        ]
    },
    "cómo puedo rastrear mi pedido": {
        "respuesta": "Una vez que tu pedido haya sido enviado, te enviaremos un número de rastreo por correo o mensaje. Así podrás monitorear su progreso hasta que llegue a tus manos.",
        "palabras_clave": [
            "rastrear", "seguimiento", "donde esta mi pedido", "en que va", "numero de guia",
            "ya enviaron", "como va mi pedido", "seguimiento de pedido", "numero de rastreo"
        ]
    },
    "puedo agendar una cita para asesoría": {
        "respuesta": "Sí, puedes agendar una asesoría personalizada por llamada o mensaje. Te orientamos en diseño, impresión y acabados. Contáctanos y coordinamos una fecha.",
        "palabras_clave": [
            "asesoria", "consulta", "quiero ayuda", "quiero que me asesoren", "puedo agendar",
            "quiero una reunion", "me pueden orientar", "cita para asesoría", "asesoramiento",
            "asesoria personalizada"
        ]
    },
    "como empiezo si no tengo modelo 3d": {
        "respuesta": "¡No te preocupes! Si no tienes un modelo 3D, nuestro equipo puede ayudarte a diseñarlo desde cero. Solo cuéntanos tu idea, referencias o bocetos y nosotros nos encargamos del resto.",
        "palabras_clave": [
            "no tengo modelo", "como empiezo", "no se modelar", "me ayudan con diseño",
            "pueden modelar", "hacer modelo por mi", "no tengo archivo", "necesito ayuda para diseño",
            "diseñar desde cero", "ayuda con modelo 3d"
        ]
    },
    "pueden escalar una figura a un tamaño especifico": {
        "respuesta": "Sí, podemos ajustar el tamaño de tu figura a las dimensiones que necesites, siempre que sea físicamente posible dentro de los límites de impresión. Solo dinos las medidas deseadas.",
        "palabras_clave": [
            "escalar figura", "hacerla mas grande", "hacerla mas chica", "ajustar tamaño",
            "pueden redimensionar", "escala personalizada", "necesito otro tamaño",
            "cambiar tamaño", "redimensionar figura"
        ]
    },
    "cuanto cuesta una figura personalizada": {
        "respuesta": "El costo depende del tamaño, nivel de detalle y si ya tienes el archivo 3D o necesitas que lo diseñemos. Escríbenos con tu idea y te damos una cotización sin compromiso.",
        "palabras_clave": [
            "cuanto cuesta", "precio figura", "valor figura", "cuanto vale", "que precio tiene",
            "precio personalizado", "precio custom", "me cotizas", "costo de figura",
            "cuanto cobran", "cotización"
        ]
    },
    "puedo combinar partes de varias figuras en una sola": {
        "respuesta": "Sí, podemos combinar diferentes elementos de varias figuras para crear una nueva pieza personalizada. Solo asegúrate de tener derechos o permisos sobre los archivos si no son propios.",
        "palabras_clave": [
            "combinar figuras", "juntar partes", "mezclar modelos", "usar partes diferentes",
            "hacer mashup", "fusionar modelos", "hacer figura combinada", "combinar modelos",
            "unir figuras"
        ]
    },
    "pueden imprimir en otros materiales ademas de resina": {
        "respuesta": "Actualmente trabajamos principalmente con resina por su detalle y calidad, pero estamos explorando la integración de filamento PLA y otros materiales para el futuro cercano.",
        "palabras_clave": [
            "otros materiales", "solo resina", "usan pla", "usan filamento",
            "impresion en otro material", "impresion con pla", "resina o pla",
            "material alternativo", "materiales de impresion"
        ]
    },
    "ofrecen servicio de modelado 3d": {
        "respuesta": "Sí, contamos con servicio de modelado 3D desde cero. Solo dinos tu idea, referencias o bocetos y te enviaremos una propuesta de diseño personalizada.",
        "palabras_clave": [
            "servicio de modelado", "pueden modelar", "diseñan 3d", "diseño personalizado",
            "hacen modelos", "modelado desde cero", "crear figura", "modelado 3d",
            "diseño 3d personalizado"
        ]
    },
    "que tipo de archivos aceptan para impresion": {
        "respuesta": "Los formatos que aceptamos son principalmente STL y OBJ. Si tienes otro tipo de archivo, puedes consultarnos para ver si es compatible.",
        "palabras_clave": [
            "que archivo aceptan", "archivos validos", "formato compatible", "formatos soportados",
            "que formatos usan", "puedo enviar este archivo", "formatos de archivo",
            "formatos para imprimir"
        ]
    },
    "puedo ver avances de mi pedido": {
        "respuesta": "Sí, durante el proceso te enviaremos avances del diseño o fotos del modelo antes de imprimir. Queremos que estés completamente satisfecho antes de finalizar.",
        "palabras_clave": [
            "puedo ver avances", "mandan fotos", "ver progreso", "me muestran avances",
            "puedo ver como va", "puedo ver diseño", "avances de pedido", "fotos del progreso"
        ]
    },
    "pueden hacer llaveros personalizados": {
        "respuesta": "¡Claro! Podemos crear llaveros personalizados en 3D con nombres, logotipos o personajes. Son una excelente opción para regalos o eventos.",
        "palabras_clave": [
            "llaveros", "llavero personalizado", "hacen llaveros", "quiero un llavero",
            "pueden hacer llavero", "personalizar llavero", "llaveros 3d"
        ]
    },
    "que colores de resina manejan": {
        "respuesta": "Trabajamos principalmente con resina azul para usarlo como base, pero también podemos imprimir en resina blanca bajo pedido especial. En general, el color base no afecta la calidad del modelo, ya que muchos clientes los pintan después.",
        "palabras_clave": [
            "colores resina", "color de la resina", "de que color imprimen", "que color usan",
            "puede ser otro color", "colores disponibles", "puede ser blanca", "puede ser negra",
            "resina blanca", "resina gris", "resina negra", "color base", "resinas de colores"
        ]
    }
}





}

#hola

default_responses = [
    "No estoy seguro de entender. ¿Podrías reformular tu pregunta?",
    "No tengo información sobre ese tema. Prueba con alguna de nuestras preguntas frecuentes.",
    "Mi conocimiento es limitado sobre ese tema. ¿Quieres preguntar sobre algo más?"
]

def remove_accents(input_str):
    try:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    except:
        return input_str

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '').lower().strip()
    user_input = remove_accents(user_input)

    best_match = None
    best_score = 0

    # Comparación con las claves principales
    for key, value in responses.items():
        normalized_key = remove_accents(key.lower())
        score = fuzz.ratio(user_input, normalized_key)
        if score > best_score:
            best_match = value["respuesta"]
            best_score = score

    if best_score >= 70:
        return jsonify({'reply': best_match})

    # Comparación con palabras clave
    for key, value in responses.items():
        for keyword in value["palabras_clave"]:
            normalized_keyword = remove_accents(keyword.lower())
            score = fuzz.partial_ratio(user_input, normalized_keyword)
            if score >= 70:
                return jsonify({'reply': value["respuesta"]})

    return jsonify({'reply': random.choice(default_responses)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)