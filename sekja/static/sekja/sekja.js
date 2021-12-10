document.addEventListener("DOMContentLoaded", () => {
  console.log("Document Loaded") 
})

function login_pengguna() {
   const login_h1_text = document.querySelector('#login-h1-text');
   const login_admin_text = document.querySelector('#login-admin-text');
   const login_pengguna_text = document.querySelector('#login-pengguna-text');
   const status_user_form = document.querySelector('#status-user-form');

   // Ubah judul login
   login_h1_text.innerHTML = "Login";
   // Ubah value status_user_form
   status_user_form.value = 2
   // Hide/Show login role text
   login_admin_text.style.display = 'block';
   login_pengguna_text.style.display = 'none';
}

function login_admin() {
   const login_h1_text = document.querySelector('#login-h1-text');
   const login_admin_text = document.querySelector('#login-admin-text');
   const login_pengguna_text = document.querySelector('#login-pengguna-text');
   const status_user_form = document.querySelector('#status-user-form');

   // Ubah judul login
   login_h1_text.innerHTML = "Login (Admin)";
   // Ubah value status_user_form
   status_user_form.value = 1
   // Hide/Show login role text
   login_admin_text.style.display = 'none';
   login_pengguna_text.style.display = 'block';
}