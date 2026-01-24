export default function SearchInput({ value, onChange }) {
  return (
    <input
      className="search-input"
      placeholder="Search by name, email or department"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}
