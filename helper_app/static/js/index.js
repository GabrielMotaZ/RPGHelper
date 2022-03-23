const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    const characterName = document.getElementById('static_character_name').value;
    const stringSend = JSON.stringify({
        characterName: characterName,
        message: message
    });
    chatSocket.send(stringSend);
    messageInputDom.value = '';
    scroll_down();
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.characterName + '\n ' + data.message + '\n\n');
    scroll_down();
};

const targetDiv = document.getElementById("hiddenDiv");
const btn = document.getElementById("toggle");
btn.onclick = function () {
    if (targetDiv.style.display !== "none") {
        targetDiv.style.display = "none";
    } else {
        targetDiv.style.display = "block";
    }
    scroll_down();
};

function send_skill_results(name, result) {
    /*
    this will get the value and skill name,
    separate value string,
    roll dices and
    send the message to the chat.
    */
    
    var finalResult = 0;
    var finalAnswer = '';
    resultList = result.replace(/\s/g,'').split('+');
    for (i=0; i<resultList.length; i++) {
        resultList[i] = '+' + resultList[i];
    }
    for (i=0; i<resultList.length; i++) {
        if (resultList[i].includes('-')) {
            resultList[i] = resultList[i].slit('-');
            for (j=1; j<resultList[i].length; j++) {
                resultList.push('-' + resultList[i][j]);
                resultList[i].splice(j, 1);
            }
        }
    }
    for (i=0; i<resultList.length; i++) {
        if (resultList[i].includes('d')) {
            resultList[i] = resultList[i].split('d');
            for (j=0; j<parseInt(resultList[i][0]); j++) {
                var num = Math.floor(Math.random() * parseInt(resultList[i][1])) + 1;
                finalResult += num;
                finalAnswer += '1d' + resultList[i][1] + ' = ' + num + '\n';
            }
        } else if (resultList[i].includes('+') || resultList[i].includes('-')) {
            if (resultList[i].includes('+')) {
                resultList[i] = resultList[i].replace('+','');
                finalResult += parseInt(resultList[i]);
                finalAnswer += ' +' + resultList[i] + '\n';
            }
            if (resultList[i].includes('-')) {
                resultList[i] = resultList[i].replace('-','');
                finalResult -= parseInt(resultList[i]);
                finalAnswer += ' -' + resultList[i] + '\n';
            }
        } else {
            finalAnswer = 'error in ' + (i+1) + ' place in results';
            break;
        }
    }
    finalAnswer += 'final result for ' + name + ', ' + result + ': ' + finalResult;
    const characterName = document.getElementById('static_character_name').value;
    chatSocket.send(JSON.stringify({
        'message': finalAnswer,
        'characterName': characterName
    }));
    scroll_down();
}


function scroll_down(){
    document.getElementById('chat-log').scrollTop = document.getElementById('chat-log').scrollHeight;
}
