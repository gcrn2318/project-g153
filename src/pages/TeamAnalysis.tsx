import React, { useState } from 'react';
import { Users, Trophy, TrendingUp, Target } from 'lucide-react';

const TeamAnalysis = () => {
  const [selectedTeam, setSelectedTeam] = useState('Chennai Super Kings');

  const teams = {
    'Chennai Super Kings': {
      color: '#ffd700',
      titles: 4,
      winRate: 59.8,
      keyPlayers: ['MS Dhoni', 'Ravindra Jadeja', 'Ruturaj Gaikwad'],
      strengths: ['Consistent Performance', 'Strong Home Record', 'Experienced Squad'],
      weaknesses: ['Aging Squad', 'Overseas Dependency', 'Death Bowling']
    },
    'Mumbai Indians': {
      color: '#004ba0',
      titles: 5,
      winRate: 57.2,
      keyPlayers: ['Rohit Sharma', 'Jasprit Bumrah', 'Suryakumar Yadav'],
      strengths: ['Death Bowling', 'Power Hitting', 'Strong Core Team'],
      weaknesses: ['Middle Overs Batting', 'Spin Bowling Options', 'Inconsistent Openers']
    }
    // Add more teams as needed
  };

  const selectedTeamData = teams[selectedTeam];

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Team Analysis</h2>
        <select
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
          className="p-2 border rounded-md"
        >
          {Object.keys(teams).map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<Trophy className="h-6 w-6" />}
          title="IPL Titles"
          value={selectedTeamData.titles}
          color={selectedTeamData.color}
        />
        <StatCard
          icon={<TrendingUp className="h-6 w-6" />}
          title="Win Rate"
          value={`${selectedTeamData.winRate}%`}
          color={selectedTeamData.color}
        />
        <StatCard
          icon={<Users className="h-6 w-6" />}
          title="Squad Size"
          value="25"
          color={selectedTeamData.color}
        />
        <StatCard
          icon={<Target className="h-6 w-6" />}
          title="Current Position"
          value="4th"
          color={selectedTeamData.color}
        />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-4">Key Players</h3>
          <div className="space-y-4">
            {selectedTeamData.keyPlayers.map((player, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: selectedTeamData.color }} />
                <span>{player}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-4">Team Analysis</h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Strengths</h4>
              <ul className="list-disc list-inside space-y-1">
                {selectedTeamData.strengths.map((strength, index) => (
                  <li key={index}>{strength}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Areas for Improvement</h4>
              <ul className="list-disc list-inside space-y-1">
                {selectedTeamData.weaknesses.map((weakness, index) => (
                  <li key={index}>{weakness}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, color }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div style={{ color }}>{icon}</div>
        <span className="text-2xl font-bold" style={{ color }}>{value}</span>
      </div>
      <h3 className="text-gray-600">{title}</h3>
    </div>
  );
};

export default TeamAnalysis;