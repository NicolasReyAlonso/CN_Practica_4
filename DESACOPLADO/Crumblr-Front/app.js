const API_URL = "https://0lqziua1y9.execute-api.us-east-1.amazonaws.com/prod/crumbs";
const API_KEY = "McAPKEIMdV1s6P4C5IVvr4sxz5jE9CQa7JcjqMlR";


async function fetchCrumbs() {
  const res = await fetch(API_URL, {
    headers: { "x-api-key": API_KEY }
  });

  if (!res.ok) {
    alert("Error al obtener los crumbs");
    return;
  }

  const data = await res.json();
  const list = document.getElementById("crumbs-list");
  list.innerHTML = "";

  data.forEach(crumb => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div id="crumb-${crumb.crumb_id}">
        <p class="content">${crumb.content}</p>
        ${crumb.image_url ? `<img src="${crumb.image_url}" alt="Crumb image">` : ""}
        <small>${new Date(crumb.created_at).toLocaleString()}</small>
      </div>
      <button onclick="editCrumb('${crumb.crumb_id}', '${crumb.content.replace(/'/g, "\\'")}', '${crumb.image_url || ""}')">✏️</button>
      <button onclick="deleteCrumb('${crumb.crumb_id}')">🗑️</button>
    `;
    list.appendChild(li);
  });
}

async function createCrumb(e) {
  e.preventDefault();
  const content = document.getElementById("content").value.trim();
  const image_url = document.getElementById("image_url").value.trim();

  if (!content) return alert("El contenido no puede estar vacío");

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY
    },
    body: JSON.stringify({ content, image_url })
  });

  if (res.ok) {
    document.getElementById("create-form").reset();
    fetchCrumbs();
  } else {
    alert("Error al crear el crumb");
  }
}

async function deleteCrumb(id) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
    headers: { "x-api-key": API_KEY }
  });

  if (res.ok) fetchCrumbs();
  else alert("Error al eliminar el crumb");
}

// 🆕 Nueva función para editar un crumb
function editCrumb(id, currentContent, currentImage) {
  const newContent = prompt("Editá el contenido del crumb:", currentContent);
  if (newContent === null) return; // usuario canceló

  const newImage = prompt("Editá la URL de imagen (o dejá vacío):", currentImage);
  updateCrumb(id, newContent, newImage);
}

async function updateCrumb(id, content, image_url) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY
    },
    body: JSON.stringify({ content, image_url })
  });

  if (res.ok) {
    fetchCrumbs();
  } else {
    alert("Error al actualizar el crumb");
  }
}

document.getElementById("create-form").addEventListener("submit", createCrumb);
fetchCrumbs();