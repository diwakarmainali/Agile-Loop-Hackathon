"use client"
import { useState, useEffect } from "react";
import { FaBell, FaCog, FaListAlt } from 'react-icons/fa';
import { MdDashboard, MdWallet } from "react-icons/md";
import { FaSignOutAlt } from 'react-icons/fa';

const Sidebar = ({ isOpen }) => {
    const [open, setOpen] = useState(isOpen);

    useEffect(() => {
        setOpen(isOpen);
    }, [isOpen]);

    const Menus = [
        { title: "Overview", icon: <MdDashboard /> },
        { title: "Settings", icon: <FaCog /> },
        { title: "Sign Out", icon: <FaSignOutAlt/>, gap: true  },
    ];

    return (
        <div className={`${open ? 'block' : 'hidden'} md:block`}>
            <div className={`${open ? "w-60" : "w-20"} bg-black h-screen p-4 flex flex-col justify-between relative duration-300`}>
                <img
                    src="/images/control.png"
                    className={`absolute cursor-pointer -right-3 top-9 w-7 border-dark-purple
                        border-2 rounded-full ${!open && "rotate-180"}`}
                    onClick={() => setOpen(!open)}
                />
                <ul className="pt-1">
                    {Menus.map((Menu, index) => (
                        <li
                            key={index}
                            className={`flex rounded-md p-2 cursor-pointer hover:bg-light-white text-gray-300 text-sm items-center gap-x-4
                            ${Menu.gap ? "absolute bottom-6" : "mt-2"} ${index === 0 && "bg-light-white"}`}
                        >
                            {Menu.icon}
                            <span className={`${!open && "hidden"} origin-left duration-200`}>
                                {Menu.title}
                            </span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default Sidebar;