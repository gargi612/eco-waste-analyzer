import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
from sklearn.metrics import classification_report, confusion_matrix

from dataset import create_dataloaders
from train import build_model


def evaluate_model(model, test_loader, class_names, device):
    """
    Evaluates the model on the test set and generates detailed metrics.
    """
    model.eval()
    
    all_preds = []
    all_labels = []
    
    print("[INFO] Running evaluation on test set...")
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    # 1. Overall Accuracy
    correct = np.sum(all_preds == all_labels)
    total = len(all_labels)
    accuracy = correct / total
    print(f"\n[RESULTS] Overall Test Accuracy: {accuracy:.4f} ({correct}/{total})")
    
    # 2. Classification Report (Precision, Recall, F1)
    print("\n[RESULTS] Classification Report:")
    report = classification_report(all_labels, all_preds, target_names=class_names, digits=4)
    print(report)
    
    # 3. Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix - Waste Classification')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    # Save confusion matrix plot
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/confusion_matrix.png')
    print("[INFO] Confusion matrix saved to 'results/confusion_matrix.png'")
    
    return accuracy, report, cm


def main(args):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Using device: {device}")

    # 1. Load Data
    print("[INFO] Initializing Test DataLoader...")
    _, _, test_loader, class_names, _ = create_dataloaders(
        data_dir=args.data_dir,
        batch_size=args.batch_size,
        num_workers=args.workers,
        handle_imbalance='none' # Imbalance handling not needed for evaluation
    )
    
    if test_loader is None or len(test_loader) == 0:
        print("[ERROR] Could not load test dataset.")
        return

    # 2. Load Model
    print(f"[INFO] Loading model weights from: {args.weights_path}")
    if not os.path.exists(args.weights_path):
        print(f"[ERROR] Weights file not found at {args.weights_path}. Train the model first.")
        return
        
    # Check if classes.pt exists to ensure class names align
    classes_path = os.path.join(os.path.dirname(args.weights_path), "classes.pt")
    if os.path.exists(classes_path):
        saved_classes = torch.load(classes_path)
        if saved_classes != class_names:
            print(f"[WARNING] Class names mismatch! Model trained on {saved_classes}, but evaluating on {class_names}")
    
    model = build_model(num_classes=len(class_names), device=device)
    model.load_state_dict(torch.load(args.weights_path, map_location=device))
    
    # 3. Evaluate
    evaluate_model(model, test_loader, class_names, device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Waste Classification Model")
    parser.add_argument('--data_dir', type=str, default='dataset', help='Path to dataset directory')
    parser.add_argument('--weights_path', type=str, default='weights/best_model.pth', help='Path to saved model weights')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for evaluation')
    parser.add_argument('--workers', type=int, default=4, help='Number of dataloader workers')
    
    args = parser.parse_args()
    main(args)
