import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import styles from "./index.module.css";
import ResultCard from "../../../shared/components/ResultCard/ResultCard";

const SearchResults = () => {
  interface Reserva {
    titulo: string;
    descricao: string;
    endereco: string;
    tipo: string;
    preco: number;
    petfriendly: boolean;
    destacado: boolean;
    imagens: string[];
  }
  
  const [reservas, setReservas] = useState<Reserva[]>([]);
const location = useLocation();

useEffect(() => {
    const fetchReservas = async () => {
      try {
const query = new URLSearchParams(location.search).toString();
        const response = await axios.get(`http://127.0.0.1:8000/queries/reservas?${query}`);
        setReservas(response.data);
      } catch (error) {
        console.error("Erro ao buscar reservas:", error);
      }
    };

    fetchReservas();
  }, [location.search]);

  return (
    <div className={styles.container}>
            <div className={styles.logo}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          x="0px"
          y="0px"
          width="100"
          height="100"
          viewBox="0,0,256,256"
          style={{ mixBlendMode: "normal" }}
        >
          <g fill="none" fillRule="nonzero" stroke="none" strokeWidth="1" strokeLinecap="butt" strokeLinejoin="miter" strokeMiterlimit="10" strokeDasharray="" strokeDashoffset="0" fontFamily="none" fontWeight="none" fontSize="none" textAnchor="none">
            <g transform="scale(0.5,0.5)">
              <path d="M7.9,256c0,-137 111.1,-248.1 248.1,-248.1c137,0 248.1,111.1 248.1,248.1c0,137 -111.1,248.1 -248.1,248.1c-137,0 -248.1,-111.1 -248.1,-248.1z" fill="#eb808c"></path>
              <path d="M408.1,206.8l-150.1,-74.9c-1.3,-0.6 -2.7,-0.6 -4,0l-150.2,74.9c-1.7,0.8 -2.7,2.4 -2.7,4.3v29.6c0,1.6 0.8,3.1 2.2,4c1.4,0.9 3.1,1 4.5,0.3l148.2,-74l148.1,74c0.6,0.3 1.3,0.5 2,0.5c0.9,0 1.8,-0.2 2.5,-0.7c1.4,-0.9 2.2,-2.4 2.2,-4v-29.8c0,-1.8 -1,-3.5 -2.7,-4.2z" fill="#ffffff"></path>
              <path d="M380.5,245.8l-124.5,-62l-124.5,62v115h69v-88.2h47.5v88.2h132.5z" fill="#ffffff"></path>
              <path d="M263.7,272.6h32v32h-32z" fill="#eb808c"></path>
            </g>
          </g>
        </svg>
      </div>

      <h1 className={styles.title}>Resultados da Busca</h1>
      <div className={styles.resultsContainer}>
        {reservas.map((reserva) => (
        <ResultCard
          key={reserva.titulo}
            title={reserva.titulo}
            description={reserva.descricao}
            state={reserva.endereco.split(", ").pop() || ""}
            reservationType={reserva.tipo}
            price={`R$ ${reserva.preco}`}
            petFriendly={reserva.petfriendly}
          highlighted={reserva.destacado}
          imageUrl={`/path/to/image/${reserva.imagens[0]}`}
          />
        ))}
      </div>
    </div>
  );
};

export default SearchResults;