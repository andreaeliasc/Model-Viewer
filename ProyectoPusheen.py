#Andrea Estefania Elias Cobar
#Carnet 17048
#Graficas por Computador
#Basado en el codigo de Dennis Aldana y modificado por Andrea Elias

#Se importan las librerias necesarias para el proyecto
import pygame
import numpy
import glm
import pyassimp
import time
import math
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import glRotatef

#Se inicia el Pygame
pygame.init()
#Se crea la patalla en donde se hara el display
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
#Se crea una variable control del tiempo de renderizado
clock = pygame.time.Clock()

#Se realzan los shaders de los vertices
vertex_shader = """
//Se establece la version del codigo
#version 460

//Se crean las variables de posicion, normales y coordenadas de textura del shader
layout (location = 0) in vec4 position;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

//Se reserva el espacio de las matrices
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

//Se definen los vectores de color y luz
uniform vec4 color;
uniform vec4 light;

//Se crean los vectores de salida de vertex Color y las coordenadas de textura
out vec4 vertexColor;
out vec2 vertexTexcoords;

void main()
{
    //Se modifica la intensidad de la luz en el shader
    float intensity = dot(normal, normalize(light - position));

    //Se crea una inclinacion en los vertices 
    vec4 inclinacion = vec4(position.x + position.y * 0.1, position.yzw);
    //Se inclinan los vertices y multiplican por el resto de matrices
    gl_Position = projection * view * model * inclinacion;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}

"""


#Se realiza el shader de fragmentacion del color
fragment_shader = """
//Se define la version
#version 460

//Se inicia la variable del color diffuse
layout (location = 0) out vec4 diffuseColor;

//Se crean los vectores de color y las coordenadas de las texturas
in vec4 vertexColor;
in vec2 vertexTexcoords;

//Se crea el objeto 2D de textura
uniform sampler2D tex;

void main()
{
    //Se calcula el difuse color de cada fragmento
    diffuseColor = vertexColor * texture(tex, vertexTexcoords);
}
"""


#Se define el color que tendra el fondo
glClearColor(0.31, 0.82, 0.96, 1.0)
#Se permite el uso del test de profundidad
glEnable(GL_DEPTH_TEST)
#Se permite el uso de texturas en 2D
glEnable(GL_TEXTURE_2D)

#Se compulan los shaders en la variable shader
shader = compileProgram(
    #Se compila el shader de vertices
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    #Se compila el shader de fragmentacion
    compileShader(fragment_shader, GL_FRAGMENT_SHADER),
)
#Se hace uso del shader compilado
glUseProgram(shader)

#Se precargan las texturas a una variable cada una
#Textura 1
#Asignamos las textura de superficie
texture_surface1 = pygame.image.load("./sources/Pusheen.jpg" )
#Guardamos la data de la textura
texture_data1 = pygame.image.tostring(texture_surface1,"RGB",1)
#Se obtiene el ancho de la imagen
width1 = texture_surface1.get_width()
#Se obtiene el alto de la imagen
height1 = texture_surface1.get_height()
#Se toman las texturas
texture1 = glGenTextures(1)

#Textura 2
#Asignamos las textura de superficie
texture_surface2 = pygame.image.load("./sources/mermaid.jpg" )
#Guardamos la data de la textura
texture_data2 = pygame.image.tostring(texture_surface2,"RGB",1)
#Se obtiene el ancho de la imagen
width2 = texture_surface2.get_width()
#Se obtiene el alto de la imagen
height2 = texture_surface2.get_height()
#Se toman las texturas
texture2 = glGenTextures(1)

#Textura 3
#Asignamos las textura de superficie
texture_surface3 = pygame.image.load("./sources/galaxy.jpg" )
#Guardamos la data de la textura
texture_data3 = pygame.image.tostring(texture_surface3,"RGB",1)
#Se obtiene el ancho de la imagen
width3 = texture_surface3.get_width()
#Se obtiene el alto de la imagen
height3 = texture_surface3.get_height()
#Se toman las texturas
texture3 = glGenTextures(1)

#Metodos
#Se lee el modelo


def glize(node, luz, cambio, colorCambio):
    #Se obtiene el nodo (parte del modelo) que es hijo del nodo padre
    model = node.transformation.astype(numpy.float32)

         

    #Se hace un for de los mershs del nodo
    for mesh in node.meshes:
        #Obtenemos el material de dicho mersh del mtl
        #material = dict(mesh.material.properties.items())
        #Obtenemos el nombre del archivo
        #texture = material['file'][2:]

        #Aqui tomamos la texura que viene con el mtl
        if cambio == 1:
            #Asignamos la textura 1 al objeto de texturas en 2D
            glBindTexture(GL_TEXTURE_2D, texture1)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width1, height1, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data1)
            #Se hace el mapeo de textura
            glGenerateMipmap(GL_TEXTURE_2D)

        #Aqui tomamos la textura de rocas azules que asignamos a todo el modelo
        elif cambio == 2:
            #Asignamos la textura 2 al objeto de texturas en 2D
            glBindTexture(GL_TEXTURE_2D, texture2)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width2, height2, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data2)
            #Se hace el mapeo de textura
            glGenerateMipmap(GL_TEXTURE_2D)
            
        #Aqui tomamos la textura de pizza que asignamos a todo el modelo
        elif cambio == 3:
            #Asignamos la textura 3 al objeto de texturas en 2D
            glBindTexture(GL_TEXTURE_2D, texture3)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width3, height3, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data3)
            #Se hace el mapeo de textura
            glGenerateMipmap(GL_TEXTURE_2D)

        #Se toman los datos de los vertices del modelo    
        vertex_data = numpy.hstack((
            numpy.array(mesh.vertices, dtype=numpy.float32),
            numpy.array(mesh.normals, dtype=numpy.float32),
            numpy.array(mesh.texturecoords[0], dtype=numpy.float32)
        ))

        #Se toman los datos de las caras del modelo
        faces = numpy.hstack(
            numpy.array(mesh.faces, dtype=numpy.int32)
        )

        #Se hace un buffer de los vertices a dibujar
        vertex_buffer_object = glGenVertexArrays(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        #Se compilan los vertices a modo de triangulos (3) en 3 glVertexAttrib pointer
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 9 * 4, None)

        glVertexAttribPointer(1, 3, GL_FLOAT, False, 9 * 4, ctypes.c_void_p(3 * 4))

        glVertexAttribPointer(2, 3, GL_FLOAT, False, 9 * 4, ctypes.c_void_p(6 * 4))


        #Se hace un buffer de buffer de elementos del objeto
        element_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)
        
        #Se obtiene la matriz de model
        glUniformMatrix4fv(
            glGetUniformLocation(shader, "model"), 1 , GL_FALSE, 
            model
        )
        #Se obtiene la matriz de view
        glUniformMatrix4fv(
            glGetUniformLocation(shader, "view"), 1 , GL_FALSE, 
            glm.value_ptr(view)
        )
        #Se obtiene la matriz de proyeccion
        glUniformMatrix4fv(
            glGetUniformLocation(shader, "projection"), 1 , GL_FALSE, 
            glm.value_ptr(projection)
        )
        #Se obtienen las propiedades difuse del material
        diffuse = mesh.material.properties["diffuse"]

        #Se obtiene la localizacion del color del shader
        glUniform4f(
            glGetUniformLocation(shader, "color"),
            colorCambio.x,colorCambio.y,colorCambio.z,
            1
        )
        #Se obtienen los valores de la luz para el modelo
        glUniform4f(
            glGetUniformLocation(shader, "light"), 
            luz.w, luz.x, luz.y, luz.z
        )
        #Se dibujan los elementos a forma de triangulos
        glDrawElements(GL_TRIANGLES, len(faces), GL_UNSIGNED_INT, None)

    #Se llaman a los nodos hijos del nodo padre
    for child in node.children:
        glize(child, luz, cambio, colorCambio)

glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glEnableVertexAttribArray(2)

#Se realiza una funcion para que la camara haga Zoom y quitar Zoom a traves de la multiplicacion de matrices
def funcionAdelante(camara, movimiento):
    #Se crea una matriz de ZOOM 3X3
    horizontal = numpy.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, movimiento],
        [0, 0, 0, 1]
        ])
    #Se para la camara a una matriz 3X1
    camaraMatriz = numpy.matrix([
        [camara.x],
        [camara.y],
        [camara.z],
        [1]
        ])
    #Se realiza el calculo de la nueva camara
    camaraAdelantada = numpy.dot(horizontal,camaraMatriz)
    #Se asignan los valores a la camara
    camara.x = float(camaraAdelantada[0])
    camara.y = float(camaraAdelantada[1])
    camara.z = float(camaraAdelantada[2])
    #Se regresa la camara
    return camara

#Se realiza una funcion para que la camara gire alrededor del modelo horizontalmente a traves de la multiplicacion de matrices
def funcionHorizontal(camara, angulo):
    #Se crea una matriz de horizontalidad 3X3
    horizontal = numpy.matrix([
        [math.cos(math.radians(angulo)), 0, math.sin(math.radians(angulo))],
        [0, 1, 0],
        [-1 * math.sin(math.radians(angulo)), 0, math.cos(math.radians(angulo))]
        ])
    #Se para la camara a una matriz 3X1
    camaraMatriz = numpy.matrix([
        [camara.x],
        [camara.y],
        [camara.z]
        ])
    #Se realiza el calculo de la nueva camara
    camaraGirada = numpy.dot(horizontal,camaraMatriz)
    #Se asignan los valores a la camara
    camara.x = float(camaraGirada[0])
    camara.y = float(camaraGirada[1])
    camara.z = float(camaraGirada[2])
    #Se regresa la camara
    return camara

#Se realiza una funcion para que la camara gire alrededor del modelo verticalmente a traves de la multiplicacion de matrices
def funcionVertical(camara, angulo):
    #Se crea una matriz de verticalidad 3X3
    vertical = numpy.matrix([
        [1, 0, 0],
        [0, math.cos(math.radians(angulo)), -1 * math.sin(math.radians(angulo))],
        [0, math.sin(math.radians(angulo)), math.cos(math.radians(angulo))]
        ])
    #Se para la camara a una matriz 3X1
    camaraMatriz = numpy.matrix([
        [camara.x],
        [camara.y],
        [camara.z]
        ])
    #Se realiza el calculo de la nueva camara
    camaraGirada = numpy.dot(vertical,camaraMatriz)
    #Se asignan los valores a la camara
    camara.x = float(camaraGirada[0])
    camara.y = float(camaraGirada[1])
    camara.z = float(camaraGirada[2])
    #Se regresa la camara
    return camara

#Se realiza una funcion para que la camara gire alrededor del modelo horizontalmente a traves de la multiplicacion de matrices
def funcionProfundidad(camara, angulo):
    #Se crea una matriz de profundidad 3X3
    profundidad = numpy.matrix([
        [math.cos(math.radians(angulo)), -1 * math.sin(math.radians(angulo)), 0],
        [math.sin(math.radians(angulo)), math.cos(math.radians(angulo)), 0],
        [0, 0, 1]
        ])
    #Se para la camara a una matriz 3X1
    camaraMatriz = numpy.matrix([
        [camara.x],
        [camara.y],
        [camara.z]
        ])
    #Se realiza el calculo de la nueva camara
    camaraGirada = numpy.dot(profundidad,camaraMatriz)
    #Se asignan los valores a la camara
    camara.x = float(camaraGirada[0])
    camara.y = float(camaraGirada[1])
    camara.z = float(camaraGirada[2])
    #Se regresa la camara
    return camara

#Se crean la matrices
model = glm.mat4(1)
view = glm.mat4(1)
projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000.0)
glViewport(0, 0, 800, 600)

scene = pyassimp.load('./sources/untitled.obj')

#Valores constantes del proyecto
camara = glm.vec3(0, 0, 50)
angulox = 0.0
anguloy = 0.0
anguloz = 0.0
profundidad = 0.0
luz = glm.vec4(-100, 300, 200 , 1)
colorCambio = glm.vec3(0.55, 0.55, 0.55)
cambio = 1

#Menu para mostrar la pantalla con el renderizado en tiempo real
while True:
    #Se limpia con color asignado a Clear el fondo en cada iteracion
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader)
    #Se crea la vista con la camara
    view = glm.lookAt(camara, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
   
    
    glize(scene.rootnode, luz, cambio, colorCambio)
    pygame.display.flip()
    for event in pygame.event.get():
        #Evento para salir cerrando la ventana
        if event.type == pygame.QUIT:
            exit()
        #Evento para salir presionando la tecla ESC
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            exit()
        #Eventos presionando teclas
        if event.type == pygame.KEYDOWN:
            #Evento de girar a la izquierda con tecla IZQUIERDA
            if event.key == pygame.K_LEFT:
                camara = funcionHorizontal(camara, -5)
                pass
            #Evento de girar a la derecha con tecla DERECHA
            if event.key == pygame.K_RIGHT:
                camara = funcionHorizontal(camara, 5)
                pass
            #Evento de girar arriba con la tecla ARRIBA
            if event.key == pygame.K_UP:
                if anguloy > -90:
                    anguloy = anguloy - 10
                    camara = funcionVertical(camara, -10)
                    pass
                else:
                    pass
            #Evento de girar abajo con la tecla ABAJO
            if event.key == pygame.K_DOWN:
                if anguloy < 70:
                    anguloy = anguloy + 10
                    camara = funcionVertical(camara, 10)
                    pass
                else:
                    pass
            #Evento de hacer ZOOM con tecla Z
            if event.key == pygame.K_z:
                if profundidad > -40:
                    profundidad = profundidad - 5
                    camara = funcionAdelante(camara, -5)
                    pass
                else:
                    pass
            #Evento de NO-ZOOM con la tecla X
            if event.key == pygame.K_x:
                if profundidad < 35:
                    profundidad = profundidad + 5
                    camara = funcionAdelante(camara, 5)
                    pass
                else:
                    pass
            #Evento de cambiar de lado la luz en Y con tecla O
            if event.key == pygame.K_o:
                luz.y = -1 * luz.y
                pass
            #Evento de cambiar de lado la luz en X con tecla P3
            if event.key == pygame.K_p:
                luz.x = -1 * luz.x
                pass
            #Evento de llenar poligonos (triangulos) con tecla T
            if event.key == pygame.K_t:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                pass
            #Evento de hacer puntos los poligonos (triangulos) con tecla Y
            if event.key == pygame.K_y:
                glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
                pass
            #Evento de hacer lineas los poligonos (triangulos) con tecla U
            if event.key == pygame.K_u:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                pass
            #Evento para cambiar la textura con tecla Q
            if event.key == pygame.K_q:
                cambio = 1
                pass
            #Evento para cambiar la textura con tecla W
            if event.key == pygame.K_w:
                cambio = 2
                pass
            #Evento para cambiar la textura con tecla E
            if event.key == pygame.K_e:
                cambio = 3
                pass
            #Evento para aumentar/disminuir la intensidad de la luz en Y con tecla K
            if event.key == pygame.K_k:
                if luz.y < 500:
                    luz.y = luz.y + 50
                    pass
                else:
                    pass
            #Evento para disminuir/aumentar la intensidad de la luz en Y con tecla L
            if event.key == pygame.K_l:
                if luz.y > -500:
                    luz.y = luz.y - 50
                    pass
                else:
                    pass
            #Evento para cambiar el fondo con tecla V a amarillo
            if event.key == pygame.K_v:
                glClearColor(0.89, 0.63, 0.06, 1.0)
                pass
            #Evento para cambiar el fondo con tecla B a celeste
            if event.key == pygame.K_b:
                glClearColor(0.31, 0.82, 0.96, 1.0)
                pass
            #Evento para aumentar el tono del canal R
            if event.key == pygame.K_a:
                colorCambio.x = colorCambio.x + 0.05
                pass
            #Evento para disminuir el tono del canal R
            if event.key == pygame.K_s:
                colorCambio.x = colorCambio.x - 0.05
                pass
            #Evento para aumentar el tono del canal G
            if event.key == pygame.K_d:
                colorCambio.y = colorCambio.y + 0.05
                pass
            #Evento para disminuir el tono del canal G
            if event.key == pygame.K_f:
                colorCambio.y = colorCambio.y - 0.05
                pass
            #Evento para aumentar el tono del canal B
            if event.key == pygame.K_g:
                colorCambio.z = colorCambio.z + 0.05
                pass
            #Evento para disminuir el tono del canal B
            if event.key == pygame.K_h:
                colorCambio.z = colorCambio.z - 0.05
                pass
            #Evento para resetear los valores originales de los canalaes del color
            if event.key == pygame.K_r:
                colorCambio.x = 0.55
                colorCambio.y = 0.55
                colorCambio.z = 0.55
                pass 

           

    clock.tick(15)
    

    


    #Se revisa que inputs se han realizado    
   

    #yaw = angulo1

    #Se le da un tiempo de pausa entre renders
    #clock.tick(15)

    #Se muestra el display   

	
    pygame.event.pump() 
