import React, { useState} from "react";
import PerfilLista from "../components/PerfilLista"
import PerfilFormulario from "../components/PerfilFormulario"

export default function GerenteDePerfis(){

    const[perfils, setPerfils] = useState([]);

    const addPerfil = (perfil) => {
        // Evitar duplicidade pelo nome 
        if (perfils.some((p) => p.nome === perfil.nome)){
            alert("Perfil ja existe!");
            return;
        }
        setPerfils([...perfils, perfil]);
    };

    return(
        <div className="space-y-6">
            <PerfilFormulario onAddProfile={addPerfil}/>
            <PerfilLista profiles={perfils}/>
        </div>
    );
}
