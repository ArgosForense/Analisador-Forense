import React ,{useState} from "react";
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import GerenciadorPerfisView from './views/GerenciadorPerfisView';

//Dados de mock(simulando API)
const PERFIS_MOCK = [
    {id:1, nome: 'Analista Jr', permissoes:['ver_alertas']},
    {id:2, nome: 'Analista Sr', permissoes:['ver_alertas','escalar_incidentes']},
    {id:3, nome: 'Gerente SOC', permissoes:['ver_alertas', 'escalar_incidentes', 'gerenciar_firewall']},
];
const PERMISSOES_MOCK = [
    'ver_alertas',
    'escalar_incidentes',
    'gerenciar_firewall',
    'auditar_logs',
    'gerenciar_usuarios',
    'acessar_configuracoes'
]
function App(){
    const [perfis, setPerfis] = useState(PERFIS_MOCK);
    const [permissoesDisponiveis] = useState(PERMISSOES_MOCK);

    const adicionarPerfil = (novoPerfil) => {
        setPerfis([...perfis, {...novoPerfil, id: Date.now()}]);
    };
    const deletarPerfil = (id) => {
        setPerfis(perfis.filter(perfil => perfil.id !==id));
    };

    //Gerencia view que esta ativa 
    const [activeView, setActiveView] = useState('users-permissions');

    return (
        <div className="flex min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <Sidebar activeView={activeView} setActiveView={setActiveView}/>
        <div className="flex-1 p-6">
        <Topbar />
        <main className="flex-1 p-6">
        <GerenciadorPerfisView
        perfis = {perfis}
        permissoesDisponiveis = {permissoesDisponiveis}
        onAdicionarPerfil = {adicionarPerfil}
        onDeletarPerfil = {deletarPerfil}
        />
        </main>
        </div>
        </div>
    )
}

export default App
