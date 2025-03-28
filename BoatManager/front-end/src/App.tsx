import React, { useState } from "react";
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { Links } from './constants'
import { ManagementPage, DeviceListPage, AlertPage, LoginPage, Unauthorized } from './pages'


const App: React.FC = () => {

  return (
    <BrowserRouter>
      <Routes>
        <Route path={Links[0]} element={<LoginPage />}></Route >
        <Route path={Links[1]} element={<DeviceListPage />}></Route >
        <Route path={Links[2]} element={<ManagementPage />}></Route >
        <Route path={Links[3]} element={<AlertPage />}></Route >
      </Routes>
    </BrowserRouter >
  )
};

export default App;

