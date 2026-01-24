import { useEffect, useState } from "react";
import { api } from "../api";
import useDebounce from "../hooks/useDebounce";
import SearchInput from "./SearchInput";
import "../styles.css";

export default function EmployeeTable({ refresh }) {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  const debouncedSearch = useDebounce(search);

  useEffect(() => {
    api
      .get("/employees", {
        params: { search: debouncedSearch, page, limit: 5 },
      })
      .then((res) => setEmployees(res.data));
  }, [debouncedSearch, page, refresh]);

  const remove = async (id) => {
    await api.delete(`/employees/${id}`);
    setEmployees(employees.filter((e) => e.id !== id));
  };

  return (
    <>
      <SearchInput value={search} onChange={setSearch} />

      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {employees.map((e) => (
            <tr key={e.id}>
              <td>{e.full_name}</td>
              <td>{e.email}</td>
              <td>{e.department}</td>
              <td>
                <button onClick={() => remove(e.id)} className="btn-danger">
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>Prev</button>
        <span>Page {page}</span>
        <button onClick={() => setPage(page + 1)}>Next</button>
      </div>
    </>
  );
}
