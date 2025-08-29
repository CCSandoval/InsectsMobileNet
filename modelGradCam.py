import tensorflow as tf
import numpy as np
import cv2

def preprocessImage(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (320, 320))
    img = np.expand_dims(img, axis=0)
    return img

def computeGradcam(model, img_path, class_index, conv_layer="conv_1"):
    grad_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=[model.get_layer(conv_layer).output, model.output]
    )

    img_array = preprocessImage(img_path)

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, class_index]  # Loss for target class

    grads = tape.gradient(loss, conv_outputs)  # Compute gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))  # Global average pooling

    conv_outputs = conv_outputs.numpy()[0]
    pooled_grads = pooled_grads.numpy()

    # Multiply feature maps by importance weights
    for i in range(pooled_grads.shape[-1]):
        conv_outputs[:, :, i] *= pooled_grads[i]

    heatmap = np.mean(conv_outputs, axis=-1)  # Compute heatmap
    heatmap = np.maximum(heatmap, 0)  # ReLU activation
    heatmap /= np.max(heatmap)  # Normalize

    return heatmap

def overlayHeatmap(img_path, heatmap, alpha=0.4):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    heatmap = np.uint8(255 * heatmap)  # Convert to 0-255 scale
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)  # Apply color map

    # heatmap = np.expand_dims(heatmap, axis=-1)
    # heatmap = np.concatenate([heatmap, heatmap, heatmap], axis=-1)

    superimposed_img = cv2.addWeighted(img, alpha, heatmap, 1 - alpha, 0)  # Blend images
    return superimposed_img