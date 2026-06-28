
use serde::{Deserialize, Serialize};

// ── Estruturas de pedido / resposta ──────────────────────────
#[derive(Serialize)]
struct ChatRequest<'a> {
    username: &'a str,
    password: &'a str,
    message:  &'a str,
}

#[derive(Deserialize)]
struct ChatResponse {
    message: String,
}

// ── Comando Tauri ─────────────────────────────────────────────
/// Envia uma mensagem ao servidor local e devolve a resposta.
/// Replica o comportamento do script Python original.
#[tauri::command]
async fn send_message(
    username: String,
    password: String,
    message:  String,
) -> Result<String, String> {
    let client = reqwest::Client::new();

    let res = client
        .post("http://localhost:8000/chat")
        .json(&ChatRequest {
            username: &username,
            password: &password,
            message:  &message,
        })
        .send()
        .await
        .map_err(|e| format!("Erro de ligação: {e}"))?;

    match res.status().as_u16() {
        401 => Err("401: Credenciais inválidas.".into()),
        200 => {
            let body: ChatResponse = res
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
        .invoke_handler(tauri::generate_handler![send_message])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

