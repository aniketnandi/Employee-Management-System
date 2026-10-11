import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import EmployeeForm from "../components/EmployeeForm";
import api, { errorMessage } from "../lib/api";
import { clearToken } from "../lib/auth";
import type { Department, Employee, User } from "../lib/types";

const currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

export default function Employees() {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [search, setSearch] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState<Employee | "new" | null>(null);
  const [newDepartment, setNewDepartment] = useState("");

  const canEdit = user?.role === "admin" || user?.role === "hr";
  const departmentNames = useMemo(() => new Map(departments.map((d) => [d.id, d.name])), [departments]);

  const loadEmployees = useCallback(async () => {
    try {
      const { data } = await api.get<Employee[]>("/employees/", {
        params: { q: search || undefined, department_id: departmentFilter || undefined },
      });
      setEmployees(data);
      setError("");
    } catch (err) {
      setError(errorMessage(err, "Failed to load employees"));
    } finally {
      setLoading(false);
    }
  }, [search, departmentFilter]);

  const loadDepartments = useCallback(async () => {
    const { data } = await api.get<Department[]>("/departments/");
    setDepartments(data);
  }, []);

  useEffect(() => {
    api.get<User>("/auth/me").then((res) => setUser(res.data)).catch(() => {});
    loadDepartments().catch((err) => setError(errorMessage(err)));
  }, [loadDepartments]);

  // Debounce search so the API isn't called on every keystroke.
  useEffect(() => {
    const timer = setTimeout(loadEmployees, 250);
    return () => clearTimeout(timer);
  }, [loadEmployees]);

  const logout = () => {
    clearToken();
    navigate("/login", { replace: true });
  };

  const remove = async (employee: Employee) => {
    if (!window.confirm(`Delete ${employee.name}? This cannot be undone.`)) return;
    try {
      await api.delete(`/employees/${employee.id}`);
      await loadEmployees();
    } catch (err) {
      setError(errorMessage(err, "Could not delete employee"));
    }
  };

  const addDepartment = async (e: FormEvent) => {
    e.preventDefault();
    if (!newDepartment.trim()) return;
    try {
      await api.post("/departments/", { name: newDepartment.trim() });
      setNewDepartment("");
      await loadDepartments();
    } catch (err) {
      setError(errorMessage(err, "Could not add department"));
    }
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2">
            <img src="/favicon.svg" alt="" className="h-8 w-8" />
            <span className="font-semibold">Employee Management</span>
          </div>
          <div className="flex items-center gap-3 text-sm">
            {user && (
              <span className="text-slate-600">
                {user.username}
                <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium uppercase text-slate-600">
                  {user.role}
                </span>
              </span>
            )}
            <button onClick={logout} className="rounded-lg px-3 py-1.5 font-medium text-slate-700 hover:bg-slate-100">
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-4 px-4 py-6">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">Employees</h1>
            <p className="text-sm text-slate-500">
              {employees.length} {employees.length === 1 ? "result" : "results"}
              {!canEdit && user && " · read-only access"}
            </p>
          </div>
          {canEdit && (
            <button
              onClick={() => setEditing("new")}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500"
            >
              + Add employee
            </button>
          )}
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <input
            type="search"
            placeholder="Search by name, email or title…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 sm:max-w-sm"
          />
          <select
            value={departmentFilter}
            onChange={(e) => setDepartmentFilter(e.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none"
          >
            <option value="">All departments</option>
            {departments.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </select>
          {canEdit && (
            <form onSubmit={addDepartment} className="flex gap-2 sm:ml-auto">
              <input
                placeholder="New department"
                value={newDepartment}
                onChange={(e) => setNewDepartment(e.target.value)}
                className="w-40 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none"
              />
              <button type="submit" className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium hover:bg-slate-50">
                Add
              </button>
            </form>
          )}
        </div>

        {error && (
          <div role="alert" className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Title</th>
                <th className="px-4 py-3">Department</th>
                <th className="px-4 py-3">Joined</th>
                <th className="px-4 py-3 text-right">Salary</th>
                {canEdit && <th className="px-4 py-3" />}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {employees.map((e) => (
                <tr key={e.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-900">{e.name}</div>
                    <div className="text-slate-500">{e.email}</div>
                  </td>
                  <td className="px-4 py-3 text-slate-700">{e.role ?? "—"}</td>
                  <td className="px-4 py-3 text-slate-700">
                    {e.department_id ? departmentNames.get(e.department_id) ?? "—" : "—"}
                  </td>
                  <td className="px-4 py-3 text-slate-700">{e.join_date ?? "—"}</td>
                  <td className="px-4 py-3 text-right tabular-nums text-slate-700">
                    {e.salary != null ? currency.format(e.salary) : "—"}
                  </td>
                  {canEdit && (
                    <td className="whitespace-nowrap px-4 py-3 text-right">
                      <button onClick={() => setEditing(e)} className="rounded px-2 py-1 font-medium text-indigo-600 hover:bg-indigo-50">
                        Edit
                      </button>
                      <button onClick={() => remove(e)} className="rounded px-2 py-1 font-medium text-red-600 hover:bg-red-50">
                        Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))}
              {!loading && employees.length === 0 && (
                <tr>
                  <td colSpan={canEdit ? 6 : 5} className="px-4 py-10 text-center text-slate-500">
                    No employees found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>

      {editing && (
        <EmployeeForm
          employee={editing === "new" ? null : editing}
          departments={departments}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null);
            loadEmployees();
          }}
        />
      )}
    </div>
  );
}
