import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Información del autor y asesor
st.title("Simulación de movimientos en SO(2)")
st.markdown("Autor: Vérochka J. Chero Reque")
st.markdown("Asesor: Mg. Oscar Santamaría Santisteban")

# Selección del movimiento
st.sidebar.title("Configuración")
movement = st.sidebar.radio(
    "Selecciona el movimiento:",
    ("Desviación radial", "Desviación cubital", "Flexión", "Extensión")
)

# Cargar imágenes desde el directorio del proyecto
arm_image_radial = Image.open("arm_radial.jpg")
arm_image_flexion = Image.open("arm_flexion.png")
hand_image_radial = Image.open("hand_radial.png")
hand_image_flexion = Image.open("hand_flexion.png")

# Límites de los movimientos (AAOS)
limits = {
    "Desviación radial": (0, 20),
    "Desviación cubital": (0, 30),
    "Flexión": (0, 80),
    "Extensión": (0, 70)
}

# Función para crear matriz de rotación
def rotation_matrix(angle):
    radians = np.radians(angle)
    return np.array([[np.cos(radians), -np.sin(radians)],
                     [np.sin(radians), np.cos(radians)]])

# Función para rotar y superponer imágenes
def rotate_and_plot_images(ax, angle, movement, arm_img_radial, arm_img_flexion, hand_img_radial, hand_img_flexion):
    radians = np.radians(angle)

    # Seleccionar la imagen del antebrazo según el movimiento
    if movement in ["Desviación radial", "Desviación cubital"]:
        arm_img = arm_img_radial
        hand_img = hand_img_radial
        arm_extent = [-0.5, 0.5, -0.8, -0.02]
        rotation_origin = (0, 0)  # Origen de rotación para desviación radial/cubital
    else:
        arm_img = arm_img_flexion
        hand_img = hand_img_flexion
        arm_extent = [-0.8, -0.02, -0.5, 0.5]
        rotation_origin = (0, 0)  # Origen de rotación para flexión/extensión

    # Dibujar el antebrazo
    ax.imshow(arm_img, extent=arm_extent, zorder=2, aspect='auto')

    # Ajustar coordenadas de la mano según la rotación
    hand_width = 0.3
    hand_height = 0.4
    hand_center = np.array([0, 0]) + np.array(rotation_origin)

    # Calcular posición de la mano después de la rotación
    rotation_mat = rotation_matrix(angle)
    hand_corners = np.array([[-hand_width / 2, -hand_height / 2],
                             [hand_width / 2, -hand_height / 2],
                             [hand_width / 2, hand_height / 2],
                             [-hand_width / 2, hand_height / 2]])
    rotated_corners = (rotation_mat @ hand_corners.T).T + hand_center

    # Dibujar la imagen de la mano rotada
    ax.imshow(hand_img.rotate(-angle, resample=Image.BICUBIC), extent=[
        rotated_corners[:, 0].min(), rotated_corners[:, 0].max(),
        rotated_corners[:, 1].min(), rotated_corners[:, 1].max()
    ], zorder=3, aspect='auto')

# Gráfico para movimientos
if movement in limits:
    st.header(f"Movimiento: {movement}")
    st.write(f"Límite (AAOS): {limits[movement][0]}° a {limits[movement][1]}°")

    # Seleccionar el ángulo dentro de los límites
    angle = st.slider(f"Ángulo para {movement}", *limits[movement], value=limits[movement][0])

    # Mostrar matriz de rotación
    rotation_mat = rotation_matrix(angle)
    st.subheader("Matriz de rotación:")
    st.write(rotation_mat)

    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(8, 8))
    rotate_and_plot_images(ax, angle, movement, arm_image_radial, arm_image_flexion, hand_image_radial, hand_image_flexion)

    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel("Y")
    ax.set_ylabel("X")
    ax.grid(True)
    ax.set_aspect('equal')  # Escala uniforme
    ax.set_title(f"Movimiento: {movement} (Ángulo: {angle}°)")

    st.pyplot(fig)
else:
    st.write("Selecciona un movimiento para visualizar.")
