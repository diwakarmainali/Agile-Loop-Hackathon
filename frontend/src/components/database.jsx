import React, { useState } from 'react';

const LeaderboardItem = ({ rank, name, score, avatar, change }) => (
  <li className="flex items-center justify-between py-3 px-4 hover:bg-gray-700 transition-colors duration-150 ease-in-out">
    <div className="flex items-center">
      <span className={`w-8 h-8 flex-shrink-0 rounded-full flex items-center justify-center mr-4 ${
        rank <= 3 ? 'bg-yellow-500 text-gray-900' : 'bg-gray-600 text-white'
      }`}>
        {rank}
      </span>
      <img src={avatar} alt={name} className="w-10 h-10 rounded-full mr-4" />
      <span className="text-lg font-semibold text-white">{name}</span>
    </div>
    <div className="flex items-center">
      <span className="text-lg font-bold text-white mr-4">{score}</span>
      <span className={`text-sm ${change > 0 ? 'text-green-500' : 'text-red-500'}`}>
        {change > 0 ? `↑${change}` : `↓${Math.abs(change)}`}
      </span>
    </div>
  </li>
);

const Leaderboard = ({ players }) => {
  const [darkMode, setDarkMode] = useState(true);
  const sortedPlayers = [...players].sort((a, b) => b.score - a.score);

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-100'} transition-colors duration-150 ease-in-out`}>
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          <div className="p-6 sm:p-10">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl sm:text-3xl font-bold text-white">Leaderboard</h2>
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="px-4 py-2 bg-gray-700 text-white rounded-md hover:bg-gray-600 transition-colors duration-150 ease-in-out"
              >
                {darkMode ? 'Light Mode' : 'Dark Mode'}
              </button>
            </div>
            <div className="bg-gray-700 rounded-lg overflow-hidden">
              <ul className="divide-y divide-gray-600">
                {sortedPlayers.map((player, index) => (
                  <LeaderboardItem
                    key={player.id}
                    rank={index + 1}
                    name={player.name}
                    score={player.score}
                    avatar={player.avatar}
                    change={player.change}
                  />
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;