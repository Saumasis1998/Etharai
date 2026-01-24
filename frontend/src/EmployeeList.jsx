import { useEffect, useState } from "react";
import { api } from "./api";

export default function EmployeeList() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    api.get("/employees").then((res) => setEmployees(res.data));
  }, []);

  const remove = async (id) => {
    await api.delete(`/employees/${id}`);
    setEmployees(employees.filter((e) => e.id !== id));
  };

  return (
    <div>
      <h3>Employees</h3>
      {employees.length === 0 && <p>No employees found</p>}
      {employees.map((e) => (
        <div key={e.id} style={{ marginBottom: "8px" }}>
          {e.full_name} ({e.department})
          <button onClick={() => remove(e.id)} style={{ marginLeft: "10px" }}>
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}
