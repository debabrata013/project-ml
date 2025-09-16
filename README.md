# Project ML: Agriculture Assistant & Plant Disease Detection

## Overview
This project is a comprehensive machine learning solution for agriculture, featuring:
- **Plant Disease Detection** using deep learning
- **Crop Yield Prediction**
- **Weather Advisory Services**
- **Location-based Recommendations**
- **Conversational AI Agents** for agricultural assistance

The project is organized into modular Python packages, Jupyter notebooks, and scripts for training, inference, and testing.

---

## Directory Structure
```
project-ml/
├── Agriculture Assistant agent/   # Main agent and tools for agriculture assistance
├── dataset/                      # Datasets for plant disease, crop production, rainfall
├── home_inv_agent/               # Home inventory agent (optional)
├── models/                       # Trained models and encoders
├── notebooks/                    # Jupyter notebooks for EDA, training, and demos
├── outputs/                      # Output files and results
├── requirements_plant_disease.txt# Requirements for plant disease environment
├── setup_plant_disease_env.py    # Script to set up plant disease environment
├── test_plant_disease_model.py   # Test script for plant disease model
├── train_plant_disease_model.py  # Training script for plant disease model
└── ...
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd project-ml
```

### 2. Python Environment
- **Recommended:** Python 3.10+
- Use `venv` or `conda` for isolation.

#### Create and Activate Environment (venv example):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
- For general use:
  ```bash
  pip install -r Agriculture\ Assistant\ agent/requirements.txt
  ```
- For plant disease detection:
  ```bash
  pip install -r requirements_plant_disease.txt
  ```

### 4. Download/Extract Datasets
- Datasets are in the `dataset/` folder.
- If zipped, extract them before running scripts.

### 5. Model Files
- Pretrained models are in `models/`.
- If missing, run training scripts in `notebooks/` or `train_plant_disease_model.py`.

### 6. Running the Assistant Agent
```bash
cd 'Agriculture Assistant agent'
python agent.py
```

### 7. Running Plant Disease Detection
```bash
python train_plant_disease_model.py   # To train
python test_plant_disease_model.py    # To test
```

### 8. Jupyter Notebooks
For EDA, training, and demos:
```bash
cd notebooks
jupyter notebook
```

---

## Key Components
- **Agriculture Assistant agent/**: Main conversational AI, weather/location tools, and integration scripts.
- **models/**: Contains `.h5` (Keras), `.pkl` (pickle) models, and encoders.
- **dataset/**: Plant disease images, crop production, rainfall data.
- **notebooks/**: Interactive analysis and training.

---

## Testing
- Unit tests are in `Agriculture Assistant agent/` (e.g., `test_crop_recommendations.py`).
- Run with:
  ```bash
  python -m unittest discover 'Agriculture Assistant agent'
  ```

---

## Tips
- Ensure all dataset paths are correct in scripts/notebooks.
- For GPU training, install TensorFlow with GPU support.
- Update requirements as needed for your environment.

---

## Contact
For issues or contributions, please open an issue or pull request on the repository.
