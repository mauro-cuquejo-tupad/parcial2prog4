import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import type { Producto, ProductoInput } from "../types/producto";
import type { UnidadMedida } from "../types/unidadMedida";
import { useEscape } from "../hooks/useEscape";

interface ProductoModalProps {
  producto: Producto | null;
  unidades: UnidadMedida[];
  onGuardar: (datos: ProductoInput) => Promise<string | null>;
  onCancelar: () => void;
}

interface FormularioProducto {
  nombre: string;
  descripcion: string;
  precio_base: string;
  stock_cantidad: string;
  unidad_venta_id: string;
  disponible: boolean;
}

export const ProductoModal = ({
  producto,
  unidades,
  onGuardar,
  onCancelar,
}: ProductoModalProps) => {
  const [formulario, setFormulario] = useState<FormularioProducto>({
    nombre: producto?.nombre ?? "",
    descripcion: producto?.descripcion ?? "",
    precio_base: producto ? String(Number(producto.precio_base)) : "",
    stock_cantidad: producto ? String(Number(producto.stock_cantidad)) : "0",
    unidad_venta_id: producto ? String(producto.unidad_venta_id) : "",
    disponible: producto?.disponible ?? true,
  });
  const [errorModal, setErrorModal] = useState<string | null>(null);
  const [guardando, setGuardando] = useState(false);

  const manejarCambioCampo = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormulario((anterior) => ({ ...anterior, [name]: value }));
  };

  const manejarEnvioFormulario = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setGuardando(true);
    setErrorModal(null);

    const datos: ProductoInput = {
      nombre: formulario.nombre,
      descripcion: formulario.descripcion.trim() === "" ? null : formulario.descripcion,
      precio_base: Number(formulario.precio_base),
      stock_cantidad: Number(formulario.stock_cantidad),
      unidad_venta_id: Number(formulario.unidad_venta_id),
      disponible: formulario.disponible,
    };

    const mensaje = await onGuardar(datos);
    if (mensaje) {
      setErrorModal(mensaje);
      setGuardando(false);
    }
  };

  // Hook personalizado para cerrar el modal al presionar tecla Escape
  useEscape(onCancelar);

  const estiloCampo =
    "rounded-xl border border-[#cbd5e1] bg-white px-3.5 py-2 text-sm text-[#0f172a] placeholder-[#94a3b8] focus:border-[#0d3b46] focus:outline-none focus:ring-2 focus:ring-[#0d3b46]/10";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0b272f]/50 p-4 backdrop-blur-xs">
      <form
        onSubmit={manejarEnvioFormulario}
        className="flex max-h-full w-full max-w-md flex-col gap-4 overflow-y-auto rounded-2xl bg-white border border-[#e2e8f0] p-6 shadow-xl"
      >
        <div className="flex items-center justify-between border-b border-[#f1f5f9] pb-3">
          <h2 className="text-lg font-bold text-[#0d3b46]">
            {producto ? "Editar producto" : "Nuevo producto"}
          </h2>
          <span className="rounded-full bg-[#f1f5f9] px-2.5 py-0.5 text-xs font-medium text-[#64748b]">
            Gestión
          </span>
        </div>

        {errorModal && (
          <p className="rounded-xl border border-[#fecaca] bg-[#fef2f2] p-3 text-xs text-[#991b1b]">
            {errorModal}
          </p>
        )}

        <label className="flex flex-col gap-1 text-xs font-semibold uppercase tracking-wider text-[#475569]">
          Nombre
          <input
            name="nombre"
            value={formulario.nombre}
            onChange={manejarCambioCampo}
            required
            minLength={3}
            placeholder="Ej: Harina 000"
            className={estiloCampo}
          />
        </label>

        <label className="flex flex-col gap-1 text-xs font-semibold uppercase tracking-wider text-[#475569]">
          Descripción
          <textarea
            name="descripcion"
            value={formulario.descripcion}
            onChange={manejarCambioCampo}
            rows={2}
            placeholder="Detalle o características del producto"
            className={estiloCampo}
          />
        </label>

        <label className="flex flex-col gap-1 text-xs font-semibold uppercase tracking-wider text-[#475569]">
          Unidad de venta
          <select
            name="unidad_venta_id"
            value={formulario.unidad_venta_id}
            onChange={manejarCambioCampo}
            required
            className={estiloCampo}
          >
            <option value="" disabled className="text-gray-400">
              Elegí una unidad
            </option>
            {unidades.map((unidad) => (
              <option key={unidad.id} value={unidad.id}>
                {unidad.nombre} ({unidad.simbolo})
              </option>
            ))}
          </select>
        </label>

        <div className="grid grid-cols-2 gap-3">
          <label className="flex flex-col gap-1 text-xs font-semibold uppercase tracking-wider text-[#475569]">
            Precio base ($)
            <input
              type="number"
              name="precio_base"
              value={formulario.precio_base}
              onChange={manejarCambioCampo}
              required
              min="0"
              step="0.01"
              className={estiloCampo}
            />
          </label>
          <label className="flex flex-col gap-1 text-xs font-semibold uppercase tracking-wider text-[#475569]">
            Stock inicial
            <input
              type="number"
              name="stock_cantidad"
              value={formulario.stock_cantidad}
              onChange={manejarCambioCampo}
              required
              min="0"
              step="0.001"
              className={estiloCampo}
            />
          </label>
        </div>

        <label className="flex items-center gap-2 text-sm text-[#334155] cursor-pointer pt-1">
          <input
            type="checkbox"
            checked={formulario.disponible}
            onChange={(e) =>
              setFormulario((anterior) => ({ ...anterior, disponible: e.target.checked }))
            }
            className="h-4 w-4 rounded border-gray-300 text-[#0d3b46] focus:ring-[#0d3b46]"
          />
          Disponible para la venta
        </label>

        <div className="flex justify-end gap-2.5 pt-3 border-t border-[#f1f5f9]">
          <button
            type="button"
            onClick={onCancelar}
            className="rounded-xl border border-[#cbd5e1] bg-white px-4 py-2 text-xs font-semibold text-[#475569] hover:bg-[#f8fafc] transition"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={guardando}
            className="rounded-xl bg-[#0d3b46] px-5 py-2 text-xs font-semibold text-white hover:bg-[#07242b] disabled:opacity-50 transition shadow-sm"
          >
            {guardando ? "Guardando..." : "Guardar producto"}
          </button>
        </div>
      </form>
    </div>
  );
};
