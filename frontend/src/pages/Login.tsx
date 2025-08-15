import { FormEvent, useState } from "react";
import api from "../lib/api";
import { setToken } from "../lib/auth";

export default function Login() {
  const [username,setUsername]=useState(""); const [password,setPassword]=useState("");
  const [error,setError]=useState("");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const form = new FormData();
      form.append("username", username);
      form.append("password", password);
      const { data } = await api.post("/api/v1/auth/login", form, { headers: { "Content-Type": "multipart/form-data" }});
      setToken(data.access_token);
      window.location.href = "/employees";
    } catch (e:any) { setError(e?.response?.data?.detail || "Login failed"); }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <form onSubmit={submit} className="w-full max-w-sm space-y-4 border p-6 rounded-xl">
        <h1 className="text-2xl font-bold">Login</h1>
        {error && <div className="text-red-600">{error}</div>}
        <input className="w-full border p-2 rounded" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input className="w-full border p-2 rounded" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="w-full bg-black text-white p-2 rounded">Sign in</button>
      </form>
    </div>
  );
}