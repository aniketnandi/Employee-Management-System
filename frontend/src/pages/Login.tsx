import { useState, type FormEvent } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import api, { errorMessage } from "../lib/api";
import { getToken, setToken } from "../lib/auth";

type Mode = "login" | "register";

const inputClass =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20";

export default function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (getToken()) return <Navigate to="/employees" replace />;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      if (mode === "register") {
        await api.post("/auth/register", { username, email, password });
      }
      const form = new URLSearchParams({ username, password });
      const { data } = await api.post("/auth/login", form);
      setToken(data.access_token);
      navigate("/employees", { replace: true });
    } catch (err) {
      setError(errorMessage(err, mode === "login" ? "Login failed" : "Registration failed"));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-6">
      <div className="w-full max-w-sm">
        <div className="mb-6 text-center">
          <img src="/favicon.svg" alt="" className="mx-auto mb-3 h-12 w-12" />
          <h1 className="text-2xl font-semibold tracking-tight">Employee Management</h1>
          <p className="mt-1 text-sm text-slate-500">
            {mode === "login" ? "Sign in to your account" : "Create a read-only account"}
          </p>
        </div>

        <form onSubmit={submit} className="space-y-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          {error && (
            <div role="alert" className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
              {error}
            </div>
          )}
          <label className="block space-y-1">
            <span className="text-sm font-medium text-slate-700">Username</span>
            <input className={inputClass} value={username} onChange={(e) => setUsername(e.target.value)} required autoFocus />
          </label>
          {mode === "register" && (
            <label className="block space-y-1">
              <span className="text-sm font-medium text-slate-700">Email</span>
              <input className={inputClass} type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </label>
          )}
          <label className="block space-y-1">
            <span className="text-sm font-medium text-slate-700">Password</span>
            <input
              className={inputClass}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              minLength={mode === "register" ? 8 : undefined}
              required
            />
          </label>
          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500 disabled:opacity-60"
          >
            {submitting ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
          </button>
          <p className="text-center text-sm text-slate-500">
            {mode === "login" ? "No account yet?" : "Already registered?"}{" "}
            <button
              type="button"
              className="font-medium text-indigo-600 hover:text-indigo-500"
              onClick={() => {
                setMode(mode === "login" ? "register" : "login");
                setError("");
              }}
            >
              {mode === "login" ? "Register" : "Sign in"}
            </button>
          </p>
        </form>

        <p className="mt-4 text-center text-xs text-slate-400">
          Demo admin: <code className="font-mono">admin</code> / <code className="font-mono">admin123</code>
        </p>
      </div>
    </div>
  );
}
