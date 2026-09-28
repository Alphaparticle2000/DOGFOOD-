import { createContext, useContext, useState } from "react";
import type { User } from "../types/auth";

interface AuthContextType {
  user: User | null;
  login: (email: string) => void;
  logout: () => void;
}

const authcontext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider = ({ children }: { children: React.ReactNode }) => {

  const [user, setUser] = useState<User | null>(null);

  const login = () => {
    const mockUser: User = {
      id: "user_01",
      name: "Himanshu",
      email: "himanshu@example.com",
      role: "participant",
    };

    setUser(mockUser);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <authcontext.Provider
      value={{
        user,
        login,
        logout,
      }}
    >
      {children}
    </authcontext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(authcontext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
};

export default AuthProvider;