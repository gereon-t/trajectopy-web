import React, { useState } from 'react';
import AppContent from './AppContent';
import SessionSelector from './components/SessionSelector';
import { createSession, getResults, getTrajectoryPositions, ENDPOINT_URL } from './api';
import { colorCycle } from './utils';
import ErrorModal from './components/ErrorModal';
import './App.css';


const LoadingScreen = () => (
  <div className="loading-screen">
    <div className="loading-spinner" />
    <p>Loading Session...</p>
  </div>
);

const App = () => {
  const [currentSession, setCurrentSession] = useState(null);
  const [initialTrajectories, setInitialTrajectories] = useState([]);
  const [initialResults, setInitialResults] = useState([]);

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);


  const handleCreateNewSession = async (name) => {
    setIsLoading(true);
    setError(null);
    try {
      const session = await createSession(name);

      setInitialTrajectories([]);
      setInitialResults([]);
      setCurrentSession(session);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadOldSession = async (session) => {
    setIsLoading(true);
    setError(null);
    try {
      const trajectoryMetadata = session.trajectories;

      const positionPromises = trajectoryMetadata.map(traj =>
        getTrajectoryPositions(session.id, traj.id)
      );
      const positionDataArray = await Promise.all(positionPromises);
      const resultsData = await getResults(session.id);
      const preloadedTrajectories = trajectoryMetadata.map((traj, index) => {
        const positionsDTO = positionDataArray.find(p => p.trajectory_id === traj.id);
        return {
          id: traj.id,
          name: traj.name,
          isVisible: true,
          positions: positionsDTO ? positionsDTO.positions : [],
          epsg: positionsDTO ? positionsDTO.epsg : 0,
          color: colorCycle[index % colorCycle.length],
          num_poses: traj.num_poses,
          duration: traj.duration,
          datarate: traj.datarate,
          has_orientations: traj.has_orientations,
        };
      });

      const preloadedResults = resultsData.map(res => ({
        id: res.id,
        name: res.name,
        reportUrl: `${ENDPOINT_URL}/results/render/${res.id}`
      }));

      setInitialTrajectories(preloadedTrajectories);
      setInitialResults(preloadedResults);
      setCurrentSession(session);

    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoBackToSessions = () => {
    setCurrentSession(null);
    setInitialTrajectories([]);
    setInitialResults([]);
  };


  if (isLoading) {
    return <LoadingScreen />;
  }

  if (error) {
    return <ErrorModal
      message={`Fatal Error: ${error} Please refresh the page.`}
      isOpen={true}
      onClose={() => setError(null)}
    />;
  }

  if (!currentSession) {
    return (
      <SessionSelector
        onCreateNew={handleCreateNewSession}
        onLoadOld={handleLoadOldSession}
        onError={(msg) => setError(msg)}
      />
    );
  }

  return (
    <AppContent
      currentSession={currentSession}
      initialTrajectories={initialTrajectories}
      initialResults={initialResults}
      onGoBack={handleGoBackToSessions}
    />
  );
}

export default App;