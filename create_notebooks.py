import json
import os

def create_nb(filename, cells):
    nb = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    for ctype, content in cells:
        if ctype == "markdown":
            cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [content]
            }
        else:
            cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [content]
            }
        nb["cells"].append(cell)
        
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

# Notebook 1
nb1_cells = [
    ("markdown", "# 01. Data Exploration\n\nThis notebook explores the synthetic dataset generated for training the ML Resume Scanner.\nIt covers class distribution, lengths, and skill frequency."),
    ("code", "import os\nimport sys\nsys.path.append('..')\n\nimport pandas as pd\nimport plotly.express as px\nfrom resume_scanner.ml.dataset import ResumeJDDatasetGenerator\n\n# Generate dataset\ngen = ResumeJDDatasetGenerator(seed=42)\nentries = gen.generate(pairs_per_domain=100)\ndf = pd.DataFrame([vars(e) for e in entries])\ndf.head()"),
    ("markdown", "## Class Distribution"),
    ("code", "fig = px.histogram(df, x='match_label', color='domain', title='Class Distribution by Domain', barmode='group')\nfig.show()"),
    ("markdown", "## Text Length Analysis"),
    ("code", "df['resume_len'] = df['resume_text'].apply(len)\ndf['jd_len'] = df['job_description'].apply(len)\n\nfig = px.scatter(df, x='resume_len', y='jd_len', color='match_label', title='Resume vs JD Length')\nfig.show()")
]

# Notebook 2
nb2_cells = [
    ("markdown", "# 02. Feature Engineering\n\nExtracts lexical and semantic features from the resume-JD pairs."),
    ("code", "import os\nimport sys\nsys.path.append('..')\n\nimport pandas as pd\nimport plotly.express as px\nfrom resume_scanner.ml.dataset import ResumeJDDatasetGenerator\nfrom resume_scanner.ml.features import FeatureExtractor\nfrom resume_scanner.ml.embeddings import get_encoder\n\n# Generate a small sample\ngen = ResumeJDDatasetGenerator(seed=42)\nentries = gen.generate(pairs_per_domain=20)\ndf = pd.DataFrame([vars(e) for e in entries])\n\nprint('Initializing Feature Extractor (loading Sentence-BERT)...')\nencoder = get_encoder()\nextractor = FeatureExtractor(encoder=encoder)"),
    ("markdown", "## Extracting Features"),
    ("code", "features_list = []\nfor i, row in df.iterrows():\n    feats = extractor.extract(row['resume_text'], row['job_description'])\n    feats['match_label'] = row['match_label']\n    feats['domain'] = row['domain']\n    features_list.append(feats)\n\nfeat_df = pd.DataFrame(features_list)\nfeat_df.head()"),
    ("markdown", "## Feature Correlations"),
    ("code", "corr = feat_df.select_dtypes('number').corr()\nfig = px.imshow(corr, title='Feature Correlation Matrix')\nfig.show()")
]

# Notebook 3
nb3_cells = [
    ("markdown", "# 03. Model Comparison\n\nTrains and evaluates Logistic Regression, Random Forest, and Gradient Boosting."),
    ("code", "import os\nimport sys\nsys.path.append('..')\n\nimport pandas as pd\nimport numpy as np\nfrom resume_scanner.ml.dataset import ResumeJDDatasetGenerator, create_train_test_split\nfrom resume_scanner.ml.features import FeatureExtractor\nfrom resume_scanner.ml.model import ModelTrainer, save_model\nfrom resume_scanner.ml.embeddings import get_encoder"),
    ("code", "# 1. Generate Dataset\ngen = ResumeJDDatasetGenerator(seed=42)\nentries = gen.generate(pairs_per_domain=100)\ntrain_entries, test_entries = create_train_test_split(entries)\n\nprint(f'Train: {len(train_entries)}, Test: {len(test_entries)}')"),
    ("code", "# 2. Extract Features\nencoder = get_encoder()\nextractor = FeatureExtractor(encoder=encoder)\n\ndef process(entries):\n    X, y = [], []\n    for e in entries:\n        X.append(extractor.extract_vector(e.resume_text, e.job_description))\n        y.append(e.match_label)\n    return np.array(X), np.array(y)\n\nX_train, y_train = process(train_entries)\nX_test, y_test = process(test_entries)"),
    ("code", "# 3. Train & Compare\ntrainer = ModelTrainer(feature_names=extractor.extract_vector.__code__.co_varnames) # Mock feature names for display\nresults = trainer.train_and_compare(X_train, y_train, X_test, y_test)\n\nimport json\nprint(json.dumps(results['comparison'], indent=2))"),
    ("code", "# 4. Save best model\nfrom resume_scanner.ml.features import FEATURE_SCHEMA\nsave_model(trainer.best_model, trainer.scaler, results['best_metrics'], FEATURE_SCHEMA)")
]

# Notebook 4
nb4_cells = [
    ("markdown", "# 04. Error Analysis\n\nAnalyzes False Positives and False Negatives from the trained model."),
    ("code", "import os\nimport sys\nsys.path.append('..')\n\nimport pandas as pd\nfrom resume_scanner.ml.model import load_model\n\ntry:\n    model, scaler, metadata, feature_names = load_model('../models')\n    print(f\"Loaded model: {metadata['model_name']} with F1: {metadata['f1']:.3f}\")\nexcept Exception as e:\n    print(f\"No trained model found: {e}\")"),
    ("markdown", "## Analysis of Misclassifications\n*Note: Run notebooks 1-3 first to generate the dataset and train the model.*")
]

create_nb("notebooks/01_data_exploration.ipynb", nb1_cells)
create_nb("notebooks/02_feature_engineering.ipynb", nb2_cells)
create_nb("notebooks/03_model_comparison.ipynb", nb3_cells)
create_nb("notebooks/04_error_analysis.ipynb", nb4_cells)

print("Notebooks created successfully.")
