export default function Header() {
  return (
    <header className="bg-slate-900 text-white p-4 shadow-md flex justify-between items-center">
      <h1 className="text-2xl font-bold tracking-wide">
        Shopp3 <span className="text-blue-400">🛍️</span>
      </h1>
      <div className="w-1/3">
        <input
          type="text"
          placeholder="Buscar produtos ou lojas..."
          className="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </header>
  );
}