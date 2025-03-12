import React, { useState } from "react";
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { Links } from './constants'
import { ManagementPage, DeviceListPage, AlertPage } from './pages'

//import './App.css';

const App: React.FC = () => {

  return (
    <BrowserRouter>
      <Routes>
        <Route path={Links[0]} element={<ManagementPage />}></Route >
        <Route path={Links[1]} element={<DeviceListPage />}></Route >
        <Route path={Links[2]} element={<AlertPage />}></Route >
      </Routes>
    </BrowserRouter >
  )
};

export default App;

