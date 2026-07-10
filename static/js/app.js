// ===== SaúdeAP — JavaScript Frontend =====

// --- Helpers ---
async function api(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return res.json();
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// --- Modal ---
function openModal(id) {
  document.getElementById(id).classList.add('active');
}

function closeModal(id) {
  document.getElementById(id).classList.remove('active');
  // Limpa o formulário se existir
  const form = document.querySelector(`#${id} form`);
  if (form) form.reset();
  const idField = document.querySelector(`#${id} [data-field="id"]`);
  if (idField) idField.value = '';
}

// --- Toast/Alert ---
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `position:fixed;top:1rem;right:1rem;padding:0.75rem 1.25rem;border-radius:0.5rem;color:#fff;font-size:0.875rem;z-index:9999;background:${type === 'error' ? '#dc2626' : '#16a34a'};box-shadow:0 4px 12px rgba(0,0,0,0.15);`;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// --- Confirmação de exclusão ---
function confirmDelete(message) {
  return confirm(message || 'Tem certeza que deseja remover este registro?');
}

// --- Formatação de data ---
function formatDate(dateStr) {
  if (!dateStr) return '-';
  const d = new Date(dateStr);
  return d.toLocaleDateString('pt-BR');
}

// --- Status do estoque ---
function getEstoqueStatus(quantidade) {
  if (quantidade <= 0) return { class: 'badge-danger', label: 'Indisponível' };
  if (quantidade <= 10) return { class: 'badge-warning', label: `${quantidade} unid.` };
  return { class: 'badge-success', label: 'Disponível' };
}

// --- Preenche um <select> com opções ---
function fillSelect(selector, items, valueKey, labelKey, placeholder = 'Selecione...') {

    const select = document.querySelector(selector);

    if (!select) {
        console.log("Select não encontrado:", selector);
        return;
    }

    select.innerHTML = `<option value="">${placeholder}</option>`;

    items.forEach(item => {

        select.innerHTML += `
            <option value="${item[valueKey]}">
                ${item[labelKey]}
            </option>
        `;

    });

}