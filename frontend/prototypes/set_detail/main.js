var set = null;
var cards = null;

function loadSet(id) {
    var setReq = new XMLHttpRequest();
    setReq.open("GET", "http://127.0.0.1:8000/sets/" + id + "/");
    setReq.send();
    setReq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(this.responseText));
            set = JSON.parse(this.response);
            loadCards(set['cards']);
        }
    }
}

function loadCards(link) {
    var cardsReq = new XMLHttpRequest();
    cardsReq.open("GET", link);
    cardsReq.send();
    cardsReq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(this.responseText));
            cards = JSON.parse(this.responseText);
            displaySet(set, cards);
        }
    }
}

function displaySet(set, cards) {
    let main = document.getElementsByTagName('main')[0];
    let cardsContainer = document.getElementById('cards');

    title = document.getElementById('set-title');
    title.innerHTML = set['name'];
    
    for(let i = 0; i < cards.length; i++) {
        var cardContainer = document.createElement('div');
        cardContainer.setAttribute('class', 'card');
        var frontP = document.createElement('p');
        frontP.innerHTML = cards[i]['front'];
        cardContainer.appendChild(frontP);
        var backP = document.createElement('p');
        backP.innerHTML = cards[i]['back'];
        cardContainer.appendChild(backP);
        cardsContainer.appendChild(cardContainer);
    }
}

loadSet(1);