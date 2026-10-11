import { useState, type FormEvent } from "react";
import api, { errorMessage } from "../lib/api";
import type { Department, Employee, EmployeeInput } from "../lib/types";

type Props = {
  employee: Employee | null;
  departments: Department[];
  onClose: () => void;
  onSaved: () => void;
};

const inputClass =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20";

function toForm(employee: Employee | null) {
  return {
    name: employee?.name ?? "",
    email: employee?.email ?? "",
    phone: employee?.phone ?? "",
    role: employee?.role ?? "",
    join_date: employee?.join_date ?? "",
    salary: employee?.salary?.toString() ?? "",
    department_id: employee?.department_id?.toString() ?? "",
  };
}

export default function EmployeeForm({ employee, departments, onClose, onSaved }: Props) {
  const [form, setForm] = useState(() => toForm(employee));
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const set = (field: keyof typeof form) => (e: { target: { value: string } }) =>
    setForm((f) => ({ ...f, [field]: e.target.value }));

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSaving(true);
    const payload: EmployeeInput = {
      name: form.name.trim(),
      email: form.email.trim(),
      phone: form.phone.trim() || null,
      role: form.role.trim() || null,
      join_date: form.join_date || null,
      salary: form.salary === "" ? null : Number(form.salary),
      department_id: form.department_id === "" ? null : Number(form.department_id),
    };
    try {
      if (employee) await api.put(`/employees/${employee.id}`, payload);
      else await api.post("/employees/", payload);
      onSaved();
    } catch (err) {
      setError(errorMessage(err, "Could not save employee"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-10 flex items-center justify-center bg-slate-900/40 p-4" onClick={onClose}>
      <form
        onSubmit={submit}
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-lg space-y-4 rounded-2xl bg-white p-6 shadow-xl"
      >
        <h2 className="text-lg font-semibold">{employee ? "Edit employee" : "Add employee"}</h2>
        {error && (
          <div role="alert" className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <label className="space-y-1 sm:col-span-2">
            <span className="text-sm font-medium text-slate-700">Full name *</span>
            <input className={inputClass} value={form.name} onChange={set("name")} required autoFocus />
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Email *</span>
            <input className={inputClass} type="email" value={form.email} onChange={set("email")} required />
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Phone</span>
            <input className={inputClass} value={form.phone} onChange={set("phone")} />
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Job title</span>
            <input className={inputClass} value={form.role} onChange={set("role")} />
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Department</span>
            <select className={inputClass} value={form.department_id} onChange={set("department_id")}>
              <option value="">— None —</option>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Join date</span>
            <input className={inputClass} type="date" value={form.join_date} onChange={set("join_date")} />
          </label>
          <label className="space-y-1">
            <span className="text-sm font-medium text-slate-700">Salary (USD)</span>
            <input className={inputClass} type="number" min="0" step="0.01" value={form.salary} onChange={set("salary")} />
          </label>
        </div>
        <div className="flex justify-end gap-2 pt-2">
          <button type="button" onClick={onClose} className="rounded-lg px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100">
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500 disabled:opacity-60"
          >
            {saving ? "Saving…" : "Save"}
          </button>
        </div>
      </form>
    </div>
  );
}
