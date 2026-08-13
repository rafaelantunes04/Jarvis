use serde::{Deserialize, Serialize};
use serde_json::Value;

// Login
#[derive(Serialize)]
pub struct LoginRequest<'a> {
    pub username: &'a str,
    pub password: &'a str,
}

// Chat
#[derive(Serialize)]
pub struct ChatRequest<'a> {
    pub message: &'a str,
}

#[derive(Deserialize)]
pub struct ChatResponse {
    pub message: String,
}

// Memory
#[derive(Deserialize)]
pub struct MemoryResponse {
    pub conv_buffer: Vec<Value>,
    pub token_buffer: Vec<Value>,
}