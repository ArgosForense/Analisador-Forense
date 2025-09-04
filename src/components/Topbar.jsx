import React from 'react';
import { UserCircleIcon, ChevronDownIcon } from '@heroicons/react/24/outline';

function Topbar() {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm p-4 flex justify-end items-center">
      <div className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
        <UserCircleIcon className="w-7 h-7" />
        <span className="font-medium">Admin User</span>
        <ChevronDownIcon className="w-4 h-4" />
      </div>
    </header>
  );
}

export default Topbar;
