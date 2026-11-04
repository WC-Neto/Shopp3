import Header from "@/components/header";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <Header />
      <section className="p-8">
        <h2 className="text-xl font-semibold mb-2">Vitrine Principal 🛍️</h2>
        <p className="text-slate-400">
          Em breve, os produtos e lojas cadastrados aparecerão aqui!
        </p>
      </section>
    </main>
  );
}