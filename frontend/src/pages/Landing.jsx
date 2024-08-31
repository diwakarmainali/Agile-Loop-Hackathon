// src/components/LandingPage.js
import React from 'react';
import OuterNavbar from '../components/OuterNavbar';
import Footer from '../components/Footer';
import DashboardImg from '/images/dashboard-quixflow-1.png'


const LandingPage = () => {
    return (
        <div className="min-h-screen flex flex-col">
        <OuterNavbar />
      
        <main className='flex-grow max-w-7xl mx-auto py-2 px-4 sm:px-6 lg:px-8'>
          <div className='w-full flex flex-col items-center gap-4 py-2 justify-center'>
            <div className='text-gray-300 text-center'>
              <p className='p-2'><b>Powered by</b></p>
              <img
                className="mt-3 max-w-full h-auto"
                alt="Picture"
                src="images/picture1-1.png"
              />
            </div>
            <div className='flex flex-col gap-4 p-6 w-full sm:w-auto'>
              <a href='#' className='block'>
                <img
                  className="max-w-full h-auto"
                  alt="Picture"
                  src="images/group-2.png"
                />
              </a>
            </div>
            <div className='w-full sm:w-auto'>
              <a href='#' className='block'>
                <img
                  className="max-w-full h-auto"
                  alt="Picture"
                  src="images/frame-2.png"
                />
              </a>
            </div>
          </div>
      
          <div className='w-full flex justify-center mt-4'>
            <img 
              className='py-4 max-w-full h-auto'
              src={DashboardImg}
              alt="Dashboard"
            />
          </div>
        </main>
      
        <Footer />
      </div>
    );
};

export default LandingPage;
