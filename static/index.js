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
  //   const xhttp = new XMLHttpRequest();
  // xhttp.onload = function() {
  //     const add_style = document.getElementById("custom-style")
  //     const add_element = document.getElementById("custom-content")
  //     const text = JSON.parse(this.responseText)
  //     console.log(text)
  //     if (text.action === "new_style"){
  //         console.log("new_style")
  //         add_style.innerHTML += text.data
  //     }
  //     if (text.action === "add"){
  //         console.log("new_element")
  //         add_element.insertAdjacentHTML("beforeend", text.data)
  //     }
  //     context.push({role: "assistant", content: text.message})
      // const text = this.responseText.split(/\r?\n/)
      // const last_line = text.pop()
      // console.log(text)
      // console.log(last_line)
      // if (text.join().startsWith('```html')) {
      //     console.log()
          // chat_text_el.innerHTML += '<p class="text-left">' + last_line + '</p>'
          // const text2 = text.join('\n').slice(7, text.join('\n').length-3)
          // document.body.insertAdjacentHTML('beforeend', text2)
      // }
      // else{
      //     chat_text_el.innerHTML += '<p class="text-left">' + text + '</p>'
      // }

    // }
    // context.push({role: "user", content: message})
    // xhttp.open('POST', '/chatgpt', true)
    // xhttp.send(JSON.stringify(context))
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

const chat_text_el = document.getElementById('chat-text-block')
chat_text_el.scrollTo(0, chat_text_el.scrollHeight)
const text_input = document.getElementById('text-input');
text_input.addEventListener("keydown", (event) => {
    if (event.code === 'Enter'){
        const text = text_input.value
        chat_text_el.innerHTML += '<p class="text-right">' + text_input.value + '</p>'
        text_input.value = '';
        chat_text_el.scrollTo(0, chat_text_el.scrollHeight)
        sendRequest(text).then(data => makeData(data))
        return false;
    }
})

const chat_el = document.getElementById('chat-block')
