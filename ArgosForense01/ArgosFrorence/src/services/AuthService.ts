// src/services/AuthService.ts
import { User } from "../models/User";

export async function login(user: User): Promise<boolean> {
  // Simula um login bem simples
  if (user.username === "admin" && user.password === "1234") {
    return true;
  }
  return false;
}

