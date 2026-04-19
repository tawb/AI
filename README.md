# AI Project

AI/ML projects in Python: a genetic algorithm for optimizing multi-vehicle delivery routes under capacity constraints, and an image classifier using a decision tree trained on RGB pixel features.

---

## Project 1: Vehicle Routing Problem — Genetic Algorithm

### Problem

Assign **60 packages** (6–15 kg each, with priority levels) to **6 delivery vans** (120 kg capacity) and find routes that minimize total travel distance. All vehicles start and return to a depot at (0, 0).

### How It Works

- **Population** — Random feasible assignments generated via shuffled first-fit packing
- **Selection** — Rank-based proportional selection
- **Crossover** — Two parents merge and redistribute packages to produce children
- **Mutation** — Random package swaps between vehicles (respecting capacity)
- **Elitism** — Top 2 solutions carry over each generation

The algorithm runs for 500 generations and visualizes the best route using Python's `turtle` module.

### Files

| File | Description |
|------|-------------|
| `data.json` | Input data — 60 packages and 6 vehicles |
| `data_classes.py` | Core classes (`Package`, `Vehicle`, `Solution`) and data loading |
| `genatic.py` | Genetic algorithm + animated route visualization |

### Run

```bash
python genatic.py
```

---

## Project 2: Image Classification — Decision Tree

### Problem

Classify images into categories using pixel-level RGB features and a decision tree.

### How It Works

1. Images are loaded from subfolders inside `project_dataset/`, resized to 32×32, converted to RGB, and flattened into 3072-length feature vectors.
2. A `DecisionTreeClassifier` (entropy, max_depth=10) is trained on 80% of the data.
3. Evaluated with accuracy, classification report, and confusion matrix.

### Files

| File | Location | Description |
|------|----------|-------------|
| `preprocess_dataset.py` | `project_dataset/` | Loads and preprocesses images, saves to `.pkl` |
| `decision_tree_model.py` | `project_dataset/` | Trains and evaluates the decision tree |
| `processed_data_rgb.pkl` | `project_dataset/` | Preprocessed dataset (features + labels) |

### Dataset Structure

Place your images in subfolders by class:

```
project_dataset/
├── class_a/
│   ├── img1.jpg
│   └── img2.png
├── class_b/
│   ├── img3.jpg
│   └── ...
├── preprocess_dataset.py
├── decision_tree_model.py
└── processed_data_rgb.pkl
```

### Run

```bash
cd project_dataset

# Step 1: Preprocess
python preprocess_dataset.py

# Step 2: Train and evaluate
python decision_tree_model.py
```

---

## Requirements

- Python 3.8+
- NumPy
- Pillow
- scikit-learn
- Matplotlib
- Seaborn

```bash
pip install numpy pillow scikit-learn matplotlib seaborn
```

> **Note:** The route visualization requires a graphical display (`turtle` module).
