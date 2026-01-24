import { useState } from "react";
import { api } from "./api";

export default function EmployeeForm() {
  const [form, setForm] = useState({
    employee_id: "",
    full_name: "",
    email: "",
    department: "",
  });

  const submit = async () => {
    if (!form.employee_id || !form.full_name) return alert("Required fields missing");
    await api.post("/employees", form);
    window.location.reload();
  };

  return (
    <div>
      <h3>Add Employee</h3>
      {Object.keys(form).map((key) => (
        <input
          key={key}
          placeholder={key}
          value={form[key]}
          onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          style={{ display: "block", marginBottom: "10px" }}
        />
      ))}
      <button onClick={submit}>Add</button>
    </div>
  );
}
