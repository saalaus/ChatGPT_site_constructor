let context = []
const add_style = document.getElementById("custom-style")
const add_element = document.getElementById("custom-content")


Split(["#split-0", "#split-1", "#split-2"], {
    minSize: 0,
    sizes: [90, 10, 10],
});


function replaceScript(addCode){
    const add_code = document.getElementById("custom-code");
    const value = add_code.innerText

    var newScriptTag = document.createElement("script");
    newScriptTag.id = "custom-code"
    newScriptTag.textContent = value + addCode + "\n"
    add_code.parentNode.replaceChild(newScriptTag, add_code)
}

function addElement({code, to, before, after}){
    const add_element = document.querySelector(to) ||
                        document.getElementById("custom-content");

    if(before){
        add_element.insertAdjacentHTML("beforebegin", code)
    }
    else if(after){
        add_element.insertAdjacentHTML("afterend", code)
    }
    else{
        add_element.insertAdjacentHTML("beforeend", code)
    }
}

function makeData(data){
    switch (data.operation) {
        case "style":
            add_style.innerHTML += data.code + '\n'
            break
        case "add":
            addElement(data)
            break
        case "code":
            replaceScript(data.code);
            break
        case "edit":
            document.querySelector(data.element)[data.attribute] = data.value
            break
        case "del":
            document.querySelector(data.element).remove()
            break
        case "list":
            data.code.forEach(element => {
                makeData(element)
            });
            break
        default:
            console.error(data)
            break
    }
}
function sendRequest(message){
    context.push({role: "user", content: message})

    return fetch("/completion", {
        method: "POST",
        body: JSON.stringify(context),
    })
        .then((data) => data.json())
        .then((data) => data.result)
        .then((data) => {
            context.push({ role: "assistant", content: JSON.stringify(data) });
            return data;
        });
}


const text_input = document.getElementById('text-input');
text_input.addEventListener("keydown", (event) => {
    if (event.code === 'Enter'){
        text_input.disabled = true
        const text = text_input.value
        sendRequest(text).then(data => {
            makeData(data)
            text_input.disabled = false;
        })
        text_input.value = ""
        return false;
    }
})

const chat_el = document.getElementById('chat-block')
