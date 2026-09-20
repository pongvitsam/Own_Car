/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './mockup/**/*.html',
  ],
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      colors: {
        premium: {
          blue: '#2563EB',
          light: '#F7F8FA',
          ink: '#1A1D24',
          elevated: '#FFFFFF',
        },
      },
      fontFamily: {
        sans: ['Sarabun', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      boxShadow: {
        premium: '0 2px 8px rgba(26, 29, 36, 0.06)',
        'premium-lg': '0 12px 40px rgba(26, 29, 36, 0.1)',
        'premium-glow': '0 0 0 2px rgba(37, 99, 235, 0.25), 0 4px 16px rgba(37, 99, 235, 0.15)',
      },
    },
    screens: {
      xs: '400px',
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
  },
};
