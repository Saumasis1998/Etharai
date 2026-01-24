import { useState } from "react";
import EmployeeModal from "./components/EmployeeModal";
import EmployeeTable from "./components/EmployeeTable";
import "./styles.css";

function App() {
  const [open, setOpen] = useState(false);
  const [refresh, setRefresh] = useState(0);

  return (
    <div className="container">
      <header className="header">
        <h2>HRMS Lite</h2>
        <button onClick={() => setOpen(true)} className="btn-primary">
          + Add Employee
        </button>
      </header>

      <EmployeeTable refresh={refresh} />

      <EmployeeModal
        open={open}
        onClose={() => setOpen(false)}
        onSuccess={() => setRefresh((r) => r + 1)}
      />
    </div>
  );
}

export default App;
