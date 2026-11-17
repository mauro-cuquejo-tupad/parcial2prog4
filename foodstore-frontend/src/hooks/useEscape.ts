import { useEffect } from "react"


export const useEscape = (onEscape: () => void) => {
    useEffect(() => {
        const manejarTecla = (evento: KeyboardEvent) => {
            if (evento.key === "Escape") {
                onEscape();
            }
        };

        window.addEventListener("keydown", manejarTecla);
        return () => {
            window.removeEventListener("keydown", manejarTecla);
        };
    }, [onEscape]);
};