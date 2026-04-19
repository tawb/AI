from PIL import Image
import numpy as np
import os
import pickle
from collections import Counter
import matplotlib.pyplot as plt

def preprocess_images_rgb(base_path='project_dataset', image_size=(32, 32)):
    data = []
    labels = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                continue  # skip non-image files

            file_path = os.path.join(root, file)
            try:
                img = Image.open(file_path).convert('RGB')
                img = img.resize(image_size)
                img_array = np.array(img).flatten()
                data.append(img_array)

                # Just use the parent folder name as the label
                label = os.path.basename(os.path.dirname(file_path))
                labels.append(label)

            except Exception as e:
                print(f"Skipping {file_path}: {e}")

    return np.array(data), np.array(labels)

# Process images
X_rgb, y_rgb = preprocess_images_rgb("project_dataset", image_size=(32, 32))

# Save processed data
with open("processed_data_rgb.pkl", "wb") as f:
    pickle.dump((X_rgb, y_rgb), f)

print(f"✅ Done! Processed {len(X_rgb)} images with shape {X_rgb.shape}")

# Summary and label count
label_counts = Counter(y_rgb)
for lbl, cnt in sorted(label_counts.items()):
    print(f"{lbl:<30} : {cnt}")

print(f"\nTotal categories: {len(label_counts)}")
print(f"Total images    : {sum(label_counts.values())}")

# Visualization 
plt.figure(figsize=(10, 4 + 0.15 * len(label_counts)))
plt.barh(list(label_counts.keys()), list(label_counts.values()))
plt.title("Image count per label")
plt.xlabel("# images")
plt.tight_layout()
plt.show()
