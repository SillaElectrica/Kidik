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
        "respuesta": "Somos Chanco3D, una empresa innovadora y especializada en la creación de piezas personalizadas con resina. Nos dedicamos a diseñar y fabricar modelos tridimensionales de alta calidad...",
        "palabras_clave": [
            "identidad corporativa", "historia organizacional", "filosofía empresarial", 
            "cultura organizacional", "valores fundacionales", "antecedentes históricos",
            "estructura organizacional", "equipo fundador", "orígenes compañía",
            "principios rectores", "visión corporativa", "mision empresarial",
            "contexto fundacional", "legado empresarial", "esencia corporativa",
            "fundadores empresa", "trayectoria institucional", "código ético",
            "ADN empresarial", "propósito corporativo"
        ]
    },
    "tiempo estimado de la entrega": {
        "respuesta": "El tiempo estimado de entrega depende del proyecto...",
        "palabras_clave": [
            "duración fabricación", "tiempo producción", "plazo ejecución",
            "espera producto", "demora logística", "periodo fabricación",
            "tiempo manufactura", "cronograma entrega", "rapidez despacho",
            "velocidad producción", "tiempo estándar", "duración aproximada",
            "fecha recepción", "tiempo proceso", "ventana entrega",
            "calendario producción", "plazo máximo", "tiempo mínimo",
            "horario envíos", "estimación logística"
        ]
    },
    "qué materiales trabajamos en la empresa": {
        "respuesta": "En nuestra empresa, nos especializamos principalmente en el uso de resina fotopolimérica a base de agua, un material innovador y de alta calidad que nos permite obtener resultados excepcionales en cada proyecto.",
        "palabras_clave": [
            "composicion resina", "tipo fotopolimero", "especificaciones tecnicas",
            "caracteristicas material", "propiedades resina", "componentes quimicos",
            "formulacion material", "tecnologia resina", "innovacion materiales",
            "ventajas fotopolimero", "comparativa materiales", "calidad resina",
            "certificaciones material", "seguridad quimica", "resistencia material",
            "durabilidad piezas", "especificaciones fabricacion", "detalles tecnicos",
            "informacion material", "tecnologia impresion"
        ]
    },
    "por qué elegirnos a nosotros": {
        "respuesta": "Ofrecemos un trato cercano, productos personalizados, materiales de calidad y una ética de trabajo responsable porque creemos que la satisfacción del cliente es nuestra máxima prioridad. Nos esforzamos por conocer y entender las necesidades de cada persona para brindar soluciones únicas que se adapten a sus expectativas. Además, seleccionamos solo materiales de la más alta calidad para garantizar que nuestros productos sean duraderos y eficaces. Todo esto lo hacemos con un enfoque ético, actuando con responsabilidad y transparencia en cada paso, lo que nos permite construir relaciones de confianza y brindar un servicio que realmente marque la diferencia.",
        "palabras_clave": [
            "diferenciacion competencia", "excelencia servicio", "calidad superior",
            "experiencia unica", "valor agregado", "ventajas exclusivas",
            "beneficios especiales", "razones preferirnos", "motivos elegir",
            "diferencias competidores", "exclusividad servicio", "garantias calidad",
            "compromiso cliente", "atencion personalizada", "enfoque premium",
            "servicio diferenciado", "calidad garantizada", "experiencia compra",
            "satisfaccion asegurada", "confiabilidad empresa"
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
            "beneficios resina", "resina vs otros", "superioridad resina",
            "comparativa ventajas", "pros resina", "fortalezas material",
            "rendimiento resina", "eficiencia fotopolimero", "resultados superiores",
            "calidad impresion", "precisión detalles", "nitidez impresion",
            "fidelidad reproduccion", "exactitud dimensional", "terminado profesional",
            "acabado premium", "ventajas tecnicas", "performance material",
            "eficacia resina", "productividad impresion"
        ]
    },
    "en donde se hacen entregas": {
        "respuesta": "Actualmente realizamos entregas exclusivamente en León, Guanajuato. Estamos trabajando para expandir nuestro servicio a todo México. Para envíos especiales fuera de esta zona, contáctanos para evaluar posibilidades.",
        "palabras_clave": [
            "cobertura geografica", "zonas servicio", "localizacion entregas",
            "region cubierta", "alcance logistico", "distribucion pedidos",
            "radio entrega", "ubicaciones servicio", "municipios atendidos",
            "localidades cubiertas", "expansion futura", "nuevas zonas",
            "ampliacion cobertura", "envios proximamente", "lugares disponibles",
            "ciudades actuales", "entregas locales", "servicio regional",
            "area operaciones", "territorio actual"
        ]
    },
    "tengo un problema con mi producto": {
        "respuesta": (
            "¡Lamentamos los inconvenientes!\n"
            "Por favor contáctanos a <a href='mailto:Chanco3D@gmail.com'>Chanco3D@gmail.com</a> con:\n"
            "1) Tu número de pedido,\n"
            "2) Descripción del problema,\n"
            "3) Fotos si aplica.\n"
            "Nuestro equipo te responderá en menos de 24 horas hábiles en mensaje directo con una solución."
        ),
        "palabras_clave": [
            "incidencia producto", "falla fabricacion", "error pedido",
            "defecto pieza", "imperfeccion", "daño recibido",
            "problema calidad", "reclamo producto", "solicitud garantia",
            "averia figura", "mal estado", "defectuoso recibido",
            "inconformidad producto", "reparacion pieza", "cambio producto",
            "devolucion posible", "reembolso pedido", "queja formal",
            "reporte falla", "soporte tecnico"
        ]
    },
    "qué tipo de figuras imprimen en 3d": {
        "respuesta": "En Chanco3D, nos especializamos en la impresión de figuras personalizadas y model kits. Utilizando tecnología avanzada de impresión 3D en resina, transformamos tus ideas y diseños en piezas únicas con detalles excepcionales. Ya sea que busques una figura personalizada que capture un personaje o momento especial, o un model kit que puedas ensamblar y pintar, estamos aquí para hacer realidad tu visión.",
        "palabras_clave": [
            "catalogo productos", "tipologia figuras", "modelos disponibles",
            "variedad piezas", "ejemplos impresion", "muestras trabajo",
            "coleccion figuras", "gama productos", "lineas produccion",
            "especializaciones impresion", "categorias figuras", "estilos disponibles",
            "tematicas impresion", "diseños habituales", "productos estrella",
            "impresiones comunes", "piezas tipicas", "modelos frecuentes",
            "creaciones habituales", "figuras populares"
        ]
    },
    "puedo enviar mi propio modelo 3d para que lo impriman": {
        "respuesta": (
            "¡Sí! Aceptamos archivos en formatos .STL u .OBJ\n\n"
            "Recomendamos:\n"
            "1) Que el modelo esté optimizado para impresión,\n"
            "2) Que no tenga errores de malla o huecos,\n"
            "3) Que esté en la escala correcta,\n"
            "4) Y que venga orientado de forma adecuada si es posible."
        ),
        "palabras_clave": [
            "archivos aceptados", "formatos compatibles", "requisitos modelo",
            "especificaciones archivo", "preparacion modelo", "optimizacion impresion",
            "checklist impresion", "validacion archivos", "diseño propio",
            "creacion personal", "modelado externo", "archivos terceros",
            "diseños cliente", "propiedad intelectual", "derechos autor",
            "licencias uso", "originalidad diseños", "autoria modelos",
            "verificacion archivos", "comprobacion modelos"
        ]
    },
    "venden kits de pintura y pinceles": {
        "respuesta": "Sí, en Chanco3D ofrecemos kits de pintura y pinceles especialmente diseñados para que puedas personalizar tus figuras impresas en 3D. Cada kit incluye una selección de colores vibrantes y pinceles de alta calidad, perfectos para trabajos de detalle y acabados precisos.",
        "palabras_clave": [
            "accesorios pintura", "materiales acabado", "herramientas personalizacion",
            "kits completos", "insumos decoracion", "productos terminacion",
            "pinturas acrilicas", "pinceles calidad", "sets completos",
            "complementos figuras", "accesorios modelismo", "materiales artistas",
            "productos manualidades", "acabados profesionales", "mejoras esteticas",
            "decoracion piezas", "personalizacion opcional", "mejoras visuales",
            "detallado figuras", "accesorios creativos"
        ]
    },
    "Que pasa si mi modelo tiene errores": {
        "respuesta": "Si tu modelo presenta errores o no es imprimible, nuestro equipo especializado realizará una revisión detallada y te notificaremos sobre los ajustes necesarios. Estamos aquí para ayudarte en todo el proceso: podemos asesorarte para corregir el modelo y asegurarnos de que sea perfectamente funcional para la impresión. Si prefieres, también podemos diseñar un modelo alternativo que cumpla con tus expectativas y requisitos.",
        "palabras_clave": [
            "correccion modelos", "revision archivos", "validacion impresion",
            "deteccion errores", "solucion problemas", "ajustes necesarios",
            "reparacion modelos", "optimizacion archivos", "asesoria tecnica",
            "diseño alternativo", "modificacion piezas", "adaptacion modelos",
            "mejoras diseño", "preparacion impresion", "validacion tecnica",
            "comprobacion viabilidad", "analisis modelos", "diagnostico archivos",
            "soluciones impresion", "alternativas diseño"
        ]
    },
    "Tamaño maximo de impresion": {
        "respuesta": "El modelo impreso puede alcanzar un tamaño máximo de 12.7 x 8 x 16 cm, lo que garantiza un equilibrio entre detalle, estabilidad y compatibilidad con el proceso de impresión.",
        "palabras_clave": [
            "dimensiones maximas", "limites impresion", "capacidad maquina",
            "restricciones tamaño", "volumen maximo", "medidas maximas",
            "escala maxima", "tamaño permitido", "capacidad produccion",
            "limite dimensional", "especificaciones tecnicas", "parametros impresion",
            "alcance impresora", "restricciones fisicas", "volumen construccion",
            "area impresion", "zona trabajo", "capacidad fabricacion",
            "limites maquina", "escala produccion"
        ]
    },
    "cómo puedo hacer un pedido": {
        "respuesta": "Para hacer un pedido, solo necesitas contactarnos por mensaje directo o a través de nuestro correo. Cuéntanos qué figura deseas, si tienes un modelo o necesitas uno personalizado, y nosotros te guiaremos paso a paso. También estamos trabajando en una tienda en línea para que puedas hacerlo todo desde la web.",
        "palabras_clave": [
            "proceso compra", "pasos pedido", "solicitar producto",
            "realizar encargo", "iniciar proyecto", "contratar servicios",
            "adquisicion productos", "compra figuras", "encargo piezas",
            "solicitud impresion", "orden trabajo", "registro pedido",
            "formalizacion compra", "procedimiento compra", "flujo pedido",
            "canales venta", "metodos compra", "opciones adquisicion",
            "iniciar transaccion", "comenzar proyecto"
        ]
    },
    "puedo pedir una figura pintada": {
        "respuesta": "Sí, ofrecemos la opción de figuras pintadas bajo pedido especial. Puedes elegir entre pintura completa o detalles personalizados. También puedes optar por recibir tu figura sin pintar junto a un kit de pintura para personalizarla tú mismo.",
        "palabras_clave": [
            "acabado pintado", "terminado profesional", "pintura especializada",
            "decoracion completa", "coloracion piezas", "personalizacion color",
            "pintura artistica", "acabados premium", "detallado manual",
            "decoracion opcional", "mejoras esteticas", "pintura a mano",
            "terminados especiales", "servicio adicional", "opciones decoracion",
            "variantes presentacion", "alternativas acabado", "estilos pintura",
            "técnicas coloracion", "personalizacion visual"
        ]
    },
    "cómo cuidar mi figura impresa": {
        "respuesta": "Para conservar tu figura impresa en buen estado, evita la exposición directa al sol y al calor extremo. Límpiala con un paño seco y guárdala en un lugar fresco. Si está pintada, evita productos de limpieza con químicos.",
        "palabras_clave": [
            "mantenimiento piezas", "conservacion figuras", "durabilidad productos",
            "cuidados resina", "preservacion impresos", "proteccion figuras",
            "limpieza segura", "almacenamiento correcto", "vida util",
            "recomendaciones uso", "instrucciones cuidado", "precauciones manejo",
            "tratamiento piezas", "proteccion ambiental", "evitar deterioro",
            "alargar vida", "conservar calidad", "prevencion daños",
            "manejo adecuado", "optimizacion durabilidad"
        ]
    },
    "aceptan pagos con tarjeta o transferencia": {
        "respuesta": "Aceptamos pagos por transferencia bancaria, depósito y pagos con tarjeta vía plataformas como Mercado Pago. Escríbenos para darte los datos exactos según el método que prefieras.",
        "palabras_clave": [
            "metodos pago", "opciones pago", "formas transaccion",
            "sistemas cobro", "plataformas pago", "transferencias bancarias",
            "pago electronico", "datos deposito", "informacion pago",
            "requisitos pago", "proceso pago", "confirmacion pago",
            "seguridad transacciones", "comprobante pago", "facturacion electronica",
            "datos facturacion", "pago seguro", "proteccion datos",
            "confidencialidad pago", "alternativas pago"
        ]
    },
    "puedo pedir una figura de un videojuego o anime": {
        "respuesta": "¡Claro! Podemos imprimir figuras basadas en videojuegos, anime o personajes personalizados. Solo asegúrate de que el diseño que nos compartas no infrinja derechos si es para uso comercial.",
        "palabras_clave": [
            "personajes licencia", "figuras populares", "diseños comerciales",
            "marcas registradas", "propiedad intelectual", "derechos autor",
            "franquicias conocidas", "series famosas", "peliculas reconocidas",
            "videojuegos populares", "anime manga", "cultura pop",
            "referencias culturales", "iconos populares", "personajes ficcion",
            "creaciones famosas", "obras conocidas", "licencias oficiales",
            "permisos necesarios", "autorizaciones uso"
        ]
    },
    "pueden hacer prototipos o piezas funcionales": {
        "respuesta": "Sí, realizamos prototipos personalizados y piezas funcionales en resina con gran precisión. Ideal para pruebas, diseño de productos o ingeniería. Cuéntanos qué necesitas y lo evaluamos juntos.",
        "palabras_clave": [
            "aplicaciones industriales", "usos tecnicos", "piezas mecanicas",
            "componentes funcionales", "partes operativas", "prototipado rapido",
            "pruebas concepto", "validacion diseño", "ingenieria inversa",
            "maquetas funcionales", "modelos prueba", "piezas reemplazo",
            "componentes maquinas", "partes ensamblaje", "soluciones industriales",
            "aplicaciones practicas", "usos profesionales", "ingenieria aplicada",
            "desarrollo producto", "innovacion industrial"
        ]
    },
    "tienen tienda física o solo en línea": {
        "respuesta": "Por el momento trabajamos bajo pedido y atendemos en línea. No contamos con una tienda fisica, pero puedes contactarnos para entregas locales en León, Guanajuato.",
        "palabras_clave": [
            "punto venta", "establecimiento fisico", "visita taller",
            "atencion presencial", "consultorio diseño", "oficinas empresa",
            "ubicacion fisica", "direccion legal", "sede central",
            "taller produccion", "fabrica visita", "showroom productos",
            "exposicion piezas", "muestrario fisico", "almacen central",
            "logistica distribucion", "centro operaciones", "instalaciones empresa",
            "infraestructura fisica", "espacios trabajo"
        ]
    },
    "cómo puedo rastrear mi pedido": {
        "respuesta": "Una vez que tu pedido haya sido enviado, te enviaremos un número de rastreo por correo o mensaje. Así podrás monitorear su progreso hasta que llegue a tus manos.",
        "palabras_clave": [
            "seguimiento envio", "localizacion paquete", "estado entrega",
            "guia transporte", "codigo seguimiento", "informacion envio",
            "logistica entrega", "distribucion pedido", "ubicacion actual",
            "tiempo transito", "proceso envio", "compania transporte",
            "datos mensajeria", "confirmacion recepcion", "notificacion entrega",
            "alerta llegada", "monitoreo paquete", "historial envio",
            "detalles logisticos", "informacion reparto"
        ]
    },
    "puedo agendar una cita para asesoría": {
        "respuesta": "Sí, puedes agendar una asesoría personalizada por llamada o mensaje. Te orientamos en diseño, impresión y acabados. Contáctanos y coordinamos una fecha.",
        "palabras_clave": [
            "consultoria diseño", "asesoramiento tecnico", "reunion informativa",
            "soporte especializado", "orientacion profesional", "consultas tecnicas",
            "evaluacion proyecto", "analisis viabilidad", "planeacion impresion",
            "discusion diseño", "sesion informacion", "conversacion inicial",
            "diagnostico proyecto", "evaluacion necesidades", "propuesta solucion",
            "recomendaciones expertas", "guia profesional", "apoyo tecnico",
            "acompañamiento proyecto", "tutoría impresion"
        ]
    },
    "como empiezo si no tengo modelo 3d": {
        "respuesta": "¡No te preocupes! Si no tienes un modelo 3D, nuestro equipo puede ayudarte a diseñarlo desde cero. Solo cuéntanos tu idea, referencias o bocetos y nosotros nos encargamos del resto.",
        "palabras_clave": [
            "creacion diseño", "desarrollo modelo", "idea inicial",
            "concepto basico", "bocetos diseño", "referencias visuales",
            "inspiracion diseño", "material referencia", "partir cero",
            "sin archivo", "sin modelo", "diseño completo",
            "creacion completa", "desarrollo completo", "proceso diseño",
            "transformacion idea", "materializacion concepto", "conceptualizacion",
            "diseño profesional", "creacion personalizada"
        ]
    },
    "pueden escalar una figura a un tamaño especifico": {
        "respuesta": "Sí, podemos ajustar el tamaño de tu figura a las dimensiones que necesites, siempre que sea físicamente posible dentro de los límites de impresión. Solo dinos las medidas deseadas.",
        "palabras_clave": [
            "ajuste dimensiones", "modificacion tamaño", "escala personalizada",
            "redimensionamiento", "adaptacion medidas", "cambio proporciones",
            "especificaciones tamaño", "requerimientos dimensionales", "necesidades tamaño",
            "personalizacion escala", "variacion dimensiones", "alteracion tamaño",
            "reescalado modelo", "optimizacion tamaño", "proporciones exactas",
            "medidas exactas", "precision dimensional", "ajuste exacto",
            "calibracion tamaño", "especificacion medidas"
        ]
    },
    "cuanto cuesta una figura personalizada": {
        "respuesta": "El costo depende del tamaño, nivel de detalle y si ya tienes el archivo 3D o necesitas que lo diseñemos. Escríbenos con tu idea y te damos una cotización sin compromiso.",
        "palabras_clave": [
            "presupuesto proyecto", "estimacion costo", "calculadora precios",
            "tarifas impresion", "precios personalizados", "cotizacion exacta",
            "coste aproximado", "valor estimado", "facturacion proyecto",
            "inversion necesaria", "rango precios", "escala costos",
            "variables precio", "factores costo", "determinacion precio",
            "analisis costos", "evaluacion presupuesto", "presupuestacion",
            "simulador costos", "estimador precios"
        ]
    },
    "puedo combinar partes de varias figuras en una sola": {
        "respuesta": "Sí, podemos combinar diferentes elementos de varias figuras para crear una nueva pieza personalizada. Solo asegúrate de tener derechos o permisos sobre los archivos si no son propios.",
        "palabras_clave": [
            "fusion diseños", "mezcla elementos", "combinacion piezas",
            "ensamblaje modelos", "unión componentes", "creacion hibrida",
            "diseño compuesto", "modelo mixto", "integracion partes",
            "sintesis diseño", "composicion personalizada", "montaje custom",
            "estructura combinada", "figura fusionada", "mezcla creativa",
            "diseño ensamblado", "modelo integrado", "pieza mixta",
            "creacion unica", "diseño exclusivo"
        ]
    },
    "pueden imprimir en otros materiales ademas de resina": {
        "respuesta": "Actualmente trabajamos principalmente con resina por su detalle y calidad, pero estamos explorando la integración de filamento PLA y otros materiales para el futuro cercano.",
        "palabras_clave": [
            "alternativas materiales", "futuros materiales", "evolucion tecnologica",
            "nuevos materiales", "opciones futuras", "desarrollo materiales",
            "innovacion resinas", "mejoras materiales", "sustitutos resina",
            "comparativa materiales", "ventajas desventajas", "tecnicas avanzadas",
            "tecnologia materiales", "propuestas futuras", "cambios materiales",
            "adaptacion materiales", "experimentacion materiales", "pruebas materiales",
            "evaluacion alternativas", "estudio materiales"
        ]
    },
    "ofrecen servicio de modelado 3d": {
        "respuesta": "Sí, contamos con servicio de modelado 3D desde cero. Solo dinos tu idea, referencias o bocetos y te enviaremos una propuesta de diseño personalizada.",
        "palabras_clave": [
            "creacion digital", "diseño asistido", "modelado computarizado",
            "desarrollo virtual", "prototipado digital", "ingenieria diseño",
            "elaboracion modelos", "construccion digital", "generacion 3d",
            "produccion digital", "creacion asistida", "diseño computacional",
            "modelado profesional", "servicio completo", "solucion integral",
            "paquete completo", "diseño total", "proceso completo",
            "desarrollo total", "creacion profesional"
        ]
    },
    "que tipo de archivos aceptan para impresion": {
        "respuesta": "Los formatos que aceptamos son principalmente STL y OBJ. Si tienes otro tipo de archivo, puedes consultarnos para ver si es compatible.",
        "palabras_clave": [
            "formatos soportados", "extensiones aceptadas", "archivos validos",
            "ficheros compatibles", "tipos archivo", "especificaciones formato",
            "requisitos archivo", "preparacion archivos", "conversion formatos",
            "exportacion correcta", "configuracion archivos", "parametros archivo",
            "optimizacion archivos", "validacion formatos", "comprobacion archivos",
            "verificacion compatibilidad", "analisis archivos", "revision formatos",
            "adecuacion archivos", "preprocesamiento archivos"
        ]
    },
    "puedo ver avances de mi pedido": {
        "respuesta": "Sí, durante el proceso te enviaremos avances del diseño o fotos del modelo antes de imprimir. Queremos que estés completamente satisfecho antes de finalizar.",
        "palabras_clave": [
            "seguimiento proceso", "actualizaciones estado", "fotos progreso",
            "imagenes avance", "control calidad", "verificacion diseño",
            "aprobacion cliente", "feedback proceso", "revisiones intermedias",
            "confirmaciones paso", "validaciones parciales", "monitoreo produccion",
            "supervision proceso", "acompañamiento fabricacion", "comunicacion constante",
            "transparencia proceso", "participacion cliente", "interaccion continua",
            "colaboracion activa", "retroalimentacion constante"
        ]
    },
    "pueden hacer llaveros personalizados": {
        "respuesta": "¡Claro! Podemos crear llaveros personalizados en 3D con nombres, logotipos o personajes. Son una excelente opción para regalos o eventos.",
        "palabras_clave": [
            "souvenirs personalizados", "recuerdos eventos", "regalos corporativos",
            "detalles promocionales", "objetos publicitarios", "merchandising personalizado",
            "articulos promocionales", "productos marca", "regalos originales",
            "detalles unicos", "objetos conmemorativos", "souvenirs creativos",
            "regalos empresariales", "articulos personalizables", "productos exclusivos",
            "objetos identificativos", "accesorios identificacion", "elementos distintivos",
            "articulos con logo", "productos branding"
        ]
    },
    "que colores de resina manejan": {
        "respuesta": "Trabajamos principalmente con resina azul para usarlo como base, pero también podemos imprimir en resina blanca bajo pedido especial. En general, el color base no afecta la calidad del modelo, ya que muchos clientes los pintan después.",
        "palabras_clave": [
            "gama colores", "opciones coloracion", "variantes resina",
            "disponibilidad colores", "paleta colores", "escala cromatica",
            "alternativas color", "personalizacion color", "seleccion color",
            "preferencias color", "efectos visuales", "apariencia final",
            "terminado color", "aspecto visual", "caracteristicas esteticas",
            "opacidad resina", "transparencia resina", "brillo resina",
            "textura resina", "efectos especiales"
        ]
    },
    "quien eres tu": {
        "respuesta": "Soy Kidik, un asistente virtual que resolverá tus dudas acerca de la impresión 3D en nuestra empresa.",
        "palabras_clave": [
            "identidad asistente", "funcion bot", "rol chatbot",
            "presentacion virtual", "descripcion asistente", "caracteristicas bot",
            "capacidades asistente", "ayuda virtual", "soporte digital",
            "interfaz conversacional", "agente virtual", "asistente inteligente",
            "chatbot empresa", "soporte automatizado", "ayuda automatizada",
            "asistencia digital", "interaccion programada", "conversacion automatizada",
            "respuestas automaticas", "sistema dialogos"
        ]
    },
    "que haces": {
        "respuesta": "Respondo las dudas que tengas acerca de tus pedidos o sobre la impresión 3D en nuestra empresa.",
        "palabras_clave": [
            "funcionalidades bot", "utilidad asistente", "beneficio chatbot",
            "valor agregado", "servicio chatbot", "ventajas asistente",
            "proposito bot", "objetivo asistente", "mision chatbot",
            "ayuda proporcionada", "soporte ofrecido", "asistencia brindada",
            "soluciones dadas", "respuestas proporcionadas", "informacion brindada",
            "datos ofrecidos", "conocimiento compartido", "orientacion dada",
            "guia proporcionada", "apoyo brindado"
        ]
    },
    "con que estas creado": {
        "respuesta": "Soy un chatbot creado con HTML conectado a una API en Python para responder a tus consultas.",
        "palabras_clave": [
            "tecnologia base", "infraestructura tecnica", "plataforma desarrollo",
            "arquitectura sistema", "desarrollo software", "programacion chatbot",
            "codigo fuente", "lenguajes programacion", "frameworks utilizados",
            "herramientas desarrollo", "tecnologias implementadas", "sistemas utilizados",
            "plataforma operativa", "entorno desarrollo", "stack tecnologico",
            "componentes tecnicos", "implementacion tecnica", "detalles implementacion",
            "especificaciones tecnicas", "caracteristicas sistema"
        ]
    },
    "mi figura se daño en camino": {
        "respuesta": (
            "Lamentamos los inconvenientes. Por favor contáctanos con tu número de pedido y fotos del daño. "
            "Si cumple con los requisitos de garantía, nos encargaremos de reponer la pieza sin costo adicional."
        ),
        "palabras_clave": [
            "reclamo garantia", "problema transporte", "daño transito",
            "incidencia logistica", "averia envio", "problema mensajeria",
            "fallo entrega", "reposicion producto", "solicitud garantia",
            "reembolso posible", "devolucion producto", "cambio producto",
            "soporte postventa", "asistencia garantia", "solucion problema",
            "resolucion incidencia", "proceso garantia", "politica devoluciones",
            "procedimiento reclamacion", "atencion postventa"
        ]
    },
    "cuentas chistes": {
        "respuesta": [
            "¿Por qué el filamento nunca discute con la impresora? Porque siempre siguen la misma línea.",
            "¿Qué le dijo la impresora 3D al diseñador? ¡Deja de darme curvas tan difíciles!",
            "Mi impresora 3D es muy buena contando chistes... siempre imprime sonrisas.",
            "¿Qué hace una figura 3D cuando se aburre? Se queda en stand-by.",
            "La impresora 3D fue a terapia... tenía demasiados problemas en capas."
        ],
        "palabras_clave": [
            "humor impresion", "bromas 3d", "chistes tecnologia",
            "diversion digital", "entretenimiento chatbot", "interaccion divertida",
            "momento alegre", "risas garantizadas", "humor tecnico",
            "chistes nerds", "bromas geek", "diversion geek",
            "entretenimiento tecnico", "alegria digital", "interaccion amena",
            "conversacion divertida", "dialogo alegre", "ambiente distendido",
            "tono humoristico", "momento desenfadado"
        ]
    },
    "qué garantías ofrecen": {
        "respuesta": "Ofrecemos garantía de 30 días contra defectos de fabricación. No cubre daños por mal uso o manipulación inadecuada. Para hacer válida la garantía, conserva tu comprobante de compra.",
        "palabras_clave": [
            "politica garantias", "cobertura garantia", "proteccion compra",
            "seguridad producto", "aval calidad", "certificado garantia",
            "proteccion cliente", "respaldo producto", "seguridad postventa",
            "condiciones garantia", "terminos cobertura", "derechos garantia",
            "procedimientos garantia", "validez garantia", "extension cobertura",
            "limitaciones garantia", "exclusiones garantia", "vigencia garantia",
            "documentacion garantia", "requisitos garantia"
        ]
    },
    "hacen envíos internacionales": {
        "respuesta": "Actualmente solo realizamos envíos nacionales dentro de México. Estamos evaluando opciones para ofrecer envíos internacionales en el futuro.",
        "palabras_clave": [
            "envios exterior", "exportaciones", "shipping internacional",
            "entregas globales", "distribucion internacional", "logistica global",
            "envios otros paises", "cobertura mundial", "servicio global",
            "expansion internacional", "envios america", "distribucion mundial",
            "entrega fronteras", "transporte internacional", "aduanas envios",
            "importaciones", "regulaciones internacionales", "tarifas internacionales",
            "costos envios exterior", "tiempos internacionales"
        ]
    },
    "qué resolucion de impresion tienen": {
        "respuesta": "Nuestras impresoras trabajan con una resolución de capa de hasta 25 micras, lo que permite detalles extremadamente finos y superficies suaves en tus piezas.",
        "palabras_clave": [
            "precision impresion", "calidad detalle", "nitidez impresion",
            "micras capa", "definicion impresion", "tecnologia precision",
            "especificaciones tecnicas", "parametros calidad", "nivel detalle",
            "exactitud impresion", "fidelidad reproduccion", "calidad superficial",
            "acabado fino", "tecnologia avanzada", "capacidad resolucion",
            "performance tecnica", "equipo precision", "caracteristicas maquina",
            "especificaciones equipo", "tecnologia impresora"
        ]
    },
    "tienen descuentos por volumen": {
        "respuesta": "Sí, ofrecemos descuentos progresivos para pedidos grandes. El porcentaje varía según la cantidad de piezas y complejidad. Contáctanos con los detalles de tu proyecto para una cotización especial.",
        "palabras_clave": [
            "ofertas cantidad", "precios mayoristas", "descuentos compra",
            "promociones volumen", "venta al por mayor", "tarifas especiales",
            "economias escala", "beneficios volumen", "ahorro cantidad",
            "precios escalonados", "descuentos progresivos", "tarifas preferenciales",
            "condiciones especiales", "promociones empresa", "ofertas corporativas",
            "precios proyecto", "cotizaciones especiales", "ventajas cantidad",
            "incentivos compra", "bonificaciones volumen"
        ]
    },
    "puedo recoger mi pedido en persona": {
        "respuesta": "Sí, ofrecemos la opción de recoger tu pedido en nuestro taller en León, Guanajuato. Coordinaremos una cita para que puedas venir a recogerlo y verificar que todo esté correcto.",
        "palabras_clave": [
            "retiro local", "recogida taller", "entrega personal",
            "servicio pickup", "retiro fisico", "recoger producto",
            "entrega directa", "recogida directa", "sin envio",
            "ahorro envio", "retiro sucursal", "recoger personalmente",
            "visita taller", "entrega manual", "recogida almacen",
            "retiro almacen", "recoger en local", "entrega presencial",
            "recogida fisica", "retiro sin costo"
        ]
    },
    "qué métodos de embalaje utilizan": {
        "respuesta": "Utilizamos embalaje especializado con materiales protectores como espuma personalizada, cajas de doble pared y protectores de esquina. Cada pieza se envía con instrucciones de manejo para garantizar que llegue en perfecto estado.",
        "palabras_clave": [
            "proteccion envio", "materiales embalaje", "empaque seguro",
            "seguridad transporte", "proteccion producto", "envio cuidadoso",
            "packaging especial", "embalaje profesional", "materiales proteccion",
            "cuidado producto", "prevencion daños", "empaquetado seguro",
            "proteccion fisica", "seguridad paquete", "embalaje premium",
            "materiales amortiguacion", "proteccion esquinas", "sistema embalaje",
            "tecnologia packaging", "soluciones embalaje"
        ]
    },
    "ofrecen servicio de pintura profesional": {
        "respuesta": "Sí, ofrecemos servicio de pintura profesional como opción adicional. Nuestros artistas utilizan técnicas de aerografía y pincelado para lograr acabados de alta calidad y realismo en tus figuras.",
        "palabras_clave": [
            "pintura artistica", "acabado premium", "decoracion profesional",
            "pintura detallada", "terminado experto", "coloracion profesional",
            "técnicas avanzadas", "aerografia figuras", "pintura a mano",
            "acabados especiales", "detallado experto", "mejoras esteticas",
            "personalizacion avanzada", "servicio completo", "pintura calidad",
            "arte digital", "transformacion visual", "mejora apariencia",
            "embellecimiento piezas", "realce detalles"
        ]
    },
    "puedo solicitar una muestra física": {
        "respuesta": "Actualmente no ofrecemos muestras físicas debido a los costos de producción, pero podemos compartirte fotos detalladas de trabajos anteriores similares a lo que buscas.",
        "palabras_clave": [
            "muestras producto", "ejemplos fisicos", "demostracion material",
            "pruebas fisicas", "testeo producto", "evaluacion muestra",
            "verificacion calidad", "comprobacion material", "analisis previo",
            "examen producto", "inspeccion muestra", "revision fisica",
            "prueba tangible", "experiencia tactil", "evaluacion manual",
            "verificacion tactil", "confirmacion calidad", "validacion muestra",
            "aprobacion previa", "aceptacion producto"
        ]
    },
    "qué cuidados requiere la resina después de imprimir": {
        "respuesta": "Las piezas en resina requieren curación UV post-impresión para alcanzar su máxima resistencia. Te recomendamos evitar exposición prolongada al sol directo y limpiar con alcohol isopropílico para mantener su calidad.",
        "palabras_clave": [
            "curado resina", "postprocesado", "tratamiento postimpresion",
            "cuidados postproduccion", "mantenimiento resina", "proteccion piezas",
            "durabilidad resina", "conservacion material", "tratamiento superficial",
            "acabado profesional", "proteccion uv", "resistencia quimica",
            "estabilidad dimensional", "preservacion propiedades", "optimizacion durabilidad",
            "mejoras postproduccion", "tratamientos adicionales", "proteccion ambiental",
            "resistencia intemperie", "proteccion exterior"
        ]
    },
    "tienen opciones ecológicas": {
        "respuesta": "Estamos implementando gradualmente resinas biodegradables y procesos más sostenibles. Actualmente ofrecemos opciones con menor impacto ambiental y estamos en constante búsqueda de alternativas ecológicas.",
        "palabras_clave": [
            "resinas ecologicas", "impresion sostenible", "materiales biodegradables",
            "procesos verdes", "manufactura responsable", "sustentabilidad impresion",
            "eco-friendly", "alternativas verdes", "conciencia ambiental",
            "produccion limpia", "tecnologia sostenible", "innovacion ecologica",
            "respeto ambiental", "materiales responsables", "procesos sustentables",
            "manufactura verde", "impresion responsable", "soluciones ecologicas",
            "productos verdes", "compromiso ambiental"
        ]
    },
    "catálogo de modelos disponible": {
        "respuesta": "Contamos con un catálogo predeterminado que incluye una variedad de modelos 3D, como llaveros y figuras, para que puedas elegir fácilmente. Este catálogo está diseñado para ofrecer opciones listas para imprimir, facilitando el proceso si buscas algo rápido y con buen diseño.",
        "palabras_clave": [
            "modelos predefinidos", "opciones prediseñadas", "selección estándar",
            "figuras catálogo", "diseños disponibles", "productos existentes",
            "colección disponible", "gama predeterminada", "modelos base",
            "alternativas preexistentes", "inventario diseños", "existencias modelos",
            "selección básica", "base de datos modelos", "archivo diseños"
        ]
    },
    "figuras personalizadas desde cero": {
        "respuesta": "Sí, hacemos figuras desde cero. Ponte en contacto con nosotros para que podamos hacer una cotización personalizada y revisar juntos los detalles del diseño, así aseguramos que el resultado final sea justo lo que necesitas.",
        "palabras_clave": [
            "creación exclusiva", "diseño original", "desarrollo personalizado",
            "concepción única", "elaboración exclusiva", "idea inicial",
            "proyecto único", "creación total", "personalización absoluta",
            "diseño integral", "desarrollo completo", "creación desde cero"
        ]
    },
    "precio figura pequeña": {
        "respuesta": "El precio de una figura pequeña está aproximadamente en 1.5 pesos mexicanos por gramo. Este costo puede variar según el diseño, el material y el nivel de detalle, pero sirve como una referencia general para que pueda calcular el presupuesto de su impresión.",
        "palabras_clave": [
            "costo miniatura", "valor pequeña", "precio reducido",
            "cotización pequeña", "tarifa ligera", "presupuesto compacto",
            "inversión mínima", "precio gramo", "costo por peso",
            "tarifación gramaje", "valoración peso", "presupuesto liviano"
        ]
    },
    "pedidos urgentes": {
        "respuesta": "No",
        "palabras_clave": [
            "inmediato", "express", "prioritario",
            "rápido", "acelerado", "inmediato",
            "urgente", "pronta entrega", "entrega rápida",
            "servicio express", "tiempo récord", "producción acelerada"
        ]
    },
    "colores disponibles": {
        "respuesta": "Por el momento, nuestra impresión 3D está disponible únicamente en colores gris y blanco. Estos colores básicos nos permiten mantener un control óptimo sobre la calidad y los tiempos de producción, garantizando resultados consistentes y precisos. ",
        "palabras_clave": [
            "gama cromática", "paleta disponible", "opciones color",
            "escala tonal", "variantes color", "disponibilidad tonal",
            "alternativas color", "colores stock", "tonalidades existentes",
            "opciones estéticas", "espectro disponible"
        ]
    },
    "retoques y pintura post-impresión": {
        "respuesta": "Solo si usted lo desea, ofrecemos el servicio de pintado para su figura impresa en 3D. Este proceso se realiza de manera cuidadosa para resaltar los detalles y darle un acabado profesional y personalizado. Tenga en cuenta que este servicio implica un costo adicional, ya que requiere tiempo, materiales y mano de obra especializada para asegurar un resultado de alta calidad. Si está interesado, podemos proporcionarle más información sobre las opciones de colores y estilos disponibles.",
        "palabras_clave": [
            "acabados adicionales", "mejoras estéticas", "detallado postproducción",
            "terminado especial", "pintura final", "embellecimiento",
            "toques finales", "mejoras superficiales", "refinamiento pieza",
            "detallado manual", "acabado premium"
        ]
    },
    "modificación de archivos existentes": {
        "respuesta": "Sí, solo que habrá que hacer una cotización, hablar de los detalles del modelo y el tiempo de entrega.",
        "palabras_clave": [
            "adaptación diseño", "ajuste modelo", "personalización existente",
            "modificación prediseño", "cambios archivo", "alteración diseño",
            "reescalado diseño", "optimización existente", "evolución modelo",
            "transformación diseño", "actualización archivo"
        ]
    },
    "pedidos múltiples": {
        "respuesta": "Sí.",
        "palabras_clave": [
            "producción masiva", "seriado", "réplicas",
            "múltiples unidades", "cantidad", "volumen",
            "serie", "fabricación múltiple", "pedido repetitivo",
            "producción en serie", "fabricación seriada"
        ]
    },
    "resistencia de la resina": {
        "respuesta": "La resina es resistente y ofrece buena durabilidad, especialmente para piezas detalladas y de tamaño pequeño a mediano. Puede tener propiedades como resistencia al impacto, flexibilidad o rigidez, adaptándose a diferentes necesidades",
        "palabras_clave": [
            "durabilidad material", "robustez piezas", "fortaleza estructural",
            "solidez impresión", "tenacidad resina", "performance mecánica",
            "estabilidad material", "fiabilidad estructural", "consistencia física",
            "calidad estructural", "rendimiento físico"
        ]
    },
    "llaveros y accesorios pequeños": {
        "respuesta": "Sí, porque con resina se pueden crear detalles muy diminutos y precisos, lo que permite lograr acabados finos y diseños complejos que serían difíciles de conseguir con otros materiales.",
        "palabras_clave": [
            "miniaturas", "accesorios detalle", "productos diminutos",
            "objetos pequeños", "detalles precisos", "elementos miniatura",
            "artículos pequeños", "piezas micro", "accesorios precisos",
            "detallado fino", "objetos precisos"
        ]
    },
    "diseños descargados de internet": {
        "respuesta": "Sí, aceptamos modelos descargados de internet siempre y cuando cumplan con nuestras normas de calidad, diseño y derechos de autor. De esta manera, garantizamos que las piezas impresas sean seguras, funcionales y respeten las regulaciones establecidas para nuestro servicio.",
        "palabras_clave": [
            "archivos online", "modelos web", "descargas digitales",
            "diseños externos", "archivos terceros", "contenido descargado",
            "modelos online", "diseños web", "archivos digitales",
            "contenido externo", "archivos foráneos"
        ]
    },
    "piezas móviles o articuladas": {
        "respuesta": "Sí, se pueden fabricar piezas articuladas o movibles mediante impresión 3D. Esto se logra diseñando las partes con las tolerancias adecuadas para que encajen y se muevan entre sí sin necesidad de ensamblaje adicional. Así, las piezas pueden tener funciones mecánicas integradas directamente desde la impresión, lo que permite crear objetos complejos con partes móviles listas para usar.",
        "palabras_clave": [
            "mecanismos", "partes móviles", "ensamblajes",
            "articulaciones", "componentes móviles", "sistemas articulados",
            "mecanismos impresos", "partes funcionales", "movimiento pieza",
            "funcionalidad mecánica", "ingeniería impresa"
        ]
    },
    "origen del nombre Chanco3D": {
        "respuesta": "La empresa Chanco 3D surge como una iniciativa innovadora impulsada por la necesidad creciente de soluciones de fabricación digital en la región...",
        "palabras_clave": [
            "significado nombre", "etimología marca", "origen denominación",
            "historia marca", "razón nombre", "procedencia denominación",
            "inspiración nombre", "fundamento marca", "concepto identidad",
            "nacimiento marca", "esencia nombre"
        ]
    },
    "colores mezclados": {
        "respuesta": "Podemos hacer piezas 3D huecas con un color sólido de base en la impresión, para que pesen menos usando menos material sin perder resistencia. Esto ayuda a reducir costos y hace que las piezas sean más fáciles de manejar y transportar, manteniendo un acabado uniforme y atractivo.",
        "palabras_clave": [
            "policromía", "multicolor", "mezcla tonal",
            "degradados", "variación cromática", "combinación colores",
            "efectos color", "variedad tonal", "paleta múltiple",
            "arcoiris", "cromatismo"
        ]
    },
    "pagos en línea": {
        "respuesta": "De momento solo aceptamos transferencia, pero estamos trabajando en introducir más métodos de pago.",
        "palabras_clave": [
            "pago digital", "transacción online", "pago electrónico",
            "comercio electrónico", "pago web", "transacción digital",
            "pago automatizado", "pago instantáneo", "transferencia digital",
            "pago plataforma", "transacción electrónica"
        ]
    },
    "peso piezas de resina": {
        "respuesta": "Entre 10 a 50 gramos por pieza de un tamaño pequeño.",
        "palabras_clave": [
            "masa piezas", "gramaje resina", "peso estándar",
            "medida peso", "carga pieza", "peso promedio",
            "gramaje estándar", "peso típico", "masa estándar",
            "rango peso", "característica peso"
        ]
    },
    "piezas huecas": {
        "respuesta": "Podemos hacer piezas 3D huecas para que pesen menos, usando menos material sin perder resistencia. Esto ayuda a reducir costos y hace que las piezas sean más fáciles de manejar y transportar. Además, al ser más livianas, pueden ser más prácticas para diferentes usos donde el peso es importante.",
        "palabras_clave": [
            "estructura vacía", "ahorro material", "aligeramiento",
            "reducción peso", "cavidad interna", "núcleo hueco",
            "optimización material", "interior vacío", "diseño ligero",
            "estructura liviana", "peso reducido"
        ]
    },
    "Que significa kidik": {
    "respuesta": "Kidik representa un asistente virtual diseñado para ser ágil, accesible y amigable, que facilita la interacción y ayuda a resolver dudas de manera rápida y sencilla. Su nombre evoca dinamismo y cercanía, reflejando un apoyo confiable y siempre disponible para acompañarte en tus consultas diarias.",
    "palabras_clave": [
        "significado kidik", "etimología kidik", "origen nombre kidik",
        "concepto kidik", "definición kidik", "kidik que significa",
        "explicación kidik", "kidik significado", "porque kidik",
        "kidik representación", "esencia kidik", "fundamento kidik",
        "kidik nombre", "kidik denominación", "kidik identidad",
        "kidik propósito", "kidik filosofía", "kidik esencia",
        "kidik concepto", "kidik razón ser"
    ]
},
    "Cerebreate": {
    "respuesta": [
        "¡Activando el protocolo Cerebrón™! 🧠 No garantizo respuestas lógicas, pero sí contundentes… y con gran presencia.",
    ],
    "palabras_clave": ["cerebreate"]
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