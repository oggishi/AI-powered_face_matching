"""
Train a Flower Classification Model with Keras Transfer Learning

- Supports datasets in ImageFolder structure: train/valid[/test]/<class>/*.jpg
- Compatible with Oxford 102 Flowers after running dataset_downloader.py
- Uses EfficientNetB0 by default; fallback to MobileNetV2 if unavailable
- Saves model and class map for API inference

Usage examples:
python ml_models/train_flower_model.py --data-dir ./datasets/oxford_flowers102 \
  --img-size 224 --batch-size 32 --epochs 10 --model-out ./ml_models/artifacts/flower_model \
  --class-map-out ./ml_models/artifacts/flower_class_map.json

Author: AI Assistant
Date: 2025-12-23
"""

import os
import json
import math
import argparse
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models

AUTOTUNE = tf.data.AUTOTUNE


def build_datasets(data_dir: str, img_size: int, batch_size: int):
    data_dir = Path(data_dir)
    train_dir = data_dir / 'train'
    valid_dir = data_dir / 'valid'
    test_dir = data_dir / 'test'

    if not train_dir.exists() or not valid_dir.exists():
        raise RuntimeError(
            "Dataset must contain 'train' and 'valid' directories")

    def make_ds(directory):
        return tf.keras.preprocessing.image_dataset_from_directory(
            directory,
            labels='inferred',
            label_mode='int',
            image_size=(img_size, img_size),
            batch_size=batch_size,
            shuffle=True
        )

    train_ds = make_ds(str(train_dir))
    val_ds = make_ds(str(valid_dir))
    test_ds = make_ds(str(test_dir)) if test_dir.exists() else None

    class_names = train_ds.class_names

    # Cache and prefetch for performance
    def configure(ds):
        return ds.cache().prefetch(buffer_size=AUTOTUNE)

    return configure(train_ds), configure(val_ds), configure(test_ds) if test_ds else None, class_names


def build_model(num_classes: int, img_size: int) -> tf.keras.Model:
    input_shape = (img_size, img_size, 3)

    # Try EfficientNetB0 first
    base_model = None
    try:
        base_model = tf.keras.applications.EfficientNetB0(
            include_top=False, weights='imagenet', input_shape=input_shape
        )
        preprocess = tf.keras.applications.efficientnet.preprocess_input
    except Exception:
        base_model = tf.keras.applications.MobileNetV2(
            include_top=False, weights='imagenet', input_shape=input_shape
        )
        preprocess = tf.keras.applications.mobilenet_v2.preprocess_input

    base_model.trainable = False

    inputs = layers.Input(shape=input_shape)
    x = preprocess(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def fine_tune(model: tf.keras.Model, base_trainable_layers: int = 40):
    # Unfreeze top layers of the base model for fine-tuning
    base_model = None
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model):
            base_model = layer
            break
    if base_model is None:
        return model

    base_model.trainable = True
    for layer in base_model.layers[:-base_trainable_layers]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-4),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def save_artifacts(model: tf.keras.Model, class_names, model_out: str, class_map_out: str):
    Path(model_out).parent.mkdir(parents=True, exist_ok=True)
    Path(class_map_out).parent.mkdir(parents=True, exist_ok=True)

    # Save model in TensorFlow SavedModel format for robust loading
    model.save(model_out)

    # Save class map
    with open(class_map_out, 'w', encoding='utf-8') as f:
        # store as list for simplicity
        json.dump(class_names, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str, required=True)
    parser.add_argument('--img-size', type=int, default=224)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--finetune-epochs', type=int, default=5)
    parser.add_argument('--model-out', type=str,
                        default='./ml_models/artifacts/flower_model')
    parser.add_argument('--class-map-out', type=str,
                        default='./ml_models/artifacts/flower_class_map.json')
    args = parser.parse_args()

    train_ds, val_ds, test_ds, class_names = build_datasets(
        args.data_dir, args.img_size, args.batch_size)

    model = build_model(num_classes=len(class_names), img_size=args.img_size)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy', patience=3, restore_best_weights=True)
    ]

    model.fit(train_ds, validation_data=val_ds,
              epochs=args.epochs, callbacks=callbacks)

    # Optional fine-tuning
    model = fine_tune(model)
    model.fit(train_ds, validation_data=val_ds,
              epochs=args.finetune_epochs, callbacks=callbacks)

    # Evaluate
    if test_ds is not None:
        test_loss, test_acc = model.evaluate(test_ds)
        print({"test_loss": float(test_loss), "test_acc": float(test_acc)})

    save_artifacts(model, class_names, args.model_out, args.class_map_out)
    print(f"Saved model to {args.model_out}")
    print(f"Saved class map to {args.class_map_out}")


if __name__ == '__main__':
    main()
