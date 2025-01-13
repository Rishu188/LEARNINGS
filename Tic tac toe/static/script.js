document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("board");
    const status = document.getElementById("status");
    const playerInput = document.getElementById("player-input");
    const startBtn = document.getElementById("start-btn");
    const startModal = document.getElementById("start-modal");
    const playerScore = document.getElementById("player-score");
    const aiScore = document.getElementById("ai-score");

    let playerName = "Player";
    let gameActive = false;

    // Initialize the game
    function initializeBoard() {
        board.innerHTML = ""; // Clear the board
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.index = i;
            board.appendChild(cell);
        }
    }

    // Fetch data from the server
    async function fetchData(url, data) {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        return response.json();
    }

    // Handle cell clicks
    board.addEventListener("click", async (event) => {
        if (!gameActive) return;

        const target = event.target;
        if (!target.classList.contains("cell")) return;

        const index = parseInt(target.dataset.index, 10);
        const result = await fetchData("/play", { move: index });

        updateBoard(result.board);
        if (result.winner) {
            status.textContent = `${result.winner} wins!`;
            updateScores(result.scores);
            gameActive = false;
        } else {
            status.textContent = "Your turn!";
        }
    });

    // Update the board visually
    function updateBoard(boardState) {
        const cells = document.querySelectorAll(".cell");
        cells.forEach((cell, index) => {
            cell.textContent = boardState[index];
        });
    }

    // Update the scores
  function updateScores(scores) {
    document.getElementById("player-score").textContent = scores.Player;
    document.getElementById("ai-score").textContent = scores.AI;
}
    

    // Start a new game
    startBtn.addEventListener("click", async () => {
        playerName = playerInput.value || "Player";
        startModal.style.display = "none";
        const result = await fetchData("/start", { player_name: playerName });
        updateScores(result.scores);
        initializeBoard();
        gameActive = true;
        status.textContent = "Your turn!";
    });

    // Initialize the modal and game
    startModal.style.display = "block";
});
