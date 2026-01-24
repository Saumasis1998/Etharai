import { useState } from "react";
import { api } from "../api";
import "../styles.css";

export default function EmployeeModal({ open, onClose, onSuccess }) {
  const [form, setForm] = useState({
    employee_id: "",
    full_name: "",
    email: "",
    department: "",
  });

  if (!open) return null;

  const submit = async () => {
    await api.post("/employees", form);
    onSuccess();
    onClose();
  };

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h3>Add Employee</h3>

        {Object.keys(form).map((key) => (
          <input
            key={key}
            placeholder={key.replace("_", " ")}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}

        <div className="modal-actions">
          <button onClick={submit} className="btn-primary">Save</button>
          <button onClick={onClose} className="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  );
}
