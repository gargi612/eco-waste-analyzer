import argparse
import copy
import os
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import models

from dataset import create_dataloaders


def build_model(num_classes=3, device="cpu"):
    """
    Loads MobileNetV2 with pretrained weights and replaces the classifier head.
    """
    print("[INFO] Loading Pretrained MobileNetV2...")
    # Load pretrained model
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    
    # Freeze early layers to speed up training & prevent overfitting on small datasets
    for param in model.features[:-4].parameters():
        param.requires_grad = False

    # Replace the classifier head
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Sequential(
        nn.Dropout(p=0.4),
        nn.Linear(num_ftrs, 512),
        nn.ReLU(),
        nn.Dropout(p=0.3),
        nn.Linear(512, num_classes)
    )
    
    return model.to(device)


def train_model(model, dataloaders, criterion, optimizer, scheduler, device, num_epochs=25, patience=5, save_dir="weights"):
    """
    Standard PyTorch training loop with validation, learning rate scheduling, and early stopping.
    """
    os.makedirs(save_dir, exist_ok=True)
    since = time.time()

    val_acc_history = []
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    epochs_no_improve = 0
    save_path = os.path.join(save_dir, "best_model.pth")

    for epoch in range(num_epochs):
        print(f'\nEpoch {epoch+1}/{num_epochs}')
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # Zero the parameter gradients
                optimizer.zero_grad()

                # Forward pass
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)

                    # Backward pass + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # Statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # Deep copy the model and Early Stopping logic
            if phase == 'val':
                val_acc_history.append(epoch_acc.item())
                if epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())
                    torch.save(model.state_dict(), save_path)
                    epochs_no_improve = 0
                    print(f" -> Best model saved with Val Acc: {best_acc:.4f}")
                else:
                    epochs_no_improve += 1
                    print(f" -> No improvement for {epochs_no_improve} epochs.")

        if epochs_no_improve >= patience:
            print(f"\n[INFO] Early stopping triggered after {patience} epochs without improvement.")
            break

    time_elapsed = time.time() - since
    print(f'\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc: {best_acc:4f}')

    # Load best model weights
    model.load_state_dict(best_model_wts)
    return model, val_acc_history


def main(args):
    # Setup Device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Using device: {device}")

    # 1. Load Data
    print("[INFO] Initializing DataLoaders...")
    train_loader, val_loader, _, class_names, loss_weights = create_dataloaders(
        data_dir=args.data_dir,
        batch_size=args.batch_size,
        num_workers=args.workers,
        handle_imbalance=args.imbalance_strategy
    )
    
    if train_loader is None:
        return # Dataset directory was empty

    dataloaders = {'train': train_loader, 'val': val_loader}

    # 2. Build Model
    model = build_model(num_classes=len(class_names), device=device)

    # 3. Define Loss Function
    if loss_weights is not None and args.imbalance_strategy == 'weights':
        print("[INFO] Using Weighted CrossEntropyLoss")
        criterion = nn.CrossEntropyLoss(weight=loss_weights.to(device))
    else:
        criterion = nn.CrossEntropyLoss()

    # 4. Define Optimizer and Scheduler
    optimizer = optim.Adam(model.classifier.parameters(), lr=args.lr, weight_decay=1e-4) # Train only head first
    
    # Cosine Annealing reduces LR smoothly to a minimum
    scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)

    # 5. Train Model
    print("\n[INFO] Starting Training Phase...")
    model, val_history = train_model(
        model=model,
        dataloaders=dataloaders,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        num_epochs=args.epochs,
        patience=args.patience,
        save_dir=args.save_dir
    )
    print("\n[INFO] Saving Final Model and Labels...")
    torch.save(class_names, os.path.join(args.save_dir, "classes.pt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Waste Classification Model")
    parser.add_argument('--data_dir', type=str, default='dataset', help='Path to dataset directory')
    parser.add_argument('--save_dir', type=str, default='weights', help='Directory to save model weights')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for training')
    parser.add_argument('--epochs', type=int, default=25, help='Number of epochs to train')
    parser.add_argument('--patience', type=int, default=5, help='Early stopping patience')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--workers', type=int, default=4, help='Number of dataloader workers')
    parser.add_argument('--imbalance_strategy', type=str, default='sampler', choices=['sampler', 'weights', 'none'], help='How to handle class imbalance')
    
    args = parser.parse_args()
    main(args)
