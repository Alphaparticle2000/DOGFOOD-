export type UserRole =
  | "participant"
  | "judge"
  | "organizer"
  | "admin";

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

export interface AuthSession {
  accessToken: string;
  user: User;
}