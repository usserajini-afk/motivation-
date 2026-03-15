let currentChat = Date.now().toString();

function newChat(){

currentChat = Date.now().toString();

document.getElementById("chatbox").innerHTML="";

}

function sendMessage(){

let msg = document.getElementById("message").value;

fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
message:msg,
chat_id:currentChat
})
})
.then(res=>res.json())
.then(data=>{

let chatbox=document.getElementById("chatbox");

chatbox.innerHTML += "<p><b>You:</b> "+msg+"</p>";

chatbox.innerHTML += "<p><b>Bot:</b> "+data.reply+"</p>";

loadHistory();

});

document.getElementById("message").value="";

}

function loadHistory(){

fetch("/history")
.then(res=>res.json())
.then(data=>{
console.log('History data:', data);
let historyDiv=document.getElementById("history");

historyDiv.innerHTML="";

if (data.length === 0) {
    historyDiv.innerHTML = '<p style="color:#ccc">No chats yet. Send a message to start.</p>';
    return;
}

data.forEach(chat=>{

historyDiv.innerHTML +=
`<p onclick="openChat('${chat.id}')">${chat.title}</p>`;

});

})
.catch(err=>console.error('Error loading history:', err));

}

function openChat(id){

currentChat=id;

fetch("/load_chat/"+id)
.then(res=>res.json())
.then(data=>{

let chatbox=document.getElementById("chatbox");

chatbox.innerHTML="";

data.forEach(m=>{

chatbox.innerHTML += "<p><b>You:</b> "+m.user+"</p>";

chatbox.innerHTML += "<p><b>Bot:</b> "+m.bot+"</p>";

});

});

}

loadHistory();