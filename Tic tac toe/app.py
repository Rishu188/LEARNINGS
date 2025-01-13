from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="template")

# Initialize game state
board = [" " for _ in range(9)]
scores = {"Player": 0, "AI": 0}
player_name = ""

# Check for winner
def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] and board[condition[0]] != " ":
            return board[condition[0]]
    return None

# Minimax algorithm for AI
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":  # AI wins
        return 1
    elif winner == "X":  # Human wins
        return -1
    elif " " not in board:  # Draw
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

# AI move
def ai_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    global board, player_name, scores
    board = [" " for _ in range(9)]
    player_name = request.json.get("player_name", "Player")
    return jsonify({"player_name": player_name, "scores": scores})

@app.route("/play", methods=["POST"])
def play():
    global board, scores
    move = int(request.json["move"])
    if board[move] == " ":
        board[move] = "X"
        winner = check_winner(board)
        if winner:
            scores["Player"] += 1
            return jsonify({"board": board, "winner": "Player", "scores": scores})
        elif " " not in board:
            return jsonify({"board": board, "winner": "Draw", "scores": scores})

        ai_move()
        winner = check_winner(board)
        if winner:
            scores["AI"] += 1
            return jsonify({"board": board, "winner": "AI", "scores": scores})
    return jsonify({"board": board, "winner": None, "scores": scores})

@app.route("/reset", methods=["POST"])
def reset_game():
    global board
    board = [" " for _ in range(9)]
    return jsonify({"board": board})

if __name__ == "__main__":
    app.run(debug=True)


