"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import api from "./api";

interface User {
  id: number;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ error?: string }>;
  register: (
    email: string,
    password: string,
    name: string
  ) => Promise<{ error?: string }>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      const token = api.getToken();
      if (token) {
        const result = await api.getMe();
        if (result.data?.user) {
          setUser(result.data.user);
        } else {
          api.logout();
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const result = await api.login(email, password);

    if (result.error) {
      return { error: result.error };
    }

    if (result.data?.user) {
      setUser(result.data.user);
      router.push("/dashboard");
    }

    return {};
  };

  const register = async (email: string, password: string, name: string) => {
    const result = await api.register(email, password, name);

    if (result.error) {
      return { error: result.error };
    }

    if (result.data?.user) {
      setUser(result.data.user);
      router.push("/dashboard");
    }

    return {};
  };

  const logout = () => {
    api.logout();
    setUser(null);
    router.push("/");
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
