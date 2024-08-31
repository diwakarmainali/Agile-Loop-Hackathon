import React from 'react'

// function Footer() {
//     return (
//         <footer className="">
//             <div className='flex flex-row md:justify-between'>
//                 <div className='flex w-full p-2 items-center justify-center '>
//                     <img
//                         className=""
//                         alt="Mask group"
//                         src="images/mask-group.svg"
//                     />

//                 </div>
//             </div>
//             <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
//                 <p className="text-center text-gray-400">&copy; 2024 QuixFlow. All rights reserved.</p>
//             </div>
//         </footer>
//     )
// }

// export default Footer

const Footer = () => {
  return (
    <footer className="bg-gray-1000 text-white py-8">
      <div className="container mx-auto px-4 border-t border-gray-700 mt-[100px]">
        <div className="flex flex-wrap justify-between mt-4 p-10">
          <div className="w-full md:w-1/4 mb-6 md:mb-0">
            <h3 className="text-lg font-semibold mb-2">Quixflow</h3>
            <p className="text-sm"> Quixflow supercharges your SaaS productivity using Agile Loop AI.</p>
          </div>
          <div className="w-full md:w-1/4 mb-6 md:mb-0">
            <h3 className="text-lg font-semibold mb-2">Quick Links</h3>
            <ul className="text-sm">
              <li className="mb-2"><a href="#" className="hover:text-gray-300">Home</a></li>
              <li className="mb-2"><a href="#" className="hover:text-gray-300">Pricing</a></li>
              <li className="mb-2"><a href="#" className="hover:text-gray-300">Contact</a></li>
            </ul>
          </div>
          <div className="w-full md:w-1/4 mb-6 md:mb-0">
            <h3 className="text-lg font-semibold mb-2">Contact Us</h3>
            <p className="text-sm">xyz Main Street<br />City, State 12345<br />Phone: (000) 000-0000<br />Email: info@example.com</p>
          </div>
          <div className="w-full md:w-1/4 mb-6 md:mb-0">
            <h3 className="text-lg font-semibold mb-2">Follow Us</h3>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-sm text-center">
          <p>&copy; {new Date().getFullYear()} QuixFlow. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;