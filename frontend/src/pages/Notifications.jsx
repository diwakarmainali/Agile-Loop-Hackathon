import React from 'react';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';
import { FaInfoCircle, FaCheckCircle, FaExclamationCircle } from 'react-icons/fa';

function Notifications() {
    const notifications = [
        { id: '001', icon: <FaInfoCircle />, type: 'Info', message: 'Your order has been shipped.', date: '2024-06-10', status: 'Unread' },
        { id: '002', icon: <FaCheckCircle />, type: 'Success', message: 'Your payment was successful.', date: '2024-06-09', status: 'Read' },
        { id: '005', icon: <FaExclamationCircle />, type: 'Warning', message: 'Unusual login attempt detected.', date: '2024-06-06', status: 'Unread' },
    ];

    const typeColors = {
        'Info': 'text-blue-500',
        'Success': 'text-green-500',
        'Warning': 'text-yellow-500'
    };

    return (
        <div>
            <Navbar />
            <main className='flex max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 flex-col gap-8'>
                <div className='flex justify-end'>
                    <div className='flex flex-col gap-2'>
                        <div className='h-16 rounded-lg bg-blue-500'></div>
                        <h2 className='text-2xl font-bold'>Hi Darel,</h2>
                    </div>
                </div>

                <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
                    {notifications.map((notification, index) => (
                        <div
                            key={index}
                            className={`group flex flex-col border border-gray-200 rounded-lg transition-transform transform hover:scale-105 hover:shadow-lg p-4 ${notification.status === 'Unread' ? 'bg-gray-100' : 'bg-white'}`}
                        >
                            <div className='flex justify-between items-center'>
                                <div className={`text-3xl ${typeColors[notification.type]}`}>
                                    {notification.icon}
                                </div>
                                <div className={`h-4 w-4 rounded-full border ${typeColors[notification.type]}`}></div>
                            </div>
                            <div className='mt-4'>
                                <h3 className={`text-lg font-semibold ${typeColors[notification.type]}`}>{notification.type}</h3>
                                <p className='text-gray-500'>{notification.message}</p>
                            </div>
                            <div className='flex justify-between items-center mt-4'>
                                <p className='text-sm text-gray-400'>Date:</p>
                                <p className='text-sm font-semibold'>{notification.date}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Notifications;
