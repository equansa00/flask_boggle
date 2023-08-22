document.querySelector("#guess-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    let word = document.querySelector("#guess-input").value;
    let response = await axios.get('/check-word', { params: { word: word } });
    document.querySelector("#message").innerText = response.data.result;

    if (response.data.result === 'ok') {
        score += word.length;
        document.querySelector("#score").innerText = `Score: ${score}`;
    }
});

let score = 0;

let timeLeft = 60;
setInterval(function() {
    if (timeLeft > 0) {
        timeLeft--;
        document.querySelector("#timer").innerText = `Time left: ${timeLeft}`;
    } else {
        document.querySelector("#guess-form").disabled = true;
    }
}, 1000);

async function endGame() {
    let response = await axios.post('/post-score', { score: score });
    alert(`High Score: ${response.data.new_highscore}, Games Played: ${response.data.playcount}`);
}
