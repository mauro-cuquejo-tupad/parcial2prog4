interface NavbarProps {
  nombreApp: string;
}

export const Navbar = ({ nombreApp }: NavbarProps) => {
  return (
    <nav className="flex items-center justify-between bg-[#0b272f] px-8 py-4 text-white shadow-sm">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/20 bg-white/10 text-xs font-bold tracking-wider text-white">
          UTN
        </div>
        <div>
          <span className="text-lg font-bold tracking-tight text-white block leading-tight">
            {nombreApp}
          </span>
          <span className="text-[10px] font-medium text-emerald-400 block tracking-wider uppercase">
            TUPaD • Recup. 2do Parcial
          </span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-500/20 text-xs font-semibold text-emerald-300 border border-emerald-500/30">
          <img src="../src/assets/perfil.png" alt="foto perfil" className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-500/20 text-xs font-semibold text-emerald-300 border border-emerald-500/30" />
        </div>
        <div className="text-xs text-slate-300">
          Mauro Cuquejo
        </div>
      </div>
    </nav>
  );
};
