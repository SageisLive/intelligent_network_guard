import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def run_evaluation():
    print("Loading 'phishing_features.csv' dataset...")
    df = pd.read_csv('phishing_features.csv')
    X = df.drop(columns=['index', 'Result'])
    y = df['Result'].replace(-1, 0)

    print("Splitting dataset into 80% training and 20% testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=7, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=30, max_depth=10, random_state=42),
        "Support Vector Machine": SVC(kernel='rbf', probability=False),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=30, max_depth=5, random_state=42),
        "Multi-Layer Perceptron": MLPClassifier(hidden_layer_sizes=(20,), max_iter=300, random_state=42)
    }

    cell_text = []
    row_labels = []
    cm_dict = {}

    print("Executing model training and validation...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        cell_text.append([f"{acc:.4f}", f"{prec:.4f}", f"{rec:.4f}", f"{f1:.4f}"])
        row_labels.append(name)
        cm_dict[name] = cm

    print("Generating metrics_table.png...")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('off')
    
    columns = ["Accuracy", "Precision", "Recall", "F1-Score"]
    table_data = [["Model Architecture"] + columns]
    
    for i in range(len(row_labels)):
        table_data.append([row_labels[i]] + cell_text[i])
        
    # Rebalanced column widths to guarantee the text stays inside the bounds
    table = ax.table(
        cellText=table_data, 
        loc='center', 
        cellLoc='center', 
        colWidths=[0.40, 0.15, 0.15, 0.15, 0.15]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    # Scaling only the vertical height, leaving the horizontal ratio mathematically intact
    table.scale(1, 2.5) 
    
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#0f172a') 
        else:
            if col == 0:
                cell.set_text_props(weight='bold')
            
            if row % 2 == 1:
                cell.set_facecolor('#e2e8f0') 
            else:
                cell.set_facecolor('#ffffff') 
                
    plt.title('Empirical Evaluation Metrics', fontsize=26, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('metrics_table.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print("Generating confusion_matrices.png...")
    fig_cm, axes = plt.subplots(nrows=2, ncols=4, figsize=(18, 9))
    fig_cm.patch.set_facecolor('#1e1e2f')
    axes = axes.flatten()

    for idx, (name, cm) in enumerate(cm_dict.items()):
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], cbar=False,
                    xticklabels=['Legitimate', 'Phishing'],
                    yticklabels=['Legitimate', 'Phishing'],
                    annot_kws={"size": 14, "weight": "bold"})
        
        axes[idx].set_title(name, fontsize=13, fontweight='bold', color='white', pad=10)
        axes[idx].set_ylabel('Actual Label', color='white')
        axes[idx].set_xlabel('Predicted Label', color='white')
        axes[idx].tick_params(colors='white')

    axes[7].axis('off')

    plt.suptitle('Confusion Matrices for Threat Detection Models', fontsize=20, fontweight='bold', color='white', y=1.02)
    plt.tight_layout()
    
    plt.savefig('confusion_matrices.png', dpi=300, bbox_inches='tight', facecolor=fig_cm.get_facecolor())
    plt.close()

    print("Success! Visualizations have been saved to your folder.")

if __name__ == "__main__":
    run_evaluation()