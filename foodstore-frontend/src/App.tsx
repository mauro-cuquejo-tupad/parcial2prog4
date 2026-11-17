import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar";
import { ProductoList } from "./components/ProductoList";
import { ProductoModal } from "./components/ProductoModal";
import { ModalConfirmacion } from "./components/ModalConfirmacion";
import { Footer } from "./components/Footer";
import type { Producto, ProductoInput } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";

const API_URL = "http://localhost:8000/api/v1";

const extraerMensajeError = async (response: Response): Promise<string> => {
  try {
    const data: { detail?: string } = await response.json();
    return data.detail ?? "Ocurrió un error inesperado";
  } catch {
    return "Ocurrió un error inesperado";
  }
};

export const App = () => {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [unidades, setUnidades] = useState<UnidadMedida[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [modalProductoAbierto, setModalProductoAbierto] = useState(false);
  const [productoSeleccionado, setProductoSeleccionado] = useState<Producto | null>(null);

  const [modalConfirmarAbierto, setModalConfirmarAbierto] = useState(false);
  const [productoParaAnular, setProductoParaAnular] = useState<Producto | null>(null);

  const obtenerCatalogoCompleto = async () => {
    try {
      const [productosResponse, unidadesResponse] = await Promise.all([
        fetch(`${API_URL}/productos?limit=50`),
        fetch(`${API_URL}/unidades-medida`),
      ]);
      if (!productosResponse.ok || !unidadesResponse.ok) {
        throw new Error("No se pudo cargar el catálogo de productos");
      }
      setProductos(await productosResponse.json());
      setUnidades(await unidadesResponse.json());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    obtenerCatalogoCompleto();
  }, []);

  const abrirModalAnular = (producto: Producto) => {
    setProductoParaAnular(producto);
    setModalConfirmarAbierto(true);
  };

  const cerrarModalAnular = () => {
    setProductoParaAnular(null);
    setModalConfirmarAbierto(false);
  };

  const confirmarAnulacionProducto = async () => {
    if (!productoParaAnular) return;

    try {
      const response = await fetch(`${API_URL}/productos/${productoParaAnular.id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error(await extraerMensajeError(response));
      }
      cerrarModalAnular();
      await obtenerCatalogoCompleto();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
      cerrarModalAnular();
    }
  };

  const alternarDisponibilidadProducto = async (producto: Producto) => {
    const datos: ProductoInput = {
      nombre: producto.nombre,
      descripcion: producto.descripcion,
      precio_base: Number(producto.precio_base),
      stock_cantidad: Number(producto.stock_cantidad),
      unidad_venta_id: producto.unidad_venta_id,
      disponible: !producto.disponible,
    };

    try {
      const response = await fetch(`${API_URL}/productos/${producto.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      });
      if (!response.ok) {
        throw new Error(await extraerMensajeError(response));
      }
      await obtenerCatalogoCompleto();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    }
  };

  const abrirCreacionProducto = () => {
    setProductoSeleccionado(null);
    setModalProductoAbierto(true);
  };

  const abrirEdicionProducto = (producto: Producto) => {
    setProductoSeleccionado(producto);
    setModalProductoAbierto(true);
  };

  const cerrarModalProducto = () => {
    setModalProductoAbierto(false);
    setProductoSeleccionado(null);
  };

  const guardarDatosProducto = async (datos: ProductoInput): Promise<string | null> => {
    const url = productoSeleccionado
      ? `${API_URL}/productos/${productoSeleccionado.id}`
      : `${API_URL}/productos`;
    try {
      const response = await fetch(url, {
        method: productoSeleccionado ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      });
      if (!response.ok) {
        return await extraerMensajeError(response);
      }
      await obtenerCatalogoCompleto();
      cerrarModalProducto();
      return null;
    } catch {
      return "No se pudo conectar con el servidor";
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-[#f0f4f8] text-[#0f172a] font-sans antialiased">
      <Navbar nombreApp="FOODSTORE" />

      {modalProductoAbierto && (
        <ProductoModal
          producto={productoSeleccionado}
          unidades={unidades}
          onGuardar={guardarDatosProducto}
          onCancelar={cerrarModalProducto}
        />
      )}

      {modalConfirmarAbierto && productoParaAnular && (
        <ModalConfirmacion
          mensaje={
            <>
              ¿Estás seguro de que deseas anular el producto{" "}
              <strong className="font-bold text-[#0d3b46]">{productoParaAnular.nombre}</strong>?
            </>
          }
          onConfirmar={confirmarAnulacionProducto}
          onCancelar={cerrarModalAnular}
        />
      )}

      <main className="mx-auto w-full max-w-6xl flex-1 px-6 py-8 md:px-8">
        {/* Cabecera estilo portal UTN */}
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#0d3b46]">
              Gestión de Catálogo
            </span>
            <h1 className="text-3xl font-extrabold tracking-tight text-[#0d3b46] mt-1">
              Productos disponibles
            </h1>
            <p className="text-sm text-[#64748b] mt-1">
              Administrá precios, stock y estado de los productos.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-[#e6f4f1] border border-[#a7f3d0] px-3 py-1 text-xs font-medium text-[#065f46]">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              Base de datos conectada
            </span>
            <button
              type="button"
              onClick={abrirCreacionProducto}
              disabled={cargando || unidades.length === 0}
              className="inline-flex items-center gap-2 rounded-xl bg-[#0d3b46] px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-[#07242b] disabled:opacity-40 transition"
            >
              <span className="hidden md:inline">✚ Nuevo producto</span>
            </button>
          </div>
        </div>

        {cargando && (
          <div className="rounded-2xl border border-[#e2e8f0] bg-white p-12 text-center text-sm text-[#64748b] shadow-sm">
            Cargando catálogo de productos...
          </div>
        )}

        {error && (
          <div className="mb-6 rounded-2xl border border-[#fecaca] bg-[#fef2f2] p-4 text-sm text-[#991b1b] shadow-sm">
            {error}
          </div>
        )}

        {!cargando && !error && productos.length === 0 && (
          <div className="rounded-2xl border border-[#e2e8f0] bg-white p-12 text-center text-sm text-[#64748b] shadow-sm">
            Todavía no hay productos registrados en el catálogo.
          </div>
        )}

        {!cargando && productos.length > 0 && (
          <ProductoList
            productos={productos}
            onEditar={abrirEdicionProducto}
            onCambiarDisponibilidad={alternarDisponibilidadProducto}
            onAnular={abrirModalAnular}
          />
        )}
      </main>

      <Footer />
    </div>
  );
};
