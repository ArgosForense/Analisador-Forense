import React from "react";

export default function ProfileList({ profiles }) {
  if (profiles.length === 0) {
    return <p className="text-gray-600">Nenhum perfil criado ainda.</p>;
  }

  return (
    <ul className="space-y-2">
      {profiles.map((profile, index) => (
        <li
          key={index}
          className="p-3 bg-white shadow rounded flex justify-between items-center"
        >
          <span className="font-medium">{profile.name}</span>
          <span className="text-sm text-gray-600">
            {profile.permissions.join(", ")}
          </span>
        </li>
      ))}
    </ul>
  );
}

