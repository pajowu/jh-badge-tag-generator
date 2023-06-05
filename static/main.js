window.onload = () => {
  fetch("/bottle_types")
    .then((data) => data.json())
    .then((data) => {
      window.bottleTypes = data;
      updateBottleTypeSelector();
    });
  document
    .getElementById("bottle_selection_form")
    .addEventListener("submit", loadBottleType);
  document
    .getElementById("clip_form")
    .addEventListener("submit", generateBottleTag);
};

function updateBottleTypeSelector() {
  selector = document.getElementById("bottle_type_selector");
  selector.innerHTML = "";
  for (const key of Object.keys(window.bottleTypes)) {
    console.log(key);
    const node = document.createElement("option");
    node.name = key;
    node.textContent = key;
    selector.appendChild(node);
  }
}

function loadBottleType(e) {
  e.preventDefault();
  const bottle_type = e.target.bottle_type_selector.value;
  const bottle_config = window.bottleTypes[bottle_type];
  for (const [k, v] of Object.entries(bottle_config)) {
    document.getElementsByName(k).forEach((elem) => {
      elem.value = v;
    });
  }
}
function downloadTextAsFile(filename, mime_type, text) {
  const elem = document.createElement("a");
  elem.setAttribute(
    "href",
    "data:" + mime_type + ";charset=utf-8," + encodeURIComponent(text)
  );
  elem.setAttribute("download", filename);
  elem.style.display = "none";
  document.body.appendChild(elem);
  elem.click();
  document.body.removeChild(elem);
}

async function generateBottleTag(e) {
  e.preventDefault();
  var formData = new FormData(e.target);
  const data = Object.fromEntries(formData);
  document.getElementById("generate_button").disabled = true;
  response = await fetch("/generate_tag", {
    method: "POST",
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" },
  })
  if (response.status !== 200) {
    alert("Failed to generate tag")
  } else {
    downloadTextAsFile(formData.get("label") + ".stl", "model/stl", await response.text())
  }

  document.getElementById("generate_button").disabled = false;
//     .then((response) => {
//       if (response.status !== 200) {
//         throw "Failed to generate tag";
//       } else {
//         response
//           .text()
//           .then((e) =>
//             downloadTextAsFile(formData.name + ".stl", "model/stl", e)
//           );
//       }
//     })
//     .catch((err) => alert(err));
}
