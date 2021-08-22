const url = "http://127.0.0.1:5000/process-text";

const $formLex = document.getElementById("formLex");
const $textLex = document.getElementById("textLex");
const $textResults = document.getElementById("textResults");
const $btnLex = document.getElementById("btnLex");

$btnLex.onclick = (e) => {
  e.preventDefault();
  sendInfo($textLex.value);
};

const sendInfo = async (text) => {
  $textResults.innerHTML = "";
  data = { text: text };
  const settings = {
    method: "POST",
    body: JSON.stringify(data),
    headers: new Headers({
      "content-type": "application/json",
    }),
    mode: "no-cors",
  };
  const res = await fetch(`${url}`, settings);
  data = await res.json()
  data.results.map(lex => $textResults.innerHTML += `${lex}\n`)
};
