const API_URL = "https://v4vbkmeftj.execute-api.us-east-1.amazonaws.com/prod/crumbs"; // tu endpoint
const API_KEY = "x3SV9yBfwuWJ3M3NyT3E541ykzkEWdN9jrMj40ah"; // 🔑 poné aquí tu API Key real

async function fetchCrumbs() {
  const res = await fetch(API_URL, {
    headers: {
      "x-api-key": API_KEY
    }
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
      <div>
        <p>${crumb.content}</p>
        ${crumb.image_url ? `<img src="${crumb.image_url}" alt="Crumb image">` : ""}
        <small>${new Date(crumb.created_at).toLocaleString()}</small>
      </div>
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
    headers: {
      "x-api-key": API_KEY
    }
  });

  if (res.ok) fetchCrumbs();
  else alert("Error al eliminar el crumb");
}

document.getElementById("create-form").addEventListener("submit", createCrumb);
fetchCrumbs();
