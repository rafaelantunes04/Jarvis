use reqwest::Client;
mod api_classes;

// Estado global (partilhado entre comandos)
struct AppState {
    client: Client,
}

#[tauri::command]
async fn login(
    state: tauri::State<'_, AppState>,
    username: String,
    password: String,
) -> Result<String, String> {
    let res = state.client
        .post("http://127.0.0.1:8000/login")
        .json(&api_classes::LoginRequest {
            username: &username,
            password: &password,
        })
        .send()
        .await
        .map_err(|e| format!("Erro de ligação: {e}"))?;

    match res.status().as_u16() {
        401 => Err("401: Credenciais inválidas.".into()),
        200 => {
            let body: api_classes::LoginResponse = res
                .json()
                .await
                .map_err(|e| format!("Erro ao ler resposta: {e}"))?;
            Ok(body.token)
        }
        status => Err(format!("Servidor devolveu HTTP {status}")),
    }
}

#[tauri::command]
async fn chat(
    state: tauri::State<'_, AppState>,
    message: String,
    token: String,
) -> Result<String, String> {
    let res = state.client
        .post("http://127.0.0.1:8000/chat")
        .json(&api_classes::ChatRequest {
            message: &message,
            token: &token,
        })
        .send()
        .await
        .map_err(|e| format!("Erro de ligação: {e}"))?;

    match res.status().as_u16() {
        401 => Err("401: Token Expirado ou Invalido".into()),
        200 => {
            let body: api_classes::ChatResponse = res
                .json()
                .await
                .map_err(|e| format!("Erro ao ler resposta: {e}"))?;
            Ok(body.message)
        }
        status => Err(format!("Servidor devolveu HTTP {status}")),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .manage(AppState {
            client: Client::new(),
        })
        .invoke_handler(tauri::generate_handler![chat, login])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}