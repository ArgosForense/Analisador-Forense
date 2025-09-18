import { User } from "../models/User";
import { login } from "../services/AuthService";

export class LoginViewModel {
  error: string = "";

  async signIn(user: User): Promise<boolean> {
    const success = await login(user);
    if (!success) {
      this.error = "Usuário ou senha incorretos";
      return false;
    }
    this.error = "";
    return true;
  }
}

