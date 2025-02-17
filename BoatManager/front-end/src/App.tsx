
import React, { useState } from "react";
import ManagementPage from "./components/ManagementPage";
import DeviceListPage from "./components/DeviceListPage";
import './App.css';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState("management");

  return (
    <div className="container">
      <nav>
        <button onClick={() => setCurrentPage("management")}>Manage Devices</button>
        <button onClick={() => setCurrentPage("list")}>View Devices</button>
      </nav>

      {currentPage === "management" && <ManagementPage />}
      {currentPage === "list" && <DeviceListPage />}
    </div>
  );
};

export default App;

