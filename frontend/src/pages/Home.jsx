import React, { useState } from 'react';
import Sidebar from '../components/SideBar';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';
import TabComponent from '../components/TabComponent';

function Home() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className="flex flex-row min-h-screen">
            <Sidebar isOpen={isSidebarOpen} />
            <div className="flex-1 bg-[#141414] flex flex-col">
                <Navbar toggleSidebar={toggleSidebar} />
                <div className="flex-1 p-4">
                    <TabComponent />
                </div>
            </div>
        </div>
    );
}

export default Home;