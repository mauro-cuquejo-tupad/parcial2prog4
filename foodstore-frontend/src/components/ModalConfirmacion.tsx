interface ModalConfirmacionProps {
  mensaje: string;
  onConfirmar: () => void;
  onCancelar: () => void;
}

export const ModalConfirmacion = ({
  mensaje,
  onConfirmar,
  onCancelar,
}: ModalConfirmacionProps) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0b272f]/50 p-4 backdrop-blur-xs">
      <div className="flex w-full max-w-sm flex-col gap-4 rounded-2xl bg-white border border-[#e2e8f0] p-6 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-50 text-red-600 font-bold">
            !
          </div>
          <div>
            <h3 className="text-base font-bold text-[#0d3b46]">
              Confirmar anulación
            </h3>
            <p className="text-xs text-[#64748b]">
              Esta acción dará de baja el producto
            </p>
          </div>
        </div>

        <p className="text-sm text-[#334155] leading-relaxed">
          {mensaje}
        </p>

        <div className="flex justify-end gap-2.5 mt-2 pt-3 border-t border-[#f1f5f9]">
          <button
            type="button"
            onClick={onCancelar}
            className="rounded-xl border border-[#cbd5e1] bg-white px-4 py-2 text-xs font-semibold text-[#475569] hover:bg-[#f8fafc] transition shadow-sm"
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={onConfirmar}
            className="rounded-xl bg-[#dc2626] px-4 py-2 text-xs font-semibold text-white hover:bg-[#b91c1c] transition shadow-sm"
          >
            Confirmar anulación
          </button>
        </div>
      </div>
    </div>
  );
};
