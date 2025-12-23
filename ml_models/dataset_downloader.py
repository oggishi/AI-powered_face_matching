"""
Dataset Downloader for Flower Recognition
Supports:
1. Oxford 102 Flowers Dataset (102 categories)
2. Flowers Recognition Dataset (5 categories: daisy, dandelion, rose, sunflower, tulip)
3. Custom Kaggle datasets

Author: AI Assistant
Date: 2025-12-22
"""

import tensorflow as tf
import tensorflow_datasets as tfds
from pathlib import Path
import logging
import shutil
import os
from typing import Optional
import requests
from zipfile import ZipFile
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_oxford_flowers(data_dir: str = './datasets') -> Path:
    """
    Download and prepare Oxford 102 Flowers dataset
    
    Args:
        data_dir: Directory to save dataset
    
    Returns:
        Path to dataset directory
    """
    logger.info("Downloading Oxford 102 Flowers dataset...")
    
    data_dir = Path(data_dir)
    oxford_dir = data_dir / 'oxford_flowers102'
    
    if oxford_dir.exists() and len(list(oxford_dir.glob('*'))) > 0:
        logger.info(f"Dataset already exists at {oxford_dir}")
        return oxford_dir
    
    # Download using tensorflow_datasets
    try:
        # Download dataset
        (train_ds, val_ds, test_ds), info = tfds.load(
            'oxford_flowers102',
            split=['train', 'validation', 'test'],
            with_info=True,
            as_supervised=True,
            download=True,
            data_dir=str(data_dir / 'tfds')
        )
        
        # Create directory structure
        train_dir = oxford_dir / 'train'
        valid_dir = oxford_dir / 'valid'
        test_dir = oxford_dir / 'test'
        
        for d in [train_dir, valid_dir, test_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Save images to directories
        logger.info("Saving training images...")
        save_dataset_to_directory(train_ds, train_dir, info.features['label'].num_classes)
        
        logger.info("Saving validation images...")
        save_dataset_to_directory(val_ds, valid_dir, info.features['label'].num_classes)
        
        logger.info("Saving test images...")
        save_dataset_to_directory(test_ds, test_dir, info.features['label'].num_classes)
        
        logger.info(f"Oxford 102 Flowers dataset downloaded to {oxford_dir}")
        logger.info(f"Classes: {info.features['label'].num_classes}")
        
        return oxford_dir
        
    except Exception as e:
        logger.error(f"Error downloading Oxford Flowers: {e}")
        logger.info("Please manually download from:")
        logger.info("https://www.robots.ox.ac.uk/~vgg/data/flowers/102/")
        raise


def save_dataset_to_directory(dataset, output_dir: Path, num_classes: int):
    """
    Save TensorFlow dataset to directory structure
    
    Args:
        dataset: TensorFlow dataset
        output_dir: Output directory
        num_classes: Number of classes
    """
    # Create class directories
    for i in range(num_classes):
        class_dir = output_dir / str(i)
        class_dir.mkdir(parents=True, exist_ok=True)
    
    # Counter for each class
    class_counters = {i: 0 for i in range(num_classes)}
    
    # Save images
    for image, label in tqdm(dataset, desc=f"Saving to {output_dir.name}"):
        label = int(label.numpy())
        class_dir = output_dir / str(label)
        
        # Save image
        image_path = class_dir / f"{class_counters[label]:05d}.jpg"
        
        # Convert to PIL and save
        image_np = image.numpy()
        tf.keras.preprocessing.image.save_img(str(image_path), image_np)
        
        class_counters[label] += 1


def download_flowers_recognition(data_dir: str = './datasets') -> Path:
    """
    Download Flowers Recognition Dataset (5 classes)
    Dataset: https://www.kaggle.com/datasets/alxmamaev/flowers-recognition
    
    Args:
        data_dir: Directory to save dataset
    
    Returns:
        Path to dataset directory
    """
    logger.info("Downloading Flowers Recognition dataset...")
    
    data_dir = Path(data_dir)
    flowers_dir = data_dir / 'flowers_recognition'
    
    if flowers_dir.exists() and len(list(flowers_dir.glob('*'))) > 0:
        logger.info(f"Dataset already exists at {flowers_dir}")
        return flowers_dir
    
    # This dataset needs to be downloaded from Kaggle
    logger.info("="*60)
    logger.info("MANUAL DOWNLOAD REQUIRED")
    logger.info("="*60)
    logger.info("Please download the Flowers Recognition dataset from:")
    logger.info("https://www.kaggle.com/datasets/alxmamaev/flowers-recognition")
    logger.info("")
    logger.info("Steps:")
    logger.info("1. Download the dataset ZIP file")
    logger.info("2. Extract it to: " + str(flowers_dir))
    logger.info("3. Organize into train/valid folders")
    logger.info("="*60)
    
    # Note: To automate this, users need Kaggle API credentials
    logger.info("\nAlternatively, install kaggle CLI:")
    logger.info("pip install kaggle")
    logger.info("Then run:")
    logger.info(f"kaggle datasets download -d alxmamaev/flowers-recognition -p {data_dir}")
    
    return flowers_dir


def download_from_url(url: str, output_path: Path, extract: bool = True):
    """
    Download file from URL with progress bar
    
    Args:
        url: URL to download from
        output_path: Path to save file
        extract: Whether to extract ZIP files
    """
    logger.info(f"Downloading from {url}...")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download with progress bar
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    
    logger.info(f"Downloaded to {output_path}")
    
    # Extract if ZIP
    if extract and output_path.suffix == '.zip':
        logger.info("Extracting ZIP file...")
        with ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(output_path.parent)
        logger.info("Extraction complete")


def prepare_custom_dataset(
    source_dir: str,
    output_dir: str,
    train_split: float = 0.8,
    val_split: float = 0.1
):
    """
    Prepare custom dataset by splitting into train/val/test
    
    Args:
        source_dir: Source directory with class folders
        output_dir: Output directory
        train_split: Training data ratio
        val_split: Validation data ratio
    """
    import random
    from shutil import copy2
    
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    
    logger.info(f"Preparing dataset from {source_dir}...")
    
    # Create output directories
    train_dir = output_dir / 'train'
    val_dir = output_dir / 'valid'
    test_dir = output_dir / 'test'
    
    for d in [train_dir, val_dir, test_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Get class directories
    class_dirs = [d for d in source_dir.iterdir() if d.is_dir()]
    
    logger.info(f"Found {len(class_dirs)} classes")
    
    for class_dir in class_dirs:
        class_name = class_dir.name
        logger.info(f"Processing class: {class_name}")
        
        # Get all images
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            images.extend(list(class_dir.glob(ext)))
        
        # Shuffle
        random.shuffle(images)
        
        # Split
        n_total = len(images)
        n_train = int(n_total * train_split)
        n_val = int(n_total * val_split)
        
        train_images = images[:n_train]
        val_images = images[n_train:n_train + n_val]
        test_images = images[n_train + n_val:]
        
        # Create class directories
        (train_dir / class_name).mkdir(exist_ok=True)
        (val_dir / class_name).mkdir(exist_ok=True)
        (test_dir / class_name).mkdir(exist_ok=True)
        
        # Copy files
        for img in train_images:
            copy2(img, train_dir / class_name / img.name)
        
        for img in val_images:
            copy2(img, val_dir / class_name / img.name)
        
        for img in test_images:
            copy2(img, test_dir / class_name / img.name)
        
        logger.info(f"  Train: {len(train_images)}, Val: {len(val_images)}, Test: {len(test_images)}")
    
    logger.info(f"Dataset prepared at {output_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Download flower datasets')
    parser.add_argument('--dataset', type=str, required=True,
                      choices=['oxford', 'flowers_recognition', 'custom'],
                      help='Dataset to download')
    parser.add_argument('--data-dir', type=str, default='./datasets',
                      help='Directory to save dataset')
    parser.add_argument('--source-dir', type=str, default=None,
                      help='Source directory for custom dataset')
    
    args = parser.parse_args()
    
    if args.dataset == 'oxford':
        download_oxford_flowers(args.data_dir)
    elif args.dataset == 'flowers_recognition':
        download_flowers_recognition(args.data_dir)
    elif args.dataset == 'custom':
        if not args.source_dir:
            logger.error("Please provide --source-dir for custom dataset")
        else:
            prepare_custom_dataset(args.source_dir, args.data_dir)
