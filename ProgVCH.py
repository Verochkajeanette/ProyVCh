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
        arm_x, arm_y = [0, 0], [-0.8, 0.0]  # Antebrazo en eje Y
        arm_extent = [-0.5, 0.5, -0.8, -0.02]
    else:
        arm_img = arm_img_flexion
        hand_img = hand_img_flexion
        arm_x, arm_y = [-0.8, 0.0], [0, 0]  # Antebrazo en eje X
        arm_extent = [-0.8, -0.02, -0.5, 0.5]

    # Dibujar el antebrazo
    ax.plot(arm_x, arm_y, color='blue', lw=2, label="Antebrazo")
    if arm_img:
        ax.imshow(arm_img, extent=arm_extent, zorder=2, aspect='auto')

    # Coordenadas de la mano rotada según el movimiento
    if movement == "Desviación radial":
        hand_x = -0.5 * np.sin(radians)
        hand_y = 0.5 * np.cos(radians)
    elif movement == "Desviación cubital":
        hand_x = 0.5 * np.sin(radians)
        hand_y = 0.5 * np.cos(radians)
    elif movement == "Flexión":
        hand_x = 0.5 * np.cos(radians)
        hand_y = -0.5 * np.sin(radians)
    elif movement == "Extensión":
        hand_x = 0.5 * np.cos(radians)
        hand_y = 0.5 * np.sin(radians)

    ax.quiver(arm_x[-1], arm_y[-1], hand_x, hand_y, angles='xy', scale_units='xy', scale=1.0, color='red', label="Mano")

    # Rotar y agregar la imagen de la mano
    if hand_img:
        rotation_mat = rotation_matrix(angle)
        hand_center = np.array([hand_x, hand_y])
        hand_extent = np.array([[-0.15, -0.15], [0.15, -0.15], [0.15, 0.15], [-0.15, 0.15]])  # Tamaño aumentado
        rotated_extent = (rotation_mat @ hand_extent.T).T + hand_center

        ax.imshow(hand_img.rotate(-angle, resample=Image.BICUBIC), extent=[
            rotated_extent[:, 0].min(), rotated_extent[:, 0].max(),
            rotated_extent[:, 1].min(), rotated_extent[:, 1].max()
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
    ax.legend()
    ax.set_aspect('equal')  # Escala uniforme
    ax.autoscale_view()  # Ajustar límites automáticamente
    ax.set_title(f"Movimiento: {movement} (Ángulo: {angle}°)")

    st.pyplot(fig)
else:
    st.write("Selecciona un movimiento para visualizar.")

