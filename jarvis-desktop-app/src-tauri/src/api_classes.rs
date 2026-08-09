use serde::{Deserialize, Serialize};
use serde_json::Value;

// Login
#[derive(Serialize)]
pub struct LoginRequest<'a> {
    pub username: &'a str,
    pub password: &'a str,
}

#[derive(Deserialize)]
pub struct LoginResponse {
    pub token: String,
}

// Chat
#[derive(Serialize)]
pub struct ChatRequest<'a> {
    pub message: &'a str,
    pub token: &'a str,
}

#[derive(Deserialize)]
pub struct ChatResponse {
    pub message: String,
}

// Memory
#[derive(Serialize)]
pub struct MemoryRequest<'a> {
    pub token: &'a str,
}

#[derive(Deserialize)]
pub struct MemoryResponse {
    pub conv_buffer: Vec<Value>,
    pub token_buffer: Vec<Value>,
}