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
#[derive(Deserialize, Serialize)]
pub struct MemoryMessageExchange {
    pub question: String,
    pub answer: String,
}

#[derive(Deserialize, Serialize)]
pub struct MemoryResponse {
    pub conv_buffer: Vec<MemoryMessageExchange>,
    pub token_buffer: Vec<MemoryMessageExchange>,
    pub long_term_memory: Vec<Value>,
}