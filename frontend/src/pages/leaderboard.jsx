import React from 'react';

const LeaderboardItem = ({ rank, name, location, score, wins, time, avatar }) => (
  <tr className="border-b border-gray-700">
    <td className="py-3 px-4 text-center">{rank}</td>
    <td className="py-3 px-4 flex items-center">
      <img src={avatar} alt={name} className="w-8 h-8 rounded-full mr-3" />
      <span>{name}</span>
    </td>
    <td className="py-3 px-4">{location}</td>
    <td className="py-3 px-4">{score}</td>
    <td className="py-3 px-4">{wins}</td>
    <td className="py-3 px-4">{time}</td>
  </tr>
);

const Leaderboard = () => {
  const leaderboardData = [
    { rank: 1, name: "Damien Braun", location: "Edinburgh", score: 1000, wins: 50, time: "2h 30m", avatar: "https://i.pravatar.cc/150?img=1" },
    { rank: 2, name: "Aisha Patel", location: "Mumbai", score: 950, wins: 48, time: "2h 45m", avatar: "https://i.pravatar.cc/150?img=2" },
    { rank: 3, name: "Carlos Rodriguez", location: "Madrid", score: 900, wins: 45, time: "3h 00m", avatar: "https://i.pravatar.cc/150?img=3" },
    { rank: 4, name: "Sophie Chen", location: "Shanghai", score: 850, wins: 42, time: "3h 15m", avatar: "https://i.pravatar.cc/150?img=4" },
    { rank: 5, name: "Lucas Müller", location: "Berlin", score: 800, wins: 40, time: "3h 30m", avatar: "https://i.pravatar.cc/150?img=5" },
    { rank: 6, name: "Emma Watson", location: "London", score: 750, wins: 38, time: "3h 45m", avatar: "https://i.pravatar.cc/150?img=6" },
    { rank: 7, name: "Hiroshi Tanaka", location: "Tokyo", score: 700, wins: 35, time: "4h 00m", avatar: "https://i.pravatar.cc/150?img=7" },
    { rank: 8, name: "Isabella Silva", location: "São Paulo", score: 650, wins: 32, time: "4h 15m", avatar: "https://i.pravatar.cc/150?img=8" },
    { rank: 9, name: "Ahmed Hassan", location: "Cairo", score: 600, wins: 30, time: "4h 30m", avatar: "https://i.pravatar.cc/150?img=9" },
    { rank: 10, name: "Olivia Kim", location: "Seoul", score: 550, wins: 28, time: "4h 45m", avatar: "https://i.pravatar.cc/150?img=10" },
  ];
  return (
    <div className="bg-gray-900 text-white p-8 rounded-lg shadow-lg max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Leaderboard</h1>
          <p className="text-gray-400">Quixflow people</p>
        </div>
      </div>
      <div className="overflow-x-auto bg-gray-800 rounded-lg">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-700">
              <th className="py-3 px-4 text-left">#</th>
              <th className="py-3 px-4 text-left">Participant name</th>
              <th className="py-3 px-4 text-left">Location</th>
              <th className="py-3 px-4 text-left">Score</th>
              <th className="py-3 px-4 text-left">Wins</th>
              <th className="py-3 px-4 text-left">Time</th>
            </tr>
          </thead>
          <tbody>
            {leaderboardData.map((item, index) => (
              <LeaderboardItem key={index} {...item} />
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-6 flex justify-center">
  
      </div>
    </div>
  );
};

export default Leaderboard;