import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_models(csv_path="phishing_features.csv"):
    df = pd.read_csv(csv_path)
    X = df.drop(columns=['index', 'Result'])
    y = df['Result'].replace(-1, 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=7, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42),
        "Support Vector Machine": SVC(kernel='rbf', probability=True),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=50, max_depth=5, random_state=42),
        "Multi-Layer Perceptron": MLPClassifier(hidden_layer_sizes=(30,), max_iter=500, random_state=42)
    }
    
    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        results.append({
            "Model": name,
            "Accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
            "Precision": round(precision_score(y_test, y_pred) * 100, 2),
            "Recall": round(recall_score(y_test, y_pred) * 100, 2),
            "F1-Score": round(f1_score(y_test, y_pred) * 100, 2)
        })
    return pd.DataFrame(results)