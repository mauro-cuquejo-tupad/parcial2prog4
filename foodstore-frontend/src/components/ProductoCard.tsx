import type { Producto } from "../types/producto";

interface ProductoCardProps {
  producto: Producto;
  onEditar: (producto: Producto) => void;
  onCambiarDisponibilidad: (producto: Producto) => void;
  onAnular: (producto: Producto) => void;
}

export const ProductoCard = ({
  producto,
  onEditar,
  onCambiarDisponibilidad,
  onAnular,
}: ProductoCardProps) => {
  const simbolo = producto.unidad_venta.simbolo;
  const precio = Number(producto.precio_base).toLocaleString("es-AR", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  const stock = Number(producto.stock_cantidad).toLocaleString("es-AR", {
    maximumFractionDigits: 3,
  });

  return (
    <article className="flex flex-col gap-3 rounded-2xl bg-white border border-[#e2e8f0] p-6 shadow-sm transition hover:shadow-md hover:border-[#cbd5e1]">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#e6f4f1] text-[#0d3b46] font-semibold">
            {simbolo.toUpperCase()}
          </div>
          <div>
            <h3 className="text-base font-semibold text-[#0f172a] leading-snug">
              {producto.nombre}
            </h3>
            {producto.descripcion && (
              <p className="text-xs text-[#64748b] line-clamp-2 mt-0.5">
                {producto.descripcion}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="my-1 flex items-baseline justify-between border-y border-[#f1f5f9] py-3">
        <div>
          <span className="text-xs uppercase font-medium text-[#64748b] block">Precio unitario</span>
          <span className="text-xl font-bold text-[#0d3b46]">
            $ {precio}
          </span>
          <span className="text-xs font-normal text-[#64748b]"> / {simbolo}</span>
        </div>
        <div className="text-right">
          <span className="text-xs uppercase font-medium text-[#64748b] block">Stock</span>
          <span className="text-sm font-semibold text-[#334155]">
            {stock} {simbolo}
          </span>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 text-xs">
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-medium border ${
            producto.disponible
              ? "bg-[#ecfdf5] text-[#065f46] border-[#a7f3d0]"
              : "bg-[#f1f5f9] text-[#475569] border-[#cbd5e1]"
          }`}
        >
          <span className={`h-1.5 w-1.5 rounded-full ${producto.disponible ? "bg-emerald-500" : "bg-slate-400"}`} />
          {producto.disponible ? "Venta activa" : "Venta pausada"}
        </span>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-medium border ${
            producto.hay_stock
              ? "bg-[#f0fdf4] text-[#166534] border-[#bbf7d0]"
              : "bg-[#fef2f2] text-[#991b1b] border-[#fecaca]"
          }`}
        >
          {producto.hay_stock ? "Con stock" : "Sin stock"}
        </span>
      </div>

      <div className="mt-auto flex flex-wrap gap-2 pt-2 border-t border-[#f1f5f9]">
        <button
          type="button"
          onClick={() => onEditar(producto)}
          className="rounded-xl border border-[#cbd5e1] bg-white px-3.5 py-1.5 text-xs font-semibold text-[#0f172a] hover:bg-[#f8fafc] transition shadow-sm"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onCambiarDisponibilidad(producto)}
          className={`rounded-xl border px-3.5 py-1.5 text-xs font-semibold transition shadow-sm ${
            producto.disponible
              ? "border-[#fde68a] bg-[#fffbeb] text-[#92400e] hover:bg-[#fef3c7]"
              : "border-[#bbf7d0] bg-[#f0fdf4] text-[#166534] hover:bg-[#dcfce7]"
          }`}
        >
          {producto.disponible ? "Pausar venta" : "Reanudar venta"}
        </button>
        <button
          type="button"
          onClick={() => onAnular(producto)}
          className="rounded-xl border border-[#fecaca] bg-white px-3.5 py-1.5 text-xs font-semibold text-[#dc2626] hover:bg-[#fef2f2] transition shadow-sm ml-auto"
        >
          Anular
        </button>
      </div>
    </article>
  );
};
