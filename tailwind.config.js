/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#1a365d',
          700: '#152a4a',
          800: '#0f1f38',
          900: '#0a1628',
        },
        accent: {
          400: '#d4a90a',
          500: '#b7940a',
          600: '#9a7c08',
        },
        burger: {
          bun: '#F4A460',
          bunDark: '#CD853F',
          meat: '#8B4513',
          lettuce: '#228B22',
          tomato: '#DC143C',
          cheese: '#FFD700',
          onion: '#DDA0DD',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'slide-left': 'slideLeft 3s ease-in-out infinite',
        'slide-right': 'slideRight 3s ease-in-out infinite',
        'slide-left-slow': 'slideLeft 4s ease-in-out infinite',
        'bounce-slow': 'bounce 2s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        slideLeft: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(-10px)' },
        },
        slideRight: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(10px)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 5px rgba(244, 164, 96, 0.5)' },
          '50%': { boxShadow: '0 0 20px rgba(244, 164, 96, 0.8), 0 0 30px rgba(244, 164, 96, 0.4)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
      },
    },
  },
  plugins: [],
}
