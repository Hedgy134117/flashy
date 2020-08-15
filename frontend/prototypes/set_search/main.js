var globalSets = null;

function loadSets() {
    var setReq = new XMLHttpRequest();
    setReq.open("GET", "http://127.0.0.1:8000/sets/");
    setReq.send();
    setReq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            globalSets = JSON.parse(this.responseText);
            displaySets(globalSets);
        }
    }
}

function displaySets(sets) {
    document.getElementById('set-list').innerHTML = '';
    for (let setIndex = 0; setIndex < sets.length; setIndex++) {
        var set = document.createElement('li');
        set.appendChild(document.createTextNode(sets[setIndex]['name']));
        document.getElementById('set-list').appendChild(set);
    }
}

function onInput(evt) {
    let input = this.value;
    let possibleSets = [];

    for (let i = 0; i < globalSets.length; i++) {
        if (globalSets[i]['name'].toLowerCase().search(input.toLowerCase()) != -1) {
            possibleSets.push(globalSets[i]);
        }
    }

    displaySets(possibleSets);
}

document.getElementById('set-search').addEventListener('input', onInput, false);
loadSets();