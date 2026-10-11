export type Role = "admin" | "hr" | "employee";

export type User = {
  id: number;
  username: string;
  email: string;
  role: Role;
};

export type Department = {
  id: number;
  name: string;
};

export type Employee = {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  role: string | null;
  join_date: string | null;
  salary: number | null;
  department_id: number | null;
};

export type EmployeeInput = Omit<Employee, "id">;
