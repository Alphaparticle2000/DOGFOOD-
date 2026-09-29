export type UserRole = "participant" | "organizer" | "judge";

export interface User {
    name: string;
    id: string;
    email: string;
    role: UserRole;
}