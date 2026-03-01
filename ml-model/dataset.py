import os
import shutil
import urllib.request
import zipfile
import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from torch.utils.data import DataLoader, Subset, WeightedRandomSampler
from torchvision import datasets, transforms
from PIL import Image

# ==============================================================================
# 1. DATASET SETUP & DOWNLOAD UTILITY
# ==============================================================================
def setup_dataset_structure(base_dir="dataset"):
    """
    Creates the required directory structure for the Waste Classification dataset.
    You will need to place your images inside these directories.
    """
    classes = ['biodegradable', 'recyclable', 'hazardous']
    for cls in classes:
        os.makedirs(os.path.join(base_dir, cls), exist_ok=True)
    print(f"[INFO] Created dataset structure at '{base_dir}/'")
    print(f"[INFO] Expected classes: {classes}")

def download_and_combine_data(target_dir="dataset"):
    """
    Placeholder script to demonstrate how you would automate dataset preparation.
    In reality, you would use kagglehub or direct URLs.
    """
    print("[INFO] Setting up dataset...")
    setup_dataset_structure(target_dir)
    print("Please populate these folders with images. Recommended sources:")
    print(" 1. TrashNet: https://github.com/garythung/trashnet")
    print(" 2. TACO: http://tacodataset.org/")
    print(" 3. Kaggle Waste: https://www.kaggle.com/datasets/techsash/waste-classification-data")
    print("\n[NOTE] Hazardous class is often missing. Supplement it by scraping Google Images")
    print("for terms like 'used batteries', 'e-waste', 'medical waste', 'chemical bottles'.")

# ==============================================================================
# 2. PREPROCESSING PIPELINE
# ==============================================================================
def get_transforms():
    """
    Returns transformations tailored for MobileNetV2 (224x224, ImageNet Means).
    Applies strong augmentations for training to prevent overfitting.
    """
    # MobileNetV2 standards
    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std = [0.229, 0.224, 0.225]

    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),               # Resize to larger than required
        transforms.RandomResizedCrop(224),           # Random crop back to 224x224
        transforms.RandomHorizontalFlip(p=0.5),      # Left-Right flip
        transforms.RandomVerticalFlip(p=0.2),        # Up-Down flip
        transforms.RandomRotation(degrees=30),       # Rotate +/- 30 degrees
        transforms.ColorJitter(
            brightness=0.3, contrast=0.3, 
            saturation=0.3, hue=0.1
        ),                                           # Color variations
        transforms.GaussianBlur(3, sigma=(0.1, 2.0)),# Simulate camera blur
        transforms.ToTensor(),                       # Convert PIL image to Torch Tensor
        transforms.Normalize(
            mean=imagenet_mean, 
            std=imagenet_std
        )                                            # Normalize
    ])

    test_transform = transforms.Compose([
        transforms.Resize((256, 256)),               # Resize consistently
        transforms.CenterCrop(224),                  # Center crop to 224x224
        transforms.ToTensor(),
        transforms.Normalize(
            mean=imagenet_mean, 
            std=imagenet_std
        )
    ])

    return train_transform, test_transform

# ==============================================================================
# 3. UTILITY FUNCTIONS
# ==============================================================================
def count_images_per_class(dataset):
    """
    Calculates the exact number of images in each class.
    Works for both ImageFolder and Subset types.
    """
    if hasattr(dataset, 'indices'):
        # It's a Subset
        targets = [dataset.dataset.targets[i] for i in dataset.indices]
        class_names = dataset.dataset.classes
    else:
        # It's an ImageFolder
        targets = dataset.targets
        class_names = dataset.classes
        
    counts = Counter(targets)
    distribution = {class_names[k]: v for k, v in counts.items()}
    return distribution, counts

def visualize_batch(loader, class_names):
    """
    Takes a DataLoader batch, denormalizes the images, and plots them using matplotlib.
    """
    images, labels = next(iter(loader))
    
    # ImageNet exact values for denormalization
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    
    num_images = min(16, len(images))
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    fig.suptitle("Augmented Training Batch Samples", fontsize=16)
    
    for i, ax in enumerate(axes.flatten()):
        if i >= num_images:
            ax.axis('off')
            continue
            
        # Re-arrange dimensions from (C, H, W) -> (H, W, C)
        img = images[i].numpy().transpose((1, 2, 0))
        # De-normalize
        img = std * img + mean
        img = np.clip(img, 0, 1)
        
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(class_names[labels[i]])
        
    plt.tight_layout()
    plt.show()

def save_preprocessed_dataset(dataset, output_dir="preprocessed_data"):
    """
    Saves the preprocessed tensor dataset to disk. Useful for testing pipelines faster.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"[INFO] Saving preprocessed dataset to '{output_dir}/'...")
    for idx, (img_tensor, label) in enumerate(dataset):
        torch.save((img_tensor, label), os.path.join(output_dir, f"sample_{idx}.pt"))
    print("[INFO] Save complete.")

# ==============================================================================
# 4. CLASS IMBALANCE HANDLING
# ==============================================================================
def get_class_weights(dataset, num_classes):
    """
    Approach A: Returns weights to be passed into nn.CrossEntropyLoss(weight=weights)
    Formula: Total_samples / (num_classes * class_count)
    """
    _, counts = count_images_per_class(dataset)
    total_samples = sum(counts.values())
    weights = [0.0] * num_classes
    
    for cls_idx, count in counts.items():
        if count > 0:
            weights[cls_idx] = total_samples / (num_classes * count)
            
    # Normalize weights manually to avoid explosion (optional but recommended)
    weights = np.array(weights)
    weights = weights / np.sum(weights) * num_classes 
    
    return torch.FloatTensor(weights)

def get_weighted_sampler(dataset):
    """
    Approach B: Creates a WeightedRandomSampler so the DataLoader naturally 
    samples minority classes more often during training.
    """
    _, counts = count_images_per_class(dataset)
    class_weights = {k: 1.0 / v for k, v in counts.items()}
    
    if hasattr(dataset, 'indices'):
        sample_weights = [class_weights[dataset.dataset.targets[i]] for i in dataset.indices]
    else:
        sample_weights = [class_weights[t] for t in dataset.targets]
        
    sampler = WeightedRandomSampler(
        weights=sample_weights, 
        num_samples=len(sample_weights), 
        replacement=True
    )
    return sampler

# ==============================================================================
# 5. MAIN DATALOADER CREATION
# ==============================================================================
def create_dataloaders(data_dir="dataset", batch_size=32, num_workers=4, handle_imbalance='sampler'):
    """
    Orchestrates the creation of 70/20/10 Train/Val/Test DataLoaders.
    
    Args:
        data_dir: Source folder with images.
        batch_size: Batch size of dataloaders. Minimum 32 recommended.
        num_workers: CPU cores optimized for preprocessing.
        handle_imbalance: 'sampler', 'weights', or None
    
    Returns:
        train_loader, val_loader, test_loader, class_names, loss_weights
    """
    if not os.path.exists(data_dir) or not any(os.scandir(data_dir)):
        download_and_combine_data(data_dir)
        print("[WARNING] Dataset directory was empty. Created structure, please add images and re-run.")
        return None, None, None, [], None

    train_transform, test_transform = get_transforms()
    
    # 1. We load the entire dataset twice with different transforms 
    # to maintain clean indexing for our subset splits later.
    train_dataset_base = datasets.ImageFolder(root=data_dir, transform=train_transform)
    test_dataset_base = datasets.ImageFolder(root=data_dir, transform=test_transform)
    
    class_names = train_dataset_base.classes
    total_size = len(train_dataset_base)
    print(f"[INFO] Found {total_size} images across classes: {class_names}")

    # 2. Determine split sizes (70% / 20% / 10%)
    train_size = int(0.7 * total_size)
    val_size = int(0.2 * total_size)
    test_size = total_size - train_size - val_size
    
    # 3. Generate balanced random indices
    generator = torch.Generator().manual_seed(42) # Fixed seed for reproducibility
    indices = torch.randperm(total_size, generator=generator).tolist()
    
    train_idx = indices[:train_size]
    val_idx = indices[train_size:train_size + val_size]
    test_idx = indices[train_size + val_size:]
    
    # 4. Create subsets (notice we use the augmented base for train, static base for val/test)
    train_subset = Subset(train_dataset_base, train_idx)
    val_subset = Subset(test_dataset_base, val_idx)
    test_subset = Subset(test_dataset_base, test_idx)

    print("\n[INFO] Dataset Split:")
    print(f"  Training:   {len(train_subset)}")
    print(f"  Validation: {len(val_subset)}")
    print(f"  Testing:    {len(test_subset)}")

    train_dist, _ = count_images_per_class(train_subset)
    print(f"\n[INFO] Training Class Distribution: {train_dist}")
    
    # 5. Handle Imbalance & Dataloaders
    loss_weights = None
    
    if handle_imbalance == 'sampler':
        print("[INFO] Using WeightedRandomSampler for DataLoaders...")
        sampler = get_weighted_sampler(train_subset)
        train_loader = DataLoader(
            train_subset, batch_size=batch_size, 
            sampler=sampler, num_workers=num_workers, 
            drop_last=True
        )
    else:
        if handle_imbalance == 'weights':
            print("[INFO] Calculating class weights for CrossEntropyLoss...")
            loss_weights = get_class_weights(train_subset, len(class_names))
            
        train_loader = DataLoader(
            train_subset, batch_size=batch_size, 
            shuffle=True, num_workers=num_workers, 
            drop_last=True
        )

    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_subset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, val_loader, test_loader, class_names, loss_weights

if __name__ == "__main__":
    # Test pipeline
    print("=== Initializing Computer Vision Dataset Pipeline ===\n")
    
    # By default, use handle_imbalance='sampler'
    train_dl, val_dl, test_dl, classes, cls_weights = create_dataloaders(
        data_dir="dataset",
        batch_size=32,
        num_workers=4,
        handle_imbalance='sampler'
    )
    
    if train_dl is not None:
        print("\n[INFO] Pipeline Ready! Showing sample batch...")
        visualize_batch(train_dl, classes)
