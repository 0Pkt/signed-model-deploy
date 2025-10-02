from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7)

clf = RandomForestClassifier(n_estimators=50, random_state=7).fit(Xtr, ytr)
print("Accuracy:", clf.score(Xte, yte))
joblib.dump(clf, "model.pkl")
print("Saved model.pkl")
