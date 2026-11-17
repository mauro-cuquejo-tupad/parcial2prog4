import type { Categoria } from "./categoria";
import type { UnidadMedida } from "./unidadMedida";

export interface Producto {
  id: number;
  unidad_venta_id: number;
  nombre: string;
  descripcion: string | null;
  precio_base: string;
  stock_cantidad: string;
  disponible: boolean;
  activo: boolean;
  anulado_at: string | null;
  hay_stock: boolean;
  unidad_venta: Pick<UnidadMedida, "id" | "nombre" | "simbolo">;
  categorias: Pick<Categoria, "id" | "nombre">[];
}

export interface ProductoInput {
  nombre: string;
  descripcion: string | null;
  precio_base: number;
  stock_cantidad: number;
  unidad_venta_id: number;
  disponible: boolean;
}