// src/App.tsx (actualizado)
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import NewProject from './pages/NewProject';
import GenerationProgress from './pages/GenerationProgress';
import ProjectResult from './pages/ProjectResult';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new-project" element={<NewProject />} />
        <Route path="/project-progress" element={<GenerationProgress />} />
        <Route path="/project-result" element={<ProjectResult />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;