import React from 'react';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';
import { FaClipboardList, FaClock, FaCheckCircle, FaTruck, FaTimesCircle, FaShoppingCart, FaCar, FaTools, FaTasks } from 'react-icons/fa';

function Orders() {
    const orders = [
        { id: '001', icon: <FaShoppingCart />, status: 'In Progress', type: 'Shop', description: 'Order placed, waiting for processing.', date: '2024-06-01', fee: '$15.00' },
        { id: '002', icon: <FaCar />, status: 'In Progress', type: 'Drive', description: 'Order is being prepared.', date: '2024-06-02', fee: '$20.00' },
        { id: '003', icon: <FaTruck />, status: 'In Progress', type: 'Delivery PickUp', description: 'Order has been shipped.', date: '2024-06-03', fee: '$10.00' },
        { id: '004', icon: <FaCheckCircle />, status: 'Completed', type: 'Handyman', description: 'Order has been delivered.', date: '2024-06-04', fee: '$30.00' },
        { id: '005', icon: <FaTimesCircle />, status: 'Cancelled', type: 'Multiple Tasks', description: 'Order has been cancelled.', date: '2024-06-05', fee: '$0.00' },
    ];

    const statusColors = {
        'Completed': 'text-green-600',
        'In Progress': 'text-yellow-600',
        'Cancelled': 'text-red-600'
    };

    const circleColors = {
        'Completed': 'border-green-600',
        'In Progress': 'border-yellow-600',
        'Cancelled': 'border-red-600'
    };


    const statusIcons = {
        'Completed': <FaCheckCircle />,
        'In Progress': <FaClock />,
        'Cancelled': <FaTimesCircle />
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
                    {orders.map((order, index) => (
                        <div
                            key={index}
                            className='group flex flex-col border border-gray-200 rounded-lg transition-transform transform hover:scale-105 hover:shadow-lg p-4'
                        >
                            <div className='flex justify-between items-center'>
                                <div className={`text-3xl ${statusColors[order.status]}`}>
                                    {statusIcons[order.status]}
                                </div>
                                {/*<div className={`h-4 w-4 rounded-full border-2 ${circleColors[order.status]}`}>
                                
                                </div> */}
                            </div>
                            <div className='mt-4'>
                                <h3 className='text-lg font-semibold'>{order.type}</h3>
                                <p className='text-gray-500'>{order.description}</p>
                            </div>
                            <div className='flex justify-between items-center mt-4'>
                                <p className='text-sm text-gray-400'>Status:</p>
                                <p className={`text-sm font-semibold ${statusColors[order.status]}`}>{order.status}</p>
                            </div>
                            <div className='flex justify-between items-center mt-2'>
                                <p className='text-sm text-gray-400'>Date Placed:</p>
                                <p className='text-sm font-semibold'>{order.date}</p>
                            </div>
                            <div className='flex justify-between items-center mt-2'>
                                <p className='text-sm text-gray-400'>Order Fee:</p>
                                <p className='text-sm font-semibold'>{order.fee}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Orders;
