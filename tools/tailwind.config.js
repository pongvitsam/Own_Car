/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './mockup/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // One accent family (ink navy): legacy indigo-* and blue-* classes render as the app's navy.
        indigo: {
          50: '#F4F5F8', 100: '#E8EBF1', 200: '#CDD3E0', 300: '#A3ADC4', 400: '#6F7C9C',
          500: '#44527A', 600: '#1E2A4A', 700: '#18223D', 800: '#121A30', 900: '#0D1324', 950: '#090E1B',
        },
        blue: {
          50: '#F4F5F8', 100: '#E8EBF1', 200: '#CDD3E0', 300: '#A3ADC4', 400: '#6F7C9C',
          500: '#44527A', 600: '#1E2A4A', 700: '#18223D', 800: '#121A30', 900: '#0D1324', 950: '#090E1B',
        },
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
