from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Input model
class MatchInput(BaseModel):
    currentScore: int
    wickets: int
    oversCompleted: float
    target: int

# Output model
class MatchOutput(BaseModel):
    runs_needed: int
    balls_remaining: int
    required_run_rate: float
    prediction: str

# Convert overs to balls
def overs_to_balls(overs: float) -> int:
    over = int(overs)
    balls = int((overs - over) * 10)
    return over * 6 + balls

@app.post("/predict/win", response_model=MatchOutput)
def predict_win(data: MatchInput):

    # T20 total balls
    total_balls = 20 * 6    

    # Runs needed
    runs_needed = data.target - data.currentScore

    # Balls faced
    balls_faced = overs_to_balls(data.oversCompleted)

    # Balls remaining
    balls_remaining = total_balls - balls_faced

    # Required Run Rate
    required_run_rate = (runs_needed / balls_remaining) * 6

    # Prediction logic 
    if required_run_rate <= 5:
        prediction = "Very High"
    elif required_run_rate <= 7:
        prediction = "High"
    elif required_run_rate <= 9:
        prediction = "Medium"
    elif required_run_rate <= 11:
        prediction = "Low"
    else:
        prediction = "Very Low"

    return {
        "runs_needed": runs_needed,
        "balls_remaining": balls_remaining,
        "required_run_rate": round(required_run_rate, 2),
        "prediction": prediction
    }