from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

app = Flask(__name__)

# Load and preprocess the dataset
matches = pd.read_csv("matches.csv", index_col=0)
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype(int)
matches["day_code"] = matches["date"].dt.dayofweek
matches["target"] = (matches["result"] == "W").astype(int)

cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]

def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    return group.dropna(subset=new_cols)

matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
matches_rolling = matches_rolling.droplevel('team')
matches_rolling.index = range(matches_rolling.shape[0])

predictors = ["venue_code", "opp_code", "hour", "day_code"] + new_cols
rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

def make_predictions(data, predictors):
    train = data[data["date"] < "2024-01-01"]
    test = data[data["date"] > "2024-01-01"]
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    precision = precision_score(test["target"], preds)
    return combined, precision

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict')
def predict():
    team = request.args.get('team', default='Manchester United', type=str)
    combined, _ = make_predictions(matches_rolling, predictors)

    combined = combined.merge(
        matches_rolling[["date", "team", "opponent", "result"]],
        left_index=True, right_index=True
    )
    
    # Drop duplicates after merging
    combined = combined.drop_duplicates()
    team_matches = combined[combined["team"] == team]
    team_matches = team_matches.sort_values(by="date", ascending=False)  # Sort by date descending

    data = team_matches[["date", "team", "opponent", "result", "actual", "predicted"]]
    return jsonify(data.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
