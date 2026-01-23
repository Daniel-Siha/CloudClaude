'use client'

import React from 'react'

interface MenuItem {
  name: string
  description: string
  price: string
}

interface MenuSection {
  title: string
  items: MenuItem[]
  bgColor: string
  animationClass: string
}

const menuData: MenuSection[] = [
  {
    title: 'Klassiekers',
    items: [
      { name: 'Buiten Burger', description: 'Huisgemaakte burger met verse sla, tomaat en speciale saus', price: '€12,50' },
      { name: 'Cheese Deluxe', description: 'Dubbele cheddar, bacon en karamel uien', price: '€14,50' },
      { name: 'Veggie Garden', description: 'Gegrilde groenten burger met avocado', price: '€11,50' },
    ],
    bgColor: 'from-burger-bun to-burger-bunDark',
    animationClass: 'animate-slide-left',
  },
  {
    title: 'Specials',
    items: [
      { name: 'BBQ Beast', description: 'Pulled pork, coleslaw en BBQ saus', price: '€15,50' },
      { name: 'Truffle Dream', description: 'Truffel mayo, brie en rucola', price: '€16,50' },
      { name: 'Spicy Inferno', description: 'Jalapeños, sriracha en pepper jack', price: '€14,00' },
    ],
    bgColor: 'from-burger-meat to-amber-900',
    animationClass: 'animate-slide-right',
  },
  {
    title: 'Sides & Drinks',
    items: [
      { name: 'Loaded Fries', description: 'Friet met kaas, bacon en bieslook', price: '€6,50' },
      { name: 'Onion Rings', description: 'Krokante uienringen met dipsaus', price: '€5,50' },
      { name: 'Craft Limonade', description: 'Huisgemaakte limonade naar keuze', price: '€4,00' },
    ],
    bgColor: 'from-burger-lettuce to-green-800',
    animationClass: 'animate-slide-left-slow',
  },
]

export default function AnimatedBurgerMenuCard() {
  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      {/* Header met logo animatie */}
      <div className="text-center mb-8 animate-float">
        <div className="inline-block relative">
          {/* Burger icon */}
          <div className="w-20 h-20 mx-auto mb-4 relative">
            <div className="absolute w-full h-4 bg-burger-bun rounded-t-full top-0 animate-bounce-slow" style={{ animationDelay: '0ms' }} />
            <div className="absolute w-full h-2 bg-burger-lettuce top-4" style={{ animationDelay: '100ms' }} />
            <div className="absolute w-full h-2 bg-burger-tomato top-6" />
            <div className="absolute w-full h-2 bg-burger-cheese top-8" />
            <div className="absolute w-full h-4 bg-burger-meat rounded-sm top-10" />
            <div className="absolute w-full h-4 bg-burger-bun rounded-b-full top-14 animate-bounce-slow" style={{ animationDelay: '200ms' }} />
          </div>
          <h1 className="text-4xl font-bold text-burger-bunDark tracking-wide">
            Burger Buiten
          </h1>
          <p className="text-burger-meat mt-2 text-lg italic">Verse smaken, buiten genieten</p>
        </div>
      </div>

      {/* Menu kaart met 3 horizontale secties */}
      <div className="rounded-2xl overflow-hidden shadow-2xl animate-pulse-glow">
        {menuData.map((section, sectionIndex) => (
          <div
            key={section.title}
            className={`
              bg-gradient-to-r ${section.bgColor}
              p-6
              ${sectionIndex !== menuData.length - 1 ? 'border-b-4 border-white/20' : ''}
              ${section.animationClass}
            `}
          >
            {/* Section header */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white drop-shadow-lg">
                {section.title}
              </h2>
              <div className="flex gap-1">
                {[...Array(3)].map((_, i) => (
                  <span
                    key={i}
                    className="w-2 h-2 bg-white/60 rounded-full animate-pulse"
                    style={{ animationDelay: `${i * 200}ms` }}
                  />
                ))}
              </div>
            </div>

            {/* Menu items */}
            <div className="space-y-3">
              {section.items.map((item, itemIndex) => (
                <div
                  key={item.name}
                  className="
                    bg-white/10 backdrop-blur-sm rounded-lg p-4
                    hover:bg-white/20 transition-all duration-300
                    hover:scale-[1.02] cursor-pointer
                    border border-white/10
                  "
                  style={{ animationDelay: `${itemIndex * 100}ms` }}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white">
                        {item.name}
                      </h3>
                      <p className="text-white/80 text-sm mt-1">
                        {item.description}
                      </p>
                    </div>
                    <span className="text-xl font-bold text-white ml-4 whitespace-nowrap">
                      {item.price}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="text-center mt-6 text-burger-meat/70 text-sm animate-pulse">
        <p>Alle burgers worden geserveerd met friet</p>
        <p className="mt-1">Allergenen? Vraag onze medewerkers!</p>
      </div>
    </div>
  )
}
