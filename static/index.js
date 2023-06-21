let context = []
const add_style = document.getElementById("custom-style")
const add_element = document.getElementById("custom-content")

function makeData(data){
    switch (data.operation) {
        case "style":
            add_style.innerHTML += data.code
            break
        case "add":
            add_element.insertAdjacentHTML("beforeend", data.code)
            break
        default:
            console.error(data)
    }
}
function sendRequest(message){
    context.push({role: "user", content: message})

    return fetch("/chatgpt", {
        method: "POST",
        body: JSON.stringify(context)
    })
        .then(data => data.json())
        .then(data => {
            context.push({role: "assistant", content: JSON.stringify(data)})
            return data
        })
}


const text_input = document.getElementById('text-input');
text_input.addEventListener("keydown", (event) => {
    if (event.code === 'Enter'){
        const text = text_input.value
        sendRequest(text).then(data => makeData(data))
        text_input.value = ""
        return false;
    }
})

const chat_el = document.getElementById('chat-block')
