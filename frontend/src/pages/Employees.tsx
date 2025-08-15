import { useEffect, useState } from "react";
import api from "../lib/api";
import { authHeader } from "../lib/auth";

type Employee = { id:number; name:string; email:string; role?:string; phone?:string };

export default function Employees(){
  const [list,setList] = useState<Employee[]>([]);
  const [error,setError] = useState("");

  useEffect(()=>{
    api.get("/api/v1/employees/", { headers: authHeader() })
      .then(res => setList(res.data))
      .catch(err => setError(err?.response?.data?.detail || "Failed to load"));
  },[]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Employees</h1>
      {error && <div className="text-red-600">{error}</div>}
      <div className="space-y-2">
        {list.map(e => (
          <div key={e.id} className="border rounded p-3">
            <div className="font-semibold">{e.name}</div>
            <div className="text-sm">{e.email} {e.role ? `• ${e.role}` : ""}</div>
          </div>
        ))}
      </div>
    </div>
  );
}