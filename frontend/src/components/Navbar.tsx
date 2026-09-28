import React from 'react'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { NavLink } from 'react-router-dom'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className='w-full max-w-5xl mx-auto rounded-xl border border-gray-600 bg-[#0E1428]'>
        <div className='bg-[#0E1428] text-white flex items-center justify-between rounded-xl border border-gray-600 px-4 py-3 shadow-lg'>
          <h1 className='font-extrabold text-green-400'>HACKATHON RAPTX</h1>
          <div className='hidden md:flex justify-center gap-3'>
            <NavLink to='/myteam' className='p-3 hover:text-gray-300 transition'>
              My Team
            </NavLink>
            <NavLink to='/gallery' className='py-3 hover:text-gray-300 transition'>
              Gallery
            </NavLink>
            <NavLink to='/login' className='p-3 hover:text-purple-500 hover:bg-white/10 hover:rounded-2xl transition'>
              Login
            </NavLink>
          </div>
           <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden rounded-lg p-2 hover:bg-white/10 transition">
              {isOpen ? (
                <X size={26} />
              ) : (
                <Menu size={26} />
              )}
            </button>
        </div>

        {isOpen && (
        <div className="md:hidden border-t border-gray-700 px-4 py-3">

          <div className="flex flex-col gap-1">

            <NavLink
              to="/myteam"
              onClick={() => setIsOpen(false)}
              className="rounded-lg px-3 py-3 text-white hover:bg-white/10 transition"
            >
              My Team
            </NavLink>

            <NavLink
              to="/gallery"
              onClick={() => setIsOpen(false)}
              className="rounded-lg px-3 py-3 text-white hover:bg-white/10 transition"
            >
              Gallery
            </NavLink>

            <NavLink
              to="/login"
              onClick={() => setIsOpen(false)}
              className="rounded-lg px-3 py-3 text-white hover:bg-purple-400 transition"
            >
              Login
            </NavLink>

          </div>

        </div>
      )}
    </div>
  )
}

export default Navbar