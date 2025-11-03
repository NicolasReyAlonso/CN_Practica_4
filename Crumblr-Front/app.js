const API_URL = "http://localhost:8080/crumbs"; // cámbialo por tu dominio en AWS

async function fetchCrumbs() {
  const res = await fetch(API_URL);
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
    headers: { "Content-Type": "application/json" },
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
  const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  if (res.ok) fetchCrumbs();
  else alert("Error al eliminar el crumb");
}

document.getElementById("create-form").addEventListener("submit", createCrumb);
fetchCrumbs();
