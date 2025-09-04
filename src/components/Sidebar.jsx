import React from "react";
import {ShieldCheckIcon, BellAlertIcon, BugAntIcon, DocumentTextIcon, UsersIcon, Cog6ToothIcon, ShieldExclamationIcon } from '@heroicons/react/24/outline';


function Sidebar({ activeView, setActiveView }) {
  const navItems = [
    { name: 'Dashboard', icon: <ShieldCheckIcon className="w-5 h-5" />, path: 'dashboard' },
    { name: 'Alerts', icon: <BellAlertIcon className="w-5 h-5" />, path: 'alerts' },
    { name: 'Incidents', icon: <BugAntIcon className="w-5 h-5" />, path: 'incidents' },
    { name: 'Reports', icon: <DocumentTextIcon className="w-5 h-5" />, path: 'reports' },
    { name: 'Users & Permissions', icon: <UsersIcon className="w-5 h-5" />, path: 'users-permissions' },
    { name: 'Settings', icon: <Cog6ToothIcon className="w-5 h-5" />, path: 'settings' },
  ];

    return (
        <aside className="w-64 bg-gray-800 text-white p-4 flex flex-col">
            <div className="flex items-center gap-2 mb-8">
                <ShieldExclamationIcon className="w-8 h-8 text-blue-500"/>
                <h2 className="text-xl font-semibold">SOC Menager</h2>
            </div>
            <nav className="flex-1">
                <ul>
                    {navItems.map((item) => (
                        <li key={item.path} className="mb-2">
                            <button
                                onClick={() => setActiveView(item.path)}
                                className={`flex items-center gap-3 w-full py-2 px-3 rouded-md transition-colors duration-200 ${
                                    activeView === item.path 
                                    ? 'bg-blue-600 text-white'
                                    : 'hover:bg-gray-700 text-gray-300 hover:text-white'
                                }`}
                            >
                            {item.icon}
                            <span>{item.name}</span>
                            </button>
                        </li>
                    ))}
                </ul>
            </nav>
            {/* tem que add um rodape*/}
            <div className="mt-auto pt-4 border-t border-gray-700 text-sm text-gray-400">
            </div>
        </aside>

    );
}

export default Sidebar;

